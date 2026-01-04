#!/bin/bash

# STORY-170 AC-1: Iteration Counter in Phase Headers
# Test that phase headers include iteration number in format: "TDD Iteration: X/5"
#
# This test SHOULD FAIL initially (Red phase - TDD)
# Implementation needed: Add "TDD Iteration: X/5" to phase headers in SKILL.md

set -e

SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"

echo "TEST: AC-1 - Iteration Counter in Phase Headers"
echo "================================================"
echo ""

# Check if SKILL.md exists
if [ ! -f "$SKILL_FILE" ]; then
    echo "FAIL: $SKILL_FILE does not exist"
    exit 1
fi

echo "Checking for iteration counter format in phase headers..."
echo ""

# Test 1: Check that SKILL.md contains the new phase header format with iteration
# Looking for pattern like "TDD Iteration:" in phase display templates
if grep -q "TDD Iteration:" "$SKILL_FILE"; then
    echo "PASS: Found 'TDD Iteration:' pattern in SKILL.md"
else
    echo "FAIL: 'TDD Iteration:' pattern not found in SKILL.md"
    echo ""
    echo "Expected format in phase headers:"
    echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Phase 2/10: Implementation - Green Phase"
    echo "  TDD Iteration: 1/5"
    echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 1
fi

# Test 2: Check the format includes X/5 (iteration count out of max 5)
if grep -qE "TDD Iteration:.*[0-9]/5" "$SKILL_FILE"; then
    echo "PASS: Found iteration counter with X/5 format"
else
    echo "FAIL: Iteration counter X/5 format not found"
    echo ""
    echo "Expected: 'TDD Iteration: 1/5' (or similar)"
    exit 1
fi

# Test 3: Verify iteration counter appears in phase display template section
# Look for it near the Phase NN/10 display patterns
PHASE_DISPLAY_SECTION=$(grep -A5 "Phase NN/10:" "$SKILL_FILE" 2>/dev/null || true)

if echo "$PHASE_DISPLAY_SECTION" | grep -q "TDD Iteration:"; then
    echo "PASS: Iteration counter is placed in phase display template"
else
    echo "FAIL: Iteration counter not found in phase display template section"
    echo ""
    echo "The TDD Iteration line should appear in the phase display template:"
    echo "  Phase NN/10: [Phase Name]"
    echo "  TDD Iteration: X/5"
    exit 1
fi

# Test 4: Check for iteration_count variable initialization
if grep -qE "iteration_count\s*=\s*1" "$SKILL_FILE"; then
    echo "PASS: Found iteration_count initialization"
else
    echo "FAIL: iteration_count variable initialization not found"
    echo ""
    echo "Expected: 'iteration_count = 1' in workflow initialization"
    exit 1
fi

echo ""
echo "================================================"
echo "ALL TESTS PASSED: AC-1 Iteration Counter in Phase Headers"
echo "================================================"
exit 0
