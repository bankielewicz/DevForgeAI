#!/usr/bin/env bash
# STORY-404 AC#1: Small story single-pass behavior preserved
# TDD Red Phase - These tests MUST fail before implementation
#
# Validates that the ac-compliance-verifier specification documents:
# - A threshold check for stories with <5 ACs
# - Single-pass verification for small stories
# - Report format unchanged for small stories
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

echo "=== AC#1: Small Story Single-Pass Behavior Preserved ==="
echo ""

# Test 1: Verifier source file exists
if [ -f "$VERIFIER_FILE" ]; then
    run_test "Verifier source file exists" 0
else
    run_test "Verifier source file exists" 1
    echo "--- AC#1 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 2: Verifier spec mentions a threshold for chunking activation (e.g., "5" ACs)
# The spec must document that stories with fewer than 5 ACs use single-pass
if grep -qP 'fewer than 5|less than 5|<\s*5|threshold.*5|5\+?\s*ACs?' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec documents threshold of 5 ACs for chunking activation" 0
else
    run_test "Spec documents threshold of 5 ACs for chunking activation" 1
fi

# Test 3: Verifier spec explicitly states single-pass for small stories
if grep -qi 'single.pass\|single pass\|all ACs.*single\|one pass\|without chunking' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec documents single-pass behavior for small stories" 0
else
    run_test "Spec documents single-pass behavior for small stories" 1
fi

# Test 4: Verifier spec states report format unchanged for small stories
if grep -qi 'unchanged\|identical\|same format\|format preserved\|backward.compatible' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec states report format unchanged for small stories" 0
else
    run_test "Spec states report format unchanged for small stories" 1
fi

echo ""
echo "--- AC#1 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
