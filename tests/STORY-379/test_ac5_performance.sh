#!/bin/bash
# STORY-379 AC#5: Performance Expectations with Measurable Benchmarks
# Tests verify the performance section contains:
#   - Token reduction range (40-80%)
#   - Cold start overhead documented
#   - Warm search performance documented
#   - Index size expectations
#   - Treelint vs Grep comparison table
#
# TDD Red Phase: All tests MUST FAIL because docs/guides/treelint-integration-guide.md does not exist yet.

set -e

GUIDE="/mnt/c/Projects/DevForgeAI2/docs/guides/treelint-integration-guide.md"

echo "=== AC#5: Performance Expectations with Measurable Benchmarks ==="

# Test 1: Guide file exists
echo -n "Test 1: Guide file exists... "
if [ -f "$GUIDE" ]; then
    echo "PASS"
else
    echo "FAIL - File does not exist"
    exit 1
fi

# Test 2: Performance section header exists
echo -n "Test 2: Performance section header exists... "
if grep -qi "## Performance\|## Performance Expectations\|## Performance Benefits" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Performance section header not found"
    exit 1
fi

# Test 3: Token reduction range 40-80% stated
echo -n "Test 3: Token reduction range 40-80% stated... "
if grep -q "40-80%" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - '40-80%' token reduction range not found"
    exit 1
fi

# Test 4: Cold start overhead documented
echo -n "Test 4: Cold start overhead documented... "
if grep -qi "cold start\|cold-start\|first.*search\|initial.*index\|index.*build" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Cold start overhead not documented"
    exit 1
fi

# Test 5: Warm search performance documented
echo -n "Test 5: Warm search / daemon mode performance documented... "
if grep -qi "warm.*search\|warm.*start\|daemon.*mode\|cached\|subsequent.*search" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Warm search performance not documented"
    exit 1
fi

# Test 6: Index size expectations documented
echo -n "Test 6: Index size expectations documented... "
if grep -qi "index.*size\|proportional\|codebase.*size\|LOC\|storage" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Index size expectations not documented"
    exit 1
fi

# Test 7: Comparison table present (Treelint vs Grep)
echo -n "Test 7: Treelint vs Grep comparison table present... "
if grep -q "|" "$GUIDE" && grep -qi "Treelint\|treelint" "$GUIDE" && grep -qi "Grep\|grep" "$GUIDE"; then
    # Verify it is a table with both Treelint and Grep in table rows
    TABLE_LINES=$(grep -i "|.*[Tt]reelint\|[Tt]reelint.*|" "$GUIDE" | wc -l)
    if [ "$TABLE_LINES" -ge 1 ]; then
        echo "PASS"
    else
        echo "FAIL - Comparison table does not contain Treelint in table rows"
        exit 1
    fi
else
    echo "FAIL - Treelint vs Grep comparison table not found"
    exit 1
fi

# Test 8: Cold vs warm comparison data present
echo -n "Test 8: Cold vs warm comparison data present... "
if grep -qi "cold" "$GUIDE" && grep -qi "warm" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Cold and warm comparison data not present"
    exit 1
fi

echo ""
echo "=== AC#5 All Tests Passed ==="
exit 0
