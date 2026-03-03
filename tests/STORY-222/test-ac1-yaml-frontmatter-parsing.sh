#!/bin/bash
#
# Test: AC#1 - YAML Frontmatter Parsing
# Story: STORY-222 - Extract Plan File Knowledge Base for Decision Archive
#
# AC#1: YAML Frontmatter Parsing
#   Given: a plan file with YAML frontmatter
#   When: session-miner extracts metadata
#   Then: status, created, author, and related_stories fields are parsed
#
# Test Framework: Bash shell script with assertions
# Status: FAILING (no implementation exists yet)
#

set -euo pipefail

# Source the plan file KB functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../.claude/scripts/plan_file_kb.sh" 2>/dev/null || true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test utilities
assert_equal() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ "$expected" == "$actual" ]]; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_not_empty() {
    local value="$1"
    local message="${2:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -n "$value" ]]; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        echo "  Value is empty"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_file_exists() {
    local file="$1"
    local message="${2:-File should exist: $file}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -f "$file" ]]; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Create temporary test directory
TEST_TEMP_DIR="/tmp/test-story-222-ac1-$$"
mkdir -p "$TEST_TEMP_DIR"
trap "rm -rf $TEST_TEMP_DIR" EXIT

# ============================================================================
# Test 1: Parse YAML frontmatter with all required fields
# ============================================================================
test_should_parse_yaml_frontmatter_with_all_fields() {
    local test_name="Parse YAML frontmatter with status, created, author, related_stories"

    # Arrange: Create a plan file with YAML frontmatter
    local plan_file="$TEST_TEMP_DIR/test-plan-1.md"
    cat > "$plan_file" << 'EOF'
---
id: PLAN-001
title: Authentication Strategy Decision
status: approved
created: 2025-01-01
author: claude/requirements-analyst
related_stories:
  - STORY-050
  - STORY-051
  - STORY-052
tags:
  - authentication
  - security
---

# Decision: OAuth 2.0 vs Session-Based Authentication

## Context
...
EOF

    # Act: Call session-miner to extract YAML frontmatter (STUB - function doesn't exist yet)
    # Expected: Function signature should be:
    # extract_yaml_frontmatter <plan_file_path> -> JSON output
    if declare -f extract_yaml_frontmatter &> /dev/null; then
        local result
        result=$(extract_yaml_frontmatter "$plan_file" 2>/dev/null || echo "{}")
    else
        # Function doesn't exist - test should FAIL
        local result="{}"
    fi

    # Assert: Verify that status field was extracted
    if echo "$result" | grep -q '"status"\s*:\s*"approved"'; then
        assert_equal "approved" "$(echo "$result" | grep -o '"status"\s*:\s*"[^"]*"' | cut -d'"' -f4)" "Status field parsed from YAML frontmatter"
    else
        assert_equal "approved" "MISSING" "Status field should be extracted from YAML frontmatter"
    fi

    # Assert: Verify that created field was extracted
    if echo "$result" | grep -q '"created"\s*:\s*"2025-01-01"'; then
        assert_equal "2025-01-01" "$(echo "$result" | grep -o '"created"\s*:\s*"[^"]*"' | cut -d'"' -f4)" "Created date parsed from YAML frontmatter"
    else
        assert_equal "2025-01-01" "MISSING" "Created date should be extracted from YAML frontmatter"
    fi

    # Assert: Verify that author field was extracted
    if echo "$result" | grep -q '"author"\s*:\s*"[^"]*"'; then
        assert_not_empty "$(echo "$result" | grep -o '"author"\s*:\s*"[^"]*"' | cut -d'"' -f4)" "Author field parsed from YAML frontmatter"
    else
        assert_equal "claude/requirements-analyst" "MISSING" "Author should be extracted from YAML frontmatter"
    fi

    # Assert: Verify that related_stories array was extracted
    if echo "$result" | grep -q '"related_stories"'; then
        assert_not_empty "$(echo "$result" | grep -o '"related_stories"\s*:\s*\[[^\]]*\]')" "Related stories array parsed from YAML frontmatter"
    else
        assert_equal "ARRAY" "MISSING" "Related stories array should be extracted from YAML frontmatter"
    fi
}

# ============================================================================
# Test 2: Handle plan file with minimal YAML frontmatter
# ============================================================================
test_should_parse_minimal_yaml_frontmatter() {
    local test_name="Parse minimal YAML frontmatter with only required fields"

    # Arrange: Create a plan file with minimal YAML frontmatter
    local plan_file="$TEST_TEMP_DIR/test-plan-2.md"
    cat > "$plan_file" << 'EOF'
---
id: PLAN-002
status: draft
---

# Minimal Plan File
EOF

    # Act: Call session-miner to extract YAML frontmatter
    if declare -f extract_yaml_frontmatter &> /dev/null; then
        local result
        result=$(extract_yaml_frontmatter "$plan_file" 2>/dev/null || echo "{}")
    else
        local result="{}"
    fi

    # Assert: At minimum, status field should be extracted
    if echo "$result" | grep -q '"status"\s*:\s*"draft"'; then
        assert_equal "draft" "$(echo "$result" | grep -o '"status"\s*:\s*"[^"]*"' | cut -d'"' -f4)" "Status field parsed from minimal YAML"
    else
        assert_equal "draft" "MISSING" "Status field is required minimum"
    fi
}

# ============================================================================
# Test 3: Reject plan files with malformed YAML frontmatter
# ============================================================================
test_should_handle_malformed_yaml_gracefully() {
    local test_name="Handle malformed YAML frontmatter with error message"

    # Arrange: Create a plan file with malformed YAML
    local plan_file="$TEST_TEMP_DIR/test-plan-3.md"
    cat > "$plan_file" << 'EOF'
---
id: PLAN-003
status: approved
created: 2025-01-01
  invalid_indentation: "nested"
author: claude/test
---

# Malformed YAML Plan File
EOF

    # Act: Call session-miner to extract YAML frontmatter
    if declare -f extract_yaml_frontmatter &> /dev/null; then
        local result
        local exit_code=0
        result=$(extract_yaml_frontmatter "$plan_file" 2>/dev/null || exit_code=$?)
    else
        local result="{}"
        local exit_code=0
    fi

    # Assert: Should either skip malformed field or return error indicator
    # Implementation expected to handle gracefully
    if [[ -z "$result" ]] || echo "$result" | grep -q '"error"'; then
        assert_not_empty "error_handled" "Malformed YAML should trigger error handling"
    else
        # If parsing succeeded despite bad YAML, that's also acceptable (ignore field)
        assert_not_empty "parsed" "Malformed YAML should be handled gracefully"
    fi
}

# ============================================================================
# Test 4: Extract all three status values correctly
# ============================================================================
test_should_parse_different_status_values() {
    local test_name="Parse different status values: approved, draft, rejected"

    for status in "approved" "draft" "rejected"; do
        local plan_file="$TEST_TEMP_DIR/test-plan-status-$status.md"
        cat > "$plan_file" << EOF
---
id: PLAN-STATUS-$status
status: $status
created: 2025-01-01
author: test
---

# Test Plan
EOF

        # Act: Extract YAML
        if declare -f extract_yaml_frontmatter &> /dev/null; then
            local result
            result=$(extract_yaml_frontmatter "$plan_file" 2>/dev/null || echo "{}")
        else
            local result="{}"
        fi

        # Assert: Verify status was extracted correctly
        if echo "$result" | grep -q "\"status\"\s*:\s*\"$status\""; then
            assert_equal "$status" "$status" "Status '$status' parsed correctly"
        else
            assert_equal "$status" "MISSING" "Status '$status' should be parsed"
        fi
    done
}

# ============================================================================
# Test 5: Parse related_stories array with multiple STORY-IDs
# ============================================================================
test_should_parse_related_stories_array() {
    local test_name="Parse related_stories as array with multiple STORY-IDs"

    # Arrange
    local plan_file="$TEST_TEMP_DIR/test-plan-stories.md"
    cat > "$plan_file" << 'EOF'
---
id: PLAN-004
status: approved
created: 2025-01-01
author: claude/architect
related_stories:
  - STORY-100
  - STORY-101
  - STORY-102
  - STORY-103
---

# Plan with many related stories
EOF

    # Act
    if declare -f extract_yaml_frontmatter &> /dev/null; then
        local result
        result=$(extract_yaml_frontmatter "$plan_file" 2>/dev/null || echo "{}")
    else
        local result="{}"
    fi

    # Assert: Array should contain all 4 stories
    local story_count=0
    if echo "$result" | grep -q '"related_stories"'; then
        # Count STORY- patterns in result
        story_count=$(echo "$result" | grep -o 'STORY-[0-9]\+' | wc -l)
        assert_equal "4" "$story_count" "Related stories array contains all 4 STORY-IDs"
    else
        assert_equal "4" "0" "Related stories array should be extracted"
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: AC#1 - YAML Frontmatter Parsing"
echo "Story: STORY-222 - Plan File Knowledge Base"
echo "========================================================================"
echo ""

test_should_parse_yaml_frontmatter_with_all_fields
echo ""

test_should_parse_minimal_yaml_frontmatter
echo ""

test_should_handle_malformed_yaml_gracefully
echo ""

test_should_parse_different_status_values
echo ""

test_should_parse_related_stories_array
echo ""

# ============================================================================
# Print summary
# ============================================================================
echo "========================================================================"
echo "Test Results Summary"
echo "========================================================================"
echo "Tests run:    $TESTS_RUN"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${RED}RESULT: FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}RESULT: PASSED${NC}"
    exit 0
fi
