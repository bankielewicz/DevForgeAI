#!/usr/bin/env bash
# STORY-375 AC#4: Reduction Percentage Calculated and Reported
# TDD Red Phase - These tests MUST fail initially
# Tests verify the research document contains analysis:
#   - Per-query reduction percentage
#   - Overall weighted average reduction
#   - PASS/FAIL classification against 40% target
#   - Regression queries identified (Treelint worse than Grep)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RESEARCH_DIR="$PROJECT_ROOT/devforgeai/specs/research"

# Find the research document
RESEARCH_FILE=""
for f in "$RESEARCH_DIR"/RESEARCH-*-treelint-token-validation*.md; do
    if [ -f "$f" ]; then
        RESEARCH_FILE="$f"
        break
    fi
done

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

echo "=== AC#4: Reduction Percentage Calculated and Reported ==="
echo ""

# Guard: if no document, all tests fail
if [ -z "$RESEARCH_FILE" ] || [ ! -f "$RESEARCH_FILE" ]; then
    run_test "Analysis section exists in document" 1
    run_test "Per-query reduction percentages present" 1
    run_test "Overall weighted average reduction calculated" 1
    run_test "PASS/FAIL classification against 40% target present" 1
    run_test "Regression queries identified (or explicitly stated none)" 1
    run_test "Reduction calculation formula documented" 1
else
    # Test 1: Analysis section exists
    if grep -qi "## Analysis\|## Reduction Analysis\|## Comparison\|## Results.*Analysis" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Analysis section exists in document" 0
    else
        run_test "Analysis section exists in document" 1
    fi

    # Test 2: Per-query reduction percentage present
    if grep -q "[0-9]\{1,3\}\(\.[0-9]\{1,2\}\)\?%" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Per-query reduction percentages present" 0
    else
        run_test "Per-query reduction percentages present" 1
    fi

    # Test 3: Overall weighted average reduction
    if grep -qi "weighted.*average\|overall.*reduction\|average.*reduction\|overall.*average" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Overall weighted average reduction calculated" 0
    else
        run_test "Overall weighted average reduction calculated" 1
    fi

    # Test 4: PASS/FAIL classification against 40% target
    has_classification=false
    has_target=false
    if grep -q "PASS\|FAIL" "$RESEARCH_FILE" 2>/dev/null; then
        has_classification=true
    fi
    if grep -q "40%" "$RESEARCH_FILE" 2>/dev/null; then
        has_target=true
    fi
    if $has_classification && $has_target; then
        run_test "PASS/FAIL classification against 40% target present" 0
    else
        run_test "PASS/FAIL classification against 40% target present" 1
    fi

    # Test 5: Regression queries identified
    if grep -qi "regression\|worse.*than.*grep\|negative.*reduction\|treelint.*worse\|no.*regression" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Regression queries identified (or explicitly stated none)" 0
    else
        run_test "Regression queries identified (or explicitly stated none)" 1
    fi

    # Test 6: Reduction formula documented
    if grep -qi "baseline.*treelint.*baseline\|reduction.*formula\|percentage.*calculation\|(baseline - treelint)" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Reduction calculation formula documented" 0
    else
        run_test "Reduction calculation formula documented" 1
    fi
fi

echo ""
echo "--- AC#4 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
