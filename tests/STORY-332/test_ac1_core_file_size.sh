#!/bin/bash
# Test: AC#1 - Core File Size Compliance
# Story: STORY-332 - Refactor session-miner.md with Progressive Disclosure
# Purpose: Verify core file is <=300 lines with 8 required sections
#
# Expected: PASS (Green phase) - Refactored file meets all requirements

# Note: Removed set -e to allow all tests to run and report failures at the end

# Configuration
CORE_FILE="src/claude/agents/session-miner.md"
MAX_LINES=300
REQUIRED_SECTIONS=(
    "^---$"                      # YAML frontmatter start
    "^## Purpose"                # Purpose section
    "^## When Invoked"           # When Invoked section
    "^## Core Workflow"          # Core Workflow section (or Workflow)
    "^## Success Criteria"       # Success Criteria section
    "^## Error Handling"         # Error Handling section
    "^## Reference Loading"      # Reference Loading section
    "^## Observation Capture"    # Observation Capture section (allows MANDATORY suffix)
)
SECTION_NAMES=(
    "YAML frontmatter"
    "Purpose"
    "When Invoked"
    "Core Workflow"
    "Success Criteria"
    "Error Handling"
    "Reference Loading"
    "Observation Capture"
)

# Test tracking
TESTS_PASSED=0
TESTS_FAILED=0

echo "=============================================="
echo "  AC#1: Core File Size Compliance Tests"
echo "  STORY-332 - Progressive Disclosure Refactor"
echo "=============================================="
echo ""

# Test 1: Verify core file exists
echo "Test 1: Core file exists"
if [[ -f "$CORE_FILE" ]]; then
    echo "  PASS: $CORE_FILE exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: $CORE_FILE does not exist"
    echo "  Expected: File exists at $CORE_FILE"
    ((TESTS_FAILED++))
    echo ""
    echo "=============================================="
    echo "  RESULT: $TESTS_PASSED passed, $TESTS_FAILED failed"
    echo "  STATUS: FAILED (cannot continue without file)"
    echo "=============================================="
    exit 1
fi

# Test 2: Verify line count <= 300
echo ""
echo "Test 2: Line count <= $MAX_LINES"
LINE_COUNT=$(wc -l < "$CORE_FILE")
if [[ $LINE_COUNT -le $MAX_LINES ]]; then
    echo "  PASS: Core file has $LINE_COUNT lines (<= $MAX_LINES)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Core file has $LINE_COUNT lines (exceeds $MAX_LINES)"
    echo "  Expected: <= $MAX_LINES lines"
    echo "  Actual: $LINE_COUNT lines"
    echo "  Overage: $((LINE_COUNT - MAX_LINES)) lines"
    ((TESTS_FAILED++))
fi

# Test 3: Verify 8 required sections present
echo ""
echo "Test 3: All 8 required sections present"
SECTIONS_FOUND=0
MISSING_SECTIONS=()

for i in "${!REQUIRED_SECTIONS[@]}"; do
    pattern="${REQUIRED_SECTIONS[$i]}"
    name="${SECTION_NAMES[$i]}"

    if grep -qE "$pattern" "$CORE_FILE"; then
        ((SECTIONS_FOUND++))
    else
        MISSING_SECTIONS+=("$name")
    fi
done

if [[ $SECTIONS_FOUND -eq 8 ]]; then
    echo "  PASS: All 8 required sections found"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Only $SECTIONS_FOUND/8 required sections found"
    echo "  Missing sections:"
    for section in "${MISSING_SECTIONS[@]}"; do
        echo "    - $section"
    done
    ((TESTS_FAILED++))
fi

# Test 4: Verify YAML frontmatter has required fields
echo ""
echo "Test 4: YAML frontmatter contains required fields"
YAML_FIELDS=("name:" "description:" "tools:" "model:" "proactive_triggers:")
YAML_FOUND=0
MISSING_YAML=()

for field in "${YAML_FIELDS[@]}"; do
    if grep -q "^$field" "$CORE_FILE" || grep -q "^  $field" "$CORE_FILE"; then
        ((YAML_FOUND++))
    else
        MISSING_YAML+=("$field")
    fi
done

if [[ $YAML_FOUND -eq ${#YAML_FIELDS[@]} ]]; then
    echo "  PASS: All YAML frontmatter fields present"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Missing YAML frontmatter fields"
    for field in "${MISSING_YAML[@]}"; do
        echo "    - $field"
    done
    ((TESTS_FAILED++))
fi

# Test 5: Verify character count (NFR-001: <= 12,000 characters)
echo ""
echo "Test 5: Character count <= 12,000 (token efficiency)"
CHAR_COUNT=$(wc -c < "$CORE_FILE")
if [[ $CHAR_COUNT -le 12000 ]]; then
    echo "  PASS: Core file has $CHAR_COUNT characters (<= 12,000)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Core file has $CHAR_COUNT characters (exceeds 12,000)"
    echo "  Expected: <= 12,000 characters for 60%+ token reduction"
    echo "  Actual: $CHAR_COUNT characters"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "=============================================="
echo "  AC#1 TEST SUMMARY"
echo "=============================================="
echo "  Tests passed: $TESTS_PASSED"
echo "  Tests failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "  STATUS: PASSED - All AC#1 requirements met"
    exit 0
else
    echo "  STATUS: FAILED - $TESTS_FAILED requirement(s) not met"
    exit 1
fi
