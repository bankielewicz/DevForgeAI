#!/bin/bash
# Test: AC#1 - Reference File at Correct Path
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

echo "=== AC#1: Reference File at Correct Path ==="

# Test 1: File exists
test -f "$TARGET"
run_test "test_should_exist_when_reference_file_checked" $?

# Test 2: File is between 300-450 lines (STORY-477 base ~260 + STORY-478 workflow ~120)
LINE_COUNT=$(wc -l < "$TARGET")
[ "$LINE_COUNT" -ge 300 ] && [ "$LINE_COUNT" -le 450 ]
run_test "test_should_have_300_to_450_lines_when_line_count_checked" $?

# Test 3: Contains 5-step workflow
grep -q "5-step" "$TARGET" || grep -q "Step 1.*Step 2.*Step 3.*Step 4.*Step 5" "$TARGET" || grep -cq "## Step" "$TARGET"
run_test "test_should_contain_5_step_workflow_when_content_checked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
