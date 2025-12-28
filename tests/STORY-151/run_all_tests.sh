#!/usr/bin/env bash

# STORY-151: Post-Subagent Recording Hook - Test Suite Runner
# Runs all unit and integration tests for the hook

set -euo pipefail

# Setup
readonly TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${TEST_DIR}/../../" && pwd)"

# Color codes
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m'

# Counters
total_tests=0
total_passed=0
total_failed=0
failed_test_files=()

# Test suites
readonly UNIT_TESTS=(
    "unit/test_hook_registration.sh"
    "unit/test_story_context_extraction.sh"
    "unit/test_subagent_filtering.sh"
    "unit/test_state_file_handling.sh"
    "unit/test_logging.sh"
)

readonly INTEGRATION_TESTS=(
    "integration/test_full_recording_workflow.sh"
)

# Functions
print_header() {
    echo ""
    echo -e "${CYAN}========================================================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================================================${NC}"
}

run_test_suite() {
    local test_file="$1"
    local full_path="$TEST_DIR/$test_file"

    if [[ ! -f "$full_path" ]]; then
        echo -e "${RED}ERROR: Test file not found: $full_path${NC}"
        return 1
    fi

    echo ""
    echo -e "${YELLOW}Running: $test_file${NC}"
    echo "────────────────────────────────────────────────────────────────────────────"

    # Make test file executable
    chmod +x "$full_path"

    # Run test and capture results
    if "$full_path"; then
        echo -e "${GREEN}✓ Test suite passed${NC}"
        return 0
    else
        local exit_code=$?
        echo -e "${RED}✗ Test suite failed (exit code: $exit_code)${NC}"
        failed_test_files+=("$test_file")
        return 1
    fi
}

# MAIN EXECUTION
print_header "STORY-151: Post-Subagent Recording Hook - Test Suite"

echo ""
echo "Project Root: $PROJECT_ROOT"
echo "Test Directory: $TEST_DIR"
echo ""

# Run unit tests
print_header "UNIT TESTS"
echo "Testing individual components (hooks, extraction, filtering, state handling, logging)"
echo ""

for test_file in "${UNIT_TESTS[@]}"; do
    if run_test_suite "$test_file"; then
        ((total_passed++)) || true
    else
        ((total_failed++)) || true
    fi
    ((total_tests++)) || true
done

# Run integration tests
print_header "INTEGRATION TESTS"
echo "Testing end-to-end workflows and component interactions"
echo ""

for test_file in "${INTEGRATION_TESTS[@]}"; do
    if run_test_suite "$test_file"; then
        ((total_passed++)) || true
    else
        ((total_failed++)) || true
    fi
    ((total_tests++)) || true
done

# Print final summary
print_header "FINAL TEST SUMMARY"

echo "Total Test Suites: $total_tests"
echo -e "Passed: ${GREEN}$total_passed${NC}"
echo -e "Failed: ${RED}$total_failed${NC}"

if [[ $total_failed -gt 0 ]]; then
    echo ""
    echo -e "${RED}Failed test suites:${NC}"
    for failed_test in "${failed_test_files[@]}"; do
        echo -e "  ${RED}✗${NC} $failed_test"
    done
    echo ""
    echo -e "${YELLOW}Note: Test failures are expected in TDD Red phase${NC}"
    echo -e "${YELLOW}Tests SHOULD fail because implementation doesn't exist yet.${NC}"
    echo ""
fi

# Expected behavior in Red phase
echo -e "${CYAN}Expected Behavior (TDD Red Phase):${NC}"
echo "All tests SHOULD FAIL because:"
echo "  • Hook script (devforgeai/hooks/post-subagent-recording.sh) doesn't exist"
echo "  • Hook not registered in .claude/hooks.yaml"
echo "  • Config file (devforgeai/config/workflow-subagents.yaml) doesn't exist"
echo "  • Log path doesn't exist"
echo ""
echo "This is correct for TDD Red phase - tests drive implementation."
echo ""

# Exit with appropriate code
if [[ $total_failed -gt 0 ]]; then
    echo -e "${YELLOW}Phase: TDD Red (Failing Tests - Expected)${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed! (Move to Phase 03: Implementation)${NC}"
    exit 0
fi
