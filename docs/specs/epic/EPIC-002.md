---
id: EPIC-002
type: epic
title: "PRD skill MVP"
status: draft
version: 3
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
  - {id: PRD-001, item: FR-005,  relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: FR-003,  relation: refines, version: 9, hash: null, note: "provenance and user decisions, applied to the PRD skill"}
  - {id: PRD-001, item: FR-004,  relation: refines, version: 9, hash: null, note: "handoff from prd to the architecture step (ADR-002)"}
  - {id: PRD-001, item: NFR-001, relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: NFR-002, relation: refines, version: 9, hash: null}
  - {id: PRD-001, item: NFR-003, relation: refines, version: 9, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- epic-specific ---
priority: must
target_release: "MVP"
---

# EPIC-002 — PRD skill MVP

## 1. Goal

A user runs `/devforgeai:prd` after a brainstorm and ends up with a schema-valid PRD. Every
requirement in it traces to a promoted brainstorm idea. Every decision in it (stage, operating
context, priority, release, scope) was made by the user or is visibly left open.

## 2. Business value

The PRD is where scope is decided. If the AI makes those decisions silently, every epic and story
built on the PRD inherits choices nobody made. If requirements don't trace to the brainstorm,
the chain from idea to test breaks at its second link.

## 3. Scope

**In scope**
- The `prd` skill in the `devforgeai` plugin, with its provenance record and eval suite.
- Selecting a BRN as input, writing a new PRD, or extending an existing one.
- An interview limited to what the BRN and the request don't answer.
- Scope maturity (stage), operating context, and priority and release per requirement, as user decisions.
- Architecture context read and classified (commitments, constraints, preferences, open decisions); design itself stays in ADRs.

**Out of scope**
- The architecture and `epic` skills. The PRD skill hands off to the architecture step (ADR-002).
- Architecture design, which belongs to the architecture step (ADR-002).
- The `devforgeai` CLI.

## 4. Done when

```yaml items
done_when:
  - id: DW-01
    status: active
    criterion: "From a converged BRN, /devforgeai:prd writes docs/specs/prd/PRD-NNN.md that validates against prd.schema.json, where every requirement cites a promoted idea and every stage, operating context, priority and release value was supplied by the user or is null."
    evidence_method: "claude plugin eval suite for the prd skill passes at threshold 0.8"
  - id: DW-02
    status: active
    criterion: "A second BRN can extend an existing PRD without renumbering or changing the meaning of any existing item."
    evidence_method: "Eval case extend-or-new plus a manual extension run"
```

## 5. Dependencies and risks

- The skill depends on the brainstorm skill's downstream contract (SPEC-001 §5), which is in place.
- PRD-001#ASM-01 (plugin packaging) is still open.

## 6. Technical notes (optional)

See SPEC-002.

## 7. Story map

<!-- GENERATED from stories whose upstream cites this epic. Do not edit by hand. -->

## 8. Open questions

- None beyond SPEC-002 §13.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-23 | claude-code | Initial draft |
| 2 | 2026-09-23 | claude-code | Operating context as a separate decision; architecture context read and classified |
| 3 | 2026-09-23 | claude-code | Handoff goes to the architecture step (ADR-002) |
