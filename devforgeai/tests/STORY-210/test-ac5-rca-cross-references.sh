#!/bin/bash

################################################################################
# TEST SUITE: AC#5 - Related RCAs Cross-Referenced
# Story: STORY-210
# Description: Verify RCA cross-references with table format and relationships
#
# Acceptance Criteria:
# - "Related RCAs" section with table format exists
# - RCA-009 present with date 2025-11-14 and STORY-027
# - RCA-011 present with date 2025-11-19 and STORY-044
# - RCA-013 present with date 2025-11-22 and STORY-057
# - RCA-018 present with date 2025-12-05 and STORY-078
# - Relationship descriptions present:
#   - RCA-009: "First identification"
#   - RCA-011: "Phase 1 Step 4 specific"
#   - RCA-013: "Late-phase pattern (4.5-7)"
#   - RCA-018: "Comprehensive analysis"
#
# Test Status: FAILING (Red Phase) - table not present
################################################################################

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#5: Related RCAs Cross-Referenced"
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

# Test Related RCAs section header
assert_contains_pattern "$PATTERNS_FILE" "^### Related RCAs" "Related RCAs section present" || true

# Test RCA-009 entry (first identification)
assert_contains_pattern "$PATTERNS_FILE" "RCA-009" "RCA-009 referenced" || true
assert_contains_pattern "$PATTERNS_FILE" "2025-11-14" "RCA-009 date (2025-11-14) present" || true
assert_contains_pattern "$PATTERNS_FILE" "STORY-027" "STORY-027 referenced with RCA-009" || true
assert_contains_pattern "$PATTERNS_FILE" "First identification" "RCA-009 relationship: First identification" || true

# Test RCA-011 entry (Phase 1 specific)
assert_contains_pattern "$PATTERNS_FILE" "RCA-011" "RCA-011 referenced" || true
assert_contains_pattern "$PATTERNS_FILE" "2025-11-19" "RCA-011 date (2025-11-19) present" || true
assert_contains_pattern "$PATTERNS_FILE" "STORY-044" "STORY-044 referenced with RCA-011" || true
assert_contains_pattern "$PATTERNS_FILE" "Phase 1.*specific" "RCA-011 relationship: Phase 1 specific" || true

# Test RCA-013 entry (Late-phase pattern)
assert_contains_pattern "$PATTERNS_FILE" "RCA-013" "RCA-013 referenced" || true
assert_contains_pattern "$PATTERNS_FILE" "2025-11-22" "RCA-013 date (2025-11-22) present" || true
assert_contains_pattern "$PATTERNS_FILE" "STORY-057" "STORY-057 referenced with RCA-013" || true
assert_contains_pattern "$PATTERNS_FILE" "Late-phase" "RCA-013 relationship: Late-phase pattern" || true

# Test RCA-018 entry (Comprehensive analysis)
assert_contains_pattern "$PATTERNS_FILE" "RCA-018" "RCA-018 referenced" || true
assert_contains_pattern "$PATTERNS_FILE" "2025-12-05" "RCA-018 date (2025-12-05) present" || true
assert_contains_pattern "$PATTERNS_FILE" "STORY-078" "STORY-078 referenced with RCA-018" || true
assert_contains_pattern "$PATTERNS_FILE" "Comprehensive" "RCA-018 relationship: Comprehensive analysis" || true

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
