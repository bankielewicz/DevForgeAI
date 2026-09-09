---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-{{number}}"
artifact_type: "handoff"
project_id: "{{project_id}}"
revision: 1
status: draft
created_at_utc: "{{ISO-8601-UTC-time}}"
producer:
  skill: "{{producing-skill}}"
  skill_revision: "{{exact-producer-revision-or-digest}}"
execution_ref: "{{SESSION-ID}}@{{revision}}"
upstream: []
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Skill handoff

## You are here [STATE-001]

- Skill and use case: {{name and goal}}
- Current phase: {{phase}}
- Task state: {{complete / partial / blocked; distinguish from document status}}
- Session/worktree assignment: {{external SESSION reference}}
- Exact candidate or artifact scope: {{identity}}
- Existing authorization carried forward: {{reference}}

## Inputs consumed and outputs produced [IO-001]

List consumed inputs and completed task outputs here. Exclude this handoff itself: it cannot contain its own complete-byte digest. When no task artifact was produced, say so instead of inventing an output row. Hash each listed file only after its bytes are complete.

| Direction | Artifact ID/revision | Store/path | SHA-256 | Relevant sections | Decision/freshness state |
| --- | --- | --- | --- | --- | --- |
| input | {{identity}} | {{locator}} | {{digest}} | {{IDs}} | {{state}} |
| output | {{identity}} | {{locator}} | {{digest}} | {{IDs}} | {{state}} |

## What changed and what remains open [CHANGES-001]

{{Concrete outcome, new proposals versus adopted decisions, unresolved questions, and work not completed.}}

## Observed verification [VERIFY-001]

| Check | Outcome | Raw evidence / external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| {{check}} | NOT_RUN | {{reference}} | {{cause/limit}} |

## Continuation directory [NEXT-001]

| Order | Task | Owner / skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | {{one immediate next task}} | {{user / skill / external operator}} | {{required inputs or decisions}} | {{artifact/receipt}} |

## Copyable next-session prompt [PROMPT-001]

Goal: {{one concrete result}}
Context: {{exact artifact references and the relevant sections}}
Output: {{named template/deliverable and permitted destination}}
Boundaries: {{assigned worktree/fence, existing decisions, and consequential limits}}
Verify: {{observable completion checks}}

Use an actual installed skill name or known command. If the capability is not implemented, make the next task authoring/evaluation of that capability; do not present a fictional command as runnable.

## Resume and custody [CUSTODY-001]

- Task output readback: {{completed task-output paths and digests, or none produced; exclude this handoff}}
- This handoff's location: {{saved path, or not yet persisted; no self-digest}}
- This handoff's external receipt: compute its digest after saving and reading it back; deliver the path and digest in the permitted outbox or terminal response. Do not insert that digest into this document or modify this document to record the later receipt.
- Worktree ownership disposition: {{retained / handed off / released with operator reference}}
- External gate state: {{actual receipt reference, not an inferred phase}}
- Conditions invalidating this handoff: {{source, candidate, runtime, or assignment changes}}
