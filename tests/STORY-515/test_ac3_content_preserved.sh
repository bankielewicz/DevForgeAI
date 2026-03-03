#!/bin/bash
# Test: AC#3 - All Original Content Preserved
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

echo "=== AC#3: All Original Content Preserved ==="
echo ""

# === Arrange ===
POST_CHECKPOINT=$(sed -n '/^## Validation Checkpoint/,$p' "$TARGET_FILE")

# === Act & Assert ===

# Test 1: observation-extractor reference preserved (from Observation Capture EPIC-051)
echo "$POST_CHECKPOINT" | grep -q 'observation-extractor'
run_test "test_should_preserve_observation_extractor_reference_when_content_restructured" $?

# Test 2: session_path reference preserved (from Session Memory Update)
echo "$POST_CHECKPOINT" | grep -q 'session_path'
run_test "test_should_preserve_session_path_reference_when_content_restructured" $?

# Test 3: category and friction references preserved (from general Observation Capture)
echo "$POST_CHECKPOINT" | grep -q 'category'
CATEGORY_RESULT=$?
echo "$POST_CHECKPOINT" | grep -q 'friction'
FRICTION_RESULT=$?
if [ "$CATEGORY_RESULT" -eq 0 ] && [ "$FRICTION_RESULT" -eq 0 ]; then
    COMBINED=0
else
    COMBINED=1
fi
run_test "test_should_preserve_category_and_friction_references_when_content_restructured" $COMBINED

# Test 4: phase-complete exit gate command preserved
echo "$POST_CHECKPOINT" | grep -q 'phase-complete'
run_test "test_should_preserve_phase_complete_command_when_content_restructured" $?

# Test 5: AC Checklist grep pattern preserved (from AC Checklist Update Verification)
echo "$POST_CHECKPOINT" | grep -q 'Grep(pattern='
run_test "test_should_preserve_grep_pattern_from_ac_checklist_verification_when_restructured" $?

# Test 6: Session memory Edit block preserved
echo "$POST_CHECKPOINT" | grep -q 'Edit('
run_test "test_should_preserve_edit_block_from_session_memory_when_restructured" $?

# Test 7: observation-capture.md reference preserved
echo "$POST_CHECKPOINT" | grep -q 'observation-capture.md'
run_test "test_should_preserve_observation_capture_md_reference_when_restructured" $?

# Test 8: Pre-checkpoint Test Integrity Snapshot untouched (should exist BEFORE Validation Checkpoint)
PRE_CHECKPOINT=$(sed -n '1,/^## Validation Checkpoint/p' "$TARGET_FILE")
echo "$PRE_CHECKPOINT" | grep -q 'Test Integrity Snapshot'
run_test "test_should_preserve_test_integrity_snapshot_in_pre_checkpoint_when_restructured" $?

# Test 9: Content is under numbered categories (not flat ### headings)
# The old structure has "### AC Checklist Update Verification" as a direct ### heading
# The new structure should have it as #### under a numbered ### category
# This test checks that the OLD flat structure is gone
OLD_FLAT_HEADING=$(echo "$POST_CHECKPOINT" | grep -c '^### AC Checklist Update Verification')
if [ "$OLD_FLAT_HEADING" -eq 0 ]; then
    RESTRUCTURED=0
else
    RESTRUCTURED=1
fi
run_test "test_should_not_have_old_flat_ac_checklist_heading_when_restructured" $RESTRUCTURED

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
