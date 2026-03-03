#!/bin/bash
# Test AC#6: Works Correctly WITH Treelint
# STORY-377: Update devforgeai-development Skill for Treelint
#
# Validates:
# - All 4 phase reference files contain Treelint context that subagents will receive
# - SKILL.md Treelint Integration section is a valid documentation section
# - Treelint context notes reference the shared patterns file path consistently
# - All phase files reference consistent Treelint terminology
# - The shared reference file (.claude/agents/references/treelint-search-patterns.md) exists in src/
#
# Expected: FAIL initially (TDD Red phase - no Treelint context in phase files yet)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/SKILL.md"
RED_PHASE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/tdd-red-phase.md"
GREEN_PHASE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/tdd-green-phase.md"
REFACTOR_PHASE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/tdd-refactor-phase.md"
SHARED_TREELINT_REF="$PROJECT_ROOT/src/claude/agents/references/treelint-search-patterns.md"

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
# Test 1: Shared Treelint reference file exists in src/ tree
# -----------------------------------------------------------------------------
test_shared_reference_exists() {
    local test_name="Shared Treelint reference file exists in src/ tree"
    if [ -f "$SHARED_TREELINT_REF" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $SHARED_TREELINT_REF"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: All 4 target files exist
# -----------------------------------------------------------------------------
test_all_target_files_exist() {
    local test_name="All 4 target files exist"
    local missing_count=0
    local missing_files=""

    for file in "$SKILL_FILE" "$RED_PHASE_FILE" "$GREEN_PHASE_FILE" "$REFACTOR_PHASE_FILE"; do
        if [ ! -f "$file" ]; then
            missing_count=$((missing_count + 1))
            missing_files="$missing_files $(basename $file)"
        fi
    done

    if [ "$missing_count" -eq 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "$missing_count files missing:$missing_files"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: SKILL.md has Treelint content for subagent awareness
# -----------------------------------------------------------------------------
test_skill_has_treelint_content() {
    local test_name="SKILL.md has Treelint content"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "SKILL.md not found"
        return
    fi

    if grep -qi "treelint" "$SKILL_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Treelint content in SKILL.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: tdd-red-phase.md has Treelint content
# -----------------------------------------------------------------------------
test_red_phase_has_treelint() {
    local test_name="tdd-red-phase.md has Treelint content"

    if [ ! -f "$RED_PHASE_FILE" ]; then
        fail_test "$test_name" "File not found"
        return
    fi

    if grep -qi "treelint" "$RED_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Treelint content in tdd-red-phase.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: tdd-green-phase.md has Treelint content
# -----------------------------------------------------------------------------
test_green_phase_has_treelint() {
    local test_name="tdd-green-phase.md has Treelint content"

    if [ ! -f "$GREEN_PHASE_FILE" ]; then
        fail_test "$test_name" "File not found"
        return
    fi

    if grep -qi "treelint" "$GREEN_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Treelint content in tdd-green-phase.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: tdd-refactor-phase.md has Treelint content
# -----------------------------------------------------------------------------
test_refactor_phase_has_treelint() {
    local test_name="tdd-refactor-phase.md has Treelint content"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "File not found"
        return
    fi

    if grep -qi "treelint" "$REFACTOR_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Treelint content in tdd-refactor-phase.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Consistent Treelint terminology across files
# -----------------------------------------------------------------------------
test_consistent_terminology() {
    local test_name="Consistent Treelint terminology across all phase files"

    local files_with_treelint=0
    local files_checked=0

    for file in "$RED_PHASE_FILE" "$GREEN_PHASE_FILE" "$REFACTOR_PHASE_FILE"; do
        if [ -f "$file" ]; then
            files_checked=$((files_checked + 1))
            if grep -qi "treelint" "$file"; then
                files_with_treelint=$((files_with_treelint + 1))
            fi
        fi
    done

    if [ "$files_checked" -eq 0 ]; then
        fail_test "$test_name" "No phase files found to check"
        return
    fi

    # All 3 phase reference files should mention Treelint
    if [ "$files_with_treelint" -eq 3 ]; then
        pass_test "$test_name ($files_with_treelint/3 files have Treelint references)"
    else
        fail_test "$test_name" "Only $files_with_treelint/3 phase files mention Treelint"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Treelint reference file path is referenced consistently
# -----------------------------------------------------------------------------
test_reference_path_consistency() {
    local test_name="Treelint reference path referenced consistently"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "SKILL.md not found"
        return
    fi

    # Check that SKILL.md references the shared patterns file
    if grep -q "treelint-search-patterns" "$SKILL_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "treelint-search-patterns path not referenced in SKILL.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Total Treelint additions across all files reasonable (under 3000 chars)
# -----------------------------------------------------------------------------
test_total_treelint_additions_reasonable() {
    local test_name="Total Treelint additions across all files under 3000 chars"

    local total_chars=0

    for file in "$SKILL_FILE" "$RED_PHASE_FILE" "$GREEN_PHASE_FILE" "$REFACTOR_PHASE_FILE"; do
        if [ -f "$file" ]; then
            local treelint_chars
            treelint_chars=$(grep -i "treelint" "$file" | wc -c)
            total_chars=$((total_chars + treelint_chars))
        fi
    done

    if [ "$total_chars" -eq 0 ]; then
        fail_test "$test_name" "No Treelint content found across any files"
        return
    fi

    if [ "$total_chars" -le 3000 ]; then
        pass_test "$test_name (actual: $total_chars chars total)"
    else
        fail_test "$test_name" "Total Treelint content is $total_chars chars (max: 3000)"
    fi
}

# -----------------------------------------------------------------------------
# Test 10: Shared reference file has required YAML frontmatter
# -----------------------------------------------------------------------------
test_shared_ref_has_frontmatter() {
    local test_name="Shared reference file has YAML frontmatter"

    if [ ! -f "$SHARED_TREELINT_REF" ]; then
        fail_test "$test_name" "Shared reference file not found"
        return
    fi

    local first_line
    first_line=$(head -1 "$SHARED_TREELINT_REF")

    if [ "$first_line" = "---" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File does not start with YAML frontmatter delimiter (---)"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-377 AC#6: Works Correctly WITH Treelint"
echo "=============================================="
echo "Checking files:"
echo "  - $SKILL_FILE"
echo "  - $RED_PHASE_FILE"
echo "  - $GREEN_PHASE_FILE"
echo "  - $REFACTOR_PHASE_FILE"
echo "  - $SHARED_TREELINT_REF"
echo "----------------------------------------------"
echo ""

run_test "1" test_shared_reference_exists
run_test "2" test_all_target_files_exist
run_test "3" test_skill_has_treelint_content
run_test "4" test_red_phase_has_treelint
run_test "5" test_green_phase_has_treelint
run_test "6" test_refactor_phase_has_treelint
run_test "7" test_consistent_terminology
run_test "8" test_reference_path_consistency
run_test "9" test_total_treelint_additions_reasonable
run_test "10" test_shared_ref_has_frontmatter

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
