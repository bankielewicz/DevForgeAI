#!/bin/bash
# STORY-351 AC#4: Distribution Pattern Documented
# Tests "bundled in installer" pattern with installation path and checksum verification

set -e

DEPS_FILE="devforgeai/specs/context/dependencies.md"

echo "AC#4: Testing distribution pattern documentation..."

# Test 1: "bundled in installer" pattern documented
if ! grep -qi "bundled.*installer\|bundled in.*installer" "$DEPS_FILE"; then
    echo "FAIL: 'bundled in installer' distribution pattern not found"
    exit 1
fi

# Test 2: Installation path documented
if ! grep -q "\.treelint/bin/treelint\|Installation Path" "$DEPS_FILE"; then
    echo "FAIL: Installation path not documented"
    exit 1
fi

# Test 3: Checksum verification mentioned
if ! grep -qi "checksum\|SHA256" "$DEPS_FILE"; then
    echo "FAIL: Checksum verification not documented"
    exit 1
fi

echo "PASS: AC#4 - Distribution pattern documented"
exit 0
