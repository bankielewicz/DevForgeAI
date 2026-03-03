#!/bin/bash
# Test Runner: STORY-397 - Batch Rollout Wave 3
# Executes all AC test suites and provides consolidated results
# Generated: 2026-02-13

set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_TESTS=0
SUITE_RESULTS=()

echo "================================================================="
echo "  STORY-397: Batch Rollout Wave 3 - Full Test Suite"
echo "  Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "================================================================="
echo ""

run_suite() {
    local suite_file="$1"
    local suite_name="$2"
    local suite_exit=0

    echo ""
    echo "-----------------------------------------------------------------"
    echo "  Running: ${suite_name}"
    echo "-----------------------------------------------------------------"

    if [ -f "${SCRIPT_DIR}/${suite_file}" ]; then
        bash "${SCRIPT_DIR}/${suite_file}"
        suite_exit=$?
    else
        echo "  ERROR: Test file not found: ${suite_file}"
        suite_exit=99
    fi

    if [ "$suite_exit" -eq 0 ]; then
        SUITE_RESULTS+=("  PASS  ${suite_name}")
    else
        SUITE_RESULTS+=("  FAIL  ${suite_name}")
        ((TOTAL_FAILED++))
    fi
    ((TOTAL_TESTS++))

    return $suite_exit
}

# Execute all test suites (continue even if one fails)
run_suite "test_ac1_template_conformance.sh" "AC#1: Template Conformance (17 Agents)" || true
run_suite "test_ac2_anthropic_patterns.sh"   "AC#2: Anthropic Patterns" || true
run_suite "test_ac3_skill_improvements.sh"   "AC#3: Skill Improvements (17 Skills)" || true
run_suite "test_ac4_command_improvements.sh" "AC#4: Command Improvements (39 Commands)" || true
run_suite "test_ac5_agent_generator_last.sh" "AC#5: agent-generator Last" || true
run_suite "test_ac6_regression_validation.sh" "AC#6: Regression Validation" || true

# Consolidated results
echo ""
echo "================================================================="
echo "  STORY-397: Consolidated Results"
echo "================================================================="
for result in "${SUITE_RESULTS[@]}"; do
    echo "$result"
done
echo ""
echo "  Suites: ${TOTAL_TESTS} total"
echo "  Failed suites: ${TOTAL_FAILED}"
echo "================================================================="

if [ "$TOTAL_FAILED" -eq 0 ]; then
    echo "  STATUS: ALL SUITES PASSED"
    exit 0
else
    echo "  STATUS: ${TOTAL_FAILED} SUITE(S) FAILED"
    exit 1
fi
