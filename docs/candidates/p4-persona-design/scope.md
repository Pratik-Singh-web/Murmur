# P4 — Seller-Fit Adaptive Voice Persona: scope (chosen problem)

> **Chosen 8 Oct 2026** (see [decision log](../../05-decision-log.md)). Confirm against the official problem statement at 10:30 on Day 1; if it differs, update this file first. Evidence: [research/ps07-data-analysis.md](../../../research/ps07-data-analysis.md).

## One line

VANI picks a persona that fits **this** seller before dialling (voice, tone, pace, language, opener, value hook) and **adapts it live** when the seller turns out busy, confused, sceptical or interested, so that more calls end in a meeting with a sales executive.

## The problem, in numbers (Apr–Sep 2026, 269,455 answered bot calls)

- One persona ("Payal", same script) for 149k very different sellers.
- **11.5%** of answered calls fix a meeting; **28%** end within 10 seconds; **55%** of evaluated calls are dropped, 1 in 10 right after the bot says "IndiaMART".
- Fit varies: new sellers 20.6% vs established enterprises 12.7% on first attempts.
- Retries collapse: 16.3% on attempt 1 → 7.2% on attempt 3 → <3% from attempt 6.
- The one personalised-script trial: 14.8% vs 12.0% matched (directional, one afternoon).

## Users

| User | What changes for them |
|---|---|
| Seller | A call that sounds relevant to their business, respects their time, in their language |
| IndiaMART sales | More (and more genuine) meetings per 1,000 calls; fewer wasted retries |
| VANI team | A persona engine + playbook they can tune, measure and roll out by segment |

## What we build

1. **Persona engine** — seller profile → persona card. Six data-backed personas (established enterprise, new seller, busy retailer, manufacturer, service provider, trader/wholesaler), plus overlays: language zone, attempt number, lead type, flags. Rules are transparent; an LLM only writes the short seller brief and opener wording from the card.
2. **Persona playbook** — for each persona: voice and pace profile, formality, opener (2 variants), value hook, pitch length cap, objection responses, booking style, stop rules.
3. **Sarvam voice agent(s)** — per-persona voice/pace via agent variants; per-call persona card via `agent_variables`; multi-state conversation flow.
4. **Live adaptation** — signal detection (busy, confusion/identity question, bot question, scepticism/already-met, price/interest, frustration, language switch) → switch *mode* mid-call (compress, reassure, clarify, close, exit politely) and language.
5. **Write-back + next-attempt policy** — on-end webhook stores outcome and signals; the next attempt gets a different hook or is not made (stop after attempt 3–4 unless the seller asked for a callback).
6. **Evaluation** — Sarvam Tests (AI-simulated sellers built from real transcripts and objections) comparing **baseline single persona vs seller-fit persona**, plus live demo calls.

## Non-goals

- Changing who gets called or the lead buckets (only the *how*, plus a stop rule).
- Voice cloning or brand-new voices.
- Claiming causal lift from historical data (we measure our own lift in simulation and say so).
- Production rollout; we deliver a design ready for an A/B test.

## Persona summary (detail in the playbook during build)

| Persona | Share | Today | Voice & pace | Tone | Opener hook | Pitch cap |
|---|---|---|---|---|---|---|
| Established enterprise | 25% | 12.7% | Mature, measured (≈1.0×) | Formal "aap/sir", concise, ROI | "Your [category] listing gets enquiries you may be missing — 15 minutes with your account manager?" | 2 short turns |
| New seller | 31% | 20.6% | Warm, friendly (≈1.0×) | Guiding, encouraging | "Congratulations on starting on IndiaMART — our executive can set your profile up to get buyers" | 3 turns |
| Busy retailer / shopkeeper | 13% | 14.7% | Brisk (≈1.1×) | Respectful, to the point | "30 seconds only — buyers near [locality] are asking for [product]" | 1–2 turns |
| Manufacturer | 10% | 14.6% | Clear, steady | Practical, B2B | Bulk/B2B buyer demand in their category | 2 turns |
| Service provider | 8% | 16.2% | Warm | Consultative | Local service enquiries | 2–3 turns |
| Trader / wholesaler | 14% | 14.5% | Brisk | Business-like | Wholesale buyers / repeat orders | 2 turns |

Overlays: **zone language** for Tamil, Telugu, Bengali, Gujarati, Marathi, Punjabi, Odia sellers; **attempt 2+** → shorter, new hook, offer callback slot; **attempt ≥4** → don't dial unless a callback was requested; **already with an exec** → acknowledge and offer a follow-up; **do-not-call** → excluded.

## Live adaptation modes

| Signal (detected from seller speech) | Seen in | Mode switch |
|---|---|---|
| "Busy / baad mein / abhi nahi" | 18% of transcripts | **Compress**: one-line value + offer two callback slots, close fast |
| "Kaun? / kahan se? / kya kaam hai?" | 36% of question calls | **Clarify**: who, why, benefit in one sentence |
| "Already met / already have IndiaMART" | 4% | **Acknowledge**: reference past contact, offer follow-up meeting |
| Price / cost / package questions | 4% (MF 34%) | **Interest**: brief honest answer → move to booking |
| "Is this a bot?" | 2% | **Transparent**: confirm AI assistant, offer human callback |
| Irritation / "don't call again" | 2% | **Exit**: apologise, mark do-not-call, end |
| Speaks another language | zone-dependent | **Switch language** (built-in) |

## Success metrics

| Metric | How | Target for demo |
|---|---|---|
| Meeting-fixed rate (simulated) | Sarvam Tests, 6 personas × scenarios, baseline vs ours | Higher than baseline on every persona; report delta + n |
| Early drop | Simulated seller ends call within 2 turns | Lower than baseline |
| Turns / seconds to the ask | Transcript | Fewer for busy personas |
| Correct handling of signals | Judge per scenario (busy, bot question, already met …) | ≥90% pass |
| False meeting-fixed | Seller refused but logged MF | 0 in tests (baseline 2.4% historical) |
| Persona fit | Judge: did tone/opener match the seller card? | ≥90% |

## Demo story (5–7 min)

1. **Data** (60 s): one bot for everyone → 28% gone in 10 s; fit gap 12.7% vs 20.6%; retries collapse.
2. **Persona engine** (60 s): two real-looking (synthetic) seller cards → two different persona cards.
3. **Live call 1** (90 s): established enterprise — formal, concise, books a slot.
4. **Live call 2** (90 s): busy shopkeeper in Hinglish → says "busy" → bot compresses, offers callback; switches language when the seller does.
5. **Numbers** (60 s): simulated baseline vs seller-fit per persona; business case (+1 pp ≈ 740 meetings/month).

## Cut list (in order)

1. Code-first voice switching (stay on the hosted agent)
2. Attempt-history write-back (keep attempt overlay as a variable)
3. Six personas → four (merge manufacturer, trader, service)
4. Second opener variant per persona

**Never cut:** persona engine output, two contrasting live calls, the busy-mode adaptation, baseline-vs-ours numbers.
