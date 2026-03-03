#!/bin/bash
# Test: AC#2 - Phase 03 Observation Capture at Exit Gate
# Story: STORY-336
# Expected: FAIL (RED phase) - Observation Capture (EPIC-051) section does not exist yet

set -e

PHASE_FILE=".claude/skills/devforgeai-development/phases/phase-03-implementation.md"
TEST_NAME="AC2: Phase 03 Observation Capture"

echo "=== $TEST_NAME ==="

# Test 1: Verify "Observation Capture (EPIC-051)" section header exists
echo "Test 1: Checking for 'Observation Capture (EPIC-051)' section header..."
if grep -q "## Observation Capture (EPIC-051)" "$PHASE_FILE" || \
   grep -q "### Observation Capture (EPIC-051)" "$PHASE_FILE"; then
    echo "  PASS: Section header found"
else
    echo "  FAIL: Section header 'Observation Capture (EPIC-051)' not found"
    exit 1
fi

# Test 2: Verify backend-architect subagent handling
echo "Test 2: Checking for backend-architect observation collection..."
if grep -i "backend-architect" "$PHASE_FILE" | grep -qi "observation"; then
    echo "  PASS: backend-architect observation handling found"
else
    echo "  FAIL: backend-architect observation handling not found in section"
    exit 1
fi

# Test 3: Verify code-reviewer subagent handling
echo "Test 3: Checking for code-reviewer observation collection..."
if grep -i "code-reviewer" "$PHASE_FILE" | grep -qi "observation"; then
    echo "  PASS: code-reviewer observation handling found"
else
    echo "  FAIL: code-reviewer observation handling not found in section"
    exit 1
fi

# Test 4: Verify observation-extractor invocation
echo "Test 4: Checking for observation-extractor Task() invocation..."
if grep -q 'Task.*subagent_type.*observation-extractor' "$PHASE_FILE" || \
   grep -q 'subagent_type="observation-extractor"' "$PHASE_FILE"; then
    echo "  PASS: observation-extractor invocation found"
else
    echo "  FAIL: observation-extractor Task() invocation not found"
    exit 1
fi

# Test 5: Verify OBS-03 ID pattern
echo "Test 5: Checking for OBS-03-{timestamp} ID pattern..."
if grep -q "OBS-03" "$PHASE_FILE"; then
    echo "  PASS: OBS-03 ID pattern found"
else
    echo "  FAIL: OBS-03-{timestamp} ID pattern not found"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
