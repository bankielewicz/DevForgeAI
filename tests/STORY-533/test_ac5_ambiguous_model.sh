#!/bin/bash
# Test: AC#5 - Ambiguous Model Handling
# Story: STORY-533
# Generated: 2026-03-04

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/planning-business/references/business-model-patterns.md"

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

echo "=== AC#5: Ambiguous Model Handling ==="
echo ""

# --- Act & Assert ---

# Test 1: Ambiguity detection section exists
grep -qi "ambigu" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_ambiguity_section_when_multi_model_handling_defined" $?

# Test 2: 0.1 threshold for ambiguity
grep -q "0\.1" "$TARGET_FILE" 2>/dev/null
run_test "test_should_define_0_1_threshold_when_ambiguity_detection_configured" $?

# Test 3: AskUserQuestion instruction present
grep -q "AskUserQuestion" "$TARGET_FILE" 2>/dev/null
run_test "test_should_instruct_askuserquestion_when_ambiguous_model_detected" $?

# Test 4: Candidates ranked by confidence
grep -qi "rank\|candidate" "$TARGET_FILE" 2>/dev/null
run_test "test_should_rank_candidates_when_multiple_models_match" $?

# Test 5: User selection flow described
grep -qi "select\|choose\|user.*model" "$TARGET_FILE" 2>/dev/null
run_test "test_should_describe_user_selection_when_ambiguity_resolved" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of $((PASSED + FAILED)) tests"
[ $FAILED -eq 0 ] && exit 0 || exit 1
