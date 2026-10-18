# Отчёт по поиску

[источник] OpenAlex, 48 работ, тема soil health indicators,
запросы через API 2026-10-18.

Модели: BM25 (k1=1,2, b=0,75) и векторный поиск
(sentence-transformers/all-MiniLM-L6-v2, косинус).

## Запрос: soil organic carbon indicators of soil health

| ранг | BM25 | вектор |
|---|---|---|
| 1 | W3004850069 — Biochar physicochemical properties | W2792709023 — Soil quality: A critical review |
| 2 | W2792709023 — Soil quality: A critical review | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation |
| 3 | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation | W2588003345 — SoilGrids250m |
| 4 | W2588003345 — SoilGrids250m | W3004850069 — Biochar physicochemical properties |
| 5 | W3130661498 — Heavy Metals and Pesticides Toxicity | W3096865429 — Polycyclic Aromatic Hydrocarbons |

Общих документов в топ-5: 4 из 5.

[написано] Обе модели возвращают один и тот же набор обзорных работ; разница —
в порядке. Вектор ставит на первое место наиболее релевантный обзор качества
почвы, BM25 — статью о биоугле, где SOC упоминается лишь как одна из
характеристик. Пятые места расходятся: у BM25 — про тяжёлые металлы, у вектора
— про ПАУ; обе работы к теме не относятся. Специальных статей об индикаторах
SOC в библиотеке нет, поэтому ни одна модель не смогла их вернуть — это
ограничение библиотеки, а не модели.

---

## Запрос: microbial biomass as soil health indicator

| ранг | BM25 | вектор |
|---|---|---|
| 1 | W3004850069 — Biochar physicochemical properties | W2792709023 — Soil quality: A critical review |
| 2 | W2792709023 — Soil quality: A critical review | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation |
| 3 | W2604323123 — Gut microbiota functions | W2588003345 — SoilGrids250m |
| 4 | W3096865429 — Polycyclic Aromatic Hydrocarbons | W3004850069 — Biochar physicochemical properties |
| 5 | W3130661498 — Heavy Metals and Pesticides Toxicity | W1886677716 — Plant biostimulants |

Общих документов в топ-5: 2 из 5.

[написано] Классический провал BM25: на третье место попала статья «Gut
microbiota functions» — про микробиом кишечника, не почвы. Совпадение по слову
«microbial» дало ей высокий вес. Вектор такую ошибку не совершает: наверху
два обзора по качеству почвы, где микробная биомасса действительно обсуждается.
Но ни одна модель не нашла статью именно о MBC как индикаторе — таких работ в
собранной библиотеке нет.

---

## Запрос: minimum data set for soil quality index

| ранг | BM25 | вектор |
|---|---|---|
| 1 | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation | W2792709023 — Soil quality: A critical review |
| 2 | W2792709023 — Soil quality: A critical review | W2588003345 — SoilGrids250m |
| 3 | W2588003345 — SoilGrids250m | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation |
| 4 | W4292296492 — Recent advances in biodegradable polymers | W2564630286 — ReCiPe2016 |
| 5 | W3004850069 — Biochar physicochemical properties | W2790979755 — Deep learning in agriculture |

Общих документов в топ-5: 3 из 5.

[написано] Ни одна модель не нашла работ о minimum data set (MDS): в библиотеке
их нет. Три обзора совпадают у обеих моделей. Четвёртое-пятое места — промахи
по разным причинам: BM25 цепляется за «data set» (статья о биодеградируемых
полимерах), вектор — за «index» (LCA-метод ReCiPe и обзор deep learning в
сельском хозяйстве). Пример того, что семантика «индекс» и «набор данных» в
векторе тоже размыта.

---

## Запрос: aggregate stability and soil health

| ранг | BM25 | вектор |
|---|---|---|
| 1 | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation |
| 2 | W3130661498 — Heavy Metals and Pesticides Toxicity | W2792709023 — Soil quality: A critical review |
| 3 | W2792709023 — Soil quality: A critical review | W2588003345 — SoilGrids250m |
| 4 | W2588003345 — SoilGrids250m | W2175751433 — Safeguarding human health in the Anthropocene |
| 5 | W2175751433 — Safeguarding human health in the Anthropocene | W2779282391 — Microplastics and Nanoplastics |

Общих документов в топ-5: 4 из 5.

[написано] Снова совпадают четыре работы из пяти; ядро — Lal 2015 и обзор
качества почвы. Специальной статьи об агрегатной стабильности в библиотеке нет,
поэтому обе модели возвращают общие обзоры, а на нижних позициях — случайные
совпадения по «health» и «soil». Это иллюстрирует главный тезис лекции: если
целевой темы в коллекции нет, её не найдёт никакая модель.

---

## Запрос: soil enzyme activity as indicator

| ранг | BM25 | вектор |
|---|---|---|
| 1 | W2792709023 — Soil quality: A critical review | W2792709023 — Soil quality: A critical review |
| 2 | W2604323123 — Gut microbiota functions | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation |
| 3 | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation | W2588003345 — SoilGrids250m |
| 4 | W3152719213 — Toxic Mechanisms of Five Heavy Metals | W1886677716 — Plant biostimulants |
| 5 | W3004850069 — Biochar physicochemical properties | W3125960586 — Agriculture Development, Pesticides |

Общих документов в топ-5: 2 из 5.

[написано] Снова BM25 возвращает «Gut microbiota functions» — теперь из-за слова
«activity». Вектор держит обзоры по качеству почвы наверху, но и он не находит
работ именно о почвенных ферментах: в библиотеке нет ни одной статьи о soil
enzymes (β-glucosidase, FDA, LAP, URE). Это дыра в покрытии, которая видна
только при сравнении с целевой темой — обе модели «отвечают», но не по делу.

---

## Запрос: permanganate oxidizable carbon soil health

| ранг | BM25 | вектор |
|---|---|---|
| 1 | W3004850069 — Biochar physicochemical properties | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation |
| 2 | W1502801871 — Restoring Soil Quality to Mitigate Soil Degradation | W3004850069 — Biochar physicochemical properties |
| 3 | W3130661498 — Heavy Metals and Pesticides Toxicity | W2784350055 — Carbon capture and storage (CCS) |
| 4 | W2588003345 — SoilGrids250m | W2795272585 — Efficient hydrogen peroxide generation |
| 5 | W2784350055 — Carbon capture and storage (CCS) | W2588003345 — SoilGrids250m |

Общих документов в топ-5: 4 из 5.

[написано] Обе модели промахнулись: в библиотеке нет статьи о POXC (permanganate
oxidizable carbon). Слово «carbon» у обеих цепляет работу про CCS (carbon capture
and storage) — у вектора она даже на третьем месте, хотя к почвенному углероду
отношения не имеет. Это ограничение мешка слов и слабой специализации
кодировщика: «carbon» в разных контекстах не различается.

---
