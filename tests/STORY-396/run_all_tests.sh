#!/bin/bash
# Test Runner: STORY-396 - All Acceptance Criteria
# Story: STORY-396
# Generated: 2026-02-13

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "========================================================"
echo "STORY-396: Batch Rollout Wave 2 - Full Test Suite"
echo "========================================================"
echo ""

TEST_FILES=(
    "test_ac1_template_conformance.sh"
    "test_ac2_anthropic_patterns.sh"
    "test_ac3_before_after_evaluation.sh"
    "test_ac4_zero_regression.sh"
    "test_ac5_line_limits.sh"
    "test_ac6_prompt_versioning.sh"
    "test_ac7_operational_sync.sh"
)

for test_file in "${TEST_FILES[@]}"; do
    echo "--------------------------------------------------------"
    echo "Running: $test_file"
    echo "--------------------------------------------------------"
    if bash "$SCRIPT_DIR/$test_file"; then
        echo ">>> SUITE PASSED: $test_file"
    else
        echo ">>> SUITE FAILED: $test_file"
        ((TOTAL_FAIL++))
    fi
    echo ""
done

echo "========================================================"
echo "STORY-396 Summary: ${#TEST_FILES[@]} suites run"
if [ "$TOTAL_FAIL" -gt 0 ]; then
    echo "RESULT: FAILED ($TOTAL_FAIL suite(s) failed)"
    exit 1
else
    echo "RESULT: ALL PASSED"
    exit 0
fi
echo "========================================================"
