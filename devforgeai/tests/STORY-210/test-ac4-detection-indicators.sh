#!/bin/bash

################################################################################
# TEST SUITE: AC#4 - Detection Indicators for User and Claude
# Story: STORY-210
# Description: Verify detection indicators documented for both user and Claude
#
# Acceptance Criteria:
# - "Detection Indicators" section exists
# - "For User:" subsection present
# - "For Claude (self-detection):" subsection present
# - User indicators include:
#   - "Workflow displays \"COMPLETE\" but todo list shows pending phases"
#   - "Story file not updated"
#   - "No git commit"
# - Claude indicators include:
#   - "About to display \"Workflow Complete\" banner"
#   - "TodoWrite shows <10 phases completed"
#   - "Run self-check before declaring complete"
#
# Test Status: FAILING (Red Phase) - sections not present
################################################################################

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#4: Detection Indicators for User and Claude"
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

# Test Detection Indicators section header
assert_contains_pattern "$PATTERNS_FILE" "^### Detection Indicators" "Detection Indicators section present" || true

# Test "For User:" subsection
assert_contains_pattern "$PATTERNS_FILE" "^\*\*For User:\*\*" "For User subsection present" || true

# Test user indicators
assert_contains_pattern "$PATTERNS_FILE" "Workflow displays.*COMPLETE.*todo list shows pending" "User indicator: Workflow displays COMPLETE" || true
assert_contains_pattern "$PATTERNS_FILE" "Story file not updated" "User indicator: Story file not updated" || true
assert_contains_pattern "$PATTERNS_FILE" "No git commit" "User indicator: No git commit" || true

# Test "For Claude (self-detection):" subsection
assert_contains_pattern "$PATTERNS_FILE" "^\*\*For Claude" "For Claude subsection present" || true

# Test Claude self-detection indicators
assert_contains_pattern "$PATTERNS_FILE" "About to display.*Workflow Complete.*banner" "Claude indicator: About to display COMPLETE banner" || true
assert_contains_pattern "$PATTERNS_FILE" "TodoWrite shows.*phases completed" "Claude indicator: TodoWrite phases completed" || true
assert_contains_pattern "$PATTERNS_FILE" "Run.*self-check" "Claude indicator: Run self-check" || true

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
