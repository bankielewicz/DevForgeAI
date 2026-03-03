#!/bin/bash
# Test: AC#1 - Phase file contains Step 4.5 with correct title, Edit patterns, and reference
# Story: STORY-516
# Generated: 2026-02-28

PASSED=0
FAILED=0

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/implementing-stories/phases/phase-07-dod-update.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#1: Phase file Step 4.5 ==="

# Test 1: Step 4.5 heading with "Populate TDD" present
grep -q '4\.5\..*Populate.*TDD' "$TARGET_FILE"
run_test "Step 4.5 heading contains Populate TDD" $?

# Test 2: Step 4.5 area contains Edit( pattern and TDD Workflow Summary
grep -A 30 '4\.5\..*Populate.*TDD' "$TARGET_FILE" | grep -q 'Edit('
run_test "Step 4.5 contains Edit( pattern" $?

grep -A 30 '4\.5\..*Populate.*TDD' "$TARGET_FILE" | grep -q 'TDD Workflow Summary'
run_test "Step 4.5 references TDD Workflow Summary" $?

# Test 3: Step 4.5 references dod-update-workflow.md Step 5 for detailed template
grep -A 40 '4\.5\..*Populate.*TDD' "$TARGET_FILE" | grep -q 'Step 5'
run_test "Step 4.5 references Step 5 for detailed template" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
