# Cloud and inference notes -- proposed, no accounts configured

## Coding agents are engineers, not experimental subjects

Use Claude Code or Codex as implementer and the other as reviewer; swap as needed.
Give one task at a time with an explicit branch, allowed paths, and tests. Do not
give either unrestricted cloud deletion, test-label, or production credentials.

## Runpod

Use Pods for model serving and training. Keep code, logs, and results somewhere
other than a GPU worker alone.

- Pull an approved image by digest and a clean source revision. Record CUDA,
  driver, GPU, and serving configuration.
- Mount a persistent volume and verify the actual mount. Keep checkpoints and
  response banks there and publish verified copies to the artifact store.
- Serve inference behind authentication or an SSH tunnel, never openly.
- Checkpoint and resume by run and shard IDs so a preempted worker cannot cause
  duplicate aggregation or overwrite good results.
- Stopping a Pod, terminating it, and deleting a network volume have different
  data consequences. Verify restores before large runs.

## Fixed judges: two tracks

Reproducibility track: self-hosted open-weight judges with immutable weight and
tokenizer revisions and fixed serving settings. External-validity track: strong
hosted judges through an explicitly routed API with archived responses. Neither
identities nor licenses are selected yet. Hosted endpoint pinning constrains routing
but does not prove immutable backend weights.

## OpenRouter

- Use an exact model identifier and an explicit endpoint slug. Disable fallbacks and
  automatic model selection for any fixed-judge arm.
- Require support for requested parameters; unsupported settings fail.
- Keep messages, policy, tools, decode settings, and parser fixed. No implicit tool
  or web access for a judge.
- Check retention and data-use terms before training on closed-model outputs.
- Record requested identity, returned metadata, request IDs, usage, finish reason,
  and every attempt. Mark unavailable metadata unknown rather than inventing it.
- Preserve failures and refusals. Retries follow a prespecified rule.

`configs/openrouter.judge.template.json` is a starting point with unresolved fields,
not an API-ready request.

## Response cache

Key by a hash of the exact normalized request, the complete revealed history,
backend and model configuration, judge prompt, decode settings, parser version,
dataset version, and sample ID. Never cache by episode and action alone. Deliberate
repeats need new sample identities; a retry is not an independent replicate.
Partition cache namespaces by role and split so controllers cannot browse
counterfactual or held-out outcomes.

Offline replay still charges each simulated policy its defined inspection cost.
Record that separately from what collection actually used, since inspection burden
is a measured research variable rather than a spending concern.
