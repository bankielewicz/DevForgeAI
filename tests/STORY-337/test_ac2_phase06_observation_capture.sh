#!/bin/bash
# Test: AC#2 - Phase 06 Observation Capture with deferral gap category observations
# Story: STORY-337
# Expected: FAIL (RED phase) - Observation Capture (EPIC-051) section does not exist yet

set -e

PHASE_FILE="src/claude/skills/devforgeai-development/phases/phase-06-deferral.md"
TEST_NAME="AC2: Phase 06 Observation Capture"

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

# Test 2: Verify deferral-validator observation collection
echo "Test 2: Checking for deferral-validator observation handling..."
if grep -i "deferral-validator" "$PHASE_FILE" | grep -qi "observation"; then
    echo "  PASS: deferral-validator observation handling found"
else
    echo "  FAIL: deferral-validator observation handling not found in section"
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

# Test 4: Verify phase-state.json append pattern
echo "Test 4: Checking for phase-state.json append pattern..."
if grep -q "phase-state.json" "$PHASE_FILE" && \
   grep -q "observations\[\]" "$PHASE_FILE"; then
    echo "  PASS: Phase-state.json append pattern found"
else
    echo "  FAIL: Phase-state.json observations[] append pattern missing"
    exit 1
fi

# Test 5: Verify OBS-06 ID pattern
echo "Test 5: Checking for OBS-06-{timestamp} ID pattern..."
if grep -q "OBS-06" "$PHASE_FILE"; then
    echo "  PASS: OBS-06 ID pattern found"
else
    echo "  FAIL: OBS-06-{timestamp} ID pattern not found"
    exit 1
fi

# Test 6: Verify gap category support in deferral context
echo "Test 6: Checking for deferral gap category observations support..."
if grep -qi "gap" "$PHASE_FILE" && grep -qi "deferral" "$PHASE_FILE"; then
    echo "  PASS: Deferral gap category context found"
else
    echo "  FAIL: Deferral gap category observations support missing"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
