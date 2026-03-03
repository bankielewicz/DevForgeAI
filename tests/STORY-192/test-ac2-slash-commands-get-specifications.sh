#!/bin/bash
# STORY-192 AC-2: Slash Commands Get Specifications
# Test: test-automator.md generates "Test Specification Document" for Slash Commands
#
# Structural test validating that test-automator.md has output logic
# distinguishing Test Specification Documents for Slash Commands.
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
echo "STORY-192 AC-2: Slash Commands Get Specifications"
echo "=============================================="
echo ""

# Verify test file exists
if [[ ! -f "$TEST_FILE" ]]; then
    echo "FAIL: Test file does not exist: $TEST_FILE"
    exit 1
fi

# Test 1: Test Specification Document terminology
# Looking for explicit mention of "Test Specification Document"
assert_pattern_exists \
    "[Tt]est [Ss]pecification [Dd]ocument" \
    "Term 'Test Specification Document' is used"

# Test 2: Slash Commands associated with specifications (not executable tests)
# Looking for logic linking Slash Commands to specifications
assert_pattern_exists \
    "[Ss]lash [Cc]ommand.*[Ss]pecification|[Ss]pecification.*[Ss]lash [Cc]ommand" \
    "Slash Commands linked to specifications"

# Test 3: Not executable for Slash Commands
# Looking for clarification that Slash Command tests are NOT executable
assert_pattern_exists \
    "not executable|non-executable|specification.*not.*executable" \
    "Non-executable nature documented for Slash Commands"

# Test 4: Generate instruction for specifications
# Looking for generate/output instruction for specifications
assert_pattern_exists \
    "[Gg]enerate.*[Ss]pecification|[Oo]utput.*[Ss]pecification" \
    "Generate/output instruction for specifications present"

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
