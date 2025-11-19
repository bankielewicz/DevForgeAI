#!/bin/bash

##############################################################################
# Master Test Runner: STORY-042 Complete Test Suite
#
# Purpose: Execute all test suites for file migration validation
# Runs: AC tests (25), Business Rules (17), Edge Cases (28), Config (31)
# Total: ~101 test cases organized by concern
#
# Usage:
#   bash tests/STORY-042/run-tests.sh [--verbose] [--suite=NAME]
#   bash tests/STORY-042/run-tests.sh --verbose            # All tests, detailed output
#   bash tests/STORY-042/run-tests.sh --suite=ac           # AC tests only
#   bash tests/STORY-042/run-tests.sh --suite=business     # Business rules only
#   bash tests/STORY-042/run-tests.sh --suite=edge         # Edge cases only
#   bash tests/STORY-042/run-tests.sh --suite=config       # Configuration tests only
##############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Test directories and files
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_DIR="${TEST_DIR}/reports"
SUMMARY_FILE="${REPORT_DIR}/test-summary.txt"
RESULTS_FILE="${REPORT_DIR}/test-results.json"

# Test suite files
AC_TESTS="${TEST_DIR}/test-ac-migration-files.sh"
BR_TESTS="${TEST_DIR}/test-business-rules.sh"
EC_TESTS="${TEST_DIR}/test-edge-cases.sh"
CONFIG_TESTS="${TEST_DIR}/test-migration-config.sh"

# Counters
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
START_TIME=$(date +%s)

# Options
VERBOSE=false
SUITE_FILTER=""

##############################################################################
# Functions
##############################################################################

print_header() {
    local text=$1
    echo -e "\n${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} $text"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
}

print_section() {
    local text=$1
    echo -e "\n${CYAN}▶ $text${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

make_executable() {
    local file=$1
    if [ -f "$file" ]; then
        chmod +x "$file"
    fi
}

run_test_suite() {
    local suite_name=$1
    local test_file=$2
    local suite_id=$3

    if [ ! -f "$test_file" ]; then
        print_error "Test file not found: $test_file"
        return 1
    fi

    print_section "Running $suite_name Test Suite ($suite_id)"
    make_executable "$test_file"

    # Run the test suite and capture output
    local output
    local exit_code

    if [ "$VERBOSE" = true ]; then
        output=$("$test_file" 2>&1)
        exit_code=$?
    else
        output=$("$test_file" 2>&1 | grep -E "^\[Test|Tests run:|Tests passed:|Tests failed:|✓|✗")
        exit_code=$?
    fi

    echo "$output"

    # Extract counts from output
    local passed=$(echo "$output" | grep -E "Tests passed:" | awk '{print $NF}' | head -1)
    local failed=$(echo "$output" | grep -E "Tests failed:" | awk '{print $NF}' | head -1)
    local run=$(echo "$output" | grep -E "Tests run:" | awk '{print $NF}' | head -1)

    if [ -n "$run" ]; then
        TOTAL_TESTS=$((TOTAL_TESTS + run))
        TOTAL_PASSED=$((TOTAL_PASSED + ${passed:-0}))
        TOTAL_FAILED=$((TOTAL_FAILED + ${failed:-0}))
    fi

    [ "$exit_code" -eq 0 ] && print_success "$suite_name completed" || print_error "$suite_name failed"
    return $exit_code
}

create_report_directory() {
    if [ ! -d "$REPORT_DIR" ]; then
        mkdir -p "$REPORT_DIR"
    fi
}

generate_summary() {
    create_report_directory

    local elapsed=$(($(date +%s) - START_TIME))
    local min=$((elapsed / 60))
    local sec=$((elapsed % 60))

    {
        echo "═══════════════════════════════════════════════════════════"
        echo "STORY-042: File Migration Test Suite Summary"
        echo "═══════════════════════════════════════════════════════════"
        echo ""
        echo "Test Execution Details:"
        echo "  Date: $(date)"
        echo "  Duration: ${min}m ${sec}s"
        echo "  Report: $RESULTS_FILE"
        echo ""
        echo "Test Results:"
        echo "  Total Tests Run: $TOTAL_TESTS"
        echo "  Tests Passed: $TOTAL_PASSED ($([ $TOTAL_TESTS -gt 0 ] && echo $((TOTAL_PASSED * 100 / TOTAL_TESTS)) || echo 0)%)"
        echo "  Tests Failed: $TOTAL_FAILED"
        echo ""
        echo "Coverage Summary:"
        echo "  - Acceptance Criteria (AC): 25 tests"
        echo "    ├─ AC-1 (.claude/ structure): 5 tests"
        echo "    ├─ AC-2 (.devforgeai/ content): 5 tests"
        echo "    ├─ AC-3 (CLAUDE.md template): 5 tests"
        echo "    ├─ AC-4 (Checksum validation): 5 tests"
        echo "    ├─ AC-5 (Exclusions): 7 tests"
        echo "    ├─ AC-6 (Git tracking): 4 tests"
        echo "    └─ AC-7 (Preserve originals): 5 tests"
        echo ""
        echo "  - Business Rules (BR): 17 tests"
        echo "    ├─ BR-001 (Originals unchanged): 4 tests"
        echo "    ├─ BR-002 (Source files only): 6 tests"
        echo "    ├─ BR-003 (File integrity): 4 tests"
        echo "    ├─ BR-004 (Exclusion patterns): 4 tests"
        echo "    ├─ BR-005 (Idempotency): 3 tests"
        echo "    └─ BR-006 (Fail fast): 3 tests"
        echo ""
        echo "  - Edge Cases (EC): 28 tests"
        echo "    ├─ EC-1 (Existing files): 4 tests"
        echo "    ├─ EC-2 (Permission errors): 4 tests"
        echo "    ├─ EC-3 (Partial copy): 4 tests"
        echo "    ├─ EC-4 (Corruption): 4 tests"
        echo "    ├─ EC-5 (Symlinks): 4 tests"
        echo "    ├─ EC-6 (Large files): 4 tests"
        echo "    └─ EC-7 (Case conflicts): 4 tests"
        echo ""
        echo "  - Configuration (CONF): 31 tests"
        echo "    ├─ MigrationScript (Worker): 7 tests"
        echo "    ├─ MigrationConfig (Config): 6 tests"
        echo "    ├─ ChecksumManifest (Data): 5 tests"
        echo "    ├─ MigrationLogger (Logging): 6 tests"
        echo "    └─ NFRs (Non-Functional): 5 tests"
        echo ""
        echo "═══════════════════════════════════════════════════════════"

        if [ "$TOTAL_FAILED" -eq 0 ]; then
            echo -e "${GREEN}✓ ALL TESTS PASSED - Ready for implementation${NC}"
        else
            echo -e "${RED}✗ $TOTAL_FAILED tests failed - Review implementation${NC}"
        fi
        echo "═══════════════════════════════════════════════════════════"
    } | tee "$SUMMARY_FILE"
}

generate_json_results() {
    create_report_directory

    {
        echo "{"
        echo "  \"test_suite\": \"STORY-042-File-Migration\","
        echo "  \"execution_date\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
        echo "  \"test_results\": {"
        echo "    \"total_tests\": $TOTAL_TESTS,"
        echo "    \"passed\": $TOTAL_PASSED,"
        echo "    \"failed\": $TOTAL_FAILED,"
        echo "    \"pass_rate\": $([ $TOTAL_TESTS -gt 0 ] && echo "scale=2; $TOTAL_PASSED * 100 / $TOTAL_TESTS" | bc || echo "0")"
        echo "  },"
        echo "  \"components\": {"
        echo "    \"acceptance_criteria\": 25,"
        echo "    \"business_rules\": 17,"
        echo "    \"edge_cases\": 28,"
        echo "    \"configuration\": 31"
        echo "  },"
        echo "  \"status\": \"$([ $TOTAL_FAILED -eq 0 ] && echo 'PASS' || echo 'FAIL')\""
        echo "}"
    } > "$RESULTS_FILE"
}

show_usage() {
    cat << EOF
${BLUE}STORY-042 Test Suite Runner${NC}

Usage:
  bash $(basename "$0") [OPTIONS]

Options:
  --help              Show this help message
  --verbose           Show detailed test output
  --suite=NAME        Run specific test suite only
                      NAME: ac, business, edge, config, or all (default)
  --report-only       Generate report without running tests

Test Suites:
  ac       - Acceptance Criteria Tests (25 tests)
  business - Business Rules Tests (17 tests)
  edge     - Edge Cases Tests (28 tests)
  config   - Configuration Tests (31 tests)

Examples:
  # Run all tests with verbose output
  bash run-tests.sh --verbose

  # Run only acceptance criteria tests
  bash run-tests.sh --suite=ac

  # Run all tests silently and generate summary
  bash run-tests.sh

${BLUE}═══════════════════════════════════════════════════════════${NC}
EOF
}

##############################################################################
# Parse Command Line Arguments
##############################################################################

while [ $# -gt 0 ]; do
    case "$1" in
        --help)
            show_usage
            exit 0
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --suite=*)
            SUITE_FILTER="${1#--suite=}"
            shift
            ;;
        --report-only)
            generate_summary
            generate_json_results
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

##############################################################################
# Main Test Execution
##############################################################################

print_header "STORY-042: File Migration - Complete Test Suite"

echo "Starting test execution..."
echo "  Report directory: $REPORT_DIR"
echo "  Verbose mode: $VERBOSE"
[ -n "$SUITE_FILTER" ] && echo "  Running suite: $SUITE_FILTER" || echo "  Running all suites"

FAILED_SUITES=0

# Run selected test suites
if [ -z "$SUITE_FILTER" ] || [ "$SUITE_FILTER" = "all" ] || [ "$SUITE_FILTER" = "ac" ]; then
    run_test_suite "Acceptance Criteria" "$AC_TESTS" "AC" || FAILED_SUITES=$((FAILED_SUITES + 1))
fi

if [ -z "$SUITE_FILTER" ] || [ "$SUITE_FILTER" = "all" ] || [ "$SUITE_FILTER" = "business" ]; then
    run_test_suite "Business Rules" "$BR_TESTS" "BR" || FAILED_SUITES=$((FAILED_SUITES + 1))
fi

if [ -z "$SUITE_FILTER" ] || [ "$SUITE_FILTER" = "all" ] || [ "$SUITE_FILTER" = "edge" ]; then
    run_test_suite "Edge Cases" "$EC_TESTS" "EC" || FAILED_SUITES=$((FAILED_SUITES + 1))
fi

if [ -z "$SUITE_FILTER" ] || [ "$SUITE_FILTER" = "all" ] || [ "$SUITE_FILTER" = "config" ]; then
    run_test_suite "Configuration" "$CONFIG_TESTS" "CONF" || FAILED_SUITES=$((FAILED_SUITES + 1))
fi

# Generate reports
generate_summary
generate_json_results

# Final status
print_header "Test Execution Complete"
echo ""
echo "Results Summary:"
echo "  Total: $TOTAL_TESTS tests"
echo "  Passed: ${GREEN}$TOTAL_PASSED${NC}"
echo "  Failed: ${RED}$TOTAL_FAILED${NC}"
echo ""
echo "Reports:"
echo "  Summary: $SUMMARY_FILE"
echo "  JSON: $RESULTS_FILE"
echo ""

# Exit with appropriate code
if [ "$FAILED_SUITES" -eq 0 ] && [ "$TOTAL_FAILED" -eq 0 ]; then
    print_success "All tests passed! Ready for Phase 2 implementation."
    exit 0
else
    print_error "$FAILED_SUITES suite(s) failed, $TOTAL_FAILED test(s) failed."
    exit 1
fi
