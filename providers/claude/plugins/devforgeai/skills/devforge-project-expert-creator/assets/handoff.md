---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-{{allocated-identity}}"
artifact_type: "handoff"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{actual-ISO-8601-UTC-time}}"
producer:
  skill: "devforge-project-expert-creator"
  skill_revision: "{{digest of the loaded SKILL.md file, or unknown with a reason}}"
execution_ref: "{{SESSION-ID}}@{{revision}}, or null with the reason recorded in missing_inputs}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Authoring handoff: {{target skill}}

Populate this at authoring completion, at a transfer, or at a recovery checkpoint. Aim for something a person can scan; length is not an acceptance condition. The specification, package record and change record keep the full detail - link them rather than copying them here. Replace these directions with actual content.

## Result and next action

- **Result:** {{what was created, reused or enhanced; complete or partial; the candidate identity is in the evidence below}}
- **Why:** {{the one decision that affects what happens next; point at the detailed record for the rest}}
- **Limits and blockers:** {{unresolved findings or questions, and any authority or readiness that affects the next action}}
- **Next:** {{one concrete task, the actual owner, the permitted writes, and the expected deliverable}}
- **Readiness:** {{ready within the receiver's existing assignment, or prepared with the exact missing prerequisite and its owner}}
- **Validation status:** Not performed.
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** {{requirements recorded; no gate implemented by this skill / not applicable}}

## Outputs produced

Exclude this handoff from the table: it cannot contain its own digest, and it does not list itself among its own outputs. Hash each file only after its bytes are final. Where no artifact of a kind was produced, say so instead of inventing a row.

| Direction | Artifact ID and revision | Store and path | SHA-256 | Relevant sections | State |
| --- | --- | --- | --- | --- | --- |
| input | {{identity}} | {{locator}} | {{digest}} | {{IDs}} | {{decision or freshness state}} |
| output | {{identity}} | {{locator}} | {{digest}} | {{IDs}} | {{state}} |

## Evidence and reading order

Record the exact path and digest references once, in `upstream` and `evidence`. Use names and links below to navigate them rather than repeating the inventories.

| Read when | Record and relevant sections or IDs | Purpose |
| --- | --- | --- |
| First | {{candidate manifest / package record and the specification}} | Identify the exact candidate and the assigned requirements. |
| Before acting | {{change record and decision references}} | Preserve the decisions, boundaries, pending work and honest evidence limits. |
| For an affected question | {{discovery record, retained sources or prior reports; exact section and finding IDs}} | Recover the rationale, alternatives, search limits and original evidence. |

Required detail that is missing must be saved in the appropriate record and referenced, or named in `missing_inputs`. Shortening this handoff cannot discard it, and it does not reduce the receiver's review coverage.

## Proposed evaluation cases

The cases proposed for this candidate, with their independently stated expectations, live in {{path to the specification's acceptance-expectation section, or the cases file}}. They were captured, not executed.

| Check | Outcome | Evidence or receipt | Cause or scope limit |
| --- | --- | --- | --- |
| {{proposed case or check}} | NOT_RUN | {{reference, or none}} | {{cause or limit}} |

Use `NOT_RUN` for something planned and unattempted, `COULD_NOT_RUN` with the actual cause for a required observation that was blocked, and `NOT_APPLICABLE` only for a stated scope exclusion. The absence of an error is not a pass.

## Copyable next task

Include a runnable task only when the receiving skill or owner, the input locations, the writable output destination and any required allowance are all known. Distinguish a host path from a sandbox alias. Name an installed skill or a plain-language task - never a slash command for a skill you have not confirmed is installed. Otherwise give the concrete prerequisite task and label the evaluation pending.

```text
Goal: {{one concrete result}}
Context: {{this saved handoff's path, and the reading order it gives}}
Task: {{one authorised task and its scope, against the candidate and specification named there}}
Preserve: {{the decisions, constraints and prior evidence that must survive}}
Output: {{required results and the next handoff}} to {{assigned output directory}}
Stop at: {{completion, or the stated missing prerequisite}}
```

## Retention and continuation limits

- **Output readback:** {{completed output paths and digests, or none produced; excludes this handoff}}
- **This handoff's location:** {{saved path, or not yet persisted; no self-digest}}
- **This handoff's receipt:** compute its digest after saving and reading it back, then deliver the path and digest in the permitted outbox or the terminal response. Do not write that digest into this document.
- **Worktree ownership:** {{retained / handed off / released, with the operator reference}}
- **External gate state:** {{actual receipt reference, or none; never an inferred phase}}
- **Conditions invalidating this handoff:** {{source, candidate, runtime or assignment changes}}

Retain the exact referenced bytes and any earlier failures; a digest cannot recover a missing source. Record an identity change as a new revision rather than rewriting prior evidence.

A prepared transfer is not receiving execution and not acceptance. This document authorises no evaluation, installation, activation or automatic invocation of a receiver. No self-digest, and no circular receipt reference.
