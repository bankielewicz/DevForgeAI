#!/bin/bash
# Unit Test: AC#3 - Consequence Tracking and Correlation
# Tests correlation between anti-pattern usage and subsequent errors

set -e

TEST_NAME="Consequence Tracking - Error Correlation"
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

# Test 1: Track violation followed by error in same session
test_violation_followed_by_error() {
    echo -n "Test 3.1: Track violation followed by error in same session... "

    # From fixture:
    # Entry 1: Bash(command="cat story.md") - anti-pattern (session abc123)
    # Entry 2: "File not found: story.md" - error (session abc123)
    # Expected: Correlation detected - anti-pattern likely caused error

    # FAIL: No consequence tracking implemented yet
    if grep -q "consequence\|correlation\|followed by error\|caused error" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to track violation-to-error correlation"
        echo "  Actual: Consequence tracking not implemented"
        return 1
    fi
}

# Test 2: Calculate correlation rate
test_calculate_correlation_rate() {
    echo -n "Test 3.2: Calculate correlation rate (violations causing errors)... "

    # Check if session-miner has correlation_rate field
    if grep -q "correlation_rate" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have correlation_rate field"
        echo "  Actual: Field not found"
        return 1
    fi
}

# Test 3: Session-scoped correlation (not cross-session)
test_session_scoped_correlation() {
    echo -n "Test 3.3: Correlation is session-scoped (not cross-session)... "

    # Check if session-miner has session-scoped correlation docs
    if grep -q "Session-Scoped\|same session\|within.*session" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Session-scoped correlation documentation"
        echo "  Actual: Not found"
        return 1
    fi
}

# Test 4: Temporal proximity check (violation before error)
test_temporal_proximity() {
    echo -n "Test 3.4: Verify temporal proximity (violation must precede error)... "

    # Check if session-miner has temporal proximity logic
    if grep -q "Temporal Proximity\|time window\|timestamp.*<" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Temporal proximity check documentation"
        echo "  Actual: Not found"
        return 1
    fi
}

# Test 5: Violation without subsequent error (no correlation)
test_violation_no_subsequent_error() {
    echo -n "Test 3.5: Violation without subsequent error reports no correlation... "

    # Check if session-miner has uncorrelated violations handling
    if grep -q "uncorrelated\|no.*error.*follow\|non-correlated" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Uncorrelated violations documentation"
        echo "  Actual: Not found"
        return 1
    fi
}

# Test 6: Report consequence summary
test_consequence_summary_report() {
    echo -n "Test 3.6: Generate consequence summary report... "

    # Check if session-miner has consequence summary output structure
    if grep -q "consequence_correlation\|correlated_violations\|consequence.*summary" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Consequence summary output structure"
        echo "  Actual: Not found"
        return 1
    fi
}

# Test 7: Identify high-risk patterns (most likely to cause errors)
test_identify_high_risk_patterns() {
    echo -n "Test 3.7: Identify high-risk patterns (highest correlation)... "

    # Check if session-miner has high-risk pattern identification
    if grep -q "high_risk_patterns\|High-Risk Pattern\|>50%" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: High-risk pattern identification"
        echo "  Actual: Not found"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_violation_followed_by_error || FAILED_TESTS=$((FAILED_TESTS + 1))
test_calculate_correlation_rate || FAILED_TESTS=$((FAILED_TESTS + 1))
test_session_scoped_correlation || FAILED_TESTS=$((FAILED_TESTS + 1))
test_temporal_proximity || FAILED_TESTS=$((FAILED_TESTS + 1))
test_violation_no_subsequent_error || FAILED_TESTS=$((FAILED_TESTS + 1))
test_consequence_summary_report || FAILED_TESTS=$((FAILED_TESTS + 1))
test_identify_high_risk_patterns || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    echo -e "${YELLOW}This is expected - TDD Red Phase${NC}"
    exit 1
fi
