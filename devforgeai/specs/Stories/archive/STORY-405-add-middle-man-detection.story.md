---
id: STORY-405
title: Add Middle Man Detection to Anti-Pattern-Scanner
type: feature
epic: EPIC-064
sprint: SPRINT-13
status: QA Approved
points: 3
depends_on: []
priority: High
advisory: false
assigned_to: TBD
created: 2026-02-13
format_version: "2.9"
---

# Story: Add Middle Man Detection to Anti-Pattern-Scanner

## Description

**As a** framework user,
**I want** the anti-pattern-scanner to automatically detect middle man classes (classes where most methods delegate to another class),
**so that** AI-generated code with unnecessary indirection is flagged for refactoring.

## Provenance

```xml
<provenance>
  <origin document="EPIC-064" section="Feature 4: Tier 2 Detections">
    <quote>"A class where the majority of its methods simply delegate to another class. The class adds no value and should be removed, with clients calling the delegated class directly."</quote>
    <line_reference>lines 549-590</line_reference>
    <quantified_impact>Detects unnecessary proxy/wrapper classes that add complexity without value</quantified_impact>
  </origin>

  <decision rationale="treelint-method-body-analysis">
    <selected>Treelint AST method body size analysis (delegation = body <= 2 lines)</selected>
    <rejected alternative="grep-only">Cannot reliably identify method body boundaries with regex</rejected>
    <trade_off>Treelint provides accurate body size; Grep fallback less accurate</trade_off>
  </decision>

  <hypothesis id="H1" validation="delegation-ratio" success_criteria="correctly identify 80%+ delegation ratio">
    Body size <= 2 lines accurately identifies single-statement delegation methods
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Treelint-Based Method Body Analysis

```xml
<acceptance_criteria id="AC1" implements="PHASE5-MIDDLEMAN">
  <given>A Python, TypeScript, or JavaScript codebase with Treelint v0.12.0+ available</given>
  <when>The anti-pattern-scanner executes Phase 5 middle man detection</when>
  <then>For each class, method body sizes are calculated as (lines.end - lines.start), and methods with body size <= 2 are classified as delegation methods</then>
  <verification>
    <source_files>
      <file hint="Method analysis">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-405/test_ac1_method_body_analysis.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Delegation Ratio Calculation

```xml
<acceptance_criteria id="AC2" implements="PHASE5-RATIO">
  <given>Method body sizes have been calculated for a class</given>
  <when>Middle man analysis executes</when>
  <then>delegation_ratio = delegation_methods / total_methods is calculated, and classes with delegation_ratio > 0.80 AND total_methods >= 3 are flagged</then>
  <verification>
    <source_files>
      <file hint="Ratio calculation">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-405/test_ac2_delegation_ratio.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Minimum Method Threshold

```xml
<acceptance_criteria id="AC3" implements="PHASE5-MINTHRESHOLD">
  <given>A class with fewer than 3 methods</given>
  <when>Middle man analysis executes</when>
  <then>The class is NOT flagged regardless of delegation ratio (prevents false positives on small utility classes)</then>
  <verification>
    <source_files>
      <file hint="Threshold logic">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-405/test_ac3_minimum_threshold.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Grep Fallback for Unsupported Languages

```xml
<acceptance_criteria id="AC4" implements="PHASE5-GREPFALLBACK">
  <given>A codebase with C#, Java, or Go files (unsupported by Treelint)</given>
  <when>Middle man detection executes</when>
  <then>Grep-based method detection with line counting is used as fallback</then>
  <verification>
    <source_files>
      <file hint="Fallback logic">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-405/test_ac4_grep_fallback.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: JSON Output Format Compliance

```xml
<acceptance_criteria id="AC5" implements="PHASE5-OUTPUT">
  <given>A middle man violation has been detected</given>
  <when>The anti-pattern-scanner returns findings</when>
  <then>Output includes smell_type: "middle_man", severity: "MEDIUM", class_name, file, line, total_methods, delegating_methods, delegation_ratio, evidence, and remediation fields</then>
  <verification>
    <source_files>
      <file hint="Output contract">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-405/test_ac5_json_output.py</test_file>
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
      name: "MiddleManDetector"
      file_path: ".claude/agents/anti-pattern-scanner.md"
      interface: "Phase 5 Code Smell Detection"
      requirements:
        - id: "SVC-001"
          description: "Calculate method body size using Treelint members.methods[].lines"
          implements_ac: ["AC1"]
          testable: true
          test_requirement: "Test: Verify body_size = lines.end - lines.start calculated correctly"
          priority: "Critical"
        - id: "SVC-002"
          description: "Calculate delegation ratio for each class"
          implements_ac: ["AC2"]
          testable: true
          test_requirement: "Test: Verify delegation_ratio = delegation_methods / total_methods"
          priority: "Critical"
        - id: "SVC-003"
          description: "Enforce minimum method threshold (>= 3)"
          implements_ac: ["AC3"]
          testable: true
          test_requirement: "Test: Verify classes with 2 methods never flagged"
          priority: "High"
        - id: "SVC-004"
          description: "Implement Grep fallback for unsupported languages"
          implements_ac: ["AC4"]
          testable: true
          test_requirement: "Test: Verify Grep fallback activates for .cs, .java, .go"
          priority: "High"

    - type: "Configuration"
      name: "MiddleManThresholds"
      file_path: ".claude/agents/anti-pattern-scanner.md"
      required_keys:
        - key: "middle_man.delegation_threshold"
          type: "float"
          example: 0.80
          required: true
          default: 0.80
          validation: "delegation_ratio > threshold flags violation"
          test_requirement: "Test: Verify 0.81 ratio flagged, 0.79 ratio not flagged"
        - key: "middle_man.min_methods"
          type: "int"
          example: 3
          required: true
          default: 3
          validation: "total_methods >= threshold required for detection"
          test_requirement: "Test: Verify 2-method class not flagged"
        - key: "middle_man.delegation_body_size"
          type: "int"
          example: 2
          required: true
          default: 2
          validation: "body_size <= threshold = delegation method"
          test_requirement: "Test: Verify 2-line method is delegation, 3-line is not"

    - type: "DataModel"
      name: "MiddleManFinding"
      purpose: "JSON output schema for middle man smell detection"
      fields:
        - name: "smell_type"
          type: "String"
          constraints: "Required, value: 'middle_man'"
          description: "Smell type identifier"
          test_requirement: "Test: Verify smell_type is always 'middle_man'"
        - name: "severity"
          type: "Enum"
          constraints: "Required, value: 'MEDIUM'"
          description: "Fixed severity for middle man"
          test_requirement: "Test: Verify severity is always 'MEDIUM'"
        - name: "class_name"
          type: "String"
          constraints: "Required"
          description: "Name of the middle man class"
          test_requirement: "Test: Verify class_name matches actual class"
        - name: "file"
          type: "String"
          constraints: "Required, relative path"
          description: "File where class is defined"
          test_requirement: "Test: Verify file path exists"
        - name: "line"
          type: "Int"
          constraints: "Required, positive"
          description: "Line number of class definition"
          test_requirement: "Test: Verify line points to class keyword"
        - name: "total_methods"
          type: "Int"
          constraints: "Required, >= 3"
          description: "Total methods in class"
          test_requirement: "Test: Verify total_methods >= 3"
        - name: "delegating_methods"
          type: "Int"
          constraints: "Required"
          description: "Number of delegation methods"
          test_requirement: "Test: Verify delegating_methods count correct"
        - name: "delegation_ratio"
          type: "Float"
          constraints: "Required, range 0.0-1.0"
          description: "Ratio of delegating to total methods"
          test_requirement: "Test: Verify delegation_ratio = delegating_methods / total_methods"
        - name: "evidence"
          type: "String"
          constraints: "Required"
          description: "Human-readable explanation"
          test_requirement: "Test: Verify evidence describes delegation pattern"
        - name: "remediation"
          type: "String"
          constraints: "Required"
          description: "Suggested fix action"
          test_requirement: "Test: Verify remediation suggests removing proxy"

  business_rules:
    - id: "BR-001"
      rule: "Delegation method: body size <= 2 lines"
      trigger: "During method body analysis"
      validation: "lines.end - lines.start <= 2"
      error_handling: "If lines unavailable → skip class"
      test_requirement: "Test: Verify 1-line return statement is delegation"
      priority: "Critical"
    - id: "BR-002"
      rule: "Middle man threshold: delegation_ratio > 0.80"
      trigger: "After delegation ratio calculated"
      validation: "ratio must exceed 80% to flag"
      error_handling: "N/A"
      test_requirement: "Test: Verify 7/8 methods = 0.875 flagged, 6/8 = 0.75 not flagged"
      priority: "Critical"
    - id: "BR-003"
      rule: "Minimum method count: total_methods >= 3"
      trigger: "Before flagging class"
      validation: "Prevents false positives on small utility classes"
      error_handling: "N/A"
      test_requirement: "Test: Verify 2-method class with 100% delegation not flagged"
      priority: "High"
    - id: "BR-004"
      rule: "Facade classes with complex orchestration are NOT middle men"
      trigger: "When multi-line methods detected"
      validation: "Methods > 2 lines indicate orchestration, not pure delegation"
      error_handling: "N/A"
      test_requirement: "Test: Verify facade with 5-line orchestration methods not flagged"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Treelint query execution time"
      metric: "< 100ms per class enumeration query"
      test_requirement: "Test: Time treelint search --type class and verify < 100ms"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Graceful degradation when Treelint unavailable"
      metric: "Fall back to Grep without HALT"
      test_requirement: "Test: Verify scanner completes when Treelint missing"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Adapter classes"
    limitation: "Legitimate adapter pattern classes may have high delegation ratio but serve a valid purpose"
    decision: "workaround:medium severity allows human review"
    discovered_phase: "Architecture"
    impact: "Minor - MEDIUM severity doesn't block QA, allows manual review"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Treelint query:** < 100ms per class enumeration
- **Full analysis:** < 30 seconds for typical project

---

### Reliability

**Error Handling:**
- Treelint unavailable → fall back to Grep
- Lines unavailable → skip class

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
1. **Happy Path:** Class with 8 methods, 7 single-line delegations → detected (ratio 0.875)
2. **Edge Cases:**
   - Class with 3 methods, all short → detected but borderline (ratio 1.0, check context)
   - Facade class with complex orchestration → not detected (methods are multi-line)
   - Adapter class (legitimate pattern) → may detect, MEDIUM severity allows review
   - Class with 2 methods → not detected (below minimum threshold)
3. **Error Cases:**
   - Treelint unavailable → Grep fallback

---

## Acceptance Criteria Verification Checklist

### AC#1: Treelint-Based Method Body Analysis

- [x] Method body size calculation implemented - **Phase:** 3 - calculate_method_body_size()
- [x] Delegation method threshold (<=2 lines) enforced - **Phase:** 3 - is_delegation_method()

### AC#2: Delegation Ratio Calculation

- [x] delegation_ratio formula implemented - **Phase:** 3 - calculate_delegation_ratio()
- [x] Threshold > 0.80 enforced - **Phase:** 3 - detect_middle_man()

### AC#3: Minimum Method Threshold

- [x] Minimum 3 methods check implemented - **Phase:** 3 - detect_middle_man()

### AC#4: Grep Fallback for Unsupported Languages

- [x] Grep-based method detection implemented - **Phase:** 3 - detect_middle_man_grep()
- [x] Fallback trigger on Treelint exit 127/126 - **Phase:** 3 - should_use_grep_fallback()

### AC#5: JSON Output Format Compliance

- [x] MiddleManFinding schema implemented - **Phase:** 3 - build_middle_man_finding()
- [x] All required fields populated - **Phase:** 3 - 10 fields with evidence/remediation

---

**Checklist Progress:** 9/9 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Phase 5 middle man detection added to anti-pattern-scanner.md
- [x] Treelint method body size calculation implemented
- [x] Delegation ratio calculation implemented
- [x] Minimum method threshold (>=3) enforced
- [x] Grep fallback implemented

### Quality
- [x] All 5 acceptance criteria have passing tests - 74 tests passing
- [x] Edge cases covered (small classes, facades, adapters) - via test fixtures
- [x] Code coverage > 95% for detection logic - 100% function coverage

### Testing
- [x] Unit tests for method body analysis (test_ac1_method_body_analysis.py) - Created: 13 tests
- [x] Unit tests for delegation ratio (test_ac2_delegation_ratio.py) - Created: 14 tests
- [x] Unit tests for minimum threshold (test_ac3_minimum_threshold.py) - Created: 6 tests
- [x] Unit tests for Grep fallback (test_ac4_grep_fallback.py) - Created: 12 tests
- [x] Unit tests for JSON output (test_ac5_json_output.py) - Created: 29 tests

### Documentation
- [x] anti-pattern-scanner.md Phase 5 updated with middle man detection

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | Complete | 74 tests created, all failing |
| Phase 03 (Green) | Complete | All 74 tests passing |
| Phase 04 (Refactor) | Complete | DRY violations fixed, complexity reduced |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| tests/STORY-405/__init__.py | Created | Package marker |
| tests/STORY-405/middle_man_detector.py | Created | Stub implementation |
| tests/STORY-405/test_ac1_method_body_analysis.py | Created | 13 tests |
| tests/STORY-405/test_ac2_delegation_ratio.py | Created | 14 tests |
| tests/STORY-405/test_ac3_minimum_threshold.py | Created | 6 tests |
| tests/STORY-405/test_ac4_grep_fallback.py | Created | 12 tests |
| tests/STORY-405/test_ac5_json_output.py | Created | 29 tests |

---

## Implementation Notes

- [x] Phase 5 middle man detection added to anti-pattern-scanner.md - Completed: Added middle man detection section with Treelint AST analysis, delegation ratio calculation, minimum method threshold, Grep fallback, and MiddleManFinding output schema to both .claude/agents/ and src/claude/agents/ anti-pattern-scanner.md
- [x] Treelint method body size calculation implemented - Completed: calculate_method_body_size() computes body_size = lines.end - lines.start from Treelint JSON output
- [x] Delegation ratio calculation implemented - Completed: calculate_delegation_ratio() = delegation_methods / total_methods, with detect_middle_man() flagging ratio > 0.80
- [x] Minimum method threshold (>=3) enforced - Completed: Classes with fewer than 3 methods are skipped (prevents false positives on small utility classes)
- [x] Grep fallback implemented - Completed: detect_middle_man_grep() supports C#, Java, Go with brace-delimited scanning and Go receiver method pattern matching
- [x] All 5 acceptance criteria have passing tests - Completed: 74 tests across 5 test files, all passing
- [x] Edge cases covered (small classes, facades, adapters) - Completed: Test fixtures cover boundary conditions (0.80 exact boundary, 2-method classes, multi-line facade methods)
- [x] Code coverage > 95% for detection logic - Completed: 96% statement coverage (179 stmts, 7 missed defensive guards)
- [x] Unit tests for method body analysis (test_ac1_method_body_analysis.py) - Completed: 13 tests for body size calculation and delegation classification
- [x] Unit tests for delegation ratio (test_ac2_delegation_ratio.py) - Completed: 14 tests for ratio calculation and middle man detection
- [x] Unit tests for minimum threshold (test_ac3_minimum_threshold.py) - Completed: 6 tests for minimum method threshold enforcement
- [x] Unit tests for Grep fallback (test_ac4_grep_fallback.py) - Completed: 12 tests for fallback decision logic and language-specific detection
- [x] Unit tests for JSON output (test_ac5_json_output.py) - Completed: 29 tests for all 10 MiddleManFinding output fields
- [x] anti-pattern-scanner.md Phase 5 updated with middle man detection - Completed: Added complete middle man detection documentation to Phase 5 Code Smells section

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-16

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-13 15:00 | .claude/devforgeai-story-creation | Created | Story created from EPIC-064 Feature 4 | STORY-405-add-middle-man-detection.story.md |
| 2026-02-16 12:30 | .claude/qa-result-interpreter | QA Deep | PASSED: Coverage 96%, 74/74 tests, 0 critical violations | - |

## Notes

**Design Decisions:**
- Delegation method = body <= 2 lines (single statement + optional return)
- Minimum 3 methods to avoid false positives on small utility classes
- MEDIUM severity to allow human review of legitimate adapter/wrapper patterns

**Test Scenarios (from EPIC-064):**
- Class with 8 methods, 7 single-line delegations → detected (ratio 0.875)
- Class with 3 methods, all short → detected but borderline (ratio 1.0, check context)
- Facade class with complex orchestration → not detected (methods are multi-line)
- Adapter class (legitimate pattern) → may detect, LLM context helps distinguish
- Class with 2 methods → not detected (below minimum threshold)

**References:**
- EPIC-064: AI-Generated Code Smell Detection Gap Closure (lines 549-590)

---

Story Template Version: 2.9
Last Updated: 2026-02-13
