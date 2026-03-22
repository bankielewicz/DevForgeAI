---
id: STORY-407
title: Add Treelint JSON Schema Validation to Story Requirements Analyst
type: refactor
epic: EPIC-063
sprint: Backlog
status: QA Approved
priority: Low
points: 1
created: 2026-02-08
updated: 2026-02-08
assignee: unassigned
tags: [framework, subagent, treelint, validation, refactor]
source_recommendation: REC-STORY368-002
template_version: "2.8"
---

# STORY-407: Add Treelint JSON Schema Validation to Story Requirements Analyst

## Description

Add a conditional Treelint JSON schema validation step to the story-requirements-analyst subagent. When stories reference Treelint output fields, cross-reference field names against the canonical schema to prevent typos.

<!-- provenance>
  <origin document="EPIC-063" section="Feature 9">
    <quote>When stories reference Treelint output fields, cross-reference field names against the canonical schema to prevent typos</quote>
    <line_reference>lines 550-604</line_reference>
  </origin>
  <decision rationale="Catch typos early at story creation, not during development">
    <selected>Conditional schema validation in story-requirements-analyst</selected>
    <rejected>Validate at development time only</rejected>
    <trade_off>Creation-time overhead vs development-time failures</trade_off>
  </decision>
</provenance -->

## User Story

**As a** DevForgeAI story author,
**I want** the story-requirements-analyst subagent to conditionally validate Treelint field names against the canonical schema,
**So that** typos in Treelint field references are caught at story creation time rather than propagating into acceptance criteria and failing during development.

## Acceptance Criteria

<acceptance_criteria id="AC1" title="Non-Treelint stories skip validation entirely">
  <given>A feature description containing no Treelint-related keywords</given>
  <when>The story-requirements-analyst subagent processes the description</when>
  <then>No Treelint schema validation executes, no schema file is loaded, zero additional overhead</then>
  <verification>
    <method>Process non-Treelint story, verify no Read() to treelint-search-patterns.md</method>
    <expected_result>Validation step skipped entirely</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/story-requirements-analyst.md" hint="Add conditional detection"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC2" title="Treelint keyword detection triggers schema loading">
  <given>A feature description containing Treelint-related keywords (treelint, AST, dependency graph, etc.)</given>
  <when>The story-requirements-analyst processes the description</when>
  <then>The subagent loads canonical field definitions from `src/claude/agents/references/treelint-search-patterns.md`</then>
  <verification>
    <method>Process Treelint story, verify Read() to schema file</method>
    <expected_result>Schema file loaded for cross-reference</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/references/treelint-search-patterns.md" hint="Canonical schema source"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC3" title="Field name mismatches produce non-blocking warnings">
  <given>The subagent detects a Treelint field reference that doesn't match canonical schema</given>
  <when>The cross-reference check completes</when>
  <then>Non-blocking WARNING emitted with field name and closest match; generation continues</then>
  <verification>
    <method>Test with typo like "dependecies" instead of "dependencies"</method>
    <expected_result>WARNING output, story generation completes</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/story-requirements-analyst.md" hint="Warning output format"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC4" title="Valid Treelint field references pass silently">
  <given>All Treelint field references match canonical field names exactly</given>
  <when>The cross-reference check completes</when>
  <then>No warning emitted, validation produces zero visible output (silent pass)</then>
  <verification>
    <method>Test with valid field names (results, count, name)</method>
    <expected_result>No warnings, silent pass</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/references/treelint-search-patterns.md" hint="Valid field list"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC5" title="Content-only output contract preserved">
  <given>Treelint schema validation is enabled</given>
  <when>The subagent completes all processing</when>
  <then>Subagent returns ONLY markdown content (no file creation), all 4 required sections present</then>
  <verification>
    <method>Verify output conforms to requirements-analyst-contract.yaml</method>
    <expected_result>Content only, no file creation</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml" hint="Lines 56-59: output contract"/>
  </source_files>
</acceptance_criteria>

## Technical Specification

### Component Overview

| Component | Type | Description |
|-----------|------|-------------|
| story-requirements-analyst.md | Subagent | Add conditional Treelint schema validation |

### Technical Details

```yaml
technical_specification:
  version: "2.0"
  components:
    - type: Subagent
      name: story-requirements-analyst
      file_path: src/claude/agents/story-requirements-analyst.md
      description: Add conditional Treelint field validation step
      dependencies:
        - src/claude/agents/references/treelint-search-patterns.md (Read-only)
        - src/claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml
      test_requirement: Non-Treelint stories skip validation, Treelint stories trigger schema check

  business_rules:
    - rule: Keyword detection gate
      description: Treelint keywords (treelint, AST, dependency graph, etc.) trigger validation
      test_requirement: Feature without keywords triggers no schema load

    - rule: Non-blocking warnings
      description: Field mismatches produce warnings, never halt
      test_requirement: Story with typo produces warning but completes

    - rule: Content-only output
      description: Subagent returns markdown only, no file creation
      test_requirement: Output conforms to requirements-analyst-contract.yaml

  non_functional_requirements:
    - category: Performance
      requirement: Minimal overhead
      metric: < 200ms for Treelint stories, 0ms for non-Treelint
      test_requirement: Measure validation step duration
```

### Treelint Keyword Detection

Keywords (case-insensitive, word-boundary for AST):
- `treelint`
- `AST` (with word boundary: `\bAST\b`)
- `dependency graph`
- `function signatures`
- `syntax tree`
- `code search`

### Canonical Field Set

Fields from `treelint-search-patterns.md`:
`results`, `type`, `name`, `file`, `lines`, `start`, `end`, `signature`, `body`, `count`, `query`, `members`, `methods`, `properties`, `class_methods`, `bases`, `files`, `path`, `rank`, `score`, `references`, `complexity`, `total_files`, `returned`

> **Note:** These fields are documented in the 'Output Format' or 'Field Reference' section of `src/claude/agents/references/treelint-search-patterns.md`. During implementation, use Grep to locate the exact section containing the canonical field definitions.

### Warning Format

```
WARNING: Story references Treelint field '{field_name}' which does not match canonical schema. Closest match: '{closest_field}'
```

### Files to Modify

| File | Action | Description |
|------|--------|-------------|
| `src/claude/agents/story-requirements-analyst.md` | Edit | Add conditional Treelint validation step |

## Edge Cases

1. **AST in unrelated words:** Detection must use word-boundary matching (`\bAST\b`) to avoid matching LAST, CAST, BLAST.

2. **Schema file missing:** Log warning, skip validation, continue generating output.

3. **Multiple field mismatches:** Each mismatch produces individual WARNING line.

4. **Treelint mention but no field references:** Load schema, find zero fields, silent pass.

5. **Fields in code blocks:** Still detect and validate fields inside backtick regions.

6. **Case sensitivity:** Treelint fields are case-sensitive. Warn on case mismatches.

## Non-Functional Requirements

| Category | Requirement | Metric |
|----------|-------------|--------|
| Performance | Treelint overhead | < 200ms for validation step |
| Performance | Non-Treelint overhead | 0ms (step skipped) |
| Reliability | Schema missing | Graceful degradation with warning |
| Scalability | Future fields | Auto-discovered from updated schema file |

## Definition of Done

### Implementation
- [x] Keyword detection step added with 6 keywords - Completed: 6 Treelint keywords (treelint, AST, dependency graph, function signatures, syntax tree, code search) with conditional gate
- [x] Word-boundary matching for AST - Completed: \bAST\b pattern prevents false matches (LAST, CAST, BLAST)
- [x] Schema loading conditional on keyword detection - Completed: Read() to treelint-search-patterns.md only when keywords detected
- [x] Field cross-reference against canonical set - Completed: 24 canonical fields validated against story references
- [x] Non-blocking warning output format - Completed: WARNING format with field name and closest match suggestion
- [x] Content-only output contract preserved - Completed: No file creation, all 4 required sections present

### Quality
- [x] Non-Treelint stories: zero overhead - Completed: Validation step skipped entirely when no keywords detected
- [x] Field mismatches: WARNING, not HALT - Completed: Non-blocking warnings, story generation continues
- [x] Valid fields: silent pass - Completed: Zero visible output for valid field references
- [x] All 4 required sections still present in output - Completed: Verified output conforms to requirements-analyst-contract.yaml

### Testing
- [x] Non-Treelint story: no schema Read() - Completed: Test verifies no schema file loading for non-Treelint descriptions
- [x] Treelint story: schema loaded - Completed: Test verifies Read() to treelint-search-patterns.md
- [x] Typo "dependecies": WARNING with closest match - Completed: Test verifies WARNING output with "dependencies" suggestion
- [x] Valid "results": silent pass - Completed: Test verifies zero warnings for valid field names
- [x] Output conforms to contract (content only) - Completed: Test verifies no file creation, 4 sections present

### Documentation
- [x] Validation step documented in subagent - Completed: Treelint Schema Validation section added to story-requirements-analyst.md

## Notes

- **Source Recommendation:** REC-STORY368-002 from STORY-368 Phase 09 framework-analyst analysis
- **Root Cause:** Treelint field typos detected late during development
- **Impact:** Catch typos at story creation, not development time

## Key References

| Reference | Path | Relevance |
|-----------|------|-----------|
| Story Requirements Analyst | `src/claude/agents/story-requirements-analyst.md` | Target file |
| Treelint Search Patterns | `src/claude/agents/references/treelint-search-patterns.md` | Canonical schema (319 lines) |
| Requirements Analyst Contract | `src/claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml` | Output contract |

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-10
**Branch:** main

- [x] Keyword detection step added with 6 keywords - Completed: 6 Treelint keywords (treelint, AST, dependency graph, function signatures, syntax tree, code search) with conditional gate
- [x] Word-boundary matching for AST - Completed: \bAST\b pattern prevents false matches (LAST, CAST, BLAST)
- [x] Schema loading conditional on keyword detection - Completed: Read() to treelint-search-patterns.md only when keywords detected
- [x] Field cross-reference against canonical set - Completed: 24 canonical fields validated against story references
- [x] Non-blocking warning output format - Completed: WARNING format with field name and closest match suggestion
- [x] Content-only output contract preserved - Completed: No file creation, all 4 required sections present
- [x] Non-Treelint stories: zero overhead - Completed: Validation step skipped entirely when no keywords detected
- [x] Field mismatches: WARNING, not HALT - Completed: Non-blocking warnings, story generation continues
- [x] Valid fields: silent pass - Completed: Zero visible output for valid field references
- [x] All 4 required sections still present in output - Completed: Verified output conforms to requirements-analyst-contract.yaml
- [x] Non-Treelint story: no schema Read() - Completed: Test verifies no schema file loading for non-Treelint descriptions
- [x] Treelint story: schema loaded - Completed: Test verifies Read() to treelint-search-patterns.md
- [x] Typo "dependecies": WARNING with closest match - Completed: Test verifies WARNING output with "dependencies" suggestion
- [x] Valid "results": silent pass - Completed: Test verifies zero warnings for valid field names
- [x] Output conforms to contract (content only) - Completed: Test verifies no file creation, 4 sections present
- [x] Validation step documented in subagent - Completed: Treelint Schema Validation section added to story-requirements-analyst.md

### TDD Workflow Summary

**Phase 02 (Red):** 37 grep-based tests generated across 5 AC suites following STORY-368 convention
**Phase 03 (Green):** Treelint schema validation section added to story-requirements-analyst.md via backend-architect
**Phase 04 (Refactor):** Code reviewed and refined by refactoring-specialist and code-reviewer
**Phase 05 (Integration):** All 37 tests passing, 5 integration points verified

### Files Modified

- `src/claude/agents/story-requirements-analyst.md` - Added conditional Treelint validation step

### Test Results

- **Total tests:** 37
- **Pass rate:** 100%
- **Test suites:** 5 (AC1-AC5)

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-08 | claude/opus | Story Creation | Initial story created from EPIC-063 Feature 9 | STORY-407-add-treelint-schema-validation.story.md |
| 2026-02-10 | .claude/qa-result-interpreter | QA Deep | PASSED: 37/37 tests, 0 violations, 2/2 validators | devforgeai/qa/reports/STORY-407-qa-report.md |
| 2026-02-10 | .claude/opus | DoD Update (Phase 07) | Development complete, 16/16 DoD items marked, Implementation Notes added | STORY-407-add-treelint-schema-validation.story.md |
