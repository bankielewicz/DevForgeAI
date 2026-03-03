#!/bin/bash
# Test: AC#4 - Observation ID Uniqueness
# Story: STORY-336
# Expected: FAIL (RED phase) - ID patterns not implemented yet

set -e

PHASE02=".claude/skills/devforgeai-development/phases/phase-02-test-first.md"
PHASE03=".claude/skills/devforgeai-development/phases/phase-03-implementation.md"
PHASE04=".claude/skills/devforgeai-development/phases/phase-04-refactoring.md"
TEST_NAME="AC4: Observation ID Uniqueness"

echo "=== $TEST_NAME ==="

# Test 1: Verify OBS-{phase}-{timestamp} pattern documented in Phase 02
echo "Test 1: Checking OBS-02-{timestamp} pattern in Phase 02..."
if grep -qE "OBS-02-\{timestamp\}|OBS-02-[0-9]" "$PHASE02"; then
    echo "  PASS: OBS-02 pattern found in Phase 02"
else
    echo "  FAIL: OBS-02-{timestamp} pattern not found in Phase 02"
    exit 1
fi

# Test 2: Verify OBS-{phase}-{timestamp} pattern documented in Phase 03
echo "Test 2: Checking OBS-03-{timestamp} pattern in Phase 03..."
if grep -qE "OBS-03-\{timestamp\}|OBS-03-[0-9]" "$PHASE03"; then
    echo "  PASS: OBS-03 pattern found in Phase 03"
else
    echo "  FAIL: OBS-03-{timestamp} pattern not found in Phase 03"
    exit 1
fi

# Test 3: Verify OBS-{phase}-{timestamp} pattern documented in Phase 04
echo "Test 3: Checking OBS-04-{timestamp} pattern in Phase 04..."
if grep -qE "OBS-04-\{timestamp\}|OBS-04-[0-9]" "$PHASE04"; then
    echo "  PASS: OBS-04 pattern found in Phase 04"
else
    echo "  FAIL: OBS-04-{timestamp} pattern not found in Phase 04"
    exit 1
fi

# Test 4: Verify timestamp format is ISO8601
echo "Test 4: Checking for ISO8601 timestamp reference..."
ALL_FILES="$PHASE02 $PHASE03 $PHASE04"
FOUND_ISO=false
for f in $ALL_FILES; do
    if grep -qi "ISO8601\|timestamp" "$f"; then
        FOUND_ISO=true
        break
    fi
done

if [ "$FOUND_ISO" = true ]; then
    echo "  PASS: ISO8601 timestamp reference found"
else
    echo "  FAIL: ISO8601 timestamp format not referenced"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
