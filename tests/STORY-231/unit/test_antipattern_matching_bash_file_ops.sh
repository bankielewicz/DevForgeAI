#!/bin/bash
# Unit Test: AC#1 - Anti-Pattern Matching for Bash File Operations
# Tests detection of Category 1: Bash for file ops (CRITICAL)

set -e

TEST_NAME="Anti-Pattern Matching - Bash File Operations"
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

# Test 1: Detect Bash cat command as anti-pattern
test_detect_bash_cat_antipattern() {
    echo -n "Test 1.1: Detect Bash(command=\"cat\") as Category 1 violation... "

    # Expected: session-miner should detect this pattern from anti-patterns.md
    # Pattern: Bash(command="cat file.txt") should trigger Category 1

    # Check if session-miner has detection logic for Bash cat
    if grep -q 'Bash(command="cat' "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have Bash cat detection pattern"
        echo "  Actual: Pattern not found in session-miner.md"
        return 1
    fi
}

# Test 2: Detect Bash echo redirect as anti-pattern
test_detect_bash_echo_redirect_antipattern() {
    echo -n "Test 1.2: Detect Bash(command=\"echo '...' > file\") as Category 1 violation... "

    # Check if session-miner has detection logic for Bash echo redirect
    # Pattern is documented as `echo >` in Category Detection Rules table
    if grep -q 'echo >' "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have echo > detection pattern"
        echo "  Actual: Pattern not found in session-miner.md"
        return 1
    fi
}

# Test 3: Detect Bash find command as anti-pattern
test_detect_bash_find_antipattern() {
    echo -n "Test 1.3: Detect Bash(command=\"find\") as Category 1 violation... "

    # Check if session-miner has detection logic for Bash find
    # Pattern is documented as `find` in Category Detection Rules table (line 1102)
    if grep -q '`find`' "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: session-miner to have find detection pattern"
        echo "  Actual: Pattern not found in session-miner.md"
        return 1
    fi
}

# Test 4: Session-miner has anti-pattern detection section
test_session_miner_has_antipattern_section() {
    echo -n "Test 1.4: session-miner.md contains Anti-Pattern Mining section... "

    # FAIL: Section not yet added to session-miner.md
    if grep -q "Anti-Pattern Mining\|Anti-Pattern Occurrences\|STORY-231" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Anti-Pattern Mining section in session-miner.md"
        echo "  Actual: Section not found"
        return 1
    fi
}

# Test 5: Verify anti-patterns.md has all 10 categories documented
test_antipatterns_has_all_categories() {
    echo -n "Test 1.5: anti-patterns.md has all 10 categories... "

    categories_found=0
    for i in 1 2 3 4 5 6 7 8 9 10; do
        if grep -q "Category $i:" "$PROJECT_ROOT/devforgeai/specs/context/anti-patterns.md" 2>/dev/null; then
            categories_found=$((categories_found + 1))
        fi
    done

    if [ $categories_found -eq 10 ]; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: 10 categories in anti-patterns.md"
        echo "  Actual: Found $categories_found categories"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_detect_bash_cat_antipattern || FAILED_TESTS=$((FAILED_TESTS + 1))
test_detect_bash_echo_redirect_antipattern || FAILED_TESTS=$((FAILED_TESTS + 1))
test_detect_bash_find_antipattern || FAILED_TESTS=$((FAILED_TESTS + 1))
test_session_miner_has_antipattern_section || FAILED_TESTS=$((FAILED_TESTS + 1))
test_antipatterns_has_all_categories || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    echo -e "${YELLOW}This is expected - TDD Red Phase${NC}"
    exit 1
fi
