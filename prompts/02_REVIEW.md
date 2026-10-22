Read AGENTS.md, the assigned task, the implementation handoff, and the actual diff.
Review in a separate checkout/worktree with no cloud-admin or sealed-test credentials.
Do not trust claimed test success: reproduce the stated checks when possible.

Prioritize scientific correctness: oracle leakage, unauthorized observations,
metadata/split leakage, changes to fixed judges, missing failure denominators,
pre-/post-audit contamination, invalid cache/sample semantics, and baseline unfairness.
Then review ordinary engineering and security: dependency reproducibility, resume,
artifacts, secrets, permissive access, and destructive commands.

Report defects with severity, concrete file locations, and a reproducer/test where
possible. Note any check you could not run. Do not treat agreement between coding
agents as independent oracle validation. Do not silently broaden scope or merge.
End with a recommendation: ready for human review, needs correction, or blocked.
