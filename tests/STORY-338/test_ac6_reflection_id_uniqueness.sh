#!/bin/bash
# Test: AC#6 - Reflection IDs Are Unique
# Story: STORY-338
# Expected: FAIL (RED phase) - ID uniqueness pattern not documented yet
#
# Acceptance Criteria:
# - IDs follow REF-{phase}-{timestamp} pattern (ISO8601 milliseconds)
# - No duplicate IDs even for rapid failures

set -e

# Files to test - both src/ and operational copies
SRC_RED_PHASE="src/claude/skills/devforgeai-development/references/tdd-red-phase.md"
SRC_GREEN_PHASE="src/claude/skills/devforgeai-development/references/tdd-green-phase.md"
SRC_REFACTOR_PHASE="src/claude/skills/devforgeai-development/references/tdd-refactor-phase.md"
OP_RED_PHASE=".claude/skills/devforgeai-development/references/tdd-red-phase.md"
OP_GREEN_PHASE=".claude/skills/devforgeai-development/references/tdd-green-phase.md"
OP_REFACTOR_PHASE=".claude/skills/devforgeai-development/references/tdd-refactor-phase.md"

TEST_NAME="AC6: Reflection ID Uniqueness"

echo "=== $TEST_NAME ==="

# Test 1: Verify REF-{phase}-{timestamp} pattern is documented
echo "Test 1: Checking for 'REF-{phase}-{timestamp}' pattern documentation..."
FOUND_PATTERN=0

for FILE in "$SRC_RED_PHASE" "$SRC_GREEN_PHASE" "$SRC_REFACTOR_PHASE" \
            "$OP_RED_PHASE" "$OP_GREEN_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ] && grep -qE "REF-\{phase\}-\{timestamp\}|REF-0[234]-\{timestamp\}|REF-0[234]-[0-9]+" "$FILE"; then
        FOUND_PATTERN=1
        echo "  Found pattern in: $FILE"
        break
    fi
done

if [ "$FOUND_PATTERN" -eq 1 ]; then
    echo "  PASS: REF-{phase}-{timestamp} pattern documented"
else
    echo "  FAIL: REF-{phase}-{timestamp} pattern not documented"
    exit 1
fi

# Test 2: Verify timestamp uses ISO8601 format or milliseconds
echo "Test 2: Checking for ISO8601/millisecond timestamp documentation..."
FOUND_ISO8601=0

for FILE in "$SRC_RED_PHASE" "$SRC_GREEN_PHASE" "$SRC_REFACTOR_PHASE" \
            "$OP_RED_PHASE" "$OP_GREEN_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ] && grep -qiE "ISO8601|millisecond|timestamp.*unique|unique.*timestamp" "$FILE"; then
        FOUND_ISO8601=1
        echo "  Found timestamp format in: $FILE"
        break
    fi
done

if [ "$FOUND_ISO8601" -eq 1 ]; then
    echo "  PASS: ISO8601/millisecond timestamp format documented"
else
    echo "  FAIL: Timestamp format (ISO8601 milliseconds) not documented"
    exit 1
fi

# Test 3: Verify uniqueness guarantee is mentioned
echo "Test 3: Checking for ID uniqueness guarantee..."
FOUND_UNIQUENESS=0

for FILE in "$SRC_RED_PHASE" "$SRC_GREEN_PHASE" "$SRC_REFACTOR_PHASE" \
            "$OP_RED_PHASE" "$OP_GREEN_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ] && grep -qiE "unique.*ID|ID.*unique|no duplicate|avoid.*collision" "$FILE"; then
        FOUND_UNIQUENESS=1
        echo "  Found uniqueness guarantee in: $FILE"
        break
    fi
done

if [ "$FOUND_UNIQUENESS" -eq 1 ]; then
    echo "  PASS: ID uniqueness guarantee documented"
else
    echo "  FAIL: ID uniqueness guarantee not documented"
    exit 1
fi

# Test 4: Verify phase-specific ID prefixes (REF-02, REF-03, REF-04)
echo "Test 4: Checking for phase-specific ID prefixes..."
FOUND_02=0
FOUND_03=0
FOUND_04=0

for FILE in "$SRC_RED_PHASE" "$OP_RED_PHASE"; do
    if [ -f "$FILE" ] && grep -qE "REF-02" "$FILE"; then
        FOUND_02=1
    fi
done

for FILE in "$SRC_GREEN_PHASE" "$OP_GREEN_PHASE"; do
    if [ -f "$FILE" ] && grep -qE "REF-03" "$FILE"; then
        FOUND_03=1
    fi
done

for FILE in "$SRC_REFACTOR_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ] && grep -qE "REF-04" "$FILE"; then
        FOUND_04=1
    fi
done

if [ "$FOUND_02" -eq 1 ] && [ "$FOUND_03" -eq 1 ] && [ "$FOUND_04" -eq 1 ]; then
    echo "  PASS: Phase-specific ID prefixes (REF-02, REF-03, REF-04) documented"
else
    echo "  FAIL: Missing phase-specific ID prefixes:"
    [ "$FOUND_02" -eq 0 ] && echo "    - REF-02 not found in tdd-red-phase.md"
    [ "$FOUND_03" -eq 0 ] && echo "    - REF-03 not found in tdd-green-phase.md"
    [ "$FOUND_04" -eq 0 ] && echo "    - REF-04 not found in tdd-refactor-phase.md"
    exit 1
fi

# Test 5: Verify rapid failure handling (multiple quick failures)
echo "Test 5: Checking for rapid failure handling documentation..."
FOUND_RAPID=0

for FILE in "$SRC_RED_PHASE" "$SRC_GREEN_PHASE" "$SRC_REFACTOR_PHASE" \
            "$OP_RED_PHASE" "$OP_GREEN_PHASE" "$OP_REFACTOR_PHASE"; do
    if [ -f "$FILE" ] && grep -qiE "rapid|consecutive|quick.*failure|millisecond precision|no.*collision" "$FILE"; then
        FOUND_RAPID=1
        echo "  Found rapid failure handling in: $FILE"
        break
    fi
done

if [ "$FOUND_RAPID" -eq 1 ]; then
    echo "  PASS: Rapid failure handling documented (millisecond precision)"
else
    echo "  FAIL: No documentation for handling rapid/consecutive failures"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
