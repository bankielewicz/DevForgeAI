#!/bin/bash
# Test: AC#3 - Adaptive Pacing from User Profile
# Story: STORY-546
# Generated: 2026-03-05

PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/SKILL.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#3: Adaptive Pacing from User Profile ==="

# Test 1: Skill references user profile
grep -qi "user.profile\|profile" "$SKILL_FILE" 2>/dev/null
run_test "test_should_reference_profile_when_skill_evaluated" $?

# Test 2: Skill uses Read tool for profile (read-only access)
grep -qE "Read\(" "$SKILL_FILE" 2>/dev/null
run_test "test_should_use_read_tool_when_accessing_profile" $?

# Test 3: Skill does NOT use Write/Edit on profile
! grep -qE "(Write|Edit)\(.*profile" "$SKILL_FILE" 2>/dev/null
run_test "test_should_not_write_profile_when_skill_inspected" $?

# Test 4: Skill mentions experience level adaptation
grep -qi "experience.level\|experience_level\|beginner\|intermediate\|advanced" "$SKILL_FILE" 2>/dev/null
run_test "test_should_adapt_to_experience_level_when_skill_evaluated" $?

# Test 5: Skill handles missing profile gracefully
grep -qi "fallback\|default\|absent\|missing.*profile\|profile.*missing" "$SKILL_FILE" 2>/dev/null
run_test "test_should_handle_missing_profile_when_skill_evaluated" $?

# Test 6: Skill explicitly states read-only constraint on profile
grep -qiE "read.only.*profile|profile.*read.only|does not modify.*profile|not modify the profile" "$SKILL_FILE" 2>/dev/null
run_test "test_should_state_readonly_constraint_when_skill_evaluated" $?

# Test 7: Skill adjusts explanation depth (not just verbosity)
grep -qiE "explanation.depth|adjust.*depth|depth.*adjust" "$SKILL_FILE" 2>/dev/null
run_test "test_should_adjust_explanation_depth_when_skill_evaluated" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
