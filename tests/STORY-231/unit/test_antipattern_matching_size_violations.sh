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

    # Expected: Pattern should match "SKILL.md with 2000 lines" or similar
    sample_input='Create SKILL.md with 2000 lines of inline documentation'

    # FAIL: No detection logic implemented yet
    if grep -q "Size Violations\|Exceeding Component Size" "$PROJECT_ROOT/devforgeai/specs/context/anti-patterns.md" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to detect size violation in SKILL.md"
        echo "  Actual: Size violation detection not implemented"
        return 1
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Size Violations pattern in anti-patterns.md Category 4"
        echo "  Actual: Pattern not found"
        return 1
    fi
}

# Test 2: Detect command exceeding 500 line limit
test_detect_command_size_violation() {
    echo -n "Test 1.2: Detect command file exceeding 500 lines... "

    # Expected: Pattern should detect command files > 500 lines
    sample_input='Command file has grown to 800 lines'

    # FAIL: No detection logic implemented yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: session-miner to detect command size violation"
    echo "  Actual: Size violation detection not implemented"
    return 1
}

# Test 3: Detect monolithic all-in-one skill
test_detect_monolithic_skill() {
    echo -n "Test 1.3: Detect monolithic all-in-one skill (Category 2)... "

    # Expected: Pattern should detect "devforgeai-everything" or "all-in-one" skills
    sample_input='Created devforgeai-everything skill doing ideation + architecture + dev + qa'

    # FAIL: No detection logic implemented yet
    if grep -q "Monolithic Components\|All-in-One Skill" "$PROJECT_ROOT/devforgeai/specs/context/anti-patterns.md" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to detect monolithic skill anti-pattern"
        echo "  Actual: Monolithic detection not implemented"
        return 1
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Monolithic Components pattern in anti-patterns.md Category 2"
        echo "  Actual: Pattern not found"
        return 1
    fi
}

# Test 4: Verify size within limits is NOT flagged
test_valid_size_not_flagged() {
    echo -n "Test 1.4: SKILL.md with 600 lines should NOT be flagged... "

    # Expected: 600 lines is within 1000 line limit
    sample_input='SKILL.md is 600 lines'

    # FAIL: No detection logic to verify this yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: session-miner to NOT flag valid size as violation"
    echo "  Actual: Detection logic not implemented"
    return 1
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
    echo -e "${YELLOW}This is expected - TDD Red Phase${NC}"
    exit 1
fi
