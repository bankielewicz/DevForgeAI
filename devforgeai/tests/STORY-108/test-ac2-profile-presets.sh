#!/bin/bash
################################################################################
# TEST SUITE: AC#2 - Profile Presets
# Story: STORY-108
# Description: Validates profile preset definitions (Pro/Max/API)
#
# Acceptance Criteria:
# - Pro preset: max_concurrent_tasks=4, timeout_ms=120000
# - Max preset: max_concurrent_tasks=6, timeout_ms=180000
# - API preset: max_concurrent_tasks=8, timeout_ms=300000
#
# Test Status: FAILING (Red Phase)
################################################################################

set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CONFIG_FILE="$PROJECT_ROOT/devforgeai/config/parallel-orchestration.yaml"
TEST_NAME="AC#2: Profile Presets"

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

assert_profile_exists() {
    local profile_name="$1"
    local description="Profile '$profile_name' exists"
    ((TESTS_RUN++))

    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Config file not found: $CONFIG_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    if grep -q "^  $profile_name:" "$CONFIG_FILE"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Profile not found in config"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_profile_value() {
    local profile_name="$1"
    local field_name="$2"
    local expected_value="$3"
    local description="Profile '$profile_name' has $field_name=$expected_value"
    ((TESTS_RUN++))

    if [ ! -f "$CONFIG_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Config file not found: $CONFIG_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    # Extract value from profile section (grep 10 lines after profile name)
    local actual_value
    actual_value=$(grep -A 10 "^  $profile_name:" "$CONFIG_FILE" | grep "$field_name:" | head -1 | awk '{print $2}' | tr -d ' ' | sed 's/#.*//')

    if [ "$actual_value" = "$expected_value" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Actual: $actual_value"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected: $expected_value"
        echo "  Actual: $actual_value"
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

echo -e "${BLUE}Test Group 1: Pro Profile (Claude Pro Tier)${NC}"
echo "----------------------------------------"

# Tests 1-3: Pro profile
assert_profile_exists "pro"
assert_profile_value "pro" "max_concurrent_tasks" "4"
assert_profile_value "pro" "timeout_ms" "120000"

echo ""
echo -e "${BLUE}Test Group 2: Max Profile (Power Users)${NC}"
echo "----------------------------------------"

# Tests 4-6: Max profile
assert_profile_exists "max"
assert_profile_value "max" "max_concurrent_tasks" "6"
assert_profile_value "max" "timeout_ms" "180000"

echo ""
echo -e "${BLUE}Test Group 3: API Profile (Enterprise)${NC}"
echo "----------------------------------------"

# Tests 7-9: API profile
assert_profile_exists "api"
assert_profile_value "api" "max_concurrent_tasks" "8"
assert_profile_value "api" "timeout_ms" "300000"

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
