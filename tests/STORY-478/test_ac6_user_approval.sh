#!/bin/bash
# Test: AC#6 - User Approval via AskUserQuestion
# Story: STORY-478
# Generated: 2026-02-23
set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET="$PROJECT_ROOT/src/claude/skills/designing-systems/references/domain-reference-generation.md"
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

echo "=== AC#6: User Approval via AskUserQuestion ==="

# Test 1: Contains AskUserQuestion
grep -q "AskUserQuestion" "$TARGET"
run_test "test_should_contain_askuserquestion_when_reference_checked" $?

# Test 2: Option "Generate all"
grep -q "Generate all" "$TARGET"
run_test "test_should_contain_generate_all_option_when_checked" $?

# Test 3: Option "Select individually"
grep -q "Select individually" "$TARGET"
run_test "test_should_contain_select_individually_option_when_checked" $?

# Test 4: Option "Skip"
grep -q "Skip" "$TARGET"
run_test "test_should_contain_skip_option_when_checked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
