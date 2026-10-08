"""Place one outbound call through Sarvam with the right voice variant and persona card.

Usage (from solution/):
  python -m service.dial --card-glid 900000010 --phone +9198XXXXXXXX --dry-run
  python -m service.dial --card-glid 900000010 --phone +9198XXXXXXXX            # real call
  python -m service.dial --card-glid 900000010 --phone +9198XXXXXXXX --baseline # 'before' agent

Reads settings from .env (see .env.example) and cards from out/cards.jsonl.
API: POST https://apps.sarvam.ai/api/outbounds/v1/orgs/{org}/workspaces/{ws}/outbounds
(docs.sarvam.ai/conversations/api/instant-outbound/create). Auth header name is configurable
because the docs page doesn't state it — confirm in the Sarvam console (API keys page).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
SEND_KEYS = ["seller_glid", "persona_id", "persona_label", "voice_variant", "language", "agent_name", "address",
             "company", "category", "city", "tone", "formality", "pitch_cap_turns", "opener", "value_hook", "ask",
             "slot_1", "slot_2", "avoid", "attempt_no", "attempt_note", "flag_note"]


def load_env(path: Path) -> None:
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip() and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def find_card(glid: str, cards: Path) -> dict:
    for line in cards.read_text(encoding="utf-8").splitlines():
        c = json.loads(line)
        if c["seller_glid"] == glid:
            return c
    sys.exit(f"no card for {glid} in {cards} — run persona_engine/build_cards.py first")


def build_payload(card: dict, phone: str, baseline: bool) -> dict:
    variant = "BASELINE" if baseline else card["voice_variant"].upper()
    app_id = os.environ.get(f"SARVAM_APP_ID_{variant}")
    version = int(os.environ.get(f"SARVAM_APP_VERSION_{variant}", "1"))
    if not app_id:
        sys.exit(f"set SARVAM_APP_ID_{variant} in .env")
    lang = card.get("language", "Hindi")
    webhook = os.environ.get("MURMUR_PUBLIC_URL", "").rstrip("/")
    payload = {
        "app_config": {
            "app_id": app_id,
            "app_version": version,
            "connection_config": {
                "connection_id": os.environ["SARVAM_CONNECTION_ID"],
                "agent_phone_number": os.environ["SARVAM_AGENT_PHONE"],
            },
            "agent_variables": {k: card.get(k, "") for k in SEND_KEYS},
            "app_overrides": {"initial_language_name": lang},
        },
        "user_config": {"user_phone_number": phone},
    }
    if webhook:
        payload["webhook_config"] = {
            "url": f"{webhook}/webhooks/sarvam?token={os.environ.get('MURMUR_TOKEN', 'change-me')}",
            "metadata": {"seller_glid": card["seller_glid"], "persona_id": card["persona_id"],
                         "voice_variant": card["voice_variant"], "attempt_no": card.get("attempt_no", "1"),
                         "agent_label": "baseline" if baseline else "seller_fit"},
        }
    return payload


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--card-glid", required=True)
    ap.add_argument("--phone", required=True, help="E.164, e.g. +9198XXXXXXXX (must be whitelisted / your own)")
    ap.add_argument("--cards", default=str(ROOT / "out" / "cards.jsonl"))
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    load_env(ROOT / ".env")
    card = find_card(args.card_glid, Path(args.cards))
    payload = build_payload(card, args.phone, args.baseline)
    url = (f"https://apps.sarvam.ai/api/outbounds/v1/orgs/{os.environ['SARVAM_ORG_ID']}"
           f"/workspaces/{os.environ['SARVAM_WORKSPACE_ID']}/outbounds")
    if args.dry_run:
        print(url)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    headers = {os.environ.get("SARVAM_AUTH_HEADER", "api-subscription-key"): os.environ["SARVAM_API_KEY"],
               "Content-Type": "application/json"}
    r = httpx.post(url, json=payload, headers=headers, timeout=30)
    print(r.status_code, r.text)


if __name__ == "__main__":
    main()
