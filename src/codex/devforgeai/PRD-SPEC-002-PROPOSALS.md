# Proposed clarifications for SPEC-002 — NOT APPROVED

These proposals are separate from the unchanged approved SPEC-002 v1. They are not
requirements, permission to edit that specification, or evidence that the Codex port
passes it. The port's approved-extension pre-write guard remains until an owner supplies
a concrete failure disposition. No decision is inferred from importing this package.

## Validation lifecycle and count (D-03, D-04)

Proposed owner decision: count one initial validation followed by at most three actual
repair-and-readback cycles. Record each check and repair. A missing external capability
may stop earlier with its error; a no-op rewrite does not count as a repair.

Proposed failure disposition: a new failed PRD stays `draft`; a changed extension of an
approved PRD stays `in-review`, with `approved_by` empty and `approved_on` null. Never
restore `approved` onto changed content after validation fails. Preserve existing item
bytes, version/change history and the unresolved errors. This changes ERR-06's previous-
status wording and therefore needs an explicit owner decision; it is not silently applied.

## Answered-none and partial quality answers (D-05)

Proposed clarification: distinguish a required category with no answer from one explicitly
answered `none` and one partially answered. Record explicit none in prose as the user's
answer, without inventing an NFR. Mark only the remaining unanswered gaps. An answer of
none never cancels a mandatory platform or other policy requirement. Applicable policy
still contributes categories, and unknown context still uses the production floor while
remaining null. Add separate behavioral checks for all of these paths.

## Provider provenance and review history (D-01, D-02, D-08)

Proposed clarification: identify the actual authoring provider (`codex` for Codex) in new
records, while preserving earlier authors and rows. New documents start `reviewed_by: []`;
extensions preserve existing human review history without treating it as review of the
new revision. Exact current model/session identifiers remain required for full conformance.

No production integration for obtaining missing identity is proposed without evidence of
a supported host interface. Configuration defaults, guessed variables, copied historical
IDs and evaluator-only injection are excluded. If the owner wants provisional documents
with unavailable identity to be considered conformant, that is a separate contract decision;
this port currently discloses them as incomplete and does not grant that exception.

## Policy validation coverage (D-09)

Choose a single maintained runtime contract for the schema checks missing from the policy
reference, then exercise invalid date/author/link/type fields as well as semantic SV rules.
Avoid introducing a second divergent schema framework. The existing handwritten checklist
and test for max_calls=50 do not demonstrate complete policy-schema validation.

## Traceability wording (D-07)

Proposed clarification: every FR derives from a promoted idea; NFRs cite only their actual
source and user-stated NFRs need no artificial BRN link. Align the original template's
author comment with the already precise BRN mapping at an owner-approved source revision.
The template remains byte-identical in this import.
