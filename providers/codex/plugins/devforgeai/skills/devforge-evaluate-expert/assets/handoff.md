---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-{{number}}"
artifact_type: "handoff"
project_id: "{{project-id}}"
revision: 1
status: draft
created_at_utc: "{{actual-UTC-time}}"
producer:
  skill: "devforge-evaluate-expert"
  skill_revision: "{{exact-loaded-validator-revision-or-digest}}"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Prepared skill validation handoff

Use at completion, transfer or recovery. Keep the populated brief about one page when practical; this is a usability target, not a gate. Follow [handoff preparation](../references/manual-operation.md#concise-handoff-and-retained-evidence), replace placeholders and remove template instructions. Retain the standard envelope. Record only facts observed when authored; preparation is not receiving execution.

## Outcome and next action

- **Result:** {{target; reporting complete/partial/blocked; separate candidate disposition and requested scope: Routine, Full, local unqualified baseline, or scoped inspection}}.
- **Decision and why:** {{supported change IDs or no justified target changes; one short evidence-based reason; detailed rationale locator below}}.
- **Next:** {{actual owner; one bounded action; completion evidence; last completed phase/task if resuming}}.
- **Limits/blockers:** {{material findings, missing observations and required setup with owner; explicit acceptance/qualification/receiving state; no target edits by evaluator}}.
- **Invocation readiness:** {{ready within the recorded assignment, or BLOCKED with exact missing receiver path, output fence, authority, review/execution allocation or stale inputs}}.

## Evidence and reading order

Fill the envelope's upstream/evidence fields with exact saved record identities using the existing artifact contract. Put each pin once in this handoff; refer to its artifact ID and section below. Existing manifests and reports retain their linked file hashes. Preserve source bytes/snapshots and raw history; a digest alone cannot reconstruct them.

| Read | Existing record and section locator | Purpose |
| --- | --- | --- |
| First | {{EVREPORT/verification results: Decision and coverage; Recovery and continuation}} | Outcome, justified next action and missing evidence |
| Then | {{repair specification: Change decision; allowed scope; selected CHG IDs}} | Requirements, rationale, invariants and bounded changes; or evaluation prerequisites only |
| Before dependent work | {{EVPLAN/assignment: exact scope, writes, review/execution bounds; XPKG/source manifest and XSPEC/spec sections}} | Verify current authority and the affected candidate/specification bytes |
| When investigating | {{EVREPORT Findings and evidence locators; relevant case/attempt/source snapshot}} | Trace a specific finding, dispute or recovery question to retained observations |

Open relevant records in that order, not every linked transcript or reference. Complete required checks/reviews remain required; selective retrieval does not narrow their coverage. Use retained storage accessible to the receiver. Identify any retention/access limit and its owner; if a required record cannot be retrieved or preserved through the assigned transfer, mark that dependent action blocked. A temporary path alone does not establish loss or authorize cleanup.

## Copyable next task

Populate only with verified receiving-environment paths and the existing assignment. A host path and a sandbox mount alias are different locators; show the verified mapping in the referenced assignment. If setup is missing, replace the code block with the concrete operator prerequisite task and mark readiness BLOCKED; do not supply a supposedly runnable prompt with unresolved placeholders.

```text
Use $devforge-project-expert-creator, loading {{actual accessible receiver SKILL.md}}.
Read {{this saved handoff path}} and follow its evidence reading order.
Implement only {{authorized CHG IDs}} from the referenced repair specification.
Verify the frozen candidate and affected specification references before writing;
preserve their requirements, Enforced choices, unrelated behavior and old evidence.
Canonical write fence: {{assigned paths}}. Save new records to {{assigned output directory}}.
Use only {{existing assignment/allocation reference and relevant section}}; do not
execute validation, install, activate hooks or initiate another receiving skill.
Return the new candidate manifest, change record, updated specification and prepared evaluator handoff.
```

When no target changes are justified, use the concrete operator/evaluation prerequisite task instead. The evaluator does not fix the target or authorize new execution. A subsequent user-initiated evaluation requires its own current assignment; this prepared return neither starts it nor recursively triggers Full qualification.

## Continuation details, when needed

Reference {{EVREPORT Recovery and continuation / Workspace preparation and native continuation}} for retained workspaces, owned processes, assignment disposition, pending readiness and invalidating input changes. Keep a consequential blocker visible above; do not duplicate the full records here.

For an actually selected managed assignment only, reference its creation-time final-byte checks, receipt publication/readback, transition, receiving and rendered-delivery observations with their distinct outcomes. Runtime owns authoritative custody and lease transfer; ordinary manual identities are evaluator observations. Omit managed details in ordinary manual use. Never add this document's own digest, call a controller as fallback, or rewrite it to claim a later receipt. Preserve prior artifacts and use a separate later record for new events.
