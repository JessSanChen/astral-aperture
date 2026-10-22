# Handoff protocol

## Durable memory

Keep three layers distinct:
- Stable context: the confirmed brief, shared instructions, architecture contracts.
- Changing state: reviewed task handoffs, next task, open decisions, source commit.
- Evidence: immutable run specs, logs, metrics, hashes, reports, and source verification.

Chats and tool-local memory are conveniences, not the project database. Do not rely
on automatic memory to travel between laptops, Pods, Claude, Codex, or research chats.
A plain-text, human-reviewed handoff is the portable unit.

## Task start

Read the authoritative context, latest reviewed state, and assigned task. Record
which source revision you received. Check actual files and tests before trusting a
previous agent's claim. State unresolved assumptions but do not ask routine questions
that the available code or documents can resolve.

## Task finish

Use `../templates/HANDOFF.md`, saved as `handoffs/<task-id>-<revision>.md`. Include
exact commands and observed outcomes; separate code written from code tested and
research observations from interpretations. The human/integrator reviews the diff,
then updates shared CURRENT_STATE and any approved decision. Agents should not all
write a single handoff.md that loses concurrent work.

## Coding agent -> another coding agent

Transfer the commit/PR, task spec, handoff, changed interfaces, public fixtures,
verified test output, and artifact references. The next agent must rerun the stated
checks. Do not copy secrets, raw protected data, or an entire transcript unnecessarily.

## Coding agent -> research chat

Transfer a reviewed compact status export, the current experiment spec, the local
report with uncertainty/denominators, and relevant diffs/source citations. Explicitly
state that this chat does not automatically see a repository or another chat's state.
For development data only, include a few approved failure examples when scientifically
useful; sealed evaluation examples are not routine handoff material.

## Research chat -> implementation

Transfer one accepted question/task, observation boundary, artifact contracts,
baselines, acceptance tests, and status of choices. An interesting idea in a chat is
not permission to tune judges, modify holdouts, or rewrite the research target.

## B -> C

Share minimal trace/policy/judge/action schemas and generic infrastructure. Do not
share final held-out labels, prompts derived from failures on that holdout, or caches
of sealed episodes as reusable training data. Record exposure when any test artifact
enters development. A later interaction study remains optional.

## Human review boundary

A second model review is not an independent label oracle. Human/independent checks
remain necessary for policy semantics, rendering validity, and the main claim.
