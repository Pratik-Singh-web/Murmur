# 01 — Task list

Living checklist. Update status in the same commit as the work. Status: `[ ]` todo · `[~]` in progress · `[x]` done · `[-]` dropped.

Owners: **P** = Pratik · **E** = engineer · **N** = non-tech member. Roles get confirmed once the problem is chosen.

> **Problem not chosen yet.** Phases 0–1 and the generic tasks apply to any problem. Problem-specific tasks are listed per candidate and get activated after the Day-1 decision.

---

## Phase 0 — Before the event (by Thu 8 Oct)

| Status | Task | Owner |
|---|---|---|
| [x] | Read the hackathon deck; list all problems | P |
| [x] | Size per-GLID data in Call Insights (coverage, repeat behaviour, timing) | P |
| [x] | Rank candidates: P2 leading, P4 fallback, P1 third; write the Day-1 gate | P |
| [x] | Check Sarvam agent platform: hooks, variables, webhooks, models, gaps | P |
| [x] | Create repo with docs and research | P |
| [ ] | Push repo to GitHub (private) | P |
| [ ] | Confirm team members; add them as collaborators | P |
| [ ] | Each member: Sarvam access, laptop ready (Python 3.11, Node 20, ngrok/cloudflared) | All |
| [ ] | Everyone reads docs 02–04 and the two candidate designs | All |

No code is written before Day 1 (pre-built solutions are disqualified).

## Phase 1 — Day 1 morning: choose the problem (Fri 9 Oct, 9:00–13:00)

| Status | Task | Owner |
|---|---|---|
| [ ] | Attend problem statements (10:30); confirm the list (deck shows 6, says 7) | All |
| [ ] | Ask organisers: starter APIs + sample GLIDs; is Call Insights allowed and readable by code; may per-GLID data go to Sarvam? | P |
| [ ] | Ask Sarvam: chat/WhatsApp channel? mid-call voice/pace/language switch? multi-agent? does a LiveKit/Pipecat build count for "agent ID"? | P |
| [ ] | Score shortlisted problems with the rubric ([doc 02](02-what-we-are-building.md#selection-criteria-scored-on-day-1)) | All |
| [ ] | **Decide by 13:00**; fill "Final choice" in doc 02; log in [05-decision-log](05-decision-log.md) | P |
| [ ] | Assign owners for every component | P |

## Phase 2 — Day 1 afternoon: skeleton end to end (13:00–20:00)

Generic (any problem):

| Status | Task | Owner |
|---|---|---|
| [ ] | Scaffold repo: `service/`, `agent/`, `eval/`, `samples/`, `.env.example` | E |
| [ ] | FastAPI service with `/health`, on-start hook, on-end webhook, shared-secret auth | E |
| [ ] | Tunnel up; Sarvam can reach the service | P |
| [ ] | Sarvam agent v0: greeting, system prompt, variables, language settings | P |
| [ ] | First end-to-end call: hook → agent → webhook stored | P + E |
| [ ] | Demo scenarios (3) in Hindi/Hinglish + English | N |
| [ ] | Evaluation sheet: cases + what "good" looks like | N |

If **P2 — Global Context** ([design](candidates/p2-global-context/scope.md)):

| Status | Task | Owner |
|---|---|---|
| [ ] | `buyer.md` / `seller.md` templates (fixed sections, ≤ ~400 tokens) | E + P |
| [ ] | Ingest sample GLIDs from allowed sources into the event store | E |
| [ ] | Context builder v0 (templates only) + `GET /context/{glid}`, `POST /events` | E |
| [ ] | On-start hook returns context → agent variables; on-end webhook → event → rebuild | P |

If **P4 — Persona Design** ([sketch](candidates/p4-persona-design.md)):

| Status | Task | Owner |
|---|---|---|
| [ ] | Persona specs (3–4) and selection rules from organiser seller data | N + P |
| [ ] | Agent states / prompts per persona; switch triggers | P |
| [ ] | Decide hosted (tone/language switch) vs code-first (voice switch) based on Sarvam answer | P |

**End-of-day check:** one real call completes the full loop for the chosen problem.

## Phase 3 — Day 2 morning: complete + measure (Sat 10 Oct, 9:00–13:00)

| Status | Task | Owner |
|---|---|---|
| [ ] | Finish the core feature for the chosen problem (P2: chat channel + cross-channel resume; P4: live switch) | P |
| [ ] | Guardrails: wrong person, stale or missing data, fallbacks | P |
| [ ] | Latency and freshness logging | E |
| [ ] | Eval run: baseline vs ours, 20–30 simulated cases + 3–5 real calls | N + E |

## Phase 4 — Day 2 afternoon: submission (13:00–23:59, window opens 14:00)

| Status | Task | Owner |
|---|---|---|
| [ ] | Code freeze 18:00 | All |
| [ ] | Sample outputs (synthetic/masked) → `samples/` | E |
| [ ] | Approach note | P + N |
| [ ] | `skills.md` | N |
| [ ] | README final: setup, run, architecture image | P |
| [ ] | Record 5–7 min demo video | N + P |
| [ ] | Submit: video, approach note, Sarvam agent ID / live link, repo, skills.md, sample outputs | P |
| [ ] | Tag `v1.0-submission` | P |

## Cut rules (if time runs out)

Cut polish and secondary features first; **never cut** the live voice demo, the end-to-end loop, or the baseline-vs-ours number. Problem-specific cut lists go in the chosen candidate's scope doc.
