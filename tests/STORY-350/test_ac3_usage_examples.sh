#!/bin/bash
# STORY-350 AC#3: Usage Examples for Subagent Integration
# Test: Verify at least 3 usage examples with --format json flag

set -e

TECH_STACK="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md"

echo "=== AC#3: Usage Examples for Subagent Integration ==="

# Test 1: Count treelint examples with --format json
echo -n "Test 1: At least 3 treelint examples with --format json... "
COUNT=$(grep -c "treelint.*--format json" "$TECH_STACK" 2>/dev/null || true)
COUNT=${COUNT:-0}
if [ "$COUNT" -ge 3 ]; then
    echo "PASS ($COUNT examples found)"
else
    echo "FAIL - Only $COUNT examples found (need 3+)"
    exit 1
fi

# Test 2: treelint search example exists
echo -n "Test 2: treelint search example exists... "
if grep -q "treelint search" "$TECH_STACK"; then
    echo "PASS"
else
    echo "FAIL - treelint search example not found"
    exit 1
fi

# Test 3: treelint map example exists
echo -n "Test 3: treelint map example exists... "
if grep -q "treelint map" "$TECH_STACK"; then
    echo "PASS"
else
    echo "FAIL - treelint map example not found"
    exit 1
fi

# Test 4: treelint deps example exists
echo -n "Test 4: treelint deps example exists... "
if grep -q "treelint deps" "$TECH_STACK"; then
    echo "PASS"
else
    echo "FAIL - treelint deps example not found"
    exit 1
fi

echo ""
echo "=== AC#3 All Tests Passed ==="
exit 0
