Read AGENTS.md, docs/START_HERE.md, docs/CURRENT_STATE.md, and
context/ASTRAL_Project_Brief_v4_B1_Selected.md before making changes.

Work as the implementation engineer for ASTRAL B1. B1 is selected, but no algorithm
or empirical claim is established. This repository may contain only a specification
scaffold: do not pretend the research harness exists.

First complete tasks/B1-000_REPO_AUDIT.md using any explicitly available existing
ASTRAL code. Record absent access without inventing an integration. Then implement
tasks/B1-001_OFFLINE_VERTICAL_SLICE.md. Keep the original scanner untouched. Use a
task branch, write tests, and run the offline smoke path.

Use dummy workflows and mock judges only. Do not call external APIs, provision
cloud resources, read credentials, access sealed tests, train a router, or change
the scientific question. Preserve the independent oracle and observation boundary.

Return a reviewable diff, exact commands and observed results, limitations, and a
handoff from templates/HANDOFF.md. Distinguish implemented behavior from future
interfaces and engineering tests from scientific findings. Stop after the offline
slice is demonstrated or clearly report the blocker.
