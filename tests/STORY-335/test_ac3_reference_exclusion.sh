#!/bin/bash
# Test AC#3: Exclusion Pattern for Reference Files
# STORY-335: Add Subagent Size Enforcement Mechanism
#
# Validates:
# - Pre-commit hook excludes files in references/ subdirectories
# - CI workflow excludes files in references/ subdirectories
# - Only core .md files are size-checked
# - Reference files can exceed 500/600 lines without triggering warnings/failures
#
# Expected: FAIL initially (TDD Red phase - implementation does not exist yet)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
HOOK_SCRIPT="$PROJECT_ROOT/.claude/hooks/pre-commit-subagent-size.sh"
WORKFLOW_FILE="$PROJECT_ROOT/.github/workflows/subagent-size-check.yml"

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
# Test 1: Hook script contains references/ exclusion pattern
# -----------------------------------------------------------------------------
test_hook_references_exclusion() {
    local test_name="Hook script excludes references/ directories"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check for grep -v '/references/' or similar exclusion pattern
    if grep -qE "grep[[:space:]]+-v.*references|references.*exclude|not.*path.*references|-not.*references" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No references/ exclusion pattern found in hook script"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: CI workflow contains references/ exclusion pattern
# -----------------------------------------------------------------------------
test_workflow_references_exclusion() {
    local test_name="CI workflow excludes references/ directories"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    # Check for exclusion pattern in workflow
    # Use grep -- to handle patterns starting with dashes
    if grep -qE -- "-not.*path.*references|--exclude.*references|grep.*-v.*references" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No references/ exclusion pattern found in workflow"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Hook exclusion uses grep -v pattern
# -----------------------------------------------------------------------------
test_hook_grep_exclusion() {
    local test_name="Hook uses grep -v for exclusion"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    if grep -qE "grep[[:space:]]+-v[[:space:]]+['\"]?/references/" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "grep -v '/references/' pattern not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Workflow uses find with -not -path for exclusion
# -----------------------------------------------------------------------------
test_workflow_find_exclusion() {
    local test_name="Workflow uses find with -not -path for exclusion"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    # Use grep -- to handle patterns starting with dashes
    if grep -qE -- "-not[[:space:]]+-path.*references|! -path.*references" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "find -not -path pattern for references/ not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Hook comment explains reference file exclusion
# -----------------------------------------------------------------------------
test_hook_exclusion_comment() {
    local test_name="Hook contains comment explaining reference exclusion"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check for comment explaining why references are excluded
    if grep -qiE "#.*reference.*exclud|#.*exclud.*reference|#.*overflow" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No comment explaining reference exclusion found"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Workflow comment explains reference file exclusion
# -----------------------------------------------------------------------------
test_workflow_exclusion_comment() {
    local test_name="Workflow contains comment explaining reference exclusion"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    # Check for comment explaining why references are excluded
    if grep -qiE "#.*reference.*exclud|#.*exclud.*reference|#.*overflow" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No comment explaining reference exclusion found"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Hook handles nested references/ paths correctly
# -----------------------------------------------------------------------------
test_hook_nested_references() {
    local test_name="Hook handles nested paths like agents/foo/references/"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - hook script does not exist"
        return
    fi

    # Check that exclusion pattern works for paths like:
    # src/claude/agents/test-automator/references/file.md
    # .claude/agents/test-automator/references/file.md
    if grep -qE "/references/" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Exclusion pattern does not handle nested paths"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Workflow paths filter excludes references at correct level
# -----------------------------------------------------------------------------
test_workflow_paths_specificity() {
    local test_name="Workflow exclusion handles subdirectory references correctly"

    if [ ! -f "$WORKFLOW_FILE" ]; then
        fail_test "$test_name" "Cannot check - workflow does not exist"
        return
    fi

    # Ensure workflow handles patterns like:
    # src/claude/agents/*/references/*.md
    if grep -qE "\*/references/|/references/" "$WORKFLOW_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Workflow exclusion does not handle subdirectory pattern"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: ADR-012 mentioned for reference exclusion rationale
# -----------------------------------------------------------------------------
test_adr_reference_rationale() {
    local test_name="ADR-012 mentioned as rationale for reference exclusion"

    local adr_in_hook=false
    local adr_in_workflow=false

    if [ -f "$HOOK_SCRIPT" ] && grep -qE "ADR-012" "$HOOK_SCRIPT"; then
        adr_in_hook=true
    fi

    if [ -f "$WORKFLOW_FILE" ] && grep -qE "ADR-012" "$WORKFLOW_FILE"; then
        adr_in_workflow=true
    fi

    if [ "$adr_in_hook" = true ] || [ "$adr_in_workflow" = true ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "ADR-012 not mentioned in either file"
    fi
}

# -----------------------------------------------------------------------------
# Test 10: Both files exist (combined check)
# -----------------------------------------------------------------------------
test_both_files_exist() {
    local test_name="Both hook script and workflow file exist"

    local hook_exists=false
    local workflow_exists=false

    if [ -f "$HOOK_SCRIPT" ]; then
        hook_exists=true
    fi

    if [ -f "$WORKFLOW_FILE" ]; then
        workflow_exists=true
    fi

    if [ "$hook_exists" = true ] && [ "$workflow_exists" = true ]; then
        pass_test "$test_name"
    else
        local missing=""
        if [ "$hook_exists" = false ]; then
            missing="hook script"
        fi
        if [ "$workflow_exists" = false ]; then
            if [ -n "$missing" ]; then
                missing="$missing and "
            fi
            missing="${missing}workflow file"
        fi
        fail_test "$test_name" "Missing: $missing"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-335 AC#3: Reference File Exclusion"
echo "=============================================="
echo "Hook script: $HOOK_SCRIPT"
echo "Workflow: $WORKFLOW_FILE"
echo "Expected: Files in references/ are excluded from size checks"
echo "----------------------------------------------"
echo ""

run_test "1" test_hook_references_exclusion
run_test "2" test_workflow_references_exclusion
run_test "3" test_hook_grep_exclusion
run_test "4" test_workflow_find_exclusion
run_test "5" test_hook_exclusion_comment
run_test "6" test_workflow_exclusion_comment
run_test "7" test_hook_nested_references
run_test "8" test_workflow_paths_specificity
run_test "9" test_adr_reference_rationale
run_test "10" test_both_files_exist

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
