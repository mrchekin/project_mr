#!/usr/bin/env python3
"""Проверка графа: заметки индикаторов и провенанс источников.

Договор (METHOD.md §3):
  Д9.1 Каждый notes/Индикатор-*.md соответствует строке таблицы.
  Д9.2 Хотя бы 5 индикаторов таблицы имеют заметки.
  Д10  У каждого notes/Источник-*.md есть найденЗапросом.

Код 0 — принято, 1 — есть нарушения.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "paper" / "indicators_table.md"
NOTES = ROOT / "notes"
MIN_COVERAGE = 5

HEADER = ["indicator", "category", "method",
          "sensitivity", "source_file", "source_page"]


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def ok(msg):
    print(f"OK: {msg}")


def read_indicators():
    lines = [ln for ln in TABLE.read_text(encoding="utf-8").splitlines()
             if ln.strip()]
    sep = next(i for i, ln in enumerate(lines)
               if "---" in ln and "|" in ln)
    header = [c.strip() for c in lines[sep - 1].strip("|").split("|")]
    if header != HEADER:
        fail(f"столбцы не совпадают с договором: {header}")
    rows = [ln for ln in lines[sep + 1:] if ln.strip().startswith("|")]
    return [r.strip("|").split("|")[0].strip() for r in rows]


def read_notes_types():
    out = {}
    for f in NOTES.glob("*.md"):
        m = re.search(r"^type:\s*(\S+)\s*$",
                      f.read_text(encoding="utf-8"), re.M)
        if m:
            out.setdefault(m.group(1), []).append(f)
    return out


def note_indicator_name(path):
    return path.stem.replace("Индикатор-", "", 1).strip()


def short_code(name):
    """Короткий код: до первого пробела, скобки или дефиса.

    'LAP (leucine aminopeptidase)' → 'lap'
    'SOC content'                  → 'soc'
    'pH'                           → 'ph'
    """
    return re.split(r"[\s(\-]", name.strip().lower(), maxsplit=1)[0]


def main():
    if not TABLE.exists():
        fail(f"нет файла {TABLE}")
    if not NOTES.exists():
        fail(f"нет папки {NOTES}")

    indicators = read_indicators()
    types = read_notes_types()

    # Д9.1
    indicator_notes = types.get("Индикатор", [])
    table_full = [i.strip().lower() for i in indicators]
    table_codes = {short_code(i) for i in indicators}

    orphans = []
    for f in indicator_notes:
        name = note_indicator_name(f).lower()
        code = short_code(name)
        if code in table_codes:
            continue
        if any(name in full or full.startswith(name + " ")
               for full in table_full):
            continue
        orphans.append(f.stem)
    if orphans:
        fail(f"заметки без строки в таблице: {orphans}")

    # Д9.2
    covered = {note_indicator_name(f).lower() for f in indicator_notes}
    if len(covered) < MIN_COVERAGE:
        fail(f"заметок только {len(covered)}, нужно >= {MIN_COVERAGE}")

    # Д10
    sources = types.get("Источник", [])
    no_prov = [f.stem for f in sources
               if "найденЗапросом" not in f.read_text(encoding="utf-8")]
    if no_prov:
        fail(f"у источников нет провенанса: {no_prov}")

    ok(f"граф: {len(indicator_notes)} заметок индикаторов "
       f"(из {len(indicators)} строк), {len(sources)} источников "
       f"с провенансом")


if __name__ == "__main__":
    main()
