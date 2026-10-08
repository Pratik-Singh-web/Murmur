# P2 — Global Context: scope (candidate, not final)

> Candidate design for Problem 2. Used only if P2 is chosen at the Day-1 gate. Shared stack: [../../03-architecture.md](../../03-architecture.md).

## One line

A per-GLID memory file that VANI reads before every call or chat and rewrites after it, so buyers and sellers never have to repeat themselves across channels.

## The problem

VANI talks to buyers and sellers over voice, and IndiaMART also reaches them over chat/WhatsApp. Each conversation starts cold. The user re-explains the product, quantity, city and language they already gave.

How often this happens (Call Insights, 8 Sep–7 Oct 2026, paid-seller RFQ calls only — a lower bound; details in [research/problem-selection.md](../../../research/problem-selection.md)):

- **12%** of buyers came back about the same category 2+ times in 30 days.
- **79%** of those repeaters spoke to 2+ different sellers → the memory must be about the **buyer's need**, not one seller.
- Repeats are fast: median gap **~18 min**, 65% within 1 hour, 83% within 24 hours → the memory must refresh in **minutes**, not overnight.

## Users

| User | What they get |
|---|---|
| Buyer | VANI opens with "Last time you asked for 500 kg of HDPE granules for Kanpur — still looking?" in their language, and doesn't re-ask known details |
| Seller | VANI knows their categories, recent enquiry patterns and open follow-ups |
| IndiaMART | Shorter calls, higher completion, a reusable profile other bots and teams can read |

## What we build (scope)

1. **`buyer.md` and `seller.md` per GLID** — markdown, ≤ ~400 tokens, fixed sections:
   - **Who:** city, B2B/B2C, preferred language
   - **Active needs:** product, specs, quantity, budget/price seen — each with a date
   - **Last 3 interactions:** channel, date, outcome
   - **Open loops:** next steps and blockers from the last conversations
   - **Don't re-ask:** facts already confirmed
   - Seller file is an aggregate (sellers have up to 1,000+ RFQs a month): categories, enquiry volume, common buyer questions, open follow-ups.
2. **Context service** — builds and serves the files by GLID; accepts events from every channel.
3. **Sarvam voice agent** — on-start hook loads the file into agent variables → personalised opener; on-end webhook sends transcript + extracted variables back → file updated.
4. **Second channel (chat)** — a simple web chat on Sarvam LLM using the same service, to prove cross-channel resume.
5. **Evaluation** — cold vs with-memory on simulated users built from real histories.

## Non-goals

- Not a CRM or a full user-profile platform.
- No names, phone numbers or KYC in the files (not available, not needed).
- No long-term behaviour modelling or recommendations.
- No changes to production VANI.
- Facts are never invented by the LLM: facts come from structured fields with dates; the LLM only phrases them.

## Design principles

- **Wrong memory is worse than no memory.** Every fact carries a date and source; stale facts are confirmed, not assumed.
- **Compact over complete.** The file goes into a prompt; size is a cost and a latency.
- **Fresh in minutes.** The on-end write-back covers same-hour repeats; batch sources cover older history.
- **Reusable.** Plain markdown any bot, agent or human can read.

## Success metrics (from the problem statement)

| Metric | How we measure | Target |
|---|---|---|
| Freshness | Time from conversation end → file updated | < 60 s |
| Compactness | Tokens per file; fixed section structure | ≤ 400 tokens |
| Resumed without re-asking | % of known facts the bot did **not** ask again | ≥ 80% (vs ~0% cold) |
| Personalised-opening lift | Turns to goal, call length: cold vs memory | Fewer turns; report the delta |
| Reusability | Same file used by voice agent and chat bot unchanged | Yes, demoed |

## Demo story (5–7 min video)

1. **Cold call** — buyer calls VANI, asks for a product; VANI collects specs, quantity, city. Call ends.
2. **File appears** — show `buyer.md` updated within seconds, with dated facts.
3. **Chat, minutes later** — buyer opens chat: "Any update?" → bot knows the requirement, doesn't re-ask, moves to next step.
4. **Second call, different language** — VANI greets in the buyer's language, references the open loop.
5. **Numbers** — eval table: cold vs memory (re-asked questions, turns, latency, file size).

## Submission checklist (from the deck)

- [ ] 5–7 min demo video
- [ ] Approach note (sources, lookback window, refresh logic)
- [ ] Sarvam agent ID / live link
- [ ] Code + README
- [ ] `skills.md`
- [ ] Sample outputs: `buyer.md` + `seller.md` for sample GLIDs

Judging: Business Impact 25% · Completeness 20% · Technical Robustness 20% · Voice Experience 20% · Demo & skills.md 15%.
