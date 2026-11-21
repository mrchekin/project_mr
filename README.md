# Чувствительные показатели здоровья почвы

Учебный проект курса ШАД Яндекса об ИИ-агентах для исследователя.
Научная задача — подготовить обзор показателей здоровья почвы: сравнить
их отклик на агротехнические практики, методы измерения и условия применения.

Агент используется для работы с литературой, заметками, таблицей индикаторов,
графом проекта и текстом статьи. Правила работы описаны в [AGENTS.md](AGENTS.md).

## Материалы проекта

В основе обзора — корпус из 47 научных статей. Конференционные версии
подготовлены путём сокращения полного обзора.

| Материал | Содержание | Исходник |
|---|---|---|
| Полный обзор | Развёрнутый текст, 19 библиографических позиций | [Markdown](paper/review_soil_health_indicators.md), [LaTeX](paper/review_soil_health_indicators.tex) |
| Таблица индикаторов | 25 строк: показатель, категория, метод, чувствительность, воздействие и источник | [indicators_table.md](paper/indicators_table.md) |
| Конференционная версия на русском | Сокращённый обзор, 13 библиографических позиций | [conference_review.tex](paper/conference_review.tex) |
| Конференционная версия на английском | Sensitive Indicators of Soil Health: Responses to Management and Limitations | [conference_review_en.tex](paper/conference_review_en.tex) |
| Таблица сокращений | Сокращения, используемые в английской статье | [conference_abbreviations_en.tex](paper/conference_abbreviations_en.tex) |

В английской версии таблица сокращений размещена в разделе 1 (Table 1),
сравнительная таблица индикаторов — Table 2.

PDF-файлы хранятся локально: `paper/review_soil_health_indicators.pdf`,
`paper/conference_review.pdf` и `paper/conference_review_en.pdf`.
В Git включены исходники статей и класс оформления.

## Навигация

- [INDEX.md](INDEX.md) — карта файлов проекта.
- [STATUS.md](STATUS.md) — текущее состояние работы.
- [AGENTS.md](AGENTS.md) — договор с агентом.
- [METHOD.md](METHOD.md) — методика технических проверок.
- [diary.md](diary.md) — журнал работы.
- [reports/](reports/) — отчёты и материалы учебных заданий.

## Структура

| Путь | Назначение |
|---|---|
| [paper/](paper/) | Научные статьи, тексты обзора и класс LaTeX |
| [notes/](notes/) | Заметки источников, индикаторов, групп и запросов |
| [ontology/](ontology/), [ontology.yaml](ontology.yaml) | Классы и отношения графа проекта |
| [tasks/](tasks/) | Задачи и подзадачи |
| [checks/](checks/) | Скрипты технической проверки и тесты |
| [memory/](memory/), [cascade.sh](cascade.sh) | Уровни сжатия статьи Lal 2016 |
| [library/](library/) | Метаданные и аннотации публикаций из OpenAlex |
| [scripts/](scripts/), [src/](src/) | Запуск проверок, поиск и обработка материалов |
| [results/](results/) | Производные файлы и результаты экспериментов |
| [data/](data/) | Исходные данные |

Локальные Markdown-копии статей находятся в `results/converted/paper/`.
Исходные PDF, конвертированные тексты и бинарные рисунки исключены из Git.
Материалы: [архив на Яндекс Диске](https://disk.360.yandex.ru/d/iLRsL0SoqkfneQ).

## Окружение

Из корня проекта в Ubuntu/WSL:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
~~~

Активация окружения в Windows PowerShell:

~~~powershell
.\.venv\Scripts\Activate.ps1
~~~

Зависимости технических проверок перечислены в
[requirements.txt](requirements.txt). Для конвертации статей используется
pymupdf4llm, для сборки LaTeX — pdflatex.

## Технические проверки

~~~bash
python -B checks/check.py
python -B -m pytest checks -q -p no:cacheprovider
python -B checks/check_graph.py
~~~

Для файловых проверок нужны локальные источники с именами из столбца
source_file в таблице индикаторов.

[Общий запуск](scripts/run_verifier.py) выполняет проверки по этапам
и записывает результаты в `results/verifier_log.csv`, заменяя прежний журнал.
Описание процедур — в [METHOD.md](METHOD.md).

## Сборка статьи

Английская конференционная версия собирается из корня проекта:

~~~bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error conference_review_en.tex
pdflatex -interaction=nonstopmode -halt-on-error conference_review_en.tex
cd ..
~~~

Два прохода обновляют ссылки и нумерацию. Результат —
`paper/conference_review_en.pdf`. Используются класс
[ai4science_ysda.cls](paper/ai4science_ysda.cls) и установленные LaTeX-пакеты.

Русская версия собирается аналогично из `conference_review.tex`.
Полный обзор собирается из `review_soil_health_indicators.tex`;
для него нужен локальный рисунок `paper/figures/graphical_abstract.pdf`.

## Учебные этапы

| Этап | Материалы |
|---|---|
| Среда и контекст | Договор с агентом, журнал, память, онтология и [сравнение поиска](reports/my_search_report.md) |
| Проверка | [Отчёт ДЗ 2](reports/hw2_report.md), [дерево подцелей](SUBGOALS.md), [журнал попыток](ATTEMPTS.md) и тесты |
| Подготовка статьи | Полный обзор, конференционные версии, таблица сокращений и отчёты редактуры |
| Развёртывание | [Материалы локального запуска и подготовки VPS](tasks/развернуть-агента.md) |

Материалы ДЗ 2 сохранены в ветке `hw2`; метка `exp-verifier` относится
к более раннему этапу проекта.
