---
id: EPIC-003
type: epic
title: "Adaptive foundations"
status: draft
version: 1
created: 2026-09-23
updated: 2026-09-23
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
  - {id: PRD-001, item: FR-006, relation: refines, version: 4, hash: null}
  - {id: PRD-001, item: FR-007, relation: refines, version: 4, hash: null}
  - {id: PRD-001, item: FR-008, relation: refines, version: 4, hash: null}
  - {id: PRD-001, item: FR-009, relation: refines, version: 4, hash: null}
  - {id: ADR-003, relation: informed_by, version: 1, hash: null, note: "proposed: the design this epic delivers"}
supersedes: []
superseded_by: null
blocked_by: []
# --- epic-specific ---
priority: null
target_release: "MVP"
---

# EPIC-003 — Adaptive foundations

## 1. Goal

Core workflows read organization and project policy through configuration contract v1. They resolve
conflicts by defined rules, record which policy informed each document, and give different,
source-cited results for different organizations, all without editing the core workflow.

## 2. Business value

This is what makes DevForgeAI adaptive rather than one-size-fits-all. Building it before most workflows
exist means each new workflow reads settings instead of hardcoding them.

## 3. Scope

**In scope**
- Configuration contract v1: `policy.schema.json`, the policy template, and three settings (ADR-003 A3).
- Policy resolution in the prd skill (STORY-002).
- The two-organization demonstration in the Architecture Definition workflow (future SPEC-003).

**Out of scope**
- Experts and custom workflows (PRD-001 FR-010 and FR-011, later).
- Synchronizing organization policy across repositories.

## 4. Done when

```yaml items
done_when:
  - id: DW-01
    status: active
    criterion: "The prd skill applies approved policy settings, stops on invalid, contradictory or disallowed settings, and records the settings it used or that framework defaults were used."
    evidence_method: "prd eval cases for applied, invalid and missing policy pass at threshold 0.8"
  - id: DW-02
    status: active
    criterion: "The Architecture Definition workflow gives appropriately different, source-cited results for Organization A and Organization B from the same PRD, with no change under src/ between the runs."
    evidence_method: "The ADR-003 demonstration, run as SPEC-003's eval cases"
```

## 5. Dependencies and risks

- DW-02 depends on the Architecture Definition skill (ADR-002), which isn't specified yet, so DW-02 has no satisfying story yet.
- ADR-002 and ADR-003 are still proposed.

## 6. Technical notes (optional)

See ADR-003.

## 7. Story map

<!-- GENERATED from stories whose upstream cites this epic. Do not edit by hand. -->

## 8. Open questions

- None beyond ADR-003.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-23 | claude-code | Initial draft |
