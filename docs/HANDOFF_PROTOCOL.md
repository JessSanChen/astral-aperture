# Handoff protocol

Chats and tool-local memory are conveniences, not the project record. A plain-text,
human-reviewed handoff is the portable unit between laptops, Pods, Claude, Codex,
and research chats.

## Task start

Read the current state and the assigned task. Record the source revision you
received. Check actual files and tests before trusting a previous agent's claims.

## Task finish

Write `handoffs/<task-id>-<revision>.md` from `../templates/HANDOFF.md` with exact
commands and observed outcomes. Separate code written from code tested, and
observations from interpretations. The human reviews the diff and updates
CURRENT_STATE. Do not overwrite another agent's handoff.

## Between agents and chats

- Coding agent to coding agent: commit, task spec, handoff, changed interfaces,
  verified test output. The next agent reruns the stated checks.
- Coding agent to research chat: compact status, current experiment spec, local
  report with denominators, relevant diffs. The chat does not see the repository.
  Sealed evaluation examples are never routine handoff material.
- Research chat to implementation: one accepted task, its observation boundary,
  baselines, and acceptance tests. An idea in a chat is not permission to tune
  judges, modify holdouts, or change the research target.
- B to C: minimal schemas and generic infrastructure. Never held-out labels or
  prompts derived from holdout failures. Record any test-artifact exposure.

A second model review is a useful check, not an independent label oracle.
