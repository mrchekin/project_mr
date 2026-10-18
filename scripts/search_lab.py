#!/usr/bin/env python3
"""Мини-замена search_lab.ipynb: BM25 vs векторный поиск на library/."""
import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

LIB = Path("library")
REPORT = Path("reports/my_search_report.md")
REPORT.parent.mkdir(exist_ok=True)

QUERIES = [
    "soil organic carbon indicators of soil health",
    "microbial biomass as soil health indicator",
    "minimum data set for soil quality index",
    "aggregate stability and soil health",
    "soil enzyme activity as indicator",
    "permanganate oxidizable carbon soil health",
]

def tokens(s):
    return re.findall(r"[a-zа-я0-9]+", s.lower())

def load_docs():
    docs = []
    for f in sorted(LIB.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        # первые две строки — title
        title = ""
        for ln in text.splitlines():
            if ln.startswith("# "):
                title = ln[2:].strip()
                break
        # берём всё, кроме YAML-фронтматтера
        body = text
        if body.startswith("---"):
            parts = body.split("---", 2)
            if len(parts) >= 3:
                body = parts[2]
        docs.append({"id": f.stem, "title": title, "text": body.strip()[:3000]})
    return docs

def main():
    docs = load_docs()
    print(f"документов: {len(docs)}")
    if len(docs) < 20:
        print("!!! меньше 20 работ — добавьте ещё в library/")

    print("индексируем BM25…")
    bm25 = BM25Okapi([tokens(d["text"]) for d in docs])

    print("загружаем кодировщик (скачивание ~90 МБ при первом запуске)…")
    encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("кодируем документы…")
    vecs = encoder.encode([d["text"] for d in docs], normalize_embeddings=True)

    lines = ["# Отчёт по поиску\n\n"]
    lines.append(f"[источник] OpenAlex, {len(docs)} работ, тема soil health indicators, "
                 f"запросы через API 2026-10-18\n\n")
    lines.append("Модели: BM25 (k1=1,2, b=0,75) и векторный поиск "
                 "(sentence-transformers/all-MiniLM-L6-v2, косинус).\n\n")

    for q in QUERIES:
        lines.append(f"## Запрос: {q}\n\n")

        bm25_scores = bm25.get_scores(tokens(q))
        bm25_top = np.argsort(-bm25_scores)[:5]

        qv = encoder.encode([q], normalize_embeddings=True)[0]
        sims = vecs @ qv
        vec_top = np.argsort(-sims)[:5]

        lines.append("| ранг | BM25 | вектор |\n|---|---|---|\n")
        for r in range(5):
            b = docs[bm25_top[r]]
            v = docs[vec_top[r]]
            b_label = f"{b['id']} — {b['title'][:50]}"
            v_label = f"{v['id']} — {v['title'][:50]}"
            lines.append(f"| {r+1} | {b_label} | {v_label} |\n")

        overlap = len(set(bm25_top) & set(vec_top))
        lines.append(f"\nОбщих документов в топ-5: {overlap} из 5.\n\n")
        lines.append("[написано] \n\n")
        lines.append("---\n\n")

    REPORT.write_text("".join(lines), encoding="utf-8")
    print(f"отчёт: {REPORT}")
    print(f"строк [написано]: заполните их вручную")

if __name__ == "__main__":
    main()
