---
type: Задача
status: принята
---

# Добавить Kuzyakov 2010 в обзор

## Запрос пользователя
Найти в paper/ 1 статью Kuzyakov и добавить основные мысли из неё в обзор.

## Готово, когда
- В `paper/review_soil_health_indicators.md` добавлен абзац (до 6 предложений) с основной мыслью Kuzyakov 2010.
- Абзац продублирован в `paper/review_soil_health_indicators.tex`.
- Запись добавлена в раздел «Литература» в `.md` и `.tex`.
- `python checks/check.py` возвращает код 0.
- PDF пересобран.

## Не входит
- Изменение таблицы индикаторов.
- Добавление строк в `indicators_table.md`.

## Итог
- Найдена статья Kuzyakov (2010) `kuz 1-s2.0-S0038071710001355-main.pdf` (в paper/ также есть Kuzyakov et al. 2000).
- Абзац (5 предложений) с основной мыслью добавлен в раздел 4 `.md` и `.tex`.
- Запись добавлена в Литературу `.md` (п. 18) и `.tex` (bibitem kuzyakov2010).
- PDF пересобран (pdflatex, exit 0).
- `python checks/check.py` → код 0.

- тип: [[Задача]]