#!/bin/bash
###############################################################################
# STORY-221 Test Suite: AC#3 - Streaming/Pagination Support for Large Files
#
# Acceptance Criteria:
# Given the history.jsonl file exceeds 50MB,
# When the session-miner processes entries,
# Then processing uses chunked reads with offset/limit parameters to avoid
#      context window exhaustion.
#
# Test Framework: Bash (Documentation verification for subagent specs)
# Status: Verifies session-miner.md documents streaming/pagination support
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
# Test AC#3.1: Documents streaming/chunked reading
###############################################################################

test_documents_streaming() {
    local test_name="AC#3.1: Documents streaming/chunked reading support"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_streaming=$(grep -ci "stream\|chunk" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_streaming" -ge 2 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing streaming docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#3.2: Documents offset parameter
###############################################################################

test_documents_offset() {
    local test_name="AC#3.2: Documents offset parameter"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_offset=$(grep -ci "offset" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_offset" -ge 3 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing offset docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#3.3: Documents limit parameter
###############################################################################

test_documents_limit() {
    local test_name="AC#3.3: Documents limit parameter"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_limit=$(grep -ci "limit" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_limit" -ge 3 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing limit docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#3.4: Documents pagination metadata (has_more, next_offset)
###############################################################################

test_documents_pagination_metadata() {
    local test_name="AC#3.4: Documents pagination metadata (has_more, next_offset)"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_more=$(grep -ci "has.more\|has_more" "$SESSION_MINER" 2>/dev/null || echo "0")
    local next_offset=$(grep -ci "next.offset\|next_offset" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_more" -ge 1 && "$next_offset" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing pagination metadata docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#3.5: Documents large file handling (50MB+)
###############################################################################

test_documents_large_file() {
    local test_name="AC#3.5: Documents large file handling (50MB+)"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_large=$(grep -ci "50.mb\|86.mb\|large" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_large" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing large file docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#3.6: Documents context window awareness
###############################################################################

test_documents_context_window() {
    local test_name="AC#3.6: Documents context window awareness"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_context=$(grep -ci "context.window\|context window" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_context" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing context window docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#3.7: Documents performance target (<30 seconds)
###############################################################################

test_documents_performance() {
    local test_name="AC#3.7: Documents performance target (<30 seconds)"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_perf=$(grep -ci "30.second\|30 second\|performance" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_perf" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing performance docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Main Test Execution
###############################################################################

main() {
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}STORY-221 Test Suite: AC#3 - Streaming/Pagination Support for Large Files${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    # Run all tests
    test_documents_streaming
    test_documents_offset
    test_documents_limit
    test_documents_pagination_metadata
    test_documents_large_file
    test_documents_context_window
    test_documents_performance

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
