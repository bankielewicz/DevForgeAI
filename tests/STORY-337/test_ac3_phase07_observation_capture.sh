#!/bin/bash
# Test: AC#3 - Phase 07 Observation Capture with DoD completion status observations
# Story: STORY-337
# Expected: FAIL (RED phase) - Observation Capture (EPIC-051) section does not exist yet

set -e

PHASE_FILE="src/claude/skills/devforgeai-development/phases/phase-07-dod-update.md"
TEST_NAME="AC3: Phase 07 Observation Capture"

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

# Test 2: Verify DoD completion status observation support
echo "Test 2: Checking for DoD completion status observation instructions..."
if grep -qi "DoD" "$PHASE_FILE" && grep -qi "completion" "$PHASE_FILE"; then
    echo "  PASS: DoD completion observation context found"
else
    echo "  FAIL: DoD completion status observation instructions missing"
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

# Test 5: Verify OBS-07 ID pattern
echo "Test 5: Checking for OBS-07-{timestamp} ID pattern..."
if grep -q "OBS-07" "$PHASE_FILE"; then
    echo "  PASS: OBS-07 ID pattern found"
else
    echo "  FAIL: OBS-07-{timestamp} ID pattern not found"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
