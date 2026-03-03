#!/bin/bash
# Unit Test: AC#2 - Violation Counting and Aggregation
# Tests counting violations per pattern type

set -e

TEST_NAME="Violation Counting - Aggregation"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"
FIXTURES_DIR="$TEST_DIR/../fixtures"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

# Test 1: Count violations per category
test_count_violations_per_category() {
    echo -n "Test 2.1: Count violations per category from sample session... "

    # Expected output structure for counting:
    # {
    #   "category_distribution": {
    #     "bash_for_file_ops": 3,
    #     "making_assumptions": 1,
    #     "context_file_violations": 1,
    #     "hardcoded_paths": 1,
    #     "size_violations": 1
    #   }
    # }

    # Check if session-miner has violation counting section
    if grep -q "violation.*count\|category_distribution\|count per pattern" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have violation counting section"
        echo "  Actual: Violation counting not implemented"
        return 1
    fi
}

# Test 2: Aggregate total violation count
test_aggregate_total_violations() {
    echo -n "Test 2.2: Aggregate total violation count... "

    # Check if session-miner has total_violations field
    if grep -q "total_violations" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have total_violations field"
        echo "  Actual: Field not found"
        return 1
    fi
}

# Test 3: Calculate violation rate
test_calculate_violation_rate() {
    echo -n "Test 2.3: Calculate violation rate (violations/total entries)... "

    # Check if session-miner has violation_rate field
    if grep -q "violation_rate" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have violation_rate field"
        echo "  Actual: Field not found"
        return 1
    fi
}

# Test 4: Report severity distribution
test_report_severity_distribution() {
    echo -n "Test 2.4: Report severity distribution (critical/high/medium/low)... "

    # Check if session-miner has severity_distribution field
    if grep -q "severity_distribution" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have severity_distribution field"
        echo "  Actual: Field not found"
        return 1
    fi
}

# Test 5: Zero violations returns empty distribution
test_zero_violations_empty_distribution() {
    echo -n "Test 2.5: Zero violations returns empty category_distribution... "

    # Check if session-miner has zero violations edge case handling
    if grep -q "Zero Violations\|no violations" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to handle zero violations case"
        echo "  Actual: Edge case not documented"
        return 1
    fi
}

# Test 6: Violation codes assigned (AP-XXX format)
test_violation_codes_assigned() {
    echo -n "Test 2.6: Violations assigned codes in AP-XXX format... "

    # Check if session-miner has AP-XXX violation codes
    if grep -q "AP-00[1-9]\|AP-010" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have AP-XXX violation codes"
        echo "  Actual: Codes not found"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_count_violations_per_category || FAILED_TESTS=$((FAILED_TESTS + 1))
test_aggregate_total_violations || FAILED_TESTS=$((FAILED_TESTS + 1))
test_calculate_violation_rate || FAILED_TESTS=$((FAILED_TESTS + 1))
test_report_severity_distribution || FAILED_TESTS=$((FAILED_TESTS + 1))
test_zero_violations_empty_distribution || FAILED_TESTS=$((FAILED_TESTS + 1))
test_violation_codes_assigned || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    echo -e "${YELLOW}This is expected - TDD Red Phase${NC}"
    exit 1
fi
