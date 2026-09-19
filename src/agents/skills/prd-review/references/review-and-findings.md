# Review dimensions and findings

Load for substantive review of selected obligations. These are document reasoning
activities; counterexamples and proposed verification are not executed tests.

## Inventory and trace the obligations

Inventory selected original clauses/outcomes, PRD requirements, acceptance
criteria and applicable shared constraints. Construct a bidirectional matrix:

| Original obligation/source locator | PRD requirement/locator | Acceptance criterion/locator | Status | Observation/finding |
| --- | --- | --- | --- | --- |

Use SATISFIED, FINDING, NOT_ASSESSED or reasoned NOT_APPLICABLE for every selected
obligation. Count each once; state actual counts and unreviewed/excluded scope.
Reverse-check PRD requirements and criteria for unsupported additions, orphan
acceptance, duplicate/competing owners and exclusions lacking scope authority.
Record these unmatched items as findings even when no original row exists.
A populated matrix or percentage does not prove substantive coverage.

A focused feature assessment includes its relevant shared constraints and
dependencies. It does not become a whole-PRD assessment because its own rows pass.

## Functional behavior and acceptance

Inspect actors, triggers, preconditions, observable outcomes/effects, state
transitions, boundaries and recovery. Reason through relevant denied/invalid
requests, conflicting states, cancellation, retry/idempotency, partial failures
and races. Identify the missing rule and its consequences without choosing a
business decision for its owner.

For example, allowing cancellation before dispatch and denying it afterward does
not determine a concurrent cancellation/dispatch race. Ask which observable
transition wins and which shared state owner guarantees it; do not invent the rule.

Criteria must distinguish compliant from noncompliant behavior and preserve
original business obligations. Challenge circular wording such as "works as
designed," lowered expectations and implementation-shaped oracles that avoid the
requirement. Preserve meaningful negative-path and cross-boundary observations.

## Quality and verification feasibility

Assess applicable performance/capacity, reliability/recovery, security/privacy,
accessibility, observability, compatibility and operations. Each supplied target
needs units, conditions/workload, observation method and decision provenance.
Challenge unsupported certification, availability, platform and cost assertions.
Missing essential targets are attributed findings/questions, not invented numbers.

Determine whether proposed verification can observe the obligation on the required
host and across components. Inspected reports, screenshots and prototype outputs
support only their identified scope and conditions. Do not rerun product tests or
claim measured coverage, rendered behavior, end-to-end success or production readiness.

## Architecture and dependency sufficiency

Review relevant state ownership, trust boundaries, component responsibilities,
stack constraints, persistence/transaction boundaries, deployment assumptions and
failure/recovery design against the selected requirements. Inspect relevant
canonical contracts; do not generate a mandatory constitution pack or rewrite
governing architecture.

Identify unsupported dependency/hosting assumptions, incompatible schema/API
contracts, duplicate state owners, migration gaps and cycles blocking next use.
Separate dependency on a contract decision, delivered implementation and qualified
evidence. Record what inspected evidence supports about feasibility and what
requires an experiment or expert decision; proposing an experiment does not run it.

Present concrete alternatives and tradeoffs where useful while retaining material
decision ownership. Record an explicitly selected decision's provenance and
whether the PRD still requires revision. A deferred implementation choice may be
nonblocking for work planning only when outcome boundaries and dependencies can
be planned safely. Name the later activity it blocks. Missing essential product
semantics or a shared contract required to define planning boundaries is blocking;
do not rename it an implementation detail to obtain PASS.

For UI products, assess applicable journeys, permissions, loading/empty/error
states, accessibility and observable frontend-to-backend effects. For headless
products, assess actual CLI/API/service/consumer interactions and state why UI
topics do not apply. Do not fabricate UI requirements.

Identify shared writable contracts/resources and cross-component acceptance.
Separate files or worktrees do not prove safe parallel execution. Preserve
remaining integration prerequisites; do not decompose stories, create worktrees
or assign a sprint.

## Actionable finding record

Use stable report-local IDs, default PRF-001 onward. Each finding contains:

- Concise title and category.
- Supporting source identity and precise locator; affected requirement/criterion IDs.
- Expected governing obligation and observed contradiction or missing information.
- Consequence for the declared scope and next use.
- Concrete correction or decision request.
- Owner, or explicitly unknown owner.
- BLOCKING or NONBLOCKING classification, blocking stage/activity and rationale.
- Independently observable resolution condition for later retest.

BLOCKING means the issue prevents the selected next use. NONBLOCKING must explain
why current use can proceed and identify any later operation still waiting.
Do not derive these decisions from a cosmetic severity score. A preference without
a governing basis is a labeled suggestion, not a mandatory defect.

Merge observations of one defect while retaining every affected location; retain
distinct defects separately. Do not leave the author guessing the missing rule or
what evidence could establish resolution. Questions preserve actual decisions,
their owners and unanswered parts. State explicitly when there are no findings.
