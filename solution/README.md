# Murmur solution — Seller-Fit Adaptive Voice Persona

VANI picks a persona that fits each seller before dialling (voice, speed, tone, opener, language) and adapts it live (busy → compress, confused → clarify, already met → acknowledge, price → book, bot? → honest, irritated → exit, other language → switch). Everything runs on **Sarvam Voice Agents**; this folder holds the persona engine, the agent configuration, a small results service and the evaluation.

**Start here → [SETUP_GUIDE.md](SETUP_GUIDE.md)** (step by step, with why).

| Folder | What | Key files |
|---|---|---|
| `persona_engine/` | Seller row → persona card → Sarvam campaign CSV | `playbook.yaml` (edit personas here), `rules.py`, `build_cards.py`, `synthetic_sellers.csv` |
| `agent/` | Everything you paste into the Sarvam console | `system_prompt.md`, `variables.md`, `knowledge_base.md`, `variants.md`, `states.md`, `baseline_agent.md` |
| `service/` | Webhook receiver, `adapt` tool, next-attempt policy, outbound dialler | `app.py`, `dial.py`, `policy.py`, `signals.py` |
| `eval/` | 34 test scenarios + scoring | `make_scenarios.py`, `scenarios.csv`, `score.py` |
| `tests/` | Smoke tests | `python tests/test_core.py` |

Design and evidence: [P4 scope](../docs/candidates/p4-persona-design/scope.md) · [architecture](../docs/candidates/p4-persona-design/architecture.md) · [data analysis](../research/ps07-data-analysis.md).

Data rule: the organiser seller files never go into git. `out/` and `.env` are ignored; the synthetic sellers are fictional.
