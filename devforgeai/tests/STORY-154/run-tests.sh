#!/usr/bin/env bash
#
# TEST RUNNER: STORY-154 Integration Tests
#
# Executes all 6 failing test scripts for Phase Execution Enforcement
#
# Usage:
#   ./run-tests.sh                    # Run all tests
#   ./run-tests.sh test-rca022-*.sh   # Run specific test
#   ./run-tests.sh --help             # Show help
#
# Exit Code Contract:
#   0 = All tests passed
#   1 = One or more tests failed
#   2 = Invalid usage
#

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT="${PROJECT_ROOT:-.}"
TEST_DIR="${PROJECT_ROOT}/devforgeai/tests/STORY-154"
LOG_DIR="${TEST_DIR}/test-logs"
REPORT_FILE="${TEST_DIR}/TEST-RESULTS.md"

# Make sure directories exist
mkdir -p "${LOG_DIR}"

# ============================================================================
# COLORS FOR OUTPUT
# ============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# FUNCTIONS
# ============================================================================

print_header() {
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================================${NC}"
}

print_test_start() {
    echo -e "${BLUE}Starting: $1${NC}"
}

print_test_pass() {
    echo -e "${GREEN}✓ PASSED: $1${NC}"
}

print_test_fail() {
    echo -e "${RED}✗ FAILED: $1${NC}"
}

print_error() {
    echo -e "${RED}Error: $1${NC}" >&2
}

print_warning() {
    echo -e "${YELLOW}Warning: $1${NC}"
}

show_help() {
    cat << 'EOF'
STORY-154 Integration Test Runner

Usage:
  ./run-tests.sh [OPTIONS] [PATTERN]

OPTIONS:
  --help              Show this help message
  --verbose           Verbose output
  --no-cleanup        Don't cleanup test artifacts
  --fast              Stop on first failure

PATTERN:
  Glob pattern to select tests (default: test-*.sh)
  Examples:
    test-rca022-*.sh       Run only RCA-022 test
    test-complete-*.sh     Run only complete workflow test
    test-*                 Run all tests (default)

EXAMPLES:
  Run all tests:
    ./run-tests.sh

  Run specific test:
    ./run-tests.sh test-rca022-scenario-blocked.sh

  Run with verbose output:
    ./run-tests.sh --verbose

Exit Codes:
  0 = All tests passed
  1 = One or more tests failed
  2 = Invalid usage

Test Results:
  Individual test logs: devforgeai/tests/STORY-154/test-logs/
  Overall report: devforgeai/tests/STORY-154/TEST-RESULTS.md
EOF
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

# Parse command line arguments
VERBOSE=false
NO_CLEANUP=false
FAST_FAIL=false
TEST_PATTERN="test-*.sh"

while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            show_help
            exit 0
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --no-cleanup)
            NO_CLEANUP=true
            shift
            ;;
        --fast)
            FAST_FAIL=true
            shift
            ;;
        -*)
            print_error "Unknown option: $1"
            show_help
            exit 2
            ;;
        *)
            TEST_PATTERN="$1"
            shift
            ;;
    esac
done

print_header "STORY-154 Integration Test Suite"
echo "Project Root: ${PROJECT_ROOT}"
echo "Test Directory: ${TEST_DIR}"
echo "Test Pattern: ${TEST_PATTERN}"
echo "Verbose Mode: ${VERBOSE}"
echo "Fast Fail Mode: ${FAST_FAIL}"
echo ""

# Change to project root
cd "${PROJECT_ROOT}"

# ============================================================================
# DISCOVERY AND EXECUTION
# ============================================================================

# Find all matching test scripts
mapfile -t TESTS < <(cd "${TEST_DIR}" && find . -maxdepth 1 -name "${TEST_PATTERN}" -type f | sort)

if [[ ${#TESTS[@]} -eq 0 ]]; then
    print_error "No tests found matching pattern: ${TEST_PATTERN}"
    exit 2
fi

echo "Found ${#TESTS[@]} test(s):"
for test in "${TESTS[@]}"; do
    echo "  - ${test}"
done
echo ""

# ============================================================================
# TEST EXECUTION
# ============================================================================

PASSED=0
FAILED=0
FAILED_TESTS=()
START_TIME=$(date +%s)

for test in "${TESTS[@]}"; do
    TEST_NAME=$(basename "$test")
    TEST_PATH="${TEST_DIR}/${test#./}"

    print_test_start "${TEST_NAME}"

    # Make test executable
    chmod +x "${TEST_PATH}"

    # Run test with timeout
    TEST_LOG="${LOG_DIR}/${TEST_NAME%.sh}.log"

    if timeout 30 bash "${TEST_PATH}" > "${TEST_LOG}" 2>&1; then
        PASSED=$((PASSED + 1))
        print_test_pass "${TEST_NAME}"

        if [[ "$VERBOSE" == "true" ]]; then
            echo "  Log: ${TEST_LOG}"
            echo "  First 10 lines of output:"
            head -n 10 "${TEST_LOG}" | sed 's/^/    /'
            echo ""
        fi
    else
        EXIT_CODE=$?
        FAILED=$((FAILED + 1))
        FAILED_TESTS+=("${TEST_NAME}")
        print_test_fail "${TEST_NAME} (exit code: ${EXIT_CODE})"

        if [[ "$VERBOSE" == "true" || "$FAST_FAIL" == "true" ]]; then
            echo "  Log: ${TEST_LOG}"
            echo "  Full output:"
            cat "${TEST_LOG}" | sed 's/^/    /'
            echo ""
        fi

        if [[ "$FAST_FAIL" == "true" ]]; then
            print_error "Fast fail mode: stopping test execution"
            break
        fi
    fi
done

# ============================================================================
# RESULTS SUMMARY
# ============================================================================

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
print_header "Test Execution Summary"
echo "Total Tests: ${#TESTS[@]}"
echo "Passed: ${PASSED}"
echo "Failed: ${FAILED}"
echo "Duration: ${DURATION} seconds"
echo ""

# ============================================================================
# REPORT GENERATION
# ============================================================================

{
    echo "# STORY-154 Integration Test Results"
    echo ""
    echo "**Date**: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "**Duration**: ${DURATION} seconds"
    echo ""
    echo "## Summary"
    echo ""
    echo "| Metric | Value |"
    echo "|--------|-------|"
    echo "| Total Tests | ${#TESTS[@]} |"
    echo "| Passed | ${PASSED} |"
    echo "| Failed | ${FAILED} |"
    echo "| Pass Rate | $((PASSED * 100 / ${#TESTS[@]}))% |"
    echo ""

    if [[ ${FAILED} -eq 0 ]]; then
        echo "## Result: PASSED ✓"
        echo ""
        echo "All acceptance criteria tests passed successfully."
        echo ""
    else
        echo "## Result: FAILED ✗"
        echo ""
        echo "Failed Tests:"
        for test in "${FAILED_TESTS[@]}"; do
            echo "- ${test}"
        done
        echo ""
    fi

    echo "## Test Details"
    echo ""

    for test in "${TESTS[@]}"; do
        TEST_NAME=$(basename "$test")
        TEST_LOG="${LOG_DIR}/${TEST_NAME%.sh}.log"

        if [[ -f "$TEST_LOG" ]]; then
            echo "### ${TEST_NAME}"
            echo ""
            echo "\`\`\`"
            head -n 30 "${TEST_LOG}"
            echo "\`\`\`"
            echo ""
        fi
    done

    echo "## Log Files"
    echo ""
    echo "Individual test logs are available in: \`devforgeai/tests/STORY-154/test-logs/\`"
    echo ""

} | tee "${REPORT_FILE}"

# ============================================================================
# CLEANUP
# ============================================================================

if [[ "${NO_CLEANUP}" != "true" && ${FAILED} -eq 0 ]]; then
    echo ""
    echo "Cleanup: Removing test artifacts..."

    # Only clean up on success
    rm -f "${LOG_DIR}"/*.log 2>/dev/null || true
    rm -f "${TEST_DIR}/test-workflows"/*.json 2>/dev/null || true
fi

# ============================================================================
# EXIT CODE
# ============================================================================

echo ""
if [[ ${FAILED} -eq 0 ]]; then
    print_header "All Tests Passed!"
    exit 0
else
    print_header "Some Tests Failed"
    exit 1
fi
