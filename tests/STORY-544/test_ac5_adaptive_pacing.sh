#!/bin/bash
# Test: AC#5 - Adaptive Pacing Reads User Profile Without Modification
# Story: STORY-544
# Generated: 2026-03-04
# TDD Phase: RED (all tests expected to FAIL - source files do not exist yet)

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/advising-legal/SKILL.md"

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

echo "=== AC#5: Adaptive Pacing and Profile Integration ==="
echo ""

# === Arrange ===
# Target: src/claude/skills/advising-legal/SKILL.md

# === Act & Assert ===

# Test 1: Skill file exists
test -f "$SKILL_FILE"
run_test "test_should_exist_when_skill_file_created" $?

# Test 2: Read-only profile access documented
grep -qi "read.only\|read only\|no.*write\|no.*mutation\|immutable.*profile" "$SKILL_FILE" 2>/dev/null
run_test "test_should_specify_read_only_profile_access_when_pacing_defined" $?

# Test 3: Experience level detection (beginner/intermediate/advanced)
grep -qi "beginner" "$SKILL_FILE" 2>/dev/null && \
grep -qi "intermediate" "$SKILL_FILE" 2>/dev/null && \
grep -qi "advanced" "$SKILL_FILE" 2>/dev/null
run_test "test_should_detect_three_experience_levels_when_pacing_configured" $?

# Test 4: Verbosity adjustment based on experience level
grep -qi "verbosity\|explanation.*depth\|detail.*level\|adjust.*pacing" "$SKILL_FILE" 2>/dev/null
run_test "test_should_adjust_verbosity_by_experience_level_when_profile_read" $?

# Test 5: Graceful fallback to intermediate when profile absent
grep -qi "fallback.*intermediate\|default.*intermediate\|absent.*intermediate\|missing.*intermediate" "$SKILL_FILE" 2>/dev/null
run_test "test_should_fallback_to_intermediate_when_profile_absent" $?

# Test 6: No error produced when profile missing
grep -qi "graceful\|no.*error\|silent.*fallback\|profile.*optional" "$SKILL_FILE" 2>/dev/null
run_test "test_should_produce_no_error_when_profile_missing" $?

# Test 7: User profile path referenced
grep -qi "user.*profile\|profile.*path\|profile.*file" "$SKILL_FILE" 2>/dev/null
run_test "test_should_reference_user_profile_path_when_pacing_integrated" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
