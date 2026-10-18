---
type: ЗапросКГрафу
source: Wikidata
retrieved: 2026-10-18
---

# Запрос к Wikidata: soil organic carbon

## Инструмент и аргументы

- инструмент: `wikidata_sparql` (MCP research-mcp)
- endpoint: https://query.wikidata.org/sparql
- Q-сущность: Q113009567 (soil organic carbon)

## Запрос SPARQL

```sparql
SELECT ?property ?propertyLabel ?value ?valueLabel WHERE {
  wd:Q113009567 ?prop ?value .
  ?property wikibase:directClaim ?prop .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "ru,en". }
}
LIMIT 20
