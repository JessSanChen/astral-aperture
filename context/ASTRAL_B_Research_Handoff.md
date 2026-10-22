# ASTRAL B — Adaptive inspection, auditing, and blind-spot discovery

**Research handoff | 21 October 2026 | Parallel investigation approved; methods remain proposals**

Read this as a self-contained brief for the B chat. Your role is a critical technical collaborator: investigate the strongest defensible question in this direction, not advocate for the last assistant's preferred algorithm. C is being investigated separately and must not be on B's critical path.

## Shared context and authority

**Confirmed by the user.** I am a research engineer on an AIxBiosecurity fellowship. I want two aligned outputs: prepare the existing ASTRAL system for possible future local partner evaluation, and produce a rigorous methodological or technical artifact suitable for a top-conference submission. The team emphasizes partner readiness; I emphasize research. A publication goal is not evidence of novelty or a promise of acceptance.

Money, compute, inference, and associated research spending are not binding constraints. Do not restrict the proposal to a lightweight method or small fine-tune on affordability grounds. Model licenses, checkpoint access, expert recruitment, data permissions, staffing, and elapsed experimental time are still requirements to establish. Approximately ten weeks was the original fellowship planning reference: provide a meaningful checkpoint on that horizon and distinguish longer extensions. Do not silently turn it into either an absolute research deadline or unlimited calendar time.

**The binding dependency constraint is partner independence.** The essential data, labels, training, experiments, and evaluation must be obtainable without a provider supplying private logs, installing ASTRAL, or granting production access. Substantial real misuse transcripts should not be assumed. Public resources, purpose-built safe environments, and independently commissioned experts are allowed. Partner independence does not mean no human expertise or synthetic-only evidence. Partner results are optional external validation.

ASTRAL, as described by the user rather than independently audited, is a local open-source scanner of an organization's AI transcripts. It monitors and flags for review; it does not block or establish harm prevention. Its cascade uses keywords, embedding similarity to private concepts, then an LLM judge over selected conversations. A hand-designed score combines user scientific capability, safeguard-bypass severity, furthest biological kill-chain stage, and harm scope. Prompt optimization and evaluation used a few hundred LLM-generated conversations labeled by assigned generator parameters from the same taxonomy. That creates concerns about construct validity, unexpressed latent labels, shared artifacts, gate misses, and rare-event evaluation; these are concerns, not an audited catalog of implementation failures.

Keep the current scanner as a versioned baseline. Reuse its evaluation infrastructure when accessible; source-code access has not been established by this handoff. On non-biological tasks, an architectural adaptation with a different fixed policy must be labeled as such, not presented as the unchanged bio scanner.

The user has explicitly approved investigating and pursuing B and C in parallel. No specific method, theorem, architecture, venue, or paper count is approved. Earlier assistant preferences for A and recommendations that C stay small are superseded. A's observability distinctions remain useful controls, not the default flagship question. Federated training, a universal safety platform, and a product pivot are not requirements.

Prefer technical work to governance research. Keep necessary authorization, privacy, and research-safety conditions explicit but proportionate. Use fictional sandbox workflows and dummy artifacts; do not generate hazardous biological procedures or operational evasion guidance. Any changed threat model must identify actor, objective, observations, attacker knowledge and controls, defender actions, and the limited transfer back to ASTRAL.

**Source provenance:** this context derives from ASTRAL_Project_Brief_v2.md and the user's subsequent explicit approval of parallel pursuit, recorded in ASTRAL_Project_Brief_v3.md. The old research-plan draft is historical proposal material. Earlier assistant literature claims are leads, not an authoritative bibliography.

## B's starting question — provisional, not a commitment

Can a monitor allocate heterogeneous inspection actions to improve detection while discovering its own blind spots and estimating errors under selective observation?

That formulation combines several objectives. Your first job is to determine whether combining them is scientifically productive or whether one should be the main target. Compare at least these three candidate formulations:

1. **Value of additional evidence:** choose between retrieving authorized context, reading another segment, consulting another judge, or independent adjudication. Does learning the marginal value of these observations outperform routing by suspicion or uncertainty?
2. **Detection versus evaluation:** allocate inspections between finding review-worthy episodes and estimating a frozen monitor's missed-error mass or conditional error rate. Is there a nontrivial frontier beyond existing active search/testing and robust active inference?
3. **Blind-spot discovery under change:** identify previously poorly detected families under explicit distribution shift or bounded adaptive pressure. What can be learned without assuming the router's confidence is calibrated or independent of judge errors?

These are search hypotheses, not a requirement to build all three. Recommend a primary scientific target after reviewing the literature. More spending or another RL router is not sufficient novelty.

## Questions the research must resolve

### Objective and unit of analysis

Define the episode, target event, inspection decision, final review decision, and timeline. Keep policy violation, review-worthiness, observed evidence, and hidden intent distinct. Decide whether B evaluates a frozen monitor, learns an inspection policy, changes the downstream judge, or studies continual discovery; those are not interchangeable.

Define the estimand precisely: errors per episode, false-negative rate conditional on positives, precision of alerts, discovered positive count, family-discovery delay, or reviewer utility. These have different denominators and data requirements. Use the actual constructed prevalence as an experimental condition, never an estimate of real misuse prevalence.

### What makes inspection scarce?

Our research compute is plentiful. Any deployment constraint must be independently motivated: human attention, elapsed response time, throughput, bounded context, costly authorized observations, or an explicitly studied resource frontier. Vary that constraint and include high-inspection reference conditions. Do not manufacture an impoverished baseline merely to make routing useful.

Distinguish a resource cost from information availability. A record that does not exist cannot be purchased by spending more tokens. A retrospective monitor that retrieves more records is not necessarily an intervention that prevents an action.

### Information and actions

What can the cheap stage see? What does each inspection reveal? Is the extra information a genuine missing observation, a new interpretation of the same text, or an independent label? What is logged about selection probabilities? Can the inspection alter the final judgment or only label it for evaluation?

Do not assume that an expensive judge is an oracle or that more context monotonically improves it. Explicitly model correlated errors between routers, summaries, judges, and renderers.

### Statistical and adversarial claims

Separate i.i.d. episodes, structured shifts, sequential adaptation, and adaptive adversaries. State the assumptions for unbiasedness, interval coverage, consistency, regret, or robustness before proposing a theorem. Nonzero audit probability supplies a chance of inspection, not a guarantee of detecting every rare event.

Distinguish sampling an episode from sampling an action inside it. If auditing changes the operational decision, report the pre-audit and post-audit estimands separately. Human or model adjudication may itself be noisy. Consider positivity, delayed labels, adaptive stopping, repeated users/task families, extreme importance weights, and effective sample size. Do not import a theorem for fixed i.i.d. sampling into an adaptive stream without justification.

An offline replay that reveals every counterfactual inspection to the evaluator can support training and benchmarking, but the policy must receive only its selected observations. Address the difference between a fixed replay corpus and a live adaptive environment.

## Literature neighborhoods to cover

Go beyond LLM routing. Review value of information and active feature acquisition; sequential diagnosis and metareasoning; active search versus active learning versus active testing; prediction-powered/active statistical inference and survey sampling; selective labels, logged-policy evaluation, and contextual bandits; security alert triage and rare-event evaluation; AI-control protocol optimization and adaptive monitor testing.

For each neighborhood, explain the different objective and what assumption prevents simply applying its existing solution. Historical foundations are as important as recent model papers. Avoid importing named techniques merely because they sound adjacent.

## Literature-review requirements

Conduct a thorough, current review from primary papers, official proceedings, and author-maintained artifacts. Organize it by concepts, competing formulations, and unresolved assumptions, not as an undifferentiated paper list. Read the closest papers in enough depth to assess their methods, label provenance, splits, assumptions, and limitations; abstracts alone cannot establish a novelty gap.

Start with the seed references below, then search backward and forward and look for contrary evidence and very close recent work. Record the search date, query families, and remaining coverage gaps. Verify title, authors, year, current version, and publication status. Check code, weights, data, and licenses separately; a link does not establish reproducibility or permission to reuse. Mark inaccessible or unverified claims rather than inventing details. Distinguish independent evidence from author-reported results.

For each of the closest approximately five to eight works, produce a comparison with: problem/estimand; observation and action model; method; supervision/oracle; data and split; assumptions; result actually established; limitation; usable artifact; and exact overlap with our proposed claim. The number is a depth guide, not a ceiling or reason to omit relevant work.

Use explicit evidence labels: **user constraint**, **established evidence**, **author-reported empirical result**, **assistant inference**, **proposed hypothesis**, and **unresolved**. A new combination of existing components is not automatically novel. State which component is borrowed, what changes, why that change matters, and the experiment that could disprove its value.

For every proposed question, supply the required research card: question; nearest prior work; exact proposed difference; dataset and label provenance; method; strongest simple baseline; experiment; resource/access assumptions; failure/stop criterion and meaning of a negative result; reusable ASTRAL deliverable. Include a conservative claim that the evidence would license and a stronger claim it would not license.

The first response must contain the substantive review and candidate plan, not merely promise later work or ask routine clarifying questions. Use reasonable assumptions, label them, and list unresolved decisions. Do not treat the handoff as an approved architecture that must be defended.

## Experimental requirements and strongest baselines

The core must be executable without partners. Candidate tasks are fictional approval, access-control, resource-allocation, and dummy-artifact workflows with independently checked outcomes. Public agent environments may contribute diversity, but audit their labels and observation boundaries before reuse. A generated actor's intent is not an outcome label.

Use both a transparent controlled layer and independently constructed external tasks. Keep environment truth outside monitor inputs. Validate natural-language renderings separately; hold out task families, generators/renderers, time periods or streams where appropriate, and model lineages. Construct label prevalence deliberately and report results conditional on it.

Baselines should include the current gating architecture where applicable, strong risk-ranked and uncertainty/disagreement allocation, uniform audits, robust active-sampling methods, a contextual router, and a learned or oracle-information inspection reference where meaningful. Label oracle-information controls as unattainable diagnostics. A full-context model is a reference, not truth.

For the main B comparison, freeze downstream judge checkpoints and policy versions. Repeat key comparisons across several fixed judges to assess generality; do not make B depend on C training a new one. Charge all routing, embedding, summaries, rereads, retries, model calls, and audits to operational budgets. Account for research training cost separately rather than pretending it is zero.

Report the detection/resource frontier, unnecessary review burden, blind-spot discovery where defined, uncertainty and coverage of error estimates, and failure modes. Use paired or clustered uncertainty estimates matched to the actual experimental units. Specify the primary outcome before extensive tuning. Keep deployment-validity limits separate from benchmark results.

## Requirements to enumerate in the proposal

Produce a dependency table covering environments and licenses; episode and trace schema; oracle implementation and independent tests; model/checkpoint access; logging of action probabilities and timestamps; storage and caching; training/inference infrastructure; independent adjudication; statistical expertise; bounded sandbox evaluation; and reproducibility. For each dependency provide a partner-independent route, evidence of availability, owner role, and fallback.

Provide a ten-week checkpoint plan and longer extensions separately. No work package may require live private logs or a provider installation. Commissioned expert work is allowed but should not be presumed secured. The goal of a decisive pilot is to test the scientific premise quickly, not to impose an artificial tiny final study.

## What the first substantive response should deliver

1. A conceptual map and verified nearest-prior-work comparison, including an explicit assessment of the earlier formulation's weaknesses.
2. Two or three narrow candidate questions, each with the complete research card specified above; one recommended lead and reasons the others might be weaker.
3. A formal problem statement with observations, actions, timeline, objective, cost model, assumptions, and threat-model transfer to ASTRAL.
4. The strongest simple baseline and a minimal decisive pilot, followed by a resource-unconstrained main experiment and necessary ablations. Give an executable experiment specification, not only “evaluate robustness.”
5. A requirements/dependency plan, ten-week checkpoint, longer extensions, uncertainty analysis, and stop/pivot criteria.
6. A publication argument: the claim, closest paper that could defeat it, proposed scientific difference, result that would change the conclusion, and claims the study cannot support.
7. A compact branch-status export using the shared protocol, explicitly separating recommendations from user decisions.

## Failure and scope discipline

A proposed method is not justified if risk ranking plus random or robust auditing matches it under the important conditions, if its benefits depend on inaccessible oracle observations, or if it cannot support its advertised error estimates. A theoretically interesting result needs appropriate assumptions and nontrivial applicability; an empirical result needs stronger evidence than a single curated shift.

A negative result is valuable only if it is reliable, consequential, and clearly characterized—not automatically publishable. If the literature already resolves a formulation, say so and move to the next defensible question within B. Do not quietly pivot into C or into a universal safety platform.

**Reusable ASTRAL deliverable:** a pluggable inspection controller, stage-level trace records, reproducible auditing/evaluation, and a local report. This is preparation for future evaluation, not production deployment or a safety certificate.

## Primary-source seed references — discovery starting points, not a completed review

Primary-source identity and broad topic were checked on **21 October 2026**. This handoff does not certify all methods, numerical claims, theorems, latest versions, code availability, or licenses. The branch must perform the full review. Relevance notes are research leads, not findings that our proposed gap exists.

### B1. Zhang et al., Efficient Contextual LLM Cascades through Budget-Constrained Policy Learning (2024)

Source: [https://arxiv.org/abs/2404.13082](https://arxiv.org/abs/2404.13082)

Why read it: A contextual model-and-prompt routing predecessor. Read the state, actions, objective, and budget treatment before claiming routing novelty.

### B2. Kossen et al., Active Testing: Sample-Efficient Model Evaluation (ICML 2021)

Source: [https://proceedings.mlr.press/v139/kossen21a.html](https://proceedings.mlr.press/v139/kossen21a.html)

Why read it: Selective acquisition for evaluating a model, including selection-bias correction. Distinguish evaluation from finding positives.

### B3. Zrnic and Candes, Active Statistical Inference (ICML 2024)

Source: [https://proceedings.mlr.press/v235/zrnic24a.html](https://proceedings.mlr.press/v235/zrnic24a.html)

Why read it: Model-assisted data collection for statistical inference. Read the actual assumptions before transferring confidence guarantees.

### B4. Li et al., Robust Sampling for Active Statistical Inference (2025)

Source: [https://arxiv.org/abs/2511.08991](https://arxiv.org/abs/2511.08991)

Why read it: Robust interpolation of active and uniform sampling when uncertainty scores are unreliable. Do not repeat an abstract-level guarantee without its theorem conditions.

### B5. Jiang et al., Efficient Nonmyopic Active Search (ICML 2017)

Source: [https://proceedings.mlr.press/v70/jiang17d.html](https://proceedings.mlr.press/v70/jiang17d.html)

Why read it: Finding as many members of a target class as possible; an essential conceptual distinction from estimating a risk.

### B6. Griffin et al., Games for AI Control: Models of Safety Evaluations of AI Deployment Protocols (2024; check subsequent revisions)

Source: [https://arxiv.org/abs/2409.07985](https://arxiv.org/abs/2409.07985)

Why read it: Partially observable adversarial protocol design with limited human assistance. A game formulation by itself is not a new contribution.

### B7. Constitutional Classifiers++: Efficient Production-Grade Defenses against Universal Jailbreaks (2026)

Source: [https://arxiv.org/abs/2601.04603](https://arxiv.org/abs/2601.04603)

Why read it: A close safety-cascade precedent. Separate transcript-accessible components from internal-model observations.

### B8. Terekhov et al., Adaptive Attacks on Trusted Monitors Subvert AI Control Protocols (2025; revised 2026)

Source: [https://arxiv.org/abs/2510.09462](https://arxiv.org/abs/2510.09462)

Why read it: Motivates including monitor security and adaptive evaluation. Examine tested conditions; do not generalize to a universal attack or defense guarantee.

### S1. Debenedetti et al., AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents (2024)

Source: [https://arxiv.org/abs/2406.13352](https://arxiv.org/abs/2406.13352)

Why read it: Candidate public environment. Audit task predicates, licenses, oracle access, and safe subset before reuse.

### S2. Kutasov et al., SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents (2025)

Source: [https://arxiv.org/abs/2506.15740](https://arxiv.org/abs/2506.15740)

Why read it: Candidate monitoring environment. Separate assigned adversarial objective, actual outcome, and evidence visible to a monitor.