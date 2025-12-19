#!/bin/bash
################################################################################
# TEST SUITE: AC#1 - Configuration File Schema
# Story: STORY-108
# Description: Validates parallel-orchestration.yaml schema structure
#
# Acceptance Criteria:
# - Config file exists at devforgeai/config/parallel-orchestration.yaml
# - File supports profile definitions with max_concurrent_tasks, timeout_ms, retry
# - Required fields: version, default_profile, profiles
#
# Test Status: FAILING (Red Phase)
################################################################################

set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CONFIG_FILE="$PROJECT_ROOT/devforgeai/config/parallel-orchestration.yaml"
TEST_NAME="AC#1: Configuration File Schema"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

################################################################################
# Helper Functions
################################################################################

assert_file_exists() {
    local file_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -f "$file_path" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  File: $file_path"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected file: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_field_present() {
    local file_path="$1"
    local field_pattern="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ ! -f "$file_path" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File not found: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi

    if grep -q "$field_pattern" "$file_path"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Pattern found: $field_pattern"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Pattern not found: $field_pattern"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# Test Suite
################################################################################

echo ""
echo "========================================"
echo "  $TEST_NAME"
echo "  Story: STORY-108"
echo "========================================"
echo ""

echo -e "${BLUE}Test Group 1: File Existence${NC}"
echo "----------------------------------------"

# Test 1: Config file exists
assert_file_exists "$CONFIG_FILE" "Config file exists at expected location"

echo ""
echo -e "${BLUE}Test Group 2: Required Top-Level Fields${NC}"
echo "----------------------------------------"

# Test 2: Version field present
assert_field_present "$CONFIG_FILE" "^version:" "Version field present at root level"

# Test 3: Default profile field present
assert_field_present "$CONFIG_FILE" "^default_profile:" "default_profile field present at root level"

# Test 4: Profiles section present
assert_field_present "$CONFIG_FILE" "^profiles:" "profiles section present at root level"

################################################################################
# Summary
################################################################################

echo ""
echo "========================================"
echo "  Test Summary"
echo "========================================"
echo "Tests Run:    $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}RESULT: FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}RESULT: PASSED${NC}"
    exit 0
fi
