#!/usr/bin/env bash
# STORY-375 AC#2: Baseline Grep-Only Workflow Measured
# TDD Red Phase - These tests MUST fail initially
# Tests verify the research document contains baseline measurement data:
#   - Baseline measurements for all test queries
#   - Per-query Grep invocation count
#   - Per-query character/token count
#   - Per-query files touched count

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

echo "=== AC#2: Baseline Grep-Only Workflow Measured ==="
echo ""

# Guard: if no document, all tests fail
if [ -z "$RESEARCH_FILE" ] || [ ! -f "$RESEARCH_FILE" ]; then
    run_test "Baseline measurement section exists" 1
    run_test "Baseline data table with invocation counts present" 1
    run_test "Per-query character/token count recorded in baseline table" 1
    run_test "Per-query files touched count recorded" 1
    run_test "All test queries (min 5) have baseline measurement entries" 1
    run_test "No missing entries in baseline data table" 1
else
    # Test 1: Baseline section exists
    if grep -qi "## Baseline\|## Grep-Only\|## Baseline.*Measurement\|## Grep.*Baseline" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Baseline measurement section exists" 0
    else
        run_test "Baseline measurement section exists" 1
    fi

    # Test 2: Baseline data table present with invocation counts
    if grep -q "|.*[Ii]nvocation\||.*invocation.*[Cc]ount\||.*grep_invocations" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Baseline data table with invocation counts present" 0
    else
        run_test "Baseline data table with invocation counts present" 1
    fi

    # Test 3: Per-query character/token count recorded
    has_token_col=false
    has_query_rows=false
    if grep -qi "character.*count\|token.*count\|chars\|tokens" "$RESEARCH_FILE" 2>/dev/null; then
        has_token_col=true
    fi
    if grep -q "|.*TQ-[0-9]" "$RESEARCH_FILE" 2>/dev/null; then
        has_query_rows=true
    fi
    if $has_token_col && $has_query_rows; then
        run_test "Per-query character/token count recorded in baseline table" 0
    else
        run_test "Per-query character/token count recorded in baseline table" 1
    fi

    # Test 4: Per-query files touched count
    if grep -qi "files.*touched\|files.*read\|files.*count\|files_touched" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Per-query files touched count recorded" 0
    else
        run_test "Per-query files touched count recorded" 1
    fi

    # Test 5: All test queries have baseline entries
    query_count=$(grep -o "TQ-[0-9]\{3\}" "$RESEARCH_FILE" 2>/dev/null | sort -u | wc -l)
    if [ "$query_count" -ge 5 ]; then
        run_test "All test queries (min 5) have baseline measurement entries" 0
    else
        run_test "All test queries (min 5) have baseline measurement entries" 1
    fi

    # Test 6: No missing baseline entries (no empty cells)
    if grep -q "||" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "No missing entries in baseline data table" 1
    else
        run_test "No missing entries in baseline data table" 0
    fi
fi

echo ""
echo "--- AC#2 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
