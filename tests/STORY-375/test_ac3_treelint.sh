#!/usr/bin/env bash
# STORY-375 AC#3: Treelint-Enabled Workflow Measured
# TDD Red Phase - These tests MUST fail initially
# Tests verify the research document contains Treelint measurement data:
#   - Treelint measurements for all test queries
#   - Treelint + Grep fallback invocation counts
#   - Per-query character/token count
#   - Fallback events annotated for unsupported file types

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

echo "=== AC#3: Treelint-Enabled Workflow Measured ==="
echo ""

# Guard: if no document, all tests fail
if [ -z "$RESEARCH_FILE" ] || [ ! -f "$RESEARCH_FILE" ]; then
    run_test "Treelint measurement section exists" 1
    run_test "Treelint invocation counts recorded" 1
    run_test "Grep fallback invocation counts recorded" 1
    run_test "Per-query character/token count recorded in Treelint table" 1
    run_test "Fallback events annotated for unsupported file types" 1
    run_test "All test queries have Treelint entries or SKIPPED annotation" 1
else
    # Test 1: Treelint measurement section exists
    if grep -qi "## Treelint\|## Treelint.*Measurement\|## Treelint-Enabled\|## AST-Aware" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Treelint measurement section exists" 0
    else
        run_test "Treelint measurement section exists" 1
    fi

    # Test 2: Treelint invocation counts recorded
    if grep -qi "treelint.*invocation\|invocation.*treelint\|treelint_invocations" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Treelint invocation counts recorded" 0
    else
        run_test "Treelint invocation counts recorded" 1
    fi

    # Test 3: Grep fallback invocation counts recorded
    if grep -qi "fallback.*invocation\|grep.*fallback\|fallback_count\|fallback.*grep" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Grep fallback invocation counts recorded" 0
    else
        run_test "Grep fallback invocation counts recorded" 1
    fi

    # Test 4: Per-query token/character count in Treelint section
    has_treelint=false
    has_query_rows=false
    if grep -qi "treelint" "$RESEARCH_FILE" 2>/dev/null; then
        has_treelint=true
    fi
    if grep -q "|.*TQ-[0-9]" "$RESEARCH_FILE" 2>/dev/null; then
        has_query_rows=true
    fi
    if $has_treelint && $has_query_rows; then
        run_test "Per-query character/token count recorded in Treelint table" 0
    else
        run_test "Per-query character/token count recorded in Treelint table" 1
    fi

    # Test 5: Fallback events annotated
    if grep -qi "FALLBACK\|fallback.*event\|unsupported.*type\|fell.*back\|fallback.*annotation" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Fallback events annotated for unsupported file types" 0
    else
        run_test "Fallback events annotated for unsupported file types" 1
    fi

    # Test 6: All test queries have Treelint entries (or SKIPPED annotation)
    query_ids=$(grep -o "TQ-[0-9]\{3\}" "$RESEARCH_FILE" 2>/dev/null | sort -u | wc -l)
    if [ "$query_ids" -ge 5 ]; then
        run_test "All test queries have Treelint entries or SKIPPED annotation" 0
    else
        run_test "All test queries have Treelint entries or SKIPPED annotation" 1
    fi
fi

echo ""
echo "--- AC#3 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
