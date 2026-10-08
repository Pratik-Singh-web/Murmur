"""Score baseline vs seller-fit.

Two inputs, use either or both:
  1. Webhook database (real/test calls):  python eval/score.py --db out/murmur.db
  2. Sarvam Tests results exported/typed into a CSV with columns
     scenario_id, agent_label (baseline|seller_fit), passed (1/0), outcome:
                                          python eval/score.py --tests eval/test_results.csv
"""
from __future__ import annotations

import argparse
import csv
import math
import sqlite3
from collections import defaultdict


def ci(p: float, n: int) -> str:
    if n == 0:
        return "-"
    h = 1.96 * math.sqrt(p * (1 - p) / n)
    return f"±{h * 100:.0f}pp"


def from_db(path: str) -> None:
    con = sqlite3.connect(path)
    rows = con.execute("SELECT agent_label, persona_id, call_outcome, meeting_time, user_turns FROM calls").fetchall()
    agg = defaultdict(lambda: {"n": 0, "mf": 0, "early": 0, "false_mf": 0, "turns": 0})
    for label, persona, outcome, mtime, uturns in rows:
        for key in ((label, "ALL"), (label, persona or "?")):
            a = agg[key]
            a["n"] += 1
            a["mf"] += outcome == "meeting_fixed"
            a["early"] += outcome == "dropped_early" or (uturns or 0) <= 1
            a["false_mf"] += outcome == "meeting_fixed" and not (mtime or "").strip()
            a["turns"] += uturns or 0
    print(f"{'agent':<11}{'persona':<24}{'calls':>6}{'MF%':>7}{'95%':>7}{'early%':>8}{'falseMF':>8}{'turns':>7}")
    for (label, persona), a in sorted(agg.items()):
        n = a["n"]; p = a["mf"] / n
        print(f"{label:<11}{persona:<24}{n:>6}{p * 100:>6.0f}%{ci(p, n):>7}{a['early'] * 100 / n:>7.0f}%{a['false_mf']:>8}{a['turns'] / n:>7.1f}")


def from_tests(path: str) -> None:
    agg = defaultdict(lambda: [0, 0])
    for r in csv.DictReader(open(path, encoding="utf-8")):
        label = r["agent_label"]
        behaviour = r["scenario_id"].split("__")[-1]
        for key in ((label, "ALL"), (label, behaviour)):
            agg[key][0] += 1
            agg[key][1] += int(r["passed"])
    print(f"{'agent':<11}{'behaviour':<16}{'runs':>6}{'pass%':>7}")
    for (label, b), (n, ok) in sorted(agg.items()):
        print(f"{label:<11}{b:<16}{n:>6}{ok * 100 / n:>6.0f}%")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--tests")
    a = ap.parse_args()
    if a.db:
        from_db(a.db)
    if a.tests:
        from_tests(a.tests)
    if not (a.db or a.tests):
        ap.print_help()
