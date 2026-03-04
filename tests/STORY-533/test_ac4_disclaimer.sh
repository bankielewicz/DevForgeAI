#!/bin/bash
# Test: AC#4 - Financial Guidance Disclaimer
# Story: STORY-533
# Generated: 2026-03-04

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/planning-business/references/viability-scoring.md"

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

echo "=== AC#4: Financial Guidance Disclaimer ==="
echo ""

# --- Act & Assert ---

# Test 1: Disclaimer section exists
grep -qi "disclaimer" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_disclaimer_section_when_scoring_output_defined" $?

# Test 2: Disclaimer states directional guidance
grep -qi "directional guidance\|guidance only" "$TARGET_FILE" 2>/dev/null
run_test "test_should_state_directional_guidance_when_disclaimer_present" $?

# Test 3: Disclaimer mentions not financial advice
grep -qi "financial.*advice\|not.*financial" "$TARGET_FILE" 2>/dev/null
run_test "test_should_mention_not_financial_advice_when_disclaimer_present" $?

# Test 4: Disclaimer mentions not investment advice
grep -qi "investment.*advice\|not.*investment" "$TARGET_FILE" 2>/dev/null
run_test "test_should_mention_not_investment_advice_when_disclaimer_present" $?

# Test 5: Disclaimer mentions not legal advice
grep -qi "legal.*advice\|not.*legal" "$TARGET_FILE" 2>/dev/null
run_test "test_should_mention_not_legal_advice_when_disclaimer_present" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of $((PASSED + FAILED)) tests"
[ $FAILED -eq 0 ] && exit 0 || exit 1
