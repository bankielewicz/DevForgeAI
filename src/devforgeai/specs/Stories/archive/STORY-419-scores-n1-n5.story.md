---
id: STORY-419
title: "Scores N1-N5 - Naming, Description, Size, Progressive Disclosure, Conciseness"
type: documentation
epic: EPIC-066
sprint: Sprint-3
status: Backlog
points: 5
depends_on: ["STORY-414", "STORY-416", "STORY-418"]
priority: High
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Scores N1-N5 - Naming, Description, Size, Progressive Disclosure, Conciseness

## Description

**As a** framework architect,
**I want** categories N1-N5 scored with evidence and remediation,
**so that** the structural and metadata conformance is quantified.

This story scores the first 5 categories (Naming Convention, Description Quality, SKILL.md Size, Progressive Disclosure, Conciseness) using ONLY the compressed deliverables from Sprint 1-2, NOT raw source files.

**CRITICAL CONSTRAINT:** This story reads ONLY:
- `02-scoring-rubric.md` (from STORY-414)
- `04-skill-md-analysis.md` (from STORY-416)
- `06-reference-files-analysis.md` (from STORY-418)

NO raw source files (.claude/skills/devforgeai-development/*) are read.

## Acceptance Criteria

### AC#1: N1 — Naming Convention Scored (1-10)

```xml
<acceptance_criteria id="AC1">
  <given>Scoring rubric (02-scoring-rubric.md) and skill analysis (04-skill-md-analysis.md) are available</given>
  <when>N1 Naming Convention is scored</when>
  <then>Score 1-10 assigned with: best practice quote from rubric, current implementation quote from analysis, gap analysis, severity, remediation recommendation</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/07-scores-n1-n5.md</test_file>
  </verification>
</acceptance_criteria>
```

**Scoring Format:**
```markdown
## N1: Naming Convention

**Score: X/10**

**Best Practice (from rubric):**
> [Exact quote from 02-scoring-rubric.md N1 section]

**Current Implementation:**
> [Quote from 04-skill-md-analysis.md frontmatter section]

**Gap Analysis:**
- [Specific gap identified]
- Severity: [CRITICAL/HIGH/MEDIUM/LOW]

**Remediation:**
- [Specific fix recommended]
- ADR Required: [Yes/No]
```

---

### AC#2: N2 — Description Quality Scored (1-10)

```xml
<acceptance_criteria id="AC2">
  <given>Scoring rubric and skill analysis are available</given>
  <when>N2 Description Quality is scored</when>
  <then>Score 1-10 assigned with evidence and remediation following N1 format</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/07-scores-n1-n5.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: N3 — SKILL.md Size Scored (1-10)

```xml
<acceptance_criteria id="AC3">
  <given>Scoring rubric and skill analysis are available</given>
  <when>N3 SKILL.md Size is scored</when>
  <then>Score 1-10 assigned with: line count evidence, overage calculation, extraction plan reference, specific remediation</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/07-scores-n1-n5.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Current line count from 04-skill-md-analysis.md
- Overage calculation (1,099 - 500 = 599 lines over)
- Extraction plan from 04-skill-md-analysis.md
- Line reduction targets

---

### AC#4: N4 — Progressive Disclosure Scored (1-10)

```xml
<acceptance_criteria id="AC4">
  <given>Scoring rubric, skill analysis, and reference analysis are available</given>
  <when>N4 Progressive Disclosure is scored</when>
  <then>Score 1-10 assigned with: depth chain evidence, one-level-deep violations, L1/L2/L3 assessment</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
      <file hint="Reference analysis">devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/07-scores-n1-n5.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Depth chain documentation from 06-reference-files-analysis.md
- One-level-deep violations count
- L1/L2/L3 layer assessment from 04-skill-md-analysis.md

---

### AC#5: N5 — Conciseness Scored (1-10)

```xml
<acceptance_criteria id="AC5">
  <given>Scoring rubric, skill analysis, and reference analysis are available</given>
  <when>N5 Conciseness is scored</when>
  <then>Score 1-10 assigned with: verbose section identification, "Claude already knows" content, specific line ranges</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
      <file hint="Reference analysis">devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/07-scores-n1-n5.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Verbose sections identified from 04-skill-md-analysis.md and 06-reference-files-analysis.md
- "Challenge each piece" assessment
- Specific line ranges for verbose content

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "ScoresN1N5"
      table: "N/A - Document output"
      purpose: "Structured scores for categories N1-N5"
      fields:
        - name: "n1_naming"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Naming convention score with evidence"
          test_requirement: "Test: Verify N1 has score and evidence"
        - name: "n2_description"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Description quality score with evidence"
          test_requirement: "Test: Verify N2 has score and evidence"
        - name: "n3_size"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "SKILL.md size score with evidence"
          test_requirement: "Test: Verify N3 has score and evidence"
        - name: "n4_disclosure"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Progressive disclosure score with evidence"
          test_requirement: "Test: Verify N4 has score and evidence"
        - name: "n5_conciseness"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Conciseness score with evidence"
          test_requirement: "Test: Verify N5 has score and evidence"

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

    - id: "BR-003"
      rule: "Severity must use standard levels"
      trigger: "When documenting gaps"
      validation: "Severity is CRITICAL, HIGH, MEDIUM, or LOW"
      test_requirement: "Test: Verify standard severity levels used"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Scoring reads only compressed deliverables"
      metric: "Input files total < 5,000 lines (rubric + 2 analyses)"
      test_requirement: "Test: Verify input file count and size"
      priority: "Critical"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Context Efficiency:**
- Input: ~3,000 lines (rubric + skill analysis + reference analysis excerpts)
- Output: < 800 lines scoring document

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-414:** Scoring Rubric Extraction
  - **Why:** Provides scoring criteria for all 5 categories
  - **Status:** Backlog (Sprint 1)

- [x] **STORY-416:** SKILL.md Analysis
  - **Why:** Provides evidence for N1, N2, N3, N4, N5
  - **Status:** Backlog (Sprint 2)

- [x] **STORY-418:** Reference Files Analysis
  - **Why:** Provides evidence for N4, N5
  - **Status:** Backlog (Sprint 2)

### External Dependencies

None.

### Technology Dependencies

None. Uses only Read and Write tools.

---

## Test Strategy

### Verification Scenarios

1. **Completeness:** All 5 categories scored (N1-N5)
2. **Evidence:** Each score has ≥1 quoted evidence
3. **Severity:** Standard levels used consistently
4. **No raw source:** No .claude/skills/ paths in Read() calls

---

## Acceptance Criteria Verification Checklist

### AC#1: N1 Naming Convention

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Best practice quoted from rubric - **Phase:** 3
- [ ] Current implementation quoted from analysis - **Phase:** 3
- [ ] Gap analysis with severity - **Phase:** 3
- [ ] Remediation recommendation - **Phase:** 3

### AC#2: N2 Description Quality

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Evidence quoted from inputs - **Phase:** 3
- [ ] Gap analysis with severity - **Phase:** 3

### AC#3: N3 SKILL.md Size

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Line count evidence - **Phase:** 3
- [ ] Extraction plan referenced - **Phase:** 3

### AC#4: N4 Progressive Disclosure

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Depth chain evidence - **Phase:** 3
- [ ] One-level-deep violations counted - **Phase:** 3

### AC#5: N5 Conciseness

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Verbose sections identified - **Phase:** 3
- [ ] Line ranges documented - **Phase:** 3

---

**Checklist Progress:** 0/17 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] N1 Naming Convention scored with evidence and remediation
- [ ] N2 Description Quality scored with evidence and remediation
- [ ] N3 SKILL.md Size scored with evidence and remediation
- [ ] N4 Progressive Disclosure scored with evidence and remediation
- [ ] N5 Conciseness scored with evidence and remediation
- [ ] Deliverable written to devforgeai/specs/requirements/dev-analysis/07-scores-n1-n5.md

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
| 2026-02-17 10:45 | devforgeai-story-creation | Created | Story created from EPIC-066 Feature G | STORY-419.story.md |

## Notes

**Design Decisions:**
- Scoring uses ONLY compressed deliverables, never raw source
- Consistent format across all 5 categories enables aggregation

**Deliverable:**
- `devforgeai/specs/requirements/dev-analysis/07-scores-n1-n5.md`

**Sprint:** Sprint 3 (Scoring - Parallelizable)

**Inputs (ONLY — no raw source files):**
- `02-scoring-rubric.md` (from STORY-414)
- `04-skill-md-analysis.md` (from STORY-416)
- `06-reference-files-analysis.md` (from STORY-418)

**Can Execute In Parallel With:**
- STORY-420 (Scores N6-N10)
- STORY-421 (Scores N11-N14)

---

Story Template Version: 2.9
Last Updated: 2026-02-17
