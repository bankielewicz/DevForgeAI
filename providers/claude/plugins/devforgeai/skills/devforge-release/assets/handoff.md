---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-{{allocated-identity}}"
artifact_type: "handoff"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{actual-ISO-8601-UTC-time}}"
producer:
  skill: "devforge-release"
  skill_revision: "{{digest of the loaded SKILL.md file, or unknown with a reason}}"
execution_ref: "{{SESSION-ID}}@{{revision}}, or null with the reason recorded in missing_inputs"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Delivery handoff: {{candidate or release scope}}

Populate this at the end of every result - a published release, a draft nobody was authorized to publish, or a blocked recheck. Aim for something a person can scan; length is not an acceptance condition. The release record holds the full inventories - link it rather than copying it here. Replace these directions with actual content.

## Result and next action

- **Result:** {{what was prepared; what, if anything, was actually executed; complete, partial or blocked - the exact identities are in the evidence below}}
- **Why:** {{the one decision that affects what happens next; point at the release record for the rest}}
- **Limits and blockers:** {{missing authority, unresolved findings, unavailable checks, and anything that affects the next action}}
- **Next:** {{one concrete task, its actual owner, the permitted writes, and the expected deliverable}}
- **Readiness:** {{ready within the receiver's existing assignment, or prepared with the exact missing prerequisite and its owner}}
- **Published:** {{nothing published / the exact external references that were created and read back}}
- **Behavioural status:** NOT_EVALUATED.
- **Enforcement status:** {{requirements recorded; no gate implemented by this skill / not applicable}}

Keep "prepared" and "published" apart in this section, not only in the table below. A reader who takes one line away from this document should not be able to take away the wrong one.

## Outputs produced

Exclude this handoff from the table: it cannot contain its own digest, and it does not list itself among its own outputs. Hash each file only after its bytes are final. Where no artifact of a kind was produced, say so instead of inventing a row.

| Direction | Artifact ID and revision | Store and path | SHA-256 | Relevant sections | State |
| --- | --- | --- | --- | --- | --- |
| input | {{QA identity and revision}} | {{locator}} | {{digest}} | {{sections relied on}} | {{decision or freshness state}} |
| input | {{development-record / story / architecture-contract, as relevant}} | {{locator}} | {{digest}} | {{sections}} | {{state}} |
| output | {{REL identity and revision}} | {{locator}} | {{digest}} | {{sections}} | {{state}} |

## Delivery observations

The five rows from the release record's delivery table, carried here so the receiver sees them without opening it. They stay five rows. Use `NOT_RUN` for something planned and unattempted, `COULD_NOT_RUN` with the actual cause for a required observation that was blocked, and `NOT_APPLICABLE` only for a stated scope exclusion. The absence of an error is not a pass, and a local result is never recorded as a hosted one.

| Event | Outcome | External reference read back | Cause or scope limit |
| --- | --- | --- | --- |
| Local candidate verification | NOT_RUN | {{receipt path, or none}} | {{cause or limit}} |
| PR creation | NOT_RUN | {{actual URL if created, or none}} | {{the authority it needs, and its owner}} |
| Merge | NOT_RUN | {{actual commit if merged, or none}} | {{cause}} |
| Deployment | NOT_RUN | {{actual deployment reference, or none}} | {{cause}} |
| Post-release verification | NOT_RUN | {{observation, or none}} | {{cause}} |
| Hosted CI | NOT_RUN | {{result locator and exact revision, or none}} | {{unavailable, unreachable, or not run for this revision}} |

## Evidence and reading order

Record the exact path and digest references once, in `upstream` and `evidence`. Use names and links below to navigate them rather than repeating the inventories.

| Read when | Record and relevant sections or IDs | Purpose |
| --- | --- | --- |
| First | {{the release record, and the QA it binds}} | Identify the exact candidate and what was actually done to it. |
| Before acting | {{the planned-actions table and any authorization references}} | See which actions are authorized, which are waiting, and on whom. |
| For an affected question | {{development-record, story, architecture-contract; exact section and rule IDs}} | Recover the scope, the verification evidence and the migration or recovery requirement. |

Required detail that is missing must be saved in the release record and referenced, or named in `missing_inputs`. Shortening this handoff cannot discard it, and it does not reduce the receiver's review coverage.

## Copyable next task

Include a runnable task only when the receiving skill or owner, the input locations, the writable output destination and any required allowance are all known. Distinguish a host path from a sandbox alias. Name an installed skill or a plain-language task - never a slash command for a skill you have not confirmed is installed. `devforge-change`, the usual consumer of a release record, is specified in the roster and may not be implemented in this environment; check before naming it, and give a plain task if it is absent.

```text
Goal: {{one concrete result}}
Context: {{this saved handoff's path, and the reading order it gives}}
Task: {{one authorised task and its scope, against the release record and candidate named there}}
Preserve: {{the decisions, authorities and prior evidence that must survive}}
Output: {{required results and the next handoff}} to {{assigned output directory}}
Stop at: {{completion, or the stated missing prerequisite}}
```

## Retention and continuation limits

- **Output readback:** {{completed output paths and digests, or none produced; excludes this handoff}}
- **This handoff's location:** {{saved path, or not yet persisted; no self-digest}}
- **This handoff's receipt:** compute its digest after saving and reading it back, then deliver the path and digest in the permitted outbox or the terminal response. Do not write that digest into this document, and do not edit this document later to record a receipt it did not have when it was written.
- **Worktree ownership:** {{retained / handed off / released, with the operator reference}}
- **External gate state:** {{actual receipt reference, or none; never an inferred phase}}
- **Conditions invalidating this handoff:** {{candidate, upstream revision, target branch or environment, authority, or assignment changes}}

Retain the exact referenced bytes and any earlier failures; a digest cannot recover a missing source. Record an identity change as a new revision rather than rewriting prior evidence. Operational failure after a real release becomes a change request or the project's existing incident process - it is not a correction to this document.

A prepared transfer is not receiving execution, and a release record is not a deployment receipt. This document authorises no publication, merge, deployment or automatic invocation of a receiver. No self-digest, and no circular receipt reference.
