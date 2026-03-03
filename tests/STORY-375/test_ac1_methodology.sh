#!/usr/bin/env bash
# STORY-375 AC#1: Token Counting Methodology Documented
# TDD Red Phase - These tests MUST fail initially
# Tests verify the research document has a methodology section with:
#   - Token definition
#   - Minimum 5 test queries with unique IDs
#   - Statistical method for reduction calculation

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RESEARCH_DIR="$PROJECT_ROOT/devforgeai/specs/research"

# Find the research document matching the naming pattern
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

echo "=== AC#1: Token Counting Methodology Documented ==="
echo ""

# Test 1: Research document exists
if [ -n "$RESEARCH_FILE" ] && [ -f "$RESEARCH_FILE" ]; then
    run_test "Research document exists at devforgeai/specs/research/" 0
else
    run_test "Research document exists at devforgeai/specs/research/" 1
fi

# Guard: if no document, remaining tests fail by definition
if [ -z "$RESEARCH_FILE" ] || [ ! -f "$RESEARCH_FILE" ]; then
    run_test "Methodology section present in document" 1
    run_test "Token definition documented (character-count proxy or API tokens)" 1
    run_test "Minimum 5 test queries defined with unique IDs (TQ-NNN)" 1
    run_test "All test query IDs are unique" 1
    run_test "Statistical method for reduction calculation documented" 1
else
    # Test 2: Methodology section present
    if grep -qi "## Methodology\|## Token Counting Methodology\|## Measurement Methodology" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Methodology section present in document" 0
    else
        run_test "Methodology section present in document" 1
    fi

    # Test 3: Token definition documented
    if grep -qi "token.*definition\|character.*count.*proxy\|what.*constitutes.*token\|token.*proxy" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Token definition documented (character-count proxy or API tokens)" 0
    else
        run_test "Token definition documented (character-count proxy or API tokens)" 1
    fi

    # Test 4: Minimum 5 test queries defined
    count=$(grep -c "TQ-[0-9]\{3\}" "$RESEARCH_FILE" 2>/dev/null || echo "0")
    if [ "$count" -ge 5 ]; then
        run_test "Minimum 5 test queries defined with unique IDs (TQ-NNN)" 0
    else
        run_test "Minimum 5 test queries defined with unique IDs (TQ-NNN)" 1
    fi

    # Test 5: All query IDs are unique
    total_ids=$(grep -o "TQ-[0-9]\{3\}" "$RESEARCH_FILE" 2>/dev/null | wc -l)
    unique_ids=$(grep -o "TQ-[0-9]\{3\}" "$RESEARCH_FILE" 2>/dev/null | sort -u | wc -l)
    if [ "$total_ids" -gt 0 ] && [ "$total_ids" -eq "$unique_ids" ]; then
        run_test "All test query IDs are unique" 0
    else
        run_test "All test query IDs are unique" 1
    fi

    # Test 6: Statistical method documented
    if grep -qi "reduction.*calculation\|statistical.*method\|weighted.*average\|percentage.*formula\|calculation.*method" "$RESEARCH_FILE" 2>/dev/null; then
        run_test "Statistical method for reduction calculation documented" 0
    else
        run_test "Statistical method for reduction calculation documented" 1
    fi
fi

echo ""
echo "--- AC#1 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
