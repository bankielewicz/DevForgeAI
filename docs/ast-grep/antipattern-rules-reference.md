# Anti-pattern Rules Reference

This document describes the 10 anti-pattern detection rules implemented for ast-grep in STORY-118.

## Overview

| Rule ID | Name | Severity | Languages | Detection Method |
|---------|------|----------|-----------|------------------|
| AP-001 | God Object | HIGH (warning) | Python, C#, TypeScript | Heuristic pattern matching |
| AP-002 | Async Void | HIGH (warning) | C# only | Exact pattern matching |
| AP-003 | Console Log | MEDIUM (info) | Python, C#, TypeScript | Exact pattern matching |
| AP-004 | Magic Numbers | MEDIUM (info) | Python, C#, TypeScript | Pattern matching with context |
| AP-005 | Long Method | MEDIUM (info) | Python, C#, TypeScript | Heuristic pattern matching |
| AP-006 | Nested Conditionals | MEDIUM (info) | Python, C#, TypeScript | Exact pattern matching |
| AP-007 | Unused Imports | MEDIUM (info) | Python, TypeScript | Pattern flagging for review |
| AP-008 | Excessive Parameters | MEDIUM (info) | Python, C#, TypeScript | Exact pattern matching |
| AP-009 | Duplicate Code | HIGH (warning) | Python, C#, TypeScript | Heuristic pattern matching |
| AP-010 | Empty Catch | HIGH (warning) | C# only | Exact pattern matching |

---

## Rule Details

### AP-001: God Object Detection

**Problem:** Classes with too many responsibilities violate the Single Responsibility Principle.

**Detection:** Matches classes with 10+ method definitions visible in the pattern.

**Thresholds (Guidance):**
- >500 lines of code
- >20 methods
- >15 fields/properties

**Limitation:** ast-grep cannot count lines or methods precisely. This rule uses heuristic pattern matching that detects classes with many visible method definitions. For precise detection, use:
- Python: pylint `R0902` (too-many-instance-attributes), `R0904` (too-many-public-methods)
- C#: SonarQube, ReSharper
- TypeScript: ESLint `max-lines-per-function`

**Fix:** Apply Single Responsibility Principle - split into focused classes.

---

### AP-002: Async Void Detection (C# Only)

**Problem:** `async void` methods cannot be awaited and exceptions propagate to the synchronization context, potentially crashing the application.

**Detection:** Exact pattern match for `async void` methods, excluding event handlers.

**Exclusions:**
- Methods with `EventArgs` parameters
- Methods named `On*`, `Handle*`, `*_Click`, `*_Changed`

**Fix:** Change `async void` to `async Task`.

---

### AP-003: Console Log Detection

**Problem:** Debug logging statements bypass structured logging and expose debug info in production.

**Detection:** Exact pattern matching for:
- Python: `print()`
- C#: `Console.WriteLine()`, `Console.Write()`, `Console.Error.WriteLine()`
- TypeScript: `console.log()`, `console.warn()`, `console.error()`, `console.debug()`, `console.info()`

**Exclusions:** Test files should be excluded at scan level (not in rule).

**Fix:** Use proper logging frameworks (Python: `logging`, C#: `ILogger`, TypeScript: winston/pino).

---

### AP-004: Magic Numbers Detection

**Problem:** Unexplained numeric literals make code harder to understand and maintain.

**Detection:** Pattern matching for numeric literals in:
- Comparisons: `if (x > 50)`
- Assignments: `timeout = 30000`

**Allowlist (Recommended):** 0, 1, -1, 2, 100, 1000

**Fix:** Extract to named constants at module/class level.

---

### AP-005: Long Method Detection

**Problem:** Methods with >50 lines are harder to understand, test, and maintain.

**Detection:** Matches functions/methods with 15+ visible statements.

**Limitation:** ast-grep cannot count lines precisely. This rule uses heuristic pattern matching. For precise detection, use:
- Python: pylint `R0915` (too-many-statements)
- C#: SonarQube
- TypeScript: ESLint `max-lines-per-function`

**Fix:** Extract logical sections into smaller functions (Extract Method refactoring).

---

### AP-006: Nested Conditionals Detection

**Problem:** Deep nesting (>3 levels) makes code harder to read and maintain.

**Detection:** Exact pattern match for 4 levels of nested `if` statements.

**Threshold:** 4+ levels triggers detection.

**Fix:** Apply Guard Clause pattern with early returns.

---

### AP-007: Unused Imports Detection

**Problem:** Unused imports increase load time and clutter the namespace.

**Detection:** Flags common import patterns for manual review.

**Limitation:** ast-grep cannot perform semantic analysis to determine if an import is truly unused. For precise detection, use:
- Python: pylint `W0611`, flake8 `F401`, autoflake
- TypeScript: ESLint `@typescript-eslint/no-unused-vars`

**Fix:** Remove unused imports. Use `autoflake` (Python) or `eslint --fix` (TypeScript).

---

### AP-008: Excessive Parameters Detection

**Problem:** Functions with >5 parameters are hard to call correctly and test.

**Detection:** Exact pattern match for functions with 6+ parameters.

**Threshold:** >5 parameters (6+) triggers detection.

**Fix:** Group related parameters into a configuration object, dataclass, or record.

---

### AP-009: Duplicate Code Detection

**Problem:** Duplicated code blocks violate DRY and increase maintenance burden.

**Detection:** Matches common duplication patterns (validation blocks, field extraction).

**Limitation:** ast-grep cannot detect arbitrary duplicate code blocks. For precise detection, use:
- jscpd (JavaScript/TypeScript)
- SonarQube (all languages)
- PMD CPD (Copy/Paste Detector)

**Fix:** Extract duplicated logic to a shared function.

---

### AP-010: Empty Catch Detection (C# Only)

**Problem:** Empty catch blocks silently swallow exceptions, hiding errors.

**Detection:** Exact pattern match for catch blocks with no statements.

**Fix:** Log the exception, rethrow, or handle appropriately.

---

## Configuration

### Threshold Configuration

Thresholds are documented in each rule's `note` field. To adjust thresholds, modify the pattern in the rule file:

**Example - Changing nested conditionals threshold from 4 to 5 levels:**

```yaml
# Before: 4 levels
rule:
  pattern: |
    if ($COND1) {
        if ($COND2) {
            if ($COND3) {
                if ($COND4) {
                    $$$BODY
                }
            }
        }
    }

# After: 5 levels
rule:
  pattern: |
    if ($COND1) {
        if ($COND2) {
            if ($COND3) {
                if ($COND4) {
                    if ($COND5) {
                        $$$BODY
                    }
                }
            }
        }
    }
```

### Test File Exclusion

To exclude test files from anti-pattern scans, use the `--filter` flag at scan level:

```bash
ast-grep scan --rule rules/python/anti-patterns/ \
  --filter '!**/test_*.py' \
  --filter '!**/tests/**' \
  src/
```

---

## Known Limitations

| Rule | Limitation | Recommended Tool |
|------|------------|------------------|
| AP-001 God Object | Cannot count lines/methods precisely | pylint, SonarQube |
| AP-005 Long Method | Cannot count lines precisely | pylint, ESLint |
| AP-007 Unused Imports | Requires semantic analysis | autoflake, ESLint |
| AP-009 Duplicate Code | Cannot detect arbitrary duplicates | jscpd, PMD CPD |

**Note:** These rules provide heuristic detection that catches many common cases. For comprehensive code quality analysis, combine ast-grep with dedicated static analysis tools.

---

## Rule Files Location

```
devforgeai/ast-grep/rules/
├── python/anti-patterns/
│   ├── console-log.yml
│   ├── duplicate-code.yml
│   ├── excessive-params.yml
│   ├── god-object.yml
│   ├── long-method.yml
│   ├── magic-numbers.yml
│   ├── nested-conditionals.yml
│   └── unused-imports.yml
├── csharp/anti-patterns/
│   ├── async-void.yml
│   ├── console-log.yml
│   ├── duplicate-code.yml
│   ├── empty-catch.yml
│   ├── excessive-params.yml
│   ├── god-object.yml
│   ├── long-method.yml
│   ├── magic-numbers.yml
│   └── nested-conditionals.yml
└── typescript/anti-patterns/
    ├── console-log.yml
    ├── duplicate-code.yml
    ├── excessive-params.yml
    ├── god-object.yml
    ├── long-method.yml
    ├── magic-numbers.yml
    ├── nested-conditionals.yml
    └── unused-imports.yml
```

---

## References

- [STORY-118: Core Anti-pattern Rules](../../devforgeai/specs/Stories/STORY-118-core-antipattern-rules.story.md)
- [EPIC-018: ast-grep Foundation & Core Rules](../../devforgeai/specs/Epics/EPIC-018-astgrep-foundation-core-rules.epic.md)
- [ast-grep Documentation](https://ast-grep.github.io/)
- [DevForgeAI Anti-patterns Context](../../devforgeai/specs/context/anti-patterns.md)

---

**Created:** 2025-12-20
**Story:** STORY-118
