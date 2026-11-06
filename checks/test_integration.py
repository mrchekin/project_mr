"""Интеграционные тесты: связывают артефакты, не проверяют функции."""
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TABLE = ROOT / "paper" / "indicators_table.md"
REVIEW = ROOT / "paper" / "review_soil_health_indicators.md"
TEX = ROOT / "paper" / "review_soil_health_indicators.tex"
PDF = ROOT / "paper" / "review_soil_health_indicators.pdf"
NOTES = ROOT / "notes"


def read_indicators():
    lines = [ln for ln in TABLE.read_text(encoding="utf-8").splitlines()
             if ln.strip()]
    sep = next(i for i, ln in enumerate(lines) if "---" in ln and "|" in ln)
    header = [c.strip() for c in lines[sep - 1].strip("|").split("|")]
    rows = []
    for ln in lines[sep + 1:]:
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        rows.append(dict(zip(header, cells)))
    return rows


def test_check_graph_passes():
    """check_graph.py → 0 (через subprocess, не pytest)."""
    r = subprocess.run([sys.executable, "checks/check_graph.py"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, f"check_graph упал: {r.stdout}\n{r.stderr}"


def test_review_has_summary_table():
    """В обзоре есть раздел «Сводная таблица» с markdown-таблицей ≥10 строк."""
    text = REVIEW.read_text(encoding="utf-8")
    # ищем раздел со «Сводная таблица» или «summary table»
    m = re.search(r"##[^\n]*(?:Сводная таблица|Summary table)",
                  text, re.IGNORECASE)
    assert m, "в обзоре нет раздела «Сводная таблица»"

    # от раздела до следующего ## — блок
    start = m.end()
    nxt = re.search(r"\n## ", text[start:])
    block = text[start:start + nxt.start()] if nxt else text[start:]

    # markdown-таблица: строки с |
    rows = [ln for ln in block.splitlines()
            if ln.strip().startswith("|") and "---" not in ln]
    # минус шапка = данные
    data_rows = max(0, len(rows) - 1)
    assert data_rows >= 10, (
        f"в сводной таблице обзора {data_rows} строк данных, нужно ≥10"
    )


def test_review_mentions_normalized_indicators():
    """Хотя бы 5 индикаторов из таблицы упомянуты в обзоре
    по первому слову/аббревиатуре (сокращения допускаются).

    «SOC content» → «soc», «microbial biomass C» → «microbial»,
    «aggregate stability» → «aggregate», «STN (total nitrogen)» → «stn».
    """
    def norm(name):
        # первое слово или аббревиатура до скобки/пробела
        s = name.strip().lower()
        s = re.split(r"[\s(]", s, maxsplit=1)[0]
        # убираем хвостовые знаки
        return re.sub(r"[^a-zа-я0-9]", "", s)

    indicators = [r["indicator"].strip() for r in read_indicators()]
    text = REVIEW.read_text(encoding="utf-8").lower()

    mentioned = [ind for ind in indicators if norm(ind) and norm(ind) in text]
    assert len(mentioned) >= 5, (
        f"в обзоре упомянуты {len(mentioned)} индикаторов из "
        f"{len(indicators)} (по нормализованному имени). Нужно ≥5. "
        f"Не найдены: {[i for i in indicators if norm(i) not in text][:10]}"
    )


def test_indicators_table_size():
    """В таблице ровно 25 строк — столько же, сколько заявлено в §5 обзора."""
    indicators = read_indicators()
    assert len(indicators) == 25, (
        f"в indicators_table.md {len(indicators)} строк, в обзоре §5 "
        f"заявлено 25 — синхронизируйте"
    )


def test_graph_connects_each_source_with_pdf():
    """У каждого Источник-*.md с pdf: paper/… есть ребро к Обзору."""
    sources = []
    for f in NOTES.glob("Источник-*.md"):
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^pdf:\s*paper/(\S+)$", text, re.M)
        if m and (ROOT / "paper" / m.group(1)).exists():
            sources.append((f.name, text))
    assert sources, "не найдено Источник-* с pdf: paper/…"
    bad = [name for name, text in sources if "Обзор индикаторов" not in text]
    assert not bad, f"у {len(bad)} источников нет связи с Обзором: {bad[:10]}"


def test_pdf_is_newer_than_tex():
    """Если PDF есть, он не старше .tex."""
    if not PDF.exists():
        pytest.skip("PDF отсутствует")
    if not TEX.exists():
        pytest.skip(".tex отсутствует")
    assert PDF.stat().st_mtime >= TEX.stat().st_mtime, \
        "PDF старше .tex — пересоберите pdflatex"
