---
schema_version: "devforge.artifact/v1"
artifact_id: "HANDOFF-001"
artifact_type: "handoff"
project_id: "shiftline"
revision: 1
status: draft
created_at_utc: "2026-09-02T10:41:00Z"
producer:
  skill: "devforge-plan"
  skill_revision: "unknown (synthetic fixture; no installed skill produced these bytes)"
execution_ref: null
upstream:
  - artifact_id: PROD-001
    revision: 2
    store: project
    path: docs/devforge/product/PROD-001.md
    sha256: "6a24a663b0472fdbb1eab071c02abc744d8c3d817a08627c07bb1056c2775d14"
    sections:
      - REQ-001
      - REQ-004
  - artifact_id: ARCH-001
    revision: 2
    store: project
    path: docs/devforge/architecture/ARCH-001.md
    sha256: "107ce6fab5b5b944fd0f7b66c8c342f007c7ad2132b6f83aa1e4b3ede50da427"
    sections:
      - RULE-003
      - RULE-006
      - CAP-001
      - CAP-002
evidence: []
supersedes: null
decision_ref: null
missing_inputs:
  - "REQ-004 denial behaviour; owner is the coordinator"
  - "No session assignment record was supplied, so execution_ref is null"
---

# Planning handoff: Shiftline self-service swaps

**Synthetic fixture.** A conforming handoff. It does not list itself among its own outputs and carries
no digest of itself.

## You are here

- **Skill and use case:** devforge-plan — derive epics and implementable stories from adopted scope.
- **Result:** partial. One epic and one authored story; four stories allocated and not yet authored.
- **Delivery slice and non-goals:** PROD-001@2 self-service swaps. Non-goals: shift creation, onboarding,
  payroll export, push notifications, multi-site coordination.
- **Session/worktree assignment:** null — no assignment record was supplied.
- **Existing authorization carried forward:** the user's 2026-08-19 adoption of PROD-001.

## Inputs consumed and outputs produced

| Direction | Artifact ID/revision | Store/path | SHA-256 | Relevant sections | Decision/freshness state |
| --- | --- | --- | --- | --- | --- |
| input | PROD-001@2 | project: docs/devforge/product/PROD-001.md | 6a24a663b0472fdbb1eab071c02abc744d8c3d817a08627c07bb1056c2775d14 | REQ-001..REQ-005, NFR-001 | accepted; current |
| input | ARCH-001@2 | project: docs/devforge/architecture/ARCH-001.md | 107ce6fab5b5b944fd0f7b66c8c342f007c7ad2132b6f83aa1e4b3ede50da427 | ADR-002, RULE-003..006, API-001, CAP-001, CAP-002 | accepted; current |
| input | UX-001@1 | project: docs/devforge/design/UX-001.md | 8718c7d728ebfe51040001ed8c068d672e55e7bb85994767be292ec9cdc97eb7 | FLOW-001 | **proposed**; not adopted |
| output | EPIC-001@1 | project: docs/devforge/epics/EPIC-001.md | e435c589f437c81fc1829b098c515eec1aab783efff8b5d98ad2d037005ba5ee | all | draft |
| output | STORY-001@1 | project: docs/devforge/stories/STORY-001.md | 77bcc7b8d9738e65e82b91bc2097a6bf6355b7319d955b56299303b72ceb5df2 | AC-001..AC-004 | draft |

## Readiness, coverage, and what remains open

- **Ready stories:** STORY-001 — references resolve, four observable criteria, scope and test policy declared
- **Blocked stories:** STORY-004 — REQ-004's denial behaviour is undefined; the coordinator owns it
- **Requirement coverage:** REQ-001, REQ-002, REQ-003, REQ-005 and NFR-001 covered; REQ-004 covered by a
  blocked story with its open question recorded
- **Dependency graph:** acyclic — STORY-001 → STORY-002 → {STORY-003, STORY-004, STORY-005}
- **Unresolved decisions:** whether an ineligible volunteer sees an offer at all or is refused on claim
- **New proposals, kept separate from inherited requirements:** none authored; UX-001's withdraw path was
  read and left out because no requirement supports it
- **Capability gaps:** CAP-001 and CAP-002 are declared needs. No expert package covering either was
  observed, so both stand as gaps.

## Observed verification

| Check | Outcome | Raw evidence / external receipt | Cause or scope limit |
| --- | --- | --- | --- |
| Upstream references resolve to the cited digests | PASS | recomputed against the two input files | This skill's own reading; no external receipt exists |
| Dependency graph acyclic | PASS | the five edges above | This skill's own reading |
| Requirement coverage accounted for | PASS | EPIC-001 coverage table | This skill's own reading |
| DevForge planning-artifact check | COULD_NOT_RUN | none | No DevForge command inspects an epic or story at this revision |
| Behavioral evaluation of any produced story | NOT_RUN | none | Out of this skill's scope |

## Continuation directory

| Order | Task | Owner / skill | Prerequisites | Completion evidence |
| --- | --- | --- | --- | --- |
| 1 | Answer REQ-004's denial behaviour | Coordinator (user) | none | A recorded decision reference |
| 2 | Author STORY-002, STORY-003, STORY-005 | devforge-plan | none | Three story documents |
| 3 | Create expertise for CAP-001 and CAP-002 | devforge-project-expert-creator, if installed | STORY-001 | An expert specification and candidate package |

## Copyable next task

```text
Goal: STORY-002, STORY-003 and STORY-005 authored against EPIC-001@1.
Context: this handoff at docs/devforge/handoffs/HANDOFF-001.md, and the two inputs it names.
Task: author the three allocated stories. Do not reopen REQ-004; STORY-004 stays blocked.
Preserve: EPIC-001's coverage table, STORY-001's AC IDs, and the non-goals above.
Output: three story documents to docs/devforge/stories/ plus an updated handoff.
Stop at: the three stories, or the first one whose acceptance behaviour is undefined.
```

## Resume and custody

- **Task output readback:** EPIC-001 and STORY-001 at the paths and digests above; excludes this handoff
- **This handoff's location:** docs/devforge/handoffs/HANDOFF-001.md; no self-digest
- **This handoff's receipt:** computed after saving and delivered in the terminal response
- **Worktree ownership disposition:** not applicable — no assignment record
- **External gate state:** none
- **Conditions invalidating this handoff:** a new PROD-001 or ARCH-001 revision, any story revision, or
  an accepted amendment

A prepared handoff is not a receiving invocation and not acceptance.
