#!/bin/bash
# STORY-331 Test Runner
# Runs all acceptance criteria tests for agent-generator.md progressive disclosure refactoring
#
# Usage: ./run_all_tests.sh
#
# Test Files:
#   - test_ac1_core_file_size.sh       - Core file <= 300 lines, 8 required sections
#   - test_ac2_reference_directory.sh  - References directory with 6-10 files
#   - test_ac3_functionality_preservation.sh - All original functionality preserved
#   - test_ac4_reference_loading.sh    - Reference Loading section with Read() calls
#   - test_ac5_observation_capture.sh  - Observation Capture section (EPIC-052)
#   - test_ac6_sync_verification.sh    - src/ and .claude/ copies identical

# Note: Not using set -e to allow test runner to continue on failures

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Tracking
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
FAILED_SUITES=""

echo "=============================================="
echo "STORY-331: Progressive Disclosure Refactoring"
echo "Running All Acceptance Criteria Tests"
echo "=============================================="
echo ""
echo "Target: src/claude/agents/agent-generator.md"
echo "Goal: Reduce from 2,370 lines to <= 300 lines"
echo "----------------------------------------------"
echo ""

run_test_suite() {
    local test_file="$1"
    local test_name="$2"

    echo ">>> Running $test_name..."

    if [ ! -f "$SCRIPT_DIR/$test_file" ]; then
        echo "[ERROR] Test file not found: $test_file"
        ((TOTAL_FAILED++))
        FAILED_SUITES="$FAILED_SUITES $test_name"
        return
    fi

    chmod +x "$SCRIPT_DIR/$test_file"

    if "$SCRIPT_DIR/$test_file"; then
        TOTAL_PASSED=$((TOTAL_PASSED + 1))
        echo ">>> $test_name: PASSED"
    else
        TOTAL_FAILED=$((TOTAL_FAILED + 1))
        FAILED_SUITES="$FAILED_SUITES $test_name"
        echo ">>> $test_name: FAILED"
    fi

    echo ""
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
}

# Run all test suites
run_test_suite "test_ac1_core_file_size.sh" "AC#1: Core File Size"
run_test_suite "test_ac2_reference_directory.sh" "AC#2: Reference Directory"
run_test_suite "test_ac3_functionality_preservation.sh" "AC#3: Functionality Preservation"
run_test_suite "test_ac4_reference_loading.sh" "AC#4: Reference Loading"
run_test_suite "test_ac5_observation_capture.sh" "AC#5: Observation Capture"
run_test_suite "test_ac6_sync_verification.sh" "AC#6: Sync Verification"

# Summary
echo "=============================================="
echo "STORY-331 Test Summary"
echo "=============================================="
echo "Test Suites Run: $TOTAL_TESTS"
echo "Test Suites Passed: $TOTAL_PASSED"
echo "Test Suites Failed: $TOTAL_FAILED"
echo ""

if [ "$TOTAL_FAILED" -gt 0 ]; then
    echo "Failed Suites:$FAILED_SUITES"
    echo ""
    echo "=============================================="
    echo "OVERALL STATUS: FAILED (TDD Red Phase)"
    echo "=============================================="
    echo ""
    echo "This is expected! Tests should fail initially."
    echo "Proceed to implementation (TDD Green Phase)."
    exit 1
else
    echo "=============================================="
    echo "OVERALL STATUS: PASSED (TDD Green Phase)"
    echo "=============================================="
    echo ""
    echo "All acceptance criteria validated!"
    exit 0
fi
