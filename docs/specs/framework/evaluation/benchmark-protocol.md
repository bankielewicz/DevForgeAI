---
id: DFF-EVAL-01
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
---

# Comparative benchmark protocol

## Purpose, ownership, and current status

This document defines the proposed evaluation alongside [MVP scope](../mvp/scope.md) and [MVP acceptance](../mvp/acceptance.md). The [framework index](../index.md) owns the documentation map. This protocol owns comparison fairness, evidence accounting, and limits on comparative claims. It contains no benchmark executions, scores, qualified runner, selected competitor cohort, or claim that DevForgeAI is best.

The intended claim is bounded: performance on a named workload, versions, hosts, and resource allowance. A finite benchmark cannot establish universal superiority. [Foundation](../foundation.md) requires supported Codex with individual ChatGPT Pro; evaluation cannot silently substitute paid API access, Enterprise features, extracted credentials, or undocumented automation.

## Comparison conditions and attribution

Register conditions before the ranking campaign:

| Condition | Configuration |
| --- | --- |
| Baseline | Codex with the selected task and applicable repository instructions, without framework additions |
| Guidance | Baseline plus the framework's selected skills and grounded project context, without its protected runtime or additional orchestration |
| Complete | The implemented MVP, including its qualified authority and selected orchestration |
| Compatible comparator | An actually available external framework using its documented supported configuration on the declared host |

Run two distinct tracks. **Controlled attribution** holds Codex version, model, effort, accessible project tools, initial inputs, host, permissions, and aggregate resource ceiling constant. Framework resources and mechanisms are the declared treatment. **Configured-product comparison** permits each system's declared recommended model/effort/orchestration within the same aggregate ceiling. Report these tracks separately; a stronger model's advantage cannot be attributed entirely to framework design.

Assess shared observable outcomes rather than demanding DevForgeAI-specific document names or private receipts from comparators. Test DevForgeAI's protected receipt contract separately as MVP acceptance. Unavailable or unsupported comparator configurations remain untested; descriptions do not earn scores. Do not select a deliberately weak baseline or repair one condition manually without recording assistance.

## Workload, snapshots, and independent evidence

Select a compact cohort covering a complete feature, a defect missed by existing tests, a shared-contract change, necessary requirement clarification, and a valid no-change outcome. Include adversarial scenarios for premature completion, stale evidence, altered oracles, scope-expanding input, interrupted/resumed work, unavailable prerequisites, and a verification follow-up that leaves the original repair active. Test recovery and adaptation with changed conventions and unfamiliar projects, not only the motivating incident.

Freeze each task's initial project snapshot, user-visible requirements, permitted effects, policy, dependencies, platform obligations, and case identity. Every paired run starts from the same identified baseline in isolated owned state. Preserve candidate snapshots and actual executions. Published artifacts must exclude credentials and private account data.

Keep development, pilot, and held-out ranking material distinct. Independent evaluators retain expected outcomes and hidden cases outside worker write access. Use the same declared feedback policy for every condition. Tuning against revealed ranking failures retires those cases from held-out use; retain their history and qualify later changes against fresh material.

Independent acceptance checks inspect delivered behavior and artifacts. Semantic judgments use a preregistered rubric and attributed review; a model judge cannot be the sole completion or integrity oracle. Compiled Rust owns DevForgeAI's authoritative validation and acceptance. Python collectors or graders produce observations only. Neither the evaluated agent's summary nor its editable manifest validates itself. The benchmark runner and any protected decision path require separate qualification; this document does not supply them.

## Execution, resources, and interventions

Register aggregate elapsed-time and usage limits, permitted concurrency, retry rules, and repetitions before execution. Repeated trials restart from baseline; continuations and child workers share the run's allowance. No best-of-attempt selection: report each assigned replicate and preserve retries. Counterbalance condition order to reduce host-load and subscription-quota effects. Do not run competing trials concurrently unless isolation and resource accounting justify it.

Combine coordinator and worker usage. Record observed tokens where available, elapsed time, tool executions, interruptions, and setup time. Missing usage is `NOT_MEASURED`, never zero. Report Pro limits as observed constraints; do not invent dollar costs, token estimates, or API-equivalent prices. An API experiment is a different track requiring its own authorization.

Record every human intervention, its reason, content or protected reference, duration, and effect on scope. Distinguish necessary clarification from rescue instructions or manual code repair. Report autonomous and assisted results separately. Safety scenarios can reward honoring interruption while task completion remains unfinished.

## Scoreboard and denominator rules

Publish raw counts, denominators, per-task/platform results, and uncertainty for repeated observations:

| Dimension | Required observations |
| --- | --- |
| Outcomes | Independently resolved assigned cases, unmet requirements, regressions, usable deliverables |
| Integrity | Unauthorized effects, evidence/oracle changes, stale-result acceptance, truthful completion claims |
| Recovery | Correct interruption handling, preserved state/evidence, successful bounded resumption |
| Adaptation | Results on changed conventions and unfamiliar projects; customization effort |
| Efficiency | Elapsed time, measured aggregate usage, tool calls, repeated ineffective work, setup overhead |
| Interventions | Clarification and rescue counts, human time, autonomous versus assisted completion |

For each condition, resolved rate is `100 * independently resolved assigned cases / all eligible assigned cases`, with each case/replicate counted once. Failed, timed-out, budget-exhausted, blocked, and unexecuted eligible assignments remain nonpasses. Report planned and actually executed counts. Subscription interruptions retain a distinct reason and remain nonpasses; they are not silently reclassified as product defects.

A demonstrated harness defect can invalidate the affected paired comparison under the preregistered adjudication rule. Preserve the defect and attempts, report invalidated counts, and apply the same exclusion/recovery to all affected conditions. A product setup failure is not automatically a harness defect. Do not retrospectively remove difficult cases or change the denominator after seeing which system failed.

Report efficiency across all attempts and separately for successful runs; hiding expensive failures distorts cost-to-outcome. Mandatory safety/integrity failures cannot be compensated by speed or an average score. Any headline ranking requires a preregistered eligibility rule and decision margin; until resolved, show the component scoreboard without declaring a winner.

DevForgeAI's own development coverage and pass-rate floors remain governed by [quality and delivery](../quality-and-delivery.md). They are independent engineering obligations, not a benchmark score, a universal managed-project threshold, or evidence of superiority over another framework.

## Pilot, references, and unresolved decisions

The pilot validates fixture independence, paired initialization, grading, cancellation, failure classification, and measurement feasibility. It can expose MVP gaps but cannot support a leaderboard claim. Its minimum contract names one bounded task and initial snapshot, independent expected outcomes, permitted effects, selected execution interface/support category, an enforceable elapsed-time/resource bound, cancellation/cleanup behavior and retained evidence. Missing usage telemetry may be a pilot observation rather than a prerequisite; do not promise token limits that the selected interface cannot enforce. A pilot that develops or tests the runner reports observations, not qualified acceptance.

The full comparator cohort, final repetition count, uncertainty method and winning margin are not prerequisites for that bounded pilot. Ranking begins only after those campaign decisions and runner qualification are complete. The pilot cannot be repackaged as a ranking by choosing favorable weights after its results are known.

[SWE-bench](https://www.swebench.com/) provides a comparison reference using percent resolved and a common mini-SWE-agent setting. [Spec Kit](https://github.github.com/spec-kit/) and [BMAD](https://docs.bmad-method.org/) are comparator-discovery references for workflow extensibility and customization. Their documentation does not establish compatibility with this campaign or comparative effectiveness; inspect exact selected versions before inclusion.

- **EVAL-Q1:** Which projects, task families, required hosts, comparator versions, and development/pilot/held-out partition form the cohort?
- **EVAL-Q2:** Which runner, isolated execution boundary, independent oracles, and Rust validation path are qualified under Codex/Pro constraints?
- **EVAL-Q3:** Which budgets, concurrency limits, feedback/retry rules, and worker-usage measurements are supported?
- **EVAL-Q4:** How many paired repetitions and what order/randomization and uncertainty method support the intended claim?
- **EVAL-Q5:** Which safety eligibility rule, decision margin, and intervention policy define a meaningful improvement?
- **EVAL-Q6:** Who adjudicates harness invalidation, semantic disputes, and held-out access, and how are decisions preserved?

Next, bind one pilot task to the relevant MVP acceptance cases and finalize only its minimum contract before implementing its runner or executing its authorized trial. Resolve EVAL-Q1..Q6 in full before the later frozen comparison campaign. This planning document itself authorizes no trial or installation.
