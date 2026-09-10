---
schema_version: "devforge.artifact/v1"
artifact_id: "XPKG-004"
artifact_type: "expert-package"
project_id: "tidepool"
revision: 2
status: accepted
created_at_utc: "2026-08-06T08:20:00Z"
producer:
  skill: "devforge-project-expert-creator"
  skill_revision: "unknown (synthetic fixture)"
execution_ref: "SESSION-052@1"
upstream:
  - artifact_id: "ARCH-002"
    revision: 3
    store: "project"
    path: "docs/devforge/architecture/ARCH-002.md"
    sha256: "recompute from fixtures/shared/ARCH-002.md"
    sections: ["AR-03", "AR-04", "AR-05"]
evidence: []
supersedes: null
decision_ref: null
missing_inputs: []
---

# Expert package record: tide-sync

Synthetic fixture.

## Canonical and generated copies

| Purpose | Path | Identity |
| --- | --- | --- |
| Canonical source | `experts/tide-sync/` | manifest below |
| Installed project copy | `.claude/skills/tide-sync/` | generated 2026-08-06; not re-generated since |

## File manifest

| Package-relative path | SHA-256 |
| --- | --- |
| `SKILL.md` | `a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90` |
| `references/reconciliation.md` | `112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00` |

## Carried decisions

- ARCH-002 AR-04: the client never resolves a conflict. Every worked example in
  `references/reconciliation.md` is written against that rule.
- `tidepool-sync` 2.4.1: the version-specific API examples target that release.

Behavioural status: NOT_EVALUATED by this record. See EVREPORT-007.
