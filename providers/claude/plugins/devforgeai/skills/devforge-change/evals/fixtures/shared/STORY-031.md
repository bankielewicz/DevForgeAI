---
schema_version: "devforge.artifact/v1"
artifact_id: "STORY-031"
artifact_type: "story"
project_id: "tidepool"
revision: 2
status: accepted
created_at_utc: "2026-08-02T11:40:00Z"
producer:
  skill: "devforge-plan"
  skill_revision: "unknown (synthetic fixture)"
execution_ref: "SESSION-051@1"
upstream:
  - artifact_id: "ARCH-002"
    revision: 3
    store: "project"
    path: "docs/devforge/architecture/ARCH-002.md"
    sha256: "recompute from fixtures/shared/ARCH-002.md"
    sections: ["AR-03", "AR-04"]
evidence: []
supersedes: null
decision_ref: "USER-ADOPTION-2026-08-02"
missing_inputs: []
---

# STORY-031: Surface a rejected reconciliation to the surveyor

Synthetic fixture.

## Acceptance criteria

- AC-1: When the server rejects a reconciliation, the queued capture stays queued and is
  marked `needs_attention`.
- AC-2: The surveyor sees the server's stated reason, not a generic failure.
- AC-3: The client does not merge, re-order or resolve the conflicting captures. This is
  the client-side half of ARCH-002 AR-04.

## Expertise

Implemented with the `tide-sync` project expert (see XPKG-tide-sync).
