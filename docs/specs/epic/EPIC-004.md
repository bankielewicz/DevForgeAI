---
id: EPIC-004
type: epic
title: "Architecture Definition skill MVP"
status: draft
version: 1
created: 2026-09-23
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
  - {id: PRD-001, item: FR-013,  relation: refines, version: 8, hash: null}
  - {id: PRD-001, item: FR-003,  relation: refines, version: 8, hash: null, note: "decisions stay the user's; outcome confirmation is not decision acceptance"}
  - {id: PRD-001, item: FR-004,  relation: refines, version: 8, hash: null, note: "handoff from architecture to the epic workflow"}
  - {id: PRD-001, item: FR-006,  relation: refines, version: 8, hash: null, note: "partial: the Architecture Definition half of the initial rollout"}
  - {id: PRD-001, item: FR-007,  relation: refines, version: 8, hash: null, note: "partial: the Architecture Definition half of the initial rollout"}
  - {id: PRD-001, item: FR-008,  relation: refines, version: 8, hash: null, note: "partial: the Architecture Definition half of the initial rollout"}
  - {id: PRD-001, item: NFR-001, relation: refines, version: 8, hash: null}
  - {id: PRD-001, item: NFR-002, relation: refines, version: 8, hash: null}
  - {id: PRD-001, item: NFR-003, relation: refines, version: 8, hash: null}
  - {id: ADR-002, relation: informed_by, version: 2, hash: null, note: "accepted: the step this skill performs"}
supersedes: []
superseded_by: null
blocked_by: []
# --- epic-specific ---
priority: must
target_release: "MVP"
---

# EPIC-004 — Architecture Definition skill MVP

## 1. Goal

A user runs `/devforgeai:architecture PRD-NNN` and gets an architecture description (ARCH) and
ADRs. The questions that separate epics must share are identified and settled only by explicit
decisions, and the user learns exactly which requirements are ready for epic work and which are blocked, and by what.

## 2. Business value

Shared foundations decided once, before work splits, instead of separately and incompatibly per story.
It also hosts the two-organization demonstration that adaptation works (EPIC-003 DW-02).

## 3. Scope

**In scope**
- The `architecture` skill, the ARCH document type, and its eval suite.
- Selecting an existing ARCH to reuse or amend, or creating one.
- Bounded, read-only inspection of named components or directories.
- Decision-specific readiness, and handing requirement changes back to the PRD owner.

**Out of scope**
- Experts, exhaustive code indexing, and detailed feature design (API fields, migrations, class structures).
- The epic skill.

## 4. Done when

```yaml items
done_when:
  - id: DW-01
    status: active
    criterion: "From a PRD, /devforgeai:architecture writes a schema-valid ARCH whose architectural questions each cite the requirements they affect, and a requirement is reported ready only when every blocking question citing it is resolved by an accepted, non-superseded ADR or an approved, active policy setting."
    evidence_method: "architecture eval suite passes at threshold 0.8, including the negative readiness cases"
  - id: DW-02
    status: active
    criterion: "With an existing ARCH for the same system, the skill proposes reusing or amending it and never creates a second baseline without the user's choice."
    evidence_method: "Eval case existing-arch-not-duplicated"
```

## 5. Dependencies and risks

- Depends on the prd skill's downstream contract (SPEC-002 §5), including `[NEEDS ADR]` markers.
- The epic skill isn't specified yet; readiness is reported now and enforced when it exists.

## 6. Technical notes (optional)

See SPEC-003.

## 7. Story map

<!-- GENERATED from stories whose upstream cites this epic. Do not edit by hand. -->

## 8. Open questions

- None beyond SPEC-003 §13.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-23 | claude-code | Initial draft |
| 1 | 2026-09-24 | claude-code | Priority must (Bryan), recorded after delivery; links re-reviewed at PRD-001 v8 |
