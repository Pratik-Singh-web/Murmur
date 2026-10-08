# P2 — Global Context: pipelines (candidate, not final)

> Candidate design for Problem 2. Used only if P2 is chosen at the Day-1 gate. Shared stack: [../../03-architecture.md](../../03-architecture.md).

If P2 is chosen, it has five pipelines. Two are batch (history), two are real time (conversations), one is offline (evaluation).

```mermaid
flowchart TB
    P1["P1 · Historical ingest<br/>(batch, once + daily)"] --> ES[("Event store")]
    P3["P3 · Write-back<br/>(real time, on conversation end)"] --> ES
    ES --> P2["P2 · Context build<br/>(on every new event)"]
    P2 --> F[("buyer.md / seller.md")]
    F --> P4["P4 · Serve<br/>(on call/chat start)"]
    F --> P5["P5 · Evaluation<br/>(offline)"]
    P4 --> CONV(("Conversation"))
    CONV --> P3
```

---

## P1 — Historical ingest (batch)

Gives the file its older context: language, categories, past needs, blockers, sellers contacted.

```mermaid
flowchart LR
    A["Select sample GLIDs<br/>(exclude 30+ RFQ pooled accounts)"] --> B["Pull per-GLID records<br/>Call Insights / starter APIs"]
    B --> C["Normalise to EVENT<br/>(channel, date, facts)"]
    C --> D["Mask: drop names/phones,<br/>keep city/category"]
    D --> E[("Event store")]
```

| Item | Value |
|---|---|
| Trigger | Once at setup; re-run daily in production |
| Input | Call Insights per-call fields (products/specs/qty, quoted prices, call_purpose, deal_readiness, outcome, intent, blockers, buyer questions, next steps, language, city, persona); starter APIs |
| Lookback | Buyers: 7–14 days in detail + compact profile beyond. Sellers: 30 days aggregated |
| Output | Events in SQLite |
| Not used | `callbacks` (not extracted since 11 Sep); readiness/blocker trends (extraction changed 4, 23, 30 Sep) |

## P2 — Context build

Turns events into the file. Runs on every new event for that GLID.

```mermaid
flowchart LR
    A["Load events for GLID<br/>within lookback"] --> B["Extract facts<br/>latest value wins, keep date + source"]
    B --> C["Rank & trim<br/>active needs → last 3 interactions → open loops"]
    C --> D["Render template<br/>fixed sections"]
    D --> E{"LLM phrasing on?"}
    E -- yes --> F["Sarvam LLM rewrites wording only<br/>validator: every fact still present, no new facts"]
    E -- no --> G["Template output"]
    F --> H["Token check ≤ 400"]
    G --> H
    H --> I[("buyer.md / seller.md<br/>+ built_at")]
```

Rules:

- Every fact has a date (`2026-10-09`) and source (`call`, `chat`, `rfq`).
- Conflicts: newest wins; older value kept only if still relevant ("earlier asked 200 kg, now 500 kg").
- Facts older than the lookback drop to the compact profile (language, city, categories).
- If the LLM output fails validation, ship the template output.

`buyer.md` shape:

```markdown
# Buyer {glid} · updated 2026-10-09 14:32 IST
## Who
City: Kanpur · Type: B2B (trader) · Language: Hindi (Hinglish ok)
## Active needs
- HDPE granules, blow-moulding grade, 500 kg, wants price ≤ ₹110/kg — 2026-10-09 (call)
## Last interactions
- 2026-10-09 call with VANI — gave specs and qty; waiting for quotes
- 2026-10-08 RFQ call with 2 sellers — price too high (blocker)
## Open loops
- Send 2–3 seller quotes under ₹110/kg
## Don't re-ask
Product, grade, quantity, city, budget
```

## P3 — Write-back (real time)

Keeps the file fresh within seconds of a conversation ending.

```mermaid
flowchart LR
    A["Sarvam on-end webhook<br/>or chat turn"] --> B["Verify secret,<br/>dedupe by interaction_id"]
    B --> C["Map output_agent_variables → facts<br/>(product, qty, city, next_step, blocker)"]
    C --> D["Store transcript ref"]
    D --> E[("Append EVENT")]
    E --> F["Trigger P2 for GLID"]
```

| Item | Value |
|---|---|
| Trigger | Sarvam call-completion webhook; every chat exchange |
| Idempotency | `interaction_id` unique; retries are no-ops |
| Facts source | Sarvam output variables (LLM-extracted at call end, typed String/Enum) — preferred over parsing raw transcripts |
| Target latency | Webhook received → file rebuilt < 60 s (expected: a few seconds) |

## P4 — Serve (on call / chat start)

```mermaid
flowchart LR
    A["Call or chat starts"] --> B{"Channel"}
    B -- "voice inbound" --> C["On-start hook: phone → GLID<br/>(demo mapping table)"]
    B -- "voice outbound" --> D["glid in agent_variables"]
    B -- "chat" --> E["glid from session"]
    C --> F["Read prebuilt file<br/>(no build on the hot path)"]
    D --> F
    E --> F
    F --> G{"File exists?"}
    G -- yes --> H["Return buyer_context, language, opener_hint"]
    G -- no --> I["Return empty context → cold greeting"]
```

Prompt rules the agent follows:

- Use the context; confirm stale facts (> 7 days) instead of assuming them.
- Never read the file out; never reveal other sellers' names or prices unless the user asks.
- If the caller says it's not them / wrong need → drop memory for this call.

Target: hook response < 300 ms.

## P5 — Evaluation (offline)

Proves the lift with numbers for the demo and approach note.

```mermaid
flowchart LR
    A["20–30 personas from real histories<br/>(masked)"] --> B["Simulated user (Sarvam LLM)<br/>with a hidden goal + known facts"]
    B --> C["Run A: cold agent"]
    B --> D["Run B: agent + buyer.md"]
    C --> E["Score transcripts"]
    D --> E
    E --> F["Report: re-asked facts, turns to goal,<br/>file tokens, freshness"]
```

| Metric | Definition |
|---|---|
| Re-ask rate | Known facts the agent asked again ÷ known facts |
| Turns to goal | Agent turns until the requirement is complete |
| Opening relevance | Did the first agent turn reference the active need? (yes/no) |
| File size | Tokens per file (p50, max) |
| Freshness | Conversation end → file rebuilt (p50, p95) |

Plus 3–5 real voice calls by the team as a sanity check; text simulation is the scaled measurement.
