#!/bin/bash
# STORY-262 Test Specification Validation
# TDD Red Phase: All tests should FAIL initially

TARGET=".claude/skills/devforgeai-development/phases/phase-04-refactoring.md"
PASS=0
FAIL=0

run_test() {
    local id="$1"
    local desc="$2"
    local cmd="$3"

    if eval "$cmd" 2>/dev/null; then
        echo "[PASS] $id: $desc"
        ((PASS++))
    else
        echo "[FAIL] $id: $desc"
        ((FAIL++))
    fi
}

echo "=== STORY-262 Test Specification Validation ==="
echo "Target: $TARGET"
echo ""

run_test "T-001" "Step 2a exists" \
    "grep -qE 'Step\s+2a|[0-9]+a\.' $TARGET"

run_test "T-002" "Coverage thresholds (95/85/80)" \
    "grep -q '95' $TARGET && grep -q '85' $TARGET && grep -q '80' $TARGET"

run_test "T-003" "test-automator remediation invocation" \
    "grep -qE 'Task.*test-automator' $TARGET"

run_test "T-004" "REMEDIATION_MODE flag" \
    "grep -qiE 'remediation.?mode' $TARGET"

run_test "T-005" "Normal flow bypass" \
    "grep -qiE 'proceed.*(threshold|coverage)' $TARGET"

run_test "T-006" "Validation checkpoint coverage" \
    "grep -A20 'Validation Checkpoint' $TARGET | grep -qiE 'coverage'"

run_test "T-007" "phase-state.json observation" \
    "grep -qiE 'coverage.*(observation|percentage)' $TARGET"

run_test "T-008" "Step 2a entry/exit gates" \
    "[ \$(grep -ciE 'entry.*(gate|condition)|exit.*(gate|condition)' $TARGET) -ge 4 ]"

run_test "T-009" "Coverage parsing (COMP-001)" \
    "grep -qiE 'parse.*coverage|extract.*percent' $TARGET"

run_test "T-010" ">= threshold comparison (COMP-003)" \
    "grep -qE '>=|greater.*equal' $TARGET"

run_test "T-011" "Graceful fallback (COMP-005)" \
    "grep -qiE 'fallback|graceful|fail.*safe' $TARGET"

run_test "T-012" "2-cycle remediation limit (BR-005)" \
    "grep -qiE '(2|two).*(cycle|attempt)' $TARGET"

echo ""
echo "=== Results ==="
echo "PASS: $PASS"
echo "FAIL: $FAIL"
echo "Total: $((PASS + FAIL))"

exit $FAIL
