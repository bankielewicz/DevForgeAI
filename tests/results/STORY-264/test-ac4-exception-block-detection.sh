#!/bin/bash
# =============================================================================
# STORY-264 AC#4: Exception Block Detection
# =============================================================================
# Test: Validates test-automator.md has guidance for detecting try/except/catch
#       blocks and generating tests that trigger each exception handler
#
# Implementation Type: Slash Command (.md) - structural validation
# Target File: .claude/agents/test-automator.md
# Expected State: FAILING (RED) - guidance not yet implemented
# =============================================================================

set -e

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
TARGET_FILE="${PROJECT_ROOT}/.claude/agents/test-automator.md"
TEST_NAME="AC#4: Exception Block Detection"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function
assert_pattern_exists() {
    local pattern="$1"
    local description="$2"
    TESTS_RUN=$((TESTS_RUN + 1))

    if grep -qE "$pattern" "$TARGET_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $description"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "       Pattern not found: $pattern"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_section_exists() {
    local section="$1"
    local description="$2"
    TESTS_RUN=$((TESTS_RUN + 1))

    if grep -qE "^##+ .*${section}" "$TARGET_FILE" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $description"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "       Section header not found: $section"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# =============================================================================
# TEST EXECUTION
# =============================================================================

echo "=============================================="
echo "STORY-264 ${TEST_NAME}"
echo "=============================================="
echo "Target: ${TARGET_FILE}"
echo ""

# Verify target file exists
if [[ ! -f "$TARGET_FILE" ]]; then
    echo -e "${RED}ERROR${NC}: Target file not found: $TARGET_FILE"
    exit 1
fi

echo "--- Structural Tests: Exception Block Detection ---"
echo ""

# Test 1: Section for exception block detection
assert_section_exists "Exception.*Block|Block.*Detection|try.*except.*Detection" \
    "Section for exception block detection exists"

# Test 2: Python try/except detection pattern
assert_pattern_exists "try.*except|except.*block|Python.*exception" \
    "Python try/except detection pattern documented"

# Test 3: JavaScript/TypeScript try/catch detection pattern
assert_pattern_exists "try.*catch|catch.*block|JavaScript.*exception|TypeScript.*exception" \
    "JavaScript/TypeScript try/catch detection pattern documented"

# Test 4: COMP-001: Parse method/function for try/except blocks
assert_pattern_exists "parse.*try|identify.*exception.*block|analyz.*exception.*handler" \
    "COMP-001: Parsing methods for exception blocks"

# Test 5: COMP-002: Map exception types to test targets
assert_pattern_exists "map.*exception.*type|exception.*type.*test|ValueError|TypeError|KeyError" \
    "COMP-002: Exception type to test mapping"

# Test 6: COMP-004: Generate exception trigger tests
assert_pattern_exists "trigger.*exception|exception.*trigger|generat.*test.*trigger" \
    "COMP-004: Exception trigger test generation"

# Test 7: Guidance for triggering specific exception handlers
assert_pattern_exists "argument.*trigger|input.*trigger|condition.*trigger" \
    "Guidance for triggering exception handlers with specific arguments"

# Test 8: Example showing detection of multiple exception handlers
assert_pattern_exists "multiple.*except|3.*except|all.*exception.*handler" \
    "Example detecting multiple exception handlers in single method"

# Test 9: finally/finally block handling
assert_pattern_exists "finally|cleanup.*block|finall.*handler" \
    "finally block handling documented"

echo ""
echo "=============================================="
echo "RESULTS: ${TESTS_PASSED}/${TESTS_RUN} tests passed"
echo "=============================================="

if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${RED}STATUS: FAILING (RED)${NC} - Implementation needed"
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING (GREEN)${NC}"
    exit 0
fi
