---
id: STORY-444
title: "Add Role Prompt to SKILL.md and ideate.md"
epic: EPIC-069
status: QA Approved
priority: High
points: 3
depends_on: []
type: documentation
created: 2026-02-18
sprint: Sprint-1
assigned_to: TBD
format_version: "2.9"
---

# Story: Add Role Prompt to SKILL.md and ideate.md

## Description

**As a** framework maintainer,
**I want** explicit role prompts added to the discovering-requirements skill per Anthropic `give-claude-a-role.md` guidance,
**so that** Claude adopts a domain-expert persona that improves output quality for requirements elicitation.

Addresses EPIC-069 audit findings:
- **4.1 (FAIL, High):** SKILL.md has no role prompt — Claude operates without domain persona
- **4.2 (FAIL, Medium):** ideate.md has no orchestrator role context

Adding "You are an expert Product Manager and Requirements Analyst..." role improves output quality per Anthropic's demonstrated examples. Currently neither SKILL.md nor ideate.md assigns Claude a domain persona.

---

## Acceptance Criteria

```xml
<acceptance_criteria id="AC1">
  <given>The discovering-requirements SKILL.md file exists</given>
  <when>A developer reads the file</when>
  <then>A "## Your Role" section exists after the execution model section (after ~line 47) containing an expert PM/requirements analyst persona definition</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#1: SKILL.md Contains Role Section

---

```xml
<acceptance_criteria id="AC2">
  <given>The ideate.md command file exists</given>
  <when>A developer reads the file</when>
  <then>The file contains orchestrator role context in its purpose/header section</then>
  <verification>
    <source_files>
      <file hint="Command file">src/claude/commands/ideate.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#2: ideate.md Contains Orchestrator Role Context

---

```xml
<acceptance_criteria id="AC3">
  <given>Role text has been added to both files</given>
  <when>The role text is reviewed</when>
  <then>The text references domain expertise including: stakeholder discovery, requirements elicitation, complexity assessment, and epic decomposition</then>
</acceptance_criteria>
```

### AC#3: Role Text References Domain Expertise

---

```xml
<acceptance_criteria id="AC4">
  <given>Role section has been added to SKILL.md</given>
  <when>The file line count is measured</when>
  <then>SKILL.md remains under 500 lines (currently 339, budget 161 lines for additions)</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#4: SKILL.md Under 500 Lines

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "SKILL.md Role Section"
      file_path: "src/claude/skills/discovering-requirements/SKILL.md"
      requirements:
        - id: "DOC-001"
          description: "Add ## Your Role section after execution model section (~line 47)"
          testable: true
          test_requirement: "Test: Grep for '## Your Role' header in SKILL.md"
          priority: "High"
        - id: "DOC-002"
          description: "Role text includes PM and requirements analyst persona"
          testable: true
          test_requirement: "Test: Grep for 'Product Manager' and 'Requirements Analyst' in role section"
          priority: "High"

    - type: "Configuration"
      name: "ideate.md Role Context"
      file_path: "src/claude/commands/ideate.md"
      requirements:
        - id: "DOC-003"
          description: "Add orchestrator role context in purpose/header section (~3 lines)"
          testable: true
          test_requirement: "Test: Grep for role context keywords in ideate.md"
          priority: "Medium"
```

---

## Definition of Done

### Implementation
- [x] SKILL.md contains `## Your Role` section after execution model section
- [x] ideate.md contains orchestrator role context in header section
- [x] Role text references all four domains: stakeholder discovery, requirements elicitation, complexity assessment, epic decomposition
- [x] SKILL.md line count remains under 500

### Quality
- [x] All 4 acceptance criteria verified
- [x] No regression in skill invocation (skill still loads and executes)

### Documentation
- [x] Role section follows Anthropic give-claude-a-role.md guidance pattern

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-18

- [x] SKILL.md contains `## Your Role` section after execution model section - Completed: Added "## Your Role" section at line 43 with expert PM/Requirements Analyst persona
- [x] ideate.md contains orchestrator role context in header section - Completed: Added "**Your Role:**" line at line 14 with orchestrator context
- [x] Role text references all four domains: stakeholder discovery, requirements elicitation, complexity assessment, epic decomposition - Completed: Both files reference all 4 domains
- [x] SKILL.md line count remains under 500 - Completed: 344 lines (156 lines headroom)
- [x] All 4 acceptance criteria verified - Completed: ac-compliance-verifier confirmed all 4 ACs PASS
- [x] No regression in skill invocation (skill still loads and executes) - Completed: Integration test verified structural integrity
- [x] Role section follows Anthropic give-claude-a-role.md guidance pattern - Completed: Uses "You are an expert [domain]..." pattern

### TDD Workflow Summary

- **Red:** 4 test files (9 assertions) — 3 failed as expected, 1 guard rail passed
- **Green:** Added role sections to both files — all 9 assertions pass
- **Refactor:** No refactoring needed (minimal documentation changes)

### Files Modified
- `src/claude/skills/discovering-requirements/SKILL.md` — Added "## Your Role" section (6 lines)
- `src/claude/commands/ideate.md` — Added "**Your Role:**" line (2 lines)

### Tests Created
- `tests/STORY-444/test_ac1_role_section_exists.sh`
- `tests/STORY-444/test_ac2_ideate_role_context.sh`
- `tests/STORY-444/test_ac3_four_domains_referenced.sh`
- `tests/STORY-444/test_ac4_skill_line_limit.sh`
- `tests/STORY-444/run_all_tests.sh`

---

## Notes

- Estimated ~10 lines added to SKILL.md, ~3 lines added to ideate.md
- Role prompt pattern: "You are an expert [domain expertise]..." per Anthropic examples
- This is a documentation-only change; no code files are modified
- Files to modify:
  - `src/claude/skills/discovering-requirements/SKILL.md`
  - `src/claude/commands/ideate.md`
