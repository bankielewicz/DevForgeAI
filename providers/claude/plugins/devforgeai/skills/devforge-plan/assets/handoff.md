---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-{{number}}"
artifact_type: "handoff"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{actual-ISO-8601-UTC-time}}"
producer:
  skill: "devforge-plan"
  skill_revision: "{{sha256 of the loaded SKILL.md file, labelled; or unknown with a reason}}"
execution_ref: "{{SESSION-ID}}@{{revision}}, or null with the reason recorded in missing_inputs}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Planning handoff: {{delivery slice}}

Replace these directions with actual content. Keep it scannable: the epics and stories hold the
detail, so link them rather than copying their tables here.

## You are here

- **Skill and use case:** devforge-plan — derive epics and implementable stories from adopted scope.
- **Result:** {{what was produced; complete, partial, or blocked}}
- **Delivery slice and non-goals:** {{PROD-ID@revision, the outcome, the explicit exclusions}}
- **Session/worktree assignment:** {{external SESSION reference, or null with the reason}}
- **Existing authorization carried forward:** {{reference, or none}}

## Inputs consumed and outputs produced

Exclude this handoff from the table. It cannot contain its own complete-byte digest, and it does not
list itself among its own outputs. Hash each file only after its bytes are final. Where no artifact of
a kind was produced, say so instead of inventing a row.

| Direction | Artifact ID/revision | Store/path | SHA-256 | Relevant sections | Decision/freshness state |
| --- | --- | --- | --- | --- | --- |
| input | {{PROD-ID@revision}} | {{locator}} | {{digest}} | {{REQ/NFR IDs actually used}} | {{adopted / proposed; current / stale}} |
| input | {{ARCH-ID@revision}} | {{locator}} | {{digest}} | {{RULE IDs actually used}} | {{state}} |
| output | {{EPIC-ID@revision}} | {{locator}} | {{digest}} | {{sections}} | draft |
| output | {{STORY-ID@revision}} | {{locator}} | {{digest}} | {{AC IDs}} | draft |

## Readiness, coverage, and what remains open

- **Ready stories:** {{IDs, and what makes each one ready}}
- **Blocked stories:** {{ID, the actual blocker, and who owns it}}
- **Requirement coverage:** {{covered IDs; uncovered IDs with their recorded deferral and reason}}
- **Dependency graph:** {{acyclic, or the cycle members}}
- **Unresolved decisions:** {{the behaviour nobody has defined, and who must define it}}
- **New proposals, kept separate from inherited requirements:** {{criteria you proposed that no
  supplied requirement supports}}
- **Capability gaps:** {{CAP IDs with no existing expert; named as gaps, never as installed packages}}

## Observed verification

| Check | Outcome | Raw evidence / external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| {{check}} | NOT_RUN | {{reference, or none}} | {{cause or limit}} |

`NOT_RUN` is planned and unattempted. `COULD_NOT_RUN` is a required observation that was blocked, with
its actual cause. `NOT_APPLICABLE` is a stated scope exclusion. The absence of an error is not a pass.
No DevForge command checks planning artifacts at this revision, so a graph, coverage or provenance
check recorded here is this skill's own reading unless an external receipt is named beside it.

## Continuation directory

| Order | Task | Owner / skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | {{one immediate next task}} | {{user / named skill / operator}} | {{required inputs or decisions}} | {{artifact or receipt}} |
| {{later}} | {{follow-on work if useful}} | {{owner}} | {{dependency}} | {{evidence}} |

## Copyable next task

Name an installed skill or write the task in plain language. Never write a slash command or a
`devforge` subcommand you have not confirmed exists — much of the roster is specified but not
implemented. Use absolute, resolvable paths for the receiving environment.

```text
Goal: {{one concrete result}}
Context: {{this handoff's saved path and the artifacts it names}}
Task: {{one authorized task and its scope}}
Preserve: {{decisions, constraints and prior evidence that must survive}}
Output: {{required results}} to {{assigned output directory}}
Stop at: {{completion, or the stated missing prerequisite}}
```

## Resume and custody

- **Task output readback:** {{completed output paths and digests, or none produced; excludes this handoff}}
- **This handoff's location:** {{saved path, or not yet persisted; no self-digest}}
- **This handoff's receipt:** compute its digest after saving and reading it back, then deliver the path
  and digest in the permitted outbox or the terminal response. Do not write that digest into this
  document.
- **Worktree ownership disposition:** {{retained / handed off / released, with the operator reference}}
- **External gate state:** {{actual receipt reference, or none; never an inferred phase}}
- **Conditions invalidating this handoff:** {{a cited upstream revision changes, a story is revised, an
  amendment is accepted, or the assignment changes}}

A prepared handoff is not a receiving invocation and not acceptance. This document authorizes no
development run, no installation, no external action, and no automatic invocation of a receiver.
