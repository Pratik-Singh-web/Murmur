"""Seller → persona assignment rules.

Rules come from the PS07 analysis (research/ps07-data-analysis.md). They are
deliberately simple and explainable: one priority-ordered list, no model.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

CURRENT_YEAR = 2026
BIG_TURNOVER = {"1.5 - 5 Cr", "5 - 25 Cr", "25 - 100 Cr", "100 - 500 Cr", "> 500 Cr"}
RETAIL = {"Trader - Retailer", "Retailer"}


def _num(v) -> float | None:
    try:
        f = float(v)
        return None if math.isnan(f) else f
    except (TypeError, ValueError):
        return None


def _flag(v) -> bool:
    return _num(v) == 1.0


@dataclass(frozen=True)
class Assignment:
    persona_id: str
    reason: str
    skip: bool = False


def assign_persona(row: dict) -> Assignment:
    """Return the persona for one seller row (dict of seller-file columns)."""
    if _flag(row.get("do_not_call_requested")):
        return Assignment("none", "seller asked not to be called", skip=True)

    turnover = (row.get("annual_turnover") or "").strip()
    btype = (row.get("business_type") or "").strip()
    products = _num(row.get("eng_product_count"))
    gst_year = _num(row.get("gst_registration_year"))
    nature = (row.get("nature_of_business") or "").strip()

    if turnover in BIG_TURNOVER or btype == "Limited Company" or (products is not None and products > 50):
        return Assignment("established_enterprise", f"turnover={turnover or '-'}, type={btype or '-'}, products={products}")
    if gst_year is not None and CURRENT_YEAR - gst_year <= 2:
        return Assignment("new_seller", f"GST registered {int(gst_year)}")
    if nature in RETAIL:
        return Assignment("busy_retailer", f"nature={nature}")
    if nature == "Manufacturer":
        return Assignment("manufacturer", "nature=Manufacturer")
    if nature == "Service Provider and Others":
        return Assignment("service_provider", "nature=Service Provider")
    return Assignment("trader_wholesaler", f"nature={nature or 'unknown'}")


def starting_language(state: str | None, language_map: dict) -> str:
    return language_map.get((state or "").strip(), language_map.get("default", "Hindi"))


def should_dial(attempt_no: int, callback_requested: bool, stop_after: int = 4) -> bool:
    """Retry policy: MF falls to ≤3.3% from attempt 5, so stop unless the seller asked for a callback."""
    return callback_requested or attempt_no <= stop_after
