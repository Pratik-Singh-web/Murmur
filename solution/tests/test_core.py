"""Smoke tests. Run from solution/:  python tests/test_core.py"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "persona_engine"))
os.environ.setdefault("MURMUR_TOKEN", "t")
os.environ["MURMUR_DB"] = str(ROOT / "out" / "test.db")

from rules import assign_persona, should_dial  # noqa: E402
from service.policy import next_action  # noqa: E402
from service.signals import mode_for  # noqa: E402


def test_rules():
    assert assign_persona({"annual_turnover": "5 - 25 Cr"}).persona_id == "established_enterprise"
    assert assign_persona({"business_type": "Limited Company"}).persona_id == "established_enterprise"
    assert assign_persona({"eng_product_count": "80"}).persona_id == "established_enterprise"
    assert assign_persona({"gst_registration_year": "2025"}).persona_id == "new_seller"
    assert assign_persona({"nature_of_business": "Retailer", "gst_registration_year": "2015"}).persona_id == "busy_retailer"
    assert assign_persona({"nature_of_business": "Manufacturer"}).persona_id == "manufacturer"
    assert assign_persona({"nature_of_business": "Service Provider and Others"}).persona_id == "service_provider"
    assert assign_persona({}).persona_id == "trader_wholesaler"
    assert assign_persona({"do_not_call_requested": "1.0"}).skip
    assert should_dial(4, False) and not should_dial(5, False) and should_dial(7, True)


def test_signals():
    assert mode_for("abhi busy hoon baad mein")[0] == "COMPRESS"
    assert mode_for("kaun bol raha hai?")[0] == "CLARIFY"
    assert mode_for("aap bot ho kya")[0] == "TRANSPARENT"
    assert mode_for("baar baar call mat karo")[0] == "EXIT"
    assert mode_for("kitna paisa lagega")[0] == "INTEREST"
    assert mode_for("executive pehle se aa chuke hain")[0] == "ACKNOWLEDGE"
    assert mode_for("haan ji boliye")[0] == "CONTINUE"


def test_policy():
    assert next_action("meeting_fixed", 1)["action"] == "done"
    assert next_action("do_not_call", 1)["action"] == "stop"
    assert next_action("callback_scheduled", 2, "kal 4 baje")["action"] == "call_at"
    assert next_action("dropped_early", 4)["action"] == "stop"
    assert next_action("not_interested", 2)["action"] == "stop"


def test_api():
    from fastapi.testclient import TestClient
    from service.app import app
    c = TestClient(app)
    assert c.get("/health").json()["ok"]
    assert c.post("/tools/adapt", json={"utterance": "busy hoon"}, headers={"X-Murmur-Token": "t"}).json()["mode"] == "COMPRESS"
    assert c.post("/webhooks/sarvam?token=wrong", json={"interaction_id": "x"}).status_code == 401
    r = c.post("/webhooks/sarvam?token=t", json={"interaction_id": "smoke-1", "output_agent_variables": {"call_outcome": "meeting_fixed", "meeting_time": "kal 11"},
                                                  "interaction_transcript": [{"role": "agent"}, {"role": "user"}, {"role": "user"}]})
    assert r.json()["next_action"]["action"] == "done"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok ", name)
    print("all tests passed")
