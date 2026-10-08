# PS07 Seller-Fit Adaptive Voice Persona — data analysis

> Analysed 8 Oct 2026 from the organiser dataset (`Persona Files/`, window 1 Apr–30 Sep 2026). **Aggregates only.** The raw files contain unmasked seller and company names and are git-ignored — never commit them or paste rows from them.
>
> Unit: one row = one answered VANI bot call unless stated. "MF" = `meeting_fixed` (the bot's goal). Shares are directional; nothing here is causal unless it says so.

## TL;DR — what the data says about persona design

1. **The first 10 seconds decide the call.** 28% of answered calls end in ≤10 s. Of 150,821 evaluator-labelled calls, **55% were dropped**: 25% with no response, **10% right after the bot said "IndiaMART"**, 7% right after it asked for the seller's company, 12% mid-pitch. The opener is the highest-leverage part of a persona.
2. **Persona fit matters: MF varies ~1.6× by seller type.** On first attempts, new sellers (GST ≤2 years) fix meetings at **20.6%** vs **12.7%** for established enterprises (≥₹1.5 Cr turnover / Ltd company / 50+ products). Today every seller gets the same "Payal" script.
3. **Retries collapse.** MF is **16.3% on attempt 1**, 9.4% on attempt 2, 7.2% on attempt 3, under 3% from attempt 6. Persona must adapt to *how many times we've already called*, and stop earlier.
4. **The only personalisation trial looks positive but is thin.** The `personalis` script ran one afternoon (30 Sep, 452 calls): **14.8% MF vs 12.0%** for `main_vani` on the same attempt/lead-type mix and hours (16–30 Sep). +2.8 pp, z ≈ 1.7 — directional, not proof.
5. **Busy is the #1 objection, not price.** Of calls with objections: scheduling/unavailable 32%, callback/defer 29%, call quality/tech 25%, explicit refusal 19%. Price comes up in only ~4% of transcripts (and those calls convert *better*, 34% — it's a buying signal).
6. **Language is mostly Hindi/Hinglish; regional is a minority overlay.** 52% of sellers are in the Hindi belt, 18% Gujarat, 16% Maharashtra; Tamil/Telugu/Bengali/Punjabi/Odia each ≤4%. Tamil-speaking calls where the bot switched did well (32% MF in transcripts, n=210).
7. **Bot-detection and frustration are rare (≈2% each)** — the problem is relevance and timing, not "I don't talk to robots".

## Datasets

| File | Rows | Use for |
|---|---|---|
| `ps07_seller_files` (2 parts) | 149,363 sellers, 58 cols | Persona input: profile, engagement, past bot history |
| `ps07_bot_calls_*` | 269,455 answered calls, 130,129 sellers | Outcomes by bot version, attempt, hour, lead type |
| `ps07_evaluator_outputs_*` | 278,332 JSON rows, 10 evaluators | Dispositions, objections, questions, drops, incorrect MF |
| `ps07_call_turns` | 139,555 turns / 12,788 calls | Turn-level transcripts (romanised Hindi/Hinglish) for live adaptation |
| `ps07_recording_sample_5000` | 5,000 calls | Audio sample (public MP3 links), balanced by outcome/version |
| `ps07_executive_calls` | 67,151 calls / 6,933 sellers | Human exec contact, Aug–Sep only |

### Data quality notes

- **Disposition labels changed in September**: "Not Interested" fell from ~50% to 19% and "General" rose to 55% — a relabel, not behaviour. Arrowhead/`last_met_a`/`personalis` also label differently. **Use `meeting_fixed` as the outcome**; don't compare NI shares across months or versions.
- Seller file `bot_*` / `calls_*` counts cover the same Apr–Sep window as the calls → using them as features to predict those calls leaks the answer. For persona assignment use profile + engagement fields; use bot history only for *later* attempts.
- `asked_if_talking_to_bot`, `showed_frustration`, `do_not_call_requested` etc. are filled for 54% of sellers (those with evaluator output).
- Transcripts are romanised by STT (even Tamil), so script-based language detection fails; language must come from state/zone + live STT language ID.
- Transcript calls are biased to longer calls (22% MF vs 11.5% overall). Don't read their MF as population MF.

## Who the sellers are (n = 149,363)

| Dimension | Distribution |
|---|---|
| Business type | Proprietorship 81%, Partnership 10%, Ltd company 7% |
| Turnover | ₹0–40 L 58%, 40 L–1.5 Cr 16%, 1.5–5 Cr 9%, 5 Cr+ 6%, blank 11% |
| Nature | Manufacturer 23%, Trader-retailer 20%, Trader-wholesaler 17%, Service 17%, Retailer 8% |
| GST age | median registration 2021; 25% registered 2025–26 |
| State (top) | Gujarat 18%, UP 17%, Maharashtra 16%, Delhi 15%, Rajasthan 7%, Haryana 6% |
| Catalogue | median 12 products, 8 categories; catalogue quality score median 15/100 |
| Bot exposure | median 2 attempts, 1 answered; answer rate median 75% |
| Flags (of 79,962 with evals) | already with an exec 5.3%, do-not-call 1.5%, asked if bot 0.2%, frustration 0.2% |

## Outcomes

**Overall:** 269,455 answered calls → **11.5% MF**; median call 22 s; 28% ≤10 s.

**By attempt number** (strongest single driver):

| Attempt | Calls | MF | ≤10 s |
|---|---|---|---|
| 1 | 129,449 | 16.3% | 18% |
| 2 | 56,089 | 9.4% | 30% |
| 3 | 36,111 | 7.2% | 36% |
| 4 | 19,118 | 5.7% | 41% |
| 5 | 11,859 | 5.1% | 45% |
| 6+ | ~17,000 | ≤2.7% | 50%+ |

**By lead type (`redis_bucket`, first attempts):** NUR 35.5% (n=739), SCHD 21.5%, PAM 21.2%, PUA 18.7%, PIM 14.9%, UA 14.8%. Lead context changes what the opener should say.

**By bot version (all attempts):** main_vani 11.6% (n=208,605), last_met_d 11.1%, arrowhead 10.7%, main 14.0%, personalis 14.2% (n=452), base_vani 18.3% (n=289, mostly first attempts → not comparable raw).

**Personalised-script trial (matched):** stratified by attempt (1/2/3+) × lead type, `personalis` 14.8% vs `main_vani` 12.0% (same strata, 16–30 Sep, 14:00–20:00), n=392 personalised calls. +2.8 pp, z ≈ 1.7. `base_vani` on the same afternoon: 20.0% vs 16.4% (n=230). One afternoon only → treat as a hypothesis to test, not a result.

## Persona fit: MF by seller segment (first attempts, main_vani, n = 99,910, base 16.7%)

| Segment | Low MF | High MF |
|---|---|---|
| GST age | 8y+: 13.6% | ≤1y: **21.8%** |
| Catalogue size | 50+ products: 11.5% | 1–5 products: **20.8%** |
| Turnover | ₹5–25 Cr: 12.0% | ₹0–40 L: 16.6% |
| Catalogue quality | CQS >40: 12.1% | CQS ≤10: 15.7% |
| Nature | Wholesaler/distributor: 12.9% | Service provider: 18.0% |
| State | Delhi 13.4%, Punjab 14.7% | MP 20.9%, Odisha 22.6% |
| Category group | Mechanical parts 13.0%, tools 13.0% | FMCG/grocery 19.5%, furniture 19.3% |

Pattern: **sellers who already have a mature IndiaMART presence are harder to move with the generic "buyers are looking in your area, meet our executive" pitch.** They hang up sooner (20–22% ≤10 s vs 16%) and need a different value proposition and tone.

## Proposed persona segments (rule-based, mutually exclusive, priority order)

| Persona | Rule | Sellers | First-attempt MF | ≤10 s | Retry MF |
|---|---|---|---|---|---|
| **Established enterprise** | turnover ≥₹1.5 Cr OR Ltd company OR 50+ products | 24.6% | 12.7% | 20.3% | 5.7% |
| **New seller** | GST ≤2 years (not established) | 30.8% | **20.6%** | 15.8% | 8.6% |
| **Busy retailer / shopkeeper** | trader-retailer or retailer | 12.9% | 14.7% | 18.6% | 6.6% |
| **Manufacturer** | manufacturer | 10.2% | 14.6% | 17.2% | 6.2% |
| **Service provider** | service & others | 7.8% | 16.2% | 17.4% | 7.8% |
| Trader / wholesaler & other | rest | 13.7% | 14.5% | 19.1% | 6.9% |

Overlays applied on top of any persona: **language zone** (state → starting language), **attempt number** (shorter, softer, option to stop), **lead type** (opener hook), **flags** (already-with-exec → acknowledge; do-not-call → don't dial).

## What sellers say (evaluators)

**Dispositions (150,821 calls):** call dropped 55% (no response 25%, after IndiaMART identity 10%, after seller identity 7%, mid-pitch 12%), callback requested 12% (half with a date/time), not interested 11%, meeting fixed 10% (+2% online), wrong number 3.5%, already in touch with IndiaMART 3%, do-not-call 0.8%.

**Objection categories (4,161 calls with ≥1 objection):** scheduling/unavailable 32%, callback/defer 29%, call quality/tech failure 25%, no response/engagement drop 20%, explicit refusal 19%, call-handling gaps by the bot 15%, existing engagement/past experience 9%, early-stage seller 5%.

**Seller questions (2,847 calls with questions):** meeting/visit details 41%, who is calling 36%, clarification 33%, purpose 28%, product/service info 23%, location 12%, pricing 10%, benefit/value 7%, frustrated 5%, "is this a bot?" 4%.

**Who ended the call (18,768):** the bot 56%, the system 35%, the seller 10%. **Incorrect meeting-fixed** (bot logged MF but seller had refused): 2.4% of 19,617 checked.

**Transcript signals (12,788 calls):** seller "busy / later" in 18% of calls (MF 12.7%); price/cost 4% (MF 34%); "already met / already" 4% (MF 13.6%); bot question 2% (MF 26%); annoyance 2% (MF 9%). Median bot turn 6.8 s / 22 words vs seller 2.0 s / 4 words — **the bot talks 3× longer per turn than the seller.**

## Implications for the design

| Finding | Design response |
|---|---|
| ~4 in 10 evaluated calls drop before the pitch (no response 25%, after identity lines 17%) | Persona-specific opener A/B variants; lead with the seller's benefit, not "IndiaMART se bol rahi hoon"; keep first turn short |
| Established sellers resist the generic pitch | Formal, concise, ROI-led persona; offer a specific slot; acknowledge existing presence |
| New sellers are receptive | Warm, guiding persona; explain the value of a meeting; can afford a slightly longer pitch |
| Busy is the #1 objection | "Busy mode" live adaptation: one-line value + offer a callback slot immediately |
| Retries collapse | Attempt-aware persona: shorter, different hook, and a stop rule after attempt 3–4 |
| Language mostly Hinglish | Start in zone language for Tamil/Telugu/Bengali/Gujarati/Marathi sellers; auto-switch on |
| Price questions are buying signals | Treat as interest: answer briefly, move to booking |
| Incorrect MF 2.4% | Explicit confirmation step before logging a meeting |

## Business case (for the approach note)

- ~74,000 answered bot calls in August 2026 → **each +1 pp of MF ≈ 740 more meetings a month** at today's volume.
- Closing half the gap between established-enterprise sellers (12.7%) and the average first attempt (16.3%) on that 25% of sellers would add ~0.4 pp to first-attempt MF on its own.
- Stopping after attempt 4 would remove ~29k low-yield answered calls (attempt 5+, MF 3.3%) per six months — cost saved and less seller annoyance.

## Optional enrichment: real buyer demand for the opener (Call Insights)

The bot's opener already claims "buyers in your city are asking in your category". RFQ data (buyer enquiries to paid sellers, Call Insights) can make that hook **true and specific**:

- **Category level works.** The top MCATs carry roughly 800–1,500 RFQs each in the 30 days 8 Sep–7 Oct 2026 (e.g. Corrugated Box, MCAT 1416: 1,492; TMT Bars, MCAT 2475: 1,068).
- **City level is too thin for one category.** Corrugated Box, 30 Sep–7 Oct: only 67 of 436 RFQs (15.4%) carry a buyer city, and the top cities have 6 RFQs each. "Many buyers in Ranchi" can't be backed up city by city.
- **Recommendation.** Use national or state category demand ("~1,500 buyers asked for corrugated boxes on IndiaMART last month"). Use city only where the count is meaningful. Never invent numbers. This is a stretch item, and it needs organiser OK to use Call Insights during the event.
- Caveats: paid sellers' calls only, so it is a lower bound; LLM-extracted; city coverage changed in late September.

## What this data cannot tell us

- **Causal effect of a persona.** VANI used essentially one persona; segment differences are associations (sellers differ, not just the script). Our own evaluation must provide the lift estimate.
- **Voice/gender/pace effects** — never varied. The 5,000-call audio sample can describe current pace, not what works better.
- Meetings that actually happened, or revenue after the meeting.

## Reproduce

Exploratory pandas scripts (local, not in git) live in the analyst's work folder; the steps are: stack file parts → join calls to sellers on `fk_glusr_usr_id` → stratify by `call_attempt_count` → evaluator JSON parsed per `eval_agent`. Re-run before quoting any number in the final submission.
