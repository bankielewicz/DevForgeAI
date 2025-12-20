#!/bin/bash
#
# STORY-109 AC#2: CLAUDE.md Section Generation Tests
# TDD Phase: RED (tests expected to fail until implementation)
#
# Tests that the registry generator produces:
# - Agent name and description table
# - Proactive trigger mapping
# - Valid markdown format
#

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Project paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
GENERATOR_SCRIPT="$PROJECT_ROOT/scripts/generate-subagent-registry.sh"
FIXTURES_DIR="$SCRIPT_DIR/test-fixtures"
RESULTS_DIR="$SCRIPT_DIR/results"

# Ensure results directory exists
mkdir -p "$RESULTS_DIR"

# Assert helpers
assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"
    TESTS_RUN=$((TESTS_RUN + 1))
    if echo "$haystack" | grep -q "$needle"; then
        echo -e "  ${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "  ${RED}✗${NC} $message"
        echo -e "    Expected to contain: '$needle'"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_contains_pattern() {
    local haystack="$1"
    local pattern="$2"
    local message="$3"
    TESTS_RUN=$((TESTS_RUN + 1))
    if echo "$haystack" | grep -qE "$pattern"; then
        echo -e "  ${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "  ${RED}✗${NC} $message"
        echo -e "    Expected pattern: '$pattern'"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Header
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  STORY-109 AC#2: Section Generation Tests${NC}"
echo -e "${BLUE}  TDD Phase: RED${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check script exists
if [ ! -f "$GENERATOR_SCRIPT" ]; then
    echo -e "${YELLOW}⚠ Generator script not found: $GENERATOR_SCRIPT${NC}"
    echo -e "${YELLOW}  This is expected in RED phase - tests will fail${NC}"
    echo ""
fi

# Try to generate registry output from fixtures
GENERATED_OUTPUT=""
if [ -f "$GENERATOR_SCRIPT" ]; then
    GENERATED_OUTPUT=$("$GENERATOR_SCRIPT" --generate-only --agents-dir "$FIXTURES_DIR" 2>/dev/null || echo "")
fi

# Test Group 1: Agent Table Format
echo -e "${BLUE}Test Group 1: Agent Table Format${NC}"

# Test 1.1: Output contains agent table header
if [ -n "$GENERATED_OUTPUT" ]; then
    assert_contains "$GENERATED_OUTPUT" "| Agent | Description | Tools |" "Agent table has correct header columns"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Agent table has correct header columns"
    echo -e "    Error: No output from generator script"
fi

# Test 1.2: Output contains table separator
if [ -n "$GENERATED_OUTPUT" ]; then
    assert_contains_pattern "$GENERATED_OUTPUT" "\|[-]+\|[-]+\|[-]+\|" "Agent table has markdown separator row"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Agent table has markdown separator row"
    echo -e "    Error: No output from generator script"
fi

echo ""

# Test Group 2: Trigger Mapping Section
echo -e "${BLUE}Test Group 2: Trigger Mapping Section${NC}"

# Test 2.1: Output contains trigger mapping header
if [ -n "$GENERATED_OUTPUT" ]; then
    assert_contains "$GENERATED_OUTPUT" "### Proactive Trigger Mapping" "Trigger mapping section header exists"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Trigger mapping section header exists"
    echo -e "    Error: No output from generator script"
fi

# Test 2.2: Trigger table has correct columns
if [ -n "$GENERATED_OUTPUT" ]; then
    assert_contains "$GENERATED_OUTPUT" "| Trigger Pattern | Recommended Agent |" "Trigger table has correct columns"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Trigger table has correct columns"
    echo -e "    Error: No output from generator script"
fi

echo ""

# Test Group 3: Marker Comments
echo -e "${BLUE}Test Group 3: Marker Comments${NC}"

# Test 3.1: Output starts with BEGIN marker
if [ -n "$GENERATED_OUTPUT" ]; then
    assert_contains "$GENERATED_OUTPUT" "<!-- BEGIN SUBAGENT REGISTRY -->" "Output contains BEGIN marker"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Output contains BEGIN marker"
    echo -e "    Error: No output from generator script"
fi

# Test 3.2: Output ends with END marker
if [ -n "$GENERATED_OUTPUT" ]; then
    assert_contains "$GENERATED_OUTPUT" "<!-- END SUBAGENT REGISTRY -->" "Output contains END marker"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Output contains END marker"
    echo -e "    Error: No output from generator script"
fi

echo ""

# Test Group 4: Valid Markdown
echo -e "${BLUE}Test Group 4: Valid Markdown${NC}"

# Test 4.1: No-edit warning present
if [ -n "$GENERATED_OUTPUT" ]; then
    assert_contains "$GENERATED_OUTPUT" "DO NOT EDIT MANUALLY" "Contains no-edit warning"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Contains no-edit warning"
    echo -e "    Error: No output from generator script"
fi

echo ""

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  Tests Run:    $TESTS_RUN"
echo -e "  ${GREEN}Passed:       $TESTS_PASSED${NC}"
echo -e "  ${RED}Failed:       $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}AC#2 FAILED - $TESTS_FAILED test(s) failed${NC}"
    exit 1
else
    echo -e "${GREEN}AC#2 PASSED - All tests passed${NC}"
    exit 0
fi
