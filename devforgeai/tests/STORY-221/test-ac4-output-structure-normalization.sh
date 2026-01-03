#!/bin/bash
###############################################################################
# STORY-221 Test Suite: AC#4 - Output Structure Normalization
#
# Acceptance Criteria:
# Given parsed entries with varying field formats,
# When the session-miner returns results,
# Then output follows consistent JSON schema for downstream consumers.
#
# Test Framework: Bash (Documentation verification for subagent specs)
# Status: Verifies session-miner.md documents output normalization patterns
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
# Test AC#4.1: Documents JSON output format
###############################################################################

test_documents_json_output() {
    local test_name="AC#4.1: Documents JSON output format"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_json=$(grep -ci "json" "$SESSION_MINER" 2>/dev/null || echo "0")
    local has_output=$(grep -ci "output" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_json" -ge 3 && "$has_output" -ge 2 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing JSON output docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#4.2: Documents entries array structure
###############################################################################

test_documents_entries_array() {
    local test_name="AC#4.2: Documents entries array structure"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_entries=$(grep -ci "entries" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_entries" -ge 3 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing entries array docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#4.3: Documents metadata object
###############################################################################

test_documents_metadata() {
    local test_name="AC#4.3: Documents metadata object"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_metadata=$(grep -ci "metadata" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_metadata" -ge 2 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing metadata docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#4.4: Documents SessionEntry schema
###############################################################################

test_documents_schema() {
    local test_name="AC#4.4: Documents SessionEntry schema"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_schema=$(grep -ci "schema\|sessionentry" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_schema" -ge 2 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing schema docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#4.5: Documents type safety
###############################################################################

test_documents_type_safety() {
    local test_name="AC#4.5: Documents type safety (String, Integer, etc.)"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_string=$(grep -ci "string" "$SESSION_MINER" 2>/dev/null || echo "0")
    local has_int=$(grep -ci "integer\|int" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_string" -ge 2 && "$has_int" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing type docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#4.6: Documents null/missing value handling
###############################################################################

test_documents_null_handling() {
    local test_name="AC#4.6: Documents null/missing value handling"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_null=$(grep -ci "null\|fallback\|missing" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_null" -ge 3 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing null handling docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#4.7: Documents downstream compatibility
###############################################################################

test_documents_downstream() {
    local test_name="AC#4.7: Documents downstream consumer compatibility"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_downstream=$(grep -ci "downstream\|consumer\|normalized" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_downstream" -ge 2 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing downstream docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#4.8: Documents error count in output
###############################################################################

test_documents_error_count() {
    local test_name="AC#4.8: Documents error count in output"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_error_count=$(grep -ci "errors.count\|errors_count\|error count" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_error_count" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing error count docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Main Test Execution
###############################################################################

main() {
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}STORY-221 Test Suite: AC#4 - Output Structure Normalization${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    # Run all tests
    test_documents_json_output
    test_documents_entries_array
    test_documents_metadata
    test_documents_schema
    test_documents_type_safety
    test_documents_null_handling
    test_documents_downstream
    test_documents_error_count

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
