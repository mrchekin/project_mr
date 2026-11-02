"""Пять свойств таблицы индикаторов через hypothesis (направление B, неделя 7)."""
import sys
from pathlib import Path

from hypothesis import given, strategies as st, settings, HealthCheck, find

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from table_ops import (
    count_by_category, filter_by_sensitivity, sort_by_indicator,
    sort_by_sensitivity, normalize_whitespace,
    VALID_CATEGORY, VALID_SENS, SENS_ORDER,
)

row = st.fixed_dictionaries({
    "indicator": st.text(min_size=2, max_size=20).filter(lambda s: s.strip()),
    "category": st.sampled_from(sorted(VALID_CATEGORY)),
    "method": st.text(min_size=2, max_size=20),
    "sensitivity": st.sampled_from(sorted(VALID_SENS)),
    "source_file": st.text(min_size=3, max_size=20),
    "source_page": st.integers(min_value=1, max_value=999).map(str),
})
rows = st.lists(row, min_size=0, max_size=30)
_slow = [HealthCheck.too_slow, HealthCheck.filter_too_much]


@given(rows=rows)
@settings(suppress_health_check=_slow, max_examples=50)
def test_count_preserves_total(rows):
    counts = count_by_category(rows)
    assert sum(counts.values()) == len(rows)


@given(rows=rows)
@settings(suppress_health_check=_slow, max_examples=50)
def test_sensitivity_order_is_monotone(rows):
    ordered = sort_by_sensitivity(rows)
    keys = [SENS_ORDER[r["sensitivity"].lower()] for r in ordered]
    assert keys == sorted(keys)


@given(rows=rows, s=st.sampled_from(sorted(VALID_SENS)))
@settings(suppress_health_check=_slow, max_examples=50)
def test_filter_returns_consistent_subset(rows, s):
    filtered = filter_by_sensitivity(rows, s)
    assert len(filtered) <= len(rows)
    assert all(r in rows for r in filtered)
    assert all(r["sensitivity"].lower() == s.lower() for r in filtered)


@given(rows=rows)
@settings(suppress_health_check=_slow, max_examples=50)
def test_sort_is_idempotent(rows):
    once = sort_by_indicator(rows)
    assert sort_by_indicator(once) == once


@given(s=st.text(max_size=100))
@settings(suppress_health_check=_slow, max_examples=50)
def test_whitespace_normalization_is_idempotent(s):
    once = normalize_whitespace(s)
    assert normalize_whitespace(once) == once


@given(rows=rows)
@settings(suppress_health_check=_slow, max_examples=50)
def test_fields_are_within_valid_sets(rows):
    for r in rows:
        assert r["category"].lower() in VALID_CATEGORY
        assert r["sensitivity"].lower() in VALID_SENS


def _broken_count(rows):
    out = {c: 0 for c in VALID_CATEGORY if c != "labile carbon"}
    for r in rows:
        c = r.get("category", "").lower()
        if c in out:
            out[c] += 1
    return out


def _broken_sens(rows):
    return sorted(rows, key=lambda r: -SENS_ORDER.get(r["sensitivity"].lower(), 99))


def _broken_filter(rows, s):
    return [r for r in rows if r["sensitivity"].lower() != s.lower()]


def _broken_idem(rows):
    return [dict(r, indicator=r.get("indicator", "") + " ") for r in rows]


def _broken_bounds(rows):
    out = list(rows)
    if out:
        out[0] = dict(out[0], sensitivity="extreme")
    return out


def test_broken_count_caught():
    bad = find(rows, lambda r: any(x["category"] == "labile carbon" for x in r)
               and sum(_broken_count(r).values()) != len(r))
    assert bad is not None


def test_broken_sens_caught():
    bad = find(rows, lambda r: len(r) >= 2 and
               [SENS_ORDER[x["sensitivity"].lower()] for x in _broken_sens(r)] !=
               sorted([SENS_ORDER[x["sensitivity"].lower()] for x in _broken_sens(r)]))
    assert bad is not None


def test_broken_filter_caught():
    bad = find(st.tuples(rows, st.sampled_from(sorted(VALID_SENS))),
               lambda t: any(x["sensitivity"].lower() != t[1].lower() for x in _broken_filter(*t)))
    assert bad is not None


def test_broken_idem_caught():
    bad = find(rows, lambda r: len(r) >= 1 and _broken_idem(_broken_idem(r)) != _broken_idem(r))
    assert bad is not None


def test_broken_bounds_caught():
    bad = find(rows, lambda r: len(r) >= 1 and
               any(x["sensitivity"].lower() not in VALID_SENS for x in _broken_bounds(r)))
    assert bad is not None
