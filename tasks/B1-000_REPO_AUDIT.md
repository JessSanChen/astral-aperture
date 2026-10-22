# B1-000: audit the starting point
Status: proposed; no repository has been inspected yet.

Read AGENTS.md, CURRENT_STATE, and the v4 project brief. Inspect only repositories
explicitly made available by the user. Record source revision, structure, existing
evaluation entry points, tests, schemas, baseline policy and config, environment,
and licenses actually found. Do not invent absent paths or assume this scaffold is
ASTRAL.

Deliver `docs/REPO_AUDIT.md`: reusable components, minimal proposed additions,
known compatibility limits, and exact checks performed. If source is unavailable,
say so and propose a standalone adapter boundary. Do not rewrite the scanner.

Acceptance: claims have file/line or command evidence; reused and proposed features
are clearly separated. Finish with a handoff. No external model calls, production
data access, or baseline changes.
