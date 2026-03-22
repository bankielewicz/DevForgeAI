---
id: STORY-446
title: "Fix YAML Frontmatter Compliance"
epic: EPIC-069
status: QA Approved
priority: Medium
points: 3
depends_on: []
type: documentation
created: 2026-02-18
sprint: Sprint-1
assigned_to: TBD
format_version: "2.9"
---

# Story: Fix YAML Frontmatter Compliance

## Description

**As a** framework maintainer,
**I want** YAML frontmatter in the discovering-requirements skill files to comply with the Anthropic Agent Skills spec,
**so that** tools parsing skill metadata get correct, spec-conformant values.

Addresses EPIC-069 audit findings:
- **1.1 (FAIL, High):** `allowed-tools` is a YAML array instead of space-delimited string
- **1.2 (FAIL, Medium):** `allowed-tools` uses non-spec tool names (`Bash(git:*)` instead of `Bash`, `Skill` instead of `Task`)
- **1.3 (PARTIAL, Medium):** ideate.md uses comma-delimited instead of space-delimited tools
- **1.5 (FAIL, Medium):** Missing `metadata:` section (author, version, category)
- **7.5 (PARTIAL, Low):** Minor formatting inconsistencies
- **1.4/1.6 (PARTIAL, Low):** Inconsistent `model` field format

Quick fixes — estimated 30 minutes total.

---

## Acceptance Criteria

```xml
<acceptance_criteria id="AC1">
  <given>SKILL.md frontmatter contains allowed-tools as a YAML array</given>
  <when>The frontmatter is updated</when>
  <then>allowed-tools is a space-delimited string (e.g., "Read Write Glob Grep Bash Task")</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#1: SKILL.md allowed-tools Is Space-Delimited String

---

```xml
<acceptance_criteria id="AC2">
  <given>SKILL.md allowed-tools contains non-spec tool names</given>
  <when>The tool names are corrected</when>
  <then>allowed-tools uses only spec-recognized names: Bash (not Bash(git:*)), Task (not Skill)</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#2: SKILL.md Uses Spec-Recognized Tool Names

---

```xml
<acceptance_criteria id="AC3">
  <given>ideate.md frontmatter uses comma-delimited allowed-tools</given>
  <when>The frontmatter is updated</when>
  <then>ideate.md allowed-tools is space-delimited (not comma-delimited)</then>
  <verification>
    <source_files>
      <file hint="Command file">src/claude/commands/ideate.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#3: ideate.md allowed-tools Is Space-Delimited

---

```xml
<acceptance_criteria id="AC4">
  <given>SKILL.md frontmatter lacks a metadata section</given>
  <when>The metadata section is added</when>
  <then>SKILL.md includes a metadata: section with author, version, and category fields</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/discovering-requirements/SKILL.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#4: SKILL.md Includes Metadata Section

---

```xml
<acceptance_criteria id="AC5">
  <given>model field format differs between SKILL.md and ideate.md</given>
  <when>The model fields are normalized</when>
  <then>model field uses consistent format across both files</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/discovering-requirements/SKILL.md</file>
      <file hint="Command file">src/claude/commands/ideate.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### AC#5: Consistent Model Field Format

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "SKILL.md Frontmatter Fix"
      file_path: "src/claude/skills/discovering-requirements/SKILL.md"
      requirements:
        - id: "DOC-001"
          description: "Convert allowed-tools from YAML array to space-delimited string"
          testable: true
          test_requirement: "Test: Verify allowed-tools line is a quoted string, not array syntax"
          priority: "High"
        - id: "DOC-002"
          description: "Replace non-spec tool names (Bash(git:*) → Bash, Skill → Task)"
          testable: true
          test_requirement: "Test: Grep for disallowed tool name patterns in frontmatter"
          priority: "High"
        - id: "DOC-003"
          description: "Add metadata: section with author, version, category"
          testable: true
          test_requirement: "Test: Grep for 'metadata:' key in SKILL.md frontmatter"
          priority: "Medium"
        - id: "DOC-004"
          description: "Normalize model field format"
          testable: true
          test_requirement: "Test: Compare model field format between SKILL.md and ideate.md"
          priority: "Low"

    - type: "Configuration"
      name: "ideate.md Frontmatter Fix"
      file_path: "src/claude/commands/ideate.md"
      requirements:
        - id: "DOC-005"
          description: "Convert allowed-tools from comma-delimited to space-delimited"
          testable: true
          test_requirement: "Test: Verify no commas in allowed-tools value"
          priority: "Medium"
        - id: "DOC-006"
          description: "Normalize model field to match SKILL.md format"
          testable: true
          test_requirement: "Test: Model field format matches SKILL.md"
          priority: "Low"
```

---

## Definition of Done

### Implementation
- [x] SKILL.md `allowed-tools` converted to space-delimited string
- [x] SKILL.md tool names corrected to spec-recognized names only
- [x] ideate.md `allowed-tools` converted to space-delimited format
- [x] SKILL.md includes `metadata:` section with author, version, category
- [x] `model` field format is consistent across both files

### Quality
- [x] All 5 acceptance criteria verified
- [x] Frontmatter validates against Agent Skills spec format
- [x] No duplicate tools in allowed-tools lists
- [x] No regression in skill invocation

### Documentation
- [x] Changes align with Anthropic Agent Skills specification

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-18

- [x] SKILL.md `allowed-tools` converted to space-delimited string - Completed: Converted YAML array (10 items) to quoted space-delimited string
- [x] SKILL.md tool names corrected to spec-recognized names only - Completed: Bash(git:*) → Bash, Skill → Task, TodoWrite removed
- [x] ideate.md `allowed-tools` converted to space-delimited format - Completed: Comma-delimited → quoted space-delimited string, Skill → Task
- [x] SKILL.md includes `metadata:` section with author, version, category - Completed: Added metadata block with author: DevForgeAI, version: "1.0", category: requirements
- [x] `model` field format is consistent across both files - Completed: Normalized SKILL.md from claude-opus-4-6 to opus (matching ideate.md)
- [x] All 5 acceptance criteria verified - Completed: ac-compliance-verifier confirmed all 5 ACs pass
- [x] Frontmatter validates against Agent Skills spec format - Completed: Space-delimited strings, spec-recognized names
- [x] No duplicate tools in allowed-tools lists - Completed: Verified no duplicates in either file
- [x] No regression in skill invocation - Completed: Integration tests confirm skill reference intact
- [x] Changes align with Anthropic Agent Skills specification - Completed: All changes per EPIC-069 audit findings

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✅ | 5 test files, 13 assertions - all FAIL |
| Phase 03 (Green) | ✅ | Frontmatter fixes applied - all 13 assertions PASS |
| Phase 04 (Refactor) | ✅ | No refactoring needed (config changes only) |
| Phase 05 (Integration) | ✅ | YAML parsing valid, cross-file consistency confirmed |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/discovering-requirements/SKILL.md | Modified | 1-10 (frontmatter) |
| src/claude/commands/ideate.md | Modified | 1-6 (frontmatter) |
| tests/STORY-446/*.sh | Created | 5 test files + runner |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| YYYY-MM-DD HH:MM | .claude/story-requirements-analyst | Created | Story created | STORY-XXX.story.md |
| 2026-02-18 | .claude/qa-result-interpreter | QA Deep | PASSED: 13/13 tests, 0 violations | - |

---

## Notes

- This is a quick-fix story — all changes are to YAML frontmatter (lines 1-16 of each file)
- Estimated 30 minutes total effort
- Files to modify:
  - `src/claude/skills/discovering-requirements/SKILL.md` (frontmatter lines 1-16)
  - `src/claude/commands/ideate.md` (frontmatter lines 1-6)
- Spec-recognized tool names: Read, Write, Edit, Glob, Grep, Bash, Task, WebFetch, WebSearch
- Non-spec names to replace: `Bash(git:*)` → `Bash`, `Skill` → `Task`
