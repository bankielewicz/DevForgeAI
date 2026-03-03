#!/usr/bin/env bash
# STORY-404 AC#6: Token reduction measurable for 5+ AC stories
# TDD Red Phase - These tests MUST fail before implementation
#
# Validates that the ac-compliance-verifier specification documents:
# - Chunking metadata logged in observations_for_persistence
# - chunk_count field in metadata
# - ac_count field in metadata
# - Metadata only present when chunking is active (5+ ACs)
#
# Expected: FAIL initially (chunking logic not yet in verifier spec)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VERIFIER_FILE="${PROJECT_ROOT}/src/claude/agents/ac-compliance-verifier.md"

PASS=0
FAIL=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    TOTAL=$((TOTAL + 1))
    if [ "$result" -eq 0 ]; then
        PASS=$((PASS + 1))
        echo "  PASS: $name"
    else
        FAIL=$((FAIL + 1))
        echo "  FAIL: $name"
    fi
}

echo "=== AC#6: Token Reduction Measurable for 5+ AC Stories ==="
echo ""

# Test 1: Verifier source file exists
if [ -f "$VERIFIER_FILE" ]; then
    run_test "Verifier source file exists" 0
else
    run_test "Verifier source file exists" 1
    echo "--- AC#6 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 2: Spec mentions chunking metadata in observations
if grep -qiP 'chunk.*metadata|metadata.*chunk|observations.*chunk_count|observations.*ac_count' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec mentions chunking metadata in observations" 0
else
    run_test "Spec mentions chunking metadata in observations" 1
fi

# Test 3: Spec documents chunk_count field
if grep -qP 'chunk_count' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec documents chunk_count field" 0
else
    run_test "Spec documents chunk_count field" 1
fi

# Test 4: Spec documents ac_count field
if grep -qP 'ac_count' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec documents ac_count field" 0
else
    run_test "Spec documents ac_count field" 1
fi

# Test 5: Spec connects metadata to observations_for_persistence JSON
if grep -qiP 'observations_for_persistence.*chunk|chunk.*observations_for_persistence' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec connects metadata to observations_for_persistence" 0
else
    run_test "Spec connects metadata to observations_for_persistence" 1
fi

echo ""
echo "--- AC#6 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
