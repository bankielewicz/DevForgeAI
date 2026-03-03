#!/bin/bash
###############################################################################
# Test Suite Runner: STORY-053 - Framework-Internal Guidance Reference
# Purpose: Execute all test suites and generate summary report
###############################################################################

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$SCRIPT_DIR"
RESULTS_FILE="$TEST_DIR/test-results.txt"
SUMMARY_FILE="$TEST_DIR/test-summary.txt"

TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

header() {
    echo ""
    echo "================================================================"
    echo "$1"
    echo "================================================================"
}

run_test_suite() {
    local test_name=$1
    local test_file=$2

    echo ""
    echo "Running: $test_name"
    echo "File: $test_file"
    echo ""

    if [ ! -f "$test_file" ]; then
        echo "ERROR: Test file not found: $test_file"
        return 1
    fi

    # Make script executable
    chmod +x "$test_file" 2>/dev/null || true

    # Run test and capture output
    if [[ "$test_file" == *.sh ]]; then
        bash "$test_file" 2>&1 || true
    elif [[ "$test_file" == *.py ]]; then
        python3 "$test_file" 2>&1 || true
    fi
}

header "STORY-053: Framework-Internal Guidance Reference - Test Suite"

echo "Test execution started at $(date)"
echo "Test directory: $TEST_DIR"
echo ""

# Execute each test suite
echo "1. Pattern Structure Tests"
echo "   Testing AC1 - Pattern Completeness"
run_test_suite "Pattern Structure Validation" "$TEST_DIR/test-pattern-structure.sh"

echo ""
echo "2. Template Syntax Tests"
echo "   Testing AC2 - Template Usability"
run_test_suite "Template Syntax Validation" "$TEST_DIR/test-template-syntax.py"

echo ""
echo "3. Quantification Table Tests"
echo "   Testing AC3 - NFR Quantification Accuracy"
run_test_suite "Quantification Table Validation" "$TEST_DIR/test-quantification-table.py"

echo ""
echo "4. Skill Integration Tests"
echo "   Testing AC4 - Skill Integration Success"
run_test_suite "Skill Integration Validation" "$TEST_DIR/test-skill-integration.sh"

echo ""
echo "5. Framework Alignment Tests"
echo "   Testing AC5 - Framework Alignment"
run_test_suite "Framework Alignment Validation" "$TEST_DIR/test-framework-alignment.sh"

echo ""
echo "6. Performance Tests"
echo "   Testing NFR-001, NFR-002, NFR-003 - Performance Requirements"
run_test_suite "Performance and NFR Validation" "$TEST_DIR/test-performance.py"

header "Test Execution Complete"

echo ""
echo "Test suites completed at $(date)"
echo ""
echo "Test files executed:"
echo "  1. test-pattern-structure.sh"
echo "  2. test-template-syntax.py"
echo "  3. test-quantification-table.py"
echo "  4. test-skill-integration.sh"
echo "  5. test-framework-alignment.sh"
echo "  6. test-performance.py"
echo ""
echo "All tests were executed. Review output above for pass/fail results."
echo ""
echo "To run individual test suites:"
echo "  bash $TEST_DIR/test-pattern-structure.sh"
echo "  python3 $TEST_DIR/test-template-syntax.py"
echo "  python3 $TEST_DIR/test-quantification-table.py"
echo "  bash $TEST_DIR/test-skill-integration.sh"
echo "  bash $TEST_DIR/test-framework-alignment.sh"
echo "  python3 $TEST_DIR/test-performance.py"
echo ""
