"""Next-attempt policy after a call (from PS07: MF 16.3% on attempt 1 → ≤3.3% from attempt 5)."""
from __future__ import annotations

STOP_AFTER = 4


def next_action(outcome: str, attempt_no: int, callback_time: str = "") -> dict:
    outcome = (outcome or "").strip()
    if outcome == "meeting_fixed":
        return {"action": "done", "why": "meeting booked — hand over to the executive"}
    if outcome in {"do_not_call", "wrong_contact"}:
        return {"action": "stop", "why": f"{outcome} — never dial again"}
    if outcome == "already_in_touch":
        return {"action": "handover", "why": "seller is with an executive — notify that executive instead of re-calling"}
    if outcome == "callback_scheduled" and callback_time:
        return {"action": "call_at", "when": callback_time, "attempt_no": attempt_no + 1,
                "opener_note": "As promised — seller asked for this time."}
    if attempt_no >= STOP_AFTER:
        return {"action": "stop", "why": f"attempt {attempt_no} reached; yield ≤3.3% beyond this"}
    if outcome == "dropped_early":
        return {"action": "retry", "attempt_no": attempt_no + 1, "change": "use the other opener variant"}
    if outcome == "not_interested":
        return {"action": "retry_later" if attempt_no == 1 else "stop",
                "attempt_no": attempt_no + 1, "why": "one soft retry after a first 'no', then stop"}
    return {"action": "retry", "attempt_no": attempt_no + 1}
