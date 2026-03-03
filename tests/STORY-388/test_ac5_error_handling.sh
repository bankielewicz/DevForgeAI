#!/bin/bash
# Test AC#5: Error Handling Patterns Included
# STORY-388: Design Command Template Variant with 15K Char Budget Compliance
#
# Validates:
# - Error Handling section has 3-5 error categories
# - Required categories: argument validation, context file, skill invocation,
#   resource not found, unexpected error
# - Each category has: detection pattern, user message, recovery action
# - Note that complex recovery belongs in skills
#
# Expected: FAIL initially (TDD Red phase - file does not exist yet)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEMPLATE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $1"
}

fail_test() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $1: $2"
}

run_test() {
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# ---------------------------------------------------------------------------
# Test 1: Error Handling section exists
# ---------------------------------------------------------------------------
test_error_section_exists() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Error Handling section" "File does not exist"
        return
    fi

    if grep -qE "^#+ .*Error Handling" "$TEMPLATE"; then
        pass_test "Error Handling section found"
    else
        fail_test "Error Handling section" "Heading not found"
    fi
}

# ---------------------------------------------------------------------------
# Test 2: 3-5 error categories present
# ---------------------------------------------------------------------------
test_error_category_count() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Error category count" "File does not exist"
        return
    fi

    local error_section
    error_section=$(sed -n '/^#\+ .*Error Handling/,/^#\+ /p' "$TEMPLATE")

    if [ -z "$error_section" ]; then
        fail_test "Error category count" "Cannot extract Error Handling section"
        return
    fi

    # Count sub-headings or bold category labels within error section
    local cat_count
    cat_count=$(echo "$error_section" | grep -cE "^###|^\*\*[A-Z]" || true)

    if [ "$cat_count" -ge 3 ] && [ "$cat_count" -le 5 ]; then
        pass_test "Error categories: $cat_count (within 3-5 range)"
    else
        fail_test "Error category count" "Found $cat_count categories (expected 3-5)"
    fi
}

# ---------------------------------------------------------------------------
# Test 3: Argument validation error category
# ---------------------------------------------------------------------------
test_argument_validation_error() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Argument validation error" "File does not exist"
        return
    fi

    if grep -qiE "argument.*valid|invalid.*argument|validation.*fail" "$TEMPLATE"; then
        pass_test "Argument validation error category found"
    else
        fail_test "Argument validation error" "No argument validation error pattern"
    fi
}

# ---------------------------------------------------------------------------
# Test 4: Context file / skill invocation errors referenced
# ---------------------------------------------------------------------------
test_context_skill_errors() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Context/skill errors" "File does not exist"
        return
    fi

    local found=0
    if grep -qi "context.*not found\|context file" "$TEMPLATE"; then
        found=$((found + 1))
    fi
    if grep -qi "skill.*invocation\|skill.*fail" "$TEMPLATE"; then
        found=$((found + 1))
    fi

    if [ "$found" -ge 2 ]; then
        pass_test "Context file and skill invocation errors referenced"
    elif [ "$found" -eq 1 ]; then
        fail_test "Context/skill errors" "Only 1 of 2 required error types found"
    else
        fail_test "Context/skill errors" "Neither context nor skill error types found"
    fi
}

# ---------------------------------------------------------------------------
# Test 5: Recovery action guidance present
# ---------------------------------------------------------------------------
test_recovery_actions() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Recovery actions" "File does not exist"
        return
    fi

    if grep -qiE "recover|resolution|action|fix|remedy|remediat" "$TEMPLATE"; then
        pass_test "Recovery action guidance found"
    else
        fail_test "Recovery actions" "No recovery action language found"
    fi
}

# ---------------------------------------------------------------------------
# Test 6: Complex recovery belongs in skills note
# ---------------------------------------------------------------------------
test_recovery_in_skills_note() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Recovery in skills note" "File does not exist"
        return
    fi

    if grep -qiE "recovery.*skill|complex.*skill|skill.*not.*command" "$TEMPLATE"; then
        pass_test "Complex recovery belongs in skills note found"
    else
        fail_test "Recovery in skills note" "No note about complex recovery in skills"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
echo "=============================================="
echo "STORY-388 AC#5: Error Handling Patterns"
echo "=============================================="
echo "Target: $TEMPLATE"
echo "----------------------------------------------"
echo ""

run_test "1" test_error_section_exists
run_test "2" test_error_category_count
run_test "3" test_argument_validation_error
run_test "4" test_context_skill_errors
run_test "5" test_recovery_actions
run_test "6" test_recovery_in_skills_note

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
