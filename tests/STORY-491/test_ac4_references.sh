#!/bin/bash
# Test: AC#4 - investigation-patterns.md has 6 categories; workflow-integration.md has 3 integration points
# Story: STORY-491
# Generated: 2026-02-23

PASSED=0
FAILED=0
PATTERNS_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/root-cause-diagnosis/references/investigation-patterns.md"
WORKFLOW_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/root-cause-diagnosis/references/workflow-integration.md"

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

echo "=== AC#4: Reference Files ==="

# --- investigation-patterns.md ---

# Test 1: File exists
test -f "$PATTERNS_FILE"
run_test "investigation-patterns.md file exists" $?

# Test 2-7: All 6 failure categories present
CATEGORIES=("Spec Drift" "Test Assertion" "Import/Dependency|Import.Dependency" "Coverage Gap" "Anti-Pattern Violation|Anti.Pattern" "DoD.*Commit|Commit.*Validation|DoD.*Validation")
CATEGORY_NAMES=("Spec Drift" "Test Assertion" "Import/Dependency" "Coverage Gaps" "Anti-Pattern Violations" "DoD/Commit Validation")
for i in "${!CATEGORIES[@]}"; do
    grep -qiE "${CATEGORIES[$i]}" "$PATTERNS_FILE" 2>/dev/null
    run_test "Category present: ${CATEGORY_NAMES[$i]}" $?
done

# --- workflow-integration.md ---

# Test 8: File exists
test -f "$WORKFLOW_FILE"
run_test "workflow-integration.md file exists" $?

# Test 9: Phase 03 integration
grep -qi "phase.*03\|phase.*3\|phase-03" "$WORKFLOW_FILE" 2>/dev/null
run_test "Phase 03 integration documented" $?

# Test 10: Phase 05 integration
grep -qi "phase.*05\|phase.*5\|phase-05" "$WORKFLOW_FILE" 2>/dev/null
run_test "Phase 05 integration documented" $?

# Test 11: QA Phase 2 integration
grep -qi "qa.*phase.*2\|qa.*phase-2\|qa.*phase 2" "$WORKFLOW_FILE" 2>/dev/null
run_test "QA Phase 2 integration documented" $?

# Test 12: Contains pseudocode/code blocks
grep -q '```' "$WORKFLOW_FILE" 2>/dev/null
run_test "Contains pseudocode blocks" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
