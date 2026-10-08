# 04 — Pipelines

> **Chosen problem: P4 — Seller-Fit Adaptive Voice Persona** ([P4 pipelines](candidates/p4-persona-design/pipelines.md)). This doc covers the pipelines **every candidate** runs through. Data pipelines specific to a problem are in its candidate folder.

## Overview

```mermaid
flowchart LR
    D["1 · Decide<br/>Day 1 by 13:00"] --> B["2 · Build loop<br/>Day 1 pm – Day 2 am"]
    B --> R["3 · Runtime pipeline<br/>per call"]
    R --> E["4 · Evaluation<br/>Day 2"]
    E --> S["5 · Submission<br/>Day 2, 14:00–23:59"]
    E -. "fix & re-run" .-> B
```

---

## 1 · Decision pipeline (Day 1, 10:30–13:00)

```mermaid
flowchart TB
    A["Problem statements presented (10:30)"] --> B["Confirm list; note any new problem"]
    B --> C["Ask organisers & Sarvam the gate questions"]
    C --> D["Score shortlisted problems<br/>(rubric-weighted, see doc 02)"]
    D --> E{"Data gate &<br/>platform gate pass?"}
    E -- "no" --> F["Drop; next problem"]
    F --> D
    E -- "yes" --> G["Pick highest score"]
    G --> H["Fill doc 02 'Final choice' + decision log"]
    H --> I["Split work, start build"]
```

Output: chosen problem, owner per component, logged in [05-decision-log](05-decision-log.md).

## 2 · Build loop (how we work)

```mermaid
flowchart LR
    T["Pick task from<br/>01-task-list"] --> BR["Branch<br/>feat/&lt;task&gt;"]
    BR --> C["Build + quick local test"]
    C --> PR["Push, short PR<br/>(or direct to main if solo-owned file)"]
    PR --> M["Merge to main"]
    M --> U["Update task status<br/>in the same commit"]
    U --> T
```

Rules:

- `main` must always run. Small commits, clear messages (`feat:`, `fix:`, `docs:`).
- Every decision → one line in the decision log. Every finding → `research/` with date and source.
- Every 3–4 hours: one end-to-end run through the runtime pipeline.

## 3 · Runtime pipeline (per call — same for every candidate)

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant S as Sarvam Agent
    participant O as Our service
    participant D as Data / store

    U->>S: Call connects
    S->>O: On-start hook (phone / agent_variables)
    O->>D: Read precomputed data
    O-->>S: Variables for this call
    S->>U: Greeting (personalised / persona-specific)
    loop Conversation
        U->>S: Speech (Saaras STT)
        S->>O: API tool call (if needed)
        O-->>S: Tool result → variables
        S->>U: Reply (Sarvam LLM → Bulbul TTS)
    end
    S-->>O: On-end webhook (transcript, output variables)
    O->>D: Store outcome and update data
```

| Stage | Target |
|---|---|
| On-start hook response | < 300 ms |
| Tool call response | < 800 ms |
| Webhook → data updated | < 60 s |

## 4 · Evaluation pipeline

```mermaid
flowchart LR
    A["Build test set<br/>20–30 cases from real patterns (masked)"] --> B["Simulated user<br/>Sarvam LLM with hidden goal"]
    B --> C["Baseline run<br/>(today's behaviour)"]
    B --> D["Our solution run"]
    C --> E["Score with problem metrics"]
    D --> E
    E --> F["Report table + 3–5 real calls"]
```

Metrics come from the official problem statement; P2's are in [candidates/p2-global-context/pipelines.md](candidates/p2-global-context/pipelines.md#p5--evaluation-offline). Always report a **baseline vs ours** delta — it drives Business Impact (25%).

## 5 · Submission pipeline (Day 2)

```mermaid
flowchart LR
    A["Code freeze 18:00"] --> B["Generate sample outputs → samples/"]
    B --> C["Approach note"]
    C --> D["skills.md"]
    D --> E["Record 5–7 min video"]
    E --> F["README final"]
    F --> G["Tag v1.0-submission"]
    G --> H["Submit all items<br/>before 23:59"]
```

| Item | Owner | Source |
|---|---|---|
| Demo video (5–7 min) | Non-tech member + Pratik | Demo script |
| Approach note | Pratik + non-tech member | docs 02–04 + eval report |
| Sarvam agent ID / live link | Pratik | Sarvam console |
| Code + README | Engineer + Pratik | repo |
| `skills.md` | Non-tech member | agent prompts + learnings |
| Sample outputs | Engineer | `samples/` |

## Candidate-specific data pipelines

| Candidate | Pipelines | Doc |
|---|---|---|
| P2 — Global Context | Historical ingest → context build → write-back → serve → evaluation | [pipelines](candidates/p2-global-context/pipelines.md) |
| **P4 — Seller-Fit Adaptive Voice Persona (chosen)** | Insight mining → persona assignment → call & adapt → write-back → evaluation | [pipelines](candidates/p4-persona-design/pipelines.md) |
