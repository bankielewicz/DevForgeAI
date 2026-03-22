---
id: STORY-321
title: Add Glossary Section to Brainstorm Output Template
type: feature
epic: EPIC-049
sprint: null
status: QA Approved
points: 1
depends_on: []
priority: High
assigned_to: null
created: 2026-01-26
format_version: "2.7"
source_rca: RCA-030
source_recommendation: REC-2
---

# Story: Add Glossary Section to Brainstorm Output Template

## Description

**As a** devforgeai-brainstorming skill,
**I want** the output template to include optional "Key Files for Context" and "Glossary" sections,
**so that** the template structure explicitly shows where context sections should be generated when needed.

**Background:** RCA-030 identified that the brainstorm template in `output-templates.md` has no placeholder for term definitions or file context, which means Claude doesn't know these sections should exist.

## Current State (Target File)

### Target File: `.claude/skills/devforgeai-brainstorming/references/output-templates.md`

**Insert Location:** After YAML frontmatter ends (line 69) and before `## Executive Summary` (line 72)

**Current Structure (excerpt lines 65-78):**
```markdown
nice_to_have:
  - "{Capability 3}"
---

# {Brainstorm Title}

## Executive Summary

{2-3 paragraph summary...}
```

**Target Structure After Edit:**
```markdown
nice_to_have:
  - "{Capability 3}"
---

# {Brainstorm Title}

## Key Files for Context (Optional)

{If brainstorm references framework-specific files:}

| Component | File Path | Purpose |
|-----------|-----------|---------|
| {Component 1} | `{full/path/to/file.md}` | {What it does} |
| {Component 2} | `{full/path/to/file.md}` | {What it does} |

---

## Glossary (Optional)

{If brainstorm uses framework-specific terminology:}

| Term | Definition |
|------|------------|
| {Term 1} | {Clear definition for someone without context} |
| {Term 2} | {Clear definition for someone without context} |

---

## Executive Summary

{2-3 paragraph summary...}
```

**Conditional Rendering Guidance to Add:**
```markdown
> **Note:** Include "Key Files for Context" when the brainstorm references:
> - Files in `.claude/` directory (skills, agents, commands)
> - Files in `devforgeai/` directory (specs, context, workflows)
> - Configuration files (hooks.yaml, settings.json, etc.)
>
> Include "Glossary" when the brainstorm uses:
> - Phase numbers (Phase 01, Phase 09, etc.)
> - DevForgeAI-specific terms (subagent, skill, context file, quality gate, etc.)
> - Workflow terminology (TDD, DoD, AC, preflight, etc.)
```

## Provenance

```xml
<provenance>
  <origin document="RCA-030" section="recommendations">
    <quote>"Template has no placeholder for term definitions"</quote>
    <line_reference>lines 158-198</line_reference>
    <quantified_impact>Makes template structure explicit so Claude knows sections should be generated</quantified_impact>
  </origin>

  <decision rationale="template-driven-consistency">
    <selected>Add optional sections to template with conditional rendering guidance</selected>
    <rejected alternative="runtime-only-generation">
      Without template placeholders, Claude may generate sections in wrong location
    </rejected>
    <trade_off>Template slightly longer but provides clear structure</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: Key Files for Context Section in Template

```xml
<acceptance_criteria id="AC1">
  <given>The brainstorm output template in output-templates.md</given>
  <when>A user reviews the template structure</when>
  <then>There is an optional "Key Files for Context" section with table format (Component, File Path, Purpose columns) positioned after frontmatter and before Executive Summary</then>
  <verification>
    <source_files>
      <file hint="Output template">.claude/skills/devforgeai-brainstorming/references/output-templates.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-321/test_ac1_key_files_section.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Glossary Section in Template

```xml
<acceptance_criteria id="AC2">
  <given>The brainstorm output template in output-templates.md</given>
  <when>A user reviews the template structure</when>
  <then>There is an optional "Glossary" section with table format (Term, Definition columns) positioned after Key Files section and before Executive Summary</then>
  <verification>
    <source_files>
      <file hint="Output template">.claude/skills/devforgeai-brainstorming/references/output-templates.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-321/test_ac2_glossary_section.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Conditional Rendering Guidance

```xml
<acceptance_criteria id="AC3">
  <given>The template sections are marked as optional</given>
  <when>Claude generates a brainstorm document</when>
  <then>The template includes clear guidance on when to include each section (framework-specific files, framework-specific terminology)</then>
  <verification>
    <source_files>
      <file hint="Output template">.claude/skills/devforgeai-brainstorming/references/output-templates.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-321/test_ac3_conditional_guidance.py</test_file>
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
      name: "Key Files Section Template"
      file_path: ".claude/skills/devforgeai-brainstorming/references/output-templates.md"
      required_keys:
        - key: "section_header"
          type: "string"
          example: "## Key Files for Context (Optional)"
          required: true
          test_requirement: "Test: Verify header exists in template"
        - key: "table_columns"
          type: "array"
          example: '["Component", "File Path", "Purpose"]'
          required: true
          test_requirement: "Test: Verify table has 3 columns"

    - type: "Configuration"
      name: "Glossary Section Template"
      file_path: ".claude/skills/devforgeai-brainstorming/references/output-templates.md"
      required_keys:
        - key: "section_header"
          type: "string"
          example: "## Glossary (Optional)"
          required: true
          test_requirement: "Test: Verify header exists in template"
        - key: "table_columns"
          type: "array"
          example: '["Term", "Definition"]'
          required: true
          test_requirement: "Test: Verify table has 2 columns"

  business_rules:
    - id: "BR-001"
      rule: "Sections are optional and only included when framework references exist"
      trigger: "Document contains DevForgeAI-specific content"
      validation: "Check for framework file paths or terminology"
      error_handling: "Omit sections if no framework content"
      test_requirement: "Test: Verify sections omitted for non-technical brainstorms"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Documentation"
      requirement: "Template must be clear and self-documenting"
      metric: "Conditional guidance present for both sections"
      test_requirement: "Test: Verify conditional guidance text exists"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Documentation

**Clarity:**
- Template sections clearly marked as "(Optional)"
- Conditional rendering guidance included inline

---

## Dependencies

### Prerequisite Stories

None - standalone template enhancement.

### External Dependencies

None.

### Technology Dependencies

None.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Template contains both optional sections
2. **Edge Cases:**
   - Sections positioned correctly (after frontmatter, before Executive Summary)
3. **Error Cases:**
   - N/A (template validation only)

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Brainstorm Generation:** Run `/brainstorm` and verify template sections appear when appropriate

---

## Acceptance Criteria Verification Checklist

### AC#1: Key Files for Context Section

- [x] Section header added - **Phase:** 3 - **Evidence:** output-templates.md line 73
- [x] Table format with 3 columns - **Phase:** 3 - **Evidence:** output-templates.md lines 77-79
- [x] Positioned after frontmatter - **Phase:** 3 - **Evidence:** output-templates.md line 73

### AC#2: Glossary Section

- [x] Section header added - **Phase:** 3 - **Evidence:** output-templates.md line 83
- [x] Table format with 2 columns - **Phase:** 3 - **Evidence:** output-templates.md lines 87-89
- [x] Positioned after Key Files - **Phase:** 3 - **Evidence:** output-templates.md line 83

### AC#3: Conditional Rendering Guidance

- [x] Guidance text for Key Files - **Phase:** 3 - **Evidence:** output-templates.md lines 91-95
- [x] Guidance text for Glossary - **Phase:** 3 - **Evidence:** output-templates.md lines 97-99

---

**Checklist Progress:** 8/8 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Key Files for Context section added to output-templates.md
- [x] Glossary section added to output-templates.md
- [x] Conditional rendering guidance added
- [x] Sections positioned correctly in template order

### Quality
- [x] All 3 acceptance criteria have passing tests (14/14 passed)
- [x] Template renders correctly in generated documents (validated by QA Light)

### Testing
- [x] Unit tests for template structure (14 tests in devforgeai/tests/STORY-321/)
- [x] Integration test with brainstorm generation (verified by integration-tester)

### Documentation
- [x] output-templates.md updated (Key Files & Glossary sections added)
- [x] RCA-030 updated with story link (RCA-030 already references STORY-321 at lines 162, 268)

---

## Implementation Notes

- [x] Key Files for Context section added to output-templates.md - Completed: lines 73-80, 3-column table
- [x] Glossary section added to output-templates.md - Completed: lines 84-91, 2-column table
- [x] Conditional rendering guidance added - Completed: lines 93-101, Note block with inclusion criteria
- [x] Sections positioned correctly in template order - Completed: Key Files → Glossary → Executive Summary
- All 14 tests passing (4 for AC#1, 4 for AC#2, 6 for AC#3)
- Both src/ and .claude/ files synced

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-26 | claude/create-stories-from-rca | Created | Story created from RCA-030 REC-2 | STORY-321.story.md |
| 2026-01-26 | claude/qa-result-interpreter | QA Deep | PASSED: 14/14 tests, 0 violations | devforgeai/qa/reports/STORY-321-qa-report.md |

## Notes

**Source:** RCA-030: Brainstorm Output Missing Cross-Session Context
**Recommendation:** REC-2 (HIGH priority)
**Effort Estimate:** 30 minutes

**Related RCAs:**
- RCA-030: Root cause analysis that identified this issue

**References:**
- `.claude/skills/devforgeai-brainstorming/references/output-templates.md` (target file)

---

Story Template Version: 2.7
Last Updated: 2026-01-26
