---
format_version: product-requirements-v1
prd_id: "<safe-topic-UTC-identifier>"
revision: 1
updated_at_utc: "<actual-RFC3339-UTC-time-ending-Z>"
disposition: NEEDS_INPUT
supersedes: null
---

# <Selected product or feature> requirements

<!-- New default-format PRDs only. Follow references/artifact-and-revision.md.
Replace placeholders and these comments; do not leave empty example rows.
Preserve valid existing conventions instead of copying this header into them.
Use only needed stable IDs. Explain meaningful non-applicability. -->

## Document context and sources

<!-- Selected request, scope, project and artifact identity, applicable policy,
permitted effects. Inventory inspected sources with SRC IDs, paths/URLs, locators,
raw-byte SHA256 for local files or access dates for external research. Attribute
conversation decisions directly. Distinguish unavailable sources and limitations. -->

## Problem, actors and outcomes

<!-- Current problem/behavior; users/consumers; OUT IDs, observable outcomes and
source/decision basis. Do not invent demand, targets or stakeholder approval. -->

## Scope and exclusions

<!-- Selected release/MVP functionality and grounded priorities, explicit excluded
work, separately proposed future ideas. Record any authorized objective change. -->

## Scenarios and interactions

<!-- Actor journeys/operations and supported success, denied/invalid, boundary,
error/recovery and cross-component behavior. UI states/accessibility where
selected; otherwise explain UI non-applicability and actual CLI/API interactions. -->

## Functional requirements

<!-- Each REQ: stable ID, source clause/decision, OUT link, actor/trigger,
preconditions, observable behavior, data/effects, dependencies and AC links or
named Q blocker. Include relevant concurrency/retry/idempotency rules only when
supported; missing product semantics remain explicit questions. -->

## Quality and operational requirements

<!-- Applicable performance, reliability, security/privacy, accessibility,
observability, compatibility and operational requirements with stable IDs and
acceptance links. Targets need units, workload/conditions, observation method and
source. Identify essential missing thresholds, actual project test policy and
policy compatibility gaps; explain non-applicability where appropriate. -->

## Data, interfaces and dependencies

<!-- Entities, state transitions and owners, access boundaries, canonical
contracts and producer/consumer obligations. Distinguish required decisions,
interfaces, qualified artifacts and evidence from proposed future availability.
Retain integrated acceptance across components. -->

## Architecture and decisions

<!-- Established canonical references and attributed DEC entries; distinguish
selected choices and proposals. Give alternatives/tradeoffs and blocking stage
for unresolved architecture. Experiments: inspected identities/conditions/results/
limitations versus proposed question/method/effects; contrary evidence proposes
an attributed revision, never silently changes a governing rule. -->

## Acceptance and traceability

<!-- Each AC gives conditions and observable expected result, plus REQ backlinks.
Map source clause/decision + OUT -> REQ -> AC/Q in both directions. Account for
all selected source obligations as mapped, excluded (scope reason), superseded
(decision source) or unresolved. Acceptance is planned, not executed evidence. -->

## Risks, assumptions and questions

<!-- Each material item: ID, evidence/basis, owner or explicit unknown owner,
affected REQs and stage/operation blocked. Distinguish product blockers from
architecture questions deliberately assigned to review/design. -->

## Review handoff

<!-- Current disposition and reasons; PRD ID/revision/actual path; input identities,
review focus and exact missing evidence/decisions. Fill a manual prd-review request
for this selected scope and governing sources/design references. No automatic
invocation or approval claim. Report final whole-file SHA256 outside this file. -->

## Revision and follow-up notes

<!-- CREATED/REVISED/UNCHANGED, retained predecessor and before-image references
when applicable; added/changed/superseded/retired IDs with origin and downstream
impact; changed/unavailable sources; separately proposed later improvements.
Independent findings remain with their reviewer; changed candidates need retest. -->
