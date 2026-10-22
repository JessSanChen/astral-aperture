# Start here

## Scientific question

Can a controller learn which permitted observation or fixed-judge computation will
improve a decision, and transfer that choice to unfamiliar workflow families?
Risk, uncertainty, and expected action-specific improvement are different targets.
A judge call is not an oracle label. More context may help or hurt a fixed judge.

## Current authority and status

B1 was explicitly selected by the user; the algorithm is undecided. The user reports
access to Claude Code, Codex, Runpod, OpenRouter, and other resources. Credentials,
quotas, available models, licenses, region, repository access, and integrations have
not been inspected. This pack proposes an implementation workflow; it does not
approve a method or prove a result.

## Reading order

1. `CURRENT_STATE.md`: what is true now and the next bounded task.
2. `DECISIONS.md`: confirmed decisions versus proposals.
3. Assigned `../tasks/` file: scope, acceptance criteria, and stop point.
4. `DESIGN_PROPOSAL.md`: minimal architecture, when relevant.
5. `../context/ASTRAL_Project_Brief_v4_B1_Selected.md`: canonical supplied context.
6. `../context/ASTRAL_Parallel_Research_Protocol.md`: B/C coordination.

Do not load the entire historical conversation into every coding task. Read the
specific task, interfaces, and current evidence; retrieve history only when needed.
The pre-B1 handoff and literature ledger are preserved under `context/`, but their
proposal status and older branch-selection statements must not override v4.

## First task

Complete B1-000 (audit accessible code and constraints), then B1-001 (offline smoke
slice). Start no external experiment until the human approves a run specification.
