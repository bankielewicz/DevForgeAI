---
id: STORY-400
title: Add Long Parameter List Detection to Anti-Pattern-Scanner
type: feature
epic: EPIC-064
sprint: SPRINT-13
status: QA Approved
points: 2
depends_on: []
priority: High
advisory: false
assigned_to: TBD
created: 2026-02-13
format_version: "2.9"
---

# Story: Add Long Parameter List Detection to Anti-Pattern-Scanner

## Description

**As a** framework user,
**I want** the anti-pattern-scanner to automatically detect functions with more than 4 parameters,
**so that** AI-generated code with overly complex method signatures is flagged for refactoring.

## Provenance

```xml
<provenance>
  <origin document="EPIC-064" section="Feature 1: Tier 1 Quick Wins">
    <quote>"A function/method with more than 4 parameters, indicating the function may be doing too much or parameters should be grouped into an object."</quote>
    <line_reference>lines 241-276</line_reference>
    <quantified_impact>Low false positive rate - parameter count is unambiguous</quantified_impact>
  </origin>

  <decision rationale="simple-threshold-no-two-stage">
    <selected>Direct parameter count check without two-stage filtering</selected>
    <rejected alternative="two-stage-filtering">Parameter count is deterministic; LLM assessment adds no value</rejected>
    <trade_off>Simpler implementation with predictable behavior</trade_off>
  </decision>

  <hypothesis id="H1" validation="threshold-validation" success_criteria="no false positives on self/cls parameters">
    Excluding self and cls (Python) from parameter count will produce accurate results
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Treelint-Based Parameter Count Detection

```xml
<acceptance_criteria id="AC1" implements="PHASE5-LONGPARAM">
  <given>A Python, TypeScript, or JavaScript codebase with Treelint v0.12.0+ available</given>
  <when>The anti-pattern-scanner executes Phase 5 (Code Smells)</when>
  <then>Functions with parameter_count greater than 4 (excluding self/cls) are flagged as long parameter list violations</then>
  <verification>
    <source_files>
      <file hint="Agent definition">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-400/test_ac1_treelint_detection.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Python Self/Cls Exclusion

```xml
<acceptance_criteria id="AC2" implements="PHASE5-SELFEXCLUDE">
  <given>A Python method with self or cls as the first parameter</given>
  <when>The anti-pattern-scanner counts parameters</when>
  <then>The self or cls parameter is excluded from the count</then>
  <verification>
    <source_files>
      <file hint="Parameter counting logic">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-400/test_ac2_self_cls_exclusion.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Variadic Parameter Handling

```xml
<acceptance_criteria id="AC3" implements="PHASE5-VARIADIC">
  <given>A Python function with *args and **kwargs</given>
  <when>The anti-pattern-scanner counts parameters</when>
  <then>*args and **kwargs are NOT counted as individual parameters</then>
  <verification>
    <source_files>
      <file hint="Variadic handling">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-400/test_ac3_variadic_handling.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Grep Fallback for Unsupported Languages

```xml
<acceptance_criteria id="AC4" implements="PHASE5-GREPFALLBACK">
  <given>A codebase with C#, Java, or Go files (unsupported by Treelint)</given>
  <when>The anti-pattern-scanner executes Phase 5 long parameter list detection</when>
  <then>Grep patterns (def\s+\w+\([^)]*,[^)]*,[^)]*,[^)]*,[^)]*\)) detecting 5+ commas in signature are used</then>
  <verification>
    <source_files>
      <file hint="Grep fallback patterns">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-400/test_ac4_grep_fallback.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: JSON Output Format Compliance

```xml
<acceptance_criteria id="AC5" implements="PHASE5-OUTPUT">
  <given>A long parameter list violation has been detected</given>
  <when>The anti-pattern-scanner returns findings</when>
  <then>Output includes smell_type: "long_parameter_list", severity: "MEDIUM", function_name, file, line, parameter_count, parameters array, evidence, and remediation fields</then>
  <verification>
    <source_files>
      <file hint="Output contract">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-400/test_ac5_json_output.py</test_file>
    <coverage_threshold>95</coverage_threshold>
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
      name: "LongParameterListDetector"
      file_path: ".claude/agents/anti-pattern-scanner.md"
      interface: "Phase 5 Code Smell Detection"
      requirements:
        - id: "SVC-001"
          description: "Extend Phase 5 to detect functions with > 4 parameters using Treelint"
          implements_ac: ["AC1"]
          testable: true
          test_requirement: "Test: Verify treelint search --type function returns signature field for parameter parsing"
          priority: "Critical"
        - id: "SVC-002"
          description: "Exclude self and cls parameters from count for Python methods"
          implements_ac: ["AC2"]
          testable: true
          test_requirement: "Test: Verify def method(self, a, b, c, d, e) counts 5 params, not 6"
          priority: "High"
        - id: "SVC-003"
          description: "Exclude *args and **kwargs from parameter count"
          implements_ac: ["AC3"]
          testable: true
          test_requirement: "Test: Verify def func(a, b, *args, **kwargs) counts 2 params, not 4"
          priority: "High"
        - id: "SVC-004"
          description: "Implement Grep fallback for unsupported languages"
          implements_ac: ["AC4"]
          testable: true
          test_requirement: "Test: Verify Grep pattern detects 5+ parameter signatures in .cs files"
          priority: "High"

    - type: "Configuration"
      name: "LongParameterListThreshold"
      file_path: ".claude/agents/anti-pattern-scanner.md"
      required_keys:
        - key: "long_parameter_list.threshold"
          type: "int"
          example: 4
          required: true
          default: 4
          validation: "parameter_count > threshold flags violation"
          test_requirement: "Test: Verify 5 params flagged, 4 params not flagged"

    - type: "DataModel"
      name: "LongParameterListFinding"
      purpose: "JSON output schema for long parameter list smell detection"
      fields:
        - name: "smell_type"
          type: "String"
          constraints: "Required, value: 'long_parameter_list'"
          description: "Smell type identifier"
          test_requirement: "Test: Verify smell_type is always 'long_parameter_list'"
        - name: "severity"
          type: "Enum"
          constraints: "Required, value: 'MEDIUM'"
          description: "Fixed severity for this smell"
          test_requirement: "Test: Verify severity is always 'MEDIUM'"
        - name: "function_name"
          type: "String"
          constraints: "Required"
          description: "Name of the function with long parameter list"
          test_requirement: "Test: Verify function_name matches actual function identifier"
        - name: "file"
          type: "String"
          constraints: "Required, relative path"
          description: "File path where function is defined"
          test_requirement: "Test: Verify file path exists and contains the function"
        - name: "line"
          type: "Int"
          constraints: "Required, positive"
          description: "Line number of function definition"
          test_requirement: "Test: Verify line number points to def/function keyword"
        - name: "parameter_count"
          type: "Int"
          constraints: "Required, > threshold"
          description: "Number of parameters (excluding self/cls/*args/**kwargs)"
          test_requirement: "Test: Verify parameter_count matches actual count"
        - name: "parameters"
          type: "Array[String]"
          constraints: "Required"
          description: "List of parameter names"
          test_requirement: "Test: Verify parameters array contains actual param names"
        - name: "evidence"
          type: "String"
          constraints: "Required"
          description: "Human-readable explanation"
          test_requirement: "Test: Verify evidence includes parameter_count and threshold"
        - name: "remediation"
          type: "String"
          constraints: "Required"
          description: "Suggested fix action"
          test_requirement: "Test: Verify remediation suggests Parameter Object pattern"

  business_rules:
    - id: "BR-001"
      rule: "Long parameter list threshold: parameter_count > 4"
      trigger: "During Phase 5 function enumeration"
      validation: "Count actual parameters, excluding self/cls/*args/**kwargs"
      error_handling: "If count <= 4, function is not flagged"
      test_requirement: "Test: Verify function with 5 params flagged, 4 params not flagged"
      priority: "Critical"
    - id: "BR-002"
      rule: "Python self/cls exclusion"
      trigger: "When first parameter is 'self' or 'cls'"
      validation: "Decrement count by 1 if first param is self/cls"
      error_handling: "N/A - standard Python method convention"
      test_requirement: "Test: Verify def method(self, a, b, c, d, e) counts 5 params"
      priority: "High"
    - id: "BR-003"
      rule: "Variadic parameter exclusion (*args, **kwargs)"
      trigger: "When parameter starts with * or **"
      validation: "Do not count parameters starting with * or **"
      error_handling: "N/A - variadic params are flexible by design"
      test_requirement: "Test: Verify def func(a, *args) counts 1 param"
      priority: "High"
    - id: "BR-004"
      rule: "No two-stage filtering required"
      trigger: "Long parameter list detection"
      validation: "Parameter count is deterministic, no LLM assessment needed"
      error_handling: "N/A"
      test_requirement: "Test: Verify detection is immediate without Stage 2 assessment"
      priority: "Low"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Treelint query execution time"
      metric: "< 100ms per function enumeration query"
      test_requirement: "Test: Time treelint search --type function and verify < 100ms"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Graceful degradation when Treelint unavailable"
      metric: "Fall back to Grep without HALT"
      test_requirement: "Test: Verify scanner completes when Treelint binary missing"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No known limitations - parameter counting is straightforward
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Treelint query:** < 100ms per function enumeration (p95)
- **Grep fallback:** < 3 seconds for 500-file project (p95)

**Throughput:**
- Process up to 5000 functions per project scan

---

### Reliability

**Error Handling:**
- Treelint unavailable → fall back to Grep without HALT
- Malformed signature → skip function, continue scanning

---

## Dependencies

### Prerequisite Stories

None - this story can begin immediately.

### Technology Dependencies

- [x] **Treelint:** v0.12.0+ (already in tech-stack.md)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for detection logic

**Test Scenarios:**
1. **Happy Path:** Function with 5 params (excl. self) → detected
2. **Edge Cases:**
   - Function with 3 params → not detected (below threshold)
   - Function with self, a, b, c, d, e → detected (5 params, self excluded)
   - Python *args, **kwargs → not counted as individual params
3. **Error Cases:**
   - Treelint unavailable → Grep fallback
   - Malformed signature → skip function

---

## Acceptance Criteria Verification Checklist

### AC#1: Treelint-Based Parameter Count Detection

- [x] Treelint search --type function query added to Phase 5 - **Phase:** 2
- [x] Signature field parsed for parameter count - **Phase:** 3
- [x] Threshold logic implemented (parameter_count > 4) - **Phase:** 3

### AC#2: Python Self/Cls Exclusion

- [x] First parameter check for self/cls - **Phase:** 3
- [x] Count decremented when self/cls detected - **Phase:** 3

### AC#3: Variadic Parameter Handling

- [x] *args excluded from count - **Phase:** 3
- [x] **kwargs excluded from count - **Phase:** 3

### AC#4: Grep Fallback for Unsupported Languages

- [x] Grep pattern for 5+ commas in signature - **Phase:** 3
- [x] Fallback trigger on Treelint exit 127/126 - **Phase:** 3

### AC#5: JSON Output Format Compliance

- [x] LongParameterListFinding schema implemented - **Phase:** 3
- [x] All required fields populated - **Phase:** 3

---

**Checklist Progress:** 12/12 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Phase 5 long parameter list detection added to anti-pattern-scanner.md
- [x] Treelint query logic for function signatures implemented
- [x] Self/cls exclusion logic implemented
- [x] Variadic parameter exclusion (*args, **kwargs) implemented
- [x] Grep fallback patterns for 5+ parameters implemented

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Edge cases covered (self/cls, variadic, threshold boundary)
- [x] Code coverage > 95% for detection logic

### Testing
- [x] Unit tests for Treelint detection (test_ac1_treelint_detection.py)
- [x] Unit tests for self/cls exclusion (test_ac2_self_cls_exclusion.py)
- [x] Unit tests for variadic handling (test_ac3_variadic_handling.py)
- [x] Unit tests for Grep fallback (test_ac4_grep_fallback.py)
- [x] Unit tests for JSON output (test_ac5_json_output.py)

### Documentation
- [x] anti-pattern-scanner.md Phase 5 updated with long parameter list detection

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-14

- [x] Phase 5 long parameter list detection added to anti-pattern-scanner.md - Completed: Added Long Parameter List Detection subsection to Phase 5 with Treelint query, parameter counting rules, Grep fallback, and LongParameterListFinding schema
- [x] Treelint query logic for function signatures implemented - Completed: detect_long_parameter_list() parses Treelint JSON output and counts effective parameters
- [x] Self/cls exclusion logic implemented - Completed: _get_effective_params() excludes self/cls only when in first parameter position
- [x] Variadic parameter exclusion (*args, **kwargs) implemented - Completed: Any parameter starting with * is excluded from count
- [x] Grep fallback patterns for 5+ parameters implemented - Completed: detect_long_parameter_list_grep() with C#/Java/Go patterns
- [x] All 5 acceptance criteria have passing tests - Completed: 82 unit tests + 28 integration tests = 110 tests, all passing
- [x] Edge cases covered (self/cls, variadic, threshold boundary) - Completed: Extensive edge case coverage including threshold boundary (3, 4, 5, 6 params), self/cls in non-first position, custom variadics
- [x] Code coverage > 95% for detection logic - Completed: 99% coverage achieved
- [x] Unit tests for Treelint detection (test_ac1_treelint_detection.py) - Completed: 17 tests
- [x] Unit tests for self/cls exclusion (test_ac2_self_cls_exclusion.py) - Completed: 10 tests
- [x] Unit tests for variadic handling (test_ac3_variadic_handling.py) - Completed: 12 tests (10 original + 2 additional)
- [x] Unit tests for Grep fallback (test_ac4_grep_fallback.py) - Completed: 18 tests
- [x] Unit tests for JSON output (test_ac5_json_output.py) - Completed: 25 tests
- [x] anti-pattern-scanner.md Phase 5 updated with long parameter list detection - Completed: src/claude/agents/anti-pattern-scanner.md updated

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✅ Complete | 82 tests generated, all failing initially |
| Phase 03 (Green) | ✅ Complete | Implementation completed, all 82 tests passing |
| Phase 04 (Refactor) | ✅ Complete | DRY violations fixed, extracted _build_finding helper |
| Phase 04.5 (AC Verify) | ✅ Complete | All 5 ACs verified with HIGH confidence |
| Phase 05 (Integration) | ✅ Complete | 28 integration tests added, 110 total tests |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| tests/STORY-400/__init__.py | Created | 1 |
| tests/STORY-400/long_parameter_list_detector.py | Created | 300 |
| tests/STORY-400/test_ac1_treelint_detection.py | Created | 280 |
| tests/STORY-400/test_ac2_self_cls_exclusion.py | Created | 229 |
| tests/STORY-400/test_ac3_variadic_handling.py | Created | 229 |
| tests/STORY-400/test_ac4_grep_fallback.py | Created | 243 |
| tests/STORY-400/test_ac5_json_output.py | Created | 325 |
| tests/STORY-400/test_integration_long_parameter_list.py | Created | 350 |
| src/claude/agents/anti-pattern-scanner.md | Modified | +50 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-13 14:10 | .claude/devforgeai-story-creation | Created | Story created from EPIC-064 Feature 1 | STORY-400-add-long-parameter-list-detection.story.md |
| 2026-02-14 14:55 | .claude/qa-result-interpreter | QA Deep | PASSED: Coverage 99%, 0 blocking violations, 3/3 validators | - |

## Notes

**Design Decisions:**
- No two-stage filtering needed - parameter count is deterministic
- Threshold of 4 matches refactoring-specialist documentation
- Self/cls exclusion follows Python conventions

**Test Scenarios (from EPIC-064):**
- Function with 5 params (excl. self) → detected
- Function with 3 params → not detected (below threshold)
- Function with self, a, b, c, d, e → detected (5 params, self excluded)
- Python *args, **kwargs → not counted as individual params

**References:**
- EPIC-064: AI-Generated Code Smell Detection Gap Closure (lines 241-276)
- refactoring-specialist: Long Parameter List threshold (>4)

---

Story Template Version: 2.9
Last Updated: 2026-02-13
