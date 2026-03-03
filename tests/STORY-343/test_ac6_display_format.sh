#!/bin/bash
# STORY-343 AC#6: Display Format Matches Specification
# TDD Red Phase - This test MUST FAIL until implementation complete

PHASE02_FILE=".claude/skills/devforgeai-development/phases/phase-02-test-first.md"
EXIT_CODE=0

echo "=== AC#6: Display Format Matches Specification ==="

# Test 1: Unicode box drawing characters used
if grep -q "━" "$PHASE02_FILE" 2>/dev/null; then
    echo "[PASS] Unicode box drawing character found"
else
    echo "[FAIL] Missing Unicode box drawing characters in display template"
    EXIT_CODE=1
fi

# Test 2: Pattern name displayed
if grep -qE 'Pattern:.*\{' "$PHASE02_FILE" 2>/dev/null || grep -q "pattern_name" "$PHASE02_FILE" 2>/dev/null; then
    echo "[PASS] Pattern name display found"
else
    echo "[FAIL] Missing pattern name in display template"
    EXIT_CODE=1
fi

# Test 3: Occurrences displayed
if grep -qE '(occurrences|Occurrences)' "$PHASE02_FILE" 2>/dev/null; then
    echo "[PASS] Occurrences display found"
else
    echo "[FAIL] Missing occurrences in display template"
    EXIT_CODE=1
fi

# Test 4: Recommendation displayed
if grep -qE '(Recommendation:|recommendation)' "$PHASE02_FILE" 2>/dev/null; then
    echo "[PASS] Recommendation display found"
else
    echo "[FAIL] Missing recommendation in display template"
    EXIT_CODE=1
fi

exit $EXIT_CODE
