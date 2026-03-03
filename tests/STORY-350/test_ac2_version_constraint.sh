#!/bin/bash
# STORY-350 AC#2: Version Constraint Specified
# Test: Verify version "v0.12.0+" with rationale for minimum version

set -e

TECH_STACK="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md"

echo "=== AC#2: Version Constraint Specified ==="

# Test 1: Version constraint v0.12.0+ exists
echo -n "Test 1: Version constraint v0.12.0+ documented... "
if grep -q "v0\.12\.0+" "$TECH_STACK"; then
    echo "PASS"
else
    echo "FAIL - Version constraint v0.12.0+ not found"
    exit 1
fi

# Test 2: Rationale for minimum version exists (daemon support or similar)
echo -n "Test 2: Version rationale provided... "
if grep -iE "(daemon|minimum|reason|rationale)" "$TECH_STACK" | grep -qi "0\.12"; then
    echo "PASS"
else
    echo "FAIL - Version rationale not found near version constraint"
    exit 1
fi

echo ""
echo "=== AC#2 All Tests Passed ==="
exit 0
