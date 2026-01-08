#!/bin/bash
# STORY-192 AC-4: Terminology Updated
# Test: phase-02-test-first.md shows "Test Specification Generated" for Slash Commands
#
# Structural test validating that phase-02-test-first.md has updated
# terminology distinguishing test specifications from executable tests.
#
# Expected: FAIL (until implementation complete)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEST_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/phases/phase-02-test-first.md"

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
echo "STORY-192 AC-4: Terminology Updated"
echo "=============================================="
echo ""

# Verify test file exists
if [[ ! -f "$TEST_FILE" ]]; then
    echo "FAIL: Test file does not exist: $TEST_FILE"
    exit 1
fi

# Test 1: Test Specification Generated terminology
# Looking for "Test Specification Generated" phrase
assert_pattern_exists \
    "[Tt]est [Ss]pecification [Gg]enerated" \
    "Term 'Test Specification Generated' is used"

# Test 2: Slash Command context for specification terminology
# Looking for Slash Command association with specification terminology
assert_pattern_exists \
    "[Ss]lash [Cc]ommand.*[Ss]pecification|[Ss]pecification.*[Ss]lash|FOR.*[Ss]lash.*[Ss]pecification" \
    "Slash Command linked to specification terminology"

# Test 3: Distinction between output types in Phase 02
# Looking for conditional output based on implementation type
assert_pattern_exists \
    "IF.*[Ss]lash|IF.*[Cc]ommand.*[Ss]pecification|IF.*\\.md.*[Ss]pecification" \
    "Conditional output based on implementation type"

# Test 4: Updated display/message for Phase 02
# Looking for display or message that uses new terminology
assert_pattern_exists \
    "[Dd]isplay.*[Ss]pecification|[Mm]essage.*[Ss]pecification|[Oo]utput.*[Ss]pecification" \
    "Display/message uses specification terminology"

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
