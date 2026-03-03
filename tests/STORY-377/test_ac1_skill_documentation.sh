#!/bin/bash
# Test AC#1: SKILL.md Documents Treelint Integration
# STORY-377: Update devforgeai-development Skill for Treelint
#
# Validates:
# - SKILL.md contains "## Treelint Integration" section heading
# - Section lists 4 subagents (test-automator, backend-architect, refactoring-specialist, code-reviewer)
# - Section mentions token reduction benefit (40-80%)
# - Section references shared Treelint reference file path
# - SKILL.md size increase stays under 2000 characters for the addition
#
# Expected: FAIL initially (TDD Red phase - SKILL.md has no Treelint Integration section)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/SKILL.md"

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
# Test 1: SKILL.md file exists
# -----------------------------------------------------------------------------
test_skill_file_exists() {
    local test_name="SKILL.md file exists"
    if [ -f "$SKILL_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $SKILL_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Contains "## Treelint Integration" section heading
# -----------------------------------------------------------------------------
test_treelint_integration_heading() {
    local test_name="Contains Treelint Integration section heading"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q "^## Treelint Integration" "$SKILL_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No '## Treelint Integration' heading found in SKILL.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Lists test-automator subagent
# -----------------------------------------------------------------------------
test_lists_test_automator() {
    local test_name="Treelint section lists test-automator subagent"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Extract content from Treelint Integration section to next ## heading
    local section_content
    section_content=$(sed -n '/^## Treelint Integration/,/^## /p' "$SKILL_FILE" | head -n -1)

    if echo "$section_content" | grep -q "test-automator"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "test-automator not mentioned in Treelint Integration section"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Lists backend-architect subagent
# -----------------------------------------------------------------------------
test_lists_backend_architect() {
    local test_name="Treelint section lists backend-architect subagent"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local section_content
    section_content=$(sed -n '/^## Treelint Integration/,/^## /p' "$SKILL_FILE" | head -n -1)

    if echo "$section_content" | grep -q "backend-architect"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "backend-architect not mentioned in Treelint Integration section"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Lists refactoring-specialist subagent
# -----------------------------------------------------------------------------
test_lists_refactoring_specialist() {
    local test_name="Treelint section lists refactoring-specialist subagent"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local section_content
    section_content=$(sed -n '/^## Treelint Integration/,/^## /p' "$SKILL_FILE" | head -n -1)

    if echo "$section_content" | grep -q "refactoring-specialist"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "refactoring-specialist not mentioned in Treelint Integration section"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Lists code-reviewer subagent
# -----------------------------------------------------------------------------
test_lists_code_reviewer() {
    local test_name="Treelint section lists code-reviewer subagent"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local section_content
    section_content=$(sed -n '/^## Treelint Integration/,/^## /p' "$SKILL_FILE" | head -n -1)

    if echo "$section_content" | grep -q "code-reviewer"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "code-reviewer not mentioned in Treelint Integration section"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Mentions token reduction benefit (40-80%)
# -----------------------------------------------------------------------------
test_mentions_token_reduction() {
    local test_name="Treelint section mentions token reduction benefit"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local section_content
    section_content=$(sed -n '/^## Treelint Integration/,/^## /p' "$SKILL_FILE" | head -n -1)

    # Check for token reduction percentage pattern (40-80%, or similar range)
    if echo "$section_content" | grep -qE "(40-80%|token.*(reduction|saving|efficiency))"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No token reduction benefit (40-80%) mentioned in Treelint Integration section"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: References shared Treelint reference file path
# -----------------------------------------------------------------------------
test_references_shared_file_path() {
    local test_name="Treelint section references shared reference file path"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local section_content
    section_content=$(sed -n '/^## Treelint Integration/,/^## /p' "$SKILL_FILE" | head -n -1)

    # Check for reference to shared treelint patterns file
    if echo "$section_content" | grep -q "treelint-search-patterns"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No reference to treelint-search-patterns file found in Treelint Integration section"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Treelint Integration section size under 2000 characters
# -----------------------------------------------------------------------------
test_section_size_limit() {
    local test_name="Treelint Integration section under 2000 characters"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local section_content
    section_content=$(sed -n '/^## Treelint Integration/,/^## /p' "$SKILL_FILE" | head -n -1)

    if [ -z "$section_content" ]; then
        fail_test "$test_name" "Treelint Integration section not found"
        return
    fi

    local char_count
    char_count=$(echo "$section_content" | wc -c)

    if [ "$char_count" -le 2000 ]; then
        pass_test "$test_name (actual: $char_count chars)"
    else
        fail_test "$test_name" "Section has $char_count characters (max: 2000)"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-377 AC#1: SKILL.md Treelint Integration"
echo "=============================================="
echo "Target file: $SKILL_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_skill_file_exists
run_test "2" test_treelint_integration_heading
run_test "3" test_lists_test_automator
run_test "4" test_lists_backend_architect
run_test "5" test_lists_refactoring_specialist
run_test "6" test_lists_code_reviewer
run_test "7" test_mentions_token_reduction
run_test "8" test_references_shared_file_path
run_test "9" test_section_size_limit

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
