#!/bin/bash
# STORY-379 AC#2: Supported Languages Matrix with File Extensions and Status
# Tests verify the supported languages section contains:
#   - Table with 5 language rows (Python, TypeScript, JavaScript, Rust, Markdown)
#   - Correct file extensions per language
#   - Support status indicator
#   - Unsupported language fallback statement
#
# TDD Red Phase: All tests MUST FAIL because docs/guides/treelint-integration-guide.md does not exist yet.

set -e

GUIDE="/mnt/c/Projects/DevForgeAI2/docs/guides/treelint-integration-guide.md"

echo "=== AC#2: Supported Languages Matrix with File Extensions and Status ==="

# Test 1: Guide file exists
echo -n "Test 1: Guide file exists... "
if [ -f "$GUIDE" ]; then
    echo "PASS"
else
    echo "FAIL - File does not exist"
    exit 1
fi

# Test 2: Supported Languages section header exists
echo -n "Test 2: Supported Languages section header exists... "
if grep -qi "Supported Languages\|Language Support" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Supported Languages section header not found"
    exit 1
fi

# Test 3: Python with .py extension listed
echo -n "Test 3: Python with .py extension listed... "
if grep -q "Python" "$GUIDE" && grep -q "\.py" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Python or .py extension not found"
    exit 1
fi

# Test 4: TypeScript with .ts/.tsx extensions listed
echo -n "Test 4: TypeScript with .ts/.tsx extensions listed... "
if grep -q "TypeScript" "$GUIDE" && grep -q "\.ts" "$GUIDE" && grep -q "\.tsx" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - TypeScript or .ts/.tsx extensions not found"
    exit 1
fi

# Test 5: JavaScript with .js/.jsx extensions listed
echo -n "Test 5: JavaScript with .js/.jsx extensions listed... "
if grep -q "JavaScript" "$GUIDE" && grep -q "\.js" "$GUIDE" && grep -q "\.jsx" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - JavaScript or .js/.jsx extensions not found"
    exit 1
fi

# Test 6: Rust with .rs extension listed
echo -n "Test 6: Rust with .rs extension listed... "
if grep -q "Rust" "$GUIDE" && grep -q "\.rs" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Rust or .rs extension not found"
    exit 1
fi

# Test 7: Markdown with .md extension listed
echo -n "Test 7: Markdown with .md extension listed... "
if grep -q "Markdown" "$GUIDE" && grep -q "\.md" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Markdown or .md extension not found"
    exit 1
fi

# Test 8: Table format present (pipe delimiters)
echo -n "Test 8: Language table format with pipe delimiters... "
if grep -q "|.*Language\|Language.*|" "$GUIDE" && grep -q "|.*Extension\|Extensions.*|" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Table format with Language and Extension columns not found"
    exit 1
fi

# Test 9: Support status indicator present
echo -n "Test 9: Support status indicator present... "
if grep -qi "Supported" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Support status indicator not found"
    exit 1
fi

# Test 10: Unsupported language fallback statement
echo -n "Test 10: Unsupported language fallback statement present... "
if grep -qi "not supported\|unsupported\|not listed" "$GUIDE" && grep -qi "Grep.*fallback\|fallback.*Grep\|fall back" "$GUIDE"; then
    echo "PASS"
else
    echo "FAIL - Unsupported language fallback statement not found"
    exit 1
fi

echo ""
echo "=== AC#2 All Tests Passed ==="
exit 0
