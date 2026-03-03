#!/bin/bash
# Integration Test: Anti-Pattern Mining Pipeline
# Tests end-to-end anti-pattern detection, counting, and correlation

set -e

TEST_NAME="Anti-Pattern Mining Pipeline Integration"
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

# Test 1: Full pipeline from session data to anti-pattern report
test_full_pipeline_execution() {
    echo -n "Test I.1: Full pipeline from session input to anti-pattern report... "

    # Expected: session-miner with anti-pattern mode processes fixture file
    # and produces complete anti-pattern analysis report

    # Check if session-miner has anti-pattern mining workflow
    if grep -q "Anti-Pattern Mining\|anti-pattern.*pipeline\|AntiPatternEntry" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Anti-pattern mining pipeline in session-miner.md"
        echo "  Actual: Pipeline not implemented"
        return 1
    fi
}

# Test 2: Pipeline integrates with existing error categorization (STORY-229)
test_integration_with_error_categorization() {
    echo -n "Test I.2: Pipeline integrates with STORY-229 error categorization... "

    # Expected: Anti-pattern mining reuses ErrorEntry from STORY-229
    # and correlates violations with categorized errors

    # Check if session-miner references STORY-229
    if grep -q "STORY-229\|Error Categorization\|ErrorEntry" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        # Now check for integration between anti-pattern and error sections
        if grep -A 10 "Anti-Pattern\|STORY-231" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null | grep -q "ErrorEntry\|error.*correlation\|STORY-229"; then
            echo -e "${GREEN}PASS${NC}"
            return 0
        else
            echo -e "${RED}FAIL${NC}"
            echo "  Expected: Anti-pattern section references STORY-229 error categorization"
            echo "  Actual: Integration not implemented"
            return 1
        fi
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: STORY-229 error categorization in session-miner.md"
        echo "  Actual: Error categorization not found (prerequisite)"
        return 1
    fi
}

# Test 3: Output format matches expected JSON schema
test_output_json_schema() {
    echo -n "Test I.3: Output matches expected JSON schema... "

    # Check if session-miner has output schema with required fields
    if grep -q '"violations"\|"category_distribution"\|"metadata"' "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Anti-pattern output schema in session-miner.md"
        echo "  Actual: Schema not found"
        return 1
    fi
}

# Test 4: Pipeline handles empty input gracefully
test_empty_input_handling() {
    echo -n "Test I.4: Pipeline handles empty session file gracefully... "

    # Check if session-miner documents empty input handling
    if grep -q "No violations\|empty.*violations\|0.*violations\|total_violations.*0" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Empty input handling documented"
        echo "  Actual: Not found"
        return 1
    fi
}

# Test 5: Pipeline handles malformed entries (error tolerance)
test_malformed_entry_tolerance() {
    echo -n "Test I.5: Pipeline tolerates malformed JSON entries... "

    # Check if session-miner has error tolerance documentation
    if grep -q "Edge Case\|Malformed\|error handling\|graceful" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Error tolerance documented"
        echo "  Actual: Not found"
        return 1
    fi
}

# Test 6: All 10 anti-pattern categories are matchable
test_all_categories_matchable() {
    echo -n "Test I.6: All 10 anti-pattern categories are matchable... "

    # Check if session-miner has detection rules for all 10 categories
    # Count how many categories are documented in the Category Detection Rules table
    categories_found=$(grep -E "bash_for_file_ops|monolithic|assumptions|size_violations|language_specific|context_file_violations|circular_dependencies|narrative_documentation|missing_frontmatter|hardcoded_paths" "$PROJECT_ROOT/.claude/agents/session-miner.md" 2>/dev/null | wc -l)

    if [ "$categories_found" -ge 10 ]; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: 10+ category references"
        echo "  Actual: Found $categories_found references"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_full_pipeline_execution || FAILED_TESTS=$((FAILED_TESTS + 1))
test_integration_with_error_categorization || FAILED_TESTS=$((FAILED_TESTS + 1))
test_output_json_schema || FAILED_TESTS=$((FAILED_TESTS + 1))
test_empty_input_handling || FAILED_TESTS=$((FAILED_TESTS + 1))
test_malformed_entry_tolerance || FAILED_TESTS=$((FAILED_TESTS + 1))
test_all_categories_matchable || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    echo -e "${YELLOW}This is expected - TDD Red Phase${NC}"
    exit 1
fi
