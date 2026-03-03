#!/bin/bash
# STORY-379 AC#7: Installation and Setup Section with Platform-Specific Instructions
# Tests verify the installation section contains:
#   - Minimum version requirement (v0.12.0+) with rationale
#   - pip install method
#   - cargo install method
#   - Bundled binary locations per source-tree.md
#   - Verification command (treelint --version)
#   - 5 platforms: Linux x86_64, Linux ARM64, macOS x86_64, macOS Apple Silicon, Windows x86_64
#
# TDD Red Phase: All tests MUST FAIL because docs/guides/treelint-integration-guide.md does not exist yet.

set -e

GUIDE="/mnt/c/Projects/DevForgeAI2/docs/guides/treelint-integration-guide.md"

echo "=== AC#7: Installation and Setup Section with Platform-Specific Instructions ==="

# Test 1: Guide file exists
echo -n "Test 1: Guide file exists... "
if [ -f "$GUIDE" ]; then
    echo "PASS"
else
    echo "FAIL - File does not exist"
    exit 1
fi

# Test 2: Installation section header exists
echo -n "Test 2: Installation section header exists... "
if grep -qi "## Installation\|## Setup\|## Installation and Setup\|## Getting Started" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Installation section header not found"
    exit 1
fi

# Test 3: Minimum version requirement v0.12.0+ stated
echo -n "Test 3: Version requirement v0.12.0+ stated... "
if grep -q "v0\.12\.0\|0\.12\.0" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Version requirement v0.12.0 not found"
    exit 1
fi

# Test 4: Version rationale provided
echo -n "Test 4: Version rationale provided... "
if grep -qi "daemon.*mode\|JSON.*output\|--format json\|language support\|minimum.*version\|v0\.12" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Version rationale not found"
    exit 1
fi

# Test 5: pip install method documented
echo -n "Test 5: pip install method documented... "
if grep -q "pip install" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - pip install method not found"
    exit 1
fi

# Test 6: cargo install method documented
echo -n "Test 6: cargo install method documented... "
if grep -q "cargo install" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - cargo install method not found"
    exit 1
fi

# Test 7: Verification command documented (treelint --version)
echo -n "Test 7: Verification command (treelint --version) documented... "
if grep -q "treelint --version\|treelint.*--version" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Verification command 'treelint --version' not found"
    exit 1
fi

# Test 8: Platform - Linux x86_64 listed
echo -n "Test 8: Platform Linux x86_64 listed... "
if grep -qi "linux.*x86_64\|linux.*x86-64\|linux.*amd64" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Linux x86_64 platform not listed"
    exit 1
fi

# Test 9: Platform - Linux ARM64 listed
echo -n "Test 9: Platform Linux ARM64 listed... "
if grep -qi "linux.*arm64\|linux.*aarch64" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Linux ARM64 platform not listed"
    exit 1
fi

# Test 10: Platform - macOS x86_64 listed
echo -n "Test 10: Platform macOS x86_64 listed... "
if grep -qi "macos.*x86_64\|darwin.*x86_64\|mac.*x86_64\|macOS.*Intel" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - macOS x86_64 platform not listed"
    exit 1
fi

# Test 11: Platform - macOS Apple Silicon listed
echo -n "Test 11: Platform macOS Apple Silicon listed... "
if grep -qi "apple.*silicon\|macos.*aarch64\|darwin.*aarch64\|macOS.*ARM\|macos.*arm64\|darwin.*arm64" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - macOS Apple Silicon platform not listed"
    exit 1
fi

# Test 12: Platform - Windows x86_64 listed
echo -n "Test 12: Platform Windows x86_64 listed... "
if grep -qi "windows.*x86_64\|windows.*amd64\|windows.*x86-64" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Windows x86_64 platform not listed"
    exit 1
fi

# Test 13: Bundled binary location referenced
echo -n "Test 13: Bundled binary location referenced... "
if grep -qi "src/bin/treelint\|bundled.*binar" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Bundled binary location not referenced"
    exit 1
fi

echo ""
echo "=== AC#7 All Tests Passed ==="
exit 0
