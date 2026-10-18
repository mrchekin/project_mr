#!/usr/bin/env python3
"""Проверка результата обзора индикаторов здоровья почвы.

Код 0 — результат принят.
Код 1 — что-то не так, см. сообщение.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT / "paper" / "review_soil_health_indicators.md"
TABLE = ROOT / "paper" / "indicators_table.md"

EXPECTED_COLUMNS = [
    "indicator", "category", "method",
    "sensitivity", "source_file", "source_page",
]


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def ok(msg):
    print(f"OK: {msg}")


def check_review():
    if not REVIEW.exists():
        fail(f"нет файла {REVIEW.relative_to(ROOT)}")

    text = REVIEW.read_text(encoding="utf-8")
    headings = [ln for ln in text.splitlines() if ln.startswith("#")]
    if len(headings) < 7:
        fail(f"в {REVIEW.name} только {len(headings)} заголовков, нужно >= 7")

    ok(f"{REVIEW.name}: {len(headings)} заголовков")


def check_table():
    if not TABLE.exists():
        fail(f"нет файла {TABLE.relative_to(ROOT)}")

    lines = [ln for ln in TABLE.read_text(encoding="utf-8").splitlines() if ln.strip()]
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
    for n, row in enumerate(rows, 1):
        cells = [c.strip() for c in row.strip("|").split("|")]
        src = cells[idx["source_file"]]
        if not (paper_dir / src).exists():
            fail(f"строка {n}: source_file={src!r} не найден в paper/")

    ok(f"{TABLE.name}: {len(rows)} строк, все source_file существуют")


def main():
    check_review()
    check_table()
    print("Проверка пройдена.")


if __name__ == "__main__":
    main()
