#!/bin/bash
# Test: AC#2 - Mandatory Steps Labeled Explicitly
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

echo "=== AC#2: Mandatory Steps Labeled Explicitly ==="
echo ""

# === Arrange ===
POST_CHECKPOINT=$(sed -n '/^## Validation Checkpoint/,$p' "$TARGET_FILE")

# === Act & Assert ===

# Test 1: Mandatory category has [MANDATORY] label
echo "$POST_CHECKPOINT" | grep -q '\[MANDATORY\]'
run_test "test_should_have_MANDATORY_label_when_mandatory_category_exists" $?

# Test 2: Optional category has [OPTIONAL] label
echo "$POST_CHECKPOINT" | grep -q '\[OPTIONAL\]'
run_test "test_should_have_OPTIONAL_label_when_optional_category_exists" $?

# Test 3: AC Checklist Update Verification is under mandatory section (between cat 1 and cat 2)
# Extract content between category 1 and category 2 headings
MANDATORY_SECTION=$(echo "$POST_CHECKPOINT" | sed -n '/### 1\. Post-Checkpoint Mandatory Steps/,/### 2\. Post-Checkpoint Optional Captures/p')
echo "$MANDATORY_SECTION" | grep -q 'AC Checklist Update Verification'
run_test "test_should_have_ac_checklist_update_under_mandatory_when_restructured" $?

# Test 4: Observation Capture (EPIC-051) is under optional section
OPTIONAL_SECTION=$(echo "$POST_CHECKPOINT" | sed -n '/### 2\. Post-Checkpoint Optional Captures/,/### 3\. Exit Gate/p')
echo "$OPTIONAL_SECTION" | grep -q 'Observation Capture (EPIC-051)'
run_test "test_should_have_observation_capture_epic051_under_optional_when_restructured" $?

# Test 5: Session Memory Update is under optional section
echo "$OPTIONAL_SECTION" | grep -q 'Session Memory Update'
run_test "test_should_have_session_memory_update_under_optional_when_restructured" $?

# Test 6: General Observation Capture is under optional section
echo "$OPTIONAL_SECTION" | grep -q 'Observation Capture'
run_test "test_should_have_general_observation_capture_under_optional_when_restructured" $?

# Test 7: [MANDATORY] label is on category 1 heading line
echo "$POST_CHECKPOINT" | grep -q '### 1\. Post-Checkpoint Mandatory Steps \[MANDATORY\]'
run_test "test_should_have_MANDATORY_on_category_1_heading_line_when_restructured" $?

# Test 8: [OPTIONAL] label is on category 2 heading line
echo "$POST_CHECKPOINT" | grep -q '### 2\. Post-Checkpoint Optional Captures \[OPTIONAL\]'
run_test "test_should_have_OPTIONAL_on_category_2_heading_line_when_restructured" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
