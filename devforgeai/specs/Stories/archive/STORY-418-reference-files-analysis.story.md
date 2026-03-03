---
id: STORY-418
title: "Reference Files Analysis - Depth Map, Token Costs, Progressive Disclosure"
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

# Story: Reference Files Analysis - Depth Map, Token Costs, Progressive Disclosure

## Description

**As a** framework architect,
**I want** a detailed analysis of all reference files,
**so that** I understand the progressive disclosure depth, token costs, and optimization opportunities.

This analysis covers the reference layer of the devforgeai-development ecosystem (~50 files, ~20,280 lines), which is the largest content layer and primary source of context window optimization opportunities.

## Acceptance Criteria

### AC#1: Reference Depth Map

```xml
<acceptance_criteria id="AC1">
  <given>All reference files exist in .claude/skills/devforgeai-development/references/</given>
  <when>Reference depth is mapped</when>
  <then>Analysis documents: maximum chain depth, specific A→B→C chains, violations of one-level-deep rule, intermediate routing files (like _index.md)</then>
  <verification>
    <source_files>
      <file hint="Reference directory">.claude/skills/devforgeai-development/references/**/*.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- CURRENT (non-conformant): Reference chains go 3+ levels deep. Example chain: SKILL.md → phase-01-preflight.md → references/preflight/_index.md → references/preflight/01.0-project-root.md. This is a 3-level chain (SKILL.md → phase → index → sub-file), violating the one-level-deep rule.
  (Source: .claude/skills/devforgeai-development/references/preflight/_index.md, lines 1-4: "Total Original: 3,020 lines → Now decomposed into 18 files")
- TARGET (Anthropic-conformant): "File references are one level deep." References should be directly accessible from SKILL.md — no A→B→C chains.
  (Source: best-practices.md, line 1089; best-practices.md, lines 228-398)
- CONTEXT FILE CONSTRAINT: Progressive disclosure pattern requires "Main file ≤1000 lines, references on-demand" but does not explicitly limit depth. However, anti-patterns.md forbids circular dependencies and architecture-constraints.md mandates single responsibility.
  (Source: devforgeai/specs/context/source-tree.md; devforgeai/specs/context/anti-patterns.md)

---

### AC#2: Token Cost Estimate

```xml
<acceptance_criteria id="AC2">
  <given>All reference files have been inventoried with line counts</given>
  <when>Token cost is estimated</when>
  <then>Analysis documents: total lines if all loaded, estimated token count, comparison to Anthropic L3 guidance, loading scenarios (worst case, typical, optimal)</then>
  <verification>
    <source_files>
      <file hint="Reference directory">.claude/skills/devforgeai-development/references/**/*.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- CURRENT (non-conformant): If ALL reference files loaded simultaneously: ~20,280 lines of references + 3,910 lines of phases + 1,099 lines of SKILL.md = ~25,289 lines (~100K+ tokens). This vastly exceeds reasonable context window usage.
  (Source: .claude/skills/devforgeai-development/references/, wc -l total: 20,280)
- TARGET (Anthropic-conformant): Progressive disclosure ensures only relevant content occupies context. L1 metadata ~100 tokens, L2 instructions <5K tokens, L3 resources loaded as-needed with "effectively unlimited" budget — but each load should be targeted, not bulk.
  (Source: overview.md, lines 101-107)
- CONTEXT FILE CONSTRAINT: Token budget constraints — Skills <1000 lines, context files <600 lines. Reference files have no explicit cap but progressive disclosure pattern implies load-on-demand, not bulk loading.
  (Source: devforgeai/specs/context/tech-stack.md)

---

### AC#3: Reference File Summary Table

```xml
<acceptance_criteria id="AC3">
  <given>All reference files have been inventoried</given>
  <when>Summary table is generated</when>
  <then>Analysis documents: file path, line count, purpose, last accessed (if detectable), redundancy flags</then>
  <verification>
    <source_files>
      <file hint="Reference directory">.claude/skills/devforgeai-development/references/**/*.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- CURRENT (mixed): ~50 reference files ranging from 23 lines (01.3-workflow-adapt.md) to 1,676 lines (git-workflow-conventions.md). 5 files exceed 700 lines; 3 files exceed 1,000 lines. Some files may be redundant or overlap in content.
  (Source: .claude/skills/devforgeai-development/references/, wc -l output)
- TARGET (Anthropic-conformant): "If Claude never accesses a bundled file, it might be unnecessary or poorly signaled." Reference files should be concise and only exist if they serve a clear, distinct purpose.
  (Source: best-practices.md, lines 794-803)
- CONTEXT FILE CONSTRAINT: Subagent files target 100-300 lines, max 500 lines. While reference files are not subagents, the framework's general principle of size discipline applies.
  (Source: devforgeai/specs/context/coding-standards.md, lines 106-112)

---

### AC#4: Largest File Analysis

```xml
<acceptance_criteria id="AC4">
  <given>Reference files have been sorted by line count</given>
  <when>Top 5 largest files are analyzed</when>
  <then>Analysis documents: content breakdown, verbose sections, Claude-already-knows content, extraction/deletion opportunities</then>
  <verification>
    <source_files>
      <file hint="Largest reference files">.claude/skills/devforgeai-development/references/*.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- CURRENT (non-conformant): 5 largest reference files total 5,897 lines:
  - git-workflow-conventions.md (1,676 lines) — 3.4x over subagent max
  - phase-06-deferral-challenge.md (1,361 lines) — 2.7x over subagent max
  - tdd-red-phase.md (1,068 lines) — 2.1x over subagent max
  - tdd-patterns.md (1,013 lines) — 2.0x over subagent max
  - slash-command-argument-validation-pattern.md (779 lines) — 1.6x over subagent max
  (Source: .claude/skills/devforgeai-development/references/, wc -l output)
- TARGET (Anthropic-conformant): "Only add context Claude doesn't already have. Challenge each piece: Does Claude really need this explanation?" Large files likely contain verbose explanations of things Claude already knows.
  (Source: best-practices.md, lines 13-55)
- CONTEXT FILE CONSTRAINT: Extract to references/ when exceeding target. But these ARE reference files — they need further decomposition or conciseness editing.
  (Source: devforgeai/specs/context/coding-standards.md, line 112)

---

### AC#5: Preflight Sub-Reference Analysis

```xml
<acceptance_criteria id="AC5">
  <given>The preflight subdirectory has been analyzed</given>
  <when>Sub-reference pattern is evaluated</when>
  <then>Analysis documents: file count, total lines, 3-level chain pattern, _index.md routing purpose, alternatives to intermediate layer</then>
  <verification>
    <source_files>
      <file hint="Preflight subdirectory">.claude/skills/devforgeai-development/references/preflight/*.md</file>
    </source_files>
    <test_file>devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md</test_file>
  </verification>
</acceptance_criteria>
```

**Evidence Required:**
- CURRENT (non-conformant): Preflight directory contains 19 files totaling ~2,208 lines, accessed via a 3-level chain: SKILL.md body → phase-01-preflight.md (line 3: "Read references/preflight/_index.md") → _index.md → individual step files (01.0-project-root.md, 01.1-git-status.md, etc.). The _index.md file serves as an intermediate routing layer.
  (Source: .claude/skills/devforgeai-development/references/preflight/_index.md, lines 1-40)
- TARGET (Anthropic-conformant): "File references are one level deep." The preflight sub-reference pattern adds an unnecessary intermediate layer (_index.md). Phase-01 should reference sub-files directly, or the index should be inlined.
  (Source: best-practices.md, line 1089)
- CONTEXT FILE CONSTRAINT: Progressive disclosure pattern is documented in source-tree.md — "Main files concise, references deep." But depth is not the same as progressive disclosure; unnecessary intermediaries add loading overhead without value.
  (Source: devforgeai/specs/context/source-tree.md)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "ReferenceFilesAnalysis"
      table: "N/A - Document output"
      purpose: "Structured analysis of all ~50 reference files"
      fields:
        - name: "depth_map"
          type: "Object"
          constraints: "Required"
          description: "Reference chain depth analysis"
          test_requirement: "Test: Verify all chains documented"
        - name: "token_cost_estimate"
          type: "Object"
          constraints: "Required"
          description: "Token usage scenarios"
          test_requirement: "Test: Verify token estimates calculated"
        - name: "file_summary_table"
          type: "Table"
          constraints: "Required"
          description: "All reference files with metrics"
          test_requirement: "Test: Verify table has ~50 rows"
        - name: "largest_file_analysis"
          type: "Array"
          constraints: "Required, 5 items"
          description: "Top 5 file deep-dive"
          test_requirement: "Test: Verify 5 files analyzed"
        - name: "preflight_analysis"
          type: "Object"
          constraints: "Required"
          description: "Preflight subdirectory pattern analysis"
          test_requirement: "Test: Verify preflight chain documented"

  business_rules:
    - id: "BR-001"
      rule: "All reference files must be inventoried"
      trigger: "When completing analysis"
      validation: "Glob count matches table row count"
      test_requirement: "Test: Verify glob count = table rows"
      priority: "Critical"

    - id: "BR-002"
      rule: "Token estimates must use consistent calculation"
      trigger: "When estimating tokens"
      validation: "~4 chars = 1 token, documented formula"
      test_requirement: "Test: Verify token formula documented"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Analysis must handle ~20,280 lines across ~50 files"
      metric: "Complete analysis via sampling (not full content read)"
      test_requirement: "Test: Verify analysis uses sampling strategy"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Context Efficiency:**
- Input: Metadata only for most files (path + line count), full read for top 5 + preflight
- Output: < 1,500 lines analysis document

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-413:** Ecosystem Inventory
  - **Why:** Need file inventory with line counts
  - **Status:** Backlog (Sprint 1)

### External Dependencies

None.

### Technology Dependencies

None. Uses only Read, Glob, Grep, and Write tools.

---

## Test Strategy

### Verification Scenarios

1. **Completeness:** All 5 AC sections present in deliverable
2. **File count:** Summary table row count matches Glob count
3. **Token calculation:** Formula documented and consistently applied
4. **Depth chains:** At least 1 3-level chain documented (known to exist)

---

## Acceptance Criteria Verification Checklist

### AC#1: Reference Depth Map

- [ ] Maximum chain depth identified - **Phase:** 3
- [ ] Specific A→B→C chains documented - **Phase:** 3
- [ ] One-level-deep violations flagged - **Phase:** 3
- [ ] Intermediate routing files identified - **Phase:** 3

### AC#2: Token Cost Estimate

- [ ] Total lines calculated - **Phase:** 3
- [ ] Token estimate formula documented - **Phase:** 3
- [ ] Loading scenarios (worst/typical/optimal) - **Phase:** 3
- [ ] Comparison to Anthropic L3 guidance - **Phase:** 3

### AC#3: Reference File Summary Table

- [ ] All ~50 files in table - **Phase:** 3
- [ ] Line counts accurate - **Phase:** 3
- [ ] Purpose documented per file - **Phase:** 3
- [ ] Redundancy flags where applicable - **Phase:** 3

### AC#4: Largest File Analysis

- [ ] Top 5 files identified - **Phase:** 3
- [ ] Content breakdown per file - **Phase:** 3
- [ ] Verbose sections identified - **Phase:** 3
- [ ] Optimization opportunities documented - **Phase:** 3

### AC#5: Preflight Sub-Reference Analysis

- [ ] File count and total lines - **Phase:** 3
- [ ] 3-level chain documented - **Phase:** 3
- [ ] _index.md purpose analyzed - **Phase:** 3
- [ ] Alternatives proposed - **Phase:** 3

---

**Checklist Progress:** 0/20 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Reference depth map complete with chain documentation
- [ ] Token cost estimate complete with scenarios
- [ ] Reference file summary table complete with all files
- [ ] Largest file analysis complete for top 5
- [ ] Preflight sub-reference analysis complete
- [ ] Deliverable written to devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md

### Quality
- [ ] File count verified via Glob
- [ ] Token formula documented
- [ ] Depth chains verified with file paths

### Documentation
- [ ] Analysis follows output template structure
- [ ] All gaps have severity ratings

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 10:40 | devforgeai-story-creation | Created | Story created from EPIC-066 Feature F | STORY-418.story.md |

## Notes

**Design Decisions:**
- Use sampling strategy for 20K+ lines (don't read all content)
- Focus on depth violations as primary conformance gap
- Token estimates use ~4 chars = 1 token approximation

**Deliverable:**
- `devforgeai/specs/requirements/dev-analysis/06-reference-files-analysis.md`

**Sprint:** Sprint 2 (Analysis - Parallelizable)

**Inputs:**
- `.claude/skills/devforgeai-development/references/**/*.md` (~50 files, ~20,280 lines)
- `01-ecosystem-inventory.md` (from STORY-413)

**Can Execute In Parallel With:**
- STORY-415 (/dev Command Analysis)
- STORY-416 (SKILL.md Analysis)
- STORY-417 (Phase Files Analysis)

---

Story Template Version: 2.9
Last Updated: 2026-02-17
