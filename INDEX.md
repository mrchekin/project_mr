# INDEX.md — что где лежит

Актуализировано 2026-11-22. Прочитай первым.

- AGENTS.md — договор, пределы проверки и правила редактуры научного обзора.
- STATUS.md — текущее состояние и следующие задачи.
- diary.md — журнал, только дописывание; подтверждение человеком и SHA256 английской версии.
- METHOD.md — текущая схема данных, 24 теста и ограничения.
- reports/project_update_2026-11-22.md — результаты текущего обновления.
- tasks/ — задачи и подзадачи; историческую приёмку ставит человек.
- paper/review_soil_health_indicators.md — полный обзор, 19 источников.
- paper/review_soil_health_indicators.tex и .pdf — полный обзор в LaTeX и PDF.
- paper/indicators_table.md — 25 строк, семь столбцов, включая sensitivity_target.
- paper/conference_review.tex и .pdf — русская конференционная версия.
- paper/conference_review_en.tex и .pdf — английская версия, подтверждена человеком 22.11.2026.
- paper/conference_abbreviations_en.tex — Table 1, сокращения в разделе 1 английской статьи.
- paper/ai4science_ysda.cls — класс конференционного оформления.
- reports/conference_review_notes.md и reports/conference_review_en_notes.md — история подготовки версий.
- paper/paper.pdf и paper/paper.txt — статья Lal 2016, только чтение.
- paper/sample/ — образец оформления; не научный источник.
- paper/figures/ — графические материалы.
- checks/check.py — структура полного обзора и валидность таблицы.
- checks/test_properties.py — семь файловых тестов.
- checks/test_properties_hypothesis.py — шесть свойств функций и пять проверок ошибочных функций.
- checks/test_integration.py — шесть интеграционных тестов; всего pytest собирает 24.
- checks/check_graph.py — минимум пять заметок индикаторов и наличие провенанса; не полная онтология.
- checks/verify_claims.py — ограниченный шаблон извлечения; на текущем обзоре 0 утверждений.
- reports/spot_check_*.md — исторические выборки, относятся к указанным в них версиям.
- scripts/run_verifier.py — запуск через sys.executable; перезаписывает results/verifier_log.csv.
- requirements.txt — зависимости проверки, не полный состав среды всех инструментов.
- ontology.yaml — девять классов, свойства и шесть правил.
- ontology/ — заметки классов.
- notes/ — объекты графа, включая 33 карточки источников.
- library/ — 48 записей OpenAlex; это отдельный набор относительно корпуса 47 статей.
- scripts/fetch_library.py — получение библиотеки; сеть требует отдельного разрешения.
- scripts/search_lab.py и reports/my_search_report.md — BM25 и векторный поиск.
- memory/L1.md, memory/L2.md, memory/L3.md — сжатие Lal; открытые замечания в L2.
- cascade.sh — каскадное сжатие; при обновлении документации не запускать.
- results/converted/paper/ — 113 Markdown-копий при аудите; две почти пустые.
- results/conference_backups/ — прежние версии английской статьи.
- results/project_update_2026-11-22/ — резервные копии и контроль текущего обновления.
- src/make_graphical_abstract.py — графический абстракт.
- data/ — исходные данные, только чтение.
- results/ — производные файлы и исторические результаты.

.obsidian/ и chekin/.obsidian/ — настройки хранилища. Пустой q, файлы
Zone.Identifier и образцы не удаляются автоматически. PDF и конвертации
исключены из Git; локальное наличие не означает публикацию на GitHub.
