# AC#2 Verification: Redundant Chained Read() Calls Removed from Source Reference Files

**Story:** STORY-453
**Generated:** 2026-02-19
**Phase:** Red (tests should FAIL before implementation)

---

## Test Configuration

**Target directory:** `src/claude/skills/discovering-requirements/references/`

**6 source files and their chained targets:**

| # | Source File | Chained Target (must NOT have executable Read()) |
|---|------------|--------------------------------------------------|
| 1 | self-validation-workflow.md | validation-checklists.md |
| 2 | requirements-elicitation-workflow.md | requirements-elicitation-guide.md |
| 3 | user-input-integration-guide.md | user-input-guidance.md |
| 4 | error-type-1-incomplete-answers.md | requirements-elicitation-guide.md |
| 5 | error-type-3-complexity-errors.md | complexity-assessment-matrix.md |
| 6 | error-type-4-validation-failures.md | validation-checklists.md |

---

## Verification Script

```bash
#!/bin/bash
# AC#2 Verification Script - STORY-453
# Run from project root

REF_DIR="src/claude/skills/discovering-requirements/references"
PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#2: Redundant Chained Read() Calls Removed ==="
echo ""

# Pattern: executable Read() calls look like Read(file_path="...target...")
# We exclude lines that are comments, prose descriptions, or inside markdown code fences
# that are clearly documentation rather than executable instructions.
# The pattern matches: Read(file_path="...targetfile...")

# --- Test 1: self-validation-workflow.md must NOT have executable Read() for validation-checklists ---
MATCHES=$(grep -cP 'Read\(file_path=.*validation-checklists' "$REF_DIR/self-validation-workflow.md" 2>/dev/null || echo "0")
[ "$MATCHES" -eq 0 ]
run_test "self-validation-workflow.md: no executable Read() for validation-checklists.md (found: $MATCHES)" $?

# --- Test 2: requirements-elicitation-workflow.md must NOT have executable Read() for requirements-elicitation-guide ---
MATCHES=$(grep -cP 'Read\(file_path=.*requirements-elicitation-guide' "$REF_DIR/requirements-elicitation-workflow.md" 2>/dev/null || echo "0")
[ "$MATCHES" -eq 0 ]
run_test "requirements-elicitation-workflow.md: no executable Read() for requirements-elicitation-guide.md (found: $MATCHES)" $?

# --- Test 3: user-input-integration-guide.md must NOT have executable Read() for user-input-guidance ---
MATCHES=$(grep -cP 'Read\(file_path=.*user-input-guidance' "$REF_DIR/user-input-integration-guide.md" 2>/dev/null || echo "0")
[ "$MATCHES" -eq 0 ]
run_test "user-input-integration-guide.md: no executable Read() for user-input-guidance.md (found: $MATCHES)" $?

# --- Test 4: error-type-1-incomplete-answers.md must NOT have executable Read() for requirements-elicitation-guide ---
MATCHES=$(grep -cP 'Read\(file_path=.*requirements-elicitation-guide' "$REF_DIR/error-type-1-incomplete-answers.md" 2>/dev/null || echo "0")
[ "$MATCHES" -eq 0 ]
run_test "error-type-1-incomplete-answers.md: no executable Read() for requirements-elicitation-guide.md (found: $MATCHES)" $?

# --- Test 5: error-type-3-complexity-errors.md must NOT have executable Read() for complexity-assessment-matrix ---
MATCHES=$(grep -cP 'Read\(file_path=.*complexity-assessment-matrix' "$REF_DIR/error-type-3-complexity-errors.md" 2>/dev/null || echo "0")
[ "$MATCHES" -eq 0 ]
run_test "error-type-3-complexity-errors.md: no executable Read() for complexity-assessment-matrix.md (found: $MATCHES)" $?

# --- Test 6: error-type-4-validation-failures.md must NOT have executable Read() for validation-checklists ---
MATCHES=$(grep -cP 'Read\(file_path=.*validation-checklists' "$REF_DIR/error-type-4-validation-failures.md" 2>/dev/null || echo "0")
[ "$MATCHES" -eq 0 ]
run_test "error-type-4-validation-failures.md: no executable Read() for validation-checklists.md (found: $MATCHES)" $?

# --- Test 7: No new chains introduced - scan ALL reference files for inter-reference Read() ---
# Count total executable Read() calls targeting other files within the references/ directory
NEW_CHAINS=$(grep -rlP 'Read\(file_path=.*references/' "$REF_DIR"/*.md 2>/dev/null | wc -l)
[ "$NEW_CHAINS" -eq 0 ]
run_test "No reference files chain-load other reference files (files with chains: $NEW_CHAINS)" $?

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ $FAILED -eq 0 ] && exit 0 || exit 1
```

---

## Expected Results (Red Phase)

| Test | Expected | Reason |
|------|----------|--------|
| Test 1: self-validation-workflow.md | FAIL | Chained Read() still present |
| Test 2: requirements-elicitation-workflow.md | FAIL | Chained Read() still present |
| Test 3: user-input-integration-guide.md | FAIL | Chained Read() still present |
| Test 4: error-type-1-incomplete-answers.md | FAIL | Chained Read() still present |
| Test 5: error-type-3-complexity-errors.md | FAIL | Chained Read() still present |
| Test 6: error-type-4-validation-failures.md | FAIL | Chained Read() still present |
| Test 7: No new chains | FAIL | Existing chains still present |

---

## Verification Evidence

After implementation, re-run the script and paste output here:

```
(pending implementation)
```
