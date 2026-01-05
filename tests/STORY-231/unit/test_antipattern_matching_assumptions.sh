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

    # Expected: "Install Redis for caching" without prior AskUserQuestion should trigger
    sample_input='Install Redis for caching layer'

    # FAIL: No detection logic implemented yet
    if grep -q "Making Assumptions\|Assuming Technology Choices" "$PROJECT_ROOT/devforgeai/specs/context/anti-patterns.md" 2>/dev/null; then
        # Check if session-miner has assumption detection
        if grep -q "assumption\|AskUserQuestion" "$PROJECT_ROOT/.claude/agents/session-miner.md" | grep -q "anti-pattern\|detect"; then
            echo -e "${GREEN}PASS${NC}"
            return 0
        else
            echo -e "${RED}FAIL${NC}"
            echo "  Expected: session-miner to detect assumption anti-patterns"
            echo "  Actual: Assumption detection not implemented"
            return 1
        fi
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Making Assumptions pattern in anti-patterns.md Category 3"
        echo "  Actual: Pattern not found"
        return 1
    fi
}

# Test 2: Verify AskUserQuestion usage is NOT flagged as anti-pattern
test_askuserquestion_not_flagged() {
    echo -n "Test 1.2: AskUserQuestion usage should NOT be flagged as anti-pattern... "

    # Expected: Using AskUserQuestion is the CORRECT behavior
    sample_input='AskUserQuestion for caching technology selection'

    # FAIL: No detection logic to verify this yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: session-miner to NOT flag AskUserQuestion as violation"
    echo "  Actual: Detection logic not implemented"
    return 1
}

# Test 3: Detect database assumption
test_detect_database_assumption() {
    echo -n "Test 1.3: Detect database assumption (Use PostgreSQL) without AskUserQuestion... "

    # Expected: "Use PostgreSQL for database" without prior choice should trigger
    sample_input='Use PostgreSQL for the database layer'

    # FAIL: No detection logic implemented yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: session-miner to detect database technology assumption"
    echo "  Actual: Detection logic not implemented"
    return 1
}

# Test 4: Detect framework assumption
test_detect_framework_assumption() {
    echo -n "Test 1.4: Detect framework assumption (Using React) without AskUserQuestion... "

    # Expected: "Build with React" without prior selection should trigger
    sample_input='Build frontend using React with TypeScript'

    # FAIL: No detection logic implemented yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: session-miner to detect frontend framework assumption"
    echo "  Actual: Detection logic not implemented"
    return 1
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
    echo -e "${YELLOW}This is expected - TDD Red Phase${NC}"
    exit 1
fi
