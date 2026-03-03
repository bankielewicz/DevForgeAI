---
id: STORY-445
title: "Create Multishot Examples Reference File"
epic: EPIC-069
status: QA Approved
priority: High
points: 8
depends_on: []
type: documentation
created: 2026-02-18
sprint: Sprint-1
assigned_to: DevForgeAI AI Agent
format_version: "2.9"
---

# Story: Create Multishot Examples Reference File

## Description

**As a** framework maintainer,
**I want** comprehensive multishot examples created for the discovering-requirements skill per Anthropic guidance,
**so that** Claude has concrete input/output examples that demonstrate expected quality and format for requirements elicitation workflows.

Addresses EPIC-069 audit findings:
- **5.1 (FAIL, High):** Zero input/output examples exist anywhere in the skill
- **5.2 (PARTIAL, Medium):** Output templates lack completed examples
- **5.5 (PARTIAL, Medium):** Domain-specific patterns lack usage examples

Create `references/examples.md` with 2-3 `<example>` tagged examples covering discovery sessions, epic decomposition, and complexity scoring. Add completed output template examples and domain pattern usage examples.

---

## Acceptance Criteria

```xml
<acceptance_criteria id="AC1">
  <given>The discovering-requirements skill references directory exists</given>
  <when>The examples file is created</when>
  <then>A new file src/claude/skills/discovering-requirements/references/examples.md exists containing 2-3 multishot examples wrapped in XML example tags</then>
  <verification>
    <source_files>
      <file hint="New examples file">src/claude/skills/discovering-requirements/references/examples.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#1: Examples File Exists with Multishot Examples

---

```xml
<acceptance_criteria id="AC2">
  <given>The examples.md file has been created</given>
  <when>The examples are reviewed</when>
  <then>Examples cover three scenarios: (a) discovery session (Phase 1), (b) epic decomposition (Phase 2), (c) complexity scoring (Phase 3)</then>
  <verification>
    <source_files>
      <file hint="New examples file">src/claude/skills/discovering-requirements/references/examples.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#2: Examples Cover Three Workflow Phases

---

```xml
<acceptance_criteria id="AC3">
  <given>Multishot examples exist in examples.md</given>
  <when>Each example is inspected</when>
  <then>Each example has input and output sections showing expected quality level</then>
</acceptance_criteria>
```

### AC#3: Each Example Has Input/Output Sections

---

```xml
<acceptance_criteria id="AC4">
  <given>The output-templates.md file exists</given>
  <when>A completed example is added</when>
  <then>output-templates.md contains at least one fully completed Completion Summary example with realistic data</then>
  <verification>
    <source_files>
      <file hint="Output templates">src/claude/skills/discovering-requirements/references/output-templates.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#4: Output Templates Has Completed Example

---

```xml
<acceptance_criteria id="AC5">
  <given>The domain-specific-patterns.md file exists</given>
  <when>A usage example section is added</when>
  <then>domain-specific-patterns.md contains a Usage Example section showing how patterns guide elicitation</then>
  <verification>
    <source_files>
      <file hint="Domain patterns">src/claude/skills/discovering-requirements/references/domain-specific-patterns.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#5: Domain Patterns Has Usage Example

---

```xml
<acceptance_criteria id="AC6">
  <given>The examples.md file has been created</given>
  <when>SKILL.md is reviewed</when>
  <then>SKILL.md references examples.md in relevant phase instructions with Read() directives</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#6: SKILL.md References Examples File

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "Multishot Examples Reference"
      file_path: "src/claude/skills/discovering-requirements/references/examples.md"
      requirements:
        - id: "DOC-001"
          description: "Create new file with 2-3 multishot examples using XML example tags"
          testable: true
          test_requirement: "Test: File exists and contains <example> XML tags"
          priority: "High"
        - id: "DOC-002"
          description: "Each example covers a distinct workflow phase (discovery, decomposition, scoring)"
          testable: true
          test_requirement: "Test: Grep for Phase 1, Phase 2, Phase 3 example headers"
          priority: "High"
        - id: "DOC-003"
          description: "Each example has <input> and <output> sections"
          testable: true
          test_requirement: "Test: Grep for <input> and <output> tags in examples.md"
          priority: "High"

    - type: "Configuration"
      name: "Output Templates Enhancement"
      file_path: "src/claude/skills/discovering-requirements/references/output-templates.md"
      requirements:
        - id: "DOC-004"
          description: "Add completed Completion Summary example with realistic data"
          testable: true
          test_requirement: "Test: Grep for completed example section in output-templates.md"
          priority: "Medium"

    - type: "Configuration"
      name: "Domain Patterns Enhancement"
      file_path: "src/claude/skills/discovering-requirements/references/domain-specific-patterns.md"
      requirements:
        - id: "DOC-005"
          description: "Add Usage Example section showing pattern-guided elicitation"
          testable: true
          test_requirement: "Test: Grep for 'Usage Example' section in domain-specific-patterns.md"
          priority: "Medium"

    - type: "Configuration"
      name: "SKILL.md Reference Pointers"
      file_path: "src/claude/skills/discovering-requirements/SKILL.md"
      requirements:
        - id: "DOC-006"
          description: "Add Read() references to examples.md in relevant phase instructions"
          testable: true
          test_requirement: "Test: Grep for 'examples.md' reference in SKILL.md"
          priority: "High"
```

---

## Definition of Done

### Implementation
- [x] New file `src/claude/skills/discovering-requirements/references/examples.md` created with 2-3 examples
- [x] Examples use `<example>`, `<input>`, and `<output>` XML tags per Anthropic format
- [x] Examples cover discovery session, epic decomposition, and complexity scoring
- [x] `output-templates.md` updated with completed Completion Summary example
- [x] `domain-specific-patterns.md` updated with Usage Example section
- [x] SKILL.md updated with Read() references to examples.md

### Quality
- [x] All 6 acceptance criteria verified
- [x] SKILL.md references load correctly (file paths valid)
- [x] No regression in skill invocation

### Documentation
- [x] Examples follow Anthropic multishot example format with XML tags

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-18

- [x] New file `src/claude/skills/discovering-requirements/references/examples.md` created with 2-3 examples - Completed: Created 306-line file with 3 multishot examples (discovery-session-saas, epic-decomposition-saas, complexity-scoring-saas) using XML example/input/output tags
- [x] Examples use `<example>`, `<input>`, and `<output>` XML tags per Anthropic format - Completed: All 3 examples use `<example name="...">` wrapper with nested `<input>` and `<output>` tags
- [x] Examples cover discovery session, epic decomposition, and complexity scoring - Completed: Phase 1 (problem statement, personas, scope), Phase 2 (6 epics with features/points), Phase 3 (38/60 score breakdown)
- [x] `output-templates.md` updated with completed Completion Summary example - Completed: Added "Completed Completion Summary Example" section with realistic SaaS data (6 epics, 198 total points, 38/60 complexity)
- [x] `domain-specific-patterns.md` updated with Usage Example section - Completed: Added "Usage Example" section demonstrating SaaS pattern-guided elicitation with feature checklist, gap analysis table, and regulatory considerations
- [x] SKILL.md updated with Read() references to examples.md - Completed: Added Read() directive in Phase overview (line 99) and "Multishot Examples (1 file)" entry in Reference Files section
- [x] All 6 acceptance criteria verified - Completed: AC compliance verifier confirmed all 6 ACs PASS with HIGH confidence
- [x] SKILL.md references load correctly (file paths valid) - Completed: Integration tester verified all cross-file references resolve correctly
- [x] No regression in skill invocation - Completed: SKILL.md retains all 19 original sections with 11 Read() directives
- [x] Examples follow Anthropic multishot example format with XML tags - Completed: Consistent XML tag structure throughout examples.md

### TDD Workflow Summary

- **Red:** 20 tests written (14 failing, 6 passing pre-existing conditions)
- **Green:** All 20 tests passing after implementation
- **Refactor:** Documentation reviewed by refactoring-specialist and code-reviewer — approved with no blocking issues

---

## Notes

- This is the highest-point story in the epic due to content creation effort
- New file: `src/claude/skills/discovering-requirements/references/examples.md`
- Edited files:
  - `src/claude/skills/discovering-requirements/references/output-templates.md`
  - `src/claude/skills/discovering-requirements/references/domain-specific-patterns.md`
  - `src/claude/skills/discovering-requirements/SKILL.md`
- Anthropic multishot format uses `<example>` with nested `<input>` / `<output>` XML tags
- Examples should demonstrate realistic requirements elicitation scenarios, not toy examples
