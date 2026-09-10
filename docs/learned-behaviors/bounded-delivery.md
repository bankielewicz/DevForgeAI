# Learned behavior: keeping delivery bounded

This is current DevForgeAI working guidance, learned from the September 2026 skill-builder / skill-validator modernization. It applies to specification, implementation, review, validation and handoff work across providers. It describes observable work patterns, not a diagnosis of a model or a claim that every iteration is wasteful.

These instructions guide agent decisions. They do not implement a hook, grant authority, alter an accepted test oracle, or activate a validation policy. Existing contracts, ownership, execution restrictions and budgets continue to apply. Use the existing plan, decision record and final report; this guidance requires no new skill, workflow, ledger, gate or approval ceremony.

## What was observed

A request for usable skill authoring and validation expanded through runtime enforcement, evaluation allocation, authentication and transport prerequisites, validation-policy design, and further implementation proposals. Reviewed documents and deterministic code progressed, but operational adoption repeatedly remained a later step. The operator had to approve a succession of locally reasonable increments without a stable account of the entire remaining path.

The failure was not simply the number of iterations. The agent optimized each immediate next action without checking whether the whole dependency chain still fit the user's intended outcome, practical effort and capacity. Prepared handoffs and successful reviews became convenient stopping points while important delivery dependencies stayed unresolved.

The evidence supports a delivery-process lesson; it does not establish model-wide behavior, subscription affordability, or the current implementation state. Earlier [utility integration evidence](../skill-authoring/skill-utilities-integration-20260907T145039Z/final-status.json) retains its creation-time claims. Consult the actual task's latest accepted revision for later policy and implementation decisions; a historical report is not current authority.

## Establish a finish line that matches the request

State the intended user outcome and the evidence that will demonstrate it in the existing task plan. For a documentation request, the finish line can be reviewed, discoverable guidance. For an operational skill request, distinguish canonical changes, required evaluation, integration, installation and observed use. A reviewed candidate is an intermediate result when the user asked for operational delivery.

Keep the following concise and together:

- The smallest useful deliverable, explicit exclusions, and accepted requirements.
- Work needed all the way to that deliverable, including any known adoption or environment prerequisites.
- The owner and evidence needed for each actual blocker.
- Available generation/time limits and operator effort, including setup, review, integration and closeout; unknown consumption stays unknown.
- The stopping condition: demonstrated requested outcome, or a specific blocked/partial result with the remaining work stated.

A legitimate research or design task can finish with a bounded answer and explicit unknowns. Do not force implementation into a design-only request, or expand a small implementation into a generalized platform merely because the model can imagine future uses.

## Bind execution to a finite specification and delivery route

Before dependent execution, fill or reuse the following fields in the existing task plan. This is a compact delivery contract, not a separate planning phase or additional artifact. Scale it to the task: a few sentences can cover these fields for a small change; the table is a guide, not a required form. Reuse settled decisions and existing acceptance criteria; clarify only ambiguities that change the outcome, authority, required evidence or limits. Resolve routine implementation choices within the assigned scope.

| Field | Required content |
| --- | --- |
| Governing specification | Named specification and revision, applicable contracts, explicit accepted amendments, and precedence if sources conflict. Do not substitute a stale recap. |
| Start condition | Selected input/candidate identities, owner and write scope, and the prerequisites actually required for the next action. Native execution additionally needs its selected environment and bounded allocation; a previous closed allocation is not renewed. |
| Delivery route | Ordered milestones from current state to usable outcome. Each names the requirement it serves, owner, output and observable completion condition. Include required installation and observed use when requested. |
| Acceptance | Map every in-scope requirement to its existing acceptance criterion and required evidence. Distinguish checks already satisfied from missing evidence; reuse only compatible observations. |
| Exclusions and limits | Explicit non-goals and applicable time, attempt, review and repair limits. Preserve original accounting. Scope or budget changes require their existing authority; this table creates none. |
| Success stop | All in-scope acceptance criteria are satisfied and the requested deliverable is available to its user. Stop work; do not append polish, generalized infrastructure or stronger claims to the accepted endpoint. |
| Blocked or partial stop | Name the exact unsatisfied criterion, observed cause, preserved result, smallest viable remedy and the decision or external change required. A reached limit or exhausted authorized remedy ends dependent execution; it does not begin another allocation. |

A new task belongs on the active route only if it serves an accepted requirement or removes an observed blocker to one. Record that mapping and its effect on the remaining route in the existing plan. Put optional improvements outside the delivery path. If a proposed change revises the specification, obtain the required decision before dependent work; do not silently move the finish line. Equally, do not remove required checks or declare a smaller result complete without an accepted scope change.

When two successive attempts address the same blocker without new evidence or a changed condition, stop that remedy and report the concrete alternative instead of repeating it or enlarging the specification. A stricter existing attempt limit still applies; this rule grants no retries. Continue independent authorized work. If an accepted task genuinely requires broader investigation, bind that investigation to its own question, output and stop condition in the same plan.

These are operational instructions for agents and reviewers. Enforcement comes only from applicable existing implemented checks and authority boundaries; this guidance does not claim universal automatic phase interception.

## Recognize different patterns

A warning sign calls for judgment, not an automatic failure or a new gate.

| Observable pattern | When further work is justified | Prevention and recovery |
| --- | --- | --- |
| Specification expansion: each answer introduces another prerequisite, subsystem or specification. | A concrete accepted requirement cannot be met by the current design, supported by a failing example or identified dependency. | Show the path to the user outcome. Compare a direct implementation with reuse and deferral before adding infrastructure. Remove unneeded proposals from the active path. |
| Repeated planning and approval: the same decision is asked again, or the next step is always another proposal. | A material change in scope, risk, authority or budget actually requires a new decision. | Carry accepted decisions forward. Bundle the remaining decision into one concrete, reviewable request. Continue unaffected authorized work; do not ask the user to choose routine implementation details. |
| Recursive validation: reviewers need reviewers, or testing the validator expands into repeated inner campaigns. | An independent semantic judgment or distinct native observation is required to establish a named claim. | Bound review depth and repairs. Use deterministic checks for mechanical assertions and independent AI for meaning. Propose evidence-layer changes explicitly when an accepted contract requires more. |
| Combinatorial test expansion: variants, arms, contexts and continuations multiply faster than useful coverage. | Each independent observation distinguishes a relevant failure or comparison that cannot be shared. | Map assertions to evidence before allocation. Reuse compatible observations only when their conditions and independence permit it. Retain each assertion and its outcome; never drop required cases to fit a cap. |
| Setup dominates: sign-ins, workspaces, transport and custody consume more effort than the useful workload. | The boundary is necessary and a simpler supported method cannot establish it. | Measure active operator work separately from waiting. Investigate authentication lifecycle separately from history isolation. Start a cost sample with an executable workload; do not make it depend on an unrelated infrastructure project. |
| Budget substitution: a smaller call cap or shorter deadline is presented as proof of affordability. | A bound controls exposure while real usage is measured. | Distinguish generation counts, internal requests, tokens, wall time and human effort. Report missing measurements as unknown. A scheduling ceiling does not establish subscription consumption or likely completion. |
| Delivery deferred: clean worktrees, commits or handoffs accumulate while the requested installed behavior stays unavailable. | The user requested that intermediate artifact, or a documented prerequisite prevents adoption. | Track source, review, merge, installation and observed operation separately. Consolidate remaining adoption blockers and their total cost. Include integration in the completion path without merging or installing outside authority. |
| Perfection loop: reruns or rewrites seek an immaculate record after usable evidence already exists. | A new change, genuine failing acceptance condition, or material uncertainty needs correction or measurement. | Preserve deviations and failures. State which conclusions they invalidate. Repeat affected checks for a concrete reason; never rerun merely to erase history or improve presentation. |
| Stale continuation: a recap sends the agent back to a completed stage or discards an accepted decision. | Fresh evidence establishes drift or invalidates the earlier result. | Read the latest identified report and actual state. Preserve valid work, correct the next action, and avoid replaying completed phases because a summary is stale. |
| Parallelism without progress: many agents and worktrees add coordination and incompatible outputs. | Independent tasks have clear ownership, bounded outputs and an integration owner. | Delegate only useful independent work. Count delegated effort within its allocation, end redundant work, and combine reviewed bytes through the assigned owner. A new chat is not isolation. |
| Premature simplification: the agent calls required evidence “ceremony” and removes it to finish cheaply. | A requirement is explicitly revised by its owner after considering the claim and consequences. | Keep necessary checks and honest unknowns. Separate optional process from accepted obligations. Propose a smaller scope or amended specification; never weaken a governing gate to pass. |
| Administrative expansion: acceptance records, review chains and bookkeeping conventions grow while the usable installed result stays blocked. | A real check for an accepted requirement at an actual transition is missing, or an observed defect needs a regression. | Simplify the accepted path and keep the real checks. Do not encode every administrative convention as another gate; gates protect correctness or authority properties, not narrative order or bookkeeping placement. |

## Justify an additional iteration

Before adding a dependency, elaborate artifact, review round or funding request, answer these points in a short paragraph in the existing plan:

1. Which user outcome or accepted requirement needs it, and what observed failure or bounded uncertainty is being addressed?
2. What happens if it is omitted, and why is the simpler supported alternative insufficient?
3. What concrete result will close this issue, who owns it, and what are the stopping conditions?
4. What does it add to total remaining model, operator and elapsed effort, including downstream integration and adoption? Name unknowns rather than inventing estimates.
5. Is it already authorized? If not, make the smallest material decision reviewable before asking.

“Best practice,” “full fidelity,” “enterprise ready,” and hypothetical future reuse are not sufficient explanations on their own. Tie them to an actual requirement and evidence. Conversely, a verified defect, a necessary safety boundary, or an explicit new user objective can justify substantial additional work.

Example: a malformed input bypasses a required state transition. A focused regression, minimal fix and independent review of that boundary can be justified. An entirely new scheduling framework for the same fix needs a separate explanation of why the existing runtime cannot satisfy the requirement.

## Recover an over-expanded specification

When successive checkpoints mainly produce more prerequisites, when the delivery endpoint keeps moving, or when the user says the process feels endless:

1. Acknowledge the observable pattern and the agent's contribution. Stop creating optional expansions and end redundant delegated work that this session owns. Continue useful work already within the bounded assignment; honor any explicit hold immediately.
2. Reconstruct the accepted user outcome, valid completed evidence and remaining blockers from the current files and decisions. Do not make the user restate information already available.
3. Put remaining work into three groups in the existing plan: necessary for the accepted outcome; a new requirement needing an explicit decision; optional enhancement that can be deferred. Removing an optional proposal from the active path does not remove an accepted obligation.
4. Replace successive local proposals with one consolidated completion path: smallest useful increment, actual adoption prerequisites, owners, evidence, total allowance and stopping conditions. If the path is infeasible, say so and present concrete scope/requirement alternatives.
5. For an over-ambitious model output, narrow its assignment to the selected artifact or behavior, fixed interfaces, explicit exclusions, observed checks and remaining allowance. Reject unrelated abstractions during review. Do not address scope creep by asking the model for an even larger specification.
6. Use a targeted change to the accepted specification when scope or evidence requirements must change. Preserve earlier versions, decisions and outcomes. The right owner accepts consequential revisions; this lesson is not a waiver.
7. Close against the requested outcome. Report what is usable, what remains unavailable, and the exact reason. Exhausting a tranche or preparing a handoff does not automatically authorize another tranche.

A concise steering instruction can be enough:

> Work toward the agreed outcome using the existing components. List only blockers that prevent it, with their evidence and smallest remedy. Defer optional generalization. Carry forward settled decisions and valid results. Continue authorized work within the remaining allowance; request one concrete scope or funding decision only when genuinely required. Finish with the actual delivery state and unresolved blockers.

## Apply the lesson in DevForgeAI

Skills carry the semantic work: selecting relevant context, making bounded proposals, explaining tradeoffs and producing useful results. The protected runtime owns mechanical transitions, budgets, checks and receipts. Moving enforcement into code does not require the model to repeatedly narrate every mechanical step. The [phases, hooks and skill content](../development-language-policy.md#phases-hooks-and-skill-content) section of the language policy defines the split: Rust owns phase state, transitions and hook-invoked checks; the skill owns the reasoning and authoring within a phase; ceremonial enforcement in skills is prohibited. Observed during the September 2026 expert-foundation work: administrative records and review chains kept expanding while usable local delivery remained blocked. The remedy is to simplify the accepted path and keep the real checks, not to encode every administrative convention as another gate.

Where an accepted and implemented validation policy supports it, use change-focused routine evidence for bounded updates and full qualification for its specified triggers. Do not assume a proposed policy is active or bootstrap a new enforcement contract into accepting itself. A generic validation request or version string is a reason to examine intent and impact, not by itself evidence that every historical experiment must run.

Keep one framework lesson and concise entry-point guidance. Do not copy this entire note into every skill or create another mandatory review workflow to enforce simplicity. Future lessons should name the observed pattern, evidence limits, prevention, legitimate exceptions and a practical remedy; link existing evidence rather than adding duplicate ledgers.
