#!/bin/bash
# Test: AC#3 - diagnosis-before-fix.md has HALT trigger, references root-cause-diagnosis skill
# Story: STORY-491
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/rules/workflow/diagnosis-before-fix.md"

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

echo "=== AC#3: Rule HALT Trigger ==="

# Test 1: File exists
test -f "$TARGET_FILE"
run_test "diagnosis-before-fix.md file exists" $?

# Test 2: Contains HALT trigger
grep -qi "HALT" "$TARGET_FILE" 2>/dev/null
run_test "Contains HALT trigger keyword" $?

# Test 3: References root-cause-diagnosis skill
grep -q "root-cause-diagnosis" "$TARGET_FILE" 2>/dev/null
run_test "References root-cause-diagnosis skill" $?

# Test 4: Contains trigger condition (when to halt)
grep -qi "trigger\|when\|before.*fix\|diagnosis.*before" "$TARGET_FILE" 2>/dev/null
run_test "Contains trigger condition for when rule activates" $?

# Test 5: Is a workflow rule (has rule-like structure)
grep -qi "rule\|enforcement\|mandatory\|must" "$TARGET_FILE" 2>/dev/null
run_test "Contains enforcement/mandatory language" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
