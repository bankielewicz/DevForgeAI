#!/bin/bash
# STORY-350 AC#1: Treelint Added to Static Analysis Tools Section
# Test: Verify "APPROVED: Treelint (ADR-013)" section exists with required content

set -e

TECH_STACK="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md"

echo "=== AC#1: Treelint Added to Static Analysis Tools Section ==="

# Test 1: Section header exists
echo -n "Test 1: APPROVED: Treelint (ADR-013) section exists... "
if grep -q "### APPROVED: Treelint (ADR-013)" "$TECH_STACK"; then
    echo "PASS"
else
    echo "FAIL - Section header not found"
    exit 1
fi

# Test 2: Status shows APPROVED
echo -n "Test 2: Status shows 'APPROVED'... "
if grep -A5 "### APPROVED: Treelint" "$TECH_STACK" | grep -q "APPROVED"; then
    echo "PASS"
else
    echo "FAIL - APPROVED status not found"
    exit 1
fi

# Test 3: Version constraint v0.12.0+ exists
echo -n "Test 3: Version v0.12.0+ specified... "
if grep -q "v0\.12\.0+" "$TECH_STACK"; then
    echo "PASS"
else
    echo "FAIL - Version constraint v0.12.0+ not found"
    exit 1
fi

# Test 4: ADR-013 reference exists
echo -n "Test 4: ADR-013 reference exists... "
if grep -q "ADR-013" "$TECH_STACK"; then
    echo "PASS"
else
    echo "FAIL - ADR-013 reference not found"
    exit 1
fi

echo ""
echo "=== AC#1 All Tests Passed ==="
exit 0
