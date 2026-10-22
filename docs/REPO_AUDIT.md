# B1-000 repository audit

Date: 2026-10-22. Status: complete for what was available.

## What was inspected

Only this repository. No ASTRAL scanner source, policy, configuration, or test
suite was made available in or alongside this working copy. Checks performed:

```
find . -type f -not -path './.git/*'
git log --oneline
```

Result: docs, prompts, tasks, templates, one OpenRouter config template, and four
preserved context snapshots. No Python package, no tests, no baseline code.

## Consequence

B1-001 was scaffolded as standalone interfaces under `src/astral_b1/`. Nothing in it
claims integration with the deployed scanner. When the ASTRAL repository is supplied,
redo this audit: record its revision, evaluation entry points, policy and config
versions, and which of its adapters the B1 package should reuse instead of its own
mock environment and judges.
