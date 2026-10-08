# P4 — Seller-Fit Adaptive Voice Persona: pipelines

> Problem-specific pipelines on top of the shared ones in [04-pipelines](../../04-pipelines.md).

```mermaid
flowchart LR
    P1["P1 · Insight mining<br/>(offline, Day 1 am)"] --> PB[("Playbook")]
    P2["P2 · Persona assignment<br/>(batch + per call)"] --> PC[("Persona cards")]
    PB --> P2
    PC --> P3["P3 · Call & adapt<br/>(real time)"]
    P3 --> P4["P4 · Write-back & next attempt<br/>(real time)"]
    P4 --> P2
    PB --> P5["P5 · Evaluation<br/>(offline)"]
    PC --> P5
```

## P1 — Insight mining (organiser data → playbook)

```mermaid
flowchart LR
    A["Stack files<br/>join on seller GLID"] --> B["Outcome by segment<br/>stratified by attempt"]
    A --> C["Evaluator JSON<br/>objections, questions, drops"]
    A --> D["Transcripts<br/>signals, phrasing that worked"]
    B --> E["Persona rules + sizes"]
    C --> F["Objection replies per persona"]
    D --> G["Openers, busy/clarify lines,<br/>test scenarios"]
    E --> H[("Playbook YAML")]
    F --> H
    G --> H
```

- Done once on Day 1 morning (exploratory version already in [research/ps07-data-analysis.md](../../../research/ps07-data-analysis.md)).
- Output contains no seller names; quotes are paraphrased.

## P2 — Persona assignment

```mermaid
flowchart LR
    A["Seller row"] --> B{"Do-not-call?"}
    B -- yes --> X["Skip"]
    B -- no --> C["Base persona<br/>priority rules"]
    C --> D["Overlays: zone language,<br/>attempt no., lead type, flags"]
    D --> E["Pick voice variant<br/>(Warm / Formal / Brisk)"]
    E --> F["Fill card from playbook<br/>LLM phrases opener only"]
    F --> G["Validate: ≤250 tokens,<br/>no personal data, facts from row"]
    G --> H[("Persona card")]
```

Rules (from the data): established (≥₹1.5 Cr / Ltd / 50+ products) → new (GST ≤2y) → retailer → manufacturer → service → trader/other. Attempt ≥4 without a requested callback → don't dial.

## P3 — Call & adapt (per call)

```mermaid
flowchart TB
    S["Open (persona opener)"] --> V["Purpose / value hook"]
    V --> K["Ask for meeting"]
    K --> B["Book slot → confirm explicitly"]
    B --> C["Close"]
    S & V & K --> SIG{"Signal?"}
    SIG -- busy --> M1["Compress: offer 2 slots"]
    SIG -- "who/why?" --> M2["Clarify in one line"]
    SIG -- "already met" --> M3["Acknowledge, follow-up"]
    SIG -- "price" --> M4["Brief answer → book"]
    SIG -- "bot?" --> M5["Confirm AI, offer human"]
    SIG -- "angry / DNC" --> M6["Apologise, exit, flag"]
    SIG -- "other language" --> M7["Switch language"]
    M1 & M2 & M3 & M4 & M5 & M7 --> K
    M6 --> C
```

Targets: first bot turn ≤ 6 s; adapt tool < 800 ms; no meeting logged without an explicit "yes" + slot.

## P4 — Write-back & next attempt

| Step | Detail |
|---|---|
| Trigger | Sarvam on-end webhook (`final_agent_variables`, `output_agent_variables`, transcript) |
| Store | outcome (meeting / callback slot / not interested / dropped / DNC), signals seen, persona, variant, attempt no. |
| Next attempt | callback slot → call at that time with "as promised" opener; dropped early → change opener variant; NI ×2 or attempt ≥4 → stop |
| Idempotent | keyed by `interaction_id` |

## P5 — Evaluation

```mermaid
flowchart LR
    A["Scenario set: 6 personas ×<br/>5 behaviours (receptive, busy,<br/>sceptical/already met, price, hostile)"] --> B["Sarvam Tests<br/>AI-simulated seller"]
    B --> C["Baseline agent<br/>(single 'Payal' persona)"]
    B --> D["Seller-fit agent"]
    C --> E["AI judge + our script"]
    D --> E
    E --> F["Per persona: MF, early drop,<br/>turns to ask, signal handling,<br/>false MF, persona fit"]
```

- 30 scenarios × 3 runs each × 2 agents ≈ 180 simulated calls; plus 4–6 real team calls.
- Report deltas with n and say clearly that simulation ≠ field result; propose a production A/B (persona vs control, stratified by attempt and lead type, MF as primary metric).
