#!/bin/bash
# Test: AC#4 - 5-Step Workflow Completeness
# Story: STORY-478
# Generated: 2026-02-23
set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET="$PROJECT_ROOT/src/claude/skills/designing-systems/references/domain-reference-generation.md"
PASSED=0
FAILED=0

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

echo "=== AC#4: 5-Step Workflow Completeness ==="

# Test 1: Step 1 - Run Detection Heuristics
grep -iq "Run Detection Heuristics" "$TARGET"
run_test "test_should_contain_step1_detection_heuristics_when_workflow_checked" $?

# Test 2: Step 2 - Present Recommendations via AskUserQuestion
grep -iq "Present Recommendations" "$TARGET"
run_test "test_should_contain_step2_present_recommendations_when_workflow_checked" $?

# Test 3: Step 3 - Generate Reference Files
grep -iq "Generate Reference Files" "$TARGET"
run_test "test_should_contain_step3_generate_reference_files_when_workflow_checked" $?

# Test 4: Step 4 - Verify No Contradictions
grep -iq "Verify No Contradictions" "$TARGET"
run_test "test_should_contain_step4_verify_no_contradictions_when_workflow_checked" $?

# Test 5: Step 5 - Report
grep -iq "Report" "$TARGET" && grep -n "Step 5" "$TARGET" | head -1 | grep -q "."
run_test "test_should_contain_step5_report_when_workflow_checked" $?

# Test 6: Steps appear in correct order (1 before 2 before 3 before 4 before 5)
S1=$(grep -n "Step 1" "$TARGET" | head -1 | cut -d: -f1)
S2=$(grep -n "Step 2" "$TARGET" | head -1 | cut -d: -f1)
S3=$(grep -n "Step 3" "$TARGET" | head -1 | cut -d: -f1)
S4=$(grep -n "Step 4" "$TARGET" | head -1 | cut -d: -f1)
S5=$(grep -n "Step 5" "$TARGET" | head -1 | cut -d: -f1)
[ "$S1" -lt "$S2" ] && [ "$S2" -lt "$S3" ] && [ "$S3" -lt "$S4" ] && [ "$S4" -lt "$S5" ]
run_test "test_should_have_steps_in_order_when_sequence_checked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
