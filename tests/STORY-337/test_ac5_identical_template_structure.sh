#!/bin/bash
# Test: AC#5 - All 4 phases use identical template structure from STORY-336 pattern
# Story: STORY-337
# Expected: FAIL (RED phase) - Observation Capture (EPIC-051) sections do not exist yet

set -e

PHASES_DIR="src/claude/skills/devforgeai-development/phases"
TEST_NAME="AC5: Identical Template Structure"

echo "=== $TEST_NAME ==="

# Define the phases to check
PHASES=("phase-05-integration.md" "phase-06-deferral.md" "phase-07-dod-update.md" "phase-08-git-workflow.md")
PHASE_NUMS=("05" "06" "07" "08")

# Test 1: All phases must have "Observation Capture (EPIC-051)" header
echo "Test 1: Checking all phases have EPIC-051 header..."
for PHASE in "${PHASES[@]}"; do
    PHASE_FILE="$PHASES_DIR/$PHASE"
    if ! grep -q "### Observation Capture (EPIC-051)" "$PHASE_FILE"; then
        echo "  FAIL: $PHASE missing '### Observation Capture (EPIC-051)' header"
        exit 1
    fi
done
echo "  PASS: All phases have EPIC-051 header"

# Test 2: All phases must have "Collect Explicit Observations" step
echo "Test 2: Checking all phases have explicit observation collection..."
for PHASE in "${PHASES[@]}"; do
    PHASE_FILE="$PHASES_DIR/$PHASE"
    if ! grep -q "Collect Explicit Observations" "$PHASE_FILE"; then
        echo "  FAIL: $PHASE missing 'Collect Explicit Observations' step"
        exit 1
    fi
done
echo "  PASS: All phases have explicit observation collection"

# Test 3: All phases must have "Invoke Observation Extractor" step
echo "Test 3: Checking all phases have observation extractor invocation..."
for PHASE in "${PHASES[@]}"; do
    PHASE_FILE="$PHASES_DIR/$PHASE"
    if ! grep -q "Invoke Observation Extractor" "$PHASE_FILE"; then
        echo "  FAIL: $PHASE missing 'Invoke Observation Extractor' step"
        exit 1
    fi
done
echo "  PASS: All phases have observation extractor invocation"

# Test 4: All phases must have "Append to Phase State" step
echo "Test 4: Checking all phases have phase state append step..."
for PHASE in "${PHASES[@]}"; do
    PHASE_FILE="$PHASES_DIR/$PHASE"
    if ! grep -q "Append to Phase State" "$PHASE_FILE"; then
        echo "  FAIL: $PHASE missing 'Append to Phase State' step"
        exit 1
    fi
done
echo "  PASS: All phases have phase state append step"

# Test 5: All phases must have correct OBS-NN ID pattern
echo "Test 5: Checking all phases have correct OBS-NN ID pattern..."
for i in "${!PHASES[@]}"; do
    PHASE="${PHASES[$i]}"
    PHASE_NUM="${PHASE_NUMS[$i]}"
    PHASE_FILE="$PHASES_DIR/$PHASE"
    if ! grep -q "OBS-$PHASE_NUM" "$PHASE_FILE"; then
        echo "  FAIL: $PHASE missing 'OBS-$PHASE_NUM' ID pattern"
        exit 1
    fi
done
echo "  PASS: All phases have correct OBS-NN ID pattern"

# Test 6: All phases must have Error Handling section for non-blocking
echo "Test 6: Checking all phases have error handling for non-blocking capture..."
for PHASE in "${PHASES[@]}"; do
    PHASE_FILE="$PHASES_DIR/$PHASE"
    if ! grep -q "Error Handling" "$PHASE_FILE" || ! grep -q "non-blocking" "$PHASE_FILE"; then
        echo "  FAIL: $PHASE missing error handling for non-blocking observation capture"
        exit 1
    fi
done
echo "  PASS: All phases have non-blocking error handling"

echo "=== All $TEST_NAME tests passed ==="
exit 0
