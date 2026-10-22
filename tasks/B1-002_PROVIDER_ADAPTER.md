# B1-002: fixed-judge gateway and replay cache
Status: proposed; live API calls require separate authorization.
Depends on: reviewed B1-001 interfaces.

Implement a mock-tested gateway with OpenRouter and/or a compatible self-hosted
backend: exact request logging, explicit route restrictions, capability checks,
bounded documented retries, and complete failure accounting. Pin configuration per
experimental arm; actual model or provider deviations must fail or invalidate the arm.

Cache by exact request, config, history, and sample identity, not only episode and
action. Partition namespaces and deny controller access to the backing bank. Record
replay-equivalent inspection usage separately from what collection actually used.

Acceptance: injected rate-limit, timeout, and parse-error cases; forbidden fallback;
cache-hit correctness; independent repeats that do not collapse; a crash/resume test;
offline report reconstruction. Document unavailable metadata honestly. Unit tests use
fixtures, not live calls.

After human approval of identity, terms, and privacy settings, a small live
development check may be separately authorized and recorded. No sealed test access
or automatic provider substitution in this task.
