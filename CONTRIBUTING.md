# Contributing to Murmur

Everything about the project — tasks, decisions, research, design — lives in this repo. If it isn't in GitHub, the rest of the team can't see it.

## Get started

```bash
git clone https://github.com/Pratik-Singh-web/Murmur.git
cd Murmur
```

Read in this order: [README](README.md) → [docs/02 What we are building](docs/02-what-we-are-building.md) → [docs/01 Task list](docs/01-task-list.md).

## Daily workflow

```bash
git pull --rebase                 # always start from the latest main
git checkout -b <type>/<short-name>   # e.g. docs/eval-plan, feat/on-start-hook
# ...make changes...
git add -A
git commit -m "docs: add evaluation plan"
git push -u origin HEAD           # then open a Pull Request on GitHub
```

- Small changes to docs can go straight to `main` (`git pull --rebase && git push`).
- Code changes go through a Pull Request; one teammate reviews.
- `main` must always work.

## Commit message prefixes

| Prefix | Use for |
|---|---|
| `docs:` | Anything in `docs/` or the README |
| `research:` | New findings in `research/` |
| `feat:` | New functionality |
| `fix:` | Bug fixes |
| `chore:` | Setup, configs, cleanup |

## Keep the docs in sync with the work

- Finished or started a task? Update its status in [docs/01-task-list.md](docs/01-task-list.md) **in the same commit**.
- Made a decision? Add a row to [docs/05-decision-log.md](docs/05-decision-log.md).
- Found something? Add it to `research/` with the date and the source.
- Changed the design? Update the matching doc in `docs/` (or `docs/candidates/<problem>/`).

## Rules

- **No customer data in git** — no names, phone numbers, GLID-level records, transcripts or exports. Aggregates only; sample outputs must be synthetic or masked. (Hackathon rule: no customer data leaves the premises.)
- **No secrets in git** — API keys go in `.env` (ignored). Share keys in person, not in commits.
- **No code before Day 1 (9 Oct)** — pre-built solutions are disqualified.
