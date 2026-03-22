---
id: STORY-414
title: "Scoring Rubric Extraction - Extract 14 Categories (N1-N14) from Anthropic Sources"
type: documentation
epic: EPIC-066
sprint: Sprint-1
status: Backlog
points: 3
depends_on: []
priority: High
advisory: false
assigned_to: DevForgeAI AI Agent
created: 2026-02-17
format_version: "2.9"
---

# Story: Scoring Rubric Extraction - Extract 14 Categories (N1-N14) from Anthropic Sources

## Description

**As a** framework architect,
**I want** all 14 scoring categories extracted with exact quoted text and line numbers from Anthropic source documents,
**so that** Sprint 3 scoring stories have a single compressed reference and never need to re-read large source files.

This rubric becomes the ONLY reference for Sprint 3 scoring stories. Once extracted, no story should re-read Anthropic source documents — they only read this compressed rubric.

## Acceptance Criteria

### AC#1: N1 — Naming Convention Rubric Extracted

```xml
<acceptance_criteria id="AC1">
  <given>Anthropic best-practices.md exists at .claude/skills/claude-code-terminal-expert/references/skills/best-practices.md</given>
  <when>N1 rubric is extracted</when>
  <then>Exact quoted text from best-practices.md lines 154-181 is captured with line numbers and scoring criteria</then>
  <verification>
    <source_files>
      <file hint="Anthropic guidelines">.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- CURRENT (non-conformant): `name: devforgeai-development` (Source: SKILL.md, line 2)
- TARGET (Anthropic-conformant): Gerund form recommended — e.g., `developing-features` or `implementing-tdd`
  (Source: best-practices.md, lines 156-165)
- CONTEXT FILE CONSTRAINT: Naming convention `devforgeai-[phase]` is LOCKED
  (Source: devforgeai/specs/context/coding-standards.md, line 117). Rename authorized by ADR-017 (Accepted) — see devforgeai/specs/adrs/ADR-017-skill-gerund-naming-no-prefix.md.

---

### AC#2: N2 — Description Quality Rubric Extracted

```xml
<acceptance_criteria id="AC2">
  <given>Anthropic best-practices.md exists</given>
  <when>N2 rubric is extracted</when>
  <then>Exact quoted text from best-practices.md lines 183-227 is captured, including third-person requirement (line 188) and discovery mechanism role (line 197)</then>
  <verification>
    <source_files>
      <file hint="Anthropic guidelines">.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: N3 — SKILL.md Size Rubric Extracted

```xml
<acceptance_criteria id="AC3">
  <given>Anthropic best-practices.md exists</given>
  <when>N3 rubric is extracted</when>
  <then>Exact quoted text from best-practices.md lines 233-235 and 1074-1076 is captured with 500-line target</then>
  <verification>
    <source_files>
      <file hint="Anthropic guidelines">.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- CURRENT: SKILL.md is 1,099 lines (2.2x over 500-line target)
- CONTEXT FILE CONSTRAINT: Skills target 500-800 lines, max 1,000 lines
  (Source: devforgeai/specs/context/coding-standards.md, lines 106-107)

---

### AC#4: N4 — Progressive Disclosure Rubric Extracted

```xml
<acceptance_criteria id="AC4">
  <given>Anthropic best-practices.md and overview.md exist</given>
  <when>N4 rubric is extracted</when>
  <then>Exact quoted text from best-practices.md lines 228-398 and overview.md lines 42-107 is captured, including three-level loading model (L1/L2/L3), one-level-deep reference rule, TOC guidance</then>
  <verification>
    <source_files>
      <file hint="Anthropic best practices">.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md</file>
      <file hint="Anthropic overview">.claude/skills/claude-code-terminal-expert/references/skills/overview.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: N5 — Conciseness Rubric Extracted

```xml
<acceptance_criteria id="AC5">
  <given>Anthropic best-practices.md exists</given>
  <when>N5 rubric is extracted</when>
  <then>Exact quoted text from best-practices.md lines 13-55 is captured, including "challenge each piece" criteria and good/bad examples</then>
  <verification>
    <source_files>
      <file hint="Anthropic guidelines">.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: N6 — Degrees of Freedom Rubric Extracted

```xml
<acceptance_criteria id="AC6">
  <given>Anthropic best-practices.md exists</given>
  <when>N6 rubric is extracted</when>
  <then>Exact quoted text from best-practices.md lines 57-122 is captured, including highway/bridge/field metaphors for HIGH/MEDIUM/LOW freedom</then>
  <verification>
    <source_files>
      <file hint="Anthropic guidelines">.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#7: N7 — Workflow Structure Rubric Extracted

```xml
<acceptance_criteria id="AC7">
  <given>Anthropic best-practices.md exists</given>
  <when>N7 rubric is extracted</when>
  <then>Exact quoted text from best-practices.md lines 399-488 is captured, including checklist pattern and sequential step guidance</then>
  <verification>
    <source_files>
      <file hint="Anthropic guidelines">.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#8: N8 — Feedback Loops Rubric Extracted

```xml
<acceptance_criteria id="AC8">
  <given>Anthropic best-practices.md exists</given>
  <when>N8 rubric is extracted</when>
  <then>Exact quoted text from best-practices.md lines 492-533 is captured, including "run validator → fix errors → repeat" pattern</then>
  <verification>
    <source_files>
      <file hint="Anthropic guidelines">.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#9: N9 — XML Tags Rubric Extracted

```xml
<acceptance_criteria id="AC9">
  <given>Anthropic prompt-engineering/use-xml-tags.md exists</given>
  <when>N9 rubric is extracted</when>
  <then>Key guidance from use-xml-tags.md is captured, including clarity, accuracy, flexibility, parseability benefits</then>
  <verification>
    <source_files>
      <file hint="XML tags guidance">.claude/skills/claude-code-terminal-expert/references/prompt-engineering/use-xml-tags.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#10: N10 — Role Prompting Rubric Extracted

```xml
<acceptance_criteria id="AC10">
  <given>Anthropic prompt-engineering/give-claude-a-role.md exists</given>
  <when>N10 rubric is extracted</when>
  <then>Key guidance from give-claude-a-role.md is captured, including system parameter usage and domain expert transformation</then>
  <verification>
    <source_files>
      <file hint="Role prompting guidance">.claude/skills/claude-code-terminal-expert/references/prompt-engineering/give-claude-a-role.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#11: N11 — Examples/Multishot Rubric Extracted

```xml
<acceptance_criteria id="AC11">
  <given>Anthropic prompt-engineering/Use-examples-multishot prompting-to-guide-Claudes-behavior.md exists</given>
  <when>N11 rubric is extracted</when>
  <then>Key guidance is captured, including 3-5 examples guidance, example tag wrapping</then>
  <verification>
    <source_files>
      <file hint="Multishot prompting">.claude/skills/claude-code-terminal-expert/references/prompt-engineering/Use-examples-multishot prompting-to-guide-Claudes-behavior.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#12: N12 — Chain of Thought Rubric Extracted

```xml
<acceptance_criteria id="AC12">
  <given>Anthropic prompt-engineering/chain-of-thought.md exists</given>
  <when>N12 rubric is extracted</when>
  <then>Key guidance is captured, including structured CoT with thinking and answer tags</then>
  <verification>
    <source_files>
      <file hint="Chain of thought">.claude/skills/claude-code-terminal-expert/references/prompt-engineering/chain-of-thought.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#13: N13 — Command-Skill Architecture Rubric Extracted

```xml
<acceptance_criteria id="AC13">
  <given>DevForgeAI architecture-constraints.md exists</given>
  <when>N13 rubric is extracted</when>
  <then>Architecture constraints captured: Commands <500 lines, thin orchestrators; Skills single responsibility; Subagents least-privilege</then>
  <verification>
    <source_files>
      <file hint="Architecture constraints">devforgeai/specs/context/architecture-constraints.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#14: N14 — Anti-Patterns Rubric Extracted

```xml
<acceptance_criteria id="AC14">
  <given>Anthropic best-practices.md exists</given>
  <when>N14 rubric is extracted</when>
  <then>Exact quoted text from best-practices.md lines 805-831 is captured, including Windows paths, too many options, deeply nested references, time-sensitive info</then>
  <verification>
    <source_files>
      <file hint="Anthropic guidelines">.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "ScoringRubric"
      table: "N/A - Document output"
      purpose: "Structured rubric for 14 scoring categories"
      fields:
        - name: "category_id"
          type: "String"
          constraints: "Required, N1-N14"
          description: "Scoring category identifier"
        - name: "category_name"
          type: "String"
          constraints: "Required"
          description: "Human-readable category name"
        - name: "quoted_criteria"
          type: "Text"
          constraints: "Required, exact quote from source"
          description: "Anthropic best practice criteria text"
        - name: "source_file"
          type: "String"
          constraints: "Required, valid file path"
          description: "Source document path"
        - name: "source_lines"
          type: "String"
          constraints: "Required, lines X-Y format"
          description: "Line range in source document"
        - name: "scoring_scale"
          type: "String"
          constraints: "Required, 1-10 scale explanation"
          description: "How to score 1-10 for this category"
          test_requirement: "Test: Verify each category has scoring guidance"

  business_rules:
    - id: "BR-001"
      rule: "All 14 categories (N1-N14) must have extracted criteria"
      trigger: "When rubric document is finalized"
      validation: "Count categories in document = 14"
      test_requirement: "Test: Document contains exactly 14 category sections"
      priority: "Critical"

    - id: "BR-002"
      rule: "Quoted text must be exact (word-for-word) from source documents"
      trigger: "When extracting criteria"
      validation: "Text comparison with source files"
      test_requirement: "Test: Spot-check 3 quotes against source files"
      priority: "Critical"

    - id: "BR-003"
      rule: "Line numbers must be accurate and verifiable"
      trigger: "When recording source lines"
      validation: "Read source file at line numbers, verify content matches"
      test_requirement: "Test: Line numbers correspond to actual content"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Rubric must be self-contained (no external lookups needed)"
      metric: "Sprint 3 stories need only read this file, not source documents"
      test_requirement: "Test: Sprint 3 stories can score without reading Anthropic sources"
      priority: "Critical"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Context Efficiency:**
- Rubric document: < 2,000 lines (compressed from ~3,000 lines of source)
- Single file loading for Sprint 3 stories

### Reliability

**Accuracy:**
- All quotes word-for-word accurate
- All line numbers verifiable

---

## Dependencies

### Prerequisite Stories

None. This story can execute in parallel with STORY-413 (both are Sprint 1).

### External Dependencies

- [x] **Anthropic reference files:** Must exist at .claude/skills/claude-code-terminal-expert/references/
  - **Status:** Complete (existing files)

### Technology Dependencies

None. Uses only Read and Write tools.

---

## Test Strategy

### Verification Scenarios

1. **Category count:** Exactly 14 categories extracted
2. **Quote accuracy:** 3+ quotes spot-checked against source files
3. **Line number accuracy:** 3+ line ranges verified against source files
4. **Completeness:** All required fields present per category

---

## Acceptance Criteria Verification Checklist

### AC#1-5: Categories N1-N5

- [ ] N1 Naming Convention extracted with quotes and line numbers - **Phase:** 3
- [ ] N2 Description Quality extracted with quotes and line numbers - **Phase:** 3
- [ ] N3 SKILL.md Size extracted with quotes and line numbers - **Phase:** 3
- [ ] N4 Progressive Disclosure extracted with quotes and line numbers - **Phase:** 3
- [ ] N5 Conciseness extracted with quotes and line numbers - **Phase:** 3

### AC#6-10: Categories N6-N10

- [ ] N6 Degrees of Freedom extracted with quotes and line numbers - **Phase:** 3
- [ ] N7 Workflow Structure extracted with quotes and line numbers - **Phase:** 3
- [ ] N8 Feedback Loops extracted with quotes and line numbers - **Phase:** 3
- [ ] N9 XML Tags extracted with quotes and line numbers - **Phase:** 3
- [ ] N10 Role Prompting extracted with quotes and line numbers - **Phase:** 3

### AC#11-14: Categories N11-N14

- [ ] N11 Examples/Multishot extracted with quotes and line numbers - **Phase:** 3
- [ ] N12 Chain of Thought extracted with quotes and line numbers - **Phase:** 3
- [ ] N13 Command-Skill Architecture extracted with quotes and line numbers - **Phase:** 3
- [ ] N14 Anti-Patterns extracted with quotes and line numbers - **Phase:** 3

---

**Checklist Progress:** 0/14 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] All 14 categories (N1-N14) extracted with exact quoted criteria
- [ ] Source file paths and line numbers documented for each category
- [ ] Scoring scale guidance (1-10) provided for each category
- [ ] Context file constraints noted where applicable
- [ ] Deliverable written to devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md

### Quality
- [ ] All 14 categories present and complete
- [ ] Quote accuracy verified (spot-check 3+ quotes)
- [ ] Line numbers verified (spot-check 3+ ranges)

### Documentation
- [ ] Rubric is self-contained (no external lookups needed for scoring)
- [ ] Format consistent across all 14 categories

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 10:20 | devforgeai-story-creation | Created | Story created from EPIC-066 Feature B | STORY-414.story.md |

## Notes

**Design Decisions:**
- Rubric is intentionally verbose (includes full quoted criteria) to eliminate Sprint 3 source file reads
- Context file constraints included to flag where ADRs may be needed

**Deliverable:**
- `devforgeai/specs/requirements/dev-analysis/02-scoring-rubric.md`

**Sprint:** Sprint 1 (Foundation)

**Anthropic Reference Files to Read:**
- `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md` (1,140 lines)
- `.claude/skills/claude-code-terminal-expert/references/skills/overview.md` (345 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/*.md` (13 files, ~1,200 lines)

**Related Stories:**
- All Sprint 3 stories (STORY-419, 420, 421) depend on this rubric

---

Story Template Version: 2.9
Last Updated: 2026-02-17
