---
id: STORY-360
title: Validate Context File Updates After Treelint Integration
type: documentation
epic: EPIC-056
sprint: Backlog
status: QA Approved
points: 2
depends_on: ["STORY-357", "STORY-358", "STORY-359"]
priority: High
advisory: false
assigned_to: Unassigned
created: 2026-02-04
format_version: "2.8"
---

# Story: Validate Context File Updates After Treelint Integration

## Description

**As a** DevForgeAI framework maintainer,
**I want** to validate that all 6 constitutional context files remain consistent, syntactically valid, and free of contradictions after the Treelint-related modifications from STORY-357, STORY-358, and STORY-359,
**so that** framework integrity is preserved and downstream skills, subagents, and validation tools can rely on accurate context constraints without encountering broken references or conflicting guidance.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-009" section="treelint-integration">
    <quote>"Zero framework validation failures after context file updates"</quote>
    <line_reference>EPIC-056, Success Metric 4</line_reference>
    <quantified_impact>Ensures 100% validation pass rate for all 6 context files after Treelint integration changes</quantified_impact>
  </origin>

  <decision rationale="final-validation-gate">
    <selected>Dedicated validation story as final gate before EPIC-056 completion</selected>
    <rejected alternative="inline-validation-per-story">
      Per-story validation would miss cross-file contradictions introduced across multiple stories
    </rejected>
    <trade_off>Adds a dependency bottleneck (must wait for all 3 predecessor stories) but catches cross-file issues</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: All 6 Context Files Pass Syntax Validation

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>STORY-357, STORY-358, and STORY-359 have been completed and merged</given>
  <when>the context-validator subagent is invoked against all 6 context files in devforgeai/specs/context/</when>
  <then>all 6 files (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md) pass syntax validation with zero CRITICAL or HIGH violations</then>
  <verification>
    <source_files>
      <file hint="tech-stack">devforgeai/specs/context/tech-stack.md</file>
      <file hint="source-tree">devforgeai/specs/context/source-tree.md</file>
      <file hint="dependencies">devforgeai/specs/context/dependencies.md</file>
      <file hint="coding-standards">devforgeai/specs/context/coding-standards.md</file>
      <file hint="architecture-constraints">devforgeai/specs/context/architecture-constraints.md</file>
      <file hint="anti-patterns">devforgeai/specs/context/anti-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-360/test_ac1_syntax_validation.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: LOCKED Markers Remain Intact in All Files

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>modifications were made to source-tree.md and anti-patterns.md</given>
  <when>each of the 6 context files is scanned for the **Status**: LOCKED marker in its header</when>
  <then>every file contains exactly one **Status**: LOCKED marker within the first 10 lines, and no file has the marker removed, altered, or relocated</then>
  <verification>
    <source_files>
      <file hint="All 6 context files">devforgeai/specs/context/</file>
    </source_files>
    <test_file>tests/STORY-360/test_ac2_locked_markers.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Version Numbers Updated in Modified Files Only

```xml
<acceptance_criteria id="AC3" implements="COMP-001">
  <given>source-tree.md was modified by STORY-357/358 and anti-patterns.md by STORY-359</given>
  <when>version metadata is inspected across all 6 context files</when>
  <then>source-tree.md shows version >= 3.6 (incremented from 3.5), anti-patterns.md shows version >= 1.1 (incremented from 1.0), and the 4 unmodified files retain their original versions (tech-stack.md v1.4, dependencies.md v1.1, coding-standards.md v1.2, architecture-constraints.md v1.0)</then>
  <verification>
    <source_files>
      <file hint="All 6 context files">devforgeai/specs/context/</file>
    </source_files>
    <test_file>tests/STORY-360/test_ac3_version_numbers.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Last Updated Dates Updated in Modified Files Only

```xml
<acceptance_criteria id="AC4" implements="COMP-001">
  <given>source-tree.md and anti-patterns.md were modified as part of EPIC-056</given>
  <when>the Last Updated metadata field is inspected in all 6 context files</when>
  <then>source-tree.md and anti-patterns.md show Last Updated dates equal to or later than their predecessor story completion dates, and the 4 unmodified files retain their original dates</then>
  <verification>
    <source_files>
      <file hint="All 6 context files">devforgeai/specs/context/</file>
    </source_files>
    <test_file>tests/STORY-360/test_ac4_last_updated_dates.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: No Circular References or Contradictions Between Files

```xml
<acceptance_criteria id="AC5" implements="COMP-001">
  <given>source-tree.md references .treelint/ directory and anti-patterns.md includes Treelint guidance</given>
  <when>cross-file consistency is verified between tech-stack.md, source-tree.md, dependencies.md, and anti-patterns.md</when>
  <then>all Treelint references are consistent (tool name spelling, version constraints v0.12.0+, ADR-013 references match), no file contradicts another (anti-patterns.md does not forbid what tech-stack.md approves), and no circular reference chains exist</then>
  <verification>
    <source_files>
      <file hint="Cross-reference check">devforgeai/specs/context/tech-stack.md</file>
      <file hint="Cross-reference check">devforgeai/specs/context/source-tree.md</file>
      <file hint="Cross-reference check">devforgeai/specs/context/dependencies.md</file>
      <file hint="Cross-reference check">devforgeai/specs/context/anti-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-360/test_ac5_cross_file_consistency.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "ContextFileValidator"
      file_path: "Invoked via context-validator subagent"
      interface: "Task(subagent_type='context-validator')"
      lifecycle: "On-demand"
      dependencies:
        - "Read tool"
        - "Grep tool"
        - "Glob tool"
      requirements:
        - id: "SVC-001"
          description: "Read and validate all 6 context files for LOCKED marker presence"
          testable: true
          test_requirement: "Test: Each file contains **Status**: LOCKED within first 10 lines"
          priority: "Critical"
        - id: "SVC-002"
          description: "Verify version numbers are correct post-EPIC-056"
          testable: true
          test_requirement: "Test: source-tree.md >= v3.6, anti-patterns.md >= v1.1, others unchanged"
          priority: "Critical"
        - id: "SVC-003"
          description: "Detect cross-file contradictions in Treelint references"
          testable: true
          test_requirement: "Test: Treelint name, version, ADR-013 consistent across 4 files"
          priority: "High"
        - id: "SVC-004"
          description: "Verify Last Updated dates current in modified files"
          testable: true
          test_requirement: "Test: Modified file dates >= story completion date; unmodified dates unchanged"
          priority: "High"
        - id: "SVC-005"
          description: "Produce structured validation report with per-file pass/fail"
          testable: true
          test_requirement: "Test: Report contains 6 file entries, each with PASS/FAIL status"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Validation must be read-only — zero writes to context files"
      trigger: "Any validation execution"
      validation: "No Write/Edit tool calls during validation"
      error_handling: "HALT if validation attempts to modify any file"
      test_requirement: "Test: Verify no Write/Edit calls in validation execution"
      priority: "Critical"
    - id: "BR-002"
      rule: "All 6 files must be validated — no short-circuit on first failure"
      trigger: "Validation encounters a failing file"
      validation: "All 6 files have validation results in report"
      error_handling: "Continue validation of remaining files after failure"
      test_requirement: "Test: Report always contains exactly 6 entries regardless of failures"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Full validation of all 6 context files completes quickly"
      metric: "< 30 seconds total execution time"
      test_requirement: "Test: Time validation execution, verify < 30s"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Deterministic results on identical file state"
      metric: "100% reproducibility — same input produces same output"
      test_requirement: "Test: Run validation twice, compare reports for identical results"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance
- Full validation: < 30 seconds total execution time
- Per-file check: < 5 seconds each
- Cross-file scan: < 10 seconds for all comparisons
- Read-only operations only (no file locks)

### Security
- Zero writes to devforgeai/specs/context/ during validation
- File access scoped to context/ and adrs/ directories only
- No credential exposure in validation output

### Reliability
- Deterministic: Identical file state → identical pass/fail results
- Graceful missing files: Report "MISSING" rather than crash
- Error isolation: Failure on one file does not prevent validating remaining 5
- No short-circuit: All checks complete even if early checks fail

### Scalability
- Supports future context file additions (enumerate from directory)
- Linear cross-reference scaling O(n) not O(n²)
- Machine-parseable output format

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-357:** Update source-tree.md with .treelint/ Directory Structure
  - **Why:** Adds .treelint/ directory to source-tree.md — must be present for validation
  - **Status:** Backlog

- [ ] **STORY-358:** Document .treelint/ Gitignore Patterns
  - **Why:** Adds gitignore patterns to source-tree.md — must be present for validation
  - **Status:** Backlog

- [ ] **STORY-359:** Add Treelint Usage Guidance to anti-patterns.md
  - **Why:** Adds Category 11 to anti-patterns.md — must be present for validation
  - **Status:** Backlog

### External Dependencies
None.

### Technology Dependencies
None — uses existing context-validator subagent.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ validation coverage

**Test Scenarios:**
1. **Happy Path:** All 6 files pass validation with correct versions, dates, and LOCKED markers
2. **Edge Cases:**
   - Predecessor story not yet merged (detect missing changes)
   - LOCKED marker shifted position (search first 10 lines, not fixed line)
   - Cross-file Treelint version constraint inconsistency
   - Empty sections in modified files
   - Duplicate anti-pattern category numbers
3. **Error Cases:**
   - Missing context file (graceful MISSING report)
   - LOCKED marker removed (CRITICAL violation)
   - Version not incremented in modified file
   - Cross-file contradiction detected

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **Full Validation Run:** context-validator subagent invoked, all 6 files validated
2. **Cross-Reference:** Treelint ADR-013 reference resolves to existing ADR file

---

## Acceptance Criteria Verification Checklist

### AC#1: All 6 Context Files Pass Syntax Validation

- [ ] context-validator invoked against all 6 files - **Phase:** 2 - **Evidence:** tests/STORY-360/test_ac1_syntax_validation.sh
- [ ] Zero CRITICAL violations - **Phase:** 2 - **Evidence:** Validation report
- [ ] Zero HIGH violations - **Phase:** 2 - **Evidence:** Validation report
- [ ] All 6 files report PASS status - **Phase:** 2 - **Evidence:** Validation report

### AC#2: LOCKED Markers Intact

- [ ] tech-stack.md LOCKED marker present - **Phase:** 2 - **Evidence:** tests/STORY-360/test_ac2_locked_markers.sh
- [ ] source-tree.md LOCKED marker present - **Phase:** 2 - **Evidence:** Grep
- [ ] dependencies.md LOCKED marker present - **Phase:** 2 - **Evidence:** Grep
- [ ] coding-standards.md LOCKED marker present - **Phase:** 2 - **Evidence:** Grep
- [ ] architecture-constraints.md LOCKED marker present - **Phase:** 2 - **Evidence:** Grep
- [ ] anti-patterns.md LOCKED marker present - **Phase:** 2 - **Evidence:** Grep

### AC#3: Version Numbers Correct

- [ ] source-tree.md version >= 3.6 - **Phase:** 2 - **Evidence:** tests/STORY-360/test_ac3_version_numbers.sh
- [ ] anti-patterns.md version >= 1.1 - **Phase:** 2 - **Evidence:** Grep
- [ ] 4 unmodified files retain original versions - **Phase:** 2 - **Evidence:** Grep

### AC#4: Last Updated Dates Correct

- [ ] source-tree.md date updated - **Phase:** 2 - **Evidence:** tests/STORY-360/test_ac4_last_updated_dates.sh
- [ ] anti-patterns.md date updated - **Phase:** 2 - **Evidence:** Grep
- [ ] 4 unmodified files retain original dates - **Phase:** 2 - **Evidence:** Grep

### AC#5: No Cross-File Contradictions

- [ ] Treelint name consistent across files - **Phase:** 2 - **Evidence:** tests/STORY-360/test_ac5_cross_file_consistency.sh
- [ ] Version constraint v0.12.0+ consistent - **Phase:** 2 - **Evidence:** Grep
- [ ] ADR-013 references resolve correctly - **Phase:** 2 - **Evidence:** File existence check
- [ ] No contradictions between tech-stack.md approvals and anti-patterns.md guidance - **Phase:** 2 - **Evidence:** Cross-reference check

---

**Checklist Progress:** 0/19 items complete (0%)

---

## Definition of Done

### Implementation
- [x] context-validator subagent invoked against all 6 context files - Completed: Invoked in Phase 03, all 6 files validated
- [x] Validation report generated with per-file PASS/FAIL status - Completed: QA report at devforgeai/qa/reports/STORY-360-qa-report.md
- [x] All 6 files pass syntax validation (zero CRITICAL/HIGH violations) - Completed: 49 syntax assertions pass
- [x] LOCKED markers verified intact in all 6 files - Completed: 25 assertions verify LOCKED markers
- [x] Version numbers verified (source-tree >= 3.6, anti-patterns >= 1.1, others unchanged) - Completed: source-tree.md v3.7, anti-patterns.md v1.1
- [x] Last Updated dates verified (modified files updated, others unchanged) - Completed: Both modified files dated 2026-02-05
- [x] Cross-file Treelint consistency verified (name, version, ADR references) - Completed: 20 cross-file assertions pass
- [x] No contradictions between context files - Completed: tech-stack.md approves, anti-patterns.md guides usage

### Quality
- [x] All 5 acceptance criteria have passing tests - Completed: 110/110 assertions pass
- [x] Validation is read-only (zero writes to context files) - Completed: BR-001 verified
- [x] All 6 files validated (no short-circuit on failure) - Completed: All 6 files in every test
- [x] Deterministic results (reproducible) - Completed: Tests run identically each execution

### Testing
- [x] tests/STORY-360/test_ac1_syntax_validation.sh passes - Completed: 49/49 PASS
- [x] tests/STORY-360/test_ac2_locked_markers.sh passes - Completed: 25/25 PASS
- [x] tests/STORY-360/test_ac3_version_numbers.sh passes - Completed: 8/8 PASS
- [x] tests/STORY-360/test_ac4_last_updated_dates.sh passes - Completed: 8/8 PASS
- [x] tests/STORY-360/test_ac5_cross_file_consistency.sh passes - Completed: 20/20 PASS

### Documentation
- [x] Validation report documented (results summary) - Completed: 110 assertions, 5 ACs, 0 violations
- [x] EPIC-056 Stories table updated with STORY-360 - Completed: Already listed in epic at line 263

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-05
**Branch:** main

- [x] context-validator subagent invoked against all 6 context files - Completed: Invoked in Phase 03, all 6 files validated
- [x] Validation report generated with per-file PASS/FAIL status - Completed: QA report at devforgeai/qa/reports/STORY-360-qa-report.md
- [x] All 6 files pass syntax validation (zero CRITICAL/HIGH violations) - Completed: 49 syntax assertions pass
- [x] LOCKED markers verified intact in all 6 files - Completed: 25 assertions verify LOCKED markers
- [x] Version numbers verified (source-tree >= 3.6, anti-patterns >= 1.1, others unchanged) - Completed: source-tree.md v3.7, anti-patterns.md v1.1
- [x] Last Updated dates verified (modified files updated, others unchanged) - Completed: Both modified files dated 2026-02-05
- [x] Cross-file Treelint consistency verified (name, version, ADR references) - Completed: 20 cross-file assertions pass
- [x] No contradictions between context files - Completed: tech-stack.md approves, anti-patterns.md guides usage
- [x] All 5 acceptance criteria have passing tests - Completed: 110/110 assertions pass
- [x] Validation is read-only (zero writes to context files) - Completed: BR-001 verified
- [x] All 6 files validated (no short-circuit on failure) - Completed: All 6 files in every test
- [x] Deterministic results (reproducible) - Completed: Tests run identically each execution
- [x] tests/STORY-360/test_ac1_syntax_validation.sh passes - Completed: 49/49 PASS
- [x] tests/STORY-360/test_ac2_locked_markers.sh passes - Completed: 25/25 PASS
- [x] tests/STORY-360/test_ac3_version_numbers.sh passes - Completed: 8/8 PASS
- [x] tests/STORY-360/test_ac4_last_updated_dates.sh passes - Completed: 8/8 PASS
- [x] tests/STORY-360/test_ac5_cross_file_consistency.sh passes - Completed: 20/20 PASS
- [x] Validation report documented (results summary) - Completed: 110 assertions, 5 ACs, 0 violations
- [x] EPIC-056 Stories table updated with STORY-360 - Completed: Already listed in epic at line 263

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 110 assertions across 5 test scripts
- Tests placed in tests/STORY-360/
- All tests follow PASS/FAIL counter pattern for bash testing

**Phase 03 (Green): Implementation**
- Validation story - no production code written
- All tests passed immediately (predecessor stories completed correctly)

**Phase 04 (Refactor): Code Quality**
- refactoring-specialist reviewed test scripts (19% duplication acceptable for shell)
- code-reviewer approved with no critical issues

**Phase 05 (Integration): Full Validation**
- Suite runner (run_all_tests.sh) aggregates all 5 tests
- Exit codes verified (0 on pass, 1 on fail)
- All 110 assertions pass consistently

**Phase 06 (Deferral): DoD Validation**
- No deferrals - all items complete

### Files Created

- tests/STORY-360/test_ac1_syntax_validation.sh (6826 bytes, 49 assertions)
- tests/STORY-360/test_ac2_locked_markers.sh (6588 bytes, 25 assertions)
- tests/STORY-360/test_ac3_version_numbers.sh (8038 bytes, 8 assertions)
- tests/STORY-360/test_ac4_last_updated_dates.sh (7977 bytes, 8 assertions)
- tests/STORY-360/test_ac5_cross_file_consistency.sh (11787 bytes, 20 assertions)
- tests/STORY-360/run_all_tests.sh (2151 bytes, suite runner)

### Test Results

- **Total assertions:** 110
- **Pass rate:** 100%
- **Test scripts:** 5 (+ 1 runner)
- **All ACs verified:** AC#1-AC#5

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-04 | claude/story-requirements-analyst | Created | Story created from EPIC-056 Feature 4 | STORY-360-validate-context-file-updates.story.md |
| 2026-02-05 | claude/opus | Development Complete | TDD workflow completed, all 110 tests pass, DoD validated | tests/STORY-360/*.sh, STORY-360 |
| 2026-02-06 | claude/qa-result-interpreter | QA Deep | PASSED: 110/110 tests, 1/1 validators, 0 violations | STORY-360-qa-report.md |

## Notes

**Design Decisions:**
- Validation story runs AFTER all 3 predecessor stories to catch cross-file issues
- Uses existing context-validator subagent (no new tooling needed)
- Read-only validation — this story does not create or modify content
- All 6 files always validated (no short-circuit) for complete coverage

**Edge Cases:**
- Predecessor stories not yet merged: Validation detects missing changes and reports which stories are incomplete
- LOCKED marker position drift: Search first 10 lines, not fixed line number
- Future context file additions: Validation enumerates from directory, not hardcoded list

**Related ADRs:**
- [ADR-013: Treelint Integration](../adrs/ADR-013-treelint-integration.md)

**References:**
- [EPIC-056: Treelint Context File Integration](../Epics/EPIC-056-treelint-context-file-integration.epic.md)
- [STORY-357: source-tree.md Update](STORY-357-update-source-tree-treelint-directory.story.md) — prerequisite
- [STORY-358: Gitignore Patterns](STORY-358-document-treelint-gitignore-patterns.story.md) — prerequisite
- [STORY-359: anti-patterns.md Guidance](STORY-359-add-treelint-guidance-anti-patterns.story.md) — prerequisite

---

Story Template Version: 2.8
Last Updated: 2026-02-04
