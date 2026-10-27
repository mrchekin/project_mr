#!/usr/bin/env python3
"""Случайная выборка тезисов из обзора для независимой проверки.

Формат ссылок в обзоре: (Автор et al., год; файл.pdf, стр. N).
Создает reports/spot_check_<дата>.md с N тезисами для сверки.
"""
import random
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT / "paper" / "review_soil_health_indicators.md"
OUT_DIR = ROOT / "reports"

N = 5
SEED = 20261019

# ссылка: (...) со словом стр./с. и номером страницы
CITATION_RE = re.compile(
    r"\([^()]{5,300}?(?:стр\.|с\.)\s*[\d\-–—, ]+\)",
    re.UNICODE,
)


def extract_claims(text):
    """Возвращает список (тезис, ссылка)."""
    # одиночные переносы склеить, абзацы оставить
    flat = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    flat = re.sub(r"[ \t]+", " ", flat)

    claims = []
    for m in CITATION_RE.finditer(flat):
        link = m.group(0)
        before = flat[max(0, m.start() - 600):m.start()]
        # последнее предложение перед ссылкой
        parts = re.split(r"(?<=[.!?])\s+", before)
        sentence = parts[-1].strip() if parts else before.strip()
        if len(sentence) < 30:
            continue
        if len(sentence) > 400:
            sentence = "…" + sentence[-400:]
        claims.append((sentence, link))
    return claims


def main():
    if not REVIEW.exists():
        print(f"FAIL: нет {REVIEW}")
        sys.exit(1)

    text = REVIEW.read_text(encoding="utf-8")
    claims = extract_claims(text)
    print(f"Найдено утверждений со ссылкой: {len(claims)}")

    if len(claims) < N:
        print(f"FAIL: нужно >= {N}. Первые 5 ссылок для отладки:")
        for m in list(CITATION_RE.finditer(text))[:5]:
            print("  >", m.group(0)[:160])
        sys.exit(1)

    # дедупликация
    seen = set()
    unique = []
    for claim, link in claims:
        key = (claim[:80], link)
        if key in seen:
            continue
        seen.add(key)
        unique.append((claim, link))

    if len(unique) < N:
        print(f"FAIL: после дедупликации {len(unique)}, нужно >= {N}")
        sys.exit(1)

    rng = random.Random(SEED)
    picked = rng.sample(unique, N)

    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f"spot_check_{date.today().isoformat()}.md"

    lines = [
        f"# Точечная проверка обзора — {date.today().isoformat()}",
        "",
        f"Случайная выборка {N} утверждений из "
        f"`paper/review_soil_health_indicators.md` (seed={SEED}).",
        "",
        "## Задание",
        "",
        "Для каждого тезиса:",
        "1. Открыть PDF/источник по ссылке и странице.",
        "2. Найти дословную цитату, подтверждающую или опровергающую тезис.",
        "3. Записать цитату и итог.",
        "",
        "Агенту с промптом «найди ошибку», не «подтверди».",
        "",
        "## Утверждения",
        "",
    ]
    for i, (claim, src) in enumerate(picked, 1):
        lines += [
            f"### {i}. {claim}",
            "",
            f"**Источник:** `{src}`",
            "",
            "**Цитата:** _______________________________",
            "",
            "**Итог:** ☐ подтверждено  ☐ опровергнуто  ☐ не найдено",
            "",
        ]
    lines += [
        "## Сводка",
        "",
        f"- Подтверждено: __ / {N}",
        f"- Опровергнуто: __ / {N}",
        f"- Не найдено: __ / {N}",
        "",
        "Критерий приемки: **подтверждено ≥ 4 из 5**.",
        "Если < 4 — обзор возвращается на доработку.",
    ]

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Отчет: {out.relative_to(ROOT)}")
    print(f"Проверьте {N} утверждений (2–3 вручную, остальные — агент).")


if __name__ == "__main__":
    main ()
