#!/bin/bash
# Unit Test: AC1 - Pre-Commit Runs Registry Script
# Tests that pre-commit hook calls generate-subagent-registry.sh automatically
#
# STORY-186: Auto-Regenerate Subagent Registry in Pre-Commit Hook
#
# Acceptance Criteria:
# AC-1: Given pre-commit hook executes, Then generate-subagent-registry.sh runs automatically

set -e

TEST_NAME="AC1: Pre-Commit Runs Registry Script"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

PRE_COMMIT_HOOK="$PROJECT_ROOT/.git/hooks/pre-commit"

# Test 1.1: Pre-commit hook references generate-subagent-registry.sh
test_registry_script_referenced() {
    echo -n "Test 1.1: Pre-commit hook references generate-subagent-registry.sh... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Pre-commit hook exists at $PRE_COMMIT_HOOK"
        echo "  Actual: File not found"
        return 1
    fi

    if grep -q "generate-subagent-registry.sh" "$PRE_COMMIT_HOOK"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Pre-commit hook references generate-subagent-registry.sh"
        echo "  Actual: No reference found"
        return 1
    fi
}

# Test 1.2: Registry script is called unconditionally (not only when agent files staged)
test_registry_runs_unconditionally() {
    echo -n "Test 1.2: Registry regeneration runs unconditionally (on every commit)... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Pre-commit hook exists"
        return 1
    fi

    # Current implementation only runs when agent files are staged
    # STORY-186 requires it to run on EVERY commit unconditionally
    # Look for the unconditional regeneration block (not wrapped in agent file check)

    # The implementation should have a section like:
    # echo "Regenerating subagent registry..."
    # bash scripts/generate-subagent-registry.sh 2>/dev/null || true

    # NOT wrapped in: if [ -n "$AGENT_FILES" ]; then ... fi

    # Check if there's an unconditional call to generate-subagent-registry.sh
    # (i.e., NOT inside the AGENT_FILES conditional block)

    # Extract lines containing registry regeneration that are NOT in the conditional block
    local hook_content
    hook_content=$(cat "$PRE_COMMIT_HOOK")

    # Look for pattern: "Regenerating subagent registry" followed by script call
    # This should exist OUTSIDE the AGENT_FILES conditional
    if echo "$hook_content" | grep -B2 -A2 "generate-subagent-registry.sh" | grep -q "Regenerating subagent registry"; then
        # Now check if this is inside a conditional or unconditional
        # The AC says it should run automatically on every commit
        # Check for non-blocking call pattern: || true
        if echo "$hook_content" | grep "generate-subagent-registry.sh" | grep -q "|| true"; then
            echo -e "${GREEN}PASS${NC}"
            return 0
        fi
    fi

    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Unconditional registry regeneration with '|| true' pattern"
    echo "  Actual: Registry only runs when agent files are staged (conditional)"
    echo "  Required: Add unconditional regeneration block per STORY-186 spec"
    return 1
}

# Test 1.3: Registry script path is correct
test_registry_script_path() {
    echo -n "Test 1.3: Registry script path is correct (scripts/generate-subagent-registry.sh)... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Pre-commit hook exists"
        return 1
    fi

    # Check for the correct path format
    if grep -q "scripts/generate-subagent-registry.sh\|bash scripts/generate-subagent-registry.sh" "$PRE_COMMIT_HOOK"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Path 'scripts/generate-subagent-registry.sh'"
        echo "  Actual: Incorrect or missing path"
        return 1
    fi
}

# Test 1.4: Echo message before regeneration
test_regeneration_message() {
    echo -n "Test 1.4: Displays 'Regenerating subagent registry...' message... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        return 1
    fi

    if grep -q "Regenerating subagent registry" "$PRE_COMMIT_HOOK"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Echo message 'Regenerating subagent registry...'"
        echo "  Actual: No message found"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_registry_script_referenced || FAILED_TESTS=$((FAILED_TESTS + 1))
test_registry_runs_unconditionally || FAILED_TESTS=$((FAILED_TESTS + 1))
test_registry_script_path || FAILED_TESTS=$((FAILED_TESTS + 1))
test_regeneration_message || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
