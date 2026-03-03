#!/bin/bash
# Test AC#4: Delegation Patterns to Skills Documented
# STORY-388: Design Command Template Variant with 15K Char Budget Compliance
#
# Validates:
# - Skill(command="devforgeai-[skillname]") syntax present
# - Context marker format with **[Param]:** ${VALUE} documented
# - MANDATORY marker present
# - "DO NOT proceed" statement present
# - Orchestration-only principle stated
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
# Test 1: Skill() invocation syntax present
# ---------------------------------------------------------------------------
test_skill_syntax() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Skill() syntax" "File does not exist"
        return
    fi

    if grep -q 'Skill(command=' "$TEMPLATE"; then
        pass_test "Skill(command=...) syntax found"
    else
        fail_test "Skill() syntax" "No 'Skill(command=' pattern found"
    fi
}

# ---------------------------------------------------------------------------
# Test 2: Context marker format documented
# ---------------------------------------------------------------------------
test_context_markers() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Context markers" "File does not exist"
        return
    fi

    # Look for **Param:** or context marker pattern
    if grep -qE '\*\*.*\*\*:.*\$' "$TEMPLATE"; then
        pass_test "Context marker format documented"
    else
        fail_test "Context markers" "No context marker pattern (**Param:** \$VALUE) found"
    fi
}

# ---------------------------------------------------------------------------
# Test 3: MANDATORY marker present
# ---------------------------------------------------------------------------
test_mandatory_marker() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "MANDATORY marker" "File does not exist"
        return
    fi

    if grep -q "MANDATORY" "$TEMPLATE"; then
        pass_test "MANDATORY marker found"
    else
        fail_test "MANDATORY marker" "No 'MANDATORY' text found"
    fi
}

# ---------------------------------------------------------------------------
# Test 4: "DO NOT proceed" statement
# ---------------------------------------------------------------------------
test_do_not_proceed() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "DO NOT proceed" "File does not exist"
        return
    fi

    if grep -qi "DO NOT.*proceed\|do not.*manual\|DO NOT.*analysis" "$TEMPLATE"; then
        pass_test "DO NOT proceed statement found"
    else
        fail_test "DO NOT proceed" "No 'DO NOT proceed' or equivalent statement found"
    fi
}

# ---------------------------------------------------------------------------
# Test 5: Orchestration-only principle stated
# ---------------------------------------------------------------------------
test_orchestration_only() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Orchestration-only" "File does not exist"
        return
    fi

    if grep -qi "orchestrat" "$TEMPLATE"; then
        pass_test "Orchestration principle referenced"
    else
        fail_test "Orchestration-only" "No orchestration principle mention found"
    fi
}

# ---------------------------------------------------------------------------
# Test 6: Skills implement business logic statement
# ---------------------------------------------------------------------------
test_skills_implement() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Skills implement logic" "File does not exist"
        return
    fi

    if grep -qiE "skill.*(implement|business logic|logic belongs)" "$TEMPLATE"; then
        pass_test "Skills implement business logic statement found"
    else
        fail_test "Skills implement logic" "No statement about skills implementing business logic"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
echo "=============================================="
echo "STORY-388 AC#4: Delegation Patterns"
echo "=============================================="
echo "Target: $TEMPLATE"
echo "----------------------------------------------"
echo ""

run_test "1" test_skill_syntax
run_test "2" test_context_markers
run_test "3" test_mandatory_marker
run_test "4" test_do_not_proceed
run_test "5" test_orchestration_only
run_test "6" test_skills_implement

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
