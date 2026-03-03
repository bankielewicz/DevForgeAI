#!/bin/bash
# STORY-350 AC#4: Fallback Behavior Documented
# Test: Verify Grep fallback guidance and language support table

set -e

TECH_STACK="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/context/tech-stack.md"

echo "=== AC#4: Fallback Behavior Documented ==="

# Test 1: Grep fallback mentioned
echo -n "Test 1: Grep fallback documented... "
if grep -qi "grep.*fallback\|fallback.*grep" "$TECH_STACK"; then
    echo "PASS"
else
    echo "FAIL - Grep fallback guidance not found"
    exit 1
fi

# Test 2: Language support table exists (check for Python)
echo -n "Test 2: Python in language support... "
if grep -qi "python" "$TECH_STACK" | grep -qi "treelint\|supported\|language"; then
    echo "PASS"
else
    # Fallback: just check Python appears near treelint section
    if grep -A50 "Treelint" "$TECH_STACK" | grep -qi "python"; then
        echo "PASS"
    else
        echo "FAIL - Python not in language support"
        exit 1
    fi
fi

# Test 3: TypeScript in language support
echo -n "Test 3: TypeScript in language support... "
if grep -A50 "Treelint" "$TECH_STACK" | grep -qi "typescript"; then
    echo "PASS"
else
    echo "FAIL - TypeScript not in language support"
    exit 1
fi

# Test 4: JavaScript in language support
echo -n "Test 4: JavaScript in language support... "
if grep -A50 "Treelint" "$TECH_STACK" | grep -qi "javascript"; then
    echo "PASS"
else
    echo "FAIL - JavaScript not in language support"
    exit 1
fi

# Test 5: Rust in language support
echo -n "Test 5: Rust in language support... "
if grep -A50 "Treelint" "$TECH_STACK" | grep -qi "rust"; then
    echo "PASS"
else
    echo "FAIL - Rust not in language support"
    exit 1
fi

# Test 6: Markdown in language support
echo -n "Test 6: Markdown in language support... "
if grep -A50 "Treelint" "$TECH_STACK" | grep -qi "markdown"; then
    echo "PASS"
else
    echo "FAIL - Markdown not in language support"
    exit 1
fi

echo ""
echo "=== AC#4 All Tests Passed ==="
exit 0
