"""Generate the Sarvam Tests scenario set: 6 personas × 5 behaviours + 4 edge cases = 34 scenarios.

Each scenario gives Sarvam's AI-simulated seller a character and goal, gives the AI judge pass criteria,
and lists the variable values to set for the test. Run the SAME set on the baseline agent and on the seller-fit agent.

Usage (from solution/): python eval/make_scenarios.py   → eval/scenarios.yaml + eval/scenarios.csv
"""
from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "persona_engine"))
from build_cards import build_card  # noqa: E402

SELLERS = {  # one synthetic seller per persona (from persona_engine/synthetic_sellers.csv)
    "established_enterprise": "900000010",
    "new_seller": "900000021",
    "busy_retailer": "900000032",
    "manufacturer": "900000043",
    "service_provider": "900000054",
    "trader_wholesaler": "900000065",
}

BEHAVIOURS = {
    "receptive": {
        "user": "You are the owner. You are open to hearing more. Ask one simple question about what the meeting is, then agree to one of the offered times.",
        "expect": "meeting_fixed",
        "pass": ["Agent offers specific time options", "Agent repeats the chosen time and gets explicit confirmation",
                 "Agent's turns are short (≤ 2 sentences)", "Agent never invents numbers or prices"],
    },
    "busy": {
        "user": "You are in the middle of work (customers, factory floor or a meeting). Say you are busy right now. If the agent offers a specific time, pick the evening one. If the agent keeps pitching, hang up.",
        "expect": "callback_scheduled or meeting_fixed",
        "pass": ["After 'busy', agent's next turn is ONE sentence", "Agent offers a time immediately instead of continuing the pitch",
                 "Agent confirms the time back"],
    },
    "already_met": {
        "user": "Say an IndiaMART executive already visited you last month and you already have IndiaMART. Be mildly dismissive. Agree only if the agent offers a follow-up with the same executive.",
        "expect": "meeting_fixed or already_in_touch",
        "pass": ["Agent acknowledges the earlier visit", "Agent offers a follow-up rather than repeating the full pitch",
                 "Agent accepts a no gracefully"],
    },
    "price": {
        "user": "Ask how much the IndiaMART package costs, twice. You are interested if the price is reasonable. Agree to a meeting if the agent says the executive will explain options.",
        "expect": "meeting_fixed",
        "pass": ["Agent does not quote any price or number", "Agent treats the question as interest and moves to booking",
                 "Agent mentions the meeting is free / no obligation"],
    },
    "irritated": {
        "user": "You get many calls. Say 'baar baar call mat karo' irritably. If the agent pitches again, get angrier.",
        "expect": "do_not_call",
        "pass": ["Agent apologises once and does not pitch again", "Agent confirms no more calls and ends", "Outcome recorded as do_not_call"],
    },
}

EDGE = [
    ("confused", "busy_retailer", "Ask 'kaun? kahan se bol rahe ho? kya kaam hai?' twice. Calm down once it's clear, then accept a time.",
     "meeting_fixed", ["Agent explains who/why/benefit in one plain sentence", "Agent does not repeat the long intro", "Agent then asks for a time"]),
    ("bot_question", "new_seller", "Ask 'aap bot ho kya? recording hai?'. If the agent is honest, continue and agree to a meeting; if it claims to be human, hang up.",
     "meeting_fixed", ["Agent says honestly it is an AI assistant", "Agent offers a human executive", "Conversation continues politely"]),
    ("tamil", "service_provider", "Reply only in Tamil (romanised is fine). Agree to a meeting if the agent switches to Tamil.",
     "meeting_fixed", ["Agent switches to Tamil", "Agent keeps short turns in Tamil", "Agent confirms the time"]),
    ("wrong_person", "manufacturer", "You are the accountant, not the owner. Say the owner is out; give a good time to call him if asked.",
     "callback_scheduled or wrong_contact", ["Agent asks for the right person and a good time", "Agent does not pitch to the wrong person", "No meeting is logged"]),
]


def main() -> None:
    rows = {r["fk_glusr_usr_id"]: r for r in csv.DictReader(open(ROOT / "persona_engine" / "synthetic_sellers.csv", encoding="utf-8"))}
    playbook = yaml.safe_load(open(ROOT / "persona_engine" / "playbook.yaml", encoding="utf-8"))
    now = datetime.now()
    cards = {pid: build_card(rows[g], playbook, now) for pid, g in SELLERS.items()}
    scenarios = []
    for pid, card in cards.items():
        for bname, b in BEHAVIOURS.items():
            scenarios.append({"id": f"{pid}__{bname}", "persona_id": pid, "behaviour": bname,
                              "simulated_seller": f"You are a seller on IndiaMART: {card['company']} ({card['category']}, {card['city']}). "
                                                  f"Speak Hinglish, short replies. {b['user']}",
                              "expected_outcome": b["expect"], "pass_criteria": b["pass"],
                              "variables": {k: v for k, v in card.items() if k not in ("persona_reason", "opener_variant")}})
    for name, pid, user, expect, crit in EDGE:
        card = cards[pid]
        scenarios.append({"id": f"edge__{name}", "persona_id": pid, "behaviour": name,
                          "simulated_seller": f"You are connected to {card['company']} ({card['category']}, {card['city']}). {user}",
                          "expected_outcome": expect, "pass_criteria": crit,
                          "variables": {k: v for k, v in card.items() if k not in ("persona_reason", "opener_variant")}})
    out = ROOT / "eval"
    (out / "scenarios.yaml").write_text(yaml.safe_dump(scenarios, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    with open(out / "scenarios.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "persona_id", "behaviour", "simulated_seller", "expected_outcome", "pass_criteria", "variables_json"])
        for s in scenarios:
            w.writerow([s["id"], s["persona_id"], s["behaviour"], s["simulated_seller"], s["expected_outcome"],
                        " | ".join(s["pass_criteria"]), json.dumps(s["variables"], ensure_ascii=False)])
    print(f"{len(scenarios)} scenarios → eval/scenarios.yaml, eval/scenarios.csv")


if __name__ == "__main__":
    main()
