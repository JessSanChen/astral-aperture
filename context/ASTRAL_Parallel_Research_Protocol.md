# ASTRAL — parallel research protocol

**21 October 2026.** Parallel pursuit of B and C is user-approved. Everything below is an assistant-proposed coordination scheme, not a commitment to a particular implementation or paper count.

## 1. Independence first

B studies inspection decisions with fixed downstream judges for its main comparisons. C studies judgment/training with fixed observation conditions for its main comparisons. Either can proceed, produce a negative result, or change direction without blocking the other. Neither requires private partner logs, deployment access, or a substantial misuse corpus.

Use existing ASTRAL as a versioned baseline and preserve its original policy. An adaptation to a neutral task must be marked as an architecture comparison, not an unchanged baseline. Code access and compatibility must be checked rather than assumed.

## 2. Minimal shared interfaces — proposed, not a platform rewrite

| Object | Minimum information | Important boundary |
|---|---|---|
| Trace/episode | Stable ID; task family; visible events; provenance; time/order; observation mask | Full simulator state and withheld evidence are evaluator-only. |
| Policy | ID/version; authorized text or specification; provenance; target decision | Trusted policy input is separate from transcript content. |
| Judge result | Verdict; applicable rule IDs where defined; evidence references; uncertainty/abstention; model/config version | A judgment is not an oracle label or a guarantee of safety. |
| Inspection action | Allowed observation request or judge call; cost; revealed information; selection probability if randomized | Information unavailable to the deployer cannot be acquired by fiat. |
| Oracle record | Independently checked outcome; specification version; label provenance; answerability where applicable | Never silently exposed to the tested monitor. |
| Evaluation record | Split ID; complete cost accounting; errors; latency; seeds; versions | Failures, retries, missing data, and exclusions must be visible. |

Do not require every task to fit one elaborate universal schema. Start with the intersection needed for reproducibility and adapters. Common tooling is useful; common generators and evaluators can also create correlated artifacts. Maintain independently constructed tests and branch-specific frozen evaluation sets.

## 3. Shared work versus separate work

Share ingestion/replay, immutable model and policy identifiers, safe environments where suitable, oracle-test conventions, provenance, cost accounting, and reporting. Separate the main scientific objectives, optimization, development feedback, and final held-out claims.

One branch must not inspect or tune against the other's held-out labels and then present that data as fresh independent evaluation. Record when any shared artifact has entered development. A successful oracle on one environment is not proof of correct labels on an adapted environment.

## 4. Later interaction test — optional

| | Existing fixed judge | C's candidate judge |
|---|---|---|
| Existing fixed inspection | Shared reference | Isolates C under baseline inspection |
| B's candidate inspection | Isolates B with baseline judge | Interaction test |

Use compatible task/policy conditions and report interactions instead of assigning all gains to both methods. Each branch's main result must remain interpretable before this combined test. A joint system is not automatically two independent scientific contributions.

## 5. Shared review standards

Every proposal should include: question; closest prior work; exact difference; data and label provenance; method; strongest simple baseline; main experiment and ablations; access/resource requirements; uncertainty estimates; stop criterion; negative-result interpretation; and reusable ASTRAL deliverable.

Record whether a finding comes from a primary source, a replication, a new experiment, or an assistant inference. Keep published result, preprint claim, conjecture, and user decision distinct. Search for competing papers rather than selecting only favorable comparisons. A thorough review need not reproduce every numerical result; emphasize arguments and assumptions.

For resources, distinguish plentiful research compute/money from actual model access, staff time, annotation quality, permissions, and the elapsed schedule. For B, justify deployment budgets separately. For C, do not assume training must be small. The ten-week horizon is a planning checkpoint, not proof that a complete top-conference result will fit.

## 6. Proposed checkpoints

**Initial review:** a serious nearest-neighbor comparison, two or three candidate questions, and the simplest experiment capable of defeating each claim.

**Pilot:** executable labels pass independent tests; a strong baseline establishes a meaningful problem; the mechanism can be isolated; the partner-independent route is real.

**Main study:** freeze the core question and primary test protocol before large-scale optimization. Scale only where it increases evidence or tests a scaling hypothesis.

**Fellowship checkpoint:** each branch reports its strongest supported claim, remaining blockers, reproducible artifacts, and a continue/pivot/stop recommendation. A partial but sound result is preferable to claiming completion without adequate evidence.

No fixed allocation between branches, staffing split, architecture, or submission deadline is imposed by this document.

## 7. Branch-status export template

Use this after each substantive research-design update. Transfer it explicitly between chats; do not assume the other chat has seen or approved it.

- Branch, date, and artifact version:
- Current question and status (proposed / user-approved / tested):
- Threat model and observation boundary:
- Nearest prior work, exact overlap, and source links:
- Proposed scientific difference and evidence for the gap:
- Main baseline and decisive experiment:
- Dataset/oracle provenance and leakage controls:
- Results, with uncertainty, or explicitly “not yet run”:
- Supported claim and claim not supported:
- Required shared interface or artifact:
- Independent dependencies and unresolved access issues:
- Stop/pivot criterion and current recommendation:
- User-confirmed decisions to add to the brief:
- Next experiment:

A chat may propose a decision-log entry. Only explicit user approval turns a recommendation into a project commitment. Existing confirmed decisions can be recorded without re-asking.

## 8. What the shared project must not drift into

No mandatory federation, private-corpus collection, partner integration, or universal safety framework. No claims that controlled software-workflow results validate biological intent detection or prevent harm. No hazardous biological examples or operational evasion instructions. Privacy, authorization, and safe release remain prerequisites, not the main scientific contribution.
