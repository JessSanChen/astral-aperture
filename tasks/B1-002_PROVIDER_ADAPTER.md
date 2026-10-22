# B1-002 — fixed-judge gateway and replay cache
Status: proposed; paid/API calls require separate authorization.
Depends on: reviewed B1-001 interfaces.

Implement a mock-tested gateway with OpenRouter and/or a compatible self-hosted
backend, exact request logging, explicit route restrictions, capability checks,
bounded documented retries, and complete failure accounting. Pin configuration per
experimental arm; actual model/provider deviations must fail or invalidate the arm.

Cache by exact request/config/history and sample identity, not only episode/action.
Partition namespaces and deny controller access to the backing bank. Record actual
collection costs separately from replay-equivalent inspection costs.

Acceptance includes injected rate-limit/timeouts/parse errors, forbidden fallback,
cache-hit correctness, independent repeats that do not collapse, a crash/resume test,
and offline report reconstruction. Document unavailable metadata honestly. Do not
infer immutability from provider names. Unit tests use fixtures, not real paid calls.

After human approval of identity, terms/privacy, and maximum job scope, a small live
development check may be separately authorized and recorded. No sealed test access,
auto-provider substitution, or large sweep in this task.
