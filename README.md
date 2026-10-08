# Murmur

Team repo for **IndiaMART Voice AI Hackathon 2.0** (9–10 Oct 2026). We will build a voice AI solution on **Sarvam** (Saaras STT, Bulbul TTS, Sarvam LLM, Voice Agents) for one of the hackathon's problem statements.

> **Status (8 Oct 2026): problem not chosen yet.** Official problem statements come out on Day 1 at 10:30; we decide by 13:00 using the criteria in [docs/02](docs/02-what-we-are-building.md). Current ranking: **P2 Global Context** (leading), **P4 Persona Design** (fallback), P1 Quality Audit (third).
>
> Per hackathon rules, all build work happens on 9–10 Oct and pre-built solutions are disqualified. Until Day 1 this repo holds **only docs and research** — no code.

## Docs

| # | Doc | What it covers |
|---|-----|----------------|
| 1 | [Task list](docs/01-task-list.md) | All tasks by phase, owners, status; problem-specific tasks per candidate |
| 2 | [What we are building](docs/02-what-we-are-building.md) | Fixed constraints, judging rubric, candidate problems, selection criteria, Day-1 gate, final choice (TBD) |
| 3 | [Architecture & tools](docs/03-architecture.md) | Shared stack for any problem, Sarvam integration points, tech choices, repo structure |
| 4 | [Pipelines](docs/04-pipelines.md) | Decision → build loop → runtime → evaluation → submission |
| 5 | [Decision log](docs/05-decision-log.md) | Every decision, why, and what would change it |

### Candidate designs

| Candidate | Status | Docs |
|---|---|---|
| P2 — Global Context: Memory Across Channels | Leading | [scope](docs/candidates/p2-global-context/scope.md) · [architecture](docs/candidates/p2-global-context/architecture.md) · [pipelines](docs/candidates/p2-global-context/pipelines.md) |
| P4 — Persona Design | Fallback | [sketch](docs/candidates/p4-persona-design.md) |
| Others | Not planned | [overview](docs/candidates/README.md) |

## Research

| Doc | What it covers |
|-----|----------------|
| [Problem selection](research/problem-selection.md) | Ranking of problems, data availability, repeat-behaviour sizing, Day-1 gate |
| [Sarvam platform notes](research/sarvam-platform-notes.md) | Hooks, variables, webhooks, tools, models, channels, and gaps |

## Contributing

Clone, branch, commit and keep docs in sync: see **[CONTRIBUTING.md](CONTRIBUTING.md)**.

```bash
git clone https://github.com/Pratik-Singh-web/Murmur.git
```

## How we keep this up to date

- Task status changes go in the same commit as the work ([01-task-list](docs/01-task-list.md)).
- Every decision → one row in [05-decision-log](docs/05-decision-log.md).
- Every new finding → `research/` with the date and its source.
- Commit prefixes: `docs:`, `research:`, `feat:`, `fix:`, `chore:`.

## Data handling

- **No customer data in this repo.** Hackathon rule: no customer data leaves the premises. `research/` holds aggregate figures only; any sample outputs must be synthetic or masked.
- Keep the GitHub repo **private** unless the organisers allow publishing.
- Secrets (Sarvam keys, endpoints) go in `.env`, never in git.

## Team

| Member | Role (to confirm after the problem is chosen) |
|--------|------|
| Pratik Singh | Sarvam agent, hooks, integration |
| Engineer (TBD) | Backend service, data pipelines |
| Non-tech member (TBD) | Demo script, evaluation, `skills.md`, video |
