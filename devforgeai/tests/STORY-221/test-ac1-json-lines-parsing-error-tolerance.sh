#!/bin/bash
###############################################################################
# STORY-221 Test Suite: AC#1 - JSON Lines Parsing with Error Tolerance
#
# Acceptance Criteria:
# Given a history.jsonl file with mixed valid and malformed entries,
# When the session-miner subagent parses the file,
# Then valid entries are extracted and malformed entries are logged but
#      do not halt processing.
#
# Test Framework: Bash (Documentation verification for subagent specs)
# Status: Verifies session-miner.md contains required documentation patterns
###############################################################################

set -uo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TEST_PASSED=0
TEST_FAILED=0
TESTS_RUN=0

# Get project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SESSION_MINER="$PROJECT_ROOT/.claude/agents/session-miner.md"

###############################################################################
# Test AC#1.1: Session-miner subagent exists
###############################################################################

test_session_miner_exists() {
    local test_name="AC#1.1: session-miner.md subagent file exists"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ -f "$SESSION_MINER" ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (file not found: $SESSION_MINER)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#1.2: Documents JSON Lines parsing
###############################################################################

test_documents_jsonl_parsing() {
    local test_name="AC#1.2: Documents JSON Lines parsing capability"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_jsonl=$(grep -ci "json.line\|jsonl\|json lines" "$SESSION_MINER" 2>/dev/null || echo "0")
    local has_parsing=$(grep -ci "pars" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_jsonl" -ge 1 && "$has_parsing" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name (JSON Lines parsing documented)"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing JSON Lines parsing docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#1.3: Documents error tolerance
###############################################################################

test_documents_error_tolerance() {
    local test_name="AC#1.3: Documents error tolerance for malformed entries"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_error=$(grep -ci "error\|malformed" "$SESSION_MINER" 2>/dev/null || echo "0")
    local has_tolerance=$(grep -ci "toleran\|skip\|continue\|graceful" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_error" -ge 1 && "$has_tolerance" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name (error tolerance documented)"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing error tolerance docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#1.4: Documents logging of malformed entries
###############################################################################

test_documents_error_logging() {
    local test_name="AC#1.4: Documents logging of malformed entries"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_log=$(grep -ci "log\|errors" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_log" -ge 2 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name (error logging documented)"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing error logging docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#1.5: Has required YAML frontmatter
###############################################################################

test_has_yaml_frontmatter() {
    local test_name="AC#1.5: Has YAML frontmatter with name, description, tools"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_name=$(grep -c "^name:" "$SESSION_MINER" 2>/dev/null || echo "0")
    local has_desc=$(grep -c "^description:" "$SESSION_MINER" 2>/dev/null || echo "0")
    local has_tools=$(grep -c "^tools:" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_name" -ge 1 && "$has_desc" -ge 1 && "$has_tools" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name (frontmatter complete)"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing frontmatter fields)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Main Test Execution
###############################################################################

main() {
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}STORY-221 Test Suite: AC#1 - JSON Lines Parsing with Error Tolerance${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    # Run all tests
    test_session_miner_exists
    test_documents_jsonl_parsing
    test_documents_error_tolerance
    test_documents_error_logging
    test_has_yaml_frontmatter

    # Print summary
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}Test Summary${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "Tests Run:    $TESTS_RUN"
    echo -e "${GREEN}Passed:       $TEST_PASSED${NC}"
    echo -e "${RED}Failed:       $TEST_FAILED${NC}"
    echo ""

    if [ $TEST_FAILED -eq 0 ]; then
        echo -e "${GREEN}All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}Some tests failed.${NC}"
        exit 1
    fi
}

main "$@"
