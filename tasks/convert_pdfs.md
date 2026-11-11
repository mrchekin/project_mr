---
type: Задача
status: выполнена
---

## Запрос пользователя
Проверить paper/, сверить PDF с MD-копиями в results/converted/paper/, сконвертировать отсутствующие.

## Готово, когда
Для каждого уникального PDF-источника в paper/ (кроме артефактов проекта) есть MD-копия в results/converted/paper/.

## Не входит
- review_soil_health_indicators.pdf (собранный PDF обзора — артефакт, не источник)
- Lal 2016.pdf (дубликат paper.pdf, у которого уже есть paper.md)
- _compressed.pdf (сжатые дубликаты оригиналов)

- тип: [[Задача]]

## Итог
Сверены 126 PDF в paper/ с MD-копиями в results/converted/paper/. Сконвертированы через pymupdf4llm (установлен в .venv) 24 уникальных PDF без MD-копий. Остались без MD только 2 намеренно исключённых: Lal 2016.pdf (идентичен paper.pdf, у которого есть paper.md) и review_soil_health_indicators.pdf (собранный PDF обзора — артефакт).
