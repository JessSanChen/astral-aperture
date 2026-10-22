# Source and verification notes

**Tool documentation checked: 21 October 2026.** These sources support tooling
mechanics, not the scientific novelty or empirical success of B1. Account permissions,
installed versions, regional inventory, licenses for selected models, and real calls
were not checked. Revalidate capabilities at installation and record installed versions.

| Primary source | Checked point |
|---|---|
| Claude Code memory: `https://code.claude.com/docs/en/memory` | File instructions/imports; tool-local auto-memory scope; compact instruction entrypoints |
| Codex AGENTS.md: `https://developers.openai.com/codex/guides/agents-md` (redirects to official ChatGPT Learn) | Project instruction discovery and overrides |
| Codex security: `https://developers.openai.com/codex/security` | Sandbox and approval boundaries |
| Claude Code permissions: `https://code.claude.com/docs/en/permissions` | Permissions versus sandboxing; shared approval scope |
| Git worktree: `https://git-scm.com/docs/git-worktree` | Multiple working trees for separate branches/reviews |
| uv locking: `https://docs.astral.sh/uv/concepts/projects/sync/` | `--locked` checks staleness; `--frozen` skips that check |
| OpenRouter routing: `https://openrouter.ai/docs/guides/routing/provider-selection` | Exact endpoint slugs, only/order, fallbacks, require_parameters, retention controls |
| OpenRouter generation metadata: `https://openrouter.ai/docs/api/api-reference/generations/get-generation` | Provider/model/request/usage fields; record unavailable fields honestly |
| OpenRouter ZDR: `https://openrouter.ai/blog/insights/zero-data-retention/` | Retention does not make processing local or control your own logs |
| Runpod storage: `https://docs.runpod.io/pods/storage/types` | Different persistence lifetimes for storage types |
| Runpod network volumes: `https://docs.runpod.io/storage/network-volumes` | Independent persistent volumes and placement constraints |
| vLLM online serving: `https://docs.vllm.ai/en/latest/serving/online_serving/` | Self-hosted serving option; configure model/template/generation settings explicitly |
| W&B experiments: `https://docs.wandb.ai/models/track` (redirects to CoreWeave docs) | Optional metrics/config/artifact tracking |

## Supplied project sources

`context/ASTRAL_Project_Brief_v4_B1_Selected.md` is copied unchanged and records the
selected direction. The parallel protocol and earlier B handoff are likewise copied
unchanged. Their methods and interfaces remain proposals where labeled that way.

The prior assistant's `context/ASTRAL_B_Source_Ledger_and_Status_2026-10-21_v0.1.md`
is preserved for provenance, not revalidated in this setup task. Its older authority
and branch-status text is superseded by v4. Do not cite its paper claims as newly
verified findings, copy source-specific guarantees without checking assumptions,
or treat linked code as permission to reuse it.
