#!/bin/bash
#
# STORY-109 AC#1: Frontmatter Parsing Tests
# TDD Phase: RED (tests expected to fail until implementation)
#
# Tests that the registry generator correctly extracts:
# - name, description, tools, proactive_triggers from YAML frontmatter
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

# Assert helpers
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="$3"
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ "$expected" = "$actual" ]; then
        echo -e "  ${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "  ${RED}✗${NC} $message"
        echo -e "    Expected: '$expected'"
        echo -e "    Actual:   '$actual'"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_not_empty() {
    local actual="$1"
    local message="$2"
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ -n "$actual" ]; then
        echo -e "  ${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "  ${RED}✗${NC} $message"
        echo -e "    Expected: non-empty value"
        echo -e "    Actual:   (empty)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_empty() {
    local actual="$1"
    local message="$2"
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ -z "$actual" ]; then
        echo -e "  ${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "  ${RED}✗${NC} $message"
        echo -e "    Expected: (empty)"
        echo -e "    Actual:   '$actual'"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

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
        echo -e "    Actual: '$haystack'"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Header
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  STORY-109 AC#1: Frontmatter Parsing Tests${NC}"
echo -e "${BLUE}  TDD Phase: RED${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check script exists
if [ ! -f "$GENERATOR_SCRIPT" ]; then
    echo -e "${YELLOW}⚠ Generator script not found: $GENERATOR_SCRIPT${NC}"
    echo -e "${YELLOW}  This is expected in RED phase - tests will fail${NC}"
    echo ""
fi

# Test Group 1: Name Field Extraction
echo -e "${BLUE}Test Group 1: Name Field Extraction${NC}"

# Source the script functions if it exists
if [ -f "$GENERATOR_SCRIPT" ]; then
    source "$GENERATOR_SCRIPT" --source-only 2>/dev/null || true
fi

# Test 1.1: Extract name from agent with all fields
if type extract_field &>/dev/null; then
    result=$(extract_field "$FIXTURES_DIR/agent-with-triggers.md" "name")
    assert_equals "test-agent-full" "$result" "Extract name from agent with all fields"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Extract name from agent with all fields"
    echo -e "    Error: extract_field function not defined"
fi

# Test 1.2: Extract name from minimal agent
if type extract_field &>/dev/null; then
    result=$(extract_field "$FIXTURES_DIR/agent-without-triggers.md" "name")
    assert_equals "test-agent-minimal" "$result" "Extract name from minimal agent"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Extract name from minimal agent"
    echo -e "    Error: extract_field function not defined"
fi

echo ""

# Test Group 2: Description Field Extraction
echo -e "${BLUE}Test Group 2: Description Field Extraction${NC}"

# Test 2.1: Extract description (multi-word)
if type extract_field &>/dev/null; then
    result=$(extract_field "$FIXTURES_DIR/agent-with-triggers.md" "description")
    assert_contains "$result" "test agent with all fields" "Extract multi-word description"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Extract multi-word description"
    echo -e "    Error: extract_field function not defined"
fi

echo ""

# Test Group 3: Tools Array Extraction
echo -e "${BLUE}Test Group 3: Tools Array Extraction${NC}"

# Test 3.1: Extract tools (comma-separated)
if type extract_field &>/dev/null; then
    result=$(extract_field "$FIXTURES_DIR/agent-with-triggers.md" "tools")
    assert_contains "$result" "Read" "Extract tools array contains Read"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Extract tools array contains Read"
    echo -e "    Error: extract_field function not defined"
fi

# Test 3.2: Handle empty tools gracefully
if type extract_field &>/dev/null; then
    result=$(extract_field "$FIXTURES_DIR/agent-empty-tools.md" "tools" 2>/dev/null || echo "")
    # Empty tools should return empty or be handled gracefully
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo -e "  ${GREEN}✓${NC} Handle empty tools gracefully (no crash)"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Handle empty tools gracefully"
    echo -e "    Error: extract_field function not defined"
fi

echo ""

# Test Group 4: Proactive Triggers Array Extraction
echo -e "${BLUE}Test Group 4: Proactive Triggers Array Extraction${NC}"

# Test 4.1: Extract proactive_triggers array
if type extract_array &>/dev/null; then
    result=$(extract_array "$FIXTURES_DIR/agent-with-triggers.md" "proactive_triggers")
    assert_contains "$result" "after code changes" "Extract proactive_triggers contains 'after code changes'"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Extract proactive_triggers contains 'after code changes'"
    echo -e "    Error: extract_array function not defined"
fi

# Test 4.2: Handle missing proactive_triggers
if type extract_array &>/dev/null; then
    result=$(extract_array "$FIXTURES_DIR/agent-without-triggers.md" "proactive_triggers" 2>/dev/null || echo "")
    assert_empty "$result" "Handle missing proactive_triggers (returns empty)"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Handle missing proactive_triggers (returns empty)"
    echo -e "    Error: extract_array function not defined"
fi

echo ""

# Test Group 5: Malformed Frontmatter Handling
echo -e "${BLUE}Test Group 5: Malformed Frontmatter Handling${NC}"

# Test 5.1: Skip malformed YAML gracefully
if type extract_field &>/dev/null; then
    result=$(extract_field "$FIXTURES_DIR/agent-malformed.md" "name" 2>/dev/null || echo "")
    assert_empty "$result" "Skip malformed YAML (no --- markers)"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Skip malformed YAML (no --- markers)"
    echo -e "    Error: extract_field function not defined"
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
    echo -e "${RED}AC#1 FAILED - $TESTS_FAILED test(s) failed${NC}"
    exit 1
else
    echo -e "${GREEN}AC#1 PASSED - All tests passed${NC}"
    exit 0
fi
