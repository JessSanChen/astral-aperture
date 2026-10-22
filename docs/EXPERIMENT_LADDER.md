# Build and experiment ladder -- proposed

## Stage 0: audit, not redesign

Inspect accessible ASTRAL code, current tests, policy/config versions, and interfaces.
Record what is actually available. A missing repository must not become an invented
integration. Preserve any baseline source/configuration at an immutable revision.

## Stage 1: offline development smoke slice

One harmless dummy-approval workflow; roughly 20-50 development executions; two
mock judges; stop/retrieve/reread actions; one acquisition initially. The exact count
is an engineering choice, not a scientific sample-size justification.

Demonstrate generation -> restricted observations -> inspection -> locked verdict
-> evaluator-only scoring -> local report. Include deliberately good/bad mock
responses to test correction, no change, and corruption bookkeeping. These injected
behaviors validate plumbing only and are not evidence that real LLM routing helps.

## Stage 2: controlled real-judge development run

After explicit external-call authorization, select one fixed available model/endpoint
and run a small development batch. Check request identity, timeout/parse/refusal
handling, evidence access, retries, and accounting. Cache exact request/response
pairs and metadata. Confirm the same report can be rebuilt with networking disabled.

## Stage 3: scientific pilot

Expand to multiple independently specified workflow families and several fixed
judges. Final sizes follow observed variation and the held-out question; the earlier
8-family/thousands-of-episodes outline remains a proposal. Freeze development and
evaluation boundaries before comparative tuning.

Answer in order:
1. Do permitted inspections reproducibly change errors enough to matter?
2. Can useful actions be predicted from allowed information rather than oracle state?
3. Does action-value prediction transfer beyond development families and renderers?

An empirical best-branch selector is evaluator-only and often optimistic. Do not
call a maximum over lucky stochastic samples attainable performance. Use repeated
samples or independent action-selection/assessment samples for expected-gain analysis.

## Stage 4: main comparisons

Only after the pilot identifies a meaningful gap, compare the proposed controller
against risk/uncertainty, fixed sequences, action-aware conditional-loss acquisition,
and full-authorized-inspection references. Preselect the primary metric and burden/
resource comparison; preserve per-family results and paired/clustered uncertainty.
Full inspection is not truth and must not be made artificially weak.

## Required metrics and error handling

Report missed-positive mass, false-negative rate when its denominator is supported,
unnecessary-review burden, alert volume, abstentions, correction and corruption
counts, latency/resource vectors, and failures. Every rate must show its denominator.
Keep pre-audit decisions immutable; post-audit repair is a separate outcome.

The smoke report can omit confidence intervals because it is engineering-only; the
scientific pilot must implement uncertainty matching base-world/family grouping.
Never treat cached repetitions or paraphrases as independent executions.

## Stop/pivot

No usable headroom, action value predictable only from hidden facts, lack of held-out
transfer, unreliable oracle/rendering, or parity with a strong existing method are
valid reasons to change the research claim. Do not quietly pivot into C, add private
data dependencies, or remove difficult cases to maintain an improvement claim.
