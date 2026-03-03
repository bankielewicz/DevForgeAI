#!/bin/bash
# Test: AC#1 - Exit Sequence Uses Numbered Categories
# Story: STORY-515
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/implementing-stories/phases/phase-02-test-first.md"

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

echo "=== AC#1: Exit Sequence Uses Numbered Categories ==="
echo ""

# === Arrange ===
# Extract post-checkpoint content (everything after "## Validation Checkpoint")
POST_CHECKPOINT=$(sed -n '/^## Validation Checkpoint/,$p' "$TARGET_FILE")

# === Act & Assert ===

# Test 1: Category 1 heading exists with number prefix
echo "$POST_CHECKPOINT" | grep -q '### 1\. Post-Checkpoint Mandatory Steps'
run_test "test_should_have_category_1_mandatory_steps_heading_when_post_checkpoint_restructured" $?

# Test 2: Category 2 heading exists with number prefix
echo "$POST_CHECKPOINT" | grep -q '### 2\. Post-Checkpoint Optional Captures'
run_test "test_should_have_category_2_optional_captures_heading_when_post_checkpoint_restructured" $?

# Test 3: Category 3 heading exists with number prefix
echo "$POST_CHECKPOINT" | grep -q '### 3\. Exit Gate'
run_test "test_should_have_category_3_exit_gate_heading_when_post_checkpoint_restructured" $?

# Test 4: Categories are in correct order (1 before 2 before 3)
LINE_CAT1=$(echo "$POST_CHECKPOINT" | grep -n '### 1\. Post-Checkpoint Mandatory Steps' | head -1 | cut -d: -f1)
LINE_CAT2=$(echo "$POST_CHECKPOINT" | grep -n '### 2\. Post-Checkpoint Optional Captures' | head -1 | cut -d: -f1)
LINE_CAT3=$(echo "$POST_CHECKPOINT" | grep -n '### 3\. Exit Gate' | head -1 | cut -d: -f1)

if [ -n "$LINE_CAT1" ] && [ -n "$LINE_CAT2" ] && [ -n "$LINE_CAT3" ] && \
   [ "$LINE_CAT1" -lt "$LINE_CAT2" ] && [ "$LINE_CAT2" -lt "$LINE_CAT3" ]; then
    ORDER_RESULT=0
else
    ORDER_RESULT=1
fi
run_test "test_should_have_categories_ordered_1_before_2_before_3_when_all_present" $ORDER_RESULT

# Test 5: Exactly 3 numbered categories exist in post-checkpoint area
COUNT=$(echo "$POST_CHECKPOINT" | grep -c '### [123]\. ')
if [ "$COUNT" -eq 3 ]; then
    COUNT_RESULT=0
else
    COUNT_RESULT=1
fi
run_test "test_should_have_exactly_3_numbered_categories_when_post_checkpoint_restructured" $COUNT_RESULT

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
