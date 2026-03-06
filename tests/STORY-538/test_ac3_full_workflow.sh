#!/bin/bash
# Test: AC#3 - Full Workflow Mode
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

echo "=== AC#3: Full Workflow Mode ==="

# === Test 1: Skill documents full workflow mode ===
grep -qi "full.*mode\|full.*workflow" "$SKILL_FILE" 2>/dev/null
run_test "Skill documents full workflow mode" $?

# === Test 2: Full mode runs phases sequentially ===
# Must document the sequence: market-sizing -> competitive-analysis -> customer-interviews
grep -qi "sequential\|market-sizing.*competitive-analysis.*customer-interviews\|phase.*1.*phase.*2.*phase.*3" "$SKILL_FILE" 2>/dev/null
run_test "Full mode specifies sequential phase execution" $?

# === Test 3: Context passing between phases is documented ===
# Full mode must pass context/output from one phase to the next
grep -qi "context.*pass\|output.*next.*phase\|phase.*context\|carry.*forward\|pass.*between.*phase" "$SKILL_FILE" 2>/dev/null
run_test "Context passing between phases documented" $?

# === Test 4: Full mode reuse detection for existing outputs ===
# BR-003: existing phase outputs trigger reuse prompt
grep -qi "reuse\|existing.*output\|already.*exist\|regenerate" "$SKILL_FILE" 2>/dev/null
run_test "Full mode detects existing outputs and offers reuse" $?

# === Test 5: Full mode ordering is market-sizing first ===
# Verify market-sizing appears before competitive-analysis in workflow
MS_LINE=$(grep -n -i "market-sizing" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)
CA_LINE=$(grep -n -i "competitive-analysis" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)
CI_LINE=$(grep -n -i "customer-interview" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)
if [ -n "$MS_LINE" ] && [ -n "$CA_LINE" ] && [ -n "$CI_LINE" ]; then
    if [ "$MS_LINE" -lt "$CA_LINE" ] && [ "$CA_LINE" -lt "$CI_LINE" ]; then
        run_test "Phase ordering: market-sizing before competitive-analysis before customer-interviews" 0
    else
        run_test "Phase ordering: market-sizing before competitive-analysis before customer-interviews" 1
    fi
else
    run_test "Phase ordering: market-sizing before competitive-analysis before customer-interviews" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
