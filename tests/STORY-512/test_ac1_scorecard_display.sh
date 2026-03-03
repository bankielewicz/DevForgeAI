#!/bin/bash
# Test: AC#1 - Epic Completeness Scorecard Display
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

echo "=== AC#1: Scorecard Display Tests ==="
echo "Target: $TARGET_FILE"
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: Scorecard section exists in artifact-generation.md
grep -qi "completeness scorecard\|completeness score" "$TARGET_FILE"
run_test "test_should_contain_completeness_scorecard_section_when_artifact_generation_loaded" $?

# Test 2: Scorecard contains present/populated indicator
grep -q "present and populated" "$TARGET_FILE"
run_test "test_should_contain_present_indicator_description_when_scorecard_defined" $?

# Test 3: Scorecard contains missing/empty indicator
grep -q "missing or empty" "$TARGET_FILE"
run_test "test_should_contain_missing_indicator_description_when_scorecard_defined" $?

# Test 4: Scorecard contains overall score pattern (e.g., "X/Y sections complete")
grep -qE "[0-9]+/[0-9]+ sections complete" "$TARGET_FILE"
run_test "test_should_contain_overall_score_pattern_when_scorecard_displayed" $?

# Test 5: Scorecard step references display after epic creation
grep -qi "after epic creation\|post-creation\|display.*scorecard\|scorecard.*display" "$TARGET_FILE"
run_test "test_should_reference_post_creation_display_when_scorecard_step_exists" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
