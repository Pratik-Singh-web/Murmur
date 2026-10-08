"""Murmur service: Sarvam webhook receiver, optional `adapt` tool, results.

Run:  uvicorn service.app:app --port 8000   (from the solution/ folder)
Expose to Sarvam with a tunnel (ngrok/cloudflared) and use:
  webhook URL : https://<tunnel>/webhooks/sarvam?token=<MURMUR_TOKEN>
  adapt tool  : https://<tunnel>/tools/adapt   (header X-Murmur-Token: <MURMUR_TOKEN>)
"""
from __future__ import annotations

import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Request

from .policy import next_action
from .signals import GUIDANCE, mode_for

DB_PATH = Path(os.getenv("MURMUR_DB", Path(__file__).resolve().parent.parent / "out" / "murmur.db"))
TOKEN = os.getenv("MURMUR_TOKEN", "change-me")

app = FastAPI(title="Murmur — seller-fit persona service")

SCHEMA = """
CREATE TABLE IF NOT EXISTS calls (
  interaction_id TEXT PRIMARY KEY,
  received_at    TEXT DEFAULT CURRENT_TIMESTAMP,
  seller_glid    TEXT, persona_id TEXT, voice_variant TEXT, agent_label TEXT,
  attempt_no     INTEGER, duration REAL,
  call_outcome   TEXT, meeting_time TEXT, callback_time TEXT, signals_seen TEXT,
  user_turns     INTEGER, agent_turns INTEGER,
  next_action    TEXT, raw TEXT
);
"""


def db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute(SCHEMA)
    return con


def _check(token: str | None) -> None:
    if token != TOKEN:
        raise HTTPException(status_code=401, detail="bad token")


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/webhooks/sarvam")
async def sarvam_webhook(request: Request, token: str | None = None) -> dict:
    _check(token)
    payload = await request.json()
    iid = payload.get("interaction_id") or payload.get("attempt_id")
    if not iid:
        raise HTTPException(status_code=400, detail="missing interaction_id")
    fv = payload.get("final_agent_variables") or {}
    ov = payload.get("output_agent_variables") or {}
    md = payload.get("metadata") or {}
    turns = payload.get("interaction_transcript") or []
    attempt_no = int(str(md.get("attempt_no") or fv.get("attempt_no") or 1))
    outcome = ov.get("call_outcome") or fv.get("call_outcome") or ""
    user_turns = sum(1 for t in turns if t.get("role") == "user")
    if not outcome and user_turns <= 1:
        outcome = "dropped_early"
    nxt = next_action(outcome, attempt_no, ov.get("callback_time", ""))
    row = (
        iid, str(md.get("seller_glid") or fv.get("seller_glid") or ""),
        md.get("persona_id") or fv.get("persona_id"), md.get("voice_variant") or fv.get("voice_variant"),
        md.get("agent_label", "seller_fit"), attempt_no, payload.get("duration"),
        outcome, ov.get("meeting_time", ""), ov.get("callback_time", ""), ov.get("signals_seen", ""),
        user_turns, sum(1 for t in turns if t.get("role") == "agent"),
        json.dumps(nxt, ensure_ascii=False), json.dumps(payload, ensure_ascii=False),
    )
    with closing(db()) as con, con:
        con.execute("INSERT OR IGNORE INTO calls (interaction_id, seller_glid, persona_id, voice_variant, agent_label,"
                    " attempt_no, duration, call_outcome, meeting_time, callback_time, signals_seen, user_turns,"
                    " agent_turns, next_action, raw) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row)
    return {"stored": iid, "next_action": nxt}


@app.post("/tools/adapt")
async def adapt(request: Request, x_murmur_token: str | None = Header(default=None)) -> dict:
    """HTTP tool for the Sarvam agent: send the seller's last utterance, get a mode + one-line guidance.
    In Sarvam, map the response fields `mode` and `guidance` into agent variables ('Save reply into variables')."""
    _check(x_murmur_token)
    body = await request.json()
    mode, signals = mode_for(body.get("utterance", ""))
    return {"mode": mode, "guidance": GUIDANCE[mode], "signals": ",".join(signals)}


@app.get("/results")
def results(token: str | None = None) -> dict:
    _check(token)
    with closing(db()) as con:
        rows = con.execute("SELECT agent_label, persona_id, call_outcome, COUNT(*) FROM calls "
                           "GROUP BY 1,2,3 ORDER BY 1,2,3").fetchall()
    return {"rows": [dict(zip(["agent", "persona", "outcome", "calls"], r)) for r in rows]}
