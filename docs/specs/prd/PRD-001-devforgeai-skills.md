---
id: PRD-001
type: prd
title: "DevForgeAI workflow skills"
status: draft
version: 2
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
upstream: []           # root document: no brainstorm preceded it
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "MVP"
stakeholders: ["Bryan"]
---

# PRD-001 — DevForgeAI workflow skills

## 1. Summary

DevForgeAI packages each step of its spec-driven workflow (brainstorm, PRD, epic, story,
specification) as an AI skill. Each skill produces a document that conforms to the DevForgeAI
templates and schemas, records its provenance, and leaves decisions to people. This PRD
currently covers only what the first skill, brainstorm, needs.

## 2. Problem and opportunity

Without skills, an AI agent asked to "brainstorm" or "write a PRD" improvises the structure each
time. The output drifts from the templates, invents IDs and links, and makes decisions (which
idea to pursue) that belong to the user. The templates and schemas define what correct output
looks like, and skills make agents produce it consistently.

## 3. Users and personas

The framework author, and later developers using DevForgeAI, working in Claude Code.

## 4. Goals and non-goals

**Goals**
- Planning documents written by AI agents are schema-valid, traceable and reviewable.

**Non-goals**
- Replacing human judgment on scope, priority or idea selection.
- Choosing the catalog of brainstorming frameworks (deferred; see FR-002).

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Share of skill-generated documents that pass devforgeai check on first write"
    baseline: "[NEEDS CLARIFICATION: no baseline until devforgeai check exists]"
    target: "at least 90%"
    measured_by: "devforgeai check results over generated documents"
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The framework shall provide a brainstorm skill that turns a user's topic into a BRN document conforming to the brainstorm template and schema."
    priority: must
    notes: null
  - id: FR-002
    status: active
    statement: "The brainstorm skill shall support brainstorming frameworks supplied as reference files, which the AI selects where appropriate, without changes to the skill's instructions."
    priority: must
    notes: "MVP delivers the extension point and one default framework; the framework catalog is chosen later."
  - id: FR-003
    status: active
    statement: "Skills shall record AI provenance in the documents they write and shall leave decisions to the user."
    priority: must
    notes: null
  - id: FR-004
    status: active
    statement: "Each workflow skill's handoff shall name the next workflow step and the document path that step consumes, and shall say when that step is not yet available."
    priority: must
    notes: "Brainstorm hands off to the PRD workflow, which consumes the BRN document."
```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    category: maintainability
    status: active
    statement: "Each SKILL.md body is at most 500 lines and its description at most 1024 characters; detailed material lives in reference files."
  - id: NFR-002
    category: compliance
    status: active
    statement: "Each skill conforms to the Agent Skills specification and validates against schemas/skill-frontmatter.schema.json and schemas/skill.schema.json."
  - id: NFR-003
    category: reliability
    status: active
    statement: "Each skill has a claude plugin eval suite run against the no-plugin baseline, and every case scores at least 0.8 over 3 runs."
```

## 8. User experience

Skills are invoked as plugin commands (`/devforgeai:<skill>`) or triggered automatically from
matching requests. They work conversationally and ask before deciding.

## 9. Constraints and dependencies

- Claude Code plugin and skill formats; `claude plugin eval` for behavioral tests.
- The `devforgeai` Rust CLI (not yet built) for structural validation.

## 10. Assumptions and risks

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "Packaging skills as a Claude Code plugin is acceptable for all intended users."
    validation: "Confirm with the framework author before the first release."
    state: open
```

## 11. Release and rollout

MVP: the brainstorm skill (EPIC-001). The workflow order is brainstorm → prd → epic → story → spec,
one skill each in the `devforgeai` plugin. The next skill, `prd`, consumes a BRN document and writes a PRD.

## 12. Open questions

- [NEEDS CLARIFICATION: which brainstorming frameworks join the catalog, and in what order]

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-22 | claude-code | Initial draft, scoped to the brainstorm skill | all |
| 2 | 2026-09-22 | claude-code | Added FR-004 (handoff names the next workflow step) | FR-004, §11 |
