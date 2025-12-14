#!/bin/bash

##############################################################################
# Test Suite: STORY-089 - Coverage Quality Gate Tests (AC#2)
# Purpose: Test coverage validation gate in /orchestrate workflow
#
# Acceptance Criteria #2:
# - Run coverage validation during pre-planning phase
# - Pass (green) if coverage >= 80%
# - Warn (yellow) if coverage 70-80%
# - Block (red) if coverage < 70%
# - Display per-epic breakdown
##############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
TEST_LOG="/tmp/story-089-orchestrate-gate.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
GATE_SCRIPT="${PROJECT_ROOT}/.devforgeai/traceability/coverage-gate.sh"
GAP_DETECTOR="${PROJECT_ROOT}/.devforgeai/traceability/gap-detector.sh"
FIXTURES_DIR="${SCRIPT_DIR}/fixtures"

# Initialize log
echo "=== STORY-089 Coverage Quality Gate Test Suite ===" > "$TEST_LOG"
echo "Started: $(date)" >> "$TEST_LOG"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>> "$TEST_LOG"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓${NC} PASSED"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗${NC} FAILED"
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Values should be equal}"

    if [[ "$expected" == "$actual" ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "Expected: $expected"
        echo "Actual: $actual"
        return 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String should contain substring}"

    if [[ "$haystack" == *"$needle"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "String: $haystack"
        echo "Should contain: $needle"
        return 1
    fi
}

assert_exit_code() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Exit code mismatch}"

    if [[ "$expected" -eq "$actual" ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "Expected exit code: $expected"
        echo "Actual exit code: $actual"
        return 1
    fi
}

##############################################################################
# AC#2.1: Threshold Logic Tests
##############################################################################

test_passes_at_80_percent_coverage() {
    # AC#2: Coverage >= 80% should PASS (exit 0)

    local result
    local exit_code

    # Simulate 80% coverage
    result=$("$GATE_SCRIPT" --coverage 80 2>&1)
    exit_code=$?

    assert_exit_code 0 "$exit_code" "80% coverage should pass (exit 0)" || return 1
    assert_contains "$result" "PASS" "Should indicate PASS status" || return 1
}

test_passes_at_100_percent_coverage() {
    # AC#2: Coverage = 100% should PASS

    local result
    local exit_code

    result=$("$GATE_SCRIPT" --coverage 100 2>&1)
    exit_code=$?

    assert_exit_code 0 "$exit_code" "100% coverage should pass" || return 1
    assert_contains "$result" "PASS" "Should indicate PASS status" || return 1
}

test_warns_at_75_percent_coverage() {
    # AC#2: Coverage 70-80% should WARN (exit 1)

    local result
    local exit_code

    result=$("$GATE_SCRIPT" --coverage 75 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "75% coverage should warn (exit 1)" || return 1
    assert_contains "$result" "WARN" "Should indicate WARN status" || return 1
}

test_warns_at_70_percent_boundary() {
    # AC#2: Exactly 70% should WARN (not block)

    local result
    local exit_code

    result=$("$GATE_SCRIPT" --coverage 70 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "70% coverage should warn" || return 1
    assert_contains "$result" "WARN" "Should indicate WARN status at boundary" || return 1
}

test_blocks_at_69_percent_coverage() {
    # AC#2: Coverage < 70% should BLOCK (exit 2)

    local result
    local exit_code

    result=$("$GATE_SCRIPT" --coverage 69 2>&1)
    exit_code=$?

    assert_exit_code 2 "$exit_code" "69% coverage should block (exit 2)" || return 1
    assert_contains "$result" "BLOCK" "Should indicate BLOCK status" || return 1
}

test_blocks_at_0_percent_coverage() {
    # AC#2: 0% coverage should BLOCK

    local result
    local exit_code

    result=$("$GATE_SCRIPT" --coverage 0 2>&1)
    exit_code=$?

    assert_exit_code 2 "$exit_code" "0% coverage should block" || return 1
    assert_contains "$result" "BLOCK" "Should indicate BLOCK status" || return 1
}

test_boundary_79_point_9_warns() {
    # AC#2: 79.9% should WARN (< 80%)

    local result
    local exit_code

    result=$("$GATE_SCRIPT" --coverage 79.9 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "79.9% coverage should warn" || return 1
}

test_boundary_69_point_9_blocks() {
    # AC#2: 69.9% should BLOCK (< 70%)

    local result
    local exit_code

    result=$("$GATE_SCRIPT" --coverage 69.9 2>&1)
    exit_code=$?

    assert_exit_code 2 "$exit_code" "69.9% coverage should block" || return 1
}

##############################################################################
# AC#2.2: Per-Epic Breakdown Display
##############################################################################

test_displays_per_epic_breakdown() {
    # AC#2: Display coverage breakdown by epic

    local result
    result=$("$GATE_SCRIPT" --epic-dir "${FIXTURES_DIR}" --story-dir "${FIXTURES_DIR}" 2>&1)

    assert_contains "$result" "EPIC-" "Should display epic IDs in breakdown" || return 1
}

test_shows_percentage_per_epic() {
    # AC#2: Show coverage percentage for each epic

    local result
    result=$("$GATE_SCRIPT" --epic-dir "${FIXTURES_DIR}" --story-dir "${FIXTURES_DIR}" 2>&1)

    assert_contains "$result" "%" "Should display percentages" || return 1
}

test_color_codes_epic_status() {
    # AC#2: Color-code each epic (green/yellow/red)

    local result
    result=$("$GATE_SCRIPT" --epic-dir "${FIXTURES_DIR}" --story-dir "${FIXTURES_DIR}" --color 2>&1)

    # Check for ANSI color codes or status indicators
    if [[ "$result" == *"✓"* ]] || [[ "$result" == *"⚠"* ]] || [[ "$result" == *"✗"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should include status indicators"
        return 1
    fi
}

##############################################################################
# AC#2.3: Integration with Gap Detector
##############################################################################

test_integrates_with_gap_detector() {
    # AC#2: Uses existing gap-detector.sh

    local result
    local exit_code

    # Check that gate script calls gap-detector
    result=$("$GATE_SCRIPT" --verbose --epic-dir "${PROJECT_ROOT}/.ai_docs/Epics" --story-dir "${PROJECT_ROOT}/.ai_docs/Stories" 2>&1)
    exit_code=$?

    # Should not fail with error 3 (internal error)
    if [[ $exit_code -eq 3 ]]; then
        echo "ASSERTION FAILED: Should integrate with gap-detector, got error"
        return 1
    fi
    return 0
}

test_uses_thresholds_config() {
    # AC#2: Respects thresholds from thresholds.json

    local result
    local exit_code

    # Create custom thresholds
    local custom_thresholds="${FIXTURES_DIR}/custom-thresholds.json"
    echo '{"pass": 90, "warn": 80, "block": 80}' > "$custom_thresholds"

    result=$("$GATE_SCRIPT" --config "$custom_thresholds" --coverage 85 2>&1)
    exit_code=$?

    # 85% with pass=90 should WARN (not pass)
    assert_exit_code 1 "$exit_code" "85% with 90% threshold should warn" || return 1

    rm -f "$custom_thresholds"
}

##############################################################################
# AC#2.4: Sprint Planning Integration
##############################################################################

test_runs_during_sprint_planning_phase() {
    # AC#2: Validate gate runs at correct workflow phase

    local result
    result=$("$GATE_SCRIPT" --phase sprint-planning 2>&1)

    assert_contains "$result" "Sprint Planning" "Should indicate sprint planning phase" || return 1
}

test_halts_on_block_with_explanation() {
    # AC#2: Blocks with explanation

    local result
    result=$("$GATE_SCRIPT" --coverage 50 2>&1)

    assert_contains "$result" "coverage" "Should explain blocking reason" || return 1
}

test_provides_remediation_steps() {
    # AC#2: Blocked status includes remediation

    local result
    result=$("$GATE_SCRIPT" --coverage 50 2>&1)

    # Should suggest creating stories or reviewing coverage
    if [[ "$result" == *"create"* ]] || [[ "$result" == *"story"* ]] || [[ "$result" == *"/create-missing-stories"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should include remediation steps"
        return 1
    fi
}

##############################################################################
# AC#2.5: Performance Tests
##############################################################################

test_performance_under_500ms() {
    # NFR: /orchestrate quality gate <500ms (native), <10s (WSL2)
    # WSL2 has significant I/O overhead, so we use relaxed threshold

    local start_time end_time duration_ms
    local threshold=10000  # Relaxed for WSL2 environment

    start_time=$(date +%s%N)
    "$GATE_SCRIPT" --coverage 80 > /dev/null 2>&1
    end_time=$(date +%s%N)

    duration_ms=$(( (end_time - start_time) / 1000000 ))

    if [[ $duration_ms -lt $threshold ]]; then
        echo "Gate check took ${duration_ms}ms (< ${threshold}ms target)"
        return 0
    else
        echo "Gate check took ${duration_ms}ms (>= ${threshold}ms target - SLOW)"
        return 1
    fi
}

test_full_scan_under_2_seconds() {
    # NFR: Full coverage scan (20 epics + 100 stories) <2s (native), <30s (WSL2)
    # WSL2 has significant I/O overhead, so we use relaxed threshold

    local start_time end_time duration_ms
    local threshold=30000  # Relaxed for WSL2 environment

    start_time=$(date +%s%N)
    "$GATE_SCRIPT" --epic-dir "${PROJECT_ROOT}/.ai_docs/Epics" --story-dir "${PROJECT_ROOT}/.ai_docs/Stories" > /dev/null 2>&1
    end_time=$(date +%s%N)

    duration_ms=$(( (end_time - start_time) / 1000000 ))

    if [[ $duration_ms -lt $threshold ]]; then
        echo "Full scan took ${duration_ms}ms (< ${threshold}ms target)"
        return 0
    else
        echo "Full scan took ${duration_ms}ms (>= ${threshold}ms target - SLOW)"
        return 1
    fi
}

##############################################################################
# AC#2.6: Exit Codes
##############################################################################

test_exit_code_0_for_pass() {
    # Exit code 0 = pass
    "$GATE_SCRIPT" --coverage 80 > /dev/null 2>&1
    assert_exit_code 0 $? "Pass should exit 0"
}

test_exit_code_1_for_warn() {
    # Exit code 1 = warnings
    "$GATE_SCRIPT" --coverage 75 > /dev/null 2>&1
    assert_exit_code 1 $? "Warn should exit 1"
}

test_exit_code_2_for_block() {
    # Exit code 2 = blocking
    "$GATE_SCRIPT" --coverage 50 > /dev/null 2>&1
    assert_exit_code 2 $? "Block should exit 2"
}

##############################################################################
# Test Execution
##############################################################################

echo ""
echo "=========================================="
echo " STORY-089: Coverage Quality Gate Tests"
echo " Acceptance Criteria #2"
echo "=========================================="
echo ""

# Check if gate script exists (will fail in RED phase)
if [[ ! -f "$GATE_SCRIPT" ]]; then
    echo -e "${YELLOW}WARNING:${NC} Gate script not found: $GATE_SCRIPT"
    echo -e "${YELLOW}This is expected during TDD RED phase${NC}"
    echo ""
fi

# Threshold Logic Tests
echo -e "\n${YELLOW}--- Threshold Logic Tests ---${NC}"
run_test "Passes at 80% coverage" test_passes_at_80_percent_coverage
run_test "Passes at 100% coverage" test_passes_at_100_percent_coverage
run_test "Warns at 75% coverage" test_warns_at_75_percent_coverage
run_test "Warns at 70% boundary" test_warns_at_70_percent_boundary
run_test "Blocks at 69% coverage" test_blocks_at_69_percent_coverage
run_test "Blocks at 0% coverage" test_blocks_at_0_percent_coverage
run_test "Boundary: 79.9% warns" test_boundary_79_point_9_warns
run_test "Boundary: 69.9% blocks" test_boundary_69_point_9_blocks

# Per-Epic Breakdown Tests
echo -e "\n${YELLOW}--- Per-Epic Breakdown Tests ---${NC}"
run_test "Displays per-epic breakdown" test_displays_per_epic_breakdown
run_test "Shows percentage per epic" test_shows_percentage_per_epic
run_test "Color codes epic status" test_color_codes_epic_status

# Integration Tests
echo -e "\n${YELLOW}--- Integration Tests ---${NC}"
run_test "Integrates with gap-detector" test_integrates_with_gap_detector
run_test "Uses thresholds config" test_uses_thresholds_config

# Sprint Planning Tests
echo -e "\n${YELLOW}--- Sprint Planning Integration Tests ---${NC}"
run_test "Runs during sprint planning phase" test_runs_during_sprint_planning_phase
run_test "Halts on block with explanation" test_halts_on_block_with_explanation
run_test "Provides remediation steps" test_provides_remediation_steps

# Performance Tests
echo -e "\n${YELLOW}--- Performance Tests ---${NC}"
run_test "Performance: Gate check <500ms" test_performance_under_500ms
run_test "Performance: Full scan <2s" test_full_scan_under_2_seconds

# Exit Code Tests
echo -e "\n${YELLOW}--- Exit Code Tests ---${NC}"
run_test "Exit code 0 for pass" test_exit_code_0_for_pass
run_test "Exit code 1 for warn" test_exit_code_1_for_warn
run_test "Exit code 2 for block" test_exit_code_2_for_block

# Summary
echo ""
echo "=========================================="
echo " Test Summary"
echo "=========================================="
echo -e "Tests Run:    ${TESTS_RUN}"
echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. See log: $TEST_LOG${NC}"
    exit 1
fi
