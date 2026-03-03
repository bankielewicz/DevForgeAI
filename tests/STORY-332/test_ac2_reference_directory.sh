#!/bin/bash
# Test: AC#2 - Reference Directory Structure
# Story: STORY-332 - Refactor session-miner.md with Progressive Disclosure
# Purpose: Verify references/ directory exists with 5-8 properly named files
#
# Expected: FAIL (Red phase) - Reference directory does not exist yet

# set -e  # Removed to allow all tests to run

# Configuration
REF_DIR="src/claude/agents/session-miner/references"
MIN_FILES=5
MAX_FILES=8

# Required reference files per Technical Specification
REQUIRED_FILES=(
    "parsing-workflow.md"
    "query-patterns.md"
    "output-formats.md"
    "error-handling.md"
    "session-analysis.md"
)

# Test tracking
TESTS_PASSED=0
TESTS_FAILED=0

echo "=============================================="
echo "  AC#2: Reference Directory Structure Tests"
echo "  STORY-332 - Progressive Disclosure Refactor"
echo "=============================================="
echo ""

# Test 1: Verify references directory exists
echo "Test 1: References directory exists"
if [[ -d "$REF_DIR" ]]; then
    echo "  PASS: $REF_DIR exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: $REF_DIR does not exist"
    echo "  Expected: Directory at $REF_DIR"
    ((TESTS_FAILED++))
    echo ""
    echo "=============================================="
    echo "  RESULT: $TESTS_PASSED passed, $TESTS_FAILED failed"
    echo "  STATUS: FAILED (cannot continue without directory)"
    echo "=============================================="
    exit 1
fi

# Test 2: Verify file count is between 5-8
echo ""
echo "Test 2: Reference file count is $MIN_FILES-$MAX_FILES"
FILE_COUNT=$(find "$REF_DIR" -maxdepth 1 -type f -name "*.md" | wc -l)
if [[ $FILE_COUNT -ge $MIN_FILES && $FILE_COUNT -le $MAX_FILES ]]; then
    echo "  PASS: Found $FILE_COUNT reference files ($MIN_FILES-$MAX_FILES expected)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Found $FILE_COUNT reference files"
    echo "  Expected: $MIN_FILES-$MAX_FILES files"
    ((TESTS_FAILED++))
fi

# Test 3: Verify required files exist
echo ""
echo "Test 3: Required reference files present"
REQUIRED_FOUND=0
MISSING_REQUIRED=()

for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "$REF_DIR/$file" ]]; then
        ((REQUIRED_FOUND++))
    else
        MISSING_REQUIRED+=("$file")
    fi
done

if [[ $REQUIRED_FOUND -eq ${#REQUIRED_FILES[@]} ]]; then
    echo "  PASS: All ${#REQUIRED_FILES[@]} required files present"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Only $REQUIRED_FOUND/${#REQUIRED_FILES[@]} required files found"
    echo "  Missing files:"
    for file in "${MISSING_REQUIRED[@]}"; do
        echo "    - $file"
    done
    ((TESTS_FAILED++))
fi

# Test 4: Verify all files use kebab-case naming
echo ""
echo "Test 4: All files use kebab-case naming"
INVALID_NAMES=()

for file in "$REF_DIR"/*.md; do
    if [[ -f "$file" ]]; then
        basename=$(basename "$file")
        # kebab-case pattern: lowercase letters, numbers, hyphens, ending in .md
        if ! [[ "$basename" =~ ^[a-z][a-z0-9-]*\.md$ ]]; then
            INVALID_NAMES+=("$basename")
        fi
    fi
done

if [[ ${#INVALID_NAMES[@]} -eq 0 ]]; then
    echo "  PASS: All files use kebab-case naming convention"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Files with invalid naming found"
    echo "  Invalid names (should be kebab-case):"
    for name in "${INVALID_NAMES[@]}"; do
        echo "    - $name"
    done
    ((TESTS_FAILED++))
fi

# Test 5: Verify each reference file has YAML frontmatter with parent field
echo ""
echo "Test 5: Reference files have parent: session-miner in frontmatter"
MISSING_PARENT=()

for file in "$REF_DIR"/*.md; do
    if [[ -f "$file" ]]; then
        basename=$(basename "$file")
        # Check for parent: session-miner in YAML frontmatter
        if ! grep -q "parent:.*session-miner" "$file"; then
            MISSING_PARENT+=("$basename")
        fi
    fi
done

if [[ ${#MISSING_PARENT[@]} -eq 0 ]]; then
    echo "  PASS: All reference files have parent: session-miner"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Files missing parent field in frontmatter"
    echo "  Missing parent: session-miner:"
    for name in "${MISSING_PARENT[@]}"; do
        echo "    - $name"
    done
    ((TESTS_FAILED++))
fi

# Test 6: List all reference files found
echo ""
echo "Test 6: Reference files inventory"
echo "  Files in $REF_DIR:"
for file in "$REF_DIR"/*.md; do
    if [[ -f "$file" ]]; then
        basename=$(basename "$file")
        lines=$(wc -l < "$file")
        echo "    - $basename ($lines lines)"
    fi
done
((TESTS_PASSED++))

# Summary
echo ""
echo "=============================================="
echo "  AC#2 TEST SUMMARY"
echo "=============================================="
echo "  Tests passed: $TESTS_PASSED"
echo "  Tests failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "  STATUS: PASSED - All AC#2 requirements met"
    exit 0
else
    echo "  STATUS: FAILED - $TESTS_FAILED requirement(s) not met"
    exit 1
fi
