# Report format and safe delivery

Load when choosing a destination, persisting, resuming, reusing or handing off a
review. The report is an assessment artifact, not an authority record.

## Select one literal output

Default to `docs/plan/prd-reviews/<prd-id>/<UTC-run>/prd-review.md` under the selected
project. Use the PRD's safe local ID where possible; otherwise derive a safe topic
identifier and record its mapping without rewriting the PRD's identity. Use actual
UTC time with sufficient precision and verify a fresh exclusive location.

Inspect literal input/output paths and relevant components. Check platform
validity, reserved names, trailing dots/spaces, spaces/non-ASCII handling and
collisions. Keep output disjoint from the PRD, governing sources and prior
evidence. Reject traversal and link/junction escape. Never treat arbitrary IDs as
unchecked path fragments or silently rename a selected root.

Reuse a selected compatible project report convention and destination with
documented semantic correspondence. Do not force PRD metadata changes or extra
reports. Missing root/destination blocks saving, not useful discussion. A
conversation-only/read-only request creates no report files.

## Default header and required body

A new default report has exactly six metadata fields:

| Field | Value |
| --- | --- |
| format_version | prd-review-v1 |
| review_id | Nonempty [A-Za-z0-9][A-Za-z0-9._-]{0,63}, platform-safe and unique within selected review history |
| created_at_utc | Actual RFC3339 UTC timestamp ending in Z |
| assessment | PASS, CHANGES_REQUIRED or INCOMPLETE under the assessment reference |
| assessment_complete | Boolean under the assessment reference; PASS requires true |
| supersedes | Selected retained prior review's project-relative path, explicit resolved external predecessor path, or null initially |

One Markdown report carries these eight semantic sections inline:

| Section | Required substance |
| --- | --- |
| Scope and context | Request; PRD ID/revision/path/digest; full/focused scope; next use; exclusions; actual review context and independence limits. |
| Evidence inventory | Governing sources, policy, architecture, observations and prior evidence; source IDs, roles, locators, paired raw-byte hashes or actual conversation/external provenance; unavailable inputs and significance. |
| Review matrix | Bidirectional original -> PRD -> acceptance -> observation/finding mappings; applicable areas, row statuses and justified unassessed/non-applicable content; actual counts with scope limits. |
| Findings and questions | Complete actionable finding records, known blockers, later-stage items, actual decisions and unknown owners; explicitly no findings when applicable. |
| Architecture and dependency disposition | Confirmed boundaries, conflicts, justified deferrals with blocking activities, evidence limitations, shared resources and integration prerequisites. |
| Assessment and limitations | Scoped result and completeness rationale; next-use and later obligations; observed input stability; unperformed verification and delivery limitations. |
| Retest and continuity | Initial review or prior report identity; selected dispositions; changed/unchanged source identities, impact reassessment, untargeted findings and unreviewed scope. |
| Manual handoff | Exact candidate/governing identities; repair/decision owner or planning consumer; concrete next request and delivery limits. |

Use stable source/candidate IDs and review-local locators where necessary. Do not
insert IDs into the PRD. Keep the report's final whole-file digest external to its
own bytes. The [template](../assets/prd-review-template.md) is a writing aid; fill
or replace its prompts with actual evidence. Do not assert successful final
readback inside a report that has not yet been read back.

## Persist and verify actual delivery

Before saving, perform the assessment reference's live-input comparison and
semantic reconciliation. Verify output scope, ownership and exclusivity again.

Create a fresh report exclusively. Collision does not authorize overwriting a
prior report or unknown work. Reconcile or select another fresh location within
already authorized scope. An actual permission denial is a delivery gap; do not
change roots or permissions to evade it.

Read all saved bytes back against intended content and the required report
semantics. A successful command, announced path or existing file alone is not
verified delivery. Then compare relevant input identities again and reconcile any
drift as directed by [assessment and retest](assessment-and-retest.md). Deliver
the actual report path and SHA256 of the final read-back bytes externally.

If writing partially succeeds, is interrupted, or full readback fails after a
successful write, retain the attempted artifact and exact observed state/error.
Useful findings remain available, but report no verified current delivery from
that attempt. Do not invent rollback, cleanup success or a successful read from
command status alone. Keep assessment/completeness and delivery outcome distinct.

On resume, inspect retained artifacts, uncertain effects and current inputs;
reconcile before retrying into a fresh authorized location. Do not replay blindly
or overwrite interrupted/stale reports. A fresh successor identifies the retained
predecessor. No persistent service or background process is needed.

When asked only to inspect/reuse an existing report, check current applicability
and return its exact identity without a ceremonial duplicate. A newly requested
assessment produces its own report. For conversation-only review state that no
saved artifact was selected and provide useful bounded findings in conversation.

## Return the next action manually

In plain English return the scoped assessment, assessment_complete, actual
saved/not-saved/failed delivery state, candidate and report identities, key findings
and material limitations. Separate any stale/historical attempt from the current
delivery observation.

- CHANGES_REQUIRED: provide a bounded manual prd-create revision request, or the
  relevant policy/architecture decision request, naming candidate, governing
  inputs, findings, owner and independent resolution conditions. Preserve any
  incomplete areas alongside known blockers.
- INCOMPLETE: name the exact missing source, decision, review area, identity check
  or separate review context needed. Preserve usable findings and partial work.
- PASS: hand the declared scope to work planning with canonical references,
  unresolved later-stage prerequisites, shared ownership and integration
  obligations. If another next use was explicitly selected, apply its stated
  prerequisites and identify that consumer.

If a workflow is unavailable, name its responsibility rather than an invented
installed command. No automatic epics/stories, sprint, worktree, implementation,
QA, merge or deployment follows. A planning assessment cannot grant authority
to implement the entire PRD or supersede canonical policy.
