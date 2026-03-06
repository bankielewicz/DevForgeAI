#!/bin/bash
# Test: AC#4 - User Profile Integration
# Story: STORY-538
# Generated: 2026-03-05

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/researching-market/SKILL.md"

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

echo "=== AC#4: User Profile Integration ==="

# === Test 1: Skill reads user profile ===
grep -q "user-profile" "$SKILL_FILE" 2>/dev/null
run_test "Skill references user profile" $?

# === Test 2: Skill adapts pacing based on profile ===
grep -qi "pacing\|task.*chunk\|chunk.*size\|adaptive" "$SKILL_FILE" 2>/dev/null
run_test "Skill adapts pacing or chunking from profile" $?

# === Test 3: Graceful fallback when profile missing ===
grep -qi "fallback\|default.*when.*missing\|profile.*not.*found\|missing.*profile" "$SKILL_FILE" 2>/dev/null
run_test "Graceful fallback when profile missing" $?

# === Test 4: Default pacing values documented ===
# BR-002: defaults should be specific (e.g., 5 questions per prompt, medium detail)
grep -qi "default.*pacing\|default.*level\|beginner\|5.*question\|medium.*detail" "$SKILL_FILE" 2>/dev/null
run_test "Default pacing values are documented" $?

# === Test 5: Profile read happens at phase start (not mid-execution) ===
# Profile loading should be in an early step (Step 0 or initialization)
grep -qi "step.*0\|load.*profile\|read.*profile\|initialization.*profile" "$SKILL_FILE" 2>/dev/null
run_test "Profile read occurs at phase initialization" $?

# === Test 6: Missing profile produces informational message ===
grep -qi "warn\|info.*message\|log.*profile.*not.*found\|WARNING.*profile" "$SKILL_FILE" 2>/dev/null
run_test "Missing profile produces informational message" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
