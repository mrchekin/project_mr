#!/usr/bin/env python3
"""Проверка технической готовности обзора.

Код 0 - технически готово к следующей проверке (verify_claims.py или человек).
Код 1 - технические дефекты, агенту нужно исправить.

Приемка после verify_claims.py / ручной сверки
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT / "paper" / "review_soil_health_indicators.md"
TABLE = ROOT / "paper" / "indicators_table.md"

EXPECTED_COLUMNS = [
    "indicator", "category", "method",
    "sensitivity", "source_file", "source_page",
]

VALID_CATEGORY = {"chemical", "physical", "biological",
                  "microbial", "labile carbon"}
VALID_SENSITIVITY = {"low", "medium", "high", "medium-high"}

PLACEHOLDER_MARKERS = {"test", "todo", "tbd", "n/a", "na",
                       "placeholder", "xxx", "??", "?"}

# смысловые разделы обзора #
# группа допустимых подстрок: раздел считается найденным,
# если в его заголовке есть хотя бы одна из них
# так «синтез» засчитывается как «сравнение», а «ограничения» - как «пробелы»
REQUIRED_SECTIONS = [
    ["введ"],                          # введение
    ["индикатор"],                     # основная часть: группы индикаторов
    ["синтез", "сравн", "метод"],      # сравнение / синтез / методы
    ["ограничен", "пробел"],           # ограничения / пробелы
    ["заключ"],                        # заключение
    ["литерат"],                       # литература
]

VALID_SOURCE_EXTS = {".pdf", ".md", ".txt"}


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def ok(msg):
    print(f"OK: {msg}")


def check_review():
    if not REVIEW.exists():
        fail(f"нет файла {REVIEW.relative_to(ROOT)}")

    text = REVIEW.read_text(encoding="utf-8")
    headings = [ln.strip() for ln in text.splitlines()
                if ln.startswith("## ") and not ln.startswith("### ")]
    if len(headings) < 7:
        fail(f"в {REVIEW.name} только {len(headings)} разделов (## ), "
             f"нужно >= 7")

    missing = []
    for group in REQUIRED_SECTIONS:
        if not any(any(sub in h.lower() for sub in group) for h in headings):
            missing.append(group[0])
    if missing:
        fail(f"в {REVIEW.name} нет обязательных разделов: {missing}")

    ok(f"{REVIEW.name}: {len(headings)} разделов, все обязательные на месте")

def is_placeholder(s):
    s = s.strip().lower()
    if not s:
        return True
    if s in PLACEHOLDER_MARKERS:
        return True
    if re.fullmatch(r"(.)\1{2,}", s):
        return True
    return False

def check_table():
    if not TABLE.exists():
        fail(f"нет файла {TABLE.relative_to(ROOT)}")
    lines = [ln for ln in TABLE.read_text(encoding="utf-8").splitlines()
             if ln.strip()]
    sep_idx = None
    for i, ln in enumerate(lines):
        if "---" in ln and "|" in ln:
            sep_idx = i
            break
    if sep_idx is None or sep_idx == 0:
        fail(f"в {TABLE.name} не найдена markdown-таблица")

    header = [c.strip() for c in lines[sep_idx - 1].strip("|").split("|")]
    missing = [c for c in EXPECTED_COLUMNS if c not in header]
    if missing:
        fail(f"в таблице нет столбцов: {missing}; есть: {header}")

    rows = [ln for ln in lines[sep_idx + 1:] if ln.strip().startswith("|")]
    if len(rows) < 10:
        fail(f"в таблице {len(rows)} строк данных, нужно >= 10")

    idx = {c: header.index(c) for c in EXPECTED_COLUMNS}
    paper_dir = ROOT / "paper"
    seen = {}
    errors = []

    for n, row in enumerate(rows, 1):
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < len(EXPECTED_COLUMNS):
            errors.append(f"строка {n}: мало ячеек ({len(cells)})")
            continue

        ind = cells[idx["indicator"]]
        cat = cells[idx["category"]].lower()
        method = cells[idx["method"]]
        sens = cells[idx["sensitivity"]].lower()
        src = cells[idx["source_file"]]
        page = cells[idx["source_page"]]

        for name, v in [("indicator", ind), ("method", method)]:
            if is_placeholder(v):
                errors.append(f"строка {n}: {name}={v!r} — заглушка")

        if cat not in VALID_CATEGORY:
            errors.append(f"строка {n}: category={cat!r} не из "
                          f"{sorted(VALID_CATEGORY)}")

        if sens not in VALID_SENSITIVITY:
            errors.append(f"строка {n}: sensitivity={sens!r} не из "
                          f"{sorted(VALID_SENSITIVITY)}")

        key = ind.lower().strip()
        if key in seen:
            errors.append(f"строка {n}: индикатор {ind!r} дублирует "
                          f"строку {seen[key]}")
        else:
            seen[key] = n

        src_path = paper_dir / src
        if not src_path.exists():
            errors.append(f"строка {n}: source_file={src!r} не найден")
        elif src_path.suffix.lower() not in VALID_SOURCE_EXTS:
            errors.append(f"строка {n}: {src!r} — не PDF/MD/TXT")

        if src_path.suffix.lower() == ".pdf":
            if not re.fullmatch(r"\d+", page):
                errors.append(f"строка {n}: source_page={page!r} "
                              f"— для PDF нужно целое число")
            elif not (1 <= int(page) <= 999):
                errors.append(f"строка {n}: source_page={page} вне 1..999")
        else:
            if is_placeholder(page):
                errors.append(f"строка {n}: source_page={page!r} - заглушка")

    if errors:
        print("FAIL:")
        for e in errors[:20]:
            print(f"  - {e}")
        if len(errors) > 20:
            print(f"  ... ещё {len(errors) - 20}")
        sys.exit(1)

    ok(f"{TABLE.name}: {len(rows)} строк, все поля валидны, "
       f"индикаторы уникальны")


def main():
    check_review()
    check_table()
    print()
    print("ТЕХНИЧЕСКИ ГОТОВО К ПРОВЕРКЕ.")
    print("Следующий шаг: python checks/verify_claims.py (или ручная "
          "сверка 3–5 тезисов).")
    print("Статус «принята» ставит только человек после проверки.")


if __name__ == "__main__":
    main()
