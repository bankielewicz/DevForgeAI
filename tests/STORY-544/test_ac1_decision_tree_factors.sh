#!/bin/bash
# Test: AC#1 - Decision Tree Guides User Through Entity Selection Factors
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

echo "=== AC#1: Decision Tree Factor Questions ==="
echo ""

# === Arrange ===
# Target: src/claude/skills/advising-legal/references/business-structure-guide.md

# === Act & Assert ===

# Test 1: Source file exists
test -f "$TARGET_FILE"
run_test "test_should_exist_when_business_structure_guide_created" $?

# Test 2: Revenue expectations question present
grep -qi "revenue expectations\|revenue.* question\|expected revenue" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_revenue_expectations_question_when_decision_tree_defined" $?

# Test 3: Partners/co-founders question present
grep -qi "partners\|co-founders\|number of partners" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_partners_cofounders_question_when_decision_tree_defined" $?

# Test 4: Liability exposure question present
grep -qi "liability exposure\|liability.* level\|liability concern" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_liability_exposure_question_when_decision_tree_defined" $?

# Test 5: Tax preferences question present
grep -qi "tax preferences\|tax.* question\|tax consideration" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_tax_preferences_question_when_decision_tree_defined" $?

# Test 6: All four entity types mentioned
for entity in "Sole Proprietorship" "LLC" "S-Corp" "C-Corp"; do
    grep -qi "$entity" "$TARGET_FILE" 2>/dev/null
    run_test "test_should_mention_entity_type_${entity// /_}_when_decision_tree_defined" $?
done

# Test 7: Sequential ordering (factors appear in specified order)
if [ -f "$TARGET_FILE" ]; then
    LINE_REVENUE=$(grep -ni "revenue" "$TARGET_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    LINE_PARTNERS=$(grep -ni "partners\|co-founders" "$TARGET_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    LINE_LIABILITY=$(grep -ni "liability" "$TARGET_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    LINE_TAX=$(grep -ni "tax" "$TARGET_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    if [ -n "$LINE_REVENUE" ] && [ -n "$LINE_PARTNERS" ] && [ -n "$LINE_LIABILITY" ] && [ -n "$LINE_TAX" ]; then
        [ "$LINE_REVENUE" -lt "$LINE_PARTNERS" ] && [ "$LINE_PARTNERS" -lt "$LINE_LIABILITY" ] && [ "$LINE_LIABILITY" -lt "$LINE_TAX" ]
        run_test "test_should_present_factors_in_sequential_order_when_decision_tree_traversed" $?
    else
        run_test "test_should_present_factors_in_sequential_order_when_decision_tree_traversed" 1
    fi
else
    run_test "test_should_present_factors_in_sequential_order_when_decision_tree_traversed" 1
fi

# Test 8: Skill file under 1,000 lines
SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/advising-legal/references/business-structure-guide.md"
if [ -f "$SKILL_FILE" ]; then
    LINE_COUNT=$(wc -l < "$SKILL_FILE")
    [ "$LINE_COUNT" -le 999 ]
    run_test "test_should_be_under_1000_lines_when_skill_file_measured" $?
else
    run_test "test_should_be_under_1000_lines_when_skill_file_measured" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
