"""Чистые функции работы с таблицей индикаторов (для hypothesis-тестов)."""
VALID_CATEGORY = {"chemical", "physical", "biological", "labile carbon"}
VALID_SENS = {"low", "medium", "high", "medium-high"}
SENS_ORDER = {"high": 0, "medium-high": 1, "medium": 2, "low": 3}


def count_by_category(rows: list[dict]) -> dict[str, int]:
    out = {c: 0 for c in VALID_CATEGORY}
    for r in rows:
        c = r.get("category", "").lower()
        if c in out:
            out[c] += 1
    return out


def filter_by_sensitivity(rows: list[dict], s: str) -> list[dict]:
    s = s.lower()
    return [r for r in rows if r.get("sensitivity", "").lower() == s]


def sort_by_indicator(rows: list[dict]) -> list[dict]:
    return sorted(rows, key=lambda r: r.get("indicator", "").lower())


def sort_by_sensitivity(rows: list[dict]) -> list[dict]:
    return sorted(
        rows,
        key=lambda r: (SENS_ORDER.get(r.get("sensitivity", "").lower(), 99),
                       r.get("indicator", "").lower()),
    )


def normalize_whitespace(s: str) -> str:
    return " ".join(s.split())
