#!/bin/bash
# STORY-192 AC-3: Code Gets Executable Tests
# Test: test-automator.md generates "Executable unit tests" for Code implementations
#
# Structural test validating that test-automator.md distinguishes
# executable unit tests for code (Python/JS/etc) implementations.
#
# Expected: FAIL (until implementation complete)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEST_FILE="$PROJECT_ROOT/.claude/agents/test-automator.md"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper function
assert_pattern_exists() {
    local pattern="$1"
    local description="$2"

    if grep -qE "$pattern" "$TEST_FILE" 2>/dev/null; then
        echo "PASS: $description"
        ((TESTS_PASSED++))
    else
        echo "FAIL: $description"
        echo "  Expected pattern: $pattern"
        echo "  File: $TEST_FILE"
        ((TESTS_FAILED++))
    fi
}

echo "=============================================="
echo "STORY-192 AC-3: Code Gets Executable Tests"
echo "=============================================="
echo ""

# Verify test file exists
if [[ ! -f "$TEST_FILE" ]]; then
    echo "FAIL: Test file does not exist: $TEST_FILE"
    exit 1
fi

# Test 1: Executable unit tests terminology
# Looking for explicit mention of "Executable unit tests"
assert_pattern_exists \
    "[Ee]xecutable unit tests|[Ee]xecutable tests" \
    "Term 'Executable unit tests' is used"

# Test 2: Code implementations linked to executable tests
# Looking for logic linking Code to executable tests
assert_pattern_exists \
    "[Cc]ode.*[Ee]xecutable|[Pp]ython.*[Ee]xecutable|implementation.*[Ee]xecutable" \
    "Code implementations linked to executable tests"

# Test 3: Distinction between specification and executable
# Looking for explicit distinction/contrast between the two types
assert_pattern_exists \
    "[Ss]pecification.*vs.*[Ee]xecutable|[Ee]xecutable.*vs.*[Ss]pecification|distinguish.*specification.*executable" \
    "Distinction between specification and executable documented"

# Test 4: Generate instruction for executable tests
# Looking for generate/output instruction for executable tests
assert_pattern_exists \
    "[Gg]enerate.*[Ee]xecutable|[Oo]utput.*test_\*|[Oo]utput.*\\.test\\." \
    "Generate/output instruction for executable tests present"

echo ""
echo "=============================================="
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
echo "=============================================="

if [[ $TESTS_FAILED -gt 0 ]]; then
    echo ""
    echo "NOTE: Failures expected until STORY-192 implementation complete."
    exit 1
fi

exit 0
