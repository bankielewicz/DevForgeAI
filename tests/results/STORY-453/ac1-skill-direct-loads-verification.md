# AC#1 Verification: All 6 Chains Flattened - Direct Load Instructions Added to SKILL.md

**Story:** STORY-453
**Generated:** 2026-02-19
**Phase:** Red (tests should FAIL before implementation)

---

## Test Configuration

**Target file:** `src/claude/skills/discovering-requirements/SKILL.md`

---

## Verification Script

Run the following commands from project root. All tests must PASS (exit 0) for AC#1 to be verified.

```bash
#!/bin/bash
# AC#1 Verification Script - STORY-453
# Run from project root: bash src/tests/results/STORY-453/ac1-skill-direct-loads-verification.md.sh

SKILL_FILE="src/claude/skills/discovering-requirements/SKILL.md"
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

echo "=== AC#1: Direct Load Instructions in SKILL.md ==="
echo ""

# --- Test 1: requirements-elicitation-guide.md direct Read() exists in Phase 2 ---
# Extract Phase 2 section and check for direct Read() of requirements-elicitation-guide.md
# The Read() must be in Phase 2, not just anywhere in the file
PHASE2_HAS_READ=$(sed -n '/## Phase 2/,/## Phase 3/p' "$SKILL_FILE" | grep -c 'Read(file_path=.*requirements-elicitation-guide\.md')
[ "$PHASE2_HAS_READ" -ge 1 ]
run_test "requirements-elicitation-guide.md Read() present in Phase 2 section" $?

# --- Test 2: validation-checklists.md direct Read() exists in Phase 3.3 ---
# The Read() must be in Phase 3 / Step 3.3 section
PHASE3_HAS_READ=$(sed -n '/## Phase 3/,/## Phase 4/p' "$SKILL_FILE" | grep -c 'Read(file_path=.*validation-checklists\.md')
[ "$PHASE3_HAS_READ" -ge 1 ]
run_test "validation-checklists.md Read() present in Phase 3 section" $?

# --- Test 3: user-input-guidance.md already loaded in Step 0.5 ---
# Confirm existing Read() for user-input-guidance.md is present (should already be there)
STEP05_HAS_READ=$(sed -n '/Step 0\.5/,/Step 0\.6\|## Phase 1/p' "$SKILL_FILE" | grep -c 'Read(file_path=.*user-input-guidance\.md')
[ "$STEP05_HAS_READ" -ge 1 ]
run_test "user-input-guidance.md Read() confirmed in Step 0.5" $?

# --- Test 4: SKILL.md line count <= 500 ---
LINE_COUNT=$(wc -l < "$SKILL_FILE")
[ "$LINE_COUNT" -le 500 ]
run_test "SKILL.md line count <= 500 (actual: $LINE_COUNT)" $?

# --- Test 5: No duplicate loads - requirements-elicitation-guide.md Read() count ---
# Should appear exactly once as a direct Read() (in Phase 2)
TOTAL_REG=$(grep -c 'Read(file_path=.*requirements-elicitation-guide\.md' "$SKILL_FILE")
[ "$TOTAL_REG" -le 2 ]
run_test "requirements-elicitation-guide.md not excessively duplicated (count: $TOTAL_REG)" $?

# --- Test 6: No duplicate loads - validation-checklists.md Read() count ---
TOTAL_VC=$(grep -c 'Read(file_path=.*validation-checklists\.md' "$SKILL_FILE")
[ "$TOTAL_VC" -le 2 ]
run_test "validation-checklists.md not excessively duplicated (count: $TOTAL_VC)" $?

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ $FAILED -eq 0 ] && exit 0 || exit 1
```

---

## Expected Results (Red Phase)

| Test | Expected | Reason |
|------|----------|--------|
| Test 1: requirements-elicitation-guide.md in Phase 2 | FAIL | Direct Read() not yet added |
| Test 2: validation-checklists.md in Phase 3 | FAIL | Direct Read() not yet added |
| Test 3: user-input-guidance.md in Step 0.5 | PASS or FAIL | May already exist |
| Test 4: SKILL.md <= 500 lines | PASS | Baseline is 407 lines |
| Test 5: No duplicate requirements-elicitation-guide | PASS | Not yet added |
| Test 6: No duplicate validation-checklists | PASS | Not yet added |

---

## Verification Evidence

After implementation, re-run the script and paste output here:

```
(pending implementation)
```
