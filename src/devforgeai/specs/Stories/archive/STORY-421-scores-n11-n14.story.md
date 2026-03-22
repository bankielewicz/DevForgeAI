---
id: STORY-421
title: "Scores N11-N14 - Examples/Multishot, Chain of Thought, Architecture, Anti-Patterns"
type: documentation
epic: EPIC-066
sprint: Sprint-3
status: Backlog
points: 5
depends_on: ["STORY-414", "STORY-415", "STORY-416", "STORY-417", "STORY-418"]
priority: High
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Scores N11-N14 - Examples/Multishot, Chain of Thought, Architecture, Anti-Patterns

## Description

**As a** framework architect,
**I want** categories N11-N14 scored with evidence and remediation,
**so that** advanced technique and architecture conformance is quantified.

This story scores the final 4 categories (Examples/Multishot, Chain of Thought, Command-Skill Architecture, Anti-Patterns) using ALL Sprint 2 deliverables plus the rubric.

**CRITICAL CONSTRAINT:** This story reads ONLY:
- `02-scoring-rubric.md` (from STORY-414)
- `03-dev-command-analysis.md` (from STORY-415)
- `04-skill-md-analysis.md` (from STORY-416)
- `05-phase-files-analysis.md` (from STORY-417)
- `06-reference-files-analysis.md` (from STORY-418)

NO raw source files (.claude/skills/devforgeai-development/*) are read.

## Acceptance Criteria

### AC#1: N11 — Examples/Multishot Scored (1-10)

```xml
<acceptance_criteria id="AC1">
  <given>Scoring rubric (02-scoring-rubric.md), skill analysis (04-skill-md-analysis.md), and phase analysis (05-phase-files-analysis.md) are available</given>
  <when>N11 Examples/Multishot is scored</when>
  <then>Score 1-10 assigned with: example count, example diversity assessment, <example> tag wrapping, 3-5 examples guidance compliance</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
      <file hint="Phase analysis">devforgeai/specs/requirements/dev-analysis/05-phase-files-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/09-scores-n11-n14.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Example count from content structure analysis
- Diversity assessment (different scenarios vs repetitive)
- `<example>` tag wrapping presence
- Compliance with 3-5 examples per decision point guidance

---

### AC#2: N12 — Chain of Thought Scored (1-10)

```xml
<acceptance_criteria id="AC2">
  <given>Scoring rubric, skill analysis, and phase analysis are available</given>
  <when>N12 Chain of Thought is scored</when>
  <then>Score 1-10 assigned with: <thinking> tag usage, <answer> tag usage, structured reasoning guidance, explicit CoT prompts</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
      <file hint="Phase analysis">devforgeai/specs/requirements/dev-analysis/05-phase-files-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/09-scores-n11-n14.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- `<thinking>` tag usage inventory
- `<answer>` tag usage inventory
- Structured reasoning guidance presence
- Explicit CoT prompts in phases

---

### AC#3: N13 — Command-Skill Architecture Scored (1-10)

```xml
<acceptance_criteria id="AC3">
  <given>Scoring rubric, command analysis, skill analysis, and phase analysis are available</given>
  <when>N13 Command-Skill Architecture is scored</when>
  <then>Score 1-10 assigned with: thin command pattern compliance, single responsibility evaluation, subagent scoping assessment, layer separation</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Command analysis">devforgeai/specs/requirements/dev-analysis/03-dev-command-analysis.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
      <file hint="Phase analysis">devforgeai/specs/requirements/dev-analysis/05-phase-files-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/09-scores-n11-n14.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Thin command pattern from 03-dev-command-analysis.md (AC#2)
- Single responsibility assessment
- Subagent scoping from 05-phase-files-analysis.md (AC#3)
- Layer separation (command → skill → phase → reference)

---

### AC#4: N14 — Anti-Patterns Scored (1-10)

```xml
<acceptance_criteria id="AC4">
  <given>Scoring rubric and ALL Sprint 2 deliverables are available</given>
  <when>N14 Anti-Patterns is scored</when>
  <then>Score 1-10 assigned with: Windows paths check, too many options check, deeply nested references check, time-sensitive info check</then>
  <verification>
    <source_files>
      <file hint="Rubric">devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</file>
      <file hint="Command analysis">devforgeai/specs/requirements/dev-analysis/03-dev-command-analysis.md</file>
      <file hint="Skill analysis">devforgeai/specs/requirements/dev-analysis/04-skill-md-analysis.md</file>
      <file hint="Phase analysis">devforgeai/specs/requirements/dev-analysis/05-phase-files-analysis.md</file>
      <file hint="Reference analysis">devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/09-scores-n11-n14.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- Windows paths check (C:\\ patterns)
- Too many options check (excessive AskUserQuestion options)
- Deeply nested references from 06-reference-files-analysis.md (AC#1)
- Time-sensitive info check (dates, versions that become stale)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "ScoresN11N14"
      table: "N/A - Document output"
      purpose: "Structured scores for categories N11-N14"
      fields:
        - name: "n11_examples"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Examples/Multishot score with evidence"
          test_requirement: "Test: Verify N11 has score and evidence"
        - name: "n12_cot"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Chain of Thought score with evidence"
          test_requirement: "Test: Verify N12 has score and evidence"
        - name: "n13_architecture"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Command-Skill Architecture score with evidence"
          test_requirement: "Test: Verify N13 has score and evidence"
        - name: "n14_antipatterns"
          type: "Object"
          constraints: "Required, score 1-10"
          description: "Anti-Patterns score with evidence"
          test_requirement: "Test: Verify N14 has score and evidence"

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
      metric: "Input files total < 8,000 lines (rubric + all 4 analyses)"
      test_requirement: "Test: Verify input file count and size"
      priority: "Critical"
```

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-414:** Scoring Rubric Extraction
  - **Why:** Provides scoring criteria for all 4 categories
  - **Status:** Backlog (Sprint 1)

- [x] **STORY-415:** /dev Command Analysis
  - **Why:** Provides evidence for N13
  - **Status:** Backlog (Sprint 2)

- [x] **STORY-416:** SKILL.md Analysis
  - **Why:** Provides evidence for N11, N12, N13, N14
  - **Status:** Backlog (Sprint 2)

- [x] **STORY-417:** Phase Files Analysis
  - **Why:** Provides evidence for N11, N12, N13
  - **Status:** Backlog (Sprint 2)

- [x] **STORY-418:** Reference Files Analysis
  - **Why:** Provides evidence for N14 (nested references)
  - **Status:** Backlog (Sprint 2)

### External Dependencies

None.

---

## Acceptance Criteria Verification Checklist

### AC#1: N11 Examples/Multishot

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Example count documented - **Phase:** 3
- [ ] Diversity assessed - **Phase:** 3
- [ ] `<example>` tag usage checked - **Phase:** 3

### AC#2: N12 Chain of Thought

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] `<thinking>` tag usage inventoried - **Phase:** 3
- [ ] Structured reasoning guidance assessed - **Phase:** 3

### AC#3: N13 Command-Skill Architecture

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Thin command pattern evaluated - **Phase:** 3
- [ ] Single responsibility assessed - **Phase:** 3
- [ ] Subagent scoping evaluated - **Phase:** 3

### AC#4: N14 Anti-Patterns

- [ ] Score assigned (1-10) - **Phase:** 3
- [ ] Windows paths checked - **Phase:** 3
- [ ] Too many options checked - **Phase:** 3
- [ ] Deeply nested references checked - **Phase:** 3
- [ ] Time-sensitive info checked - **Phase:** 3

---

**Checklist Progress:** 0/16 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] N11 Examples/Multishot scored with evidence and remediation
- [ ] N12 Chain of Thought scored with evidence and remediation
- [ ] N13 Command-Skill Architecture scored with evidence and remediation
- [ ] N14 Anti-Patterns scored with evidence and remediation
- [ ] Deliverable written to devforgeai/specs/requirements/dev-analysis/09-scores-n11-n14.md

### Quality
- [ ] All scores have quoted evidence
- [ ] Standard severity levels used
- [ ] No raw source files read

### Documentation
- [ ] Consistent scoring format across all 4 categories
- [ ] Summary table with all scores

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 10:55 | devforgeai-story-creation | Created | Story created from EPIC-066 Feature I | STORY-421.story.md |

## Notes

**Deliverable:**
- `devforgeai/specs/requirements/dev-analysis/09-scores-n11-n14.md`

**Sprint:** Sprint 3 (Scoring - Parallelizable)

**Inputs (ONLY — no raw source files):**
- `02-scoring-rubric.md` (from STORY-414)
- `03-dev-command-analysis.md` (from STORY-415)
- `04-skill-md-analysis.md` (from STORY-416)
- `05-phase-files-analysis.md` (from STORY-417)
- `06-reference-files-analysis.md` (from STORY-418)

**Can Execute In Parallel With:**
- STORY-419 (Scores N1-N5)
- STORY-420 (Scores N6-N10)

---

Story Template Version: 2.9
Last Updated: 2026-02-17
