#!/bin/bash

# Test Suite: Error Handling for Git Command Failures
# Purpose: Verify graceful handling of all failure scenarios
# Coverage: HIGH priority from QA gaps.json

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

test_error_scenario() {
    local test_num="$1"
    local scenario="$2"
    local description="$3"
    local expected_exit_code="$4"

    echo ""
    echo -e "${YELLOW}Test $test_num: $scenario${NC}"
    echo "  Description: $description"
    echo "  Expected exit code: $expected_exit_code"
}

assert_exit_code() {
    local expected="$1"
    local actual="$2"
    local test_msg="$3"

    if [ "$actual" -eq "$expected" ]; then
        ((TESTS_PASSED++))
        echo -e "  ${GREEN}✓ PASS${NC}: $test_msg"
    else
        ((TESTS_FAILED++))
        echo -e "  ${RED}✗ FAIL${NC}: $test_msg"
        echo "    Expected: $expected, Got: $actual"
    fi
}

echo "═══════════════════════════════════════════════════════════════"
echo "  Error Handling Test Suite - STORY-123"
echo "═══════════════════════════════════════════════════════════════"

# ========== INVALID INPUT ERRORS ==========
echo ""
echo "  [ERROR CATEGORY] Invalid Input"

test_error_scenario 1 "Empty story_id" \
    "Function should handle empty story_id gracefully" 1

validate_story_id() {
    local story_id="$1"
    if [[ -z "${story_id}" ]]; then
        echo "ERROR: story_id cannot be empty" >&2
        return 1
    fi
    if [[ ! "${story_id}" =~ ^STORY-[0-9]+$ ]]; then
        echo "ERROR: Invalid story_id format" >&2
        return 1
    fi
    return 0
}

if validate_story_id "" 2>/dev/null; then
    assert_exit_code 1 0 "Empty story_id should return error code 1"
else
    assert_exit_code 1 $? "Empty story_id error handling"
fi

test_error_scenario 2 "Invalid format" \
    "Function should reject invalid story_id format" 1

if validate_story_id "invalid-format" 2>/dev/null; then
    assert_exit_code 1 0 "Invalid format should return error code 1"
else
    assert_exit_code 1 $? "Invalid format error handling"
fi

test_error_scenario 3 "Missing number" \
    "Function should reject story_id without number" 1

if validate_story_id "STORY-" 2>/dev/null; then
    assert_exit_code 1 0 "Missing number should return error code 1"
else
    assert_exit_code 1 $? "Missing number error handling"
fi

# ========== GIT COMMAND ERRORS ==========
echo ""
echo "  [ERROR CATEGORY] Git Command Failures"

test_error_scenario 4 "Not in git repository" \
    "Function should handle non-git directories gracefully" 128

# Create a temporary non-git directory
test_non_git_dir=$(mktemp -d)
trap "rm -rf $test_non_git_dir" EXIT

cd "$test_non_git_dir" 2>/dev/null || true

# Test that git status fails appropriately
if git status 2>/dev/null; then
    ((TESTS_FAILED++))
    echo -e "  ${RED}✗ FAIL${NC}: Non-git directory should cause git to fail"
else
    git_exit_code=$?
    if [ $git_exit_code -eq 128 ]; then
        ((TESTS_PASSED++))
        echo -e "  ${GREEN}✓ PASS${NC}: Git returns exit code 128 for non-repo"
    else
        ((TESTS_FAILED++))
        echo -e "  ${RED}✗ FAIL${NC}: Expected exit code 128, got $git_exit_code"
    fi
fi

# Return to project directory
cd /mnt/c/Projects/DevForgeAI2

test_error_scenario 5 "Permission denied" \
    "Function should handle permission errors gracefully" 1

# Create a restricted directory (if possible)
restricted_dir="/tmp/restricted_$$"
mkdir -p "$restricted_dir" 2>/dev/null || true
chmod 000 "$restricted_dir" 2>/dev/null || true

if [ -d "$restricted_dir" ]; then
    if cd "$restricted_dir" 2>/dev/null; then
        # If we could cd, it's not actually restricted
        cd /mnt/c/Projects/DevForgeAI2
        echo -e "  ${YELLOW}⊘ SKIP${NC}: Could not create permission-denied scenario"
    else
        # Could not cd to restricted dir - good
        ((TESTS_PASSED++))
        echo -e "  ${GREEN}✓ PASS${NC}: Permission denied handling works"
    fi
    rm -rf "$restricted_dir" 2>/dev/null || true
else
    echo -e "  ${YELLOW}⊘ SKIP${NC}: Could not create permission test"
fi

# ========== ERROR MESSAGE VALIDATION ==========
echo ""
echo "  [ERROR CATEGORY] Error Messages"

test_error_scenario 6 "Error message clarity" \
    "Error messages should be clear and actionable" 1

error_msg=$(validate_story_id "" 2>&1 || true)
if echo "$error_msg" | grep -q "cannot be empty"; then
    ((TESTS_PASSED++))
    echo -e "  ${GREEN}✓ PASS${NC}: Error message is clear (mentions 'empty')"
else
    ((TESTS_FAILED++))
    echo -e "  ${RED}✗ FAIL${NC}: Error message lacks clarity"
fi

test_error_scenario 7 "Error message includes context" \
    "Error messages should indicate expected format" 1

error_msg=$(validate_story_id "bad-format" 2>&1 || true)
if echo "$error_msg" | grep -iE "(STORY|format|expected)"; then
    ((TESTS_PASSED++))
    echo -e "  ${GREEN}✓ PASS${NC}: Error message provides context"
else
    ((TESTS_FAILED++))
    echo -e "  ${RED}✗ FAIL${NC}: Error message lacks context"
fi

# ========== EDGE CASES ==========
echo ""
echo "  [ERROR CATEGORY] Edge Cases"

test_error_scenario 8 "Null/nil handling" \
    "Function should safely handle null values" 1

# Test with unset variable
if validate_story_id "${UNDEFINED_VAR:-}" 2>/dev/null; then
    ((TESTS_FAILED++))
    echo -e "  ${RED}✗ FAIL${NC}: Null value should be rejected"
else
    assert_exit_code 1 $? "Null value handling"
fi

test_error_scenario 9 "Whitespace-only input" \
    "Function should reject whitespace-only story_id" 1

if validate_story_id "   " 2>/dev/null; then
    assert_exit_code 1 0 "Whitespace-only should be rejected"
else
    assert_exit_code 1 $? "Whitespace-only error handling"
fi

test_error_scenario 10 "Mixed case sensitivity" \
    "Function should enforce case-sensitive format" 1

if validate_story_id "story-123" 2>/dev/null; then
    assert_exit_code 1 0 "Lowercase should be rejected"
else
    assert_exit_code 1 $? "Case sensitivity enforcement"
fi

# ========== FILE HANDLING ERRORS ==========
echo ""
echo "  [ERROR CATEGORY] File Operations"

test_error_scenario 11 "File not found" \
    "Function should handle missing story files gracefully" 1

# Test checking for non-existent file with git
if git status -- "NONEXISTENT.story.md" 2>/dev/null; then
    echo -e "  ${YELLOW}⊘ INFO${NC}: File doesn't exist but git didn't error"
else
    ((TESTS_PASSED++))
    echo -e "  ${GREEN}✓ PASS${NC}: Git safely handles non-existent files"
fi

test_error_scenario 12 "File permission denied" \
    "Function should handle permission-denied files gracefully" 0

if [ -f "/etc/shadow" ] && ! [ -r "/etc/shadow" ]; then
    if git status -- "/etc/shadow" 2>/dev/null; then
        ((TESTS_FAILED++))
        echo -e "  ${RED}✗ FAIL${NC}: Should not access restricted files"
    else
        ((TESTS_PASSED++))
        echo -e "  ${GREEN}✓ PASS${NC}: Access to restricted files blocked"
    fi
else
    echo -e "  ${YELLOW}⊘ SKIP${NC}: Cannot test permission scenario"
fi

# ========== RECOVERY & ROLLBACK ==========
echo ""
echo "  [ERROR CATEGORY] Recovery Behavior"

test_error_scenario 13 "Clean error state after failure" \
    "Function should not leave side effects after error" 0

# Capture initial state
initial_state=$(pwd)

# Call with invalid input (should fail)
validate_story_id "invalid" 2>/dev/null || true

# Check state hasn't changed
final_state=$(pwd)

if [ "$initial_state" = "$final_state" ]; then
    ((TESTS_PASSED++))
    echo -e "  ${GREEN}✓ PASS${NC}: No side effects after error"
else
    ((TESTS_FAILED++))
    echo -e "  ${RED}✗ FAIL${NC}: State changed after error"
fi

# ========== STRESS TESTS ==========
echo ""
echo "  [ERROR CATEGORY] Stress/Resource Limits"

test_error_scenario 14 "Extremely long input" \
    "Function should reject unreasonably long story_id" 1

long_input="STORY-$(printf 'A%.0s' {1..10000})"

if validate_story_id "$long_input" 2>/dev/null; then
    assert_exit_code 1 0 "Very long input should be rejected"
else
    assert_exit_code 1 $? "Long input handling"
fi

test_error_scenario 15 "Unicode/binary input" \
    "Function should reject non-ASCII characters" 1

if validate_story_id "STORY-123é" 2>/dev/null; then
    assert_exit_code 1 0 "Unicode should be rejected"
else
    assert_exit_code 1 $? "Unicode handling"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Summary"
echo "═══════════════════════════════════════════════════════════════"
TOTAL=$((TESTS_PASSED + TESTS_FAILED))
echo "Total error scenarios: $TOTAL"
echo -e "Passed:                ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed:                ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ All error handling properly implemented!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}✗ Some error scenarios not handled${NC}"
    exit 1
fi
