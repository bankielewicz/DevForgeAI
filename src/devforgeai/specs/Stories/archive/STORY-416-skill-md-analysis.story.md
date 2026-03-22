---
id: STORY-416
title: "SKILL.md Analysis - Frontmatter, Body Size, Progressive Disclosure"
type: documentation
epic: EPIC-066
sprint: Sprint-2
status: Backlog
points: 5
depends_on: ["STORY-413"]
priority: High
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: SKILL.md Analysis - Frontmatter, Body Size, Progressive Disclosure

## Description

**As a** framework architect,
**I want** a detailed analysis of the SKILL.md file,
**so that** I understand the primary conformance gaps in the skill's core file.

SKILL.md is the largest single file in the ecosystem (1,099 lines) and where most conformance gaps are expected. This analysis is critical for Sprint 3 scoring.

## Acceptance Criteria

### AC#1: YAML Frontmatter Evaluation

```xml
<acceptance_criteria id="AC1">
  <given>The SKILL.md file exists at .claude/skills/devforgeai-development/SKILL.md</given>
  <when>YAML frontmatter is analyzed</when>
  <then>Analysis documents: name field vs gerund convention, description vs third-person/discovery requirements, gap severity</then>
  <verification>
    <source_files>
      <file hint="Skill file">.claude/skills/devforgeai-development/SKILL.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- CURRENT: `name: devforgeai-development` — not gerund form
  (Source: .claude/skills/devforgeai-development/SKILL.md, line 2)
- TARGET: Gerund form like `developing-with-tdd` or `implementing-features`
  (Source: best-practices.md, lines 156-165)
- Analyze description against third-person and discovery requirements (best-practices.md, lines 183-227)

---

### AC#2: Body Size Analysis

```xml
<acceptance_criteria id="AC2">
  <given>The SKILL.md file has been read</given>
  <when>Body size is analyzed</when>
  <then>Analysis documents: current line count, overage from 500-line target, sections that could be extracted, extraction plan</then>
  <verification>
    <source_files>
      <file hint="Skill file">.claude/skills/devforgeai-development/SKILL.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- CURRENT: 1,099 lines — exceeds 500-line target by 599 lines (2.2x)
  (Source: .claude/skills/devforgeai-development/SKILL.md)
- TARGET: Under 500 lines (best-practices.md, lines 233-235)
- CONTEXT FILE CONSTRAINT: Skills target 500-800 lines, max 1,000 lines
  (Source: devforgeai/specs/context/coding-standards.md, lines 106-107)
- Identify which sections to extract to achieve <500 lines

**Extraction Analysis Required:**
- List each major section with line count
- Identify sections that could move to references/
- Calculate remaining lines after extraction
- Verify extraction would achieve <500 line target

---

### AC#3: Progressive Disclosure Effectiveness

```xml
<acceptance_criteria id="AC3">
  <given>The SKILL.md file and references directory have been analyzed</given>
  <when>Progressive disclosure is evaluated</when>
  <then>Analysis documents: what content is in SKILL.md body vs phases/ and references/, reference depth (one-level-deep rule), any A→B→C reference chains</then>
  <verification>
    <source_files>
      <file hint="Skill file">.claude/skills/devforgeai-development/SKILL.md</file>
      <file hint="Phase files">.claude/skills/devforgeai-development/phases/*.md</file>
      <file hint="Reference files">.claude/skills/devforgeai-development/references/*.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Map what content is in SKILL.md body vs. extracted to phases/ and references/
- Check reference depth (Anthropic: one level deep from SKILL.md)
  (Source: best-practices.md, lines 228-398)
- Identify any A→B→C reference chains (SKILL.md → phase → reference → sub-reference)
- Document violations of one-level-deep rule

---

### AC#4: Content Structure Analysis

```xml
<acceptance_criteria id="AC4">
  <given>The SKILL.md file has been fully read</given>
  <when>Content structure is analyzed</when>
  <then>Analysis documents: section organization, heading hierarchy, TOC presence (files >100 lines should have TOC), conciseness issues</then>
  <verification>
    <source_files>
      <file hint="Skill file">.claude/skills/devforgeai-development/SKILL.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Document section organization (list all ## and ### headers)
- Check for table of contents (files >100 lines should have TOC)
- Evaluate conciseness (does it over-explain things Claude already knows?)
  (Source: best-practices.md, lines 13-55)
- Identify verbose sections with specific line ranges

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "SkillMdAnalysis"
      table: "N/A - Document output"
      purpose: "Structured analysis of SKILL.md conformance"
      fields:
        - name: "frontmatter_analysis"
          type: "Object"
          constraints: "Required"
          description: "Name and description conformance"
          test_requirement: "Test: Verify frontmatter section complete"
        - name: "size_analysis"
          type: "Object"
          constraints: "Required"
          description: "Line count and extraction opportunities"
          test_requirement: "Test: Verify size analysis with extraction plan"
        - name: "progressive_disclosure_analysis"
          type: "Object"
          constraints: "Required"
          description: "Reference depth and chain analysis"
          test_requirement: "Test: Verify disclosure analysis identifies chains"
        - name: "structure_analysis"
          type: "Object"
          constraints: "Required"
          description: "Heading hierarchy and conciseness"
          test_requirement: "Test: Verify structure analysis complete"

  business_rules:
    - id: "BR-001"
      rule: "Size analysis must provide actionable extraction plan"
      trigger: "When analyzing oversized SKILL.md"
      validation: "Extraction plan achieves <500 lines if followed"
      test_requirement: "Test: Verify extraction plan math adds up to <500"
      priority: "Critical"

    - id: "BR-002"
      rule: "Reference chains must be identified with specific file paths"
      trigger: "When analyzing progressive disclosure"
      validation: "Each chain documented as A → B → C format"
      test_requirement: "Test: Verify chains have file paths at each level"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Analysis must fit in single context window"
      metric: "Total input < 2,000 lines (SKILL.md + samples of phases/references)"
      test_requirement: "Test: Verify analysis completes without context overflow"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Context Efficiency:**
- Input: ~1,100 lines (SKILL.md) + ecosystem inventory reference
- Output: < 800 lines analysis document

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-413:** Ecosystem Inventory
  - **Why:** Need file inventory to understand skill's place in ecosystem
  - **Status:** Backlog (Sprint 1)

### External Dependencies

None.

### Technology Dependencies

None. Uses only Read and Write tools.

---

## Test Strategy

### Verification Scenarios

1. **Completeness:** All 4 AC sections present in deliverable
2. **Size calculation:** Line counts verified against wc -l
3. **Chain identification:** At least 1 reference chain documented (known to exist)
4. **Extraction plan:** Math verified (current - extracted = <500)

---

## Acceptance Criteria Verification Checklist

### AC#1: YAML Frontmatter Evaluation

- [ ] Name field analyzed against gerund convention - **Phase:** 3
- [ ] Description analyzed against third-person requirements - **Phase:** 3
- [ ] Gap severity documented - **Phase:** 3

### AC#2: Body Size Analysis

- [ ] Current line count documented - **Phase:** 3
- [ ] Sections listed with individual line counts - **Phase:** 3
- [ ] Extraction plan created with target sections - **Phase:** 3
- [ ] Post-extraction line count calculated (<500) - **Phase:** 3

### AC#3: Progressive Disclosure Effectiveness

- [ ] Content mapping (SKILL.md vs phases vs references) - **Phase:** 3
- [ ] Reference depth analysis - **Phase:** 3
- [ ] A→B→C chains identified - **Phase:** 3

### AC#4: Content Structure Analysis

- [ ] Section organization documented - **Phase:** 3
- [ ] TOC presence checked - **Phase:** 3
- [ ] Verbose sections identified with line ranges - **Phase:** 3

---

**Checklist Progress:** 0/12 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] YAML frontmatter evaluation complete with CURRENT/TARGET format
- [ ] Body size analysis complete with extraction plan
- [ ] Progressive disclosure analysis complete with chain identification
- [ ] Content structure analysis complete with verbose section identification
- [ ] Deliverable written to devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md

### Quality
- [ ] Line counts verified against actual file
- [ ] Extraction plan math verified
- [ ] Reference chains documented with file paths

### Documentation
- [ ] Analysis follows output template structure
- [ ] All gaps have severity ratings

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 10:30 | devforgeai-story-creation | Created | Story created from EPIC-066 Feature D | STORY-416.story.md |

## Notes

**Design Decisions:**
- Focus on SKILL.md only (phase analysis is STORY-417, reference analysis is STORY-418)
- Extraction plan is advisory — actual extraction would be separate remediation story

**Deliverable:**
- `devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md`

**Sprint:** Sprint 2 (Analysis - Parallelizable)

**Inputs:**
- `.claude/skills/devforgeai-development/SKILL.md` (1,099 lines)
- `01-ecosystem-inventory.md` (from STORY-413)

**Can Execute In Parallel With:**
- STORY-415 (/dev Command Analysis)
- STORY-417 (Phase Files Analysis)
- STORY-418 (Reference Files Analysis)

---

Story Template Version: 2.9
Last Updated: 2026-02-17
