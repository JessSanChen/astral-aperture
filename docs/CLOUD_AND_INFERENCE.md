# Cloud and inference runbook — proposed, no accounts configured

## Claude Code and Codex are engineers, not the experimental subjects

Use either as implementer and the other as reviewer. Reverse roles as needed; no
empirical claim about their relative coding quality is assumed. Give one issue at
a time, an explicit worktree, allowed paths, tests, and a completion contract. Use
normal sandbox/approval controls. Do not give unrestricted cloud deletion, test-label,
or production credentials. A reviewer provides another check, not independent truth.

## Runpod

Use explicit Pods for initial persistent model-serving and training experiments.
Use a stable laptop/CPU host to schedule API work and aggregate reports; GPU workers
should not be the only place where code, logs, or results exist.

On a worker:
- Pull an approved image by digest and a clean source revision. Do not edit code in
  a running confirmatory job. Record CUDA/driver/GPU and serving configuration.
- Mount a deliberately chosen persistent volume. Verify the actual mount with
  `df -h`; do not assume the path name alone establishes persistence.
- Keep checkpoints/response banks on persistent storage and publish verified copies
  to the canonical artifact store. Local scratch is replaceable.
- Use an authenticated inference service through a private connection/SSH tunnel;
  do not expose an unauthenticated model server to the public internet.
- Checkpoint/resume by run and shard IDs. A preempted worker must not cause silent
  duplicate aggregation or overwrite successful results.
- Verify restore from backup before large runs. Stopping, terminating a Pod, and
  deleting a network volume are different actions with different data consequences.

Runpod docs distinguish ephemeral container storage, Pod-lifetime volume storage,
and independent network/global volumes. Standard network volumes have placement
constraints; select compatible region/GPU availability. Do not use an illustrative
price or assumed GPU inventory as a planning fact. See SOURCES.md.

## Fixed judges: use two complementary tracks

Proposed primary reproducibility track: self-host available open-weight judge
checkpoints with immutable weight/tokenizer revisions and fixed serving settings.
Proposed external-validity track: strong hosted judges through an explicitly routed
API with archived responses. Neither checkpoint identities nor licenses are selected.
B trains controllers; it does not require training these judges.

This is not a claim that open-weight models must supply the best decisions. It
separates weight-level control from access to stronger or different hosted models.
Hosted endpoint pinning constrains routing but does not prove immutable backend weights.

## OpenRouter wrapper

1. Use an exact selected model identifier and explicit endpoint slug where available.
   A base provider slug may encompass multiple regions/variants.
2. Restrict the allowed endpoint and disable fallbacks. Do not use automatic model
   selection or fallback model arrays for a fixed-judge arm.
3. Require support for requested parameters; unsupported settings should fail.
4. Keep exact messages, policy/system prompt, tools/schema, decode settings, and parser
   fixed. No web/tool access should be added implicitly to a judge.
5. Use appropriate retention/data-collection restrictions after checking endpoint
   compatibility and authorization. ZDR does not make an API local or authorize data
   transfer. Closed models' output-use/distillation terms need separate review before
   training on their outputs or producing derivative datasets.
6. Record requested identity, returned model/provider metadata when available,
   generation/request IDs, timestamp, usage, cost, finish reason, and every attempt.
   Mark unavailable metadata unknown rather than synthesizing it.
7. Preserve failures and refusals. Do not change providers/prompts to get a preferred
   answer. Retries must follow a prespecified rule and count in operational cost.

Use `configs/openrouter.judge.template.json` only as an application config starting
point. It contains unresolved fields and is not an API-ready request.

## Response cache and reproducibility

Key by a hash of the exact normalized request, complete revealed/action history,
backend/model/endpoint configuration, judge prompt/policy, tool schema, decode settings,
parser version, dataset provenance/version, and replicate/sample ID. Store response
hashes separately. Deliberate rereads/repeats need new sample identities. A retry is
an attempt within a logical call, not an independent research replicate.

Never cache solely by episode and action. Observation order and previous results can
change the request. Partition cache namespaces by experiment role and data split;
controllers must not browse cached counterfactual or held-out outcomes.

Offline replay has near-zero new inference cost, but each simulated policy still
incurs its defined inspection cost. Record that replay-equivalent resource use
separately from actual collection/training/replay spending. Do not use replay wall
time as a deployment latency estimate; measure fresh inference separately.
