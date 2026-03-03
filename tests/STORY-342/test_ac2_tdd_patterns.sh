#!/bin/bash
# STORY-342 AC#2: tdd-patterns.md Created
# Tests that tdd-patterns.md exists with correct schema

set -e

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
TDD_PATTERNS_FILE="$PROJECT_ROOT/.claude/memory/learning/tdd-patterns.md"

echo "=== AC#2: tdd-patterns.md Tests ==="

# Test 1: File exists
echo -n "Test 1: tdd-patterns.md exists... "
if [ -f "$TDD_PATTERNS_FILE" ]; then
    echo "PASS"
else
    echo "FAIL - tdd-patterns.md not found at $TDD_PATTERNS_FILE"
    exit 1
fi

# Test 2: YAML frontmatter present
echo -n "Test 2: YAML frontmatter present (starts with ---)... "
if head -1 "$TDD_PATTERNS_FILE" | grep -q "^---$"; then
    echo "PASS"
else
    echo "FAIL - File does not start with YAML frontmatter"
    exit 1
fi

# Test 3: Required field: last_updated
echo -n "Test 3: Required field 'last_updated' present... "
if grep -q "^last_updated:" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'last_updated' field in frontmatter"
    exit 1
fi

# Test 4: Required field: total_patterns
echo -n "Test 4: Required field 'total_patterns' present... "
if grep -q "^total_patterns:" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'total_patterns' field in frontmatter"
    exit 1
fi

# Test 5: Required field: version
echo -n "Test 5: Required field 'version' present... "
if grep -q "^version:" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'version' field in frontmatter"
    exit 1
fi

# Test 6: Pattern schema - Occurrences field
echo -n "Test 6: Pattern schema includes 'Occurrences' field... "
if grep -q "Occurrences:" "$TDD_PATTERNS_FILE" || grep -q "occurrences:" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'Occurrences' field in pattern schema"
    exit 1
fi

# Test 7: Pattern schema - Confidence field
echo -n "Test 7: Pattern schema includes 'Confidence' field... "
if grep -q "Confidence:" "$TDD_PATTERNS_FILE" || grep -q "confidence:" "$TDD_PATTERNS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'Confidence' field in pattern schema"
    exit 1
fi

echo ""
echo "=== AC#2 Tests Complete: All PASSED ==="
