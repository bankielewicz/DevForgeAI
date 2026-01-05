#!/bin/bash
# Unit Test: AC#1 - Anti-Pattern Matching for Making Assumptions
# Tests detection of Category 3: Making Assumptions (CRITICAL)

set -e

TEST_NAME="Anti-Pattern Matching - Making Assumptions"
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

# Test 1: Detect technology assumption without AskUserQuestion
test_detect_technology_assumption() {
    echo -n "Test 1.1: Detect technology assumption (Install Redis) without AskUserQuestion... "

    # Check if session-miner has assumption detection implementation
    # Pattern must include making_assumptions category AND Install Redis example
    if grep -q "making_assumptions" "$PROJECT_ROOT/.claude/agents/session-miner.md" && \
       grep -q "Install Redis" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have making_assumptions category with Install Redis pattern"
        echo "  Actual: Pattern not found in session-miner.md"
        return 1
    fi
}

# Test 2: Verify AskUserQuestion usage is NOT flagged as anti-pattern
test_askuserquestion_not_flagged() {
    echo -n "Test 1.2: AskUserQuestion usage should NOT be flagged as anti-pattern... "

    # Check if session-miner has exception rule for AskUserQuestion
    if grep -q "Must check AskUserQuestion context" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have AskUserQuestion exception rule"
        echo "  Actual: Exception rule not found"
        return 1
    fi
}

# Test 3: Detect database assumption
test_detect_database_assumption() {
    echo -n "Test 1.3: Detect database assumption (Use PostgreSQL) without AskUserQuestion... "

    # Check if session-miner has PostgreSQL assumption pattern
    if grep -q "Use PostgreSQL" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have Use PostgreSQL pattern"
        echo "  Actual: Pattern not found"
        return 1
    fi
}

# Test 4: Detect framework assumption
test_detect_framework_assumption() {
    echo -n "Test 1.4: Detect framework assumption (Using React) without AskUserQuestion... "

    # Check if session-miner has React assumption pattern
    if grep -q "Build with React" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have Build with React pattern"
        echo "  Actual: Pattern not found"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_detect_technology_assumption || FAILED_TESTS=$((FAILED_TESTS + 1))
test_askuserquestion_not_flagged || FAILED_TESTS=$((FAILED_TESTS + 1))
test_detect_database_assumption || FAILED_TESTS=$((FAILED_TESTS + 1))
test_detect_framework_assumption || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
