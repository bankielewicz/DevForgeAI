#!/bin/bash
# STORY-333 AC#2: Reference Directory Structure
# Tests that references/ directory exists with 6-8 files using lowercase-hyphen naming
# TDD Red Phase: These tests FAIL until implementation complete

set -e
REF_DIR="src/claude/agents/test-automator/references"
MIN_FILES=6
MAX_FILES=8

echo "=== AC#2: Reference Directory Structure ==="

# Test 1: Reference directory exists
echo -n "Test 1: Reference directory exists... "
if [ ! -d "$REF_DIR" ]; then
    echo "FAIL (directory not found: $REF_DIR)"
    exit 1
fi
echo "PASS"

# Test 2: File count between 6-8
echo -n "Test 2: File count between $MIN_FILES-$MAX_FILES... "
FILE_COUNT=$(find "$REF_DIR" -maxdepth 1 -name "*.md" -type f | wc -l)
if [ "$FILE_COUNT" -lt "$MIN_FILES" ] || [ "$FILE_COUNT" -gt "$MAX_FILES" ]; then
    echo "FAIL (got $FILE_COUNT files)"
    exit 1
fi
echo "PASS ($FILE_COUNT files)"

# Test 3: All files use lowercase-hyphen naming
echo -n "Test 3: Lowercase-hyphen naming convention... "
INVALID=$(find "$REF_DIR" -maxdepth 1 -name "*.md" -type f | xargs -I{} basename {} | grep -vE '^[a-z][a-z0-9-]*\.md$' || true)
if [ -n "$INVALID" ]; then
    echo "FAIL (invalid names: $INVALID)"
    exit 1
fi
echo "PASS"

# Test 4-9: Required reference files
REQUIRED_FILES=(
    "framework-patterns.md"
    "remediation-mode.md"
    "exception-path-coverage.md"
    "technical-specification.md"
    "common-patterns.md"
    "coverage-optimization.md"
)

for i in "${!REQUIRED_FILES[@]}"; do
    FILE="${REQUIRED_FILES[$i]}"
    TEST_NUM=$((i + 4))
    echo -n "Test $TEST_NUM: File '$FILE' exists... "
    if [ ! -f "$REF_DIR/$FILE" ]; then
        echo "FAIL"
        exit 1
    fi
    echo "PASS"
done

echo ""
echo "AC#2: All tests PASSED"
