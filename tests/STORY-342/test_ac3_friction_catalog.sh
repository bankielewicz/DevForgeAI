#!/bin/bash
# STORY-342 AC#3: friction-catalog.md Created
# Tests that friction-catalog.md exists with correct schema

set -e

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
FRICTION_FILE="$PROJECT_ROOT/.claude/memory/learning/friction-catalog.md"

echo "=== AC#3: friction-catalog.md Tests ==="

# Test 1: File exists
echo -n "Test 1: friction-catalog.md exists... "
if [ -f "$FRICTION_FILE" ]; then
    echo "PASS"
else
    echo "FAIL - friction-catalog.md not found at $FRICTION_FILE"
    exit 1
fi

# Test 2: YAML frontmatter present
echo -n "Test 2: YAML frontmatter present... "
if head -1 "$FRICTION_FILE" | grep -q "^---$"; then
    echo "PASS"
else
    echo "FAIL - File does not start with YAML frontmatter"
    exit 1
fi

# Test 3: Required field: last_updated
echo -n "Test 3: Required field 'last_updated' present... "
if grep -q "^last_updated:" "$FRICTION_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'last_updated' field in frontmatter"
    exit 1
fi

# Test 4: Required field: total_frictions
echo -n "Test 4: Required field 'total_frictions' present... "
if grep -q "^total_frictions:" "$FRICTION_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'total_frictions' field in frontmatter"
    exit 1
fi

# Test 5: Friction schema - friction_id field
echo -n "Test 5: Friction schema supports 'friction_id' field... "
if grep -qi "friction.id\|friction_id" "$FRICTION_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'friction_id' schema field"
    exit 1
fi

# Test 6: Friction schema - root_cause field
echo -n "Test 6: Friction schema supports 'root_cause' field... "
if grep -qi "root.cause\|root_cause" "$FRICTION_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'root_cause' schema field"
    exit 1
fi

# Test 7: Friction schema - solution field
echo -n "Test 7: Friction schema supports 'solution' field... "
if grep -qi "solution" "$FRICTION_FILE"; then
    echo "PASS"
else
    echo "FAIL - Missing 'solution' schema field"
    exit 1
fi

echo ""
echo "=== AC#3 Tests Complete: All PASSED ==="
