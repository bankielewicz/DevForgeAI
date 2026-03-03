#!/bin/bash
# Test: AC#3 - Phase 04 Observation Capture at Exit Gate
# Story: STORY-336
# Expected: FAIL (RED phase) - Observation Capture (EPIC-051) section does not exist yet

set -e

PHASE_FILE=".claude/skills/devforgeai-development/phases/phase-04-refactoring.md"
TEST_NAME="AC3: Phase 04 Observation Capture"

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

# Test 2: Verify section is BEFORE exit gate
echo "Test 2: Checking section placement before Exit Gate..."
# Get line numbers for both sections
OBS_LINE=$(grep -n "Observation Capture (EPIC-051)" "$PHASE_FILE" | head -1 | cut -d: -f1)
EXIT_LINE=$(grep -n "Exit Gate" "$PHASE_FILE" | head -1 | cut -d: -f1)

if [ -n "$OBS_LINE" ] && [ -n "$EXIT_LINE" ] && [ "$OBS_LINE" -lt "$EXIT_LINE" ]; then
    echo "  PASS: Observation Capture (line $OBS_LINE) before Exit Gate (line $EXIT_LINE)"
else
    echo "  FAIL: Observation Capture section must appear BEFORE Exit Gate"
    exit 1
fi

# Test 3: Verify observation-extractor invocation
echo "Test 3: Checking for observation-extractor Task() invocation..."
if grep -q 'Task.*subagent_type.*observation-extractor' "$PHASE_FILE" || \
   grep -q 'subagent_type="observation-extractor"' "$PHASE_FILE"; then
    echo "  PASS: observation-extractor invocation found"
else
    echo "  FAIL: observation-extractor Task() invocation not found"
    exit 1
fi

# Test 4: Verify OBS-04 ID pattern
echo "Test 4: Checking for OBS-04-{timestamp} ID pattern..."
if grep -q "OBS-04" "$PHASE_FILE"; then
    echo "  PASS: OBS-04 ID pattern found"
else
    echo "  FAIL: OBS-04-{timestamp} ID pattern not found"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
