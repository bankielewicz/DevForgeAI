#!/bin/bash
# Test AC#4: Comment References dod-update-workflow.md Full Path
# STORY-403: Document Implementation Notes Format in Story Template
#
# Validates:
# - Comment includes reference to dod-update-workflow.md
# - The reference includes the full path (not just filename)
#
# Expected: FAIL initially (TDD Red phase - comment does not exist yet)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEMPLATE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
EXPECTED_REF="dod-update-workflow.md"

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
# Test 1: Template contains "dod-update-workflow.md" reference
# -----------------------------------------------------------------------------
test_dod_workflow_reference_exists() {
    local test_name="Template contains dod-update-workflow.md reference"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    if grep -q "$EXPECTED_REF" "$TEMPLATE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No mention of '$EXPECTED_REF' found in template"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Reference includes directory path (not just filename)
# -----------------------------------------------------------------------------
test_full_path_reference() {
    local test_name="Reference includes full directory path"

    if [ ! -f "$TEMPLATE_FILE" ]; then
        fail_test "$test_name" "Template file not found"
        return
    fi

    # The full path should include the skill directory path
    local full_path_pattern="devforgeai-development/references/dod-update-workflow.md"

    if grep -q "$full_path_pattern" "$TEMPLATE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No full path reference matching '$full_path_pattern' found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Reference is within the Implementation Notes Format comment
# -----------------------------------------------------------------------------
test_reference_in_comment() {
    local test_name="dod-update-workflow.md reference is within HTML comment"

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

    # Find closing -->
    local comment_end
    comment_end=$(sed -n "${comment_start},\$p" "$TEMPLATE_FILE" | grep -n '\-\->' | head -1 | cut -d: -f1)
    comment_end=$((comment_start + comment_end - 1))

    # Check if dod-update-workflow.md is within that range
    local ref_in_comment
    ref_in_comment=$(sed -n "${comment_start},${comment_end}p" "$TEMPLATE_FILE" | grep -c "$EXPECTED_REF")

    if [ "$ref_in_comment" -gt 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "dod-update-workflow.md found in template but not within the format comment"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Referenced file actually exists
# -----------------------------------------------------------------------------
test_referenced_file_exists() {
    local test_name="Referenced dod-update-workflow.md file exists"

    local ref_file="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/dod-update-workflow.md"

    if [ -f "$ref_file" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Referenced file not found: $ref_file"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-403 AC#4: dod-update-workflow.md Reference"
echo "=============================================="
echo "Target file: $TEMPLATE_FILE"
echo "Expected reference: $EXPECTED_REF"
echo "----------------------------------------------"
echo ""

run_test "1" test_dod_workflow_reference_exists
run_test "2" test_full_path_reference
run_test "3" test_reference_in_comment
run_test "4" test_referenced_file_exists

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
