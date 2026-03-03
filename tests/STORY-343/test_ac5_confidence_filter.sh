#!/bin/bash
# STORY-343 AC#5: Only Confident Patterns Surfaced
# TDD Red Phase - This test MUST FAIL until implementation complete

PHASE02_FILE=".claude/skills/devforgeai-development/phases/phase-02-test-first.md"
PHASE03_FILE=".claude/skills/devforgeai-development/phases/phase-03-implementation.md"
EXIT_CODE=0

echo "=== AC#5: Only Confident Patterns Surfaced ==="

# Test 1: Confidence check in Phase 02
if grep -qE '(confidence.*>=.*low|confidence.*!=.*emerging|3\+.*occurrences|occurrences.*>=.*3)' "$PHASE02_FILE" 2>/dev/null; then
    echo "[PASS] Confidence filter logic found in Phase 02"
else
    echo "[FAIL] Missing confidence filter (>= low / 3+ occurrences) in Phase 02"
    EXIT_CODE=1
fi

# Test 2: Confidence check in Phase 03
if grep -qE '(confidence.*>=.*low|confidence.*!=.*emerging|3\+.*occurrences|occurrences.*>=.*3)' "$PHASE03_FILE" 2>/dev/null; then
    echo "[PASS] Confidence filter logic found in Phase 03"
else
    echo "[FAIL] Missing confidence filter (>= low / 3+ occurrences) in Phase 03"
    EXIT_CODE=1
fi

exit $EXIT_CODE
