# Phase 3: Refactor (Refactor Phase)

**Purpose:** Improve code quality while keeping all tests green.

**Execution Order:** After Phase 2 (Green phase) - tests are passing

**Expected Outcome:** Improved code quality, all tests still GREEN

**Token Cost:** ~1,200 tokens in skill context (~60,000 combined in isolated subagent contexts)

---

## Overview

The Refactor phase improves code quality without changing behavior. Tests remain green throughout.

**Core Principle:** Improve structure, maintain behavior.

---

## Phase 3: Refactor (Refactor Phase)

**Delegate refactoring to refactoring-specialist and code-reviewer subagents.**

### Step 1: Invoke refactoring-specialist Subagent

```
Task(
  subagent_type="refactoring-specialist",
  description="Refactor code while keeping tests green",
  prompt="Refactor the implementation from Phase 2 to improve code quality.

  Implementation files and tests available in conversation.

  Context files to enforce:
  - .devforgeai/context/anti-patterns.md (check for violations)
  - .devforgeai/context/coding-standards.md (apply patterns)
  - .devforgeai/context/architecture-constraints.md (maintain layer boundaries)

  Refactoring targets:
  1. Anti-pattern violations (God objects, tight coupling, magic numbers)
  2. Code complexity (methods >50 lines, cyclomatic complexity >10)
  3. Code duplication (DRY principle violations)
  4. Naming improvements (clarity, consistency)
  5. Performance optimizations (if low-hanging fruit)

  Requirements:
  - Keep tests GREEN throughout (run {TEST_COMMAND} after each change)
  - Use native tools (Edit for modifications, not sed)
  - Make incremental changes (one refactoring at a time)
  - HALT if tests break

  Test command: {TEST_COMMAND}

  Return:
  - Refactorings applied (list with rationale)
  - Files modified
  - Test status after each refactoring (must stay GREEN)"
)
```

### Step 2: Parse Subagent Response

```javascript
result = extract_from_subagent_output(response)

refactorings_applied = result["refactorings"]
tests_green = result["tests_remained_green"]

Display: "✓ Phase 3 (Refactor): Code improved by refactoring-specialist"
Display: "  - Refactorings applied: {len(refactorings_applied)}"

FOR refactoring in refactorings_applied:
    Display: "    • {refactoring['type']}: {refactoring['rationale']}"

IF tests_green:
    Display: "  - Tests: ✅ GREEN (all passing after refactoring)"
ELSE:
    Display: "  - Tests: ❌ BROKEN during refactoring"
    HALT development
```

### Step 3: Invoke code-reviewer Subagent

```
Task(
  subagent_type="code-reviewer",
  description="Review refactored code for quality",
  prompt="Perform comprehensive code review of the refactored implementation.

  Code and tests available in conversation.

  Review checklist:
  1. Code quality (readability, maintainability, simplicity)
  2. Security (no vulnerabilities, input validation, secrets management)
  3. Best practices (SOLID principles, design patterns)
  4. Test coverage (all paths covered, edge cases tested)
  5. Documentation (public APIs documented, complex logic explained)
  6. Performance (no obvious bottlenecks)
  7. Context file compliance (tech-stack.md, coding-standards.md, etc.)

  Provide feedback organized by priority:
  - CRITICAL (must fix before commit)
  - HIGH (should fix now)
  - MEDIUM (should fix soon)
  - LOW (nice to have)

  Return:
  - Issues found (by priority)
  - Positive observations
  - Recommendations"
)
```

### Step 4: Parse Code Review Response

```javascript
result = extract_from_subagent_output(response)

critical_issues = result["issues"]["critical"]
high_issues = result["issues"]["high"]

Display: "✓ Code review by code-reviewer complete"

IF len(critical_issues) > 0:
    Display: "  - CRITICAL issues: {len(critical_issues)} (must fix)"

    FOR issue in critical_issues:
        Display: "    🚨 {issue['description']}"

    # Re-invoke refactoring-specialist to fix critical issues
    Display: "Re-invoking refactoring-specialist to fix critical issues..."
    # [Task call with critical issues in prompt]

ELIF len(high_issues) > 0:
    Display: "  - HIGH issues: {len(high_issues)} (should fix)"

    FOR issue in high_issues:
        Display: "    ⚠️ {issue['description']}"

    # Ask user if they want to fix now
    AskUserQuestion:
        question: "{len(high_issues)} high-priority issues found. Fix now?"
        header: "Code Review"
        options:
            - label: "Fix now"
              description: "Address issues before proceeding"
            - label: "Continue"
              description: "Accept issues, proceed to Phase 4"
        multiSelect: false

ELSE:
    Display: "  - No critical or high issues found ✅"
    Display: "  Ready for Phase 4 (Integration)"
```

---

## Subagents Invoked

**refactoring-specialist:**
- Applies systematic refactoring patterns
- Maintains green tests throughout
- Targets anti-patterns, complexity, duplication

**code-reviewer:**
- Comprehensive quality review
- Security vulnerability detection
- Best practices enforcement
- Context file compliance verification

---

## Success Criteria

Phase 3 succeeds when:
- [ ] Code quality improved (complexity reduced, duplication removed)
- [ ] All tests still GREEN (no regressions)
- [ ] No CRITICAL issues from code review
- [ ] Anti-patterns removed
- [ ] Code follows coding-standards.md
- [ ] Ready for integration testing

---

## Common Refactorings

**See `references/refactoring-patterns.md` for comprehensive patterns:**
- Extract Method (long methods)
- Extract Class (God objects)
- Introduce Parameter Object (long parameter lists)
- Replace Magic Number with Constant
- Consolidate Duplicate Code
- Simplify Conditional Expressions

---

## Next Phase

**Phase 4: Integration & Validation**
- Cross-component testing
- See `references/integration-testing.md`
