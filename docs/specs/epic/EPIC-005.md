---
id: EPIC-005
type: epic
title: "Epic skill MVP"
status: draft
version: 1
created: 2026-09-24
updated: 2026-09-24
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "a2b1015f-3340-4c70-80ed-b674d486fadd"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {id: PRD-001, item: FR-014,  relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: FR-003,  relation: refines, version: 9, hash: null, note: "grouping is confirmed by the user; provenance recorded on every epic"}
  - {id: PRD-001, item: FR-004,  relation: refines, version: 9, hash: null, note: "handoff from the epic step to the story step"}
  - {id: PRD-001, item: NFR-001, relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: NFR-002, relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: NFR-003, relation: refines, version: 9, hash: null}
  - {id: ADR-002, relation: informed_by, version: 2, hash: null, note: "accepted: epics come after the Architecture Definition step"}
supersedes: []
superseded_by: null
blocked_by: []
# --- epic-specific ---
priority: must
target_release: "MVP"
---

# EPIC-005 — Epic skill MVP

## 1. Goal

A user runs `/devforgeai:epic PRD-NNN` and gets epic documents for exactly the requirements that are
ready for epic work and in the current release, grouped the way the user confirmed. Every requirement
left out is reported with its reason: blocked by an open architectural question, released later,
won't have, undecided, or already covered by an existing epic.

## 2. Business value

Epics are where work is split for delivery. An epic written for a requirement that is still blocked
starts work on an undecided foundation, which the Architecture Definition step exists to prevent
(ADR-002). This skill is the first consumer of SPEC-003's readiness rule, so it makes that rule
effective instead of advisory.

## 3. Scope

**In scope**
- The `epic` skill and its eval suite. The epic template moves from `src/staging/templates/` into the skill.
- Selecting requirements by readiness (read from the ARCH file) and by the current release.
- Proposing how to group them into epics, with the user's confirmation before anything is written.
- Reporting every requirement not included, and handing off to the story step.

**Out of scope**
- Writing stories, sprint planning, and modifying existing epics.
- Organizational policy (PRD-001 FR-012, release later).
- The `devforgeai check` CLI branch; the skill validates with its own self-check list.

## 4. Done when

```yaml items
done_when:
  - id: DW-01
    status: active
    criterion: "From a PRD with an ARCH, /devforgeai:epic writes schema-valid epics whose refines links name only requirements that are ready under SPEC-003 §4 (read from the ARCH file) and in the current release, and it reports every other requirement with its reason."
    evidence_method: "epic eval suite passes at threshold 0.8, including the negative selection cases graded on the written files"
  - id: DW-02
    status: active
    criterion: "Existing epics are never modified or duplicated: a requirement an existing epic already refines is reported as covered and gets no new epic."
    evidence_method: "Eval case existing-epic-not-duplicated"
```

## 5. Dependencies and risks

- Depends on the architecture skill's downstream contract (SPEC-003 §4 and §5): the ARCH path, stable
  DEC IDs, and the readiness rule. The architecture skill's reply is advisory; this skill reads the file.
- Risk: the architecture skill misreported readiness in its reply once in 3 v4 runs (STORY-004 AC-04).
  This skill computes readiness from the ARCH file itself, so that failure mode doesn't carry over.
- Shipping this skill makes the architecture skill's `hands-off-to-epic` "not built yet" check fail, as
  happened to prd's handoff check. SPEC-003 VER-10 needs an approved change during the build.

## 6. Technical notes (optional)

- MoSCoW priority orders the epics (Must, then Should, then Could); it never selects them.
  `release: current` selects. A `null` priority or release is undecided and is reported to the PRD owner.

## 7. Story map

<!-- GENERATED from stories whose upstream cites this epic. -->

## 8. Open questions

- None.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-24 | claude-code | Initial draft |
