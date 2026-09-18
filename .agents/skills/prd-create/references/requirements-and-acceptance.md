# Requirements, architecture and acceptance

## Outcomes and selected scope

State the problem, current behavior, actors/users/consumers, desired observable
outcomes and product/feature boundary. Separate selected release/MVP behavior,
exclusions and proposed later ideas. Preserve the user's objective until an
explicit change identifies what it supersedes. Ground priorities and quantitative
claims in inspected sources or actual decisions. Scale the PRD to the selected
capability; a large input is not a request for a whole-product rewrite.

## Functional obligations and observable criteria

For every selected requirement record its stable ID, source basis, actor/trigger,
applicable preconditions, required behavior, data/effects, dependencies and linked
acceptance criteria. Describe conditions and externally observable results that
an independent reviewer or test author can challenge. Criteria are planned
oracles, never executed-test evidence.

Cover meaningful success, denied/invalid requests, boundary states, errors and
recovery. Address concurrency, retry, idempotency, cancellation and partial failure
where relevant to the behavior. Use supported domain rules; where a material rule
is missing, attach a named question rather than invent its semantics. Translate
vague fast/secure/user-friendly claims into supported observable obligations or
an explicit unresolved decision.

For example, supplied rules permitting cancellation before dispatch and denying
it afterward require both outcomes in acceptance. If their concurrent ordering is
undefined, record the exact question and affected requirement. Do not choose an
arbitrary race winner or suggest that two happy-path criteria cover the race.

## Quality and interaction

Identify applicable performance/capacity, reliability/recovery, security/privacy,
accessibility, observability, compatibility and operational constraints from the
selected evidence and product risk. A measurable target includes units,
conditions/workload, observation method and decision source. An essential missing
target is a named blocker; unrelated requirements remain draftable. Do not invent
latency, availability, retention, platforms or compliance certification. Explain
non-applicability where useful rather than filling every category with fiction.

Consume this project's actual development/testing policy. Do not import fixed
framework language, coverage percentages or mock rules. Preserve known policy
compatibility issues for their owner rather than silently resolving them here.

For selected UI behavior describe actor journeys, actions, feedback and applicable
loading, empty, error and permission states. Include selected accessibility and
frontend-to-backend/persistence acceptance implications. Reference existing designs
and name missing decisions. Text, Markdown and Mermaid sketches may live inline;
do not create a website or browser-only deliverable, or claim rendered/interactive
QA. For CLI/API/service/library work without a selected UI, state why UI is
inapplicable and specify actual consumer requests, outputs, errors and effects.

## Data, integration and architecture

Identify logical entities, state transitions, ownership, access/trust boundaries,
producer/consumer dependencies and observable interface obligations. Reference
canonical API, schema and security contracts; do not silently redefine them in
the PRD. State whether a dependency is a needed contract decision, delivered
interface, qualified artifact or evidence. A future implementation mentioned in
a document is not a delivered dependency. Missing shared contracts, guarantees,
migration decisions or availability become specific questions with affected work.
Keep acceptance across UI/API/persistence or other components intact instead of
prematurely splitting it into stories.

Reuse established stack, layout, state ownership, trust-boundary and deployment
decisions. Record new choices only when supplied, selected or within real
delegated routine scope. For material unresolved choices show alternatives,
tradeoffs, owner and the stage they block. Reference separate governing design
documents; authoring a PRD does not select edits to them or a mandatory architecture,
stack, source-tree, frontend/backend/database/hosting document pack.

Distinguish an unresolved technical choice assigned to review/design from missing
product semantics. Review can inspect explicit architecture questions and their
effects on dependent implementation. An undefined business rule remains an
authoring blocker even if someone labels it architecture.

For inspected prototype/research evidence retain identity, conditions,
observations and limitations. A proposed experiment states its question, method,
distinguishing observations and necessary effects; do not describe it as executed.
Do not code/run a prototype, install tools or invoke a workflow. A contrary result
supports a proposed attributed requirement/design revision and impact record,
not silent policy replacement or a product QA verdict.

## Traceability and consistency

For new artifacts use stable `OUT-001`, `REQ-001`, `AC-001`, `DEC-001`, `Q-001`
and `SRC-001` namespaces as needed, with at least three decimal digits. Preserve
valid existing namespaces/IDs; do not create unused rows merely to fill a template.
Do not recycle retired IDs for a different meaning.

Map in both directions: source clause/decision and outcome -> requirement ->
criterion, and each criterion -> the requirement(s) it verifies. Each selected
requirement links criteria or a named blocking question. Disposition every
selected source obligation: mapped, explicitly excluded with scope basis,
superseded with decision provenance, or unresolved. An input source inventory is
not a clause-level mapping. Preserve retired IDs and explanations in revision
history, with downstream impact for changes.

Before delivery, read the content for unsupported claims, contradictory rules,
unmapped obligations, missing negative behavior and disguised decisions. This is
authoring consistency review, not independent PRD review or executed assessment.
A populated table or calculated mapping percentage cannot establish semantic
completeness. The [artifact contract](artifact-and-revision.md) defines disposition
and final delivery details.
