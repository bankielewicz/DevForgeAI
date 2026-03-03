#!/bin/bash
# Test AC#3: Comment References extract_section() Validator Behavior
# STORY-403: Document Implementation Notes Format in Story Template
#
# Validates:
# - Comment contains "extract_section" text
# - Comment explains that ### stops extraction
#
# Expected: FAIL initially (TDD Red phase - comment does not exist yet)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEMPLATE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md"

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $test_name"
}

fail_test() {
    local test_name="$1"
    local message="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $test_name: $message"
}

run_test() {
    local test_name="$1"
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# -----------------------------------------------------------------------------
# Test 1: Template contains "extract_section" text
# -----------------------------------------------------------------------------
test_extract_section_mentioned() {
    local test_name="Template contains 'extract_section' text"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    if grep -q 'extract_section' "$TEMPLATE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No mention of 'extract_section' found in template"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: extract_section mention is within an HTML comment
# -----------------------------------------------------------------------------
test_extract_section_in_comment() {
    local test_name="extract_section reference is within an HTML comment block"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    local comment_start
    comment_start=$(grep -n '<!--.*IMPLEMENTATION NOTES FORMAT' "$TEMPLATE_FILE" | head -1 | cut -d: -f1)

    if [ -z "$comment_start" ]; then
        fail_test "$test_name" "Implementation Notes Format comment block not found"
        return
    fi

    # Find the closing --> after the comment start
    local comment_end
    comment_end=$(sed -n "${comment_start},\$p" "$TEMPLATE_FILE" | grep -n '\-\->' | head -1 | cut -d: -f1)
    comment_end=$((comment_start + comment_end - 1))

    # Check if extract_section is within that range
    local extract_in_comment
    extract_in_comment=$(sed -n "${comment_start},${comment_end}p" "$TEMPLATE_FILE" | grep -c 'extract_section')

    if [ "$extract_in_comment" -gt 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "extract_section found in template but not within the format comment (lines $comment_start-$comment_end)"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Comment explains ### stops extraction
# -----------------------------------------------------------------------------
test_stops_at_hash_header() {
    local test_name="Comment explains ### stops extraction"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    # Look for explanation that ### header stops extraction
    if grep -q 'stops at.*###\|### header.*stop\|first ###' "$TEMPLATE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No explanation of ### stopping extraction behavior found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Comment explains consequence (items not found / commit blocked)
# -----------------------------------------------------------------------------
test_consequence_explained() {
    local test_name="Comment explains consequence of wrong format"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    # Look for explanation of what happens (cannot find, blocked, etc.)
    if grep -q 'cannot find\|commit blocked\|not found\|validator cannot' "$TEMPLATE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No explanation of consequence (items not found / commit blocked) in template"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-403 AC#3: extract_section() Reference"
echo "=============================================="
echo "Target file: $TEMPLATE_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_extract_section_mentioned
run_test "2" test_extract_section_in_comment
run_test "3" test_stops_at_hash_header
run_test "4" test_consequence_explained

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
