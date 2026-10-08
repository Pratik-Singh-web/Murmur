# Problem selection research

> **Status: recommendation, not a decision.** Updated 8 Oct 2026. The problem is chosen on Day 1 (see [docs/02](../docs/02-what-we-are-building.md)). Figures are aggregates from IndiaMART Call Insights (RFQ calls to paid sellers); they are directional and a lower bound. No customer-level data here.

## Recommendation (conditional on the Day-1 gate)

- Primary: **Problem 2 — Global Context: Memory Across Channels** (`buyer.md` / `seller.md` keyed by GLID, loaded by VANI before each call/chat, resumes across voice + chat/WhatsApp).
- Fallback: **Problem 4 — Persona Design**, only if the P2 data gate fails AND Sarvam confirms mid-call switching.
- Third: Problem 1.
- "Sarvam tools are free" is not a reason to switch: every team gets the same keys/credits (deck slide 22).

## Hackathon facts (from the deck)

- Fri 9 Oct (build) + Sat 10 Oct (build & submit), 11th floor, 9 AM. Problem statements + Sarvam walkthrough 10:30 on Day 1. Submission 2 PM–11:59 PM Day 2.
- Teams of 3, at least 1 non-tech. One problem per team. All build work during the 2 days; pre-built solutions disqualified. No customer data leaves the premises.
- Must build on Sarvam (Saaras STT, Bulbul TTS, Sarvam LLM/Mayura, Voice Agents). Submit: 5–7 min demo video, approach note, Sarvam agent ID/live link, code + README, skills.md, sample outputs.
- Rubric (1–5 per juror): Business Impact 25%, Solution Completeness 20%, Technical Robustness 20%, Voice Experience 20%, Demo & skills.md 15%.
- Deck says 7 problems but shows 6 (Seller Enrichment labelled "Problem 7 of 6"). Check on Day 1.

## Problem 2 — required outputs and metrics

- Outputs: generated buyer.md + seller.md for sample GLIDs; demo of a conversation resuming across two channels; note on sources, lookback window, refresh logic.
- Metrics: freshness (activity → file update delay), compactness/structure, conversations resumed without re-asking, lift from the personalised opening, reusability beyond the bot prompt.
- Sources: "starter API list provided, others allowed".

## Per-GLID data availability (verified 8 Oct 2026; window 8 Sep–7 Oct unless stated)

**Have:**

- ~1.08M RFQ calls in 30 days; 100% carry both a buyer GLID and a seller GLID, every day.
- Buyers: ~673K GLIDs; median 1 RFQ; 26.8% have 2+, 10.9% 3+, 3.4% 5+; 0.07% have 30+ (likely pooled accounts — exclude from demos). 90 days (calls ≥30 s): ~1.65M buyers; 29.8% 2+, 13.5% 3+, 4.9% 5+ — tripling the window adds only ~3 pts of buyers with 2+.
- Sellers: ~85K GLIDs; median 2 RFQs received; p90 36, p99 125, max ~1,280; 12.1% have 30+ → seller.md must be an aggregate.
- Per-call fields reachable by GLID: products/specs/quantity, quoted prices, call_purpose, deal_readiness, call_outcome (+notes), buyer_intent, deal_blockers, buyer questions + seller answers, next steps, languages, buyer_city (~24% filled), buyer_persona (~55%).

**Don't have:**

- Names/phones, KYC, search/browse history, BuyLead enquiries, WhatsApp/chat history, seller profile/turnover.
- Callbacks: not extracted since 11 Sep (~1.3% fill) → don't build "open loops" on callbacks; use next_steps + blockers.
- VANI's own calls (this is buyer↔paid-seller RFQ data). LLM-extracted; extraction regimes changed 4 Sep, 23 Sep, 30 Sep — don't trend readiness/blocker shares.

**Unverified (decisive):**

- Whether Call Insights is an allowed source and whether code can read it during the event.
- Whether per-GLID facts may be sent to the Sarvam-hosted agent under "no customer data leaves the premises".
- What the organisers' starter APIs cover for sample GLIDs.

## Repeat behaviour — sizes the "users repeat themselves" problem

- **12.0%** of buyers with a categorised RFQ came back about the same most-specific category 2+ times in 30 days; 2.9% 3+ times. **79.3%** of repeaters spoke to 2+ different sellers → context must be about the buyer's need, not one seller. Lower bound (paid sellers only).
- Timing (same buyer + category, consecutive RFQs, right-censored): median gap **≈18 min**; 64.9% within 1 h, 82.7% within 24 h, 95.0% within 7 d.
- Implication: freshness target is minutes. Call Insights extraction is same-day, so it can't serve same-hour repeats; VANI's own on-end write-back must. Call Insights supplies older context (language, categories, blockers, sellers contacted).

## Corrections to the 5 Oct note

- Old "18.8% of buyers / 35.8% of calls repeat the category" used `files.src_mcat_id` (matches the real category on only ~19% of products). Replaced by 12.0%.
- "Ingested within minutes" → documented same-day extraction.
- Earlier 90-day counts included calls under 30 s before 1 Sep; replaced.
- Callback promises dropped as a buyer.md section. "28.6% of requirement calls have a blocker" blends extraction regimes (26–34%) — quote as ~30%, directional.

## Persona Design (P4) check — 8 Oct

- Sarvam docs: the speaker chosen at call start stays fixed; speed and pitch are agent-level sliders; no documented tool/API to change voice, speed, pitch or language mid-call; "switch language during call" exists.
- Multi-state agents: per-state instructions + tools only; no per-state speaker/language/pace; Sarvam plans to end-of-life multi-state once multi-agent launches.
- So live mid-call switching is feasible for wording/tone/language on the hosted agent; voice/pace/pitch likely needs a code-first pipeline (LiveKit/Pipecat + Saaras/Bulbul), which is heavy and may clash with the "Agent ID" submission item.
- "Evidence from past calls" can't be causal: VANI used one persona historically.
- Upsides: data provided, strongest voice demo, non-tech member can own persona spec, Sarvam experts on the floor.

## Day-1 gate (decide by 1 PM)

- Ask organisers: (1) starter API list + sample GLIDs for P2; (2) is Call Insights an allowed source and how can code read it; (3) may per-GLID context be sent to the Sarvam agent.
- Ask Sarvam: can speaker/speed/pitch/language change mid-call? Is multi-agent available? Does a LiveKit/Pipecat build satisfy "Agent ID"?
- Rule: (1)–(3) OK → P2. If (2) fails → P4 only if Sarvam confirms mid-call switching (or the team accepts language+tone switching); otherwise P2 on starter APIs, winning on design, measured lift and demo.

## Why not the others

- **P1 Quality Audit:** high impact but 6 components + dashboard; needs VANI transcripts + human audit labels; weak voice score.
- **P3 Best Time to Call:** pure modelling, near-zero voice score, counterfactual validation is hard; no VANI dial attempts in Call Insights.
- **P5 A/B + Auto-rollout:** platform + stats + simulated sellers; no data edge; results synthetic.
- **P6 Seller Enrichment:** external sources/scraping, privacy scrutiny; small edge.

## Risks (P2)

- Crowded problem → win on data depth, measured lift, language-aware opener, freshness design backed by the repeat-timing data.
- Wrong memory is worse than none → structured, dated facts only.
- Call Insights covers paid sellers' RFQ calls only → free-seller files and many buyer fields rely on starter APIs.
- Access and privacy unconfirmed (see gate).
