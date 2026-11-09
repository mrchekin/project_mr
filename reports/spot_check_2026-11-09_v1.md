# Точечная проверка обзора — 2026-11-09

Случайная выборка 5 утверждений из `paper/review_soil_health_indicators.md` (seed=20261019).

**Проверяемая версия:** HEAD `7d0d71b`; локальные изменения не закоммичены
(`paper/review_soil_health_indicators.md`, `.tex`, `diary.md`, `STATUS.md`);
дата проверки 2026-11-09. При изменении обзора отчёт не считать проверкой новой версии.

## Задание

Для каждого тезиса:
1. Открыть PDF/источник по ссылке и странице.
2. Найти дословную цитату, подтверждающую или опровергающую тезис.
3. Записать цитату и итог.

Агенту с промптом «найди ошибку», не «подтверди».

## Утверждения

### 1. …бильные фракции, что может объясняться свойствами почвы, неоднородным распределением растительных и микробных остатков, типом и количеством вносимого органического вещества, условиями окружающей среды и временем отбора проб; кроме того, о химическом составе и сезонной динамике POXC известно мало, а его чувствительность к другим практикам (например, покровным культурам) требует дальнейшей валидации

**Источник:** `(Bongiorno et al., 2019, с. 10)`

**Цитата (PDF, физическая стр. 10):** «Some studies did not find effects of tillage
and fertilization on the labile C fractions … This can be due to the soil properties,
the non-homogeneous distribution of plant and microbial residues, organic matter
input type and quantity, environmental conditions and time of sampling»; «Currently,
little is known about the chemical composition and the seasonal dynamics of POXC.
However, there is evidence for the sensitivity of POXC to other types of soil
management beside tillage and organic matter input such as the use of cover crops,
but this should be validated with further studies»

**Проверяющий:** агент, установка «найди ошибку» (PDF `paper/1-s2.0-S1470160X18309415-mainext.pdf`)

**Итог:** ☑ подтверждено  ☐ опровергнуто  ☐ не найдено

### 2. (2023) провели глобальный метаанализ индексов качества почвы (SQI) и отметили, что из-за разнообразия почв и SQI сравнение результатов исторически затруднено; на итоговую оценку значимо влиял тип базы данных, но не число индикаторов в индексе

**Источник:** `(Bedolla-Rivera et al., 2023, с. 1)`

**Цитата (PDF, физическая стр. 1):** «However, due to the variety of soils and
SQIs, analyzing and comparing results has historically been difficult. … From the
factors analyzed, the minimum database had a significant effect on the soil quality
results, but not the number of indicators that made up the SQIU»

**Проверяющий:** агент, установка «найди ошибку» (PDF `paper/sqi agronomy-13-02166-v2_compressed.pdf`)

**Итог:** ☑ подтверждено  ☐ опровергнуто  ☐ не найдено

### 3. Лабильные фракции углерода

Изменения, вызванные агротехническими практиками, часто трудно обнаружить по общему содержанию SOC

**Источник:** `(Bongiorno et al., 2019, с. 1)`

**Цитата (PDF, физическая стр. 2):** «Since changes induced by soil practices are
often difficult to detect by total SOC measurement (Haynes, 2005), measuring
rapidly changing SOC pools, such as labile carbon pools, might be more informative
to assess soil quality»

**Примечание:** в обзоре указана «с. 1», фактически цитата на физической стр. 2 —
расхождение страницы (требует правки/решения человека).

**Проверяющий:** человек (подтверждение 2026-11-09: «цитаты в порядке»); цитату нашёл агент по PDF `paper/1-s2.0-S1470160X18309415-mainext.pdf`

**Итог:** ☑ подтверждено  ☐ опровергнуто  ☐ не найдено

### 4. Авторы заключают, что функциональные гены чувствительны к органическим вносам и дают более детальное и механистическое понимание почвенных процессов, чем обычные индикаторы

**Источник:** `(Jia, 2025, с. 1)`

**Цитата (PDF, физическая стр. 1):** «These results indicate that microbial
functional genes are sensitive to organic inputs and could provide a more detailed
and mechanistic understanding of soil processes than conventional indicators by
capturing the biochemical processes that govern nutrient dynamics»

**Проверяющий:** агент, установка «найди ошибку» (PDF `paper/researcher-s2.0-S0038071725000616-main.pdf`)

**Итог:** ☑ подтверждено  ☐ опровергнуто  ☐ не найдено

### 5. (2019) документируют развитие концепции здоровья почвы в США и рекомендуют совершенствовать инструменты оценки Soil Management Assessment Framework (SMAF) и Comprehensive Assessment of Soil Health (CASH), разрабатывать протоколы национального мониторинга и калибровать более чувствительные биологические, химические и физические индикаторы

**Источник:** `(Karlen et al., 2019, с. 1)`

**Цитата (PDF, физическая стр. 1):** «Recommendations emphasize improving the Soil
Management Assessment Framework (SMAF) and/or Comprehensive Assessment of Soil
Health (CASH) assessment tools, developing protocols for national soil health
monitoring, identifying and calibrating better indicators of soil biological,
chemical, and physical health»

**Проверяющий:** человек (подтверждение 2026-11-09: «цитаты в порядке»); цитату нашёл агент по PDF `paper/Karlen 2019_compressed.pdf`

**Итог:** ☑ подтверждено  ☐ опровергнуто  ☐ не найдено

## Сводка

- Подтверждено: 5 / 5
- Опровергнуто: 0 / 5
- Не найдено: 0 / 5

Проверено агентом: 3/5 (утверждения 1, 2, 4); человеком: №3, №5.
Оговорка: №3 подтверждён по содержанию, но страница в обзоре неверна
(указана «с. 1», фактически физическая стр. 2).

Критерий приемки: **подтверждено ≥ 4 из 5**.
Если < 4 — обзор возвращается на доработку.