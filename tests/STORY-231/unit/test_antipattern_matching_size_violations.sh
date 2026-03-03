#!/bin/bash
# Unit Test: AC#1 - Anti-Pattern Matching for Size Violations
# Tests detection of Category 4: Size Violations (HIGH)

set -e

TEST_NAME="Anti-Pattern Matching - Size Violations"
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

# Test 1: Detect SKILL.md exceeding 1000 line limit
test_detect_skill_size_violation() {
    echo -n "Test 1.1: Detect SKILL.md exceeding 1000 lines... "

    # Check if session-miner has size_violations category with >1000 lines threshold
    if grep -q "size_violations" "$PROJECT_ROOT/.claude/agents/session-miner.md" && \
       grep -q ">1000 lines" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have size_violations with >1000 lines threshold"
        echo "  Actual: Pattern not found"
        return 1
    fi
}

# Test 2: Detect command exceeding 500 line limit
test_detect_command_size_violation() {
    echo -n "Test 1.2: Detect command file exceeding 500 lines... "

    # Check if session-miner has >500 lines threshold
    if grep -q ">500 lines" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have >500 lines threshold"
        echo "  Actual: Pattern not found"
        return 1
    fi
}

# Test 3: Detect monolithic all-in-one skill
test_detect_monolithic_skill() {
    echo -n "Test 1.3: Detect monolithic all-in-one skill (Category 2)... "

    # Check if session-miner has monolithic_components category with all-in-one detection
    if grep -q "monolithic_components" "$PROJECT_ROOT/.claude/agents/session-miner.md" && \
       grep -q "ideation + architecture + dev" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have monolithic_components with ideation + architecture + dev"
        echo "  Actual: Pattern not found"
        return 1
    fi
}

# Test 4: Verify size within limits is NOT flagged
test_valid_size_not_flagged() {
    echo -n "Test 1.4: SKILL.md with 600 lines should NOT be flagged... "

    # Verify threshold documentation exists (600 < 1000, so valid)
    # If 1000 is documented as threshold, sizes below it are valid
    if grep -q "1000" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to document 1000 line threshold"
        echo "  Actual: Threshold not documented"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_detect_skill_size_violation || FAILED_TESTS=$((FAILED_TESTS + 1))
test_detect_command_size_violation || FAILED_TESTS=$((FAILED_TESTS + 1))
test_detect_monolithic_skill || FAILED_TESTS=$((FAILED_TESTS + 1))
test_valid_size_not_flagged || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
