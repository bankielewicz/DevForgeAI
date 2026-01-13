#!/bin/bash

################################################################################
# TEST SUITE: AC#3 - PATTERN-001 Specifically Documented
# Story: STORY-210
# Description: Verify PATTERN-001 (Premature Workflow Completion) is documented
#
# Acceptance Criteria:
# - PATTERN-001 section exists
# - Pattern name is "Premature Workflow Completion"
# - RCA-009 is referenced as first identification
# - RCA-013 is referenced in recurrences
# - RCA-018 is referenced in recurrences
# - Behavior mentions "completes early phases but skips late phases"
# - Root cause mentions "Missing enforcement for administrative phases"
# - CLI validation gates mentioned in prevention
# - TodoWrite integration mentioned in solution
# - Story references accurate (STORY-027, STORY-057, STORY-078)
#
# Test Status: FAILING (Red Phase) - content not present
################################################################################

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#3: PATTERN-001 Specifically Documented"
PATTERNS_FILE="$PROJECT_ROOT/devforgeai/RCA/PATTERNS.md"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to assert pattern/content exists in file
assert_contains_pattern() {
    local file_path="$1"
    local pattern="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ ! -f "$file_path" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File does not exist: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi

    if grep -q "$pattern" "$file_path" 2>/dev/null; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Pattern not found: $pattern"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Print test header
echo ""
echo "====== $TEST_NAME ======"
echo ""

# Test PATTERN-001 header
assert_contains_pattern "$PATTERNS_FILE" "^## PATTERN-001:" "PATTERN-001 section exists" || true

# Test pattern name
assert_contains_pattern "$PATTERNS_FILE" "Premature Workflow Completion" "Pattern name documented" || true

# Test RCA references
assert_contains_pattern "$PATTERNS_FILE" "RCA-009" "RCA-009 referenced" || true
assert_contains_pattern "$PATTERNS_FILE" "RCA-013" "RCA-013 referenced" || true
assert_contains_pattern "$PATTERNS_FILE" "RCA-018" "RCA-018 referenced" || true

# Test identification details
assert_contains_pattern "$PATTERNS_FILE" "2025-11-14" "RCA-009 date (2025-11-14) present" || true
assert_contains_pattern "$PATTERNS_FILE" "STORY-027" "STORY-027 referenced" || true

# Test behavioral description
assert_contains_pattern "$PATTERNS_FILE" "completes.*early phases" "Completes early phases mentioned" || true
assert_contains_pattern "$PATTERNS_FILE" "skips.*late phases" "Skips late phases mentioned" || true

# Test root cause
assert_contains_pattern "$PATTERNS_FILE" "Missing enforcement" "Missing enforcement mentioned" || true
assert_contains_pattern "$PATTERNS_FILE" "administrative phases" "Administrative phases mentioned" || true

# Test prevention strategy components
assert_contains_pattern "$PATTERNS_FILE" "CLI validation gates" "CLI validation gates mentioned" || true
assert_contains_pattern "$PATTERNS_FILE" "TodoWrite" "TodoWrite integration mentioned" || true
assert_contains_pattern "$PATTERNS_FILE" "self-check" "Self-check mentioned" || true

# Test other story references
assert_contains_pattern "$PATTERNS_FILE" "STORY-057" "STORY-057 referenced" || true
assert_contains_pattern "$PATTERNS_FILE" "STORY-078" "STORY-078 referenced" || true

# Print summary
echo ""
echo "====== Test Results ======"
echo "Tests run:   $TESTS_RUN"
echo "Passed:      $TESTS_PASSED"
echo "Failed:      $TESTS_FAILED"

# Exit with appropriate code
if [ "$TESTS_FAILED" -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
