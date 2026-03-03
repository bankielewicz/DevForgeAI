#!/bin/bash
# Test: AC#2 - Decision Context Individually Scored
# Story: STORY-512
# Generated: 2026-02-28
# Phase: RED (tests must FAIL before implementation)

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/designing-systems/references/artifact-generation.md"

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

echo "=== AC#2: Decision Context Individually Scored Tests ==="
echo "Target: $TARGET_FILE"
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: Decision Context is individually listed as a scorecard line item
grep -A 30 -i "scorecard" "$TARGET_FILE" | grep -q "Decision Context"
run_test "test_should_list_decision_context_in_scorecard_when_scoring_subsections" $?

# Test 2: Design Rationale is individually scored as a scorecard line item
grep -qE "Design Rationale.*(score|present|missing|populated|empty)" "$TARGET_FILE"
run_test "test_should_score_design_rationale_individually_when_scorecard_rendered" $?

# Test 3: Rejected Alternatives is individually scored as a scorecard line item
grep -qE "Rejected Alternatives.*(score|present|missing|populated|empty)" "$TARGET_FILE"
run_test "test_should_score_rejected_alternatives_individually_when_scorecard_rendered" $?

# Test 4: All three Decision Context items appear in a scorecard context (not just anywhere)
grep -A 30 -i "scorecard" "$TARGET_FILE" | grep -q "Decision Context" && \
grep -A 30 -i "scorecard" "$TARGET_FILE" | grep -q "Design Rationale" && \
grep -A 30 -i "scorecard" "$TARGET_FILE" | grep -q "Rejected Alternatives"
run_test "test_should_list_all_three_decision_items_within_scorecard_section_when_complete" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
