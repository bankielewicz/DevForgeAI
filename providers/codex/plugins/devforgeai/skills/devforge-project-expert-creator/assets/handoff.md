---
schema_version: devforge.artifact/v1
artifact_id: "HANDOFF-{{allocated-artifact-identity}}"
artifact_type: handoff
project_id: "{{project-id}}"
revision: 1
status: draft
created_at_utc: "{{actual-UTC-time}}"
producer:
  skill: devforge-project-expert-creator
  skill_revision: "{{actual-loaded-builder-revision-or-digest}}"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Prepared skill authoring handoff

Populate only at actual authoring completion, transfer or a recovery checkpoint. Use the shared envelope above; populate upstream/evidence with exact known references and use null plus missing_inputs for unavailable identity or runtime observations. This is substantive continuation content, not a runtime receipt or new authority.

## You are here

- Skill and use case: {{target skill, provider, requested result}}.
- Current task/phase state: {{actual phase from runtime, or unmanaged authoring/recovery; complete/partial/blocked content}}.
- Document preparation: {{prepared or partial}}.
- Runtime transition admission: {{actual observation/reference or NOT_OBSERVED}}.
- Receiving skill invocation: {{actual observation/reference or NOT_RUN}}.
- Session/worktree assignment and existing write fence: {{actual authority, worktree/branch/base, allowed paths; missing values and reasons}}.
- Existing authorization carried forward: {{user-selected scope and decision references; no expanded permission}}.

## Inputs consumed and outputs produced

Exclude this document's own digest. Use complete saved artifact references; runtime computes final identities in managed operation. If that has not occurred, retain exact paths with null identities and reasons, rather than claiming protected checks. Ordinary unmanaged authoring observations may be identified as such. Do not create circular references through a later receipt.

| Direction | Artifact ID/revision | Store/path | SHA-256 or unavailable reason | Relevant sections | Decision/freshness state |
| --- | --- | --- | --- | --- | --- |
| input | {{selected specification/contracts}} | {{exact paths}} | {{identities}} | {{requirements}} | {{selection source}} |
| input | {{former candidate/report}} | {{retained paths}} | {{identities}} | {{F/CHG IDs}} | {{historical; unchanged}} |
| output | {{authored skill manifest and specification}} | {{exact paths}} | {{observed identities or unavailable}} | {{changes}} | {{new candidate; unvalidated}} |
| output | {{substantive change record/integration specification}} | {{exact paths}} | {{observed identities or unavailable}} | {{remaining scope}} | {{prepared}} |

## What changed and what remains open

- Applied/deferred/declined changes and preserved behavior: {{F/CHG mapping and reasons}}.
- Adopted decisions: {{actual source; preserve named Optional/Enforced groups}}.
- Proposals/defaults not adopted: {{separate suggestions}}.
- Material unanswered questions and independent work: {{question, dependency, pending owner}}.
- Runtime/installation/evaluation gaps: {{actual missing capability; no self-issued approval}}.

## Observed completion evidence

Record only observations that existed when this document was authored. Leave later operations NOT_RUN/NOT_OBSERVED with their cause; never rewrite this document to assert a later receipt.

| Check | Outcome | Raw evidence / external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Substantive authoring outputs | {{saved/partial}} | {{completed paths}} | Source content only |
| Validation | Not performed | none | Separate allocated evaluation required |
| Runtime final-byte checks | {{observed or NOT_RUN}} | {{actual reference or null}} | {{creation-time limit}} |
| Runtime receipt publication/readback | {{observed or NOT_RUN}} | {{actual reference or null}} | {{creation-time limit}} |
| Native transition / receiving invocation / rendered delivery | {{separate observations or NOT_OBSERVED / NOT_RUN}} | {{actual references or null}} | A prepared document proves none of these |

## Continuation directory

| Order | Task | Allocated owner / skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | {{one immediate next task}} | {{actual owner role; unknown personal identity remains explicit}} | {{authority, candidate, contract, boundaries}} | {{concrete artifact/evidence expected}} |
| 2 | {{dependent evaluation or integration}} | {{owner}} | {{unmet dependencies}} | {{separate observations}} |

## Copyable next-session prompt

Goal: {{one concrete next result for the allocated owner}}.
Context: {{exact specification, candidate manifest and relevant sections; preserved decisions}}.
Output: {{named collision-safe deliverable in the assigned destination}}.
Boundaries: {{existing authorization, worktree/fence, forbidden changes and no implicit receiver invocation}}.
Prerequisites: {{missing authority/runtime/input observations before dependent work}}.
Completion evidence: {{what the next owner must produce under its own allocation; this does not launch it}}.

Use actual skill names or known interfaces. For an unimplemented adapter, request implementation of that capability under its owner's assignment; never present a fictional command as callable.

## Resume and custody

- Task-output write/readback observations: {{actual completed outputs only, scope and observer}}.
- This handoff's location: {{saved path; no self-digest}}.
- External receipt: {{actual preexisting runtime reference or null; later publication/readback NOT_RUN at creation}}. Runtime owns managed final identities, protected snapshot and receipt publication/readback. No model-driven advance/resume/complete/check/verify or receipt-helper fallback.
- Worktree ownership disposition: {{actual retained/handed-off/released record; prepared text does not transfer ownership}}.
- External gate state: {{actual observed reference or unavailable}}.
- Resume point: {{last substantive result and exact pending task}}.
- Invalidation: {{candidate/specification/selected sources/assignment/runtime/installation changes require affected reconciliation and new evidence; preserve prior bytes and outcomes}}.

## Manual transfer and scope

- Detailed source/XSPEC/XPKG or EVPLAN/EVREPORT references: {{exact saved artifacts and section IDs}}
- Actual requested claim and Routine/Full selection: {{mode, scope, reasons and reviewer status}}
- Accepted baseline/current Routine/qualified anchor: {{distinct exact references or missing causes}}
- Immediate/cumulative impact and compatibility: {{exact records and unresolved dependencies}}
- Receiving invocation: {{one copyable user task with this handoff's saved path and the receiver name}}
- Receiving evidence at creation: {{NOT_RUN unless the receiver has actually loaded and acted on real producer artifacts}}

The prepared handoff authorizes no automatic receiver or command. Carry existing user authority forward; retain failures and new-candidate identities. The trusted installer separately requires current manual adoption evidence. The evaluator's own handoff does not recursively trigger Full qualification.
