---
format_version: prd-review-v1
review_id: "<safe-unique-review-id>"
created_at_utc: "<actual-RFC3339-UTC-time-ending-Z>"
assessment: INCOMPLETE
assessment_complete: false
supersedes: null
---

# PRD review: <selected topic>

## Scope and context

<Actual request, project, candidate PRD ID/revision/path/SHA256, full or focused
scope, default work-planning or explicitly selected next use, exclusions,
reviewer/author context and independence limits.>

## Evidence inventory

| Source ID | Role | Path or provenance | SHA256 or non-file provenance | Supporting locators | Availability and significance |
| --- | --- | --- | --- | --- | --- |
| <source> | <candidate/governing/design/observation/prior evidence> | <relative local or resolved external path; actual conversation or URL/access date> | <paired raw-byte digest or actual decision provenance> | <section/paragraph/line> | <inspected or missing; essential/optional consequence> |

## Review matrix

| Original obligation/source locator | PRD requirement/locator | Acceptance criterion/locator | Status | Observation/finding |
| --- | --- | --- | --- | --- |
| <selected clause> | <ID or review-local locator> | <ID or locator> | <SATISFIED/FINDING/NOT_ASSESSED/NOT_APPLICABLE> | <support or explicit reason> |

<Actual distinct obligation counts, applicable review areas, reverse-mapping
observations, shared dependencies and explicit unreviewed/excluded scope.
Counts do not establish semantic completeness.>

## Findings and questions

<Explicitly state no findings when applicable. Otherwise repeat this complete
record for each distinct defect; remove unused prompts.>

### PRF-001: <concise title>

- Category: <supported category>
- Evidence: <source identity/locator; affected requirement/acceptance IDs>
- Expected obligation: <source-grounded condition>
- Observation: <contradiction or missing information>
- Consequence: <effect on scope and next use>
- Correction or decision request: <concrete bounded next action>
- Owner: <actual owner or unknown>
- Classification and blocking activity: <BLOCKING/NONBLOCKING; reason and stage>
- Resolution condition: <independently observable satisfaction>
- Nonblocking rationale, when applicable: <why current use proceeds; later operation waiting>

<Actual decisions, provenance, affected IDs and unanswered questions with owners.
Keep unsupported preferences as labeled suggestions.>

## Architecture and dependency disposition

<Confirmed boundaries, state/trust/interface owners, conflicts, supported
feasibility and limitations, planning-safe deferrals and activities they block,
contract versus implementation versus qualified-evidence prerequisites,
shared writable resources and remaining integration obligations.>

## Assessment and limitations

<Exact scoped assessment and completeness rationale, supported blockers,
missing required areas/essential sources/independence, nonblocking and later-stage
obligations, input stability observations and unperformed product verification.
Delivery readback is reported externally after it occurs.>

## Retest and continuity

<Initial review, or retained prior report path/SHA256 and selected finding IDs.
Retain old/new input identities and semantic impact of changes.>

| Prior report identity + finding ID | Original resolution condition | Current evidence and impact/regression inspection | Disposition | Reason and authority |
| --- | --- | --- | --- | --- |
| <selected finding> | <original condition> | <bound revised content and affected scope> | <VERIFIED_FIXED/STILL_PRESENT/NOT_VERIFIED/SUPERSEDED> | <independent evidence or explicit authorized supersession> |

<For initial review replace unused retest rows with "Initial review; no prior
findings selected." For retest retain untargeted findings' last status with current
applicability unassessed, failed/stale attempts and still-unreviewed scope.>

## Manual handoff

<Concrete manual revision/decision, missing-prerequisite or scoped work-planning
request. Include exact candidate/governing identities, findings and resolution
conditions, responsible owner, later prerequisites and integration obligations.
State delivery limitations. Do not invoke another workflow or include this report's
own whole-file hash; return the final read-back digest externally.>
