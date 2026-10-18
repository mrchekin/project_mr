#!/usr/bin/env python3
"""Собирает работы из OpenAlex по теме и сохраняет в library/.
С retry: сеть до api.openalex.org бывает медленной.
"""
import json, os, time
from pathlib import Path
import urllib.request, urllib.parse, urllib.error

# загрузка .env
_env = Path(".env")
if _env.exists():
    for _line in _env.read_text(encoding="utf-8").splitlines():
        if "=" in _line and not _line.startswith("#"):
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

OUT = Path("library")
OUT.mkdir(exist_ok=True)

QUERIES = [
    "soil health indicators",
    "soil quality index",
    "soil organic carbon indicator",
    "microbial indicators soil health",
    "soil health assessment framework",
    "soil enzyme activity indicator",
    "permanganate oxidizable carbon",
    "earthworm soil health",
]

API = "https://api.openalex.org/works"
HEADERS = {"User-Agent": "ai4science-course/1.0 (mailto:you@example.org)"}
key = os.environ.get("OPENALEX_API_KEY")
if key:
    HEADERS["Authorization"] = f"Bearer {key}"

def abstract_text(w):
    idx = w.get("abstract_inverted_index")
    if not idx:
        return ""
    pos = {}
    for word, arr in idx.items():
        for p in arr:
            pos[p] = word
    return " ".join(pos[i] for i in sorted(pos))

def fetch_json(url, headers, retries=4, timeout=90):
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except (TimeoutError, urllib.error.URLError, ConnectionError) as e:
            last_err = e
            wait = 2 * attempt
            print(f"  retry {attempt}/{retries} через {wait} с ({type(e).__name__})")
            time.sleep(wait)
    raise RuntimeError(f"не удалось получить ответ: {last_err}")

seen, docs = set(), []
for q in QUERIES:
    params = {
        "search": q,
        "filter": "type:article,from_publication_date:2015-01-01",
        "sort": "cited_by_count:desc",
        "per-page": "10",
        "select": "id,doi,title,publication_year,authorships,"
                  "abstract_inverted_index,cited_by_count",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    print(f"запрос: {q}")
    data = fetch_json(url, HEADERS)

    for w in data.get("results", []):
        wid = w["id"].split("/")[-1]
        if wid in seen:
            continue
        seen.add(wid)
        docs.append({
            "openalex_id": wid,
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
            "title": w.get("title") or "",
            "year": w.get("publication_year"),
            "authors": [a["author"]["display_name"] for a in w.get("authorships", [])],
            "abstract": abstract_text(w),
            "cited_by_count": w.get("cited_by_count", 0),
            "query": q,
            "retrieved": time.strftime("%Y-%m-%d"),
        })
    time.sleep(0.5)

for d in docs:
    fn = OUT / f"{d['openalex_id']}.md"
    fn.write_text(
        "---\n"
        f"openalex_id: {d['openalex_id']}\n"
        f"doi: {d['doi']}\n"
        f"year: {d['year']}\n"
        f"cited_by: {d['cited_by_count']}\n"
        f"retrieved: {d['retrieved']}\n"
        f"query: {d['query']}\n"
        "---\n\n"
        f"# {d['title']}\n\n"
        f"Авторы: {', '.join(d['authors'][:6])}\n\n"
        f"## Аннотация\n\n{d['abstract'][:2500]}\n",
        encoding="utf-8",
    )

print(f"сохранено {len(docs)} работ в {OUT}/")
