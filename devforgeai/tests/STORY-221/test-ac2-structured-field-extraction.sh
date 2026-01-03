#!/bin/bash
###############################################################################
# STORY-221 Test Suite: AC#2 - Structured Field Extraction
#
# Acceptance Criteria:
# Given a valid history.jsonl entry,
# When the session-miner extracts metadata,
# Then the following fields are normalized: timestamp, command, status,
#      duration_ms, user_input, model, session_id, project.
#
# Test Framework: Bash (Documentation verification for subagent specs)
# Status: Verifies session-miner.md documents all 8 required fields
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
# Test AC#2.1: Documents timestamp field
###############################################################################

test_documents_timestamp() {
    local test_name="AC#2.1: Documents timestamp field extraction (ISO8601)"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_timestamp=$(grep -ci "timestamp" "$SESSION_MINER" 2>/dev/null || echo "0")
    local has_iso=$(grep -ci "iso.8601\|iso8601\|datetime" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_timestamp" -ge 2 && "$has_iso" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing timestamp/ISO8601 docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#2.2: Documents command field
###############################################################################

test_documents_command() {
    local test_name="AC#2.2: Documents command field extraction"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_command=$(grep -ci "command" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_command" -ge 2 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing command field docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#2.3: Documents status field with enum values
###############################################################################

test_documents_status() {
    local test_name="AC#2.3: Documents status field (success|error|partial)"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_status=$(grep -ci "status" "$SESSION_MINER" 2>/dev/null || echo "0")
    local has_success=$(grep -ci "success" "$SESSION_MINER" 2>/dev/null || echo "0")
    local has_error=$(grep -ci "error" "$SESSION_MINER" 2>/dev/null || echo "0")
    local has_partial=$(grep -ci "partial" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_status" -ge 2 && "$has_success" -ge 1 && "$has_error" -ge 1 && "$has_partial" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing status enum docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#2.4: Documents duration_ms field
###############################################################################

test_documents_duration() {
    local test_name="AC#2.4: Documents duration_ms field"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_duration=$(grep -ci "duration" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_duration" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing duration_ms docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#2.5: Documents user_input field
###############################################################################

test_documents_user_input() {
    local test_name="AC#2.5: Documents user_input field"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_user_input=$(grep -ci "user.input\|user_input" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_user_input" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing user_input docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#2.6: Documents model field
###############################################################################

test_documents_model() {
    local test_name="AC#2.6: Documents model field"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_model=$(grep -ci "model" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_model" -ge 2 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing model docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#2.7: Documents session_id field
###############################################################################

test_documents_session_id() {
    local test_name="AC#2.7: Documents session_id field"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_session_id=$(grep -ci "session.id\|session_id" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_session_id" -ge 1 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing session_id docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Test AC#2.8: Documents project field
###############################################################################

test_documents_project() {
    local test_name="AC#2.8: Documents project field"
    ((TESTS_RUN++))

    echo -e "${YELLOW}Running: $test_name${NC}"

    if [[ ! -f "$SESSION_MINER" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name (session-miner.md not found)"
        ((TEST_FAILED++))
        return
    fi

    local has_project=$(grep -ci "project" "$SESSION_MINER" 2>/dev/null || echo "0")

    if [[ "$has_project" -ge 2 ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}FAIL${NC}: $test_name (missing project docs)"
        ((TEST_FAILED++))
    fi
}

###############################################################################
# Main Test Execution
###############################################################################

main() {
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}STORY-221 Test Suite: AC#2 - Structured Field Extraction${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    # Run all tests
    test_documents_timestamp
    test_documents_command
    test_documents_status
    test_documents_duration
    test_documents_user_input
    test_documents_model
    test_documents_session_id
    test_documents_project

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
