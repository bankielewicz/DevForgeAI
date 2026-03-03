#!/bin/bash
# Test: AC#1 - Reflection Schema in Phase State
# Story: STORY-338
# Expected: FAIL (RED phase) - reflections[] schema not documented yet
#
# Acceptance Criteria:
# - phase-state.json schema includes reflections[] array
# - Each reflection object has: id (REF-{phase}-{timestamp}), phase (string),
#   failed (boolean), iteration (number), reflection object with what_happened,
#   why_it_failed, and how_to_improve fields, and timestamp (ISO8601)

set -e

# Files to test - checking both src/ and operational copies
SRC_RED_PHASE="src/claude/skills/devforgeai-development/references/tdd-red-phase.md"
SRC_GREEN_PHASE="src/claude/skills/devforgeai-development/references/tdd-green-phase.md"
SRC_REFACTOR_PHASE="src/claude/skills/devforgeai-development/references/tdd-refactor-phase.md"
OP_RED_PHASE=".claude/skills/devforgeai-development/references/tdd-red-phase.md"
OP_GREEN_PHASE=".claude/skills/devforgeai-development/references/tdd-green-phase.md"
OP_REFACTOR_PHASE=".claude/skills/devforgeai-development/references/tdd-refactor-phase.md"

TEST_NAME="AC1: Reflection Schema in Phase State"

echo "=== $TEST_NAME ==="

# Test 1: Verify reflections[] array is documented in at least one TDD phase file
echo "Test 1: Checking for 'reflections[]' schema documentation..."
FOUND_REFLECTIONS=0

for FILE in "$SRC_RED_PHASE" "$SRC_GREEN_PHASE" "$SRC_REFACTOR_PHASE" \
            "$OP_RED_PHASE" "$OP_GREEN_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ] && grep -q "reflections\[\]" "$FILE"; then
        FOUND_REFLECTIONS=1
        echo "  Found reflections[] in: $FILE"
        break
    fi
done

if [ "$FOUND_REFLECTIONS" -eq 1 ]; then
    echo "  PASS: reflections[] schema documented"
else
    echo "  FAIL: reflections[] array schema not documented in any TDD phase file"
    exit 1
fi

# Test 2: Verify reflection ID format REF-{phase}-{timestamp} is documented
echo "Test 2: Checking for 'REF-{phase}-{timestamp}' ID pattern..."
FOUND_REF_ID=0

for FILE in "$SRC_RED_PHASE" "$SRC_GREEN_PHASE" "$SRC_REFACTOR_PHASE" \
            "$OP_RED_PHASE" "$OP_GREEN_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ] && grep -qE "REF-\{phase\}-\{timestamp\}|REF-0[234]-" "$FILE"; then
        FOUND_REF_ID=1
        echo "  Found REF ID pattern in: $FILE"
        break
    fi
done

if [ "$FOUND_REF_ID" -eq 1 ]; then
    echo "  PASS: REF-{phase}-{timestamp} ID pattern documented"
else
    echo "  FAIL: REF-{phase}-{timestamp} ID pattern not documented"
    exit 1
fi

# Test 3: Verify 'failed' boolean field is documented
echo "Test 3: Checking for 'failed' boolean field in reflection schema..."
FOUND_FAILED=0

for FILE in "$SRC_RED_PHASE" "$SRC_GREEN_PHASE" "$SRC_REFACTOR_PHASE" \
            "$OP_RED_PHASE" "$OP_GREEN_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ] && grep -qi "\"failed\":" "$FILE"; then
        FOUND_FAILED=1
        echo "  Found 'failed' field in: $FILE"
        break
    fi
done

if [ "$FOUND_FAILED" -eq 1 ]; then
    echo "  PASS: 'failed' boolean field documented"
else
    echo "  FAIL: 'failed' boolean field not documented in reflection schema"
    exit 1
fi

# Test 4: Verify 'iteration' number field is documented
echo "Test 4: Checking for 'iteration' number field in reflection schema..."
FOUND_ITERATION=0

for FILE in "$SRC_RED_PHASE" "$SRC_GREEN_PHASE" "$SRC_REFACTOR_PHASE" \
            "$OP_RED_PHASE" "$OP_GREEN_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ] && grep -qi "\"iteration\":" "$FILE"; then
        FOUND_ITERATION=1
        echo "  Found 'iteration' field in: $FILE"
        break
    fi
done

if [ "$FOUND_ITERATION" -eq 1 ]; then
    echo "  PASS: 'iteration' number field documented"
else
    echo "  FAIL: 'iteration' number field not documented in reflection schema"
    exit 1
fi

# Test 5: Verify reflection object has what_happened, why_it_failed, how_to_improve
echo "Test 5: Checking for reflection content fields (what/why/how)..."
FOUND_WHAT=0
FOUND_WHY=0
FOUND_HOW=0

for FILE in "$SRC_RED_PHASE" "$SRC_GREEN_PHASE" "$SRC_REFACTOR_PHASE" \
            "$OP_RED_PHASE" "$OP_GREEN_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ]; then
        if grep -qi "what_happened" "$FILE"; then
            FOUND_WHAT=1
        fi
        if grep -qi "why_it_failed" "$FILE"; then
            FOUND_WHY=1
        fi
        if grep -qi "how_to_improve" "$FILE"; then
            FOUND_HOW=1
        fi
    fi
done

if [ "$FOUND_WHAT" -eq 1 ] && [ "$FOUND_WHY" -eq 1 ] && [ "$FOUND_HOW" -eq 1 ]; then
    echo "  PASS: what_happened, why_it_failed, how_to_improve fields documented"
else
    echo "  FAIL: Missing reflection content fields:"
    [ "$FOUND_WHAT" -eq 0 ] && echo "    - what_happened not found"
    [ "$FOUND_WHY" -eq 0 ] && echo "    - why_it_failed not found"
    [ "$FOUND_HOW" -eq 0 ] && echo "    - how_to_improve not found"
    exit 1
fi

# Test 6: Verify timestamp field is documented (ISO8601)
echo "Test 6: Checking for 'timestamp' field with ISO8601 format..."
FOUND_TIMESTAMP=0

for FILE in "$SRC_RED_PHASE" "$SRC_GREEN_PHASE" "$SRC_REFACTOR_PHASE" \
            "$OP_RED_PHASE" "$OP_GREEN_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ] && grep -qi "\"timestamp\":" "$FILE"; then
        FOUND_TIMESTAMP=1
        echo "  Found 'timestamp' field in: $FILE"
        break
    fi
done

if [ "$FOUND_TIMESTAMP" -eq 1 ]; then
    echo "  PASS: 'timestamp' field documented"
else
    echo "  FAIL: 'timestamp' field (ISO8601) not documented in reflection schema"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
