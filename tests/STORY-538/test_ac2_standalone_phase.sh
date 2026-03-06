#!/bin/bash
# Test: AC#2 - Standalone Phase Execution
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

echo "=== AC#2: Standalone Phase Execution ==="

# === Test 1: Skill contains standalone mode documentation ===
grep -qi "standalone" "$SKILL_FILE" 2>/dev/null
run_test "Skill documents standalone mode" $?

# === Test 2: Skill has phase routing section ===
# Must have explicit routing that maps phase argument to execution
grep -qi "phase.*routing\|phase.*dispatch\|phase.*selection\|execution.*mode" "$SKILL_FILE" 2>/dev/null
run_test "Skill contains phase routing section" $?

# === Test 3: market-sizing phase can run independently ===
# Skill must document that market-sizing has no prerequisite phases
grep -qi "market-sizing.*independent\|market-sizing.*standalone\|market-sizing.*without.*prior" "$SKILL_FILE" 2>/dev/null
run_test "market-sizing documented as independently runnable" $?

# === Test 4: competitive-analysis phase can run independently ===
grep -qi "competitive-analysis.*independent\|competitive-analysis.*standalone\|competitive-analysis.*without.*prior" "$SKILL_FILE" 2>/dev/null
run_test "competitive-analysis documented as independently runnable" $?

# === Test 5: customer-interviews phase can run independently ===
grep -qi "customer-interviews.*independent\|customer-interviews.*standalone\|customer-interviews.*without.*prior" "$SKILL_FILE" 2>/dev/null
run_test "customer-interviews documented as independently runnable" $?

# === Test 6: Each phase produces its own output without requiring others ===
grep -qi "no.*prerequisite\|no.*prior.*phase\|independently.*complet" "$SKILL_FILE" 2>/dev/null
run_test "Skill states phases have no prerequisite requirement" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
