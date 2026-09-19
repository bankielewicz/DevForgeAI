# Assessment, independence, drift and retest

Load before conclusions and whenever sources change, work resumes or selected
corrections are retested. Keep result, completeness and delivery separate.

## Establish actual independence

Record known author/reviewer context and material separation limits. Independently
derive the oracle from original sources, preserve the review target and avoid
self-closing authoring findings. If this reviewing actor/session authored or
repaired the exact candidate, disclose self-review: it cannot provide independent
PASS or VERIFIED_FIXED. Preserve useful supported findings and identify the
separate review context needed for those conclusions.

Do not invent a person, model, session, fresh context or sandbox. The same model
family is not inherently disqualifying; a new terminal alone establishes no
protected separation. No subagent, paid reviewer service or different vendor is
required. This review guidance does not implement protected actor isolation.

## Reduce the result in this order

| Assessment | Required basis |
| --- | --- |
| CHANGES_REQUIRED | At least one supported unresolved BLOCKING finding prevents the declared next use, even if other assessment is incomplete. |
| INCOMPLETE | No demonstrated blocking finding yet, but a required review area, essential input, identity check or independence condition is missing/unperformed. |
| PASS | All required areas in the declared scope were assessed against sufficient consistently identified evidence; independence holds; no unresolved BLOCKING finding prevents the declared next use. |

Set assessment_complete true only when required review areas, essential inputs,
identity checks and independence conditions are satisfied. Completed assessment
may find defects: CHANGES_REQUIRED/true is valid. Defect plus incomplete review is
CHANGES_REQUIRED/false. Incomplete-only is INCOMPLETE/false. PASS requires true.

Keep nonblocking issues and later prerequisites explicit. A failed report readback
is a delivery failure, not proof of a candidate defect. Never present a known stale
conclusion as current PASS. No grade, percentage or AI success estimate overrides
a blocker. Planning PASS does not mean zero possible ambiguity, story readiness,
final architecture for all implementation, product success, user approval, release
permission or framework acceptance.

A genuinely independently assessed unaffected subset can be described separately,
with its dependencies and limits. Do not silently replace the originally requested
scope with that subset.

## Reconcile source drift semantically

Retain original content/digest pairs supporting observations. Compare relevant live
candidate and governing-source identities before report persistence and again at
final readback/delivery. Unchanged sources permit normal authorized delivery
without repeated interviews, a new permission ceremony or extra source-copy pack.

For every observed change:

1. Acquire changed content and its digest as a new pair. Retain old/new identities
   and identify changed clauses, not merely the file name.
2. Trace the changed semantics through all affected matrix rows, findings, resolution
   conditions, retest dispositions and the assessment.
3. Independently reassess each affected claim. Check the dependencies of apparently
   unaffected conclusions before retaining them. Do not refresh hashes alone,
   blindly inherit findings or discard unrelated valid observations wholesale.
4. Preserve conflicting authority or unavailable necessary content with affected
   IDs and incomplete areas. A newer source does not automatically supersede a
   co-owner or verify a fix.
5. Recompute scoped result and completeness from the reconciled evidence.

If change is observed after a report write, preserve that report as a stale attempt
and name affected conclusions. After reconciliation, create a successor in a fresh
authorized location under [report and delivery](report-and-delivery.md), or state
incomplete current delivery. Do not overwrite the attempt or announce its PASS
as current. Repeat reassessment for further observed drift, or stop the dependent
conclusion with the specific remaining uncertainty.

For an explicitly selected historical review, bind a retained immutable
candidate/source set and label the assessment historical. Do not present it as a
current review. Ordinary read/hash observations do not promise atomicity or prevent
future changes.

## Independently retest selected findings

Acquire the identified earlier report, its path/digest and selected finding IDs,
original governing obligations, revised PRD and actual current decisions. Verify
lineage and changed content independently of the author's resolution map. The
finding identity is prior report path/digest plus report-local ID; equal IDs in
unrelated reports do not identify the same defect.

For each selected finding preserve the original obligation/resolution condition,
old/new evidence, inspected affected scope and one disposition:

| Disposition | Meaning |
| --- | --- |
| VERIFIED_FIXED | Independent observation establishes the original resolution condition on the revised candidate. |
| STILL_PRESENT | Supported defect remains. |
| NOT_VERIFIED | Essential evidence, independence or assessment needed to resolve the finding is missing. |
| SUPERSEDED | An explicitly authorized governing scope/requirement change removes applicability; record provenance. This is not a demonstrated fix. |

Inspect affected requirements, acceptance criteria, repeated statements, shared
contracts and potential regressions. A corrected primary sentence with contradictory
acceptance elsewhere is not fixed. Scope deletion, weakened criteria and a changed
hash alone cannot establish repair. Record new defects separately.

Untargeted findings retain their last status and remain outstanding or historical,
with current applicability unassessed; do not silently close them. Reused
observations need unchanged identities and checked dependencies. Focused retest
PASS applies only to the selected retest scope. A new whole-PRD PASS requires a
complete selected obligation inventory and current applicability assessment of all
blocking findings.

Dispose findings in the new report, preserving earlier reports and failed attempts.
On resume, inspect actual retained writes and current paired inputs before reusing
observations. Do not automatically invoke the author or start a repair/retest loop.
