# PRD artifact, preservation and delivery

## Format and content

Deliver one PRD for the selected scope, with traceability and handoff inline.
Reuse an existing selected template/convention when it expresses these semantics;
record how its sections carry the obligations. Preserve existing metadata and
namespaces instead of forcing migration. A real format/ownership conflict needs
a specific decision. Do not create extra READMEs, constitutions, epics, stories
or schemas to satisfy this skill.

The required semantic sections are:

| Section | Required content |
| --- | --- |
| Document context and sources | Selected request/scope and artifact identity; source IDs, locators, raw-byte digests, applicable policy and permitted effects; distinguish unavailable sources. |
| Problem, actors and outcomes | Problem/current behavior, users/consumers, outcome IDs and each outcome's source basis. |
| Scope and exclusions | Selected functionality, grounded priorities, exclusions and separately labeled later ideas. |
| Scenarios and interactions | Actor journeys/operations, boundaries, negative and cross-component behavior; explain UI non-applicability when appropriate. |
| Functional requirements | Stable IDs, source basis, actor/trigger, conditions, behavior/effects, dependencies and acceptance links. |
| Quality and operational requirements | Applicable measurable obligations, actual project policy, unresolved thresholds and reasoned non-applicability. |
| Data, interfaces and dependencies | Logical entities/state ownership, producer/consumer contracts and prerequisites; distinguish known from proposed availability. |
| Architecture and decisions | Established references, attributed decisions, alternatives and unresolved design questions with blocking stage. |
| Acceptance and traceability | Observable conditions/results and bidirectional source/outcome -> requirement -> criterion mapping; account for selected source clauses not becoming requirements. |
| Risks, assumptions and questions | Each material item has an ID, basis, owner or explicit unknown owner, affected requirements and stage/operation blocked. |
| Review handoff | Disposition/reasons, input identities, PRD ID/revision/path, review focus, missing evidence/decisions and concrete manual independent-review request. |
| Revision and follow-up notes | Source action, predecessor references, added/changed/retired IDs, drift, impacts and proposed later improvements. |

### Default new artifact

Without a governing convention use
`docs/specs/products/<prd-id>/prd-rNNN.md`. Derive a short topic plus actual UTC
timestamp for a new `<prd-id>`, matching `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`.
Check platform validity (including reserved names and trailing-dot restrictions)
and collisions; this local identifier is not a project UUID. Reuse the selected
ID on revision. NNN is the positive revision padded to at least three digits.
Resolve a user-selected destination literally, including spaces or non-ASCII
characters, within the authorized scope.

Use exactly these six default metadata fields, with substantive details in the
body. Existing approved formats may express the same meanings differently.

| Field | Value |
| --- | --- |
| `format_version` | `product-requirements-v1` |
| `prd_id` | Local artifact ID described above |
| `revision` | Integer >=1; increment from the identified predecessor |
| `updated_at_utc` | Actual RFC3339 UTC timestamp ending in Z |
| `disposition` | `READY_FOR_REVIEW` or `NEEDS_INPUT` |
| `supersedes` | Project-relative retained predecessor path, or null for the first revision; never an unversioned self-reference |

These are document fields, not authoritative framework work-state fields. Never
inject them into unrelated closed records. Use the [template](../assets/prd-template.md)
for this new default format and remove its authoring comments before delivery.
Do not embed a self-referential whole-file digest: compute the final raw-byte
SHA256 after saving and report it in the delivery message or external handoff.

## Determine disposition

`READY_FOR_REVIEW` requires attributable selected outcomes/requirements,
applicable quality obligations, explicit acceptance/dependency mappings and no
known unresolved product decision or unavailable essential source that would
force invented behavior. Explicit architecture choices assigned to review/design
may remain if their later-work effects are visible.

`NEEDS_INPUT` names each exact blocking question/source, known owner or unknown
owner, affected requirements and blocked operation. Preserve useful partial
content. Both dispositions can be delivered and inspected; neither establishes
independent review, approval, implementation readiness or acceptance. Do not
produce an AI-completion probability or hide a known gap behind a label.

## Inspect before writing

Read the literal destination, ownership, lineage and relevant current input bytes.
Resolve authorized output/history boundaries and inspect path components before
creating directories or files. Reject traversal or symlink/reparse escape. Do not
switch roots or destinations to evade a real permission denial. Keep unrelated
files, governing inputs and predecessor bytes intact.

By default create a successor **exclusively**, failing on collision rather than
overwriting. Inspect competing revisions; do not claim a current successor if
lineage is missing or ambiguous. Immediately before writing, recheck destination
state against the inspected base and relevant live source identities against the
content/digest versions used for the claims. Apply the drift procedure below if
any source differs; do not replace that comparison base with a fresh hash alone.

When the user or project contract explicitly selects replacement of a canonical
path, first save its exact before-image exclusively in a fresh disjoint history
location, normally `docs/plan/prd-revisions/<prd-id>/<UTC-run>/`. Verify the retained
bytes and digest against the original, and immediately recheck the live file
against that base before targeted replacement. In default metadata `supersedes`
names the retained before-image, not the live canonical path. Missing permission
or preservation capability blocks replacement; independent drafting can continue.
Do not invent an automatic backup/restore transaction or protected atomicity.

## Reconcile source drift

Use the paired content/identity acquisition in
[intake and evidence](intake-and-evidence.md#acquire-one-content-and-identity-version).
Compare relevant live source identities with those claim-bound versions both
immediately before the write and at final delivery readback. If unchanged,
continue ordinary authorized delivery; no extra approval, source-copy artifact
or repeated interview is needed.

For each changed source:

1. Acquire and inspect the changed content with its digest from the same bytes.
   Retain the old and new observed identities in change notes. A matching file
   path or a newly calculated hash does not establish that old claims still hold.
2. Trace changed clauses through source/outcome mappings to every affected
   requirement, acceptance criterion, decision and provenance entry. Inspect
   repeated statements in scope, scenarios, interfaces and handoff as well;
   updating the primary requirement alone can leave contradictory acceptance.
3. Reconcile affected claims using the actual governing source authority. Preserve
   unaffected supported claims and stable IDs. Recency or a new digest alone
   cannot override an established decision. When authority or meaning is unclear,
   retain both positions, identify affected IDs and the exact material question,
   and mark dependent scope `NEEDS_INPUT`; continue independent drafting.
4. Update source attribution only together with the claims actually derived from
   that observed version. Record changed clauses, affected IDs, the selected
   resolution or unresolved blocker, and downstream impact in revision notes.
   Recompute readiness from reconciled content. Hash-only refresh is insufficient.
5. Recheck the candidate's semantic consistency and use the existing safe-write
   and full-readback procedure. If drift was detected after a write, retain that
   attempted artifact and identify its stale obligations. Do not hand it off as
   a current read-back candidate. Deliver reconciled content only through a safe
   successor or an already authorized canonical revision with verified history;
   do not automatically overwrite, blindly replay or claim rollback.

If drift cannot be resolved during this attempt, report the observed versions,
affected obligations and incomplete current delivery explicitly. A newly saved
`NEEDS_INPUT` document may honestly describe the unresolved versions/conflict; it
must not attribute older semantics to newer bytes. Ordinary read/hash/write checks
are observations, not an atomic transaction or a guarantee against adversarial
concurrent replacement. If further drift is observed, reconcile again or report
the remaining uncertainty rather than claiming a current candidate.

## Readback, failure and resume

Read delivered bytes completely against intended content and the artifact
contract; at this final readback compare relevant live inputs with the paired
source versions actually used for its claims. A successful command, announced
path or byte-for-byte output match alone is not current delivery. If inputs
changed, perform the semantic drift procedure above before handing off a current
candidate, even when the output matches the intended draft exactly.

On collision, competing edit, drift, access denial, partial write or failed
readback, retain the attempt and observed state. Report the actual path, error,
partial file if any, preserved history and remaining work. State that no current
read-back candidate was delivered by that attempt. Do not delete unknown work,
claim rollback or silently retry in another directory.

On resume inspect the actual destination, retained history and current sources
before any retry. Interrupted canonical replacement retains its before-image and
uncertain live state until reconciled; do not blindly replay or automatically
restore. There is no package-owned background process or cleanup helper here.
Reuse only still-supported claims; preserve unaffected requirements and decisions.

For an authorized revision, preserve surviving IDs and explain added, changed,
superseded and retired IDs, their decision origins and downstream impact. A
clarification extends the current objective; a replacement explicitly records
supersession. Review findings select a correction only under actual revision
authorization. Preserve the independent report/finding and request independent
retest; an earlier PASS remains historical evidence for its original bytes.

If the selected PRD already meets the requested authoring scope, return
`UNCHANGED` with exact current path/digest and review handoff. Reassess current
limitations in the response without silently changing stored metadata, renaming
the artifact or making a ceremonial duplicate. Interview-only work creates no
files and reports persistence as pending/not selected.

## Return the actual result

Separate source action (`CREATED`, `REVISED`, `UNCHANGED`, or no completed source
action on failure) from disposition and delivery state. Link the actual PRD and
history when present; give PRD ID/revision/path, final digest, material gaps and
the next owner. For incomplete delivery identify partial files without presenting
them as a saved review candidate. A useful `NEEDS_INPUT` document can still be a
fully saved artifact when its readback succeeds.

Supply a concrete plain-English request, filled with actual identities:

> Independently review the selected scope in PRD [ID, revision, actual path and
> SHA256], using [governing sources with locators/digests] and [canonical architecture
> references]. Assess contradictions, missing behavior, architecture sufficiency,
> feasibility, quality obligations and testable acceptance. Focus on [specific
> questions/gaps]. Return findings to the owning author; this authoring disposition
> is not your review result.

Name **prd-review** as the next responsibility. If unavailable, use this manual
request without asserting an installed command. Do not invoke review, validation,
story generation, worktree creation, sprint assignment, implementation, product
QA, merge or deployment. Changed candidates require applicable independent
assessment; this author cannot close the independent finding.
