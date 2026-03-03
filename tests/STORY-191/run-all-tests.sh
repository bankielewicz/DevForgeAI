#!/bin/bash
# STORY-191: Run all acceptance criteria tests
# Expected: ALL tests FAIL initially (TDD Red phase)

cd "$(dirname "$0")"

echo "========================================"
echo "STORY-191: Cross-Reference Format Tests"
echo "========================================"
echo ""

TOTAL_PASS=0
TOTAL_FAIL=0

for test in test-ac*.sh; do
    echo "Running: $test"
    echo "----------------------------------------"
    if bash "$test"; then
        ((TOTAL_PASS++))
    else
        ((TOTAL_FAIL++))
    fi
    echo ""
done

echo "========================================"
echo "SUMMARY: $TOTAL_PASS AC passed, $TOTAL_FAIL AC failed"
echo "========================================"

# In TDD Red phase, we expect failures
if [ $TOTAL_FAIL -gt 0 ]; then
    echo "TDD RED: Tests failing as expected"
    exit 1
else
    echo "TDD GREEN: All tests passing"
    exit 0
fi
