#!/usr/bin/env bash
# STORY-404 AC#5: Downstream consumers unaffected
# TDD Red Phase - These tests MUST fail before implementation
#
# Validates that the ac-compliance-verifier specification documents:
# - Downstream consumers (Phase 4.5/5.5, QA skill) process report without modification
# - Chunking is transparent to consumers
# - No new fields that would break existing consumers
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

echo "=== AC#5: Downstream Consumers Unaffected ==="
echo ""

# Test 1: Verifier source file exists
if [ -f "$VERIFIER_FILE" ]; then
    run_test "Verifier source file exists" 0
else
    run_test "Verifier source file exists" 1
    echo "--- AC#5 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 2: Spec documents that downstream consumers are unaffected
if grep -qiP 'downstream.*unaffect|consumer.*unaffect|transparent.*consumer|no.*modif.*consumer|backward.*compat' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec documents downstream consumers unaffected" 0
else
    run_test "Spec documents downstream consumers unaffected" 1
fi

# Test 3: Spec mentions Phase 4.5 or Phase 5.5 compatibility
if grep -qiP 'Phase\s*4\.5.*compat|Phase\s*5\.5.*compat|4\.5.*5\.5.*unaware|consumer.*no.*awareness.*chunk' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec mentions Phase 4.5/5.5 compatibility" 0
else
    run_test "Spec mentions Phase 4.5/5.5 compatibility" 1
fi

# Test 4: Spec states chunking is an internal implementation detail
if grep -qiP 'internal.*detail|implementation.*detail|transparent|opaque.*consumer|hidden.*from.*consumer' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec states chunking is internal implementation detail" 0
else
    run_test "Spec states chunking is internal implementation detail" 1
fi

echo ""
echo "--- AC#5 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
