# Дерево под-целей: таблица индикаторов и обзор

**Корень:** таблица `paper/indicators_table.md` (25 индикаторов) и обзор
`paper/review_soil_health_indicators.md` (15 источников) согласованы между
собой, с графом `notes/` и с PDF в `paper/`.

**Постановку проверил автор:** да, 02.11.2026.

| id | под-цель | родитель | вид | верификатор | команда | статус |
|---|---|---|---|---|---|---|
| G0 | таблица и обзор согласованы | — | — | `run_verifier.py` | `python scripts/run_verifier.py` → 4 pass | закрыта |
| G1 | схема таблицы (Д1–Д8) | G0 | горизонталь | `check.py` | `python checks/check.py` → 0 | закрыта |
| G2 | файловые свойства (6) | G0 | горизонталь | `pytest` | `pytest checks/test_properties.py -q` → 6 passed | закрыта |
| G3 | граф `notes/` согласован | G0 | горизонталь | `check_graph.py` | `python checks/check_graph.py` → 0 | закрыта |
| G4 | число источников `.md = .tex` | G2 | вертикаль | `test_md_and_tex_literature_match` | `pytest checks -q` → 6 passed | закрыта |
| G5 | каждое свойство падает на испорченной копии | G2 | вертикаль | ветка `bug/source-page-typo` | `git switch bug/... && pytest` → 1 failed | закрыта |
| G6 | 5 свойств с `@given` | G0 | горизонталь | `test_properties_hypothesis.py` | `pytest checks/test_properties_hypothesis.py -q` → 11 passed | закрыта |
| G7 | утверждения обзора верны | G0 | горизонталь | `verify_claims.py` + человек | `python checks/verify_claims.py` + 2–3 DOI вручную | в работе |
