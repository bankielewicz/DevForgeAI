#!/usr/bin/env bash
# STORY-404 AC#2: Chunking activates at 5+ ACs
# TDD Red Phase - These tests MUST fail before implementation
#
# Validates that the ac-compliance-verifier specification documents:
# - Chunking activation at 5+ ACs
# - Chunk size of 3 ACs per chunk
# - Correct grouping examples (5 ACs -> [3,2], 8 ACs -> [3,3,2])
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

echo "=== AC#2: Chunking Activates at 5+ ACs ==="
echo ""

# Test 1: Verifier source file exists
if [ -f "$VERIFIER_FILE" ]; then
    run_test "Verifier source file exists" 0
else
    run_test "Verifier source file exists" 1
    echo "--- AC#2 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 2: Spec documents chunking concept
if grep -qi 'chunk' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec documents chunking concept" 0
else
    run_test "Spec documents chunking concept" 1
fi

# Test 3: Spec specifies chunk size of 3
if grep -qP 'chunk.*(?:size|of)\s*3|chunks?\s*of\s*3|3\s*ACs?\s*per\s*chunk' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec specifies chunk size of 3 ACs" 0
else
    run_test "Spec specifies chunk size of 3 ACs" 1
fi

# Test 4: Spec provides grouping example for 5 ACs -> 2 chunks [3,2]
if grep -qP '5\s*ACs?.*2\s*chunk|5.*\[3,\s*2\]|\[3,\s*2\].*5' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec shows 5 ACs -> 2 chunks [3,2] example" 0
else
    run_test "Spec shows 5 ACs -> 2 chunks [3,2] example" 1
fi

# Test 5: Spec provides grouping example for 8 ACs -> 3 chunks [3,3,2]
if grep -qP '8\s*ACs?.*3\s*chunk|8.*\[3,\s*3,\s*2\]|\[3,\s*3,\s*2\].*8' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec shows 8 ACs -> 3 chunks [3,3,2] example" 0
else
    run_test "Spec shows 8 ACs -> 3 chunks [3,3,2] example" 1
fi

# Test 6: Spec documents the chunking algorithm or formula
if grep -qiP 'ceil|math\.ceil|divide.*3|grouped.*into.*chunks|chunk.*algorithm' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec documents chunking algorithm" 0
else
    run_test "Spec documents chunking algorithm" 1
fi

echo ""
echo "--- AC#2 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
