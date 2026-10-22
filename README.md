# ASTRAL B1 — bootstrap and knowledge-handoff pack

**21 October 2026 · version 0.1 · proposed implementation setup**

B1 is user-selected: study transferable action-specific inspection value for fixed,
fallible judges. C remains independently active. The technology choices in this pack
are recommendations, not newly approved scientific decisions.

## What this pack is

A repository-ready set of instructions, task contracts, experiment-record templates,
and preserved project context. It is **not an implemented experiment harness**.
No model API has been called, no Runpod infrastructure has been provisioned, no
scientific experiment has been run, and no account credentials have been accessed.
The only executable utility is `verify_pack.py`, which checks this pack's integrity.

## Begin here

1. Read `docs/START_HERE.md` and `docs/CURRENT_STATE.md`.
2. Put this pack in a new research repository, or a separate research subtree after
   auditing the existing repository. Do not overwrite an existing AGENTS.md or
   CLAUDE.md without reconciling its instructions.
3. Give a coding agent `prompts/01_BOOTSTRAP.md`. Start with task B1-000, then the
   offline smoke slice B1-001. No paid inference or cloud provisioning is authorized
   merely by opening this pack.
4. Review its diff with a separate agent using `prompts/02_REVIEW.md` and human
   review of labels and observation boundaries.
5. End each task with `templates/HANDOFF.md`. Evidence is a commit, artifact, command,
   and observed output—not an assertion that an agent remembers the work.

## Suggested initial Git setup

Run these only inside a newly created working copy of this pack:

```bash
python verify_pack.py
git init -b main
git add .
git commit -m "Add B1 research bootstrap and handoff specification"
git worktree add -b impl/B1-001 ../astral-b1-impl main
```

Select your private Git hosting and push remote separately. This pack creates no
remote. `git worktree` isolates checkouts, not credentials, agent memory, or secrets.

## Implemented versus specified

| Item | Status |
|---|---|
| Project source snapshots | Included, copied unchanged |
| Agent instructions and task contracts | Included, proposed |
| Run and request templates | Included; contain deliberate unresolved fields |
| Research code, provider adapters, Dockerfile, CI, uv.lock | Not implemented |
| ASTRAL repository inspection | Not performed |
| Runpod/OpenRouter/account integration | Not performed |
| Experimental findings | None |

Do not run example API request templates unchanged. Select an available model,
endpoint, license/terms, privacy setting, and sampling configuration first.

## Knowledge authority

Current explicit user instructions > confirmed project decisions > approved experiment
specifications > proposed designs > historical discussion. The v4 project brief is
included unchanged. The historical literature ledger is context, not newly verified
bibliographic evidence. `docs/SOURCES.md` records tool documentation checked for this pack.

`CHECKSUMS.json` records the original pack contents. After editing files, checksum
mismatches are expected; use Git to track the working repository. No downstream
code/data/model licensing is established by this pack.
