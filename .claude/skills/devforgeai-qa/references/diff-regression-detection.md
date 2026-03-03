# Diff Regression Detection Phase

**Purpose:** Analyze `git diff main...HEAD` output to detect production code regressions before QA approval.

**Reference:** ADR-025 (QA Diff Regression Detection)

---

## Detection Patterns

### Function Deletion Detection

Detect removed function definitions in production code:

**Python:**
- Removed lines matching: `^-\s*def \w+\(`
- Removed lines matching: `^-\s*async def \w+\(`

**TypeScript/JavaScript:**
- Removed lines matching: `^-\s*(export\s+)?(async\s+)?function \w+\(`
- Removed lines matching: `^-\s*export\s+(const|let)\s+\w+\s*=`

**C#:**
- Removed lines matching: `^-\s*(public|private|protected|internal)\s+.*\w+\(`

### Error Handler Removal Detection

Detect removed error handling blocks:

- Removed `try/catch` block or `catch` block body
- Removed `except` handler (Python exception handler)
- Removed error handler callback or error middleware
- Deleted error boundary components

### Function Signature Change Detection

Detect modified function signatures where parameter count or types change:

- Signature change: Compare old vs new function declaration lines
- Parameter removal: Detect parameters present in `-` line but absent in `+` line
- Parameter addition: Detect new parameters in `+` line not in `-` line
- Return type change: Detect modified return type annotations or output type declarations

### Simplified Logic Detection

Detect potentially risky simplification of conditional logic:

- Removed `if/else` branches (condition removal)
- Simplified conditional expressions (branch removal)
- Removed validation checks or guard clauses
- Reduced error path coverage

---

## Severity Classification Rules

### CRITICAL — Public API Removal (Blocks QA)

**Trigger:** Removed public API endpoint, deleted exported function, or removed public interface method.

- CRITICAL severity for public API removal or exported function deletion
- **BLOCKING:** QA approval is blocked. Exit message: "QA BLOCKED: CRITICAL diff regression detected — public API removal"
- Applies to: route handlers, exported modules, public class methods

### HIGH — Internal Function or Error Handler Removal (Blocks QA)

**Trigger:** Deleted internal function body, removed private/helper function, or removed error handler.

- HIGH severity for internal function deletion (private, helper, or utility functions)
- HIGH severity for error handler or catch block removal
- **BLOCKING:** QA approval is blocked. Exit message: "QA BLOCKED: HIGH diff regression detected — internal function or error handler removed"

### MEDIUM — Logic Simplification (Warning, Non-Blocking)

**Trigger:** Simplified conditional logic, removed validation branch, or reduced error paths.

- MEDIUM severity as a warning for simplified logic (non-blocking)
- QA approval is NOT blocked for MEDIUM-only findings
- Recorded as warning in QA report for manual review

### Severity Precedence

When a single diff hunk matches multiple severity rules:
- **CRITICAL > HIGH > MEDIUM** — highest severity wins
- Example: Deleted public function with error handler → CRITICAL (not HIGH)

---

## File Exclusion Patterns

The following file patterns are excluded from production code regression analysis (test files are not scanned):

| Pattern | Description |
|---------|-------------|
| `**/tests/**` | Test directories |
| `**/*.test.*` | Test files (Jest, Vitest) |
| `**/*.spec.*` | Spec files (Angular, Jasmine) |
| `test_*.py` | Python test files |
| `*_test.py` | Python test files (alt) |
| `**/__tests__/**` | Jest test directories |
| `**/fixtures/**` | Test fixtures |

---

## Clean Pass Behavior

When the diff contains only additive changes (new functions, new files, added code) with no deletions to production code functions, error handlers, validation logic, or API endpoints:

- Phase exits with status **PASS**
- No findings are recorded
- Phase 2 (Analysis) proceeds normally

Additive-only changes that produce a clean pass include:
- New function definitions
- New file creation
- Added test coverage
- Documentation additions
- New configuration entries

---

## Moved/Renamed Function Detection

To avoid false positives for legitimate refactoring:

1. When a function is deleted in file A, check if a function with the same name is added in file B
2. If cross-file match found: Downgrade severity to MEDIUM with annotation "Function moved/renamed"
3. If no match found: Apply standard severity classification

---

## Graceful Degradation

If `git diff main...HEAD` returns a non-zero exit code:
- Log warning: "git diff failed — skipping diff regression detection"
- Set phase result to PASS (non-blocking)
- Do NOT block QA workflow due to tool failure

---

## Secret Masking

Before logging any diff content, mask lines matching:
- `password`, `api_key`, `secret`, `token`, `credential`
- Replace matched values with `[REDACTED]`

---

## Test Integrity Verification (STORY-502)

**Purpose:** Detect unauthorized test file modifications between Phase 02 (RED) and QA by comparing SHA-256 checksums against the red-phase snapshot.

### Snapshot Comparison Algorithm

1. **Load snapshot**: Read `devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json`.

   - If red-phase-checksums.json is missing or absent: Log **WARNING** — "Test integrity snapshot not found. Skipping integrity verification." QA continues without blocking. This is graceful degradation for stories created before STORY-502.

   - If snapshot JSON is malformed or unparseable: Report **CRITICAL: SNAPSHOT CORRUPT** — snapshot file exists but cannot be parsed. Set `overall_verdict = FAIL`.

2. **Compute current checksums**: For each file in the snapshot `files` array, compute SHA-256 of the current file on disk.

3. **Compare**: For each file entry, compare `expected_sha256` (from snapshot) against `actual_sha256` (computed now).

### Finding: CRITICAL: TEST TAMPERING

When a file's checksum does not match:

```
Severity: CRITICAL
Finding: TEST TAMPERING
File: {file_path}
Expected sha256: {expected_sha256}
Actual sha256: {actual_sha256}
```

This finding indicates the test file was modified after the RED phase, which may mask regressions or weaken test coverage.

### Finding: CRITICAL: UNAUTHORIZED FILE ADDED

When a test file exists on disk in the story's test directory but is NOT present in the snapshot:

```
Severity: CRITICAL
Finding: UNAUTHORIZED FILE ADDED
File: {file_path}
```

New test files added after the RED phase may contain weakened assertions or incorrect expectations.

### Finding: CRITICAL: FILE DELETED

When a file is listed in the snapshot but no longer exists on disk:

```
Severity: CRITICAL
Finding: FILE DELETED
File: {file_path}
Expected sha256: {expected_sha256}
```

Deleted test files reduce coverage and may hide failing tests.

### No Override Rule

TEST TAMPERING, UNAUTHORIZED FILE ADDED, and FILE DELETED findings **cannot be deferred or bypassed**. There is **no override** mechanism for test integrity violations. Any such finding sets `overall_verdict = FAIL` unconditionally.

### PASS Verdict

When all checksums match and no tampering is detected:

- `test_integrity` verdict: **PASS**
- `mismatched_files`: empty (no mismatches found)
- `tampering_patterns`: empty (no tampering detected)
- All files in snapshot verified present and unchanged

---

## Test Tampering Heuristic Analysis (STORY-503)

**Purpose:** When test integrity verification (above) detects a checksum mismatch, invoke detailed heuristic pattern analysis to diagnose exactly what changed.

**Reference:** See `test-tampering-heuristics.md` for the complete heuristic pattern library covering assertion weakening, test removal/skip, test body noop, and threshold lowering detection.

**Invocation:** Only when `mismatched_files` is non-empty (zero overhead when checksums match).
