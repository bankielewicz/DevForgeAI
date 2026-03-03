#!/bin/bash
# Test: AC#4 - Phase 04 Reflection Capture on Refactoring Failure
# Story: STORY-338
# Expected: FAIL (RED phase) - Reflection Capture section does not exist yet
#
# Acceptance Criteria:
# - tdd-refactor-phase.md contains reflection capture section
# - Test-specific what_happened with test reference
# - REF-04-* ID pattern documented

set -e

# Files to test - both src/ and operational copies
SRC_PHASE_FILE="src/claude/skills/devforgeai-development/references/tdd-refactor-phase.md"
OP_PHASE_FILE=".claude/skills/devforgeai-development/references/tdd-refactor-phase.md"

TEST_NAME="AC4: Phase 04 Reflection Capture"

echo "=== $TEST_NAME ==="

# Use operational file if it exists, otherwise src/
if [ -f "$OP_PHASE_FILE" ]; then
    PHASE_FILE="$OP_PHASE_FILE"
else
    PHASE_FILE="$SRC_PHASE_FILE"
fi

if [ ! -f "$PHASE_FILE" ]; then
    echo "  FAIL: Phase file not found at $PHASE_FILE"
    exit 1
fi

echo "Testing file: $PHASE_FILE"

# Test 1: Verify "Reflection Capture" section header exists
echo "Test 1: Checking for 'Reflection Capture' section header..."
if grep -qE "##+ Reflection Capture on Failure|##+ Reflection Capture \(EPIC-051\)" "$PHASE_FILE"; then
    echo "  PASS: Section header found"
else
    echo "  FAIL: Section header 'Reflection Capture on Failure' not found"
    exit 1
fi

# Test 2: Verify what_happened includes test/refactoring reference
echo "Test 2: Checking for test-specific what_happened..."
if grep -qi "what_happened" "$PHASE_FILE"; then
    # Check for test-specific language (test, broke, failed, refactoring)
    if grep -qiE "test|refactor|broke|failed" "$PHASE_FILE"; then
        echo "  PASS: Test-specific what_happened instructions found"
    else
        echo "  FAIL: what_happened lacks test-specific references"
        exit 1
    fi
else
    echo "  FAIL: what_happened field not documented"
    exit 1
fi

# Test 3: Verify why_it_failed includes analysis of what broke
echo "Test 3: Checking for breakage analysis in why_it_failed..."
if grep -qi "why_it_failed" "$PHASE_FILE"; then
    echo "  PASS: why_it_failed generation instructions found"
else
    echo "  FAIL: why_it_failed generation instructions not found"
    exit 1
fi

# Test 4: Verify how_to_improve includes safer refactoring approach
echo "Test 4: Checking for safer refactoring approach in how_to_improve..."
if grep -qi "how_to_improve" "$PHASE_FILE"; then
    echo "  PASS: how_to_improve generation instructions found"
else
    echo "  FAIL: how_to_improve generation instructions not found"
    exit 1
fi

# Test 5: Verify REF-04-* ID pattern documented for Phase 04
echo "Test 5: Checking for 'REF-04-*' ID pattern..."
if grep -qE "REF-04-|REF-04" "$PHASE_FILE"; then
    echo "  PASS: REF-04 ID pattern found"
else
    echo "  FAIL: REF-04-{timestamp} ID pattern not found"
    exit 1
fi

# Test 6: Verify reflection is appended to phase-state.json
echo "Test 6: Checking for phase-state.json append pattern..."
if grep -q "phase-state.json" "$PHASE_FILE" && grep -qi "reflections\[\]" "$PHASE_FILE"; then
    echo "  PASS: phase-state.json append pattern found"
else
    echo "  FAIL: phase-state.json reflections[] append pattern not found"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
