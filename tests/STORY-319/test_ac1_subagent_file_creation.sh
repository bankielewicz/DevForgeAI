#!/bin/bash
# STORY-319 AC#1: Subagent File Creation
# Tests that observation-extractor.md exists with valid YAML frontmatter
# Expected: FAIL (file does not exist yet - TDD Red phase)

set -e

SUBAGENT_FILE=".claude/agents/observation-extractor.md"
SOURCE_FILE="src/claude/agents/observation-extractor.md"

echo "=== AC#1: Subagent File Creation Tests ==="

# Test 1.1: Source file exists
echo -n "Test 1.1: Source file exists at $SOURCE_FILE... "
if [ -f "$SOURCE_FILE" ]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: File exists at $SOURCE_FILE"
    exit 1
fi

# Test 1.2: Operational file exists (mirror)
echo -n "Test 1.2: Operational file exists at $SUBAGENT_FILE... "
if [ -f "$SUBAGENT_FILE" ]; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: File exists at $SUBAGENT_FILE"
    exit 1
fi

# Test 1.3: YAML frontmatter has 'name' field
echo -n "Test 1.3: YAML frontmatter contains 'name' field... "
if grep -q "^name:" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: YAML frontmatter with 'name:' field"
    exit 1
fi

# Test 1.4: YAML frontmatter has 'description' field
echo -n "Test 1.4: YAML frontmatter contains 'description' field... "
if grep -q "^description:" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: YAML frontmatter with 'description:' field"
    exit 1
fi

# Test 1.5: YAML frontmatter has 'tools' field
echo -n "Test 1.5: YAML frontmatter contains 'tools' field... "
if grep -q "^tools:" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: YAML frontmatter with 'tools:' field"
    exit 1
fi

# Test 1.6: YAML frontmatter has 'model' field
echo -n "Test 1.6: YAML frontmatter contains 'model' field... "
if grep -q "^model:" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: YAML frontmatter with 'model:' field"
    exit 1
fi

# Test 1.7: Source and operational files match
echo -n "Test 1.7: Source and operational files are identical... "
if diff -q "$SOURCE_FILE" "$SUBAGENT_FILE" > /dev/null 2>&1; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: $SOURCE_FILE and $SUBAGENT_FILE to be identical"
    exit 1
fi

echo ""
echo "=== AC#1: All tests passed ==="
exit 0
