ASTRAL — project brief, version 4
Prepared 20 October 2026; versions 3 and 4 prepared 21 October 2026. Version 3 recorded the user's explicit decision to investigate B and C in parallel. Version 4 additionally records the user's explicit selection of B1 as the lead direction within B: transferable inspection value for fixed, fallible judges. Prior versions and the historical research-plan draft are preserved. This is a context handoff, not an independent audit of the implementation. The B1 direction is selected; detailed hypotheses, methods, environments, staffing, and publication claims remain proposals unless separately approved. C remains independently active.

Current precedence: current explicit user instructions > this brief's confirmed decisions > branch handoffs as proposals > older plan drafts. The historical preference for A and affordability-based limits on C are superseded. A proposal in a branch does not become a shared decision without user approval.
1. Person, aims, and constraints
The user is a research engineer on an AIxBiosecurity fellowship. The original planning reference is approximately ten weeks; exact start/end dates have not been specified. Scheduling should be considered separately from research-resource availability.

User-confirmed resource assumption: money, compute, inference, and associated research expenditure are not limiting constraints. Do not restrict proposals to lightweight methods, small fine-tunes, small datasets, or modest experiments on affordability grounds. Specific model access and data permissions still need to be established for any concrete design.

User-confirmed dependency constraint: the core research must not depend on working with external deployment partners. Essential data generation, independent labeling, training, experiments, and evaluation must have a partner-independent path. A partner may provide optional external validation, never a prerequisite for the main result.

Publication ambition: the user targets a top conference. This is an ambition, not a prediction of acceptance or evidence of novelty.

Two outputs matter:
- Team priority: prepare the existing ASTRAL system for prospective partners.
- User priority: produce a publishable methodological or technical contribution even without partner integration or a substantial real transcript corpus.
Do not assume access to a substantial real misuse transcript corpus or deployed partner integration. Public resources, independently built safe environments, and independently commissioned expert assessment may support the core, subject to availability and authorization. Abundant compute does not by itself validate synthetic labels or establish deployment performance. Any real-world pilot should be an extension, not the critical path.

The user prefers technical and methodological research over governance work. They are open to changing or broadening the research threat model, provided the change is explicit and the connection to ASTRAL is honest.
2. Original ASTRAL design, as described by the user
ASTRAL is an open-source scanner run by an organization over its own AI interaction logs. It flags conversation-level biological-misuse risk for human review; it does not itself block requests.

Proposed adopters include inference providers, AI-scientist platforms, and enterprise deployers. The initial motivation is that a user can move outside a frontier provider's complete safeguard stack, while evidence of concern may span multiple messages or sessions.

The current pipeline is:
1. Keyword filtering.
2. Sentence-embedding similarity to a private reference concept set.
3. An expensive LLM judge over selected full transcripts.
4. A hand-designed formula combining four rubric variables into a risk score.
The four variables are user scientific capability, safeguard-bypass severity, furthest biological kill-chain stage, and potential harm scope. The judge prompt has been tuned with an automatic prompt optimizer.

Development/evaluation has used a few hundred synthetic conversations. LLM-simulated actors were assigned parameters from the same taxonomy the judge scores; those generator parameters served as labels rather than independent readings of the actual generated text.
3. Concerns motivating reconsideration
The user questions:
- Whether the rubric's constructs are observable, well defined, or scientifically justified.
- Whether synthetic labels measure what the transcript actually establishes.
- Whether the cascade misses evidence before the judge sees it.
- Whether monitoring is robust to adversarial inputs or only recognizes familiar dual-use content.
- Whether likely adopters have sufficient incentive, context, or review capacity.
- Whether a bio-only service is worth integrating compared with existing generic tools.
- Whether longitudinal monitoring implies new retention requirements.
- Whether a central, long-lived corpus of partner transcripts is feasible.
These concerns should remain open research/product questions; they are not all demonstrated failures of the implementation.
4. Earlier brainstorm: retain as possibilities, not commitments
The user considered an extensible open-source framework that distributes domain expertise across multiple domains, supports local use and testing, and improves upstream without raw transcript export. Federated-learning-inspired mechanisms were proposed as one route.

Subsequent discussion separated:
- A maintained domain policy/rubric and its tests.
- A model or process that interprets a fixed policy.
- Operational routing, auditing, and review configuration.
- Local evaluation and optional approved feedback.
- Federated prompt or model training.
A local evaluator is not inherently private; derived outputs can disclose information. Conversely, federated learning is not inherently impossible to protect. Privacy and integrity guarantees require specific threat models and mechanisms. No particular federated architecture has been selected.

The user now wants technical alternatives that need neither federation nor partner access. Do not assume that a fixed prompted judge always outperforms learning; that is an empirical question. Keep policy changes separate from training the interpreter.
5. Active parallel research tracks — B1 lead selected; exact methods not selected
A shared local replay-and-evaluation harness remains an assistant recommendation for connecting research to future partner readiness. The existing scanner should remain a versioned baseline.

The earlier assistant recommendation was Candidate A: evidence-aware monitoring under incomplete observations. The user questioned its novelty and expressed more interest in B and C. A is not an approved flagship project; evidence and observability controls can remain useful evaluation components.

Candidate B (provisional): adaptive inspection and auditing that improves detection and discovers a monitor's blind spots under selective observation. A budget in B refers to a motivated deployment constraint or experimental variable (such as latency, review capacity, or inspection cost), not the researcher's ability to pay for computation. Do not make cheapness itself the primary scientific contribution without justification.

21 October 2026 update — user-selected lead within B: B1, transferable action-specific inspection value for fixed, fallible judges. Study whether a controller can choose observations or fixed-judge computations that improve decisions on unfamiliar workflow families. Selecting this direction does not approve a particular algorithm, representation, training recipe, experimental scale, operational budget, or novelty claim. Statistical auditing remains a proposed evaluation component; B2 and B3 have not been selected as co-primary studies.

Candidate C (provisional): training policy-conditioned interpreters for systematic generalization across rules, compositions, and interaction histories, using independently grounded or executable supervision. Substantial training, verifier-reward experiments, multi-model comparisons, and large-scale evaluations are in scope if scientifically useful. The earlier framing of C as only a small local fine-tune is superseded.

User-approved direction: investigate and pursue B and C in parallel in separate chats. Do not force an immediate choice between them. Neither branch is required to wait for a method, model, partner, or positive result from the other. Shared infrastructure is desirable where it does not contaminate evaluation or create dependencies.

B1 is now the selected lead direction within B. Detailed hypotheses and methods in both branches remain proposals, not verified novelty claims or approved methods. Parallel pursuit does not commit to two accepted papers, equal staffing, or a particular eventual combination. Existing literature claims from the conversation need primary-source verification before use.

The initial controlled scope can concern observable policy-relevant events in safe sandbox environments, not hidden malicious intent or real-world biological attack prevalence. A biological application does not inherit validation from a non-biological sandbox.
6. Shared engineering deliverable
Proposed components:
- Versioned, provenance-preserving local trace schema.
- Adapter for existing ASTRAL inputs, without assuming a new logging policy.
- Frozen baseline wrapper for the current cascade and rubric.
- Local replay runner and pluggable judge interface.
- Explicit handling of missing observations, parsing failures, truncation, and timeouts.
- Stage-level records showing which cases were filtered or deeply assessed.
- Per-run versions, configurations, costs, and reproducible reports.
- Default absence of raw-transcript export or telemetry; local models or explicitly approved external model calls.
This is evaluation readiness, not proof of production readiness or a security certification.
7. Evaluation principles
A simulated actor's assigned motive is not a verified label of its transcript. Prefer outcomes checked from an executable environment for tasks where that is possible. Keep the environment oracle separate from monitor-visible observations.

Track both the full-world outcome and what is inferable from the visible record. A genuinely unanswerable observation should not be treated as an ordinary classification mistake.

Control generation artifacts with held-out scenarios, renderer/model families, and independent human inspection where feasible. Synthetic tests can support controlled mechanism claims, not deployment prevalence or real biological-misuse recall.

Equalize information access and account for all computation in method comparisons. Evaluate abstention together with useful coverage; abstaining on everything is not a successful monitor.

Research may include bounded adversarial tests in authorized toy environments. Do not publish hazardous biological content or operational evasion techniques.
8. Decision status and unknowns
Confirmed by the user:
- Approximately ten weeks was the original fellowship planning reference; resource availability is a separate issue.
- Money, compute, inference, and associated research expenditure are not limiting constraints.
- No dependency on working with partners for the core result.
- Do not assume substantial real misuse transcript access.
- Dual priority: future partner preparation and independent research output.
- Top-conference publication ambition, without a guarantee of acceptance.
- Preference for technical/methodological work.
- Investigate and pursue B and C in parallel, with separate research chats; concern that A is insufficiently novel or ambitious.
- Select B1 as the lead direction within B: transferable inspection value for fixed, fallible judges (21 October 2026).
- Openness to revised threat models.
Not yet selected:
- Detailed hypotheses and contributions within the selected B1 direction; the exact C question; specific venue; and eventual relationship between publications.
- Monitor method and evaluation environments.
- Specific model/checkpoint access and training design.
- Expert-assessment arrangements and data permissions.
- A final schedule and time allocation.
- Any commitment to federation, cross-domain deployment, or a product pivot.
Earlier literature-review responses are brainstorming inputs, not a verified bibliography. Verify sources and claims before inclusion in a paper.
9. Suggested conversation organization
Use two research chats initially:
- ASTRAL B — Adaptive inspection, auditing, and blind-spot discovery.
- ASTRAL C — Learning policy interpreters and systematic generalization.
Each branch must begin with a primary-source literature review, nearest-prior-work comparison, and partner-independent proposal covering question, scope, experiment, requirements, and failure criteria. Each must identify what can be borrowed rather than invented.

Use the branch-specific handoff and opening prompt. The shared protocol proposes compatible interfaces and a compact status-export format. Do not assume work in one chat has automatically been read, adopted, or approved in the other. Transfer findings explicitly with citations, version identifiers, and decision status. Keep this brief as the compact human-reviewed record of confirmed constraints and decisions.
10. User-confirmed constraint and decision log
21 October 2026 — resource availability and partner independence
Status: explicitly confirmed by the user. The user stated: “i am not resource constrained in terms of money, compute, inference, etc -- but i don't want to be dependent on working with partners.”

Recorded implications: remove affordability-based limits on research methods and experimental scale; require an end-to-end partner-independent core; retain future partner evaluation as an optional extension. The distinction between a deployment budget and research resources must be explicit in Candidate B.

Status at that earlier decision: no selection of A, B, or C; no approval of a particular architecture, threat model, training recipe, or product pivot. The later parallel-pursuit decision below supersedes only the branch-selection status.

Related-document status: the original research-plan draft remains a historical proposal. Its preference for A and its “small fine-tune only if resources permit” language are not current constraints. This revision does not silently approve a replacement plan or rewrite the original draft.
21 October 2026 — parallel pursuit of B and C
Status: explicitly confirmed by the user. The user requested: “let's actually investigate and pursue B and C in parallel” and specified separate chats with thorough literature reviews and proposed questions, scopes, plans, and requirements.

Recorded decisions: B and C are both active investigations. The core of each must remain partner-independent. Abundant money, compute, and inference remain available. Technical ambition and top-conference standards remain goals, not predictions of novelty or acceptance.

Assistant recommendations, not new commitments: freeze judges for B's primary comparisons; freeze observation conditions for C's primary comparisons; share a small replay/evaluation interface; combine methods only after independent effects are measured. Use roughly ten weeks as the original fellowship checkpoint and show longer extensions separately. Do not infer a new hard deadline or unlimited calendar availability.

Still unresolved: exact hypotheses, methods, environments, oracle semantics, model access, expert arrangements, staffing, submission venue, publication count, and any deployment or product pivot. No permission to change retention policies or obtain private logs is implied.

New handoff artifacts: ASTRAL_B_Research_Handoff.md; ASTRAL_C_Research_Handoff.md; ASTRAL_Parallel_Research_Protocol.md; branch opening prompts. These operationalize the investigation request; they are not approved experimental protocols.

21 October 2026 — selection of B1 within the B branch
Status: explicitly confirmed by the user. The user stated: “let's do b1” and requested a fundamental explanation and research-manager meeting talking points.

Recorded decision: B1 is the lead research direction within B, referring to the preceding proposal on transferable action-specific inspection value for fixed, fallible judges. B and C remain independent parallel investigations; no dependency on a C-produced judge or a deployment partner is introduced.

Not newly approved: the proposed factorized evidence representation, any reinforcement-learning architecture, dataset sizes, model identities, staffing commitments, detailed schedule, budget values, experimental protocol, or publication claim. No experimental result has yet been reported. The meeting preparation and pilot specifications remain recommendations for discussion.

Record scope: this entry records the user's explicit direction choice only. The remainder of this brief retains its stated evidence and proposal status. Version 3 is unchanged. This generated version is a local conversation artifact, not a silent replacement of shared Project files.
