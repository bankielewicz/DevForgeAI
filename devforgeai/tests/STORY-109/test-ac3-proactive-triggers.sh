#!/bin/bash
#
# STORY-109 AC#3: Proactive Triggers Field Tests
# TDD Phase: RED (tests expected to fail until implementation)
#
# Tests that proactive_triggers field:
# - Is documented in schema
# - Appears in registry output
# - Maps triggers to correct agents
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
SCHEMA_DOC="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references/subagent-registry.md"
FIXTURES_DIR="$SCRIPT_DIR/test-fixtures"

# Assert helpers
assert_file_exists() {
    local file="$1"
    local message="$2"
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "  ${RED}✗${NC} $message"
        echo -e "    File not found: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_file_contains() {
    local file="$1"
    local pattern="$2"
    local message="$3"
    TESTS_RUN=$((TESTS_RUN + 1))
    if [ -f "$file" ] && grep -q "$pattern" "$file"; then
        echo -e "  ${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "  ${RED}✗${NC} $message"
        echo -e "    Pattern not found: '$pattern'"
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
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Header
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  STORY-109 AC#3: Proactive Triggers Field Tests${NC}"
echo -e "${BLUE}  TDD Phase: RED${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Test Group 1: Schema Documentation
echo -e "${BLUE}Test Group 1: Schema Documentation${NC}"

# Test 1.1: Schema documentation file exists
assert_file_exists "$SCHEMA_DOC" "Schema documentation file exists"

# Test 1.2: proactive_triggers field documented
assert_file_contains "$SCHEMA_DOC" "proactive_triggers" "proactive_triggers field documented in schema"

echo ""

# Test Group 2: Triggers in Registry Output
echo -e "${BLUE}Test Group 2: Triggers in Registry Output${NC}"

# Generate output from fixtures
GENERATED_OUTPUT=""
if [ -f "$GENERATOR_SCRIPT" ]; then
    GENERATED_OUTPUT=$("$GENERATOR_SCRIPT" --generate-only --agents-dir "$FIXTURES_DIR" 2>/dev/null || echo "")
fi

# Test 2.1: Trigger appears in registry
if [ -n "$GENERATED_OUTPUT" ]; then
    assert_contains "$GENERATED_OUTPUT" "after code changes" "Trigger 'after code changes' appears in registry"
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Trigger 'after code changes' appears in registry"
    echo -e "    Error: No output from generator script"
fi

echo ""

# Test Group 3: Trigger-to-Agent Mapping
echo -e "${BLUE}Test Group 3: Trigger-to-Agent Mapping${NC}"

# Test 3.1: Trigger mapped to correct agent
if [ -n "$GENERATED_OUTPUT" ]; then
    # Look for trigger and agent on same line or in proper mapping format
    if echo "$GENERATED_OUTPUT" | grep -q "after code changes.*test-agent-full\|test-agent-full.*after code changes"; then
        assert_contains "$GENERATED_OUTPUT" "test-agent-full" "Trigger mapped to correct agent (test-agent-full)"
    else
        # Check if both exist in trigger mapping section
        TESTS_RUN=$((TESTS_RUN + 1))
        if echo "$GENERATED_OUTPUT" | grep -A5 "Trigger Pattern" | grep -q "test-agent-full"; then
            echo -e "  ${GREEN}✓${NC} Trigger mapped to correct agent (test-agent-full)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "  ${RED}✗${NC} Trigger mapped to correct agent (test-agent-full)"
            echo -e "    Trigger should map to agent that defined it"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    fi
else
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo -e "  ${RED}✗${NC} Trigger mapped to correct agent (test-agent-full)"
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
    echo -e "${RED}AC#3 FAILED - $TESTS_FAILED test(s) failed${NC}"
    exit 1
else
    echo -e "${GREEN}AC#3 PASSED - All tests passed${NC}"
    exit 0
fi
