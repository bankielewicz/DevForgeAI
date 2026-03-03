#!/bin/bash
# Test Runner: STORY-475 - Phase 5.5 Prompt Alignment Workflow Integration
# Story: STORY-475
# Phase: Red (all tests should FAIL before implementation)

TOTAL_PASS=0
TOTAL_FAIL=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

run_test_file() {
  local test_file="$1"
  local test_name="$(basename "$test_file")"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Running: $test_name"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  bash "$test_file"
  local exit_code=$?
  if [ $exit_code -eq 0 ]; then
    echo "  [SUITE PASS] $test_name"
    ((TOTAL_PASS++))
  else
    echo "  [SUITE FAIL] $test_name"
    ((TOTAL_FAIL++))
  fi
  echo ""
}

# Run all AC test files
run_test_file "$SCRIPT_DIR/test_ac1_reference_file.sh"
run_test_file "$SCRIPT_DIR/test_ac2_skillmd_insertion.sh"
run_test_file "$SCRIPT_DIR/test_ac3_layer_detection.sh"
run_test_file "$SCRIPT_DIR/test_ac4_subagent_invocation.sh"
run_test_file "$SCRIPT_DIR/test_ac5_high_blocking.sh"
run_test_file "$SCRIPT_DIR/test_ac6_gap_synthesis.sh"
run_test_file "$SCRIPT_DIR/test_ac7_claudemd_gaps.sh"
run_test_file "$SCRIPT_DIR/test_ac8_graceful_degradation.sh"
run_test_file "$SCRIPT_DIR/test_ac9_accepted_risk.sh"
run_test_file "$SCRIPT_DIR/test_ac10_workflow_steps.sh"

# Final Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STORY-475 Test Suite Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test suites passed: $TOTAL_PASS / $((TOTAL_PASS + TOTAL_FAIL))"
echo "Test suites failed: $TOTAL_FAIL / $((TOTAL_PASS + TOTAL_FAIL))"
if [ $TOTAL_FAIL -gt 0 ]; then
  echo "STATUS: RED (expected - tests written before implementation)"
  exit 1
else
  echo "STATUS: GREEN"
  exit 0
fi
