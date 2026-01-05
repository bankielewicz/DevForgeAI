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

    # From anti-patterns.md: Bash MUST be used for running tests
    # Pattern: Bash(command="npm test") should NOT trigger Category 1
    sample_input='Bash(command="npm test")'

    # FAIL: No exception logic implemented yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Bash npm test NOT flagged as anti-pattern"
    echo "  Actual: Exception handling not implemented"
    return 1
}

# Test 2: Legitimate Bash for git operations not flagged
test_legitimate_bash_git_not_flagged() {
    echo -n "Test E.2: Legitimate Bash usage (git commit) NOT flagged as violation... "

    # From anti-patterns.md: Bash MUST be used for git operations
    sample_input='Bash(command="git commit -m \"fix: bug\")"'

    # FAIL: No exception logic implemented yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Bash git NOT flagged as anti-pattern"
    echo "  Actual: Exception handling not implemented"
    return 1
}

# Test 3: Multiple violations in single entry
test_multiple_violations_single_entry() {
    echo -n "Test E.3: Multiple violations in single entry counted separately... "

    # Example: Entry contains both "Bash cat" AND "hardcoded path"
    sample_input='Bash(command="cat /home/user/file.md")'

    # Expected: Two violations counted: bash_for_file_ops AND hardcoded_paths

    # FAIL: No multi-violation handling yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Each violation type counted separately"
    echo "  Actual: Multi-violation handling not implemented"
    return 1
}

# Test 4: Case-insensitive pattern matching
test_case_insensitive_matching() {
    echo -n "Test E.4: Pattern matching is case-insensitive... "

    # "BASH(COMMAND=" should match same as "Bash(command="
    sample_input='BASH(COMMAND="CAT file.txt")'

    # FAIL: No case handling tested yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Case-insensitive pattern matching"
    echo "  Actual: Case handling not implemented"
    return 1
}

# Test 5: Very long user_input truncated for pattern matching
test_long_input_truncation() {
    echo -n "Test E.5: Very long user_input (>10000 chars) truncated safely... "

    # Expected: Truncate to 10000 chars before pattern matching
    # to prevent regex performance issues

    # FAIL: No truncation logic yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Long inputs truncated to 10000 chars"
    echo "  Actual: Truncation not implemented"
    return 1
}

# Test 6: Unicode content in user_input handled
test_unicode_content_handling() {
    echo -n "Test E.6: Unicode content in user_input handled correctly... "

    # Pattern matching should work with Unicode strings
    sample_input='Bash(command="cat story-日本語.md")'

    # FAIL: No unicode handling tested yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Unicode content matched correctly"
    echo "  Actual: Unicode handling not tested"
    return 1
}

# Test 7: Partial pattern match (Bash inside quotes)
test_partial_pattern_match() {
    echo -n "Test E.7: 'Bash' inside quotes NOT flagged as violation... "

    # The word "Bash" in documentation should not trigger
    sample_input='Documentation says: "Use Bash for tests only"'

    # FAIL: No context-aware matching yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Bash in quotes not flagged"
    echo "  Actual: Context-aware matching not implemented"
    return 1
}

# Test 8: Session with only success entries (no errors to correlate)
test_session_success_only() {
    echo -n "Test E.8: Session with only success entries reports 0% correlation... "

    # Expected: Violations detected but correlation_rate = 0

    # FAIL: No edge case handling yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: 0% correlation when no errors in session"
    echo "  Actual: Edge case not handled"
    return 1
}

# Test 9: Circular dependency detection (Category 7)
test_circular_dependency_detection() {
    echo -n "Test E.9: Circular dependency pattern detected... "

    # Pattern: "Skill A calls Skill B calls Skill A"
    sample_input='devforgeai-development calls devforgeai-qa calls devforgeai-development'

    # FAIL: No circular dependency detection yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Circular dependency flagged as Category 7 violation"
    echo "  Actual: Circular detection not implemented"
    return 1
}

# Test 10: Missing frontmatter detection (Category 9)
test_missing_frontmatter_detection() {
    echo -n "Test E.10: Missing frontmatter pattern detected... "

    # Pattern: SKILL.md or command without YAML frontmatter
    sample_input='Created SKILL.md without frontmatter'

    # FAIL: No frontmatter detection yet
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Missing frontmatter flagged as Category 9 violation"
    echo "  Actual: Frontmatter detection not implemented"
    return 1
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
    echo -e "${YELLOW}This is expected - TDD Red Phase${NC}"
    exit 1
fi
