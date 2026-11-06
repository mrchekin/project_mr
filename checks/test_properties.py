"""Свойства таблицы индикаторов (не менее пяти)."""
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "paper" / "indicators_table.md"
REVIEW = ROOT / "paper" / "review_soil_health_indicators.md"
TEX = ROOT / "paper" / "review_soil_health_indicators.tex"

HEADER = ["indicator", "category", "method",
          "sensitivity", "sensitivity_target",
          "source_file", "source_page"]
VALID_TARGET = {"tillage", "organic_input", "crop_diversity",
                "land_use_change", "general"}
VALID_CATEGORY = {"chemical", "physical", "biological",
                  "labile carbon"}
VALID_SENS = {"low", "medium", "high", "medium-high"}
SHORT_OK = {"pH", "EC", "C", "N", "P", "K",
            "Fe", "Zn", "Mn", "Cu", "Mo", "B", "Se"}


def load_rows():
    lines = [ln for ln in TABLE.read_text(encoding="utf-8").splitlines()
             if ln.strip()]
    sep = next(i for i, ln in enumerate(lines)
               if "---" in ln and "|" in ln)
    header = [c.strip() for c in lines[sep - 1].strip("|").split("|")]
    assert header == HEADER, f"столбцы: {header}"
    rows = []
    for ln in lines[sep + 1:]:
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        rows.append(dict(zip(HEADER, cells)))
    return rows


@pytest.fixture(scope="module")
def rows():
    return load_rows()


def test_every_category_has_row(rows):
    """Свойство 1: в каждой категории хотя бы 1 строка."""
    cats = {r["category"].lower() for r in rows}
    assert cats == VALID_CATEGORY, \
        f"категории: есть {cats}, ожидается {VALID_CATEGORY}"


def test_every_source_file_exists(rows):
    """Свойство 2: каждый source_file существует в paper/."""
    paper = ROOT / "paper"
    for r in rows:
        p = paper / r["source_file"]
        assert p.exists(), f"нет {r['source_file']} ({r['indicator']})"


def test_indicator_names_reasonable(rows):
    """Свойство 3: длина >= 2, кроме вайтлиста химии."""
    for r in rows:
        name = r["indicator"].strip()
        if name in SHORT_OK:
            continue
        assert len(name) >= 2, f"короткий индикатор: {name!r}"


def test_sensitivity_whitelist(rows):
    """Свойство 4: все значения sensitivity из шкалы."""
    for r in rows:
        s = r["sensitivity"].lower()
        assert s in VALID_SENS, \
            f"{r['indicator']}: sensitivity={s!r} не из {VALID_SENS}"


def test_indicator_unique(rows):
    """Свойство 5: нет дубликатов (без учёта регистра)."""
    names = [r["indicator"].lower() for r in rows]
    assert len(names) == len(set(names)), \
        f"дубликаты: {[n for n in set(names) if names.count(n) > 1]}"


def test_md_and_tex_literature_match():
    """Свойство 6: число источников в .md и .tex совпадает."""
    md = REVIEW.read_text(encoding="utf-8")
    tex = TEX.read_text(encoding="utf-8")

    md_split = md.split("## Литература", 1)
    assert len(md_split) == 2, "в .md нет раздела «## Литература»"
    md_count = len(re.findall(r"^\d+\.", md_split[1], re.M))
    tex_count = len(re.findall(r"\\bibitem\{", tex))

    assert md_count == tex_count, (
        f"Литература .md ({md_count}) и .tex ({tex_count}) не совпадают"
    )


def test_sensitivity_target_whitelist(rows):
    """Свойство 7: sensitivity_target из whitelist."""
    for r in rows:
        t = r["sensitivity_target"].strip().lower()
        assert t in VALID_TARGET, \
            f"{r['indicator']}: sensitivity_target={t!r} не из {VALID_TARGET}"
