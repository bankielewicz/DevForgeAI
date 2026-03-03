#!/bin/bash
# Test: AC#9 - audit-w3 skill completeness (scanning logic is the business logic)
# Story: STORY-462
# Generated: 2026-02-21
# TDD Phase: RED (all tests expected to FAIL before implementation)
# Verifies ALL 4 scanning phases, exit status logic, and exclusion patterns are in the skill.

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
PASSED=0
FAILED=0

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

echo "=== AC#9: audit-w3 skill completeness ==="

SKILL_FILE="$PROJECT_ROOT/src/claude/skills/auditing-w3-compliance/SKILL.md"

# Verify skill exists first
if [ ! -f "$SKILL_FILE" ]; then
    echo "  FAIL: auditing-w3-compliance/SKILL.md does not exist - ALL tests in this file fail"
    echo ""
    echo "Results: 0 passed, 6 failed"
    exit 1
fi

# --- Test 1: Skill contains CRITICAL scanning section ---
grep -qi "CRITICAL" "$SKILL_FILE"
run_test "Skill contains 'CRITICAL' scanning section" $?

# --- Test 2: Skill contains HIGH scanning section ---
grep -qi "HIGH" "$SKILL_FILE"
run_test "Skill contains 'HIGH' scanning section" $?

# --- Test 3: Skill contains MEDIUM scanning section ---
grep -qi "MEDIUM" "$SKILL_FILE"
run_test "Skill contains 'MEDIUM' scanning section" $?

# --- Test 4: Skill contains INFO scanning section ---
grep -qi "INFO" "$SKILL_FILE"
run_test "Skill contains 'INFO' scanning section" $?

# --- Test 5: Skill contains exit status logic ---
# Look for exit keyword (bash exit) or EXIT (description of exit logic)
grep -qiE "\bexit\b" "$SKILL_FILE"
run_test "Skill contains exit status logic (exit keyword)" $?

# --- Test 6: Skill contains exclusion patterns ---
grep -qi "Exclusion" "$SKILL_FILE"
run_test "Skill contains exclusion patterns section" $?

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
