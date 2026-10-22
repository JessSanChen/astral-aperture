# B1-001 — offline end-to-end plumbing
Status: proposed. Engineering smoke test, not a scientific experiment.

## Scope

After B1-000, implement a minimal typed Python package and tests, reusing compatible
existing components. Use one fictional dummy-document approval workflow with an
explicit predicate and tiny public development fixtures. Use two deterministic mock
judges. Inject correction/no-change/corruption cases only to validate accounting.

Allowed additions: src/astral_b1, tests, pyproject.toml, uv.lock, an optional Makefile,
new smoke configs and task-specific docs. Do not change preserved context snapshots,
accepted policy semantics, baseline source, or shared decision status.

## Required behavior

Generate executions; validate the predicate using separately written test cases;
render initial and retrievable evidence; pass an allowlisted ObservationView into a
controller; execute stop/retrieve/reread actions; lock pre-audit decisions; score in
the evaluator; write an immutable run manifest, decisions, costs, and local report.
One-step inspection is enough. Explicitly document that process-level isolation and
independent oracle/rendering review remain to be added.

## Acceptance

- A fresh environment can run tests and a small offline smoke run with no credentials.
- Hidden-label changes cannot alter the controller's serialized initial input.
- The controller never receives an environment object or unselected branch output.
- Cases exercise +1, 0, and -1 error-change bookkeeping without claiming real model gains.
- A replay rebuilds identical metrics from frozen outputs with networking disabled.
- Parsing/failure/abstention records are not silently discarded.
- A pre-audit decision cannot be overwritten by later oracle feedback.
- The run records code/config/data identities and denominators.
- Commands advertised as working have actually been run.

Suggested CLI target to IMPLEMENT, not an existing command:
`uv run --locked python -m astral_b1 smoke --output artifacts/smoke-001`
Choose a different interface only with a documented reason. Create real lockfiles
using the selected tooling; never fabricate resolved dependency hashes.

Stop before any API integration, GPU launch, learned router, large generation job,
or empirical scientific claim. Submit tests, limitations, and a handoff.
