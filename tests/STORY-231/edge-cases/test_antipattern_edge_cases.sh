#!/bin/bash
# Edge Case Tests: Anti-Pattern Mining
# Tests boundary conditions and unusual inputs

set -e

TEST_NAME="Anti-Pattern Mining Edge Cases"
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

# Test 1: Legitimate Bash usage (test execution) not flagged
test_legitimate_bash_not_flagged() {
    echo -n "Test E.1: Legitimate Bash usage (npm test) NOT flagged as violation... "

    # Check if session-miner has npm test in exception list
    if grep -q "npm test" "$PROJECT_ROOT/.claude/agents/session-miner.md" && \
       grep -q "Legitimate Bash Exceptions" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: npm test in Legitimate Bash Exceptions"
        echo "  Actual: Exception not documented"
        return 1
    fi
}

# Test 2: Legitimate Bash for git operations not flagged
test_legitimate_bash_git_not_flagged() {
    echo -n "Test E.2: Legitimate Bash usage (git commit) NOT flagged as violation... "

    # Check if session-miner has git in allowed_prefixes
    if grep -q 'git ' "$PROJECT_ROOT/.claude/agents/session-miner.md" && \
       grep -q "allowed_prefixes" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: git in allowed_prefixes"
        echo "  Actual: Git exception not documented"
        return 1
    fi
}

# Test 3: Multiple violations in single entry
test_multiple_violations_single_entry() {
    echo -n "Test E.3: Multiple violations in single entry counted separately... "

    # Check if session-miner documents multi-violation handling
    if grep -q "Multi-Violation Detection" "$PROJECT_ROOT/.claude/agents/session-miner.md" && \
       grep -q "Both violations counted separately" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Multi-Violation Detection documented"
        echo "  Actual: Multi-violation handling not documented"
        return 1
    fi
}

# Test 4: Case-insensitive pattern matching
test_case_insensitive_matching() {
    echo -n "Test E.4: Pattern matching is case-insensitive... "

    # Check if session-miner has case-insensitive matching documented
    if grep -q "Case-Insensitive Matching" "$PROJECT_ROOT/.claude/agents/session-miner.md" && \
       grep -q "normalize_input" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Case-Insensitive Matching with normalize_input"
        echo "  Actual: Case handling not documented"
        return 1
    fi
}

# Test 5: Very long user_input truncated for pattern matching
test_long_input_truncation() {
    echo -n "Test E.5: Very long user_input (>10000 chars) truncated safely... "

    # Check if session-miner has truncation at 10000 chars
    if grep -q "10000" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: 10000 char truncation documented"
        echo "  Actual: Truncation not documented"
        return 1
    fi
}

# Test 6: Unicode content in user_input handled
test_unicode_content_handling() {
    echo -n "Test E.6: Unicode content in user_input handled correctly... "

    # Check if session-miner documents Unicode handling
    if grep -q "Unicode" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Unicode handling documented"
        echo "  Actual: Unicode not mentioned"
        return 1
    fi
}

# Test 7: Partial pattern match (Bash inside quotes)
test_partial_pattern_match() {
    echo -n "Test E.7: 'Bash' inside quotes NOT flagged as violation... "

    # Check if session-miner has context-aware matching
    if grep -q "Context-Aware Matching" "$PROJECT_ROOT/.claude/agents/session-miner.md" && \
       grep -q "is_false_positive_context" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Context-Aware Matching with is_false_positive_context"
        echo "  Actual: Context-aware matching not documented"
        return 1
    fi
}

# Test 8: Session with only success entries (no errors to correlate)
test_session_success_only() {
    echo -n "Test E.8: Session with only success entries reports 0% correlation... "

    # Check if session-miner handles zero correlation case
    if grep -q "correlation_rate = 0" "$PROJECT_ROOT/.claude/agents/session-miner.md" || \
       grep -q "Zero Violations" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Zero correlation edge case documented"
        echo "  Actual: Edge case not documented"
        return 1
    fi
}

# Test 9: Circular dependency detection (Category 7)
test_circular_dependency_detection() {
    echo -n "Test E.9: Circular dependency pattern detected... "

    # Check if session-miner has circular_dependencies category
    if grep -q "circular_dependencies" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: circular_dependencies category documented"
        echo "  Actual: Category not found"
        return 1
    fi
}

# Test 10: Missing frontmatter detection (Category 9)
test_missing_frontmatter_detection() {
    echo -n "Test E.10: Missing frontmatter pattern detected... "

    # Check if session-miner has missing_frontmatter category
    if grep -q "missing_frontmatter" "$PROJECT_ROOT/.claude/agents/session-miner.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: missing_frontmatter category documented"
        echo "  Actual: Category not found"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_legitimate_bash_not_flagged || FAILED_TESTS=$((FAILED_TESTS + 1))
test_legitimate_bash_git_not_flagged || FAILED_TESTS=$((FAILED_TESTS + 1))
test_multiple_violations_single_entry || FAILED_TESTS=$((FAILED_TESTS + 1))
test_case_insensitive_matching || FAILED_TESTS=$((FAILED_TESTS + 1))
test_long_input_truncation || FAILED_TESTS=$((FAILED_TESTS + 1))
test_unicode_content_handling || FAILED_TESTS=$((FAILED_TESTS + 1))
test_partial_pattern_match || FAILED_TESTS=$((FAILED_TESTS + 1))
test_session_success_only || FAILED_TESTS=$((FAILED_TESTS + 1))
test_circular_dependency_detection || FAILED_TESTS=$((FAILED_TESTS + 1))
test_missing_frontmatter_detection || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
