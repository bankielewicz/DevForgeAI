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
  skill_revision: "{{actual-loaded-creator-revision-or-digest}}"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Authoring handoff: {{target skill}}

Populate at completion, transfer or recovery. Aim for a brief a person can scan; length is not an acceptance gate. Preserve the full specification, rationale, change/phase record and raw evidence in their existing files. Replace these directions with actual content.

## Result and next action

- Result: {{what was created/reused/enhanced; complete/partial authoring; candidate identity via the evidence below}}.
- Why: {{one decision affecting continuation; reference the detailed decision/change record}}.
- Limits and blockers: {{validation/hook status; unresolved findings/questions, authority or readiness that affects the next action}}.
- Next: {{one concrete task, actual owner/skill, permitted writes and expected deliverable}}.
- Readiness: {{ready within the existing receiver assignment, or prepared with the exact missing prerequisite and its owner}}.

## Evidence and reading order

Put exact path/SHA-256 references once in upstream/evidence; use links or names below to navigate them. The candidate manifest maps source files; XSPEC/XPKG and the change record retain detailed identities, requirements, decisions, phase dispositions and provenance. Do not copy their inventories here.

| Read when | Existing record and relevant sections/IDs | Purpose |
| --- | --- | --- |
| First | {{candidate manifest/XPKG and specification/XSPEC links}} | Select exact candidate and assigned requirements. |
| Before acting | {{change/phase record and decision references}} | Preserve decisions, boundaries, pending work and honest evidence limits. |
| For an affected question | {{input/discovery records, retained sources or prior reports; exact section/finding IDs}} | Recover rationale, alternatives, search limits and original evidence. |

Missing required detail must be saved in the appropriate record and referenced, or named in missing_inputs; shortening the handoff cannot discard it. Required review coverage still applies.

## Copyable next-session task

Include a task ready for the assigned receiving environment only when its skill location, input locations, writable output destination and required execution/review allowance are known. Distinguish host paths from sandbox mount aliases. Otherwise provide the concrete prerequisite task and label evaluation pending; do not leave a runnable-looking prompt with unresolved allocations.

```text
Use {{actual available receiving skill and its resolved SKILL.md path}}.
Read {{this saved handoff path}} and follow its reading order.
Perform {{one authorized task and scope}} on the candidate/specification
identified there, preserving {{essential decisions and constraints}}.
Write {{required results and next handoff}} to {{assigned output directory}}.
Use {{existing receiver/review allocation or its exact reference}}.
Stop at {{completion or stated missing prerequisite}}.
```

## Retention and continuation limits

Retain exact referenced bytes and earlier failures. A hash cannot recover a missing source. Use the assigned artifact storage; before cleanup or relocation, preserve evidence and an explicit path mapping. Record affected identity changes in a new revision rather than rewriting prior evidence.

Prepared transfer is not receiving execution or acceptance. No target validation, installation, hook activation or automatic receiving invocation is authorized by this document. In unmanaged mode, label hashes as author observations. If an actual managed assignment applies, reference its runtime/custody record and unresolved observations here; do not reproduce it. No self-digest or circular receipt references.

## Terminal display

After this handoff and its referenced detailed records are saved, use [completion-summary.md](completion-summary.md) for the terminal response. The display links here; it does not replace the evidence envelope, reading order, receiver readiness or full change record. Include the phase/obligation preservation map in the referenced specification for a structural enhancement.
