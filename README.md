# ASTRAL B1

Research scaffold for B1: transferable, action-specific inspection value for fixed,
fallible judges. `docs/START_HERE.md` has the question and reading order.

## What is here

Agent instructions, task contracts, templates, preserved project context, and the
B1-001 offline slice under `src/astral_b1/` (fictional workflow, mock judges, baseline
controllers, evaluator, replay). No model API has been called, no infrastructure has
been provisioned, and no scientific experiment has been run.

```bash
uv sync
uv run --locked pytest
uv run --locked python -m astral_b1 smoke --output artifacts/smoke-001          # offline, mock judges
uv run --locked python -m astral_b1 replay --input artifacts/smoke-001
# Real judges (needs OPENROUTER_API_KEY and human authorization):
uv run --locked python -m astral_b1 collect --output artifacts/pilot-001 --judges configs/judges.dev.json --authorized
uv run --locked python -m astral_b1 pilot --input artifacts/pilot-001            # offline analysis of the bank
```

Results so far are in `handoffs/`. The latest is the B1-003 pilot handoff.

## Workflow

1. Read `docs/START_HERE.md` and `docs/CURRENT_STATE.md`.
2. Give a coding agent `prompts/01_BOOTSTRAP.md`. Tasks run in order from `tasks/`.
3. Review the diff with a separate agent using `prompts/02_REVIEW.md`.
4. End each task with a handoff from `templates/HANDOFF.md`. Evidence is a commit,
   a command, and observed output, not an agent's recollection.

## Authority

Current human instructions > confirmed decisions in `docs/DECISIONS.md` > approved
experiment specs > proposals in `docs/` > historical discussion in `context/`.
The `context/` files are preserved snapshots. Do not edit them.
