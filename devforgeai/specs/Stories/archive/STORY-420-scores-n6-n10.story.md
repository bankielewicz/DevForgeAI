---
id: STORY-420
title: "Scores N6-N10 - Degrees of Freedom, Workflow, Feedback Loops, XML Tags, Role Prompting"
type: documentation
epic: EPIC-066
sprint: Sprint-3
status: Backlog
points: 5
depends_on: ["STORY-414", "STORY-416", "STORY-417"]
priority: High
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Scores N6-N10 - Degrees of Freedom, Workflow, Feedback Loops, XML Tags, Role Prompting

## Description

**As a** framework architect,
**I want** categories N6-N10 scored with evidence and remediation,
**so that** the prompt engineering technique conformance is quantified.

This story scores categories 6-10 (Degrees of Freedom, Workflow Structure, Feedback Loops, XML Tags, Role Prompting) using ONLY compressed deliverables from Sprint 1-2.

**CRITICAL CONSTRAINT:** This story reads ONLY:
- `02-scoring-rubric.md` (from STORY-414)
- `04-skill-md-analysis.md` (from STORY-416)
- `05-phase-files-analysis.md` (from STORY-417)

NO raw source files (.claude/skills/devforgeai-development/*) are read.

## Acceptance Criteria

### AC#1: N6 — Degrees of Freedom Scored (1-10)

```xml
<acceptance_criteria id="AC1">
  <given>Scoring rubric (02-scoring-rubric.md), skill analysis (04-skill-md-analysis.md), and phase analysis (05-phase-files-analysis.md) are available</given>
  <when>N6 Degrees of Freedom is scored</when>
  <then>Score 1-10 assigned with: highway/bridge/field metaphor assessment per phase, appropriateness analysis, fragile operations with wrong freedom level</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
      <file hint="Phase analysis">devforgeai/specs/requirements/dev-analysis/05-phase-files-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/08-scores-n6-n10.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Freedom level mapping from 05-phase-files-analysis.md (AC#5)
- Appropriateness assessment per phase
- Fragile operations (e.g., git commit) with too much freedom identified

---

### AC#2: N7 — Workflow Structure Scored (1-10)

```xml
<acceptance_criteria id="AC2">
  <given>Scoring rubric and phase analysis are available</given>
  <when>N7 Workflow Structure is scored</when>
  <then>Score 1-10 assigned with: checklist pattern presence, sequential step clarity, phase numbering consistency</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Phase analysis">devforgeai/specs/requirements/dev-analysis/05-phase-files-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/08-scores-n6-n10.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Checklist presence from 05-phase-files-analysis.md (AC#4)
- Fractional phase numbering issues (04.5, 05.5) from AC#1
- Sequential step clarity assessment

---

### AC#3: N8 — Feedback Loops Scored (1-10)

```xml
<acceptance_criteria id="AC3">
  <given>Scoring rubric and phase analysis are available</given>
  <when>N8 Feedback Loops is scored</when>
  <then>Score 1-10 assigned with: validation loop presence, "run validator → fix → repeat" pattern usage, phases with missing feedback loops</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Phase analysis">devforgeai/specs/requirements/dev-analysis/05-phase-files-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/08-scores-n6-n10.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Gate verification patterns from 05-phase-files-analysis.md (AC#2)
- devforgeai-validate usage documentation
- Phases with missing feedback loops

---

### AC#4: N9 — XML Tags Scored (1-10)

```xml
<acceptance_criteria id="AC4">
  <given>Scoring rubric and skill analysis are available</given>
  <when>N9 XML Tags is scored</when>
  <then>Score 1-10 assigned with: XML tag usage inventory, clarity/accuracy/flexibility/parseability assessment</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/08-scores-n6-n10.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- XML tag inventory from 04-skill-md-analysis.md content structure
- Assessment against Anthropic 4 benefits (clarity, accuracy, flexibility, parseability)

---

### AC#5: N10 — Role Prompting Scored (1-10)

```xml
<acceptance_criteria id="AC5">
  <given>Scoring rubric and skill analysis are available</given>
  <when>N10 Role Prompting is scored</when>
  <then>Score 1-10 assigned with: role definition presence, domain expert transformation, system parameter usage</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/08-scores-n6-n10.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Role definition presence in skill frontmatter/body
- Domain expert transformation assessment
- Clarity of role for Claude

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "ScoresN6N10"
      table: "N/A - Document output"
      purpose: "Structured scores for categories N6-N10"
      fields:
        - name: "n6_freedom"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Degrees of freedom score with evidence"
          test_requirement: "Test: Verify N6 has score and evidence"
        - name: "n7_workflow"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Workflow structure score with evidence"
          test_requirement: "Test: Verify N7 has score and evidence"
        - name: "n8_feedback"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Feedback loops score with evidence"
          test_requirement: "Test: Verify N8 has score and evidence"
        - name: "n9_xml"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "XML tags score with evidence"
          test_requirement: "Test: Verify N9 has score and evidence"
        - name: "n10_role"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Role prompting score with evidence"
          test_requirement: "Test: Verify N10 has score and evidence"

  business_rules:
    - id: "BR-001"
      rule: "Scores must be justified with quoted evidence"
      trigger: "When assigning each score"
      validation: "Each score section has ≥1 quote from input documents"
      test_requirement: "Test: Verify each score has evidence quotes"
      priority: "Critical"

    - id: "BR-002"
      rule: "NO raw source files may be read"
      trigger: "Throughout scoring process"
      validation: "Only Sprint 1-2 deliverables in Read() calls"
      test_requirement: "Test: Verify no .claude/skills/ paths read"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Scoring reads only compressed deliverables"
      metric: "Input files total < 5,000 lines"
      test_requirement: "Test: Verify input file count and size"
      priority: "Critical"
```

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-414:** Scoring Rubric Extraction
  - **Why:** Provides scoring criteria for all 5 categories
  - **Status:** Backlog (Sprint 1)

- [x] **STORY-416:** SKILL.md Analysis
  - **Why:** Provides evidence for N9, N10
  - **Status:** Backlog (Sprint 2)

- [x] **STORY-417:** Phase Files Analysis
  - **Why:** Provides evidence for N6, N7, N8
  - **Status:** Backlog (Sprint 2)

### External Dependencies

None.

---

## Acceptance Criteria Verification Checklist

### AC#1: N6 Degrees of Freedom

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Freedom level per phase documented - **Phase:** 3
- [ ] Fragile operations with wrong freedom identified - **Phase:** 3

### AC#2: N7 Workflow Structure

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Checklist pattern presence assessed - **Phase:** 3
- [ ] Phase numbering issues documented - **Phase:** 3

### AC#3: N8 Feedback Loops

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Validation loop patterns assessed - **Phase:** 3
- [ ] Missing feedback loops identified - **Phase:** 3

### AC#4: N9 XML Tags

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] XML tag inventory documented - **Phase:** 3
- [ ] 4-benefit assessment completed - **Phase:** 3

### AC#5: N10 Role Prompting

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Role definition presence assessed - **Phase:** 3
- [ ] Domain expert transformation evaluated - **Phase:** 3

---

**Checklist Progress:** 0/15 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] N6 Degrees of Freedom scored with evidence and remediation
- [ ] N7 Workflow Structure scored with evidence and remediation
- [ ] N8 Feedback Loops scored with evidence and remediation
- [ ] N9 XML Tags scored with evidence and remediation
- [ ] N10 Role Prompting scored with evidence and remediation
- [ ] Deliverable written to devforgeai/specs/requirements/dev-analysis/08-scores-n6-n10.md

### Quality
- [ ] All scores have quoted evidence
- [ ] Standard severity levels used
- [ ] No raw source files read

### Documentation
- [ ] Consistent scoring format across all 5 categories
- [ ] Summary table with all scores

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 10:50 | devforgeai-story-creation | Created | Story created from EPIC-066 Feature H | STORY-420.story.md |

## Notes

**Deliverable:**
- `devforgeai/specs/requirements/dev-analysis/08-scores-n6-n10.md`

**Sprint:** Sprint 3 (Scoring - Parallelizable)

**Inputs (ONLY — no raw source files):**
- `02-scoring-rubric.md` (from STORY-414)
- `04-skill-md-analysis.md` (from STORY-416)
- `05-phase-files-analysis.md` (from STORY-417)

**Can Execute In Parallel With:**
- STORY-419 (Scores N1-N5)
- STORY-421 (Scores N11-N14)

---

Story Template Version: 2.9
Last Updated: 2026-02-17
