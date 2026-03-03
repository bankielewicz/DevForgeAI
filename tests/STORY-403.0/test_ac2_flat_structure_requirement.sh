#!/bin/bash
# Test AC#2: Comment Explains Flat Structure Requirement
# STORY-403: Document Implementation Notes Format in Story Template
#
# Validates:
# - Comment explains DoD items must be placed DIRECTLY under ## header
# - Comment states NO ### subsection headers before DoD items
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
# Test 1: Comment contains "flat structure" or "DIRECTLY under" language
# -----------------------------------------------------------------------------
test_flat_structure_mentioned() {
    local test_name="Comment mentions flat structure or direct placement"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    # Get comment block boundaries
    local comment_start
    comment_start=$(grep -n '<!--.*IMPLEMENTATION NOTES FORMAT' "$TEMPLATE_FILE" | head -1 | cut -d: -f1)

    if [ -z "$comment_start" ]; then
        fail_test "$test_name" "Implementation Notes Format comment block not found"
        return
    fi

    # Find closing --> after comment_start
    local comment_end
    comment_end=$(sed -n "${comment_start},\$p" "$TEMPLATE_FILE" | grep -n '\-\->' | head -1 | cut -d: -f1)
    comment_end=$((comment_start + comment_end - 1))

    # Extract comment content and check for flat structure/DIRECTLY under
    local comment_content
    comment_content=$(sed -n "${comment_start},${comment_end}p" "$TEMPLATE_FILE")

    if echo "$comment_content" | grep -qi 'DIRECTLY under\|DIRECTLY under'; then
        pass_test "$test_name (found within comment lines $comment_start-$comment_end)"
    else
        fail_test "$test_name" "No mention of 'DIRECTLY under' within the Implementation Notes Format comment"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Comment warns against ### subsection headers
# -----------------------------------------------------------------------------
test_no_subsection_warning() {
    local test_name="Comment warns against ### subsection headers before DoD items"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    # Look for warning about ### headers in the context of DoD/Implementation Notes
    if grep -q 'NO ###\|no ### \|### subsection' "$TEMPLATE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No warning about ### subsection headers found in template"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Comment mentions DoD items placement requirement
# -----------------------------------------------------------------------------
test_dod_items_placement() {
    local test_name="Comment specifies DoD items must be under ## Implementation Notes"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    # Look for reference to DoD items under ## Implementation Notes
    if grep -q 'Implementation Notes' "$TEMPLATE_FILE" && grep -q 'DoD items\|DoD item' "$TEMPLATE_FILE"; then
        # Now check both are within the HTML comment area
        local comment_start
        comment_start=$(grep -n '<!--.*IMPLEMENTATION NOTES FORMAT' "$TEMPLATE_FILE" | head -1 | cut -d: -f1)

        if [ -n "$comment_start" ]; then
            local comment_end
            comment_end=$(sed -n "${comment_start},\$p" "$TEMPLATE_FILE" | grep -n '\-\->' | head -1 | cut -d: -f1)
            comment_end=$((comment_start + comment_end - 1))

            local dod_mention
            dod_mention=$(sed -n "${comment_start},${comment_end}p" "$TEMPLATE_FILE" | grep -c 'DoD items\|DoD item')

            if [ "$dod_mention" -gt 0 ]; then
                pass_test "$test_name"
            else
                fail_test "$test_name" "DoD items mentioned in template but not within the format comment"
            fi
        else
            fail_test "$test_name" "Implementation Notes Format comment block not found"
        fi
    else
        fail_test "$test_name" "No mention of DoD items or Implementation Notes in template context"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-403 AC#2: Flat Structure Requirement"
echo "=============================================="
echo "Target file: $TEMPLATE_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_flat_structure_mentioned
run_test "2" test_no_subsection_warning
run_test "3" test_dod_items_placement

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
