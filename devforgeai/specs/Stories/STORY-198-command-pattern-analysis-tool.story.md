---
id: STORY-198
title: Create Command Pattern Analysis Tool
type: feature
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: QA Approved
points: 2
depends_on: ["STORY-195"]
priority: Medium
assigned_to: Unassigned
created: 2026-01-01
source_rca: RCA-015
source_recommendation: REC-4
format_version: "2.5"
---

# Story: Create Command Pattern Analysis Tool

## Description

**As a** DevForgeAI framework maintainer,
**I want** a Python script that analyzes hook logs and recommends safe patterns to add,
**so that** I can perform data-driven hook optimization monthly.

**Context from RCA-015:**
Future hook updates need data-driven pattern selection. An analysis script that parses hook logs and suggests high-frequency safe patterns will prevent ad-hoc pattern guessing and enable systematic optimization.

## Acceptance Criteria

### AC#1: Log Parsing

**Given** the hook-unknown-commands.log file exists
**When** the analysis script is run
**Then** it parses all "UNKNOWN COMMAND REQUIRING APPROVAL:" entries

---

### AC#2: Prefix Extraction

**Given** parsed command entries
**When** prefixes are extracted
**Then** the first 2 words of each command are captured as candidate patterns

---

### AC#3: Safety Filtering

**Given** extracted command prefixes
**When** candidates are evaluated
**Then** prefixes containing dangerous operations (rm, sudo, curl, wget) are excluded

---

### AC#4: Frequency Analysis

**Given** safe candidate prefixes
**When** the script generates output
**Then** top 20 candidates are displayed with occurrence count and percentage

---

### AC#5: Impact Calculation

**Given** top 20 safe candidates
**When** the script completes
**Then** total impact (commands that would be auto-approved) is calculated and displayed

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "analyze-hook-patterns.py"
      file_path: "devforgeai/scripts/analyze-hook-patterns.py"
      interface: "CLI Script"
      lifecycle: "On-demand execution"
      dependencies: []
      requirements:
        - id: "SVC-001"
          description: "Parse hook-unknown-commands.log for UNKNOWN COMMAND entries"
          testable: true
          test_requirement: "Test: Script correctly parses sample log with 100 entries"
          priority: "Critical"
        - id: "SVC-002"
          description: "Extract first 2 words as pattern prefix"
          testable: true
          test_requirement: "Test: 'cd /tmp && python' extracts 'cd /tmp'"
          priority: "High"
        - id: "SVC-003"
          description: "Filter out dangerous prefixes (rm, sudo, curl, wget, dd)"
          testable: true
          test_requirement: "Test: 'rm -rf' prefix excluded from candidates"
          priority: "Critical"
        - id: "SVC-004"
          description: "Count frequencies and sort by occurrence"
          testable: true
          test_requirement: "Test: Top candidate has highest count"
          priority: "High"
        - id: "SVC-005"
          description: "Calculate and display total impact percentage"
          testable: true
          test_requirement: "Test: Impact percentage = sum(top 20 counts) / total * 100"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Only Python 3 standard library (no external dependencies)"
      trigger: "Script design"
      validation: "No pip install required"
      error_handling: "Use re, collections, pathlib only"
      test_requirement: "Test: Script runs without pip install"
      priority: "High"

    - id: "BR-002"
      rule: "Safe-looking patterns heuristic includes common DevForgeAI operations"
      trigger: "Candidate filtering"
      validation: "Include cd, git, python, devforgeai, which, stat, file, basename, ls, cat, grep, find"
      error_handling: "Patterns not in whitelist require manual review"
      test_requirement: "Test: 'devforgeai' prefix included in candidates"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Analyze 10,000 log entries in < 5 seconds"
      metric: "< 5 seconds for 10,000 entries"
      test_requirement: "Test: Time script on large log file"
      priority: "Low"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance
- Process 10,000 log entries: < 5 seconds
- Memory usage: < 100MB

### Reliability
- Handle missing log file gracefully
- Handle malformed log entries without crashing

---

## Dependencies

### Prerequisite Stories
- [ ] **STORY-195:** Add Common Command Composition Patterns
  - **Why:** Establishes logging infrastructure the analysis tool depends on

---

## Test Strategy

### Unit Tests
1. Test log parsing: Sample log with known entries
2. Test prefix extraction: Various command formats
3. Test safety filtering: Dangerous commands excluded
4. Test frequency counting: Correct sort order

### Integration Tests
1. Run against actual hook-unknown-commands.log
2. Verify output format matches expected structure

---

## Acceptance Criteria Verification Checklist

### AC#1: Log Parsing
- [x] Log file reading implemented - **Phase:** 3 - **Evidence:** script code
- [x] UNKNOWN COMMAND pattern matching - **Phase:** 3 - **Evidence:** regex test

### AC#2: Prefix Extraction
- [x] First 2 words extraction - **Phase:** 3 - **Evidence:** unit test

### AC#3: Safety Filtering
- [x] Dangerous prefix list defined - **Phase:** 3 - **Evidence:** code review
- [x] Filtering logic implemented - **Phase:** 3 - **Evidence:** unit test

### AC#4: Frequency Analysis
- [x] Counter for frequency analysis - **Phase:** 3 - **Evidence:** code review
- [x] Top 20 output format - **Phase:** 5 - **Evidence:** script output

### AC#5: Impact Calculation
- [x] Impact percentage calculation - **Phase:** 3 - **Evidence:** unit test
- [x] Summary output display - **Phase:** 5 - **Evidence:** script output

---

**Checklist Progress:** 9/9 items complete (100%)

---

## Definition of Done

### Implementation
- [x] analyze-hook-patterns.py created at devforgeai/scripts/ - Completed: devforgeai/scripts/analyze_hook_patterns.py created with full implementation
- [x] Log parsing with regex for UNKNOWN COMMAND - Completed: parse_log_entries() with regex pattern
- [x] Prefix extraction (first 2 words) - Completed: extract_prefix() function
- [x] Safety filtering (exclude rm, sudo, curl, wget, dd) - Completed: is_safe_prefix() with DANGEROUS_PREFIXES set
- [x] Frequency counting with Counter - Completed: analyze_frequencies() using collections.Counter
- [x] Top 20 output with percentage - Completed: top 20 sorted by count with percentage calculation
- [x] Impact calculation and summary - Completed: calculate_impact() function

### Quality
- [x] All 5 acceptance criteria have passing tests - Completed: 27 tests covering all ACs
- [x] Edge cases covered (empty log, malformed entries) - Completed: 4 edge case tests
- [x] No external dependencies (standard library only) - Completed: uses only re, collections, pathlib, argparse

### Testing
- [x] Unit tests for each function - Completed: 22 unit tests for all functions
- [x] Integration test with sample log - Completed: CLI tested with sample log output

### Documentation
- [x] Script docstring with usage instructions - Completed: module docstring with examples
- [x] Inline comments explaining logic - Completed: docstrings and comments throughout

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-09
**Branch:** refactor/devforgeai-migration

- [x] analyze-hook-patterns.py created at devforgeai/scripts/ - Completed: devforgeai/scripts/analyze_hook_patterns.py created with full implementation
- [x] Log parsing with regex for UNKNOWN COMMAND - Completed: parse_log_entries() with regex pattern
- [x] Prefix extraction (first 2 words) - Completed: extract_prefix() function
- [x] Safety filtering (exclude rm, sudo, curl, wget, dd) - Completed: is_safe_prefix() with DANGEROUS_PREFIXES set
- [x] Frequency counting with Counter - Completed: analyze_frequencies() using collections.Counter
- [x] Top 20 output with percentage - Completed: top 20 sorted by count with percentage calculation
- [x] Impact calculation and summary - Completed: calculate_impact() function
- [x] All 5 acceptance criteria have passing tests - Completed: 27 tests covering all ACs
- [x] Edge cases covered (empty log, malformed entries) - Completed: 4 edge case tests
- [x] No external dependencies (standard library only) - Completed: uses only re, collections, pathlib, argparse
- [x] Unit tests for each function - Completed: 22 unit tests for all functions
- [x] Integration test with sample log - Completed: CLI tested with sample log output
- [x] Script docstring with usage instructions - Completed: module docstring with examples
- [x] Inline comments explaining logic - Completed: docstrings and comments throughout

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 27 comprehensive tests covering all 5 acceptance criteria
- Tests placed in devforgeai/tests/STORY-198/test_analyze_hook_patterns.py
- Test framework: pytest

**Phase 03 (Green): Implementation**
- Implemented analyze_hook_patterns.py via backend-architect subagent
- 5 core functions: parse_log_entries, extract_prefix, is_safe_prefix, analyze_frequencies, calculate_impact
- All 27 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Code reviewed by code-reviewer subagent
- All cyclomatic complexity scores < 10
- Unused imports removed from test file

**Phase 05 (Integration): Full Validation**
- CLI execution verified (text + JSON output)
- Error handling tested (missing file case)
- Performance: <1s for 10K entries

### Files Created

- devforgeai/scripts/analyze_hook_patterns.py (356 lines)
- devforgeai/tests/STORY-198/test_analyze_hook_patterns.py (228 lines)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-015 REC-4 | STORY-198-command-pattern-analysis-tool.story.md |
| 2026-01-09 | claude/opus | DoD Update (Phase 07) | Development complete, all 27 tests passing, DoD validated | STORY-198, analyze_hook_patterns.py, test_analyze_hook_patterns.py |
| 2026-01-10 | claude/qa-result-interpreter | QA Deep | PASSED: Coverage 100%/85%/80%, 0 blocking violations, 3/3 validators | STORY-198-qa-report.md |

## Notes

**Source RCA:** RCA-015, REC-4 (MEDIUM priority)
**Expected Impact:** Enables systematic, data-driven hook optimization

**Usage:**
```bash
python3 devforgeai/scripts/analyze-hook-patterns.py
# Reviews unknown commands
# Outputs top 20 safe patterns to add
# Shows frequency and impact percentage
```

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
