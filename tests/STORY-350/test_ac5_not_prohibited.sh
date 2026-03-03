#!/bin/bash
# STORY-350 AC#5: Treelint NOT in PROHIBITED Sections
# Test: Verify treelint does not appear in PROHIBITED contexts

set -e

TECH_STACK="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md"

echo "=== AC#5: Treelint NOT in PROHIBITED Sections ==="

# Test 1: No "treelint" with prohibited prefix
echo -n "Test 1: No treelint with prohibited prefix... "
if grep -qi "treelint" "$TECH_STACK" | grep -q "PROHIBITED"; then
    echo "FAIL - treelint found in PROHIBITED context"
    exit 1
else
    echo "PASS"
fi

# Test 2: No treelint entries in PROHIBITED lists
echo -n "Test 2: No treelint in PROHIBITED lists... "
PROHIBITED_SECTIONS=$(grep -n "PROHIBITED" "$TECH_STACK" | cut -d: -f1)
TREELINT_PROHIBITED=0
for LINE in $PROHIBITED_SECTIONS; do
    # Check 10 lines after each PROHIBITED header for treelint
    if sed -n "${LINE},$((LINE+10))p" "$TECH_STACK" | grep -qi "treelint"; then
        TREELINT_PROHIBITED=1
        break
    fi
done
if [ "$TREELINT_PROHIBITED" -eq 1 ]; then
    echo "FAIL - treelint found near PROHIBITED section"
    exit 1
else
    echo "PASS"
fi

echo ""
echo "=== AC#5 All Tests Passed ==="
exit 0
