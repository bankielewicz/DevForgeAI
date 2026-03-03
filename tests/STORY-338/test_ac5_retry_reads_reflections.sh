#!/bin/bash
# Test: AC#5 - Retry Reads Previous Reflections for Context
# Story: STORY-338
# Expected: FAIL (RED phase) - Retry reflection read workflow does not exist yet
#
# Acceptance Criteria:
# - Phase retry workflow reads previous reflections from phase-state.json
# - Presents how_to_improve guidance before retry
# - Applies to all TDD phases (02, 03, 04)

set -e

# Files to test - both src/ and operational copies
SRC_RED_PHASE="src/claude/skills/devforgeai-development/references/tdd-red-phase.md"
SRC_GREEN_PHASE="src/claude/skills/devforgeai-development/references/tdd-green-phase.md"
SRC_REFACTOR_PHASE="src/claude/skills/devforgeai-development/references/tdd-refactor-phase.md"
OP_RED_PHASE=".claude/skills/devforgeai-development/references/tdd-red-phase.md"
OP_GREEN_PHASE=".claude/skills/devforgeai-development/references/tdd-green-phase.md"
OP_REFACTOR_PHASE=".claude/skills/devforgeai-development/references/tdd-refactor-phase.md"

TEST_NAME="AC5: Retry Reads Previous Reflections"

echo "=== $TEST_NAME ==="

# Helper function to check retry reflection read
check_retry_read() {
    local FILE=$1
    local PHASE_NUM=$2

    # Check for retry + reflection read pattern
    if grep -qiE "retry|re-run|resume" "$FILE" && \
       grep -qi "read.*reflection\|reflection.*read\|previous.*reflection" "$FILE"; then
        return 0
    fi
    return 1
}

# Helper function to check how_to_improve presentation
check_how_to_improve_guidance() {
    local FILE=$1

    # Check for how_to_improve being presented/displayed before retry
    if grep -qi "how_to_improve" "$FILE" && \
       grep -qiE "present|display|show|guide" "$FILE"; then
        return 0
    fi
    return 1
}

# Test 1: Verify Phase 02 (tdd-red-phase.md) reads previous reflections on retry
echo "Test 1: Checking Phase 02 reads previous reflections on retry..."
RED_FILE=""
if [ -f "$OP_RED_PHASE" ]; then
    RED_FILE="$OP_RED_PHASE"
elif [ -f "$SRC_RED_PHASE" ]; then
    RED_FILE="$SRC_RED_PHASE"
fi

if [ -n "$RED_FILE" ] && check_retry_read "$RED_FILE" "02"; then
    echo "  PASS: Phase 02 retry reads previous reflections"
else
    echo "  FAIL: Phase 02 (tdd-red-phase.md) does not read previous reflections on retry"
    exit 1
fi

# Test 2: Verify Phase 03 (tdd-green-phase.md) reads previous reflections on retry
echo "Test 2: Checking Phase 03 reads previous reflections on retry..."
GREEN_FILE=""
if [ -f "$OP_GREEN_PHASE" ]; then
    GREEN_FILE="$OP_GREEN_PHASE"
elif [ -f "$SRC_GREEN_PHASE" ]; then
    GREEN_FILE="$SRC_GREEN_PHASE"
fi

if [ -n "$GREEN_FILE" ] && check_retry_read "$GREEN_FILE" "03"; then
    echo "  PASS: Phase 03 retry reads previous reflections"
else
    echo "  FAIL: Phase 03 (tdd-green-phase.md) does not read previous reflections on retry"
    exit 1
fi

# Test 3: Verify Phase 04 (tdd-refactor-phase.md) reads previous reflections on retry
echo "Test 3: Checking Phase 04 reads previous reflections on retry..."
REFACTOR_FILE=""
if [ -f "$OP_REFACTOR_PHASE" ]; then
    REFACTOR_FILE="$OP_REFACTOR_PHASE"
elif [ -f "$SRC_REFACTOR_PHASE" ]; then
    REFACTOR_FILE="$SRC_REFACTOR_PHASE"
fi

if [ -n "$REFACTOR_FILE" ] && check_retry_read "$REFACTOR_FILE" "04"; then
    echo "  PASS: Phase 04 retry reads previous reflections"
else
    echo "  FAIL: Phase 04 (tdd-refactor-phase.md) does not read previous reflections on retry"
    exit 1
fi

# Test 4: Verify how_to_improve guidance is presented before retry in at least one phase
echo "Test 4: Checking how_to_improve guidance is presented before retry..."
FOUND_GUIDANCE=0

for FILE in "$RED_FILE" "$GREEN_FILE" "$REFACTOR_FILE"; do
    if [ -n "$FILE" ] && check_how_to_improve_guidance "$FILE"; then
        FOUND_GUIDANCE=1
        echo "  Found guidance presentation in: $FILE"
        break
    fi
done

if [ "$FOUND_GUIDANCE" -eq 1 ]; then
    echo "  PASS: how_to_improve guidance presented before retry"
else
    echo "  FAIL: how_to_improve guidance not presented before retry"
    exit 1
fi

# Test 5: Verify reflection context informs retry approach
echo "Test 5: Checking reflection context used to inform retry..."
FOUND_CONTEXT_USE=0

for FILE in "$RED_FILE" "$GREEN_FILE" "$REFACTOR_FILE"; do
    if [ -n "$FILE" ] && grep -qiE "avoid.*same|avoid.*pattern|learn.*from|context.*retry|inform.*retry" "$FILE"; then
        FOUND_CONTEXT_USE=1
        echo "  Found context usage in: $FILE"
        break
    fi
done

if [ "$FOUND_CONTEXT_USE" -eq 1 ]; then
    echo "  PASS: Reflection context informs retry approach"
else
    echo "  FAIL: No indication that reflection context is used to avoid same failure"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
