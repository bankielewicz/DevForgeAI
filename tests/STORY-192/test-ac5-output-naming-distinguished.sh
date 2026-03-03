#!/bin/bash
# STORY-192 AC-5: Output Naming Distinguished
# Test: test-automator.md distinguishes TEST-SPECIFICATION.md vs test_*.py
#
# Structural test validating that test-automator.md has output naming
# conventions for both specification documents and executable tests.
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
echo "STORY-192 AC-5: Output Naming Distinguished"
echo "=============================================="
echo ""

# Verify test file exists
if [[ ! -f "$TEST_FILE" ]]; then
    echo "FAIL: Test file does not exist: $TEST_FILE"
    exit 1
fi

# Test 1: TEST-SPECIFICATION.md naming pattern
# Looking for TEST-SPECIFICATION.md output pattern
assert_pattern_exists \
    "TEST-SPECIFICATION\\.md|TEST-SPECIFICATION" \
    "TEST-SPECIFICATION.md naming pattern present"

# Test 2: test_*.py naming pattern (Python executable tests)
# Looking for test_*.py output pattern
assert_pattern_exists \
    "test_\*\\.py|test_.*\\.py" \
    "test_*.py naming pattern present"

# Test 3: Alternative test naming patterns (JS/TS)
# Looking for *.test.js or similar patterns
assert_pattern_exists \
    "\\.test\\.js|\\.test\\.ts|\\.spec\\." \
    "JavaScript/TypeScript test naming patterns present"

# Test 4: Output naming section exists
# Looking for section documenting output naming conventions
assert_pattern_exists \
    "[Oo]utput [Nn]aming|[Ff]ile [Nn]aming.*[Oo]utput|[Oo]utput.*[Ff]ile.*[Nn]ame" \
    "Output naming section/documentation exists"

# Test 5: Distinction between naming conventions
# Looking for explicit contrast between the two naming schemes
assert_pattern_exists \
    "TEST-SPECIFICATION.*vs.*test_|test_.*vs.*SPECIFICATION|[Ss]pecification.*[Nn]ame.*vs" \
    "Distinction between naming conventions documented"

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
