# Candidate problems

Prepared designs for the problems we might pick. Only one will be built. Status as of 8 Oct 2026.

| Problem | Status | Design depth | Doc |
|---|---|---|---|
| P2 — Global Context: Memory Across Channels | Fallback | Detailed | [scope](p2-global-context/scope.md) · [architecture](p2-global-context/architecture.md) · [pipelines](p2-global-context/pipelines.md) |
| **P4 — Seller-Fit Adaptive Voice Persona** | **Chosen (8 Oct)** | Detailed | [scope](p4-persona-design/scope.md) · [architecture](p4-persona-design/architecture.md) · [pipelines](p4-persona-design/pipelines.md) |
| P1 — Quality Audit | Third | One-liner | [research/problem-selection.md](../../research/problem-selection.md#why-not-the-others) |
| P3, P5, P6 | Not planned | — | same |

When the problem is chosen on Day 1:

1. Fill "Final choice" in [02-what-we-are-building](../02-what-we-are-building.md).
2. Log it in [05-decision-log](../05-decision-log.md).
3. Mark the other candidates "not chosen" here; keep the docs (they are part of the approach note).
4. If the chosen problem has no prepared design, create `candidates/<problem>/` from the template below.

## Template for a new candidate

```
candidates/<problem>/
├── scope.md         # problem, users, scope, non-goals, metrics, demo story
├── architecture.md  # components on top of the shared stack, diagrams
└── pipelines.md     # data pipelines specific to this problem
```
