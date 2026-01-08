#!/bin/bash
# STORY-192 AC-1: Implementation Type Detected
# Test: test-automator.md contains implementation type detection section
#
# Structural test validating that test-automator.md has logic to detect
# Slash Command vs Code implementation types.
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
echo "STORY-192 AC-1: Implementation Type Detection"
echo "=============================================="
echo ""

# Verify test file exists
if [[ ! -f "$TEST_FILE" ]]; then
    echo "FAIL: Test file does not exist: $TEST_FILE"
    exit 1
fi

# Test 1: Section header for implementation type detection
# Looking for a section that discusses detecting implementation type
assert_pattern_exists \
    "^##.*[Ii]mplementation [Tt]ype|^##.*[Dd]etect.*[Tt]ype" \
    "Section header for implementation type detection exists"

# Test 2: Slash Command detection logic
# Looking for conditional logic that checks for Slash Command
assert_pattern_exists \
    "[Ss]lash [Cc]ommand.*\\.md|implementation_type.*==.*[Ss]lash|IF.*[Ss]lash [Cc]ommand" \
    "Slash Command detection logic present"

# Test 3: Code implementation detection logic
# Looking for conditional logic that checks for Code implementation
assert_pattern_exists \
    "implementation_type.*==.*[Cc]ode|IF.*[Cc]ode.*[Pp]ython|IF.*[Cc]ode.*\\.py" \
    "Code implementation detection logic present"

# Test 4: Detection algorithm or workflow documented
# Looking for a detection workflow or algorithm
assert_pattern_exists \
    "[Dd]etect.*implementation|[Ii]mplementation.*[Dd]etection|[Tt]ype [Dd]etection" \
    "Detection workflow/algorithm documented"

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
