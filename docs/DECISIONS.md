# Decision register

| ID | Date | Status | Decision or fact | Basis |
|---|---|---|---|---|
| D-001 | 2026-10-21 | User-confirmed | B and C proceed independently; no partner dependency | Project brief v4, sections 5 and 10 |
| D-002 | 2026-10-21 | User-confirmed | B1 is the selected B lead; algorithm remains open | Project brief v4, B1 selection entry |
| D-003 | 2026-10-21 | User-reported access | Claude Code, Codex, Runpod, OpenRouter are available | Setup request; account permissions not inspected |
| D-004 | 2026-10-21 | User-confirmed | Compute, inference, and time costs are not constraints; agents do not scale work down for them | User instruction during repo review |
| D-005 | 2026-10-22 | User-confirmed | Development judges are `anthropic/claude-sonnet-5.5` and `anthropic/claude-opus-5.5`, each pinned to provider `anthropic` on OpenRouter, fallbacks off | `configs/judges.dev.json`; user approval in session |
| D-006 | 2026-10-22 | User-confirmed | Judge prompt must require a best-effort verdict; abstention only for unreadable input. Any prompt edit is a new recorded version | handoffs/B1-002-r1.md; user approval in session |
| P-001 | 2026-10-21 | Proposed | Repository-centered instructions and handoffs | This scaffold |
| P-002 | 2026-10-21 | Proposed | Offline smoke slice before model/cloud work | This scaffold |
| P-003 | 2026-10-21 | Proposed | Open-weight reference judges plus pinned API-model comparisons | This scaffold; identities unresolved |

An agent may propose a new entry but may not mark it accepted without human
approval. Do not edit the preserved v4 snapshot.
