# Отчёт по домашней работе 2 «Проверка»: таблица индикаторов здоровья почвы

| Поле | Значение |
|---|---|
| Направление | вычислительное |
| Вариант верификатора | проверка данных + тесты на свойствах (hypothesis) |
| Репозиторий | https://github.com/mrchekin/project_mr |
| Метка git | `hw2` |
| Команда запуска | `python scripts/run_verifier.py` |

## 1. Задача и место верификатора

[написано] Таблица `paper/indicators_table.md` — 25 индикаторов здоровья почвы — основа сводного раздела обзора `paper/review_soil_health_indicators.md` (15 источников) и отчёта `reports/indicators_summary.md`. Ошибка в таблице (несуществующий `source_file`, дубликат индикатора, невалидный `source_page`, категория или sensitivity вне шкалы) переносится в обзор и в отчёт без предупреждения. Верификатор ловит такие ошибки до публикации. Второй уровень — свойства функций таблицы через hypothesis: если функция перестаёт сохранять инвариант, тест падает.

## 2. Методика

См. `METHOD.md`, §0–10. Методика записана и закоммичена **27.10.2026** (коммит `c34c5ee`) — до первого прогона верификатора. Правило принятия (§7 `METHOD.md`): `python checks/check.py` → 0, `pytest checks -q` → все тесты проходят, `check_graph.py` → 0, «до/после» пойманной ошибки сохранены.

## 3. Верификатор

- **Что проверяет:** договор о схеме таблицы (Д1–Д8), договор о графе (Д9–Д10), 6 файловых свойств, 5 свойств через hypothesis.
- **Как устроен:** `checks/check.py`, `checks/check_graph.py`, `checks/test_properties.py` (6 тестов), `checks/test_properties_hypothesis.py` (5 свойств + 5 проверок), `scripts/run_verifier.py` (4 шага).
- **Чего не проверяет:** научную корректность `sensitivity`, соответствие `source_page` реальной странице PDF, полноту покрытия заметками (5 из 25).

### 3.1. Файловые свойства (`checks/test_properties.py`, 6)

| № | Свойство | Тест |
|---|---|---|
| 1 | в каждой категории хотя бы одна строка | `test_every_category_has_row` |
| 2 | каждый `source_file` существует в `paper/` | `test_every_source_file_exists` |
| 3 | длина `indicator` ≥ 2, кроме вайтлиста | `test_indicator_names_reasonable` |
| 4 | `sensitivity` из шкалы | `test_sensitivity_whitelist` |
| 5 | индикаторы без дубликатов | `test_indicator_unique` |
| 6 | для `.pdf` `source_page` — целое 1..999 | `test_source_page_integer_for_pdf` |

### 3.2. Свойства через hypothesis (`checks/test_properties_hypothesis.py`, 5)

| № | Свойство | Функция | Тест |
|---|---|---|---|
| 1 | сохранение: сумма по категориям = длина | `count_by_category` | `test_count_preserves_total` |
| 2 | монотонность sensitivity | `sort_by_sensitivity` | `test_sensitivity_order_is_monotone` |
| 3 | согласованность фильтра | `filter_by_sensitivity` | `test_filter_returns_consistent_subset` |
| 4 | идемпотентность sort / normalize | `sort_by_indicator`, `normalize_whitespace` | `test_sort_is_idempotent`, `test_whitespace_normalization_is_idempotent` |
| 5 | границы: category/sensitivity в валидных множествах | — | `test_fields_are_within_valid_sets` |

## 4. Декомпозиция проверки

Дерево под-целей — в `SUBGOALS.md` (8 под-целей, `G0–G7`).
Корень: таблица `paper/indicators_table.md` (25 индикаторов) и обзор
`paper/review_soil_health_indicators.md` (15 источников) согласованы между
собой, с графом `notes/` и с PDF в `paper/`; проверка воспроизводится
командой `python scripts/run_verifier.py` (4 pass).

```
G0: таблица и обзор согласованы, проверка воспроизводима
├── G1: схема таблицы (Д1–Д8)             — checks/check.py           → 0
├── G2: свойства таблицы (6 + 5)           — pytest checks -q          → 17 passed
│   ├── G4: число источников .md = .tex    — test_md_and_tex_literature_match
│   │                                                                → 6 passed
│   ├── G5: свойства падают на испорченной — ветка bug/source-page-typo
│   │                                                                → 1 failed
│   └── G6: 5 свойств с @given             — checks/test_properties_hypothesis.py
│                                                                    → 11 passed
├── G3: граф notes/ согласован             — checks/check_graph.py    → 0
└── G7: утверждения обзора верны           — checks/verify_claims.py
                                              + 2–3 тезиса вручную  → отчёт
```

Каждая под-цель закрыта своим верификатором с командой, которая
различает правильный и неправильный результат (см. таблицу в `SUBGOALS.md`).

Журнал попыток — `ATTEMPTS.md` (14 строк). Правило трёх попыток
применено дважды:

- **G1** (схема таблицы): после двух неудач (строки 1–2) — первая версия
  `is_placeholder` считала `pH` и `EC` заглушками по длине, — план
  сменился: эвристика «длина ≤ 2» убрана, добавлена проверка на повторы
  символов (`(.)\1{2,}`). Строка 3 в журнале.
- **G6** (5 свойств с `@given`): после отказа `_broken_idem` (строка 12)
  — первая версия добавляла суффикс к ключу сортировки, функция осталась
  идемпотентной, hypothesis выдал `NoSuchExample`, — predicate
  переформулирован: суффикс добавляется к самому `indicator`
  (строка 13). Не повторял тот же predicate трижды.

Под-цели G0–G6 закрыты. G7 (сверка утверждений обзора) — в работе:
`verify_claims.py` создаёт отчёт со случайной выборкой тезисов, 2–3
тезиса сверяются человеком по PDF.

## 5. Результаты прогона

### 5.1. Шаги глубины (детерминированный расчёт, повторы не применимы)

| Шаг | Команда | Время | Код | Условие перехода |
|---|---|---|---|---|
| dry | `python checks/check.py` | 0,02 с | 0 | схема таблицы валидна |
| smoke | `pytest checks/test_properties.py -q` | 0,24 с | 0 (6 passed) | файловые свойства проходят |
| sweep | `pytest checks -q` | 0,26 с | 0 (17 passed) | все тесты проходят |
| full | `python checks/check_graph.py` | 0,02 с | 0 | граф согласован |

Журнал прогонов: `results/verifier_log.csv` (4 строки `pass`).

### 5.2. Свойства через hypothesis (направление B)

`checks/test_properties_hypothesis.py` — 5 свойств + 5 проверок «свойство
способно упасть» = **11 passed**.

На испорченной копии `_broken_count` (без `labile carbon`) свойство 1
падает, hypothesis печатает наименьший контрпример:
`rows=[{'category': 'labile carbon', ...}]`.
Файл: `results/hypothesis_caught_before.txt`.

### 5.3. Сводка

- `pytest checks -q`: **17 passed** (6 файловых + 11 hypothesis).
- `python scripts/run_verifier.py`: **4 pass**, код 0.
- Пойманные ошибки: **2** (обе внесены нарочно, обе воспроизводятся).

## 6. Пойманная ошибка

| Что было не так | Тип | Чем поймано | «до» | «после» |
|---|---|---|---|---|
| `source_page` заменён на `abc` в строке SOC content | внесённая | `check.py` (Д6) + `test_source_page_integer_for_pdf` | `results/caught_error_before.txt` (1 failed) | `results/caught_error_after.txt` (passed) |
| `count_by_category` не учитывает `labile carbon` | внесённая | hypothesis: `test_count_preserves_total` | `results/hypothesis_caught_before.txt` (1 failed, минимальный контрпример) | `results/hypothesis_caught_after.txt` (11 passed) |

Воспроизведение «до»:

```bash
git switch bug/source-page-typo && python -m pytest checks -q     # 1 failed
git switch main && python -m pytest checks -q                     # 17 passed

## 7. Воспроизведение

git clone https://github.com/mrchekin/project_mr && cd project_mr
git checkout hw2
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_verifier.py

## 8. Ограничения

### Что верификатор не проверяет

- **Научную корректность** значений `sensitivity` в таблице. Значения
  `low/medium/high/medium-high` — качественная оценка из источников;
  совпадает ли она с реальной чувствительностью индикатора к управлению,
  проверяет только человек, читая PDF.
- **Соответствие `source_page` реальной странице PDF.** `check.py`
  проверяет только, что это целое число 1..999. Совпадает ли номер с
  местом, где действительно приведено утверждение, — задача
  `checks/verify_claims.py` и ручной сверки 2–3 тезисов.
- **Содержание заметок в `notes/`.** `check_graph.py` проверяет наличие
  заметки индикатора и провенанса источника (`найденЗапросом`), но не
  правильность текста в заметке.
- **Полноту покрытия заметками.** Сейчас заметки есть у 5 из 25
  индикаторов таблицы. Договор `check_graph.py` требует ≥5 — это
  осознанно, полное покрытие 25/25 запланировано к неделе 9.
- **Научные утверждения обзора.** `verify_claims.py` выбирает случайные
  тезисы со ссылками; правильность выбранных утверждений проверяет
  человек. Даже если все 5 тезисов подтверждены, это не доказывает
  обзор целиком — проверка выборочная.

### Где вывод может быть неверным

- Если в таблице есть ошибка, которую не ловит ни одно свойство:
  например, `sensitivity` указан из шкалы, но не соответствует источнику —
  проверка пройдёт. Это ограничение любого верификатора: он проверяет
  только записанное правило.
- Если в `paper/` появился новый PDF не по теме обзора, `check.py`
  пройдёт (все `source_file` существуют), но таблица может ссылаться на
  источник, которого нет в списке литературы. Такую несогласованность
  ловит только ручная сверка.
- Если `notes/Источник-*.md` содержит корректный провенанс, но неверную
  аннотацию, `check_graph.py` пройдёт. Содержание аннотации — вне
  проверки.

### Что осталось непроверенным и почему

- **25/25 индикаторов с заметками.** Не сделано из-за бюджета времени;
  договор `check_graph.py` требует ≥5, а не 25 — чтобы не блокировать
  работу, пока идёт наполнение.
- **Полная сверка утверждений обзора.** `verify_claims.py` выбирает 5
  тезисов; остальные не сверены. Полная сверка требует чтения всех 15
  PDF человеком — это вне бюджета ДЗ 2.
- **Формализация (Lean, направление A).** Не применима: в задаче нет
  формализуемого ядра. Обзор литературы и таблица индикаторов не
  записываются как теорема в Lean — это качественный текст и данные, а не
  математическое утверждение с точной формулировкой.
- **Глобальная согласованность графа.** `check_graph.py` проверяет
  локальные связи (у каждой заметки есть тип, у каждого источника —
  провенанс), но не проверяет, что граф в целом образует связный
  компонент без «сиротских» узлов. Это могло бы стать под-целью G8, но
  не входит в текущий минимум. 
  
  
  
  
  
  
## 9. Использование ИИ-ассистентов

| Фрагмент или файл | Пометка | Инструмент или модель | Чем проверено |
|---|---|---|---|
| `checks/check.py` (Д1–Д8) | `[написано]` | — | `pytest` 6 passed, `check.py` → 0 |
| `checks/check_graph.py` | `[написано]` | — | `check_graph.py` → 0 |
| `checks/test_properties.py` | `[написано]` | — | `pytest` 6 passed |
| `checks/test_properties_hypothesis.py` | `[написано]` | — | `pytest` 11 passed |
| `checks/verify_claims.py` | `[порождено]` | AI4Science (deepseek-v4-flash) | отчёт `reports/spot_check_*.md`, 2–3 тезиса сверены вручную |
| `scripts/run_verifier.py` | `[написано]` | — | 4 pass в `results/verifier_log.csv` |
| `scripts/table_ops.py` | `[написано]` | — | используется в hypothesis-тестах |
| `METHOD.md` | `[написано]` | — | коммит `c34c5ee` до первого прогона |
| `SUBGOALS.md` | `[написано]` | — | — |
| `ATTEMPTS.md` | `[написано]` | — | — |
| `paper/review_soil_health_indicators.md` (15 источников) | `[порождено]` | AI4Science | `check.py` → 0, `pytest` 6 passed, 3 ссылки сверены с PDF вручную |
| `notes/Источник-{Rinot,Bagnall,Karlen,Bastida,Wolejko}*.md` | `[порождено]` | AI4Science | метаданные сверены с 1-й страницей PDF |
| `reports/hw2_report.md` §1–9 | `[написано]` | — | — |

Верификатор написан вручную. Агент участвовал в `verify_claims.py`
(генерация выборки тезисов) и в расширении обзора (5 источников).
Каждое утверждение агента проверено: `check.py`, `pytest`,
`check_graph.py`, ручная сверка 2–3 ссылок с PDF.