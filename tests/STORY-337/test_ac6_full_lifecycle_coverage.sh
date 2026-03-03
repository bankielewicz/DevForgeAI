#!/bin/bash
# Test: AC#6 - Full lifecycle coverage - all 7 phases (02-08) have observation capture
# Story: STORY-337
# Expected: FAIL (RED phase) - Phases 05-08 don't have EPIC-051 sections yet

set -e

PHASES_DIR="src/claude/skills/devforgeai-development/phases"
TEST_NAME="AC6: Full Lifecycle Coverage"

echo "=== $TEST_NAME ==="

# All phases that should have Observation Capture (EPIC-051) sections
# Per STORY-336: phases 02-04 were completed
# Per STORY-337: phases 05-08 need to be added
ALL_PHASES=("phase-02-test-first.md" "phase-03-implementation.md" "phase-04-refactoring.md" "phase-05-integration.md" "phase-06-deferral.md" "phase-07-dod-update.md" "phase-08-git-workflow.md")

# Test 1: Verify all 7 phases (02-08) have EPIC-051 header
echo "Test 1: Checking all 7 phases (02-08) have Observation Capture (EPIC-051) section..."
MISSING_COUNT=0
MISSING_PHASES=""
for PHASE in "${ALL_PHASES[@]}"; do
    PHASE_FILE="$PHASES_DIR/$PHASE"
    if ! grep -q "### Observation Capture (EPIC-051)" "$PHASE_FILE"; then
        MISSING_COUNT=$((MISSING_COUNT + 1))
        MISSING_PHASES="$MISSING_PHASES $PHASE"
    fi
done

if [ $MISSING_COUNT -gt 0 ]; then
    echo "  FAIL: $MISSING_COUNT phases missing Observation Capture (EPIC-051) section:$MISSING_PHASES"
    exit 1
fi
echo "  PASS: All 7 phases have Observation Capture (EPIC-051) section"

# Test 2: Verify all 7 phases have observation-extractor invocation
echo "Test 2: Checking all 7 phases have observation-extractor invocation..."
MISSING_COUNT=0
MISSING_PHASES=""
for PHASE in "${ALL_PHASES[@]}"; do
    PHASE_FILE="$PHASES_DIR/$PHASE"
    if ! grep -q 'subagent_type="observation-extractor"' "$PHASE_FILE" && \
       ! grep -q 'Task.*observation-extractor' "$PHASE_FILE"; then
        MISSING_COUNT=$((MISSING_COUNT + 1))
        MISSING_PHASES="$MISSING_PHASES $PHASE"
    fi
done

if [ $MISSING_COUNT -gt 0 ]; then
    echo "  FAIL: $MISSING_COUNT phases missing observation-extractor invocation:$MISSING_PHASES"
    exit 1
fi
echo "  PASS: All 7 phases have observation-extractor invocation"

# Test 3: Count total phases with EPIC-051 section (should be exactly 7)
echo "Test 3: Verifying exactly 7 phases have EPIC-051 sections..."
EPIC_051_COUNT=0
for PHASE in "${ALL_PHASES[@]}"; do
    PHASE_FILE="$PHASES_DIR/$PHASE"
    if grep -q "### Observation Capture (EPIC-051)" "$PHASE_FILE"; then
        EPIC_051_COUNT=$((EPIC_051_COUNT + 1))
    fi
done

if [ $EPIC_051_COUNT -ne 7 ]; then
    echo "  FAIL: Expected 7 phases with EPIC-051 section, found $EPIC_051_COUNT"
    exit 1
fi
echo "  PASS: Exactly 7 phases have EPIC-051 sections"

# Test 4: Verify sequential OBS ID patterns (OBS-02 through OBS-08)
echo "Test 4: Checking sequential OBS ID patterns from 02 to 08..."
PHASE_NUMS=("02" "03" "04" "05" "06" "07" "08")
for i in "${!ALL_PHASES[@]}"; do
    PHASE="${ALL_PHASES[$i]}"
    PHASE_NUM="${PHASE_NUMS[$i]}"
    PHASE_FILE="$PHASES_DIR/$PHASE"
    if ! grep -q "OBS-$PHASE_NUM" "$PHASE_FILE"; then
        echo "  FAIL: $PHASE missing 'OBS-$PHASE_NUM' ID pattern"
        exit 1
    fi
done
echo "  PASS: All phases have correct sequential OBS-NN ID patterns"

echo "=== All $TEST_NAME tests passed ==="
echo ""
echo "Summary: Full lifecycle coverage verified (phases 02-08)"
exit 0
