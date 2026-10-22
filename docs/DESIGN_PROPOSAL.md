# Minimal architecture -- proposal

## Principle

Git stores reviewed source, small specifications, decisions, prompts, and manifests.
An artifact store holds versioned datasets, response banks, checkpoints, and run
outputs. Claude Code/Codex implement bounded tasks. An ordinary deterministic runner,
not a coding-agent conversation, executes scientific experiments. Runpod supplies
replaceable compute. OpenRouter or a self-hosted backend supplies controlled model
calls. The evaluator alone holds reference outcomes and unselected observations.

First inspect the existing ASTRAL harness. Reuse compatible adapters and reporting;
keep a separate research package or repository only where it makes comparisons safer.
Do not rewrite the deployed scanner. Pin its source, policy, configuration, and data
provenance; keep any neutral-policy adaptation explicitly labeled.

## Suggested eventual source tree

```text
astral-b1/
  AGENTS.md, CLAUDE.md
  docs/                     # decisions, current state, design, source ledger
  tasks/, handoffs/          # one task and handoff per branch/PR
  configs/                  # experiment, judge, controller, split specs
  prompts/                  # fixed experiment prompts, separately versioned
  src/astral_b1/
    contracts/              # validated records and versioned interfaces
    environments/           # harmless simulator and renderer adapters
    judges/                 # mock, API, local-server adapters
    inspections/            # permitted evidence/computation actions
    controllers/            # simple baselines first; learned methods later
    replay/                 # restricted observations and response cache
    evaluation/             # evaluator-only label join and metrics
    reporting/              # local report; optional metric-tracker mirror
  tests/                    # public development fixtures only
  infra/                    # image recipe and launch/run scripts
  pyproject.toml, uv.lock
```

The tree is an implementation target, not a claim these modules exist. Use a single
small Python package until real interface needs justify splitting it. Keep custom
control logic explicit rather than embedding it in a large autonomous-agent framework.

## Four process roles

1. **Generator/evaluator:** world state, oracle, allowed observations, test labels.
2. **Controller:** visible evidence, allowed actions, prior selected outputs, budget.
3. **Inspection/model gateway:** authenticates calls, returns only requested outputs,
   and records exact requests, provider identity, cost, latency, failures, and retries.
4. **Aggregator:** joins locked predictions to labels and produces reports.

For the mock smoke test, logical separation plus adversarial unit tests is enough
for engineering validation. For real evaluation, use distinct processes/users or
containers, no shared evaluator mounts/credentials, and a narrow message interface.
Do not pass an environment object containing oracle state into controller code.
A strong isolation claim requires an actual access-control test, not a class name.

## Minimal records

| Record | Purpose and boundary |
|---|---|
| EpisodeMetadata | Stable random ID, provenance, split grouping, family for evaluator bookkeeping; metadata is not automatically a controller feature |
| PolicySpec | Trusted policy text/specification, version, hash; distinct from transcript |
| ObservationView | Only current visible messages and allowed record handles; no labels/future branches |
| InspectionAction | Action ID, valid arguments, selection probability if applicable, resource charge |
| JudgeResult | Verdict/abstention, parse status, exact judge configuration, response reference |
| OracleRecord | Independently checked outcome, oracle version, provenance; evaluator-only |
| DecisionRecord | Initial/pre-audit/post-audit stage, timing, evidence-view hash |
| RunManifest | Immutable code/config/data/model lineage, resource usage, artifact hashes |

Do not automatically expose family IDs, scenario names, privileged directory names,
seed structure, or oracle metadata to the controller. Rendering and control metadata
need explicit allowlists. Check that summaries are computed only from allowed views.

## Staged experiment flow

Generate safe executions -> validate outcome and rendering -> freeze grouped splits
-> collect bounded inspection-response trees with fixed judges -> train on authorized
training rewards -> freeze controller -> replay held-out policies under restricted
observations -> lock pre-audit decisions -> join reference labels -> report.

The collector may see the full action tree. The replay policy must not. An offline
response bank does not establish behavior against a live adaptive actor.

## Reproducibility levels

- Deterministic replay: same frozen inputs, decisions, and cached outputs reproduce
  the report. This is the first requirement.
- Fresh model rerun: newly sampled inference can differ, even with requested seeds
  or nominal temperature zero. Report the variation.
- Independent replication: another environment/renderer implementation and fixed
  model reproduce a scientific pattern. This is not supplied by a shared cache.

## Storage and bookkeeping

Keep immutable, content-hashed artifacts with small Git manifests, and separate
credentials for training, development, and sealed evaluation. Keep a verified backup
outside any GPU worker's lifecycle. Any metrics tracker is optional; the local report
must work without it and must never upload held-out examples or credentials.

Recorded scientific runs use a committed lockfile and a pinned image, and record the
model, tokenizer, chat template, precision, serving engine, policy, decode settings,
parser, and retry rule. A source commit alone is insufficient.
