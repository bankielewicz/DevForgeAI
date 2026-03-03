#!/bin/bash
# Test: AC#3 - Phase 03 Reflection Capture on Implementation Failure
# Story: STORY-338
# Expected: FAIL (RED phase) - Reflection Capture section does not exist yet
#
# Acceptance Criteria:
# - tdd-green-phase.md contains reflection capture section
# - Implementation-specific what_happened with code reference
# - REF-03-* ID pattern documented

set -e

# Files to test - both src/ and operational copies
SRC_PHASE_FILE="src/claude/skills/devforgeai-development/references/tdd-green-phase.md"
OP_PHASE_FILE=".claude/skills/devforgeai-development/references/tdd-green-phase.md"

TEST_NAME="AC3: Phase 03 Reflection Capture"

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

# Test 2: Verify what_happened includes implementation/code reference
echo "Test 2: Checking for implementation-specific what_happened..."
if grep -qi "what_happened" "$PHASE_FILE"; then
    # Check for implementation-specific language (code, file, line, implementation)
    if grep -qiE "implementation|code|file|line|function|method" "$PHASE_FILE"; then
        echo "  PASS: Implementation-specific what_happened instructions found"
    else
        echo "  FAIL: what_happened lacks implementation-specific references (file/line/code)"
        exit 1
    fi
else
    echo "  FAIL: what_happened field not documented"
    exit 1
fi

# Test 3: Verify why_it_failed includes implementation gap analysis
echo "Test 3: Checking for implementation gap analysis in why_it_failed..."
if grep -qi "why_it_failed" "$PHASE_FILE"; then
    echo "  PASS: why_it_failed generation instructions found"
else
    echo "  FAIL: why_it_failed generation instructions not found"
    exit 1
fi

# Test 4: Verify how_to_improve includes specific code changes
echo "Test 4: Checking for code change suggestions in how_to_improve..."
if grep -qi "how_to_improve" "$PHASE_FILE"; then
    echo "  PASS: how_to_improve generation instructions found"
else
    echo "  FAIL: how_to_improve generation instructions not found"
    exit 1
fi

# Test 5: Verify REF-03-* ID pattern documented for Phase 03
echo "Test 5: Checking for 'REF-03-*' ID pattern..."
if grep -qE "REF-03-|REF-03" "$PHASE_FILE"; then
    echo "  PASS: REF-03 ID pattern found"
else
    echo "  FAIL: REF-03-{timestamp} ID pattern not found"
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
