---
id: STORY-118
title: Core Anti-pattern Rules - Code Quality Detection
epic: EPIC-018
sprint: SPRINT-7
status: Ready for Dev
points: 8
depends_on: ["STORY-115", "STORY-116"]
priority: Medium
assigned_to: Unassigned
created: 2025-12-20
format_version: "2.2"
---

# Story: Core Anti-pattern Rules - Code Quality Detection

## Description

**As a** code reviewer,
**I want** ast-grep rules that detect common anti-patterns and code smells,
**so that** god objects, async void, console.log in production, and other maintainability issues are caught automatically.

**Context:** This story implements Feature 4 of EPIC-018 (ast-grep Foundation & Core Rules). It creates 10 HIGH/MEDIUM severity anti-pattern rules covering god objects, async void, console.log in production, magic numbers, long methods, and nested conditionals.

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
      file_path: ".devforgeai/ast-grep/rules/*/anti-patterns/god-object.yml"
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
      file_path: ".devforgeai/ast-grep/rules/csharp/anti-patterns/async-void.yml"
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
      file_path: ".devforgeai/ast-grep/rules/*/anti-patterns/console-log.yml"
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
      file_path: ".devforgeai/ast-grep/rules/*/anti-patterns/magic-numbers.yml"
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
      file_path: ".devforgeai/ast-grep/rules/*/anti-patterns/long-method.yml"
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
      file_path: ".devforgeai/ast-grep/rules/*/anti-patterns/nested-conditionals.yml"
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
- [ ] 10 anti-pattern rules created
- [ ] Rules implemented for Python (8 rules)
- [ ] Rules implemented for C# (10 rules including async void)
- [ ] Rules implemented for TypeScript/JavaScript (8 rules)
- [ ] Threshold configuration supported

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Detection accuracy ≥90% verified
- [ ] False positive rate <15% verified
- [ ] Code coverage >95% for anti-pattern rules

### Testing
- [ ] Test fixtures for Python (15+ files)
- [ ] Test fixtures for C# (15+ files)
- [ ] Test fixtures for TypeScript (15+ files)
- [ ] Threshold edge cases tested

### Documentation
- [ ] Rule descriptions in each rule file
- [ ] Anti-pattern reference documentation
- [ ] Configuration guide for thresholds

---

## Workflow History

### 2025-12-20 14:30:00 - Status: Ready for Dev
- Added to SPRINT-7: Sprint 7 - AST-Grep
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 32 points
- Priority in sprint: [4 of 5]

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
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
