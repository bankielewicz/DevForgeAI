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

### Snapshot Comparison Algorithm (STORY-560 CLI Integration)

**Execute CLI command:**

```bash
Bash(command="devforgeai-validate verify-test-integrity {STORY_ID} --project-root=.")
```

**Exit code handling:**

- **Exit code 0**: All checksums match OR snapshot missing with WARNING. Record `test_integrity: PASS`.
- **Exit code 1**: One or more checksums mismatch (TEST TAMPERING). Set `overall_verdict = FAIL` unconditionally. No override. No rationalization.
- **Exit code 2**: Error (corrupted JSON, file access error). Set `overall_verdict = FAIL`.

**Note:** The CLI command handles snapshot loading, checksum computation (using hashlib per BR-002), and comparison internally. It prints detailed output for each mismatch including expected vs actual SHA-256 values.

**Graceful degradation:** If snapshot is missing (exit code 0 with WARNING), QA continues without blocking. This is expected behavior for stories created before STORY-502.

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

**ANTI-RATIONALIZATION WARNING (RCA-046):** Do NOT attempt to explain away
checksum mismatches using environmental factors. The following rationalizations
are EXPLICITLY FORBIDDEN:

1. **WSL line endings** — "Checksums differ due to CRLF/LF conversion"
2. **Git analysis** — "git log/git show proves the file wasn't modified"
3. **Encoding differences** — "File encoding changed but content is the same"
4. **Platform artifacts** — "Different OS computed checksums differently"
5. **Tool differences** — "sha256sum vs hashlib produce different results"

The red-phase snapshot checksums ARE the ground truth. They were computed
in the same environment during Phase 02. If checksums mismatch, the file
was modified after RED phase — period. The reason for the modification is
irrelevant. Any modification invalidates test integrity.

**Action on mismatch:** Set `overall_verdict = FAIL`. No exceptions.
No analysis. No rationalization. Do not perform additional git investigation.
Do not construct alternative explanations. Report the mismatch and HALT.

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
