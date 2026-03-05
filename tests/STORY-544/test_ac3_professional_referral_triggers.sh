#!/bin/bash
# Test: AC#3 - Professional Referral Triggers Fire for Complex Situations
# Story: STORY-544
# Generated: 2026-03-04
# TDD Phase: RED (all tests expected to FAIL - source files do not exist yet)

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/src/claude/skills/advising-legal/references/business-structure-guide.md"

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

echo "=== AC#3: Professional Referral Triggers ==="
echo ""

# === Arrange ===
# 5 complexity triggers that must produce "Consult a Professional" blocks

# === Act & Assert ===

# Test 1: Source file exists
test -f "$TARGET_FILE"
run_test "test_should_exist_when_guide_file_created" $?

# Test 2: "Consult a Professional" block pattern exists
grep -qi "consult a professional\|consult.*professional\|professional.*referral" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_consult_professional_block_when_triggers_defined" $?

# Test 3: Multi-state operations trigger
grep -qi "multi.state" "$TARGET_FILE" 2>/dev/null
run_test "test_should_trigger_referral_when_multi_state_operations_detected" $?

# Test 4: International operations trigger
grep -qi "international" "$TARGET_FILE" 2>/dev/null
run_test "test_should_trigger_referral_when_international_operations_detected" $?

# Test 5: 2+ partners trigger
grep -qi "two.*partner\|2.*partner\|more than one.*partner\|multiple.*partner" "$TARGET_FILE" 2>/dev/null
run_test "test_should_trigger_referral_when_two_or_more_partners_detected" $?

# Test 6: S-Corp election trigger
grep -qi "s.corp.*election\|election.*s.corp" "$TARGET_FILE" 2>/dev/null
run_test "test_should_trigger_referral_when_scorp_election_questions_detected" $?

# Test 7: C-Corp equity/investor trigger
grep -qi "c.corp.*equity\|equity.*investor\|c.corp.*investor" "$TARGET_FILE" 2>/dev/null
run_test "test_should_trigger_referral_when_ccorp_equity_questions_detected" $?

# Test 8: Each trigger names the specific complexity detected
# Verify trigger blocks include explanation of why it exceeds scope
grep -qi "exceeds.*scope\|beyond.*educational\|requires.*professional\|scope.*limit" "$TARGET_FILE" 2>/dev/null
run_test "test_should_explain_scope_limitation_when_referral_triggered" $?

# Test 9: Each trigger lists professional type (attorney, CPA, or both)
grep -qi "attorney\|CPA\|certified public accountant\|lawyer" "$TARGET_FILE" 2>/dev/null
run_test "test_should_list_professional_type_when_referral_triggered" $?

# Test 10: Branch halt documented (no further recommendation after trigger)
grep -qi "halt.*branch\|stop.*recommendation\|no further.*output\|branch.*terminate" "$TARGET_FILE" 2>/dev/null
run_test "test_should_halt_branch_when_referral_triggered" $?

# Test 11: All 5 triggers have distinct referral blocks (count occurrences)
if [ -f "$TARGET_FILE" ]; then
    TRIGGER_COUNT=$(grep -ci "consult a professional\|professional.*referral" "$TARGET_FILE" 2>/dev/null)
    [ "$TRIGGER_COUNT" -ge 5 ]
    run_test "test_should_have_at_least_5_referral_blocks_when_all_triggers_defined" $?
else
    run_test "test_should_have_at_least_5_referral_blocks_when_all_triggers_defined" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
