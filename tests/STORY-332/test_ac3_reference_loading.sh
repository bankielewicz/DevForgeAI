#!/bin/bash
# Test: AC#3 - Reference Loading Instructions
# Story: STORY-332 - Refactor session-miner.md with Progressive Disclosure
# Purpose: Verify core file has Reference Loading section with Read() calls
#
# Expected: FAIL (Red phase) - Refactored file does not exist yet

# set -e  # Removed to allow all tests to run

# Configuration
CORE_FILE="src/claude/agents/session-miner.md"
REF_PATH_PREFIX="src/claude/agents/session-miner/references/"

# Major features that need Read() instructions
REQUIRED_FEATURES=(
    "parsing"
    "error"
    "analysis"
    "pattern"
)

# Test tracking
TESTS_PASSED=0
TESTS_FAILED=0

echo "=============================================="
echo "  AC#3: Reference Loading Instructions Tests"
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
    ((TESTS_FAILED++))
    echo ""
    echo "=============================================="
    echo "  RESULT: $TESTS_PASSED passed, $TESTS_FAILED failed"
    echo "  STATUS: FAILED (cannot continue without file)"
    echo "=============================================="
    exit 1
fi

# Test 2: Verify Reference Loading section exists
echo ""
echo "Test 2: Reference Loading section exists"
if grep -qE "^## Reference Loading" "$CORE_FILE"; then
    echo "  PASS: '## Reference Loading' section found"
    ((TESTS_PASSED++))
else
    echo "  FAIL: '## Reference Loading' section not found"
    echo "  Expected: Section header '## Reference Loading'"
    ((TESTS_FAILED++))
fi

# Test 3: Verify Read() calls are present
echo ""
echo "Test 3: Read() function calls present"
READ_CALLS=$(grep -c 'Read(file_path=' "$CORE_FILE" 2>/dev/null || echo "0")
if [[ $READ_CALLS -ge 5 ]]; then
    echo "  PASS: Found $READ_CALLS Read() calls (>= 5 expected)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Only $READ_CALLS Read() calls found"
    echo "  Expected: >= 5 Read() calls for reference files"
    ((TESTS_FAILED++))
fi

# Test 4: Verify Read() calls use correct path prefix
echo ""
echo "Test 4: Read() calls use correct reference path"
CORRECT_PATHS=$(grep -c "Read(file_path=\"$REF_PATH_PREFIX" "$CORE_FILE" 2>/dev/null || echo "0")
if [[ $CORRECT_PATHS -ge 5 ]]; then
    echo "  PASS: Found $CORRECT_PATHS Read() calls with correct path prefix"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Only $CORRECT_PATHS Read() calls with correct path"
    echo "  Expected path prefix: $REF_PATH_PREFIX"
    ((TESTS_FAILED++))
fi

# Test 5: Verify major features have Read() instructions
echo ""
echo "Test 5: Major features have Read() instructions"
FEATURES_FOUND=0
MISSING_FEATURES=()

for feature in "${REQUIRED_FEATURES[@]}"; do
    # Check for Read() call that mentions this feature
    if grep -qiE "Read\(file_path=.*$feature" "$CORE_FILE"; then
        ((FEATURES_FOUND++))
    else
        MISSING_FEATURES+=("$feature")
    fi
done

if [[ $FEATURES_FOUND -eq ${#REQUIRED_FEATURES[@]} ]]; then
    echo "  PASS: All ${#REQUIRED_FEATURES[@]} major features have Read() instructions"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Only $FEATURES_FOUND/${#REQUIRED_FEATURES[@]} features have Read()"
    echo "  Missing Read() for features:"
    for feature in "${MISSING_FEATURES[@]}"; do
        echo "    - $feature"
    done
    ((TESTS_FAILED++))
fi

# Test 6: Verify on-demand loading pattern documented
echo ""
echo "Test 6: On-demand loading pattern documented"
if grep -qiE "(on.?demand|load.*when.*needed|progressive.*disclosure)" "$CORE_FILE"; then
    echo "  PASS: On-demand loading pattern documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: On-demand loading pattern not documented"
    echo "  Expected: Documentation explaining when to load references"
    ((TESTS_FAILED++))
fi

# Test 7: List all Read() calls found
echo ""
echo "Test 7: Read() calls inventory"
echo "  Read() calls in core file:"
grep -n 'Read(file_path=' "$CORE_FILE" 2>/dev/null | head -20 | while read -r line; do
    echo "    $line"
done
((TESTS_PASSED++))

# Summary
echo ""
echo "=============================================="
echo "  AC#3 TEST SUMMARY"
echo "=============================================="
echo "  Tests passed: $TESTS_PASSED"
echo "  Tests failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "  STATUS: PASSED - All AC#3 requirements met"
    exit 0
else
    echo "  STATUS: FAILED - $TESTS_FAILED requirement(s) not met"
    exit 1
fi
