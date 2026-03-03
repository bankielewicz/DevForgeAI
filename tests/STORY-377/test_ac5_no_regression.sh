#!/bin/bash
# Test AC#5: No Regression Without Treelint
# STORY-377: Update devforgeai-development Skill for Treelint
#
# Validates:
# - All existing phase behavior is preserved (no breaking changes)
# - SKILL.md still contains all original required sections
# - tdd-red-phase.md still has mandatory steps and checkpoint
# - tdd-green-phase.md still has remediation mode check and implementation steps
# - tdd-refactor-phase.md still has story type skip check and light QA step
# - Treelint context notes use conditional language (not mandatory requirements)
# - No hard dependency on Treelint binary in workflow files
#
# Expected: FAIL initially (TDD Red phase - Treelint context notes will introduce
# new content that must use conditional language)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/SKILL.md"
RED_PHASE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/tdd-red-phase.md"
GREEN_PHASE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/tdd-green-phase.md"
REFACTOR_PHASE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/tdd-refactor-phase.md"

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
# Test 1: SKILL.md still contains "Purpose" section
# -----------------------------------------------------------------------------
test_skill_has_purpose() {
    local test_name="SKILL.md still contains Purpose section"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "SKILL.md not found"
        return
    fi

    if grep -q "^## Purpose" "$SKILL_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Purpose section missing from SKILL.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: SKILL.md still contains "Required Subagents Per Phase" table
# -----------------------------------------------------------------------------
test_skill_has_subagents_table() {
    local test_name="SKILL.md still contains Required Subagents Per Phase"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "SKILL.md not found"
        return
    fi

    if grep -q "Required Subagents Per Phase" "$SKILL_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Required Subagents Per Phase table missing from SKILL.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: tdd-red-phase.md still has Phase 02 Completion Checkpoint
# -----------------------------------------------------------------------------
test_red_has_checkpoint() {
    local test_name="tdd-red-phase.md still has Phase 02 Completion Checkpoint"

    if [ ! -f "$RED_PHASE_FILE" ]; then
        fail_test "$test_name" "tdd-red-phase.md not found"
        return
    fi

    if grep -q "PHASE 02 COMPLETION CHECKPOINT" "$RED_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Phase 02 Completion Checkpoint missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: tdd-green-phase.md still has Remediation Mode Check
# -----------------------------------------------------------------------------
test_green_has_remediation() {
    local test_name="tdd-green-phase.md still has Remediation Mode Check"

    if [ ! -f "$GREEN_PHASE_FILE" ]; then
        fail_test "$test_name" "tdd-green-phase.md not found"
        return
    fi

    if grep -q "Remediation Mode Check" "$GREEN_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Remediation Mode Check missing from tdd-green-phase.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: tdd-green-phase.md still has Step 1: Determine Implementation Subagent
# -----------------------------------------------------------------------------
test_green_has_determine_agent() {
    local test_name="tdd-green-phase.md still has Determine Implementation Subagent"

    if [ ! -f "$GREEN_PHASE_FILE" ]; then
        fail_test "$test_name" "tdd-green-phase.md not found"
        return
    fi

    if grep -q "Determine Implementation Subagent" "$GREEN_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Determine Implementation Subagent step missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: tdd-refactor-phase.md still has Story Type Skip Check
# -----------------------------------------------------------------------------
test_refactor_has_skip_check() {
    local test_name="tdd-refactor-phase.md still has Story Type Skip Check"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "tdd-refactor-phase.md not found"
        return
    fi

    if grep -q "Story Type Skip Check" "$REFACTOR_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Story Type Skip Check missing from tdd-refactor-phase.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: tdd-refactor-phase.md still has Light QA Validation step
# -----------------------------------------------------------------------------
test_refactor_has_light_qa() {
    local test_name="tdd-refactor-phase.md still has Light QA Validation step"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "tdd-refactor-phase.md not found"
        return
    fi

    if grep -q "Light QA Validation" "$REFACTOR_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Light QA Validation step missing from tdd-refactor-phase.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: No hard Treelint binary dependency in workflow files
# -----------------------------------------------------------------------------
test_no_hard_treelint_dependency() {
    local test_name="No hard Treelint binary dependency in workflow files"

    local hard_dependency_count=0

    for file in "$RED_PHASE_FILE" "$GREEN_PHASE_FILE" "$REFACTOR_PHASE_FILE"; do
        if [ -f "$file" ]; then
            # Check for hard requirement patterns (MUST have treelint, require treelint)
            local hard_deps
            hard_deps=$(grep -ciE "MUST.*treelint.*install|require.*treelint.*binary|treelint.*REQUIRED" "$file" 2>/dev/null)
            hard_dependency_count=$((hard_dependency_count + hard_deps))
        fi
    done

    if [ "$hard_dependency_count" -eq 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Found $hard_dependency_count hard Treelint dependency statements"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Treelint context uses conditional/optional language
# -----------------------------------------------------------------------------
test_treelint_uses_conditional_language() {
    local test_name="Treelint context uses conditional/optional language"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "SKILL.md not found"
        return
    fi

    # If Treelint Integration section exists, verify it uses conditional language
    local section_content
    section_content=$(sed -n '/^## Treelint Integration/,/^## /p' "$SKILL_FILE" | head -n -1)

    if [ -z "$section_content" ]; then
        fail_test "$test_name" "Treelint Integration section not found (cannot validate conditional language)"
        return
    fi

    # Look for conditional/optional language patterns
    if echo "$section_content" | grep -qiE "available|optional|when.*installed|if.*available|fallback"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Treelint Integration section lacks conditional/optional language"
    fi
}

# -----------------------------------------------------------------------------
# Test 10: SKILL.md line count within acceptable range (not bloated)
# -----------------------------------------------------------------------------
test_skill_not_bloated() {
    local test_name="SKILL.md line count within acceptable range"

    if [ ! -f "$SKILL_FILE" ]; then
        fail_test "$test_name" "SKILL.md not found"
        return
    fi

    local line_count
    line_count=$(wc -l < "$SKILL_FILE")

    # SKILL.md should stay under 1200 lines (current ~1075 + max 40 lines for Treelint section)
    if [ "$line_count" -le 1200 ]; then
        pass_test "$test_name (actual: $line_count lines)"
    else
        fail_test "$test_name" "SKILL.md has $line_count lines (max: 1200 to prevent bloat)"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-377 AC#5: No Regression Without Treelint"
echo "=============================================="
echo "Checking files:"
echo "  - $SKILL_FILE"
echo "  - $RED_PHASE_FILE"
echo "  - $GREEN_PHASE_FILE"
echo "  - $REFACTOR_PHASE_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_skill_has_purpose
run_test "2" test_skill_has_subagents_table
run_test "3" test_red_has_checkpoint
run_test "4" test_green_has_remediation
run_test "5" test_green_has_determine_agent
run_test "6" test_refactor_has_skip_check
run_test "7" test_refactor_has_light_qa
run_test "8" test_no_hard_treelint_dependency
run_test "9" test_treelint_uses_conditional_language
run_test "10" test_skill_not_bloated

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
