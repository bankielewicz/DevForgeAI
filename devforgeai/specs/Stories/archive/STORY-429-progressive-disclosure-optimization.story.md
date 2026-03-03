---
id: STORY-429
title: "Add Table of Contents to Reference Files and Remove Redundant Content"
type: documentation
epic: EPIC-067
sprint: Sprint-3
status: Deferred
points: 5
depends_on: ["STORY-428"]
priority: Medium
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Add Table of Contents to Reference Files and Remove Redundant Content

## Description

**As a** DevForgeAI framework maintainer,
**I want** to add table of contents to reference files exceeding 100 lines and remove the redundant Core Philosophy section,
**so that** Claude can navigate large files efficiently and unnecessary tokens are eliminated as recommended by Anthropic's best practices.

**Context:** This story addresses conformance analysis findings 3.2 (Medium) and 4.1 (Low). Finding 3.2 identified 14 reference files exceeding 100 lines without TOC headers. Finding 4.1 identified ~150 tokens of Core Philosophy content Claude already knows.

**Analysis Source:** `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md`, Categories 3, 4

## Acceptance Criteria

### AC#1: TOC Added to 14 Reference Files

```xml
<acceptance_criteria id="AC1" implements="FINDING-3.2">
  <given>14 reference files exceed 100 lines without table of contents</given>
  <when>TOC sections are added</when>
  <then>Each of the 14 files has a "## Contents" or "## Table of Contents" section at the top listing all ## and ### headers</then>
  <verification>
    <source_files>
      <file hint="Largest file">.claude/skills/devforgeai-ideation/references/error-handling.md</file>
      <file hint="Discovery workflow">.claude/skills/devforgeai-ideation/references/discovery-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-429/test_ac1_toc_presence.sh</test_file>
  </verification>
</acceptance_criteria>
```

**Files requiring TOC (per Finding 3.2):**
1. error-handling.md (1,062 lines)
2. brainstorm-data-mapping.md (1,026 lines)
3. user-input-guidance.md (897 lines)
4. completion-handoff.md (800 lines)
5. artifact-generation.md (700 lines)
6. validation-checklists.md (604 lines)
7. feasibility-analysis-workflow.md (543 lines)
8. self-validation-workflow.md (429 lines)
9. user-interaction-patterns.md (411 lines)
10. brainstorm-handoff-workflow.md (389 lines)
11. resume-logic.md (382 lines)
12. requirements-elicitation-workflow.md (368 lines)
13. complexity-assessment-workflow.md (333 lines)
14. epic-decomposition-workflow.md (309 lines)

---

### AC#2: TOC Format Follows Anthropic Pattern

```xml
<acceptance_criteria id="AC2">
  <given>TOC sections are being added</given>
  <when>TOC format is checked</when>
  <then>TOC uses bullet-point list with markdown links to section headers; format matches Anthropic best-practices.md example (lines 377-394)</then>
  <verification>
    <source_files>
      <file hint="Sample reference file">.claude/skills/devforgeai-ideation/references/discovery-workflow.md</file>
    </source_files>
    <test_file>tests/STORY-429/test_ac2_toc_format.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Core Philosophy Section Removed

```xml
<acceptance_criteria id="AC3" implements="FINDING-4.1">
  <given>SKILL.md contains Core Philosophy section (lines 49-64) explaining concepts Claude already knows</given>
  <when>The section is removed</when>
  <then>Core Philosophy section is deleted; ~120 tokens saved per invocation</then>
  <verification>
    <source_files>
      <file hint="Main skill file">.claude/skills/devforgeai-ideation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-429/test_ac3_philosophy_removed.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: All Files >100 Lines Have TOC

```xml
<acceptance_criteria id="AC4">
  <given>TOC additions complete</given>
  <when>All reference files are scanned</when>
  <then>No reference file exceeding 100 lines lacks a TOC section</then>
  <verification>
    <source_files>
      <file hint="All reference files">.claude/skills/devforgeai-ideation/references/*.md</file>
    </source_files>
    <test_file>tests/STORY-429/test_ac4_toc_completeness.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "TOC Generation Script"
      file_path: "tests/STORY-429/generate-toc.sh"
      required_keys:
        - key: "toc_format"
          type: "string"
          example: "## Table of Contents\n- [Section 1](#section-1)\n- [Section 2](#section-2)"
          required: true
          test_requirement: "Test: TOC uses markdown anchor links"

  business_rules:
    - id: "BR-001"
      rule: "Files >100 lines must have TOC at top"
      trigger: "When validating reference files"
      validation: "If line count > 100, TOC section must exist"
      error_handling: "List files missing TOC"
      test_requirement: "Test: All files >100 lines have TOC"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Token savings from Core Philosophy removal"
      metric: "~120 tokens saved per invocation"
      test_requirement: "Test: Core Philosophy section absent"
      priority: "Low"
```

---

## Definition of Done

### Implementation
- [ ] TOC added to all 14 reference files >100 lines
- [ ] TOC format matches Anthropic best-practices pattern
- [ ] Core Philosophy section removed from SKILL.md
- [ ] No reference file >100 lines lacks TOC

### Quality
- [ ] All 4 acceptance criteria have passing tests
- [ ] TOC links correctly anchor to headers
- [ ] No content lost (only TOC added, philosophy removed)

### Testing
- [ ] Test: 14 specific files have TOC
- [ ] Test: TOC format validation
- [ ] Test: Core Philosophy absent
- [ ] Test: Completeness scan

---

## Change Log

**Current Status:** Deferred — Blocked by EPIC-068

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 15:30 | devforgeai-story-creation | Created | Story created from EPIC-067 Feature 5 | STORY-429.story.md |
| 2026-02-17 | DevForgeAI AI Agent | Deferred | Blocked by EPIC-068 (Skill Responsibility Restructure). 6 of 14 target reference files moving from ideation to architecture — file paths will be invalid. Re-evaluate after EPIC-068 Sprint 1. | STORY-429.story.md |

## Notes

**Batch Operation:** Consider creating a script to auto-generate TOC for efficiency. Extract ## and ### headers, generate markdown anchor links.

**Anthropic Reference:**
- best-practices.md lines 373-397: "For reference files longer than 100 lines, include a table of contents at the top."

---

Story Template Version: 2.9
Last Updated: 2026-02-17
