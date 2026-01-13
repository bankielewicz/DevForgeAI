#!/bin/bash

################################################################################
# TEST SUITE: AC#2 - Pattern Template Structure
# Story: STORY-210
# Description: Verify PATTERNS.md contains required template sections
#
# Acceptance Criteria:
# - File contains main header "# Recurring RCA Patterns"
# - Pattern template includes all required sections:
#   - Pattern ID (PATTERN-NNN)
#   - First Identified
#   - Recurrences
#   - Frequency
#   - Status
#   - Behavior section
#   - Root Cause section
#   - Detection Indicators section
#   - Prevention Strategy section
#   - Metrics section
#   - Related RCAs section
# - Pattern Index section exists
# - "Adding New Patterns" guide section exists
#
# Test Status: FAILING (Red Phase) - structure not present
################################################################################

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#2: Pattern Template Structure"
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

# Test main header
assert_contains_pattern "$PATTERNS_FILE" "^# Recurring RCA Patterns" "Main header present" || true

# Test pattern structure sections
assert_contains_pattern "$PATTERNS_FILE" "^## PATTERN-" "Pattern header exists" || true
assert_contains_pattern "$PATTERNS_FILE" "^\*\*First Identified:\*\*" "First Identified field present" || true
assert_contains_pattern "$PATTERNS_FILE" "^\*\*Recurrences:\*\*" "Recurrences field present" || true
assert_contains_pattern "$PATTERNS_FILE" "^\*\*Frequency:\*\*" "Frequency field present" || true
assert_contains_pattern "$PATTERNS_FILE" "^\*\*Status:\*\*" "Status field present" || true

# Test required sections
assert_contains_pattern "$PATTERNS_FILE" "^### Behavior" "Behavior section present" || true
assert_contains_pattern "$PATTERNS_FILE" "^### Root Cause" "Root Cause section present" || true
assert_contains_pattern "$PATTERNS_FILE" "^### Detection Indicators" "Detection Indicators section present" || true
assert_contains_pattern "$PATTERNS_FILE" "^### Prevention Strategy" "Prevention Strategy section present" || true
assert_contains_pattern "$PATTERNS_FILE" "^### Metrics" "Metrics section present" || true
assert_contains_pattern "$PATTERNS_FILE" "^### Related RCAs" "Related RCAs section present" || true

# Test guide sections
assert_contains_pattern "$PATTERNS_FILE" "^## Pattern Index" "Pattern Index section present" || true
assert_contains_pattern "$PATTERNS_FILE" "^## Adding New Patterns" "Adding New Patterns guide present" || true

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
