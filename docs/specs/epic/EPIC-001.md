---
id: EPIC-001
type: epic
title: "Brainstorm skill MVP"
status: draft
version: 1
created: 2026-09-22
updated: 2026-09-22
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
  - {id: PRD-001, item: FR-001,  relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: FR-002,  relation: refines, version: 9, hash: null, note: "partial: extension point and one default framework only"}
  - {id: PRD-001, item: FR-003,  relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: FR-004,  relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: NFR-001, relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: NFR-002, relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: NFR-003, relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: SM-01,   relation: informed_by, version: 9, hash: null, note: "brainstorm documents are the first measured artifacts"}
supersedes: []
superseded_by: null
blocked_by: []
# --- epic-specific ---
priority: must
target_release: "MVP"
---

# EPIC-001 — Brainstorm skill MVP

## 1. Goal

A user can say "let's brainstorm <topic>" in Claude Code and end up with a schema-valid BRN
document. The ideas in it are captured, evaluated and dispositioned, and every decision was
confirmed by the user.

## 2. Business value

The brainstorm is the root of the provenance chain. If the root is unstructured, every PRD
requirement that derives from it cites nothing reliable.

## 3. Scope

**In scope**
- The `brainstorm` skill in the `devforgeai` plugin, with its provenance record and eval suite.
- The extension point for brainstorming frameworks, plus one default framework.

**Out of scope**
- The catalog of additional brainstorming frameworks (a later epic).
- The `devforgeai` CLI itself. The skill uses it when present and falls back otherwise.

## 4. Done when

```yaml items
done_when:
  - id: DW-01
    status: active
    criterion: "From a topic, /devforgeai:brainstorm produces a BRN document that validates against brainstorm.schema.json, with every disposition confirmed by the user."
    evidence_method: "claude plugin eval suite for the skill passes at threshold 0.8"
  - id: DW-02
    status: active
    criterion: "A new brainstorming framework can be added as a reference file plus an index entry, with no change to SKILL.md."
    evidence_method: "Add a test framework file and confirm the skill selects it"
```

## 5. Dependencies and risks

- Plugin packaging (PRD-001#ASM-01) is still an open assumption.

## 6. Technical notes (optional)

See SPEC-001.

## 7. Story map

<!-- GENERATED from stories whose upstream cites this epic. Do not edit by hand. -->

## 8. Open questions

- None beyond PRD-001 §12.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-22 | claude-code | Initial draft |
