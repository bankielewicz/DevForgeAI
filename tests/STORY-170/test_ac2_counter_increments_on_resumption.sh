#!/bin/bash

# STORY-170 AC-2: Counter Increments on Resumption
# Test that when Phase 4.5-R triggers resumption (user rejected deferrals),
# the iteration counter increments to "Iteration 2/5"
#
# This test SHOULD FAIL initially (Red phase - TDD)
# Implementation needed: Add iteration increment logic on resumption

set -e

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"
PHASE_06_FILE=".claude/skills/devforgeai-development/phases/phase-06-deferral.md"

echo "TEST: AC-2 - Counter Increments on Resumption"
echo "=============================================="
echo ""

# Check if required files exist
if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: $SKILL_FILE does not exist"
    exit 1
fi

echo "Checking for iteration increment logic on resumption..."
echo ""

# Test 1: Check for iteration increment logic in SKILL.md
# Should contain logic to increment iteration_count when resuming
if grep -qE "iteration_count\s*(\+\+|\+=\s*1|=.*\+\s*1)" "$SKILL_FILE"; then
    echo "PASS: Found iteration_count increment logic in SKILL.md"
else
    echo "FAIL: No iteration_count increment logic found in SKILL.md"
    echo ""
    echo "Expected: Logic to increment iteration_count on resumption"
    echo "  Example: 'iteration_count += 1' or 'iteration_count = iteration_count + 1'"
    exit 1
fi

# Test 2: Check for resumption trigger documentation
# Phase 4.5-R or Phase 06 (deferral) should trigger iteration increment
if grep -qE "(resumption|resume|loop back)" "$SKILL_FILE" | grep -qE "iteration"; then
    echo "PASS: Found resumption-iteration connection"
else
    # Alternative check - look for the trigger pattern
    if grep -qE "4\.5-R|Phase 4\.5-R|deferral.*iteration" "$SKILL_FILE"; then
        echo "PASS: Found Phase 4.5-R iteration trigger reference"
    else
        echo "FAIL: No connection between resumption and iteration increment"
        echo ""
        echo "Expected: Documentation showing iteration increments when Phase 4.5-R"
        echo "          triggers resumption (user rejected deferrals)"
        exit 1
    fi
fi

# Test 3: Check that iteration increment occurs before looping back
# When resuming, iteration should increment BEFORE re-entering earlier phase
CONTEXT=$(grep -B5 -A5 "iteration_count" "$SKILL_FILE" 2>/dev/null || true)
if echo "$CONTEXT" | grep -iqE "(loop|resume|earlier phase|Phase 02|Phase 03)"; then
    echo "PASS: Iteration increment is associated with phase looping"
else
    echo "FAIL: Iteration increment not clearly tied to phase looping"
    echo ""
    echo "Expected: Iteration increments when workflow loops back to earlier phase"
    exit 1
fi

# Test 4: Check phase-06-deferral.md for resumption logic (if exists)
if [ -f "$PHASE_06_FILE" ]; then
    if grep -qE "iteration" "$PHASE_06_FILE"; then
        echo "PASS: Found iteration reference in phase-06-deferral.md"
    else
        echo "FAIL: No iteration reference in phase-06-deferral.md"
        echo ""
        echo "Expected: Phase 06 should handle iteration increment on deferral rejection"
        exit 1
    fi
else
    echo "INFO: Phase 06 file not found, checking SKILL.md only"
fi

echo ""
echo "=============================================="
echo "ALL TESTS PASSED: AC-2 Counter Increments on Resumption"
echo "=============================================="
exit 0
