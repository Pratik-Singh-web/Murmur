# 02 — What we are building

> **Problem not decided yet.** Official problem statements are presented on Day 1 (Fri 9 Oct, 10:30). We decide by **13:00 on Day 1** using the criteria and gate below, then fill in the "Final choice" section and log it in [05-decision-log](05-decision-log.md).

## What is fixed regardless of the problem

- **A voice AI solution for an IndiaMART use case, built on Sarvam** (Saaras STT, Bulbul TTS, Sarvam LLM, Voice Agents).
- **Built entirely on 9–10 Oct.** Pre-built solutions are disqualified; this repo holds only planning until Day 1.
- **Team of 3**, at least one non-tech member. One problem per team.
- **No customer data leaves the premises.**
- **Deliverables:** 5–7 min demo video, approach note, Sarvam agent ID / live link, code + README, `skills.md`, sample outputs.

## How we will be judged

| Criterion | Weight | What it means for our choice |
|---|---|---|
| Business Impact | 25% | Pick a problem with a measurable IndiaMART outcome (calls saved, conversion, cost) |
| Solution Completeness | 20% | Pick something we can finish end to end in ~1.5 days |
| Technical Robustness | 20% | Prefer designs with clear failure handling over clever ones |
| Voice Experience | 20% | The demo must be a live, natural voice conversation, not a dashboard |
| Demo & skills.md | 15% | Clear story, numbers, reusable skills file |

## Candidate problems (from the deck — confirm on Day 1)

| # | Problem | One line | Our current view |
|---|---|---|---|
| P1 | Quality Audit | Audit VANI calls for quality | High impact, but 6 components + dashboard; weak voice score |
| **P2** | **Global Context: Memory Across Channels** | `buyer.md` / `seller.md` per GLID, loaded before each call/chat, resumes across channels | **Leading candidate** — strong data edge if Call Insights is allowed |
| P3 | Best Time to Call | Predict when to call | Pure modelling, near-zero voice score |
| **P4** | **Persona Design** | Agent persona adapts to the seller, switching live mid-call | **Fallback** — strongest voice demo; mid-call voice switching unconfirmed on Sarvam |
| P5 | A/B + Auto-rollout | Experiment platform for agent variants | Platform + stats; results synthetic |
| P6 | Seller Enrichment | Enrich seller profiles | External sources, privacy scrutiny |

The deck says 7 problems but shows 6 — check for a missing one on Day 1. Full reasoning: [research/problem-selection.md](../research/problem-selection.md). Overview of all candidates: [candidates/](candidates/README.md).

## Selection criteria (scored on Day 1)

Score each problem 1–5, weight by the rubric, plus two gates:

| Criterion | Weight |
|---|---|
| Business impact we can show with a number | 25% |
| Can we finish it end to end in the time? | 20% |
| Technical robustness achievable | 20% |
| Voice experience in the demo | 20% |
| Demo story clarity | 15% |

**Gates (fail = drop the problem):**
1. **Data access** — the data the solution needs is available to code during the event.
2. **Platform fit** — Sarvam supports what the solution needs (or we have a workable path around it).

Tie-breakers: unfair advantage (data or insight other teams lack), and work the non-tech member can own.

## Day-1 decision gate

Questions to settle in the 10:30 session and on the floor (also in [01-task-list](01-task-list.md)):

| Ask | Who | Decides |
|---|---|---|
| Starter API list + sample GLIDs for P2 | Organisers | P2 feasibility |
| Is Call Insights / PNS an allowed source, and how can code read it? | Organisers | P2 data edge |
| May per-GLID context be sent to the Sarvam-hosted agent? | Organisers | P2 privacy |
| Can speaker / speed / pitch / language change mid-call (tool, API, handoff)? Multi-agent available? | Sarvam | P4 feasibility |
| Is there a chat / WhatsApp channel for agents? | Sarvam | P2 second channel |
| Does a LiveKit/Pipecat build count for the "agent ID" item? | Sarvam | P4 build path |

Rule of thumb (current): organiser answers OK → **P2**. Call Insights not allowed → P4 if Sarvam confirms mid-call switching, otherwise P2 on starter APIs.

## Final choice

| Field | Value |
|---|---|
| Problem | _TBD — Day 1, by 13:00_ |
| Why | _TBD_ |
| What we build (one line) | _TBD_ |
| Success metrics | _TBD (copy from the official problem statement)_ |
| Demo story | _TBD_ |
| Detailed design | `docs/candidates/<chosen>/` |

## Prepared candidate designs

- [P2 — Global Context](candidates/p2-global-context/scope.md) — scope, architecture, pipelines (detailed)
- [P4 — Persona Design](candidates/p4-persona-design.md) — sketch and open questions
