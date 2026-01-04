#!/bin/bash

# STORY-170 AC-3: Warning at High Iterations
# Test that when iteration count reaches 4 of 5, a warning indicator appears:
# "Iteration 4/5 - Approaching limit"
#
# This test SHOULD FAIL initially (Red phase - TDD)
# Implementation needed: Add warning display logic at iteration threshold

set -e

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"

echo "TEST: AC-3 - Warning at High Iterations"
echo "========================================"
echo ""

# Check if SKILL.md exists
if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: $SKILL_FILE does not exist"
    exit 1
fi

echo "Checking for high iteration warning logic..."
echo ""

# Test 1: Check for "Approaching limit" warning text
if grep -q "Approaching limit" "$SKILL_FILE"; then
    echo "PASS: Found 'Approaching limit' warning text"
else
    echo "FAIL: 'Approaching limit' warning text not found"
    echo ""
    echo "Expected: Warning message 'Approaching limit' or 'Iteration 4/5 - Approaching limit'"
    exit 1
fi

# Test 2: Check for iteration threshold check (iteration >= 4 or == 4)
if grep -qE "(iteration.*>=?\s*4|iteration.*==\s*4|iteration_count.*>=?\s*4|iteration_count.*==\s*4)" "$SKILL_FILE"; then
    echo "PASS: Found iteration threshold check for 4"
else
    echo "FAIL: No iteration threshold check for 4 found"
    echo ""
    echo "Expected: Logic like 'if iteration_count >= 4' or 'if iteration == 4'"
    exit 1
fi

# Test 3: Check for conditional warning display logic
# Looking for IF/WHEN condition tied to high iteration and warning
WARNING_CONTEXT=$(grep -B3 -A3 "Approaching limit" "$SKILL_FILE" 2>/dev/null || true)
if echo "$WARNING_CONTEXT" | grep -qE "(IF|WHEN|if|when|>=|==)"; then
    echo "PASS: Warning is conditionally displayed"
else
    echo "FAIL: Warning is not conditionally displayed"
    echo ""
    echo "Expected: Conditional logic that displays warning only at high iterations"
    exit 1
fi

# Test 4: Check for complete warning format in phase header context
# Should show format like: "Iteration 4/5 - Approaching limit"
if grep -qE "Iteration\s+4/5\s*-?\s*Approaching limit" "$SKILL_FILE"; then
    echo "PASS: Found complete warning format 'Iteration 4/5 - Approaching limit'"
else
    # Alternative: check for template pattern with variable
    if grep -qE "Iteration.*Approaching limit" "$SKILL_FILE"; then
        echo "PASS: Found iteration warning template pattern"
    else
        echo "FAIL: Complete warning format not found"
        echo ""
        echo "Expected format: 'Iteration 4/5 - Approaching limit'"
        exit 1
    fi
fi

# Test 5: Check that max iterations is documented as 5
if grep -qE "(max.*iteration.*5|iteration.*max.*5|/5|out of 5)" "$SKILL_FILE"; then
    echo "PASS: Max iteration count of 5 is documented"
else
    echo "FAIL: Max iteration count of 5 not documented"
    echo ""
    echo "Expected: Documentation showing max iterations = 5"
    exit 1
fi

echo ""
echo "========================================"
echo "ALL TESTS PASSED: AC-3 Warning at High Iterations"
echo "========================================"
exit 0
