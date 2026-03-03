#!/bin/bash
# STORY-351 AC#3: Platform Support Documented
# Tests platform support table lists all required platforms with binary filenames

set -e

DEPS_FILE="devforgeai/specs/context/dependencies.md"

echo "AC#3: Testing platform support documentation..."

# Test 1: Linux x86_64
if ! grep -q "treelint-linux-x86_64" "$DEPS_FILE"; then
    echo "FAIL: Linux x86_64 binary not documented"
    exit 1
fi

# Test 2: Linux aarch64
if ! grep -q "treelint-linux-aarch64" "$DEPS_FILE"; then
    echo "FAIL: Linux aarch64 binary not documented"
    exit 1
fi

# Test 3: macOS x86_64
if ! grep -q "treelint-darwin-x86_64" "$DEPS_FILE"; then
    echo "FAIL: macOS x86_64 binary not documented"
    exit 1
fi

# Test 4: macOS aarch64 (Apple Silicon)
if ! grep -q "treelint-darwin-aarch64" "$DEPS_FILE"; then
    echo "FAIL: macOS aarch64 binary not documented"
    exit 1
fi

# Test 5: Windows x86_64
if ! grep -q "treelint-windows-x86_64" "$DEPS_FILE"; then
    echo "FAIL: Windows x86_64 binary not documented"
    exit 1
fi

echo "PASS: AC#3 - All platform binaries documented"
exit 0
