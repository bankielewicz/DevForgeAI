#!/bin/bash
# STORY-333 AC#5: Observation Capture Section (EPIC-052 Compliance)
# Tests that core file has Observation Capture with 7 categories
# TDD Red Phase: These tests FAIL until implementation complete

set -e
CORE_FILE="src/claude/agents/test-automator.md"

echo "=== AC#5: Observation Capture Section ==="

# Test 1: Observation Capture section exists
echo -n "Test 1: Observation Capture section exists... "
if ! grep -qE "^## Observation Capture" "$CORE_FILE"; then
    echo "FAIL"
    exit 1
fi
echo "PASS"

# Test 2: MANDATORY marker present
echo -n "Test 2: MANDATORY marker present... "
if ! grep -qE "MANDATORY" "$CORE_FILE"; then
    echo "FAIL"
    exit 1
fi
echo "PASS"

# Test 3: All 7 observation categories present
echo -n "Test 3: 7 observation categories... "
CATEGORIES=("friction" "success" "pattern" "gap" "idea" "bug" "warning")
MISSING=""
for CAT in "${CATEGORIES[@]}"; do
    if ! grep -q "$CAT" "$CORE_FILE"; then
        MISSING="$MISSING $CAT"
    fi
done
if [ -n "$MISSING" ]; then
    echo "FAIL (missing:$MISSING)"
    exit 1
fi
echo "PASS"

# Test 4: Severity levels documented
echo -n "Test 4: Severity levels (low/medium/high)... "
SEVERITIES=("low" "medium" "high")
for SEV in "${SEVERITIES[@]}"; do
    if ! grep -q "$SEV" "$CORE_FILE"; then
        echo "FAIL (missing: $SEV)"
        exit 1
    fi
done
echo "PASS"

# Test 5: Write() instruction for observations
echo -n "Test 5: Write() instruction present... "
if ! grep -qE "Write\(" "$CORE_FILE" || ! grep -qE "observation_json|ai-analysis" "$CORE_FILE"; then
    echo "FAIL"
    exit 1
fi
echo "PASS"

echo ""
echo "AC#5: All tests PASSED"
