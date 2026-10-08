"""Keyword signal detector for seller speech (romanised Hindi/Hinglish + some English).

Used by the optional `adapt` HTTP tool and by evaluation scoring. Phrases come from
PS07 transcripts and objection categories (paraphrased, no seller data).
"""
from __future__ import annotations

import re

# Order matters: the first matching mode wins.
SIGNALS: list[tuple[str, str, str]] = [
    ("irritated", "EXIT",
     r"baar baar|roz roz|mat karo|band karo|disturb|pareshan|call mat|dobara call|don'?t call|stop calling"),
    ("bot_question", "TRANSPARENT",
     r"\bbot\b|robot|machine|recorded|recording|computer|\bai\b|insaan ho|real person"),
    ("wrong_contact", "REDIRECT",
     r"wrong number|galat number|main nahi hoon|woh nahi hai|owner nahi|number galat"),
    ("busy", "COMPRESS",
     r"busy|baad mein|abhi nahi|free nahi|time nahi|customer hai|drive kar|meeting mein|kal karo|thodi der"),
    ("already_met", "ACKNOWLEDGE",
     r"already|pehle se|aa chuke|mil chuke|aaye the|executive se baat|already member|pehle hi"),
    ("price", "INTEREST",
     r"kitna|price|paisa|paise|charge|fees|cost|rate|package|plan kya"),
    ("confused", "CLARIFY",
     r"kaun\b|kaun bol|kahan se|kya kaam|samjha nahi|samajh nahi|kya bola|kis liye|kyun call"),
]

GUIDANCE = {
    "COMPRESS": "Seller is busy. One sentence only: offer the two time options or ask when to call back.",
    "CLARIFY": "Seller is unsure who you are. Slowly say who you are, why you called and the benefit in one sentence, then ask again.",
    "ACKNOWLEDGE": "Seller already has contact with IndiaMART. Acknowledge it and offer a follow-up meeting with their executive.",
    "INTEREST": "Price question = interest. Answer briefly without numbers, then offer the two time options.",
    "TRANSPARENT": "Say honestly you are IndiaMART's AI assistant and offer a human executive callback.",
    "EXIT": "Seller is irritated. Apologise once, confirm no more calls, end the call. Outcome: do_not_call.",
    "REDIRECT": "Wrong person. Ask politely for the right person's name and a good time, or end.",
    "CONTINUE": "No special signal. Continue the normal flow.",
}


def detect(text: str) -> list[str]:
    t = (text or "").lower()
    return [name for name, _mode, pat in SIGNALS if re.search(pat, t)]


def mode_for(text: str) -> tuple[str, list[str]]:
    t = (text or "").lower()
    for name, mode, pat in SIGNALS:
        if re.search(pat, t):
            return mode, detect(text)
    return "CONTINUE", []
