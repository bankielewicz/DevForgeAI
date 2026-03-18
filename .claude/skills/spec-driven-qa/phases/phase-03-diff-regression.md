# Phase 03: Diff Regression Detection

## Entry Gate

```bash
devforgeai-validate phase-check ${STORY_ID} --workflow=qa --from=02 --to=03 --project-root=.
# Exit 0: proceed | Exit 1: Phase 02 incomplete
```

## Contract

PURPOSE: Analyze git diff for production code regressions and verify test integrity.
REQUIRED SUBAGENTS: none
REQUIRED ARTIFACTS: Regression findings list, test integrity result, phase result (PASS/BLOCKED/WARN)
STEP COUNT: 5 mandatory steps

---

## Reference Loading

Load BEFORE executing steps:
```
Read(file_path=".claude/skills/spec-driven-qa/references/diff-regression-detection.md")
```

---

## Mandatory Steps

### Step 3.1: Execute Git Diff

EXECUTE: Run git diff to get unified diff output between main branch and HEAD. Parse output into structured hunks.
```
Bash(command="git diff main...HEAD --unified=3 2>/dev/null || git diff HEAD~1 --unified=3")

# Parse unified diff output into structured hunks:
# - file_path
# - change_type (added/modified/deleted)
# - hunks[] with line ranges and content
```
VERIFY: Diff output parsed successfully. Hunk count > 0 OR empty diff (no changes = PASS).
```
IF diff is empty:
    Display: "No changes detected -- diff regression PASS"
    Skip to Step 3.5 with result = PASS
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=03 --step=3.1 --project-root=.`

---

### Step 3.2: Apply File Exclusion

EXECUTE: Exclude test files from regression analysis. Test files should only be analyzed for integrity (Step 3.4), not for regressions.
```
Exclusion patterns:
- **/tests/**
- **/*.test.*
- **/*.spec.*
- test_*.py
- *_test.py
- *_test.go

production_hunks = [h for h in hunks if not matches_exclusion(h.file_path)]
test_hunks = [h for h in hunks if matches_exclusion(h.file_path)]

Display: "Production files: {len(production_hunks)} | Test files: {len(test_hunks)} (excluded from regression scan)"
```
VERIFY: production_hunks list populated. test_hunks separated for Step 3.4.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=03 --step=3.2 --project-root=.`

---

### Step 3.3: Scan for Regressions

EXECUTE: Scan production hunks for regression patterns.
```
Regression patterns to detect:
1. Function/method deletion (def/function/func removed without replacement)
2. Error handler removal (try/catch/except blocks removed)
3. Signature changes (parameter additions/removals that break callers)
4. Simplified logic (complex validation replaced with pass-through)
5. Weakened validation (stricter checks replaced with looser ones)
6. Removed logging/monitoring (observability regression)

FOR each production_hunk:
    FOR each pattern:
        IF hunk matches pattern:
            findings.append({
                file: hunk.file_path,
                line: hunk.start_line,
                type: pattern.name,
                severity: pattern.severity,  # CRITICAL, HIGH, MEDIUM
                description: pattern.describe(hunk)
            })

Display: "Regression findings: {len(findings)} ({critical} CRITICAL, {high} HIGH, {medium} MEDIUM)"
```
VERIFY: Findings list generated (may be empty = good). Each finding has severity classification.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=03 --step=3.3 --project-root=.`

---

### Step 3.4: Test Integrity Verification (STORY-502)

EXECUTE: If red-phase checksum snapshot exists, compare current test file checksums against it. Detects unauthorized test modifications.
```
snapshot_path = "devforgeai/qa/snapshots/${STORY_ID}/red-phase-checksums.json"
Glob(pattern=snapshot_path)

IF snapshot exists:
    Read(file_path=snapshot_path)
    snapshot = parse_json(content)

    FOR each test_file in snapshot.files:
        # Calculate current SHA256
        current_hash = Bash(command="sha256sum {test_file.path} | cut -d' ' -f1")

        IF current_hash != test_file.checksum:
            test_integrity_result = "CRITICAL: TEST TAMPERING DETECTED"
            tampering_findings.append({
                file: test_file.path,
                expected: test_file.checksum,
                actual: current_hash,
                severity: "CRITICAL",
                blocking: true  # No override possible
            })

    IF no mismatches:
        test_integrity_result = "PASS"
        Display: "Test integrity: PASS (all checksums match)"

ELSE:
    test_integrity_result = "SKIPPED"
    Display: "Test integrity: SKIPPED (no red-phase snapshot found -- graceful degradation)"
```
VERIFY: test_integrity_result is set to PASS, CRITICAL, or SKIPPED.
```
IF test_integrity_result == "CRITICAL":
    Display: "CRITICAL: Test tampering detected -- QA BLOCKED (no override)"
    # This finding blocks unconditionally
```
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=03 --step=3.4 --project-root=.`

---

### Step 3.5: Classify and Determine Result

EXECUTE: Aggregate all findings and determine phase result.
```
all_findings = findings + tampering_findings

IF any finding with severity == "CRITICAL" OR test_integrity_result == "CRITICAL":
    phase_3_result = "BLOCKED"
    Display: "Phase 03 Result: BLOCKED -- CRITICAL findings prevent QA approval"
ELIF any finding with severity == "HIGH":
    phase_3_result = "BLOCKED"
    Display: "Phase 03 Result: BLOCKED -- HIGH findings prevent QA approval"
ELIF any finding with severity == "MEDIUM":
    phase_3_result = "WARN"
    Display: "Phase 03 Result: WARN -- MEDIUM findings noted, QA continues"
ELSE:
    phase_3_result = "PASS"
    Display: "Phase 03 Result: PASS -- no regression findings"

# Store result for Phase 05 aggregation
qa_report_data["diff_regression"] = {
    result: phase_3_result,
    findings: all_findings,
    test_integrity: test_integrity_result
}
```
VERIFY: phase_3_result is set to PASS, BLOCKED, or WARN.
RECORD: `devforgeai-validate phase-record ${STORY_ID} --workflow=qa --phase=03 --step=3.5 --project-root=.`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${STORY_ID} --workflow=qa --phase=03 --checkpoint-passed --project-root=.
# Exit 0: proceed to Phase 04 | Exit 1: HALT
```

## Phase 03 Completion Display

```
Phase 03 Complete: Diff Regression Detection
  Result: {phase_3_result}
  Test integrity: {test_integrity_result}
  Findings: {critical} CRITICAL, {high} HIGH, {medium} MEDIUM
```
