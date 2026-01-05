#!/bin/bash

# STORY-172: Test Library - Shared utilities
# Provides common functions for STORY-172 tests

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test file location
PREFLIGHT_FILE="./.claude/skills/devforgeai-development/references/preflight-validation.md"

# Function to check file exists
check_file_exists() {
    if [ ! -f "$PREFLIGHT_FILE" ]; then
        echo -e "${RED}FAIL: preflight-validation.md not found${NC}"
        return 1
    fi
    return 0
}

# Function to report test result
report_result() {
    local test_name="$1"
    local result="$2"
    local message="$3"

    if [ "$result" -eq 0 ]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  $message"
    fi
    return $result
}

# Function to count pattern occurrences
count_pattern() {
    local pattern="$1"
    local file="$2"
    grep -c "$pattern" "$file" 2>/dev/null || echo "0"
}

# Export functions for use in test scripts
export -f check_file_exists
export -f report_result
export -f count_pattern
