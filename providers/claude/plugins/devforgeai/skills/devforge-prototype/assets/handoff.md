---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-{{number}}"
artifact_type: "handoff"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{actual-ISO-8601-UTC-time}}"
producer:
  skill: "devforge-prototype"
  skill_revision: "{{sha256 of the installed SKILL.md file, or unknown with a reason}}"
execution_ref: "{{SESSION-ID}}@{{revision}}, or null with the reason recorded in missing_inputs"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Experiment handoff: {{the uncertainty that was tested}}

Populate this when the experiment closes, at a transfer, or at a recovery checkpoint. Aim for something a person can scan. The plan and the report hold the full detail - link them rather than copying them here. Replace these directions with actual content.

## Result and next action

- **Question tested:** {{the uncertainty, and the decision that was waiting on it}}
- **Observed result:** {{what the measurements actually showed against the threshold in the plan; threshold met, missed, or not measured}}
- **Recommendation:** {{what you propose follows from that - stated as a recommendation, never as the decision}}
- **Prototype disposition proposed:** {{discard / keep as reference / candidate for hardening}}, adoption still the user's
- **Limits of what was measured:** {{scope, environment, sample, and anything the experiment did not cover}}
- **Next:** {{one concrete task, its actual owner, the permitted writes, and the expected deliverable}}
- **Readiness:** {{ready within the receiver's existing assignment, or prepared with the exact missing prerequisite and its owner}}
- **Validation status:** {{what was and was not independently checked; a self-run measurement is not an independent check}}
- **Enforcement status:** {{requirements recorded; no gate implemented by this skill / not applicable}}

## Inputs consumed and outputs produced

Exclude this handoff from the table: it cannot contain its own complete-byte digest, and it does not list itself among its own outputs. Hash each file only after its bytes are final. Where no artifact of a kind was produced, say so instead of inventing a row.

| Direction | Artifact ID and revision | Store and path | SHA-256 | Relevant sections | State |
| --- | --- | --- | --- | --- | --- |
| input | {{upstream brief, design or contract identity}} | {{locator}} | {{digest}} | {{section IDs relied on}} | {{draft / accepted / stale}} |
| output | {{XPLAN identity}} | {{locator}} | {{digest}} | {{case IDs}} | {{frozen before execution / revised}} |
| output | {{XREPORT identity}} | {{locator}} | {{digest}} | {{case IDs}} | {{state}} |

## Prototype identity

The prototype is a distinct thing from the report about it, and a disposition means nothing without an identity it applies to.

- **Fence actually used:** {{the declared permitted path, and confirmation that nothing was written outside it}}
- **Prototype location or snapshot:** {{path, commit or immutable reference}}
- **File manifest:** {{reference to the manifest, or the reason there is none}}
- **Reproduction steps:** {{verified commands, or the steps that could not be verified and why}}
- **Runtime observed:** {{versions and configuration that the measurements depend on}}

## Observed checks

| Check | Outcome | Raw evidence or external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| {{planned case}} | {{observed result / failed / COULD_NOT_RUN}} | {{raw output locator}} | {{cause or limit}} |

Use `NOT_RUN` for something planned and unattempted, `COULD_NOT_RUN` with the actual cause for a required observation that was blocked, and `NOT_APPLICABLE` only for a stated scope exclusion. The absence of an error is not a pass, and a measurement that could not be taken supports no claim about performance, feasibility or cost.

## Continuation directory

| Order | Task | Owner or skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | {{one immediate next task}} | {{user / named skill / external operator}} | {{required inputs or decisions}} | {{artifact or receipt}} |
| {{later}} | {{follow-on work if useful}} | {{owner}} | {{dependency}} | {{evidence}} |

The usual consumers of a prototype-report are the skills that own the affected document - define-product, design, architect, plan or change - and an experiment-plan is read by a later iteration of this skill or by review. Much of the DevForge roster is specified but not implemented, so check what is actually installed before naming it rather than reading a name off the roster. Where the natural consumer is absent, say so as a capability gap and give a plain-language task the user can act on.

## Copyable next task

Include a runnable task only when the receiving skill or owner, the input locations, the writable destination and any required allowance are all known. Name an installed skill or a plain-language task - never a slash command for a skill you have not confirmed is installed. Otherwise give the concrete prerequisite task and label the continuation pending.

```text
Goal: {{one concrete result}}
Context: {{this saved handoff's path, the XPLAN and XREPORT identities, and the sections that matter}}
Task: {{one authorised task against the artifacts named there}}
Preserve: {{the observed results, the recorded threshold, and the prior evidence that must survive}}
Output: {{required result and the next handoff}} to {{assigned output directory}}
Stop at: {{completion, or the stated missing prerequisite}}
```

## Retention and continuation limits

- **Output readback:** {{completed output paths and digests, or none produced; excludes this handoff}}
- **This handoff's location:** {{saved path, or not yet persisted; no self-digest}}
- **This handoff's receipt:** compute its digest after saving and reading it back, then deliver the path and digest in the permitted outbox or the terminal response. Do not write that digest into this document.
- **Worktree ownership:** {{retained / handed off / released, with the operator reference}}
- **External gate state:** {{actual receipt reference, or none; never an inferred phase}}
- **Conditions invalidating this handoff:** {{upstream revision, prototype, runtime or assignment changes}}

Retain the exact referenced bytes and every observed failure; a digest cannot recover a missing source. A preserved negative result is the point of the experiment, not an embarrassment to tidy away, and no later revision may quietly replace the threshold it was measured against.

A prepared handoff is not a receiving invocation and not acceptance. This document authorises no promotion of prototype code, no amendment to an accepted decision, and no external action.
