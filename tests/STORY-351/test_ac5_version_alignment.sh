#!/bin/bash
# STORY-351 AC#5: Version Constraint Aligned with tech-stack.md
# Tests version v0.12.0+ and ADR-013 reference

set -e

DEPS_FILE="devforgeai/specs/context/dependencies.md"
TECH_FILE="devforgeai/specs/context/tech-stack.md"

echo "AC#5: Testing version alignment..."

# Test 1: Version v0.12.0+ in dependencies.md
if ! grep -q "v0\.12\.0" "$DEPS_FILE"; then
    echo "FAIL: Version 'v0.12.0+' not found in dependencies.md"
    exit 1
fi

# Test 2: ADR-013 reference in dependencies.md
if ! grep -q "ADR-013" "$DEPS_FILE"; then
    echo "FAIL: ADR-013 reference not found in dependencies.md"
    exit 1
fi

# Test 3: Version matches tech-stack.md
DEPS_VERSION=$(grep -o "v0\.[0-9]*\.[0-9]*" "$DEPS_FILE" | head -1)
TECH_VERSION=$(grep -o "v0\.[0-9]*\.[0-9]*" "$TECH_FILE" | grep -E "0\.12" | head -1)

if [ "$DEPS_VERSION" != "$TECH_VERSION" ]; then
    echo "FAIL: Version mismatch - dependencies.md: $DEPS_VERSION, tech-stack.md: $TECH_VERSION"
    exit 1
fi

echo "PASS: AC#5 - Version aligned with tech-stack.md and ADR-013 referenced"
exit 0
