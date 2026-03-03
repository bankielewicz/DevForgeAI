#!/bin/bash
# STORY-351 AC#2: Binary Size Documented
# Tests that Treelint binary size "~7.7 MB" is documented with platform variation note

set -e

DEPS_FILE="devforgeai/specs/context/dependencies.md"

echo "AC#2: Testing binary size documentation..."

# Test 1: Binary size ~7.7 MB documented
if ! grep -q "~7.7 MB" "$DEPS_FILE"; then
    echo "FAIL: Binary size '~7.7 MB' not found"
    exit 1
fi

# Test 2: Platform variation note exists
if ! grep -qi "varies by platform\|varies slightly by platform\|platform.* vari" "$DEPS_FILE"; then
    echo "FAIL: Platform variation note not found"
    exit 1
fi

echo "PASS: AC#2 - Binary size documented with platform variation note"
exit 0
