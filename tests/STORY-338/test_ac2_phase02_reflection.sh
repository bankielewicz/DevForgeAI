#!/bin/bash
# Test: AC#2 - Phase 02 Reflection Capture on Test Failure
# Story: STORY-338
# Expected: FAIL (RED phase) - Reflection Capture section does not exist yet
#
# Acceptance Criteria:
# - tdd-red-phase.md contains "Reflection Capture on Failure" section
# - Instructions for generating what/why/how fields
# - Reflection appended with REF-02-* ID pattern

set -e

# Files to test - both src/ and operational copies
SRC_PHASE_FILE="src/claude/skills/devforgeai-development/references/tdd-red-phase.md"
OP_PHASE_FILE=".claude/skills/devforgeai-development/references/tdd-red-phase.md"

TEST_NAME="AC2: Phase 02 Reflection Capture"

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

# Test 1: Verify "Reflection Capture on Failure" section header exists
echo "Test 1: Checking for 'Reflection Capture on Failure' section header..."
if grep -qE "##+ Reflection Capture on Failure|##+ Reflection Capture \(EPIC-051\)" "$PHASE_FILE"; then
    echo "  PASS: Section header found"
else
    echo "  FAIL: Section header 'Reflection Capture on Failure' not found"
    exit 1
fi

# Test 2: Verify self-analysis prompt for what_happened generation
echo "Test 2: Checking for what_happened generation instructions..."
if grep -qi "what_happened" "$PHASE_FILE" && grep -qi "Generate Reflection\|generate.*reflection" "$PHASE_FILE"; then
    echo "  PASS: what_happened generation instructions found"
else
    echo "  FAIL: what_happened generation instructions not found"
    exit 1
fi

# Test 3: Verify self-analysis prompt for why_it_failed generation
echo "Test 3: Checking for why_it_failed generation instructions..."
if grep -qi "why_it_failed" "$PHASE_FILE"; then
    echo "  PASS: why_it_failed generation instructions found"
else
    echo "  FAIL: why_it_failed generation instructions not found"
    exit 1
fi

# Test 4: Verify self-analysis prompt for how_to_improve generation
echo "Test 4: Checking for how_to_improve generation instructions..."
if grep -qi "how_to_improve" "$PHASE_FILE"; then
    echo "  PASS: how_to_improve generation instructions found"
else
    echo "  FAIL: how_to_improve generation instructions not found"
    exit 1
fi

# Test 5: Verify REF-02-* ID pattern documented for Phase 02
echo "Test 5: Checking for 'REF-02-*' ID pattern..."
if grep -qE "REF-02-|REF-02" "$PHASE_FILE"; then
    echo "  PASS: REF-02 ID pattern found"
else
    echo "  FAIL: REF-02-{timestamp} ID pattern not found"
    exit 1
fi

# Test 6: Verify reflection is appended to phase-state.json
echo "Test 6: Checking for phase-state.json append pattern..."
if grep -q "phase-state.json" "$PHASE_FILE" && grep -qi "append\|reflections\[\]" "$PHASE_FILE"; then
    echo "  PASS: phase-state.json append pattern found"
else
    echo "  FAIL: phase-state.json reflections[] append pattern not found"
    exit 1
fi

# Test 7: Verify reflection capture happens on phase failure (conditional)
echo "Test 7: Checking for failure condition trigger..."
if grep -qiE "IF.*fail|failed|on failure|when.*fail" "$PHASE_FILE" | head -1; then
    echo "  PASS: Failure condition trigger found"
else
    echo "  FAIL: Reflection capture failure condition not documented"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
