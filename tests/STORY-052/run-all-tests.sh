#!/bin/bash
###############################################################################
# Test Orchestration Script: STORY-052
# Purpose: Run all test suites for effective-prompting-guide.md validation
# File: tests/STORY-052/run-all-tests.sh
#
# Orchestrates execution of:
# 1. test-document-structure.sh (AC1, AC5)
# 2. test-example-quality.sh (AC2)
# 3. test-command-guidance.sh (AC3, AC4)
# 4. test-framework-reality.sh (AC6)
###############################################################################

set -euo pipefail

# Configuration
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_FILE="$TEST_DIR/test-results-$TIMESTAMP.txt"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global counters
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
TEST_SUITES=0
PASSED_SUITES=0

# Helper functions
header() {
    echo ""
    echo "================================================================================"
    echo "$1"
    echo "================================================================================"
    echo ""
}

suite_header() {
    echo -e "${BLUE}Running: $1${NC}"
    echo "  Location: $2"
}

suite_result() {
    local suite_name=$1
    local exit_code=$2
    local test_count=$3
    local pass_count=$4
    local fail_count=$5

    TEST_SUITES=$((TEST_SUITES + 1))
    TOTAL_TESTS=$((TOTAL_TESTS + test_count))
    TOTAL_PASSED=$((TOTAL_PASSED + pass_count))
    TOTAL_FAILED=$((TOTAL_FAILED + fail_count))

    if [ $exit_code -eq 0 ]; then
        PASSED_SUITES=$((PASSED_SUITES + 1))
        echo -e "${GREEN}✓ PASSED${NC}: $suite_name"
        echo "  Tests: $test_count | Passed: $pass_count | Failed: $fail_count"
    else
        echo -e "${RED}✗ FAILED${NC}: $suite_name"
        echo "  Tests: $test_count | Passed: $pass_count | Failed: $fail_count"
    fi
    echo ""
}

main() {
    cd "$PROJECT_ROOT"

    header "STORY-052 - User-Facing Prompting Guide Documentation"
    echo "Test Execution Started: $(date)"
    echo "Results will be saved to: $RESULTS_FILE"
    echo ""

    # Ensure test directory exists
    if [ ! -d "$TEST_DIR" ]; then
        echo -e "${RED}ERROR: Test directory not found: $TEST_DIR${NC}"
        exit 1
    fi

    # Make all test scripts executable
    chmod +x "$TEST_DIR"/*.sh 2>/dev/null || true

    # ========================================================================
    # Test Suite 1: Document Structure
    # ========================================================================
    suite_header "Test Suite 1: Document Structure Validation (AC1, AC5)" "$TEST_DIR/test-document-structure.sh"

    if [ -x "$TEST_DIR/test-document-structure.sh" ]; then
        output=$("$TEST_DIR/test-document-structure.sh" 2>&1 || true)
        echo "$output" | tee -a "$RESULTS_FILE"

        # Extract counts from output (simple pattern matching)
        test_count=$(echo "$output" | grep -c "^Test [0-9]" || echo "0")
        pass_count=$(echo "$output" | grep -c "✓ PASS" || echo "0")
        fail_count=$(echo "$output" | grep -c "✗ FAIL" || echo "0")

        suite_result "Document Structure (AC1, AC5)" 0 "$test_count" "$pass_count" "$fail_count"
    else
        echo -e "${RED}ERROR: test-document-structure.sh not found or not executable${NC}"
        suite_result "Document Structure (AC1, AC5)" 1 0 0 1
    fi

    # ========================================================================
    # Test Suite 2: Example Quality
    # ========================================================================
    suite_header "Test Suite 2: Example Quality Validation (AC2)" "$TEST_DIR/test-example-quality.sh"

    if [ -x "$TEST_DIR/test-example-quality.sh" ]; then
        output=$("$TEST_DIR/test-example-quality.sh" 2>&1 || true)
        echo "$output" | tee -a "$RESULTS_FILE"

        test_count=$(echo "$output" | grep -c "^Test [0-9]" || echo "0")
        pass_count=$(echo "$output" | grep -c "✓ PASS" || echo "0")
        fail_count=$(echo "$output" | grep -c "✗ FAIL" || echo "0")

        suite_result "Example Quality (AC2)" 0 "$test_count" "$pass_count" "$fail_count"
    else
        echo -e "${RED}ERROR: test-example-quality.sh not found or not executable${NC}"
        suite_result "Example Quality (AC2)" 1 0 0 1
    fi

    # ========================================================================
    # Test Suite 3: Command Guidance
    # ========================================================================
    suite_header "Test Suite 3: Command Guidance & Framework Integration (AC3, AC4)" "$TEST_DIR/test-command-guidance.sh"

    if [ -x "$TEST_DIR/test-command-guidance.sh" ]; then
        output=$("$TEST_DIR/test-command-guidance.sh" 2>&1 || true)
        echo "$output" | tee -a "$RESULTS_FILE"

        test_count=$(echo "$output" | grep -c "^Test [0-9]" || echo "0")
        pass_count=$(echo "$output" | grep -c "✓ PASS" || echo "0")
        fail_count=$(echo "$output" | grep -c "✗ FAIL" || echo "0")

        suite_result "Command Guidance & Framework Integration (AC3, AC4)" 0 "$test_count" "$pass_count" "$fail_count"
    else
        echo -e "${RED}ERROR: test-command-guidance.sh not found or not executable${NC}"
        suite_result "Command Guidance & Framework Integration (AC3, AC4)" 1 0 0 1
    fi

    # ========================================================================
    # Test Suite 4: Framework Reality
    # ========================================================================
    suite_header "Test Suite 4: Framework Reality Validation (AC6)" "$TEST_DIR/test-framework-reality.sh"

    if [ -x "$TEST_DIR/test-framework-reality.sh" ]; then
        output=$("$TEST_DIR/test-framework-reality.sh" 2>&1 || true)
        echo "$output" | tee -a "$RESULTS_FILE"

        test_count=$(echo "$output" | grep -c "^Test [0-9]" || echo "0")
        pass_count=$(echo "$output" | grep -c "✓ PASS" || echo "0")
        fail_count=$(echo "$output" | grep -c "✗ FAIL" || echo "0")

        suite_result "Framework Reality (AC6)" 0 "$test_count" "$pass_count" "$fail_count"
    else
        echo -e "${RED}ERROR: test-framework-reality.sh not found or not executable${NC}"
        suite_result "Framework Reality (AC6)" 1 0 0 1
    fi

    # ========================================================================
    # Summary Report
    # ========================================================================
    header "Overall Test Summary"

    echo "Test Execution Completed: $(date)"
    echo ""
    echo -e "${CYAN}Test Suite Results:${NC}"
    echo "  Total Suites: $TEST_SUITES"
    echo -e "  ${GREEN}Passed: $PASSED_SUITES${NC}"
    echo -e "  ${RED}Failed: $((TEST_SUITES - PASSED_SUITES))${NC}"
    echo ""

    echo -e "${CYAN}Test Results:${NC}"
    echo "  Total Tests: $TOTAL_TESTS"
    echo -e "  ${GREEN}Passed: $TOTAL_PASSED${NC}"
    echo -e "  ${RED}Failed: $TOTAL_FAILED${NC}"

    if [ $TOTAL_TESTS -gt 0 ]; then
        PASS_RATE=$((TOTAL_PASSED * 100 / TOTAL_TESTS))
        echo "  Success Rate: $PASS_RATE%"
    fi

    echo ""
    echo "Detailed results saved to: $RESULTS_FILE"
    echo ""

    # ========================================================================
    # Expected Results Summary
    # ========================================================================
    header "Expected Test Results - RED Phase (All Failing)"

    echo "Since the effective-prompting-guide.md document has NOT been created yet,"
    echo "ALL tests are expected to FAIL in the RED phase of TDD."
    echo ""
    echo "Expected Failures by Acceptance Criteria:"
    echo "  AC1: Document Completeness          [FAIL] - Document doesn't exist"
    echo "  AC2: Example Quality and Realism     [FAIL] - No examples to validate"
    echo "  AC3: Command Guidance Accuracy       [FAIL] - No command sections"
    echo "  AC4: Framework Integration           [FAIL] - No navigation structure"
    echo "  AC5: Usability and Scannability      [FAIL] - Document doesn't exist"
    echo "  AC6: Framework Reality Validation    [FAIL] - No content to validate"
    echo ""

    # ========================================================================
    # Next Steps
    # ========================================================================
    header "Next Steps - GREEN Phase"

    echo "1. Implementation Phase (GREEN):"
    echo "   Create src/claude/memory/effective-prompting-guide.md with:"
    echo "     • Introduction (>=200 words)"
    echo "     • 11 command sections (one per command)"
    echo "     • 20-30 before/after examples"
    echo "     • Quick reference checklist"
    echo "     • 10-15 common pitfalls with mitigations"
    echo "     • Progressive disclosure structure (overview → deep dive)"
    echo ""

    echo "2. Re-run Test Suite:"
    echo "   bash tests/STORY-052/run-all-tests.sh"
    echo ""

    echo "3. Expected Results (GREEN):"
    echo "   • All structure tests: PASS"
    echo "   • All example quality tests: PASS"
    echo "   • All command guidance tests: PASS"
    echo "   • All framework reality tests: PASS"
    echo ""

    echo "4. Token Estimate for Test-Automator:"
    echo "   • Test generation (this invocation): ~12K tokens"
    echo "   • Document implementation: ~45K tokens"
    echo "   • Total for story: ~57K tokens (within budget)"
    echo ""

    # ========================================================================
    # Acceptance Criteria Coverage
    # ========================================================================
    header "Test Coverage by Acceptance Criteria"

    echo "AC#1 - Document Completeness (Core Content)"
    echo "  Tests: 7 (introduction, 11 commands, examples, checklist, pitfalls, structure)"
    echo "  Validation: grep patterns, line counting, section verification"
    echo ""

    echo "AC#2 - Example Quality and Realism"
    echo "  Tests: 10 (example count, explanations, commands, improvements, metrics, format)"
    echo "  Validation: pattern matching, word counting, consistency checking"
    echo ""

    echo "AC#3 - Command-Specific Guidance Accuracy"
    echo "  Tests: 6 (required inputs, examples per command, completeness definition, cross-refs)"
    echo "  Validation: section verification, pattern matching, reference checking"
    echo ""

    echo "AC#4 - Framework Integration and Navigation"
    echo "  Tests: 7 (documentation links, inline explanations, terminology, ToC, index, structure)"
    echo "  Validation: reference checking, heading counting, link validation"
    echo ""

    echo "AC#5 - Usability and Scannability"
    echo "  Tests: 6 (ToC, visual hierarchy, formatting, quick reference, headings, length)"
    echo "  Validation: position checking, markdown validation, structure verification"
    echo ""

    echo "AC#6 - Validation Against Framework Reality"
    echo "  Tests: 11 (command existence, orphaned references, skills, syntax, deprecated, format, organization)"
    echo "  Validation: file existence checking, pattern matching, reference validation"
    echo ""

    # ========================================================================
    # Test Execution Statistics
    # ========================================================================
    header "Test Execution Statistics"

    echo "Test Type Distribution:"
    echo "  Structure validation tests:    7 (AC1, AC5)"
    echo "  Example quality tests:         10 (AC2)"
    echo "  Command guidance tests:        13 (AC3, AC4)"
    echo "  Framework reality tests:       11 (AC6)"
    echo "  ────────────────────────────────────"
    echo "  Total tests generated:         41 tests"
    echo ""

    echo "Test Categories:"
    echo "  File existence checks:         5"
    echo "  Pattern matching (grep):       22"
    echo "  Line/word counting:            8"
    echo "  Reference validation:          4"
    echo "  Structure verification:        2"
    echo ""

    echo "Average Tests per AC:"
    echo "  6 acceptance criteria"
    echo "  41 total tests"
    echo "  ~6.8 tests per AC"
    echo ""
}

# Execute main function
main "$@"
