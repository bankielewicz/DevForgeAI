---
id: STORY-118
title: Core Anti-pattern Rules - Code Quality Detection
epic: EPIC-018
sprint: SPRINT-7
status: Cancelled
points: 8
depends_on: ["STORY-115", "STORY-116"]
priority: Medium
assigned_to: Unassigned
created: 2025-12-20
cancelled: 2025-12-21
cancellation_reason: "ast-grep limitations - see ADR-007"
format_version: "2.2"
---

# Story: Core Anti-pattern Rules - Code Quality Detection

---

## ⛔ CANCELLATION NOTICE

**Status**: CANCELLED (2025-12-21)
**Decision**: ADR-007 - Remove ast-grep and Evaluate Tree-sitter
**Reason**: ast-grep has fundamental pattern matching limitations that prevent meeting framework quality requirements

### Decision Summary

After comprehensive remediation attempts (25+ rules, 32 fixtures, 59 tests), ast-grep was found to have critical limitations:

1. **Multi-line patterns fail** when comments or type annotations exist between statements
2. **Cannot count/accumulate** (e.g., "detect classes with >20 methods" impossible)
3. **Whitespace sensitivity** breaks Python pattern matching
4. **C# AST structure** doesn't match expected patterns
5. **No semantic analysis** capability (duplicate detection, scope analysis)

### Remediation Evidence

| Metric | Before | After Remediation |
|--------|--------|------------------|
| Tests Passing | 51/59 (86.4%) | 52/59 (88.1%) |
| Quality Gate | 95% required | 88.1% achieved |
| Gap | -8.6% | -6.9% |

Despite comprehensive pattern expansion and restructuring, 6 tests remained failing due to tool limitations, not implementation issues.

### Next Steps

1. **EPIC-018**: Marked as CANCELLED
2. **Alternative**: Evaluate tree-sitter for static analysis (new epic to be created)
3. **CLI Enhancement**: Integrate tree-sitter into devforgeai CLI
4. **Reference**: ADR-007 documents decision and tree-sitter evaluation plan

---

## Description

**As a** code reviewer,
**I want** ~~ast-grep~~ **tree-sitter-based** rules that detect common anti-patterns and code smells,
**so that** god objects, async void, console.log in production, and other maintainability issues are caught automatically.

**Context:** ~~This story implements Feature 4 of EPIC-018 (ast-grep Foundation & Core Rules). It creates 10 HIGH/MEDIUM severity anti-pattern rules covering god objects, async void, console.log in production, magic numbers, long methods, and nested conditionals.~~ **CANCELLED** - See ADR-007 for decision to replace ast-grep with tree-sitter.

## Acceptance Criteria

### AC#1: God Object Detection

**Given** a class with too many responsibilities,
**When** the anti-pattern scan executes,
**Then** the rule detects:
1. Classes with >500 lines (Python, C#, TypeScript)
2. Classes with >20 methods
3. Classes with >15 fields/properties

**Severity:** HIGH

---

### AC#2: Async Void Detection (C#)

**Given** C# code with async void methods,
**When** the anti-pattern scan executes,
**Then** the rule detects:
1. `async void MethodName()` declarations
2. Allows async void for event handlers (contains EventHandler pattern)

**Severity:** HIGH

---

### AC#3: Console.log in Production Detection

**Given** code with console logging statements,
**When** the anti-pattern scan executes,
**Then** the rule detects:
1. console.log() in TypeScript/JavaScript (non-test files)
2. print() in Python (non-test files)
3. Console.WriteLine() in C# (non-test files)

**Severity:** MEDIUM (allows in test/debug contexts)

---

### AC#4: Magic Numbers Detection

**Given** code with hardcoded numeric literals,
**When** the anti-pattern scan executes,
**Then** the rule detects:
1. Numeric literals in conditionals (if x > 100)
2. Numeric literals in assignments (timeout = 5000)
3. Allows: 0, 1, -1, 100, 1000 (common safe values)
4. Allows: constants (const TIMEOUT = 5000)

**Severity:** MEDIUM

---

### AC#5: Long Method Detection

**Given** methods with excessive length,
**When** the anti-pattern scan executes,
**Then** the rule detects:
1. Methods with >50 lines (all languages)
2. Excludes test methods and generated code

**Severity:** MEDIUM

---

### AC#6: Nested Conditionals Detection

**Given** code with deeply nested conditionals,
**When** the anti-pattern scan executes,
**Then** the rule detects:
1. if/else nesting >3 levels deep
2. Mixed if/try/for nesting >4 levels
3. Suggests early return pattern

**Severity:** MEDIUM

---

### AC#7: Additional Anti-patterns (4 more)

**Given** additional code quality issues,
**When** the anti-pattern scan executes,
**Then** the rules also detect:
1. **Unused imports/variables** - MEDIUM severity
2. **Excessive parameter count** (>5 params) - MEDIUM severity
3. **Duplicate code blocks** (>10 lines repeated) - HIGH severity
4. **Empty catch blocks** - HIGH severity

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "god-object-rules"
      file_path: "devforgeai/ast-grep/rules/*/anti-patterns/god-object.yml"
      required_keys:
        - key: "id"
          type: "string"
          example: "AP-001"
          required: true
          validation: "Unique within anti-patterns category"
          test_requirement: "Test: Rule ID follows AP-XXX pattern"
        - key: "severity"
          type: "string"
          example: "HIGH"
          required: true
          default: "HIGH"
          validation: "HIGH for structural issues"
          test_requirement: "Test: Severity is HIGH for god objects"
        - key: "thresholds.max_lines"
          type: "integer"
          example: "500"
          required: true
          default: "500"
          validation: "Positive integer"
          test_requirement: "Test: Classes >500 lines flagged"
        - key: "thresholds.max_methods"
          type: "integer"
          example: "20"
          required: true
          default: "20"
          validation: "Positive integer"
          test_requirement: "Test: Classes >20 methods flagged"

    - type: "Configuration"
      name: "async-void-rules"
      file_path: "devforgeai/ast-grep/rules/csharp/anti-patterns/async-void.yml"
      required_keys:
        - key: "id"
          type: "string"
          example: "AP-002"
          required: true
          validation: "Unique within anti-patterns category"
          test_requirement: "Test: Rule ID follows AP-XXX pattern"
        - key: "rule.pattern"
          type: "string"
          example: "async void $METHOD($$$)"
          required: true
          validation: "Matches async void declaration"
          test_requirement: "Test: Pattern matches async void methods"
        - key: "rule.not.pattern"
          type: "string"
          example: "EventHandler"
          required: false
          validation: "Excludes event handlers"
          test_requirement: "Test: Event handlers not flagged"

    - type: "Configuration"
      name: "console-log-rules"
      file_path: "devforgeai/ast-grep/rules/*/anti-patterns/console-log.yml"
      required_keys:
        - key: "id"
          type: "string"
          example: "AP-003"
          required: true
          validation: "Unique within anti-patterns category"
          test_requirement: "Test: Rule ID follows AP-XXX pattern"
        - key: "severity"
          type: "string"
          example: "MEDIUM"
          required: true
          default: "MEDIUM"
          validation: "MEDIUM for non-critical issues"
          test_requirement: "Test: Severity is MEDIUM"
        - key: "rule.pattern"
          type: "string"
          example: "console.log($$$)"
          required: true
          validation: "Matches console logging"
          test_requirement: "Test: Detects console.log calls"

    - type: "Configuration"
      name: "magic-numbers-rules"
      file_path: "devforgeai/ast-grep/rules/*/anti-patterns/magic-numbers.yml"
      required_keys:
        - key: "id"
          type: "string"
          example: "AP-004"
          required: true
          validation: "Unique within anti-patterns category"
          test_requirement: "Test: Rule ID follows AP-XXX pattern"
        - key: "allowlist"
          type: "array"
          example: "[0, 1, -1, 100, 1000]"
          required: false
          default: "[0, 1, -1, 100, 1000]"
          validation: "Array of allowed numeric literals"
          test_requirement: "Test: Allowlisted values not flagged"

    - type: "Configuration"
      name: "long-method-rules"
      file_path: "devforgeai/ast-grep/rules/*/anti-patterns/long-method.yml"
      required_keys:
        - key: "id"
          type: "string"
          example: "AP-005"
          required: true
          validation: "Unique within anti-patterns category"
          test_requirement: "Test: Rule ID follows AP-XXX pattern"
        - key: "thresholds.max_lines"
          type: "integer"
          example: "50"
          required: true
          default: "50"
          validation: "Positive integer"
          test_requirement: "Test: Methods >50 lines flagged"

    - type: "Configuration"
      name: "nested-conditionals-rules"
      file_path: "devforgeai/ast-grep/rules/*/anti-patterns/nested-conditionals.yml"
      required_keys:
        - key: "id"
          type: "string"
          example: "AP-006"
          required: true
          validation: "Unique within anti-patterns category"
          test_requirement: "Test: Rule ID follows AP-XXX pattern"
        - key: "thresholds.max_depth"
          type: "integer"
          example: "3"
          required: true
          default: "3"
          validation: "Positive integer"
          test_requirement: "Test: Nesting >3 levels flagged"

  business_rules:
    - id: "BR-001"
      rule: "Anti-pattern rules have HIGH or MEDIUM severity (never CRITICAL)"
      trigger: "Rule validation"
      validation: "Check severity field is HIGH or MEDIUM"
      error_handling: "Warn if CRITICAL used for anti-pattern"
      test_requirement: "Test: Anti-pattern with CRITICAL rejected"
      priority: "Medium"
    - id: "BR-002"
      rule: "Test files are excluded from anti-pattern checks"
      trigger: "File filtering during scan"
      validation: "Check file path against test patterns"
      error_handling: "Skip file if in test directory"
      test_requirement: "Test: Files in tests/ not scanned"
      priority: "High"
    - id: "BR-003"
      rule: "Each rule must suggest a fix in the message"
      trigger: "Rule output"
      validation: "Message contains 'Consider:' or 'Instead:'"
      error_handling: "Warn if no fix suggestion"
      test_requirement: "Test: All rules include fix suggestion"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Anti-pattern scan must complete in <15s for 1000 files"
      metric: "p95 scan time <15s"
      test_requirement: "Test: Scan 1000-file fixture in <15s"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "False positive rate <15% for style rules"
      metric: "<15% false positives"
      test_requirement: "Test: 50 clean fixtures, <8 false positives"
      priority: "High"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Anti-pattern scan: <15s for 1000 files

---

### Reliability

**Detection Accuracy:**
- True positive rate: ≥90%
- False positive rate: <15%

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-115:** CLI Validator Foundation
  - **Why:** Provides ast-grep integration
  - **Status:** Backlog

- [x] **STORY-116:** Configuration Infrastructure
  - **Why:** Provides rule storage structure
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for rule logic

**Test Fixtures (per language):**

**Python:**
- god_object_large.py (class >500 lines)
- console_log_production.py (print statements)
- magic_numbers.py (hardcoded values)
- long_method.py (>50 line method)
- nested_conditionals.py (deep nesting)

**C#:**
- GodObject.cs
- AsyncVoidMethods.cs
- ConsoleWriteLine.cs
- MagicNumbers.cs
- LongMethod.cs
- NestedConditionals.cs
- EmptyCatch.cs

**TypeScript:**
- god-object.ts
- console-log.ts
- magic-numbers.ts
- long-method.ts
- nested-conditionals.ts
- unused-imports.ts

---

## Acceptance Criteria Verification Checklist

### AC#1: God Object Detection

- [ ] >500 lines detected - **Phase:** 03 - **Evidence:** test_god_object_lines.py
- [ ] >20 methods detected - **Phase:** 03 - **Evidence:** test_god_object_methods.py
- [ ] >15 fields detected - **Phase:** 03 - **Evidence:** test_god_object_fields.py

### AC#2: Async Void Detection

- [ ] async void detected - **Phase:** 03 - **Evidence:** test_async_void.py
- [ ] EventHandler excluded - **Phase:** 03 - **Evidence:** test_async_void_handler.py

### AC#3: Console.log Detection

- [ ] console.log detected - **Phase:** 03 - **Evidence:** test_console_log.py
- [ ] print() detected - **Phase:** 03 - **Evidence:** test_print_python.py
- [ ] Test files excluded - **Phase:** 03 - **Evidence:** test_console_exclude_tests.py

### AC#4: Magic Numbers Detection

- [ ] Numeric literals detected - **Phase:** 03 - **Evidence:** test_magic_numbers.py
- [ ] Allowlist working - **Phase:** 03 - **Evidence:** test_magic_allowlist.py
- [ ] Constants excluded - **Phase:** 03 - **Evidence:** test_magic_constants.py

### AC#5: Long Method Detection

- [ ] >50 lines detected - **Phase:** 03 - **Evidence:** test_long_method.py
- [ ] Test methods excluded - **Phase:** 03 - **Evidence:** test_long_method_exclude.py

### AC#6: Nested Conditionals Detection

- [ ] >3 levels detected - **Phase:** 03 - **Evidence:** test_nested_conditionals.py
- [ ] Early return suggested - **Phase:** 03 - **Evidence:** test_nested_message.py

### AC#7: Additional Anti-patterns

- [ ] Unused imports detected - **Phase:** 03 - **Evidence:** test_unused_imports.py
- [ ] Excessive params detected - **Phase:** 03 - **Evidence:** test_param_count.py
- [ ] Duplicate code detected - **Phase:** 03 - **Evidence:** test_duplicate_code.py
- [ ] Empty catch detected - **Phase:** 03 - **Evidence:** test_empty_catch.py

---

**Checklist Progress:** 0/19 items complete (0%)

---

## Definition of Done

### Implementation
- [x] 10 anti-pattern rules created (AP-001 through AP-010)
- [x] Rules implemented for Python (8 rules)
- [x] Rules implemented for C# (9 rules including async void, empty catch)
- [x] Rules implemented for TypeScript (8 rules)
- [x] Threshold configuration supported (in rule message/note fields)

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Detection accuracy ≥90% verified
- [ ] False positive rate <15% verified
- [ ] Code coverage >95% for anti-pattern rules

### Testing
- [x] Test fixtures for Python (14 files)
- [x] Test fixtures for C# (10 files)
- [x] Test fixtures for TypeScript (8 files)
- [ ] Threshold edge cases tested

### Documentation
- [x] Rule descriptions in each rule file
- [x] Anti-pattern reference documentation (docs/ast-grep/antipattern-rules-reference.md)
- [x] Configuration guide for thresholds (included in reference doc)

---

## QA Validation History

### QA Attempt 1 - 2025-12-21 (Deep Mode)
**Result:** FAILED

**Test Results:**
- Total tests: 59
- Passing: 51 (86.4%)
- Failing: 8 (13.6%)

**Blocking Issues:**
1. 8 tests failing - pattern matching issues in rule files
2. 5 incomplete DoD items (blocked by test failures)
3. 57.9% AC coverage (11/19 requirements validated)

**Failing Tests:**
- test_god_object_many_methods_python (AP-001)
- test_god_object_many_fields_python (AP-001)
- test_async_void_detected_csharp (AP-002)
- test_magic_numbers_detected_python (AP-004)
- test_long_method_test_excluded (AP-005)
- test_excessive_params_detected_python (AP-008)
- test_duplicate_code_detected_python (AP-009)
- test_empty_catch_detected_csharp (AP-010)

**Anti-Pattern Violations:** 0 CRITICAL, 0 HIGH, 2 MEDIUM, 3 LOW
**Deferral Validation:** N/A (no deferrals, items are blocking failures)
**Code Quality:** PASS (88/100 score)

**Next Steps:**
1. Fix ast-grep rule patterns for failing tests
2. Address AP-009 duplicate code limitation (architecture decision needed)
3. Re-run: `/qa STORY-118 deep`

**Report:** `devforgeai/qa/reports/STORY-118-qa-report.md`
**Gaps:** `devforgeai/qa/reports/STORY-118-gaps.json`

---

## Workflow History

### 2025-12-21 12:00:00 - Status: Cancelled
- **Decision**: Do not proceed with ast-grep due to fundamental tool limitations
- **ADR**: ADR-007 created documenting decision to remove ast-grep and evaluate tree-sitter
- **Remediation Attempted**: 52/59 tests passing (88.1%) after comprehensive pattern fixes
- **Blocking Issue**: 6 tests failing due to ast-grep pattern matching limitations (NOT implementation issues)
- **Documented Limitations**:
  - Multi-line patterns fail with comments/type annotations
  - Cannot count/accumulate (required for god object detection)
  - Whitespace sensitivity breaks Python matching
  - C# AST structure mismatches
  - No semantic analysis capability
- **Next Steps**: Evaluate tree-sitter for devforgeai CLI integration
- **Files Updated**: tech-stack.md, ADR-007 created
- **ast-grep**: UNINSTALLED from project

### 2025-12-21 00:00:00 - Status: QA Failed
- Deep QA validation executed
- 8 of 59 tests failing (86.4% pass rate)
- Status changed: Dev Complete → QA Failed
- QA report generated: devforgeai/qa/reports/STORY-118-qa-report.md
- Gaps file created for remediation: devforgeai/qa/reports/STORY-118-gaps.json
- Action required: Fix failing tests and re-run QA

### 2025-12-20 23:30:00 - Status: Dev Complete
- Implemented 25 anti-pattern rule files (AP-001 through AP-010)
- Created 19 test fixtures across Python, C#, TypeScript
- Created test file: tests/unit/test_antipattern_rules_story118.py
- Transitioned from In Development to Dev Complete
- Ready for QA validation

### 2025-12-20 14:30:00 - Status: Ready for Dev
- Added to SPRINT-7: Sprint 7 - AST-Grep
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 32 points
- Priority in sprint: [4 of 5]

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- HIGH severity for structural issues (god objects, duplicate code)
- MEDIUM severity for style issues (console.log, magic numbers)
- Configurable thresholds for flexibility
- Test file exclusion by default

**Anti-pattern Categories:**
1. **Structural:** God objects, duplicate code (HIGH)
2. **Async:** Async void (HIGH)
3. **Maintainability:** Long methods, nested conditionals (MEDIUM)
4. **Style:** Console.log, magic numbers, unused imports (MEDIUM)
5. **Error Handling:** Empty catch blocks (HIGH)
6. **API Design:** Excessive parameters (MEDIUM)

**References:**
- [EPIC-018: ast-grep Foundation & Core Rules](../Epics/EPIC-018-astgrep-foundation-core-rules.epic.md)
- [DevForgeAI anti-patterns.md](../../context/anti-patterns.md)

---

**Story Template Version:** 2.2
**Created:** 2025-12-20
