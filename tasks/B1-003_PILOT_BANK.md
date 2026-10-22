# B1-003: scientific pilot design and inspection bank
Status: proposed; experimental protocol requires human review.
Depends on: working bounded replay/gateway and independently reviewed labels.

Draft an experiment specification before collecting a large bank. Define independent
workflow-family holdouts, rendering validation, judges, primary metric, baselines,
resource frontier, stochastic replicates, and uncertainty. Keep full-inspection and
strong action-aware acquisition references. Do not select a complex algorithm first.

Collect bounded one- and two-step inspection histories on training and development
examples. The evaluator sees counterfactual branches; the tested controller sees only
selected outputs. Test headroom, allowed-information predictability, then held-out
transfer. Describe any optimistic best-branch diagnostic and avoid cherry-picking
lucky model samples. Final holdout labels and caches use separate storage and
credentials.

Acceptance: an approved spec, trustworthy labels, access-boundary checks, complete
failure accounting, and a replayable report. A negative result is acceptable; silent
task simplification, output relabeling, or test tuning is not.
