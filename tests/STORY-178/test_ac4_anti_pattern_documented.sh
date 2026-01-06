#!/bin/bash
###############################################################################
# Test Suite: STORY-178 AC-4 - Anti-Pattern Documented
#
# AC-4: Anti-Pattern Documented
# Then: "Avoid testing for specific comment text" documented
#
# Tests validate:
# - Anti-pattern guidance is present
# - Specifically warns against testing brittle text/comments
# - Explains why this is problematic
###############################################################################

set -euo pipefail

TEST_NAME="AC-4: Anti-Pattern Documented"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../.." && pwd)"
TARGET_FILE=".claude/agents/test-automator.md"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}  PASS${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}  FAIL${NC}"
    fi
}

###############################################################################
# TEST 1: Anti-pattern warning for specific text testing
###############################################################################

test_avoid_specific_text_testing() {
    # Test: Document warns against testing for specific text content
    # Core anti-pattern: testing brittle narrative text

    if grep -qiE "avoid.*(specific|exact).*(text|comment|narrative)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: 'Avoid specific text' anti-pattern"
        return 0
    elif grep -qiE "(don.?t|do not|avoid).*(test.*text|match.*comment)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Anti-pattern for text testing"
        return 0
    else
        echo "  ERROR: 'Avoid testing specific text' anti-pattern not found"
        echo "  Expected: Warning against testing specific comment/narrative text"
        return 1
    fi
}

###############################################################################
# TEST 2: Comment text anti-pattern specifically mentioned
###############################################################################

test_comment_text_anti_pattern() {
    # Test: Document specifically mentions comment text as anti-pattern

    if grep -qiE "(comment|narrative).*(brittle|fragile|anti.?pattern)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Comment text anti-pattern warning"
        return 0
    elif grep -qiE "(brittle|fragile).*(comment|narrative|text)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Brittle text testing warning"
        return 0
    elif grep -qiE "avoid.*(comment|narrative)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Avoid comment testing guidance"
        return 0
    else
        echo "  ERROR: Comment text anti-pattern not found"
        echo "  Expected: Warning about brittle comment/narrative testing"
        return 1
    fi
}

###############################################################################
# TEST 3: Anti-pattern section or clear guidance marker
###############################################################################

test_anti_pattern_marker() {
    # Test: Anti-pattern is clearly marked (with warning symbols or headers)
    # This helps users quickly identify what NOT to do

    # Look for anti-pattern markers in Specification File Testing context
    local in_context=""

    if grep -qE "^#+ .*Specification File Testing" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        in_context=$(sed -n '/^#.*Specification File Testing/,/^## [A-Z]/p' "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null | head -100)

        if echo "$in_context" | grep -qiE "(anti.?pattern|avoid|don.?t|warning|caution)" 2>/dev/null; then
            echo "  Found: Anti-pattern/warning marker in section"
            return 0
        fi
    fi

    # Fallback: check document-wide for anti-pattern markers
    if grep -qiE "(anti.?pattern|DON.?T|AVOID|WARNING:).*text" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Anti-pattern marker with text reference"
        return 0
    else
        echo "  ERROR: No clear anti-pattern marker found"
        echo "  Expected: Anti-pattern/warning marker for text testing"
        return 1
    fi
}

###############################################################################
# TEST 4: Explains WHY specific text testing is problematic
###############################################################################

test_anti_pattern_rationale() {
    # Test: Document explains why testing specific text is bad
    # Rationale: text changes frequently, breaks tests unnecessarily

    if grep -qiE "(brittle|fragile|break|fail).*(test|change)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Explanation of why text testing is problematic"
        return 0
    elif grep -qiE "(frequently|often|change).*(text|comment|narrative)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Rationale about text changes"
        return 0
    elif grep -qiE "structure.*(stable|reliable)" "$PROJECT_ROOT/$TARGET_FILE" 2>/dev/null; then
        echo "  Found: Rationale about structural stability"
        return 0
    else
        echo "  WARNING: Rationale for anti-pattern not clearly stated"
        echo "  Expected: Explanation of why specific text testing is problematic"
        # This is a soft failure - the anti-pattern itself matters more
        return 1
    fi
}

###############################################################################
# Main Test Execution
###############################################################################

main() {
    echo -e "${BLUE}=============================================================${NC}"
    echo -e "${BLUE}$TEST_NAME${NC}"
    echo -e "${BLUE}=============================================================${NC}"
    echo ""
    echo "Target file: $TARGET_FILE"
    echo ""

    run_test "AC-4.1: 'Avoid specific text testing' documented" "test_avoid_specific_text_testing"
    run_test "AC-4.2: Comment text anti-pattern mentioned" "test_comment_text_anti_pattern"
    run_test "AC-4.3: Anti-pattern clearly marked" "test_anti_pattern_marker"
    run_test "AC-4.4: Anti-pattern rationale explained" "test_anti_pattern_rationale"

    # Summary
    echo ""
    echo -e "${BLUE}=============================================================${NC}"
    echo -e "Tests run:    ${BLUE}$TESTS_RUN${NC}"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
    echo -e "${BLUE}=============================================================${NC}"

    [ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
}

main "$@"
