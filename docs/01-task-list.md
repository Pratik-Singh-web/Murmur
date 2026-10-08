# 01 — Task list

Living checklist. Update status in the same commit as the work. Status: `[ ]` todo · `[~]` in progress · `[x]` done · `[-]` dropped.

Owners: **P** = Pratik (Sarvam agent, adaptation, integration) · **E** = engineer (persona engine, service, eval harness) · **N** = non-tech member (persona playbook, scripts, test scenarios, skills.md, video).

> **Chosen problem: P4 — Seller-Fit Adaptive Voice Persona** (decided 8 Oct; confirm at the 10:30 statements on Day 1). Design: [scope](candidates/p4-persona-design/scope.md) · [architecture](candidates/p4-persona-design/architecture.md) · [pipelines](candidates/p4-persona-design/pipelines.md). Evidence: [research/ps07-data-analysis.md](../research/ps07-data-analysis.md).

---

## Phase 0 — Before the event (by Thu 8 Oct)

| Status | Task | Owner |
|---|---|---|
| [x] | Read the hackathon deck; list all problems | P |
| [x] | Rank problems; write the Day-1 gate | P |
| [x] | Check Sarvam agent platform: hooks, variables, webhooks, voices, states, tests | P |
| [x] | Create repo with docs and research; push to GitHub | P |
| [x] | Analyse organiser PS07 dataset (149k sellers, 269k bot calls, evaluators, transcripts) | P |
| [x] | Choose P4; define 6 personas + overlays + adaptation modes from the data | P |
| [x] | Keep organiser data out of git (`Persona Files/`, `*.csv` ignored) | P |
| [ ] | Make the GitHub repo private (organiser data findings are internal) | P |
| [ ] | Confirm team members; add them as collaborators; share the dataset locally (not via git) | P |
| [ ] | Each member: Sarvam account with Voice Agents access (indus.sarvam.ai/samvaad), laptop ready (Python 3.11, ngrok/cloudflared) | All |
| [ ] | N: read the P4 scope + data analysis; draft persona playbook tone notes (no code) | N |

No code and no Sarvam agents are created before Day 1 (pre-built solutions are disqualified).

## Phase 1 — Day 1 morning (Fri 9 Oct, 9:00–13:00)

| Status | Task | Owner |
|---|---|---|
| [ ] | 10:30: confirm the official PS07 statement, required outputs and metrics; update [scope](candidates/p4-persona-design/scope.md) if different | All |
| [ ] | Ask organisers: does a LiveKit build on Sarvam STT/TTS/LLM satisfy "built on Sarvam" and the agent-ID item? (decides path B vs A — [comparison](../research/voice-platform-comparison.md)) | P |
| [ ] | Ask Sarvam: mid-call voice/pace change on hosted agents? multi-agent? test-call limits? Bulbul v4 speakers per language / in API? | P |
| [ ] | Spike (1 h): LiveKit + `livekit-agents[sarvam]` — confirm `tts.update_options(speaker, pace)` changes the next utterance live; measure turn latency on web | P |
| [ ] | Ask organisers: may we use the dataset quotes in the demo (masked)? live A/B possible? | P |
| [ ] | Log answers in [05-decision-log](05-decision-log.md) | P |
| [ ] | Persona playbook v1 (YAML): 6 personas × tone, 2 openers, hook, pitch cap, objection lines, booking style | N + P |
| [ ] | Pick 3 voice variants (Warm / Formal / Brisk): speaker + pace per language; listen-test in Sarvam test panel | P + N |
| [ ] | Scaffold repo: `service/`, `agent/`, `playbook/`, `eval/`, `samples/`, `.env.example` | E |

## Phase 2 — Day 1 afternoon: end-to-end skeleton (13:00–20:00)

| Status | Task | Owner |
|---|---|---|
| [ ] | Persona engine v0: seller row → persona id + overlays → persona card (rules + templates) | E |
| [ ] | Synthetic seller cards (10) covering all personas and languages → `samples/` | E + N |
| [ ] | Path B: LiveKit agent worker with Sarvam STT/TTS/LLM; persona card from job metadata; `set_persona` tool (voice, pace, language, mode) | P |
| [ ] | Path A (thin): hosted Sarvam agent with the same prompt + persona variables — agent ID, baseline, fallback | P |
| [ ] | Path A: 3 voice variants; output variables (outcome, slot, signals) + goal rule (meeting fixed) | P |
| [ ] | FastAPI service: dialler (outbound API with `app_id` + `agent_variables`), on-end webhook, adapt tool endpoint, shared-secret auth; tunnel up | E + P |
| [ ] | First end-to-end call to a team phone: card → call → webhook stored | P + E |
| [ ] | Baseline agent: single "Payal" persona (today's script) for comparison | P |
| [ ] | Test scenarios: 6 personas × 5 behaviours (receptive, busy, sceptical/already met, price, hostile) from real objection patterns | N |

**End-of-day check:** two different seller cards produce two audibly different calls, and the webhook records the outcome.

## Phase 3 — Day 2 morning: adaptation + measurement (Sat 10 Oct, 9:00–13:00)

| Status | Task | Owner |
|---|---|---|
| [ ] | Live adaptation: busy → compress, who/why → clarify, already met → acknowledge, price → book, bot? → transparent, angry → exit, language switch | P |
| [ ] | Explicit booking confirmation (no meeting logged without "yes" + slot) | P |
| [ ] | Attempt overlay + next-attempt policy (callback timing, stop after attempt 4) | E |
| [ ] | Sarvam Tests: run scenario set on baseline vs seller-fit (×3 runs) | N + E |
| [ ] | Scoring script: MF, early drop, turns to ask, signal handling, false MF, persona fit | E |
| [ ] | Latency check: first bot turn ≤ 6 s, adapt tool < 800 ms | P |

## Phase 4 — Day 2 afternoon: submission (13:00–23:59, window opens 14:00)

| Status | Task | Owner |
|---|---|---|
| [ ] | Code freeze 18:00 | All |
| [ ] | Sample outputs: persona cards + call transcripts + eval table → `samples/` | E |
| [ ] | Approach note: data findings, persona design, platform constraints, adaptation, eval, business case, production A/B plan | P + N |
| [ ] | `skills.md` | N |
| [ ] | README final: setup, run, architecture image | P |
| [ ] | Record 5–7 min demo video (two contrasting live calls) | N + P |
| [ ] | Submit: video, approach note, Sarvam agent ID(s), repo, skills.md, sample outputs | P |
| [ ] | Tag `v1.0-submission` | P |

## Cut rules

Follow the cut list in the [P4 scope](candidates/p4-persona-design/scope.md#cut-list-in-order). **Never cut:** persona engine output, two contrasting live calls, busy-mode adaptation, baseline-vs-ours numbers.
