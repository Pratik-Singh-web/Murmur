"""Build persona cards and a Sarvam campaign CSV.

Usage:
  python persona_engine/build_cards.py --sellers persona_engine/synthetic_sellers.csv --out out/
  python persona_engine/build_cards.py --sellers "../Persona Files/.../ps07_seller_files_part1.csv" --limit 500 --out out/real   # stays local, git-ignored

Outputs:
  cards.jsonl      one persona card per seller (what the agent receives)
  campaign.csv     all sellers: phone_number + one column per agent variable
  campaign_<variant>.csv  one file per voice variant (a Sarvam campaign runs one agent)
  summary.txt      persona mix
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rules import assign_persona, starting_language  # noqa: E402

HERE = Path(__file__).resolve().parent
GENDER_WORDS = {"female": {"bol_raha": "bol rahi hoon", "lunga": "lungi"},
                "male": {"bol_raha": "bol raha hoon", "lunga": "lunga"}}

# Variables sent to Sarvam. Order = campaign CSV column order.
CARD_FIELDS = [
    "seller_glid", "persona_id", "persona_label", "voice_variant", "language",
    "agent_name", "address", "company", "category", "city",
    "tone", "formality", "pitch_cap_turns", "opener", "value_hook", "ask",
    "slot_1", "slot_2", "avoid", "attempt_no", "attempt_note", "flag_note",
]


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def next_slots(now: datetime) -> tuple[str, str]:
    day = now + timedelta(days=1)
    while day.weekday() == 6:  # skip Sunday
        day += timedelta(days=1)
    label = "kal" if (day - now).days <= 1 else day.strftime("%A")
    return f"{label} subah 11 baje", f"{label} shaam 4 baje"


def build_card(row: dict, playbook: dict, now: datetime, attempt_no: int = 1) -> dict | None:
    a = assign_persona(row)
    if a.skip:
        return None
    p = playbook["personas"][a.persona_id]
    variant = playbook["voice_variants"][p["voice_variant"]]
    gender = variant.get("gender", "female")
    agent_name = variant.get("agent_name", "Simran")
    ov = playbook["overlays"]
    lang = starting_language(row.get("seller_state"), ov["language_by_state"])
    slot_1, slot_2 = next_slots(now)
    company = (row.get("company_name") or "").strip() or "aapke business"
    category = (row.get("top_category_1") or "").strip() or "aapke products"
    fill = SafeDict(address="ji", agent_name=agent_name, company=company, category=category,
                    slot_1=slot_1, slot_2=slot_2, **GENDER_WORDS[gender])
    opener_key = "opener_a" if int(str(row.get("fk_glusr_usr_id", "0"))[-1:] or 0) % 2 == 0 else "opener_b"
    att = ov["attempt"].get(str(min(attempt_no, 3)), {})
    cap = max(1, int(p["pitch_cap_turns"]) + int(att.get("pitch_cap_delta", 0)))
    flag_note = ""
    if str(row.get("already_in_touch_with_executive", "")).strip() in {"1", "1.0"}:
        flag_note = ov["flags"]["already_in_touch_with_executive"]
    return {
        "seller_glid": str(row.get("fk_glusr_usr_id", "")),
        "persona_id": a.persona_id,
        "persona_label": p["label"],
        "persona_reason": a.reason,           # kept in cards.jsonl for explainability, not sent to the agent
        "opener_variant": opener_key,
        "voice_variant": p["voice_variant"],
        "language": lang,
        "agent_name": agent_name,
        "address": "ji",
        "company": company,
        "category": category,
        "city": (row.get("seller_city") or "").strip(),
        "tone": p["tone"],
        "formality": p["formality"],
        "pitch_cap_turns": str(cap),
        "opener": p[opener_key].format_map(fill),
        "value_hook": p["value_hook"].format_map(fill),
        "ask": p["ask"].format_map(fill),
        "slot_1": slot_1,
        "slot_2": slot_2,
        "avoid": "; ".join(p.get("avoid", [])),
        "attempt_no": str(attempt_no),
        "attempt_note": att.get("note", ""),
        "flag_note": flag_note,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sellers", required=True)
    ap.add_argument("--out", default="out")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--playbook", default=str(HERE / "playbook.yaml"))
    args = ap.parse_args()

    playbook = yaml.safe_load(open(args.playbook, encoding="utf-8"))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    mix, skipped, n = Counter(), 0, 0
    per_variant: dict[str, list] = {}
    with open(args.sellers, newline="", encoding="utf-8") as f, \
         open(out / "cards.jsonl", "w", encoding="utf-8") as cj, \
         open(out / "campaign.csv", "w", newline="", encoding="utf-8") as cc:
        w = csv.writer(cc)
        w.writerow(["phone_number"] + CARD_FIELDS)
        for row in csv.DictReader(f):
            if args.limit and n >= args.limit:
                break
            n += 1
            card = build_card(row, playbook, now, attempt_no=int(float(row.get("attempt_no") or 1)))
            if card is None:
                skipped += 1
                continue
            mix[card["persona_id"]] += 1
            cj.write(json.dumps(card, ensure_ascii=False) + "\n")
            line = [row.get("phone_number", "")] + [card[k] for k in CARD_FIELDS]
            w.writerow(line)
            per_variant.setdefault(card["voice_variant"], []).append(line)
    for variant, lines_v in per_variant.items():
        with open(out / f"campaign_{variant}.csv", "w", newline="", encoding="utf-8") as fv:
            wv = csv.writer(fv)
            wv.writerow(["phone_number"] + CARD_FIELDS)
            wv.writerows(lines_v)
    lines = [f"sellers read: {n}", f"skipped (do-not-call): {skipped}"] + [
        f"{k}: {v} ({v * 100 / max(1, sum(mix.values())):.1f}%)" for k, v in mix.most_common()]
    (out / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"wrote {out/'cards.jsonl'} and {out/'campaign.csv'}")


if __name__ == "__main__":
    main()
