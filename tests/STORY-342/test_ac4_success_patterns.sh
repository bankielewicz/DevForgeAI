#!/bin/bash
# STORY-342 AC#4: success-patterns.md Created
# Tests that success-patterns.md exists with correct schema

set -e

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
SUCCESS_FILE="$PROJECT_ROOT/.claude/memory/learning/success-patterns.md"

echo "=== AC#4: success-patterns.md Tests ==="

# Test 1: File exists
echo -n "Test 1: success-patterns.md exists... "
if [ -f "$SUCCESS_FILE" ]; then
    echo "PASS"
else
    echo "FAIL - success-patterns.md not found at $SUCCESS_FILE"
    exit 1
fi

# Test 2: YAML frontmatter present
echo -n "Test 2: YAML frontmatter present... "
if head -1 "$SUCCESS_FILE" | grep -q "^---$"; then
    echo "PASS"
else
    echo "FAIL - File does not start with YAML frontmatter"
    exit 1
fi

# Test 3: Required field: last_updated
echo -n "Test 3: Required field 'last_updated' present... "
if grep -q "^last_updated:" "$SUCCESS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'last_updated' field in frontmatter"
    exit 1
fi

# Test 4: Required field: total_patterns
echo -n "Test 4: Required field 'total_patterns' present... "
if grep -q "^total_patterns:" "$SUCCESS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'total_patterns' field in frontmatter"
    exit 1
fi

# Test 5: Pattern schema - Occurrences field
echo -n "Test 5: Pattern schema includes 'Occurrences' field... "
if grep -qi "occurrences" "$SUCCESS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'Occurrences' field in pattern schema"
    exit 1
fi

# Test 6: Pattern schema - Confidence field
echo -n "Test 6: Pattern schema includes 'Confidence' field... "
if grep -qi "confidence" "$SUCCESS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'Confidence' field in pattern schema"
    exit 1
fi

# Test 7: Pattern schema - Examples field
echo -n "Test 7: Pattern schema includes 'Examples' field... "
if grep -qi "examples" "$SUCCESS_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'Examples' field in pattern schema"
    exit 1
fi

echo ""
echo "=== AC#4 Tests Complete: All PASSED ==="
