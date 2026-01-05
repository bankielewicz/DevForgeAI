#!/bin/bash
###############################################################################
# Test Suite: STORY-177 - Integration Test: Atomic Status Update Protocol
# Purpose: Verify all ACs work together as complete atomic update protocol
# TDD Phase: RED (tests should FAIL until implementation)
###############################################################################

set -euo pipefail

QA_SKILL_FILE=".claude/skills/devforgeai-qa/SKILL.md"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

pass_test() {
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "  PASS: $1"
}

fail_test() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "  FAIL: $1"
}

test_case() {
    TEST_COUNT=$((TEST_COUNT + 1))
    echo ""
    echo "Test $TEST_COUNT: $1"
}

header() {
    echo ""
    echo "================================================================"
    echo "$1"
    echo "================================================================"
}

echo "STORY-177 Integration: Atomic Status Update Protocol"
echo "Target: $QA_SKILL_FILE"

# Check file exists
if [ ! -f "$QA_SKILL_FILE" ]; then
    echo ""
    echo "ERROR: QA skill file does not exist: $QA_SKILL_FILE"
    echo "All tests will FAIL."
    exit 1
fi

header "Integration: Complete Atomic Update Protocol"

test_case "Atomic Update Protocol section with complete workflow"
# Look for comprehensive atomic update protocol documentation
if grep -qiE "atomic.*update.*protocol" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found Atomic Update Protocol section"
else
    fail_test "Missing Atomic Update Protocol section"
fi

test_case "Complete sequence: Read -> Edit YAML -> Grep Verify -> Edit History -> Rollback"
# Check for all 5 elements present in the workflow
elements_found=0

# 1. Read current status
if grep -qE "read.*current.*status|Read.*file_path.*story" "$QA_SKILL_FILE" 2>/dev/null; then
    elements_found=$((elements_found + 1))
fi

# 2. Edit YAML frontmatter
if grep -qE "Edit.*status:|old_string.*status:" "$QA_SKILL_FILE" 2>/dev/null; then
    elements_found=$((elements_found + 1))
fi

# 3. Grep verify
if grep -qiE "grep.*verify|Grep.*status|verify.*grep" "$QA_SKILL_FILE" 2>/dev/null; then
    elements_found=$((elements_found + 1))
fi

# 4. Edit history (conditional)
if grep -qE "append.*history|Change.*Log.*entry" "$QA_SKILL_FILE" 2>/dev/null; then
    elements_found=$((elements_found + 1))
fi

# 5. Rollback on failure
if grep -qiE "rollback.*restore|restore.*original|rollback.*fail" "$QA_SKILL_FILE" 2>/dev/null; then
    elements_found=$((elements_found + 1))
fi

if [ $elements_found -ge 5 ]; then
    pass_test "Found all 5 protocol elements"
else
    fail_test "Only $elements_found/5 protocol elements found"
fi

test_case "Step 3.4 contains complete atomic protocol documentation"
step34_exists=$(grep -c "### Step 3.4" "$QA_SKILL_FILE" 2>/dev/null || echo "0")
if [ "$step34_exists" -gt 0 ]; then
    step34_content=$(sed -n '/### Step 3.4/,/### Step 3.5/p' "$QA_SKILL_FILE" 2>/dev/null || echo "")
    step34_length=$(echo "$step34_content" | wc -l)

    # Step 3.4 should have substantial content for atomic protocol
    if [ "$step34_length" -gt 20 ]; then
        pass_test "Step 3.4 has substantial protocol documentation ($step34_length lines)"
    else
        fail_test "Step 3.4 too brief ($step34_length lines) for complete protocol"
    fi
else
    fail_test "Step 3.4 section not found"
fi

test_case "Protocol enforces YAML-first ordering"
if grep -qE "(1|first).*status.*(2|then).*history|yaml.*before.*history|status.*first" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found YAML-first ordering enforcement"
else
    fail_test "Missing explicit YAML-first ordering"
fi

test_case "Protocol enforces conditional history append"
if grep -qE "only.*after.*verif|ONLY.*AFTER|if.*succeed.*then.*history" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found conditional history append enforcement"
else
    fail_test "Missing conditional history append logic"
fi

test_case "Protocol mentions atomicity guarantee"
if grep -qiE "atomic.*guarantee|ensure.*atomic|atomicity|atomic.*this.*step" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found atomicity guarantee statement"
else
    fail_test "Missing atomicity guarantee statement"
fi

test_case "Error recovery documented"
if grep -qE "error.*recovery|fail.*manual.*intervention|HALT.*diverge|recovery.*protocol" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found error recovery documentation"
else
    fail_test "Missing error recovery documentation"
fi

test_case "Validation checkpoint enforces atomic update completion"
# Check for validation checkpoint with atomic update items
if grep -qE "\[.*\].*Status.*update|\[.*\].*verif.*Read|\[.*\].*matches.*expect" "$QA_SKILL_FILE" 2>/dev/null; then
    pass_test "Found validation checkpoint for atomic update"
else
    fail_test "Missing validation checkpoint items for atomic update"
fi

header "Run Individual AC Tests"
echo ""

# Track AC test results
ac_tests_passed=0
ac_tests_failed=0

for ac_num in 1 2 3 4 5 6; do
    case $ac_num in
        1) test_file="test_ac1_yaml_frontmatter_updated_first.sh" ;;
        2) test_file="test_ac2_verification_with_grep.sh" ;;
        3) test_file="test_ac3_history_entry_after_verification.sh" ;;
        4) test_file="test_ac4_single_edit_sequence.sh" ;;
        5) test_file="test_ac5_rollback_on_failure.sh" ;;
        6) test_file="test_ac6_protocol_documented.sh" ;;
    esac

    test_path="tests/STORY-177/$test_file"

    if [ -f "$test_path" ]; then
        echo "Running AC#$ac_num test: $test_file"
        if bash "$test_path" > /dev/null 2>&1; then
            echo "  AC#$ac_num: PASSED"
            ac_tests_passed=$((ac_tests_passed + 1))
        else
            echo "  AC#$ac_num: FAILED (expected in RED phase)"
            ac_tests_failed=$((ac_tests_failed + 1))
        fi
    else
        echo "  AC#$ac_num test file not found: $test_path"
        ac_tests_failed=$((ac_tests_failed + 1))
    fi
done

header "Final Summary"
echo ""
echo "Integration Tests:"
echo "  Total: $TEST_COUNT"
echo "  Passed: $PASS_COUNT"
echo "  Failed: $FAIL_COUNT"
echo ""
echo "Individual AC Tests:"
echo "  Passed: $ac_tests_passed/6"
echo "  Failed: $ac_tests_failed/6"
echo ""

total_failed=$((FAIL_COUNT + ac_tests_failed))

if [ $total_failed -gt 0 ]; then
    echo "STATUS: RED PHASE - Tests failing as expected (TDD)"
    exit 1
else
    echo "STATUS: GREEN PHASE - All tests passing"
    exit 0
fi
