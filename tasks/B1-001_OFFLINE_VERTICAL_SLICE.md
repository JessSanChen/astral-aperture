# B1-001: offline end-to-end plumbing
Status: proposed. Engineering smoke test, not a scientific experiment.

## Scope

After B1-000, implement a minimal typed Python package and tests, reusing compatible
existing components. Use one fictional dummy-document approval workflow with an
explicit predicate and small public development fixtures. Use two deterministic mock
judges. Inject correction, no-change, and corruption cases only to validate accounting.

Allowed additions: src/astral_b1, tests, pyproject.toml, a lockfile, optional
Makefile, smoke configs, and task-specific docs. Do not change preserved context
snapshots, baseline source, or shared decision status.

## Required behavior

Generate executions; validate the predicate with separately written test cases;
render initial and retrievable evidence; pass an allowlisted ObservationView into a
controller; execute stop, retrieve, and reread actions; lock pre-audit decisions;
score in the evaluator; write an immutable run manifest, decisions, resource usage,
and a local report. One-step inspection is enough. Document that process-level
isolation and independent oracle review remain to be added.

## Acceptance

- A fresh environment can run tests and a small offline smoke run with no credentials.
- Hidden-label changes cannot alter the controller's serialized initial input.
- The controller never receives an environment object or unselected branch output.
- Cases exercise +1, 0, and -1 error-change bookkeeping without claiming real gains.
- A replay rebuilds identical metrics from frozen outputs with networking disabled.
- Parsing, failure, and abstention records are not silently discarded.
- A pre-audit decision cannot be overwritten by later oracle feedback.
- The run records code, config, and data identities and all denominators.
- Commands advertised as working have actually been run.

Suggested CLI target to implement, not an existing command:
`uv run --locked python -m astral_b1 smoke --output artifacts/smoke-001`
Choose a different interface only with a documented reason. Never fabricate
resolved dependency hashes.

Stop before any API integration, GPU launch, learned router, or empirical claim.
Submit tests, limitations, and a handoff.
