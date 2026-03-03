#!/bin/bash
# STORY-351 AC#1: Binary Dependencies Section Created
# Tests that "Binary Dependencies (EPIC-055)" section exists between Optional CLI and Platform Support

set -e

DEPS_FILE="devforgeai/specs/context/dependencies.md"

echo "AC#1: Testing Binary Dependencies section exists..."

# Test 1: Section header exists
if ! grep -q "### Binary Dependencies (EPIC-055)" "$DEPS_FILE"; then
    echo "FAIL: Binary Dependencies (EPIC-055) section not found"
    exit 1
fi

# Test 2: Section appears AFTER Optional CLI Dependencies
OPTIONAL_LINE=$(grep -n "### Optional CLI Dependencies" "$DEPS_FILE" | head -1 | cut -d: -f1)
BINARY_LINE=$(grep -n "### Binary Dependencies (EPIC-055)" "$DEPS_FILE" | head -1 | cut -d: -f1)

if [ -z "$OPTIONAL_LINE" ] || [ -z "$BINARY_LINE" ]; then
    echo "FAIL: Could not find section line numbers"
    exit 1
fi

if [ "$BINARY_LINE" -le "$OPTIONAL_LINE" ]; then
    echo "FAIL: Binary Dependencies section must appear AFTER Optional CLI Dependencies"
    exit 1
fi

# Test 3: Section appears BEFORE Platform Support
PLATFORM_LINE=$(grep -n "### Platform Support" "$DEPS_FILE" | head -1 | cut -d: -f1)

if [ -z "$PLATFORM_LINE" ]; then
    echo "FAIL: Platform Support section not found"
    exit 1
fi

if [ "$BINARY_LINE" -ge "$PLATFORM_LINE" ]; then
    echo "FAIL: Binary Dependencies section must appear BEFORE Platform Support"
    exit 1
fi

echo "PASS: AC#1 - Binary Dependencies section exists in correct location"
exit 0
