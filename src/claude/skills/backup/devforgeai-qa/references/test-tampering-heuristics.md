# Test Tampering Heuristic Patterns

**Purpose:** Diagnose exactly what changed in tampered test files when Feature 2 (checksums) detects a SHA-256 mismatch. Provides actionable evidence of tampering behavior.

**Reference:** STORY-503, ADR-025 (QA Diff Regression Detection)

---

## Assertion Weakening Patterns — Severity: CRITICAL

**Category:** `assertion_weakening`

Detects when strict assertions are replaced with weaker alternatives:

| Before | After | Language | Pattern |
|--------|-------|----------|---------|
| `toBe(expected)` | `toBeTruthy()` | JavaScript/TypeScript | Exact match replaced with truthy check |
| `assertEqual(a, b)` | `assertIn(a, collection)` | Python | Equality replaced with membership |
| `assertEquals(a, b)` | `assertTrue(condition)` | Python/Java | Equality replaced with boolean |
| `toEqual(exact)` | `toContain(partial)` | JavaScript/TypeScript | Exact match replaced with contains check |
| `toStrictEqual(exact)` | `toEqual(loose)` | JavaScript/TypeScript | Strict equality replaced with loose equality |

**Grep Detection Patterns:**
- `toBe` → `toBeTruthy`: `grep -n "toBeTruthy" {file}` (was `toBe`)
- `assertEqual` → `assertIn`: `grep -n "assertIn" {file}` (was `assertEqual`)
- `assertEquals` → `assertTrue`: `grep -n "assertTrue" {file}` (was `assertEquals`)

**Assertion weakening patterns are always CRITICAL severity — no override.**

---

## Test Removal and Skip Patterns — Severity: CRITICAL

**Category:** `test_removal_skip`

Detects deleted test functions and added skip decorators:

### Deleted Test Functions

When a function present in the Red-phase snapshot is absent in the current file:
- Python: `def test_` function no longer exists
- JavaScript: `it(`, `test(`, `describe(` blocks removed
- Report as: deleted test function with file path and original line number

### Skip/Xfail Suffixes Added

- `.skip` suffix added to `describe.skip`, `it.skip`, `test.skip`
- `.xfail` suffix added (pytest expected failure)

### Skip Decorators Added

- `@unittest.skip` decorator added to test method
- `@pytest.mark.skip` decorator added to test function
- `@pytest.mark.skipIf` decorator added with always-true condition

**Test removal/skip patterns are always CRITICAL severity — no override.**

---

## Test Body Noop Patterns — Severity: CRITICAL

**Category:** `test_body_noop`

Detects when test bodies are replaced with no-operation equivalents:

### Pass Substitution

Test body replaced with `pass` statement (Python) — the function signature exists but does nothing.

### Single Comment Substitution

Test body replaced with a single comment like `# TODO` or `// placeholder` — effectively a noop.

### Noop/Empty Block Detection

Test body replaced with empty block `{}` (JavaScript) or contains only `return` with no assertions.

**Test body noop patterns are always CRITICAL severity — no override.**

---

## Threshold Lowering Patterns — Severity: CRITICAL

**Category:** `threshold_lowering`

Detects when test configuration thresholds are weakened:

### Coverage Threshold Reduction

Coverage percentage lowered (e.g., 95% → 80%) in configuration files, CI configs, or test runner settings.

### Timeout Increase

Timeout values significantly increased (e.g., 5000ms → 60000ms), potentially masking slow/hanging tests.

### Retry Count Addition

Retry/flaky-test retry counts added where none existed, allowing intermittent failures to pass.

### Tolerance Range Widening

Numeric tolerance or delta values widened (e.g., `delta=0.01` → `delta=1.0`), accepting imprecise results.

**Threshold lowering patterns are always CRITICAL severity — no override.**

---

## Unclassified Fallback

**Category:** `unclassified_modification`

When a checksum mismatch is detected but none of the above patterns match:
- Report as `unclassified_modification` finding
- Still **CRITICAL** severity (unclassified modifications are CRITICAL)
- Ensures 100% mismatch coverage — every mismatched file produces at least one finding
- Examples: whitespace-only changes, import reordering, variable renames within tests

---

## Comparison Algorithm

**Line-by-line diff between snapshot and current file:**

1. Load Red-phase snapshot content for the mismatched file
2. Load current on-disk content
3. Compute line-by-line diff (added, removed, changed lines)
4. Apply pattern matchers in order: assertion_weakening → test_removal_skip → test_body_noop → threshold_lowering
5. Any remaining unmatched changes → unclassified_modification fallback
6. Each finding includes: file path, line number, before content, after content, pattern type

---

## Integration Protocol

**Conditional Invocation:** Heuristic analysis is only invoked when Feature 2 (checksum verification) reports `mismatched_files` as non-empty. When zero mismatches are detected, heuristic analysis is NOT invoked — zero overhead, skip heuristic analysis entirely.

**Invocation Flow:**
1. Feature 2 computes checksums and compares against Red-phase snapshot
2. IF `mismatched_files` list is empty → PASS, no heuristic analysis needed
3. IF `mismatched_files` list is non-empty → invoke heuristic pattern analyzer
4. Analyzer processes each mismatched file independently
5. Failure on one file does not prevent analysis of remaining files (BR-004)

---

## Report Integration: tampering_patterns Array

When heuristic analysis detects tampering, findings are written to the `test_integrity.tampering_patterns` array in `diff-regression-report.json`:

### Finding Schema

Each entry in the `tampering_patterns` array contains:

| Field | Type | Description |
|-------|------|-------------|
| `"file"` | string | File path of the tampered test file |
| `"line"` | integer | Line number where tampering detected |
| `"type"` | string | Pattern type: `assertion_weakening`, `test_removal_skip`, `test_body_noop`, `threshold_lowering`, or `unclassified_modification` |
| `"before"` | string | Before content (from Red-phase snapshot) |
| `"after"` | string | After content (current on-disk) |

### Verdict Behavior

When any tampering patterns are found:
- `overall_verdict`: **FAIL** — QA blocked with no override
- No deferral path exists for test tampering findings

---

## Error Handling

- **Unreadable file:** Report as `ANALYSIS_ERROR` with CRITICAL severity; continue analyzing remaining files
- **Malformed snapshot:** Report as `CRITICAL: SNAPSHOT CORRUPT`; set overall_verdict = FAIL
- **Pattern match error:** Log warning, continue with remaining patterns

---

## Performance Requirements

- Single file analysis: < 2 seconds per file (up to 500 lines)
- Total analysis: < 15 seconds for up to 10 mismatched files
- Deterministic: identical inputs produce identical findings
