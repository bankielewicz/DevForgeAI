#!/bin/bash
# Test AC#2: Observations Appended After Each Phase (02-08)
# Verifies phase files contain session memory append instructions
# Expected: FAIL (TDD Red phase - implementation not yet done)

set -e
# Check src/ (source of truth) first, fallback to .claude/ (operational)
PHASES_DIR="src/claude/skills/devforgeai-development/phases"
if [ ! -d "$PHASES_DIR" ]; then
    PHASES_DIR=".claude/skills/devforgeai-development/phases"
fi

echo "AC#2: Verifying observation append instructions in phases 02-08..."

# Test for each phase file (02-08)
PHASE_FILES=(
    "phase-02-test-first.md"
    "phase-03-implementation.md"
    "phase-04-refactoring.md"
    "phase-05-integration.md"
    "phase-06-deferral.md"
    "phase-07-dod-update.md"
    "phase-08-git-workflow.md"
)

MISSING_COUNT=0

for PHASE_FILE in "${PHASE_FILES[@]}"; do
    TARGET_FILE="$PHASES_DIR/$PHASE_FILE"

    if [ ! -f "$TARGET_FILE" ]; then
        echo "WARN: Phase file not found: $PHASE_FILE"
        continue
    fi

    # Test 1: Session Memory Update section exists
    if ! grep -q 'Session Memory' "$TARGET_FILE"; then
        echo "FAIL: Missing 'Session Memory' section in $PHASE_FILE"
        MISSING_COUNT=$((MISSING_COUNT + 1))
        continue
    fi

    # Test 2: Edit() or Append instruction for session memory
    if ! grep -qE '(Edit|append|Append).*session' "$TARGET_FILE"; then
        echo "FAIL: Missing append instruction for session memory in $PHASE_FILE"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done

if [ $MISSING_COUNT -gt 0 ]; then
    echo "FAIL: $MISSING_COUNT phase files missing session memory append instructions"
    exit 1
fi

echo "PASS: AC#2 Observations appended after each phase"
