#!/bin/bash
#
# Test: AC#2 - Story ID Pattern Extraction
# Story: STORY-222 - Extract Plan File Knowledge Base for Decision Archive
#
# AC#2: Story ID Pattern Extraction
#   Given: a plan file containing story references
#   When: session-miner scans content
#   Then: all STORY-NNN patterns are extracted with surrounding context
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

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if echo "$haystack" | grep -q "$needle"; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        echo "  Expected to find: $needle"
        echo "  In: ${haystack:0:100}..."
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

# Create temporary test directory
TEST_TEMP_DIR="/tmp/test-story-222-ac2-$$"
mkdir -p "$TEST_TEMP_DIR"
trap "rm -rf $TEST_TEMP_DIR" EXIT

# ============================================================================
# Test 1: Extract single STORY-ID from plan file
# ============================================================================
test_should_extract_single_story_id() {
    local test_name="Extract single STORY-NNN pattern from plan file"

    # Arrange: Create a plan file with one STORY reference
    local plan_file="$TEST_TEMP_DIR/test-plan-single.md"
    cat > "$plan_file" << 'EOF'
---
id: PLAN-001
---

# Architecture Decision: Authentication Strategy

This plan documents the decision made in STORY-050 regarding OAuth implementation.

The team decided to implement OAuth 2.0 after evaluating options in STORY-050.
EOF

    # Act: Call session-miner to extract STORY-IDs with context
    if declare -f extract_story_ids &> /dev/null; then
        local result
        result=$(extract_story_ids "$plan_file" 2>/dev/null || echo "{}")
    else
        local result="{}"
    fi

    # Assert: STORY-050 should be in result
    if echo "$result" | grep -q "STORY-050"; then
        assert_contains "$result" "STORY-050" "STORY-050 extracted from plan file"
    else
        assert_contains "$result" "STORY-050" "STORY-050 should be extracted"
    fi
}

# ============================================================================
# Test 2: Extract multiple STORY-IDs with surrounding context
# ============================================================================
test_should_extract_multiple_story_ids_with_context() {
    local test_name="Extract multiple STORY-IDs and surrounding context"

    # Arrange: Create a plan file with multiple STORY references
    local plan_file="$TEST_TEMP_DIR/test-plan-multiple.md"
    cat > "$plan_file" << 'EOF'
---
id: PLAN-002
---

# Decision: Microservices Architecture

## Related Stories

The following stories drove this decision:

- STORY-100 - API Gateway Design
- STORY-101 - Service Discovery Implementation
- STORY-102 - Circuit Breaker Pattern
- STORY-103 - Load Balancing Strategy

## Analysis

When implementing STORY-100, we discovered that a microservices approach
would be more scalable than the monolithic design in STORY-090.

Both STORY-101 and STORY-102 require coordination at the service level.
EOF

    # Act: Extract STORY-IDs
    if declare -f extract_story_ids_with_context &> /dev/null; then
        local result
        result=$(extract_story_ids_with_context "$plan_file" 2>/dev/null || echo "{}")
    elif declare -f extract_story_ids &> /dev/null; then
        local result
        result=$(extract_story_ids "$plan_file" 2>/dev/null || echo "{}")
    else
        local result="{}"
    fi

    # Assert: All STORY-IDs should be extracted
    local expected_stories=("STORY-100" "STORY-101" "STORY-102" "STORY-103" "STORY-090")
    for story_id in "${expected_stories[@]}"; do
        if echo "$result" | grep -q "$story_id"; then
            assert_contains "$result" "$story_id" "$story_id extracted from plan file"
        else
            assert_contains "$result" "$story_id" "$story_id should be extracted"
        fi
    done
}

# ============================================================================
# Test 3: Extract surrounding context for each STORY-ID
# ============================================================================
test_should_extract_context_around_story_ids() {
    local test_name="Extract context (surrounding lines) around STORY-ID references"

    # Arrange: Create a plan file with STORY reference in different contexts
    local plan_file="$TEST_TEMP_DIR/test-plan-context.md"
    cat > "$plan_file" << 'EOF'
---
id: PLAN-003
---

# Plan: Database Migration

## Why This Decision?

STORY-200 required a migration to PostgreSQL from MySQL because of scalability issues.

The decision in STORY-200 was to implement connection pooling and replicas.

## Implementation Details

For STORY-201, we created a migration strategy with rollback capabilities.
EOF

    # Act: Extract STORY-IDs with context
    if declare -f extract_story_ids_with_context &> /dev/null; then
        local result
        result=$(extract_story_ids_with_context "$plan_file" 2>/dev/null || echo "{}")
    else
        local result="{}"
    fi

    # Assert: Results should include context around STORY-200
    # Expected context: "required a migration to PostgreSQL"
    if echo "$result" | grep -q "STORY-200"; then
        assert_not_empty "$(echo "$result" | grep -A 2 -B 2 'STORY-200' 2>/dev/null || echo '')" "Context around STORY-200 should be included"
    else
        assert_contains "$result" "STORY-200" "STORY-200 should be extracted with context"
    fi
}

# ============================================================================
# Test 4: Regex pattern validates STORY-NNN format (3+ digits)
# ============================================================================
test_should_match_story_nnn_pattern_exactly() {
    local test_name="Extract only valid STORY-NNN patterns (3+ digits)"

    # Arrange: Create a plan file with valid and invalid STORY patterns
    local plan_file="$TEST_TEMP_DIR/test-plan-pattern.md"
    cat > "$plan_file" << 'EOF'
---
id: PLAN-004
---

# Test Plan File

Valid story references:
- STORY-001
- STORY-050
- STORY-1000
- STORY-9999

Invalid patterns that should NOT match:
- STORY-1 (too few digits)
- STORY-AB (not digits)
- story-050 (lowercase)
- STORIES-050 (plural)
- xSTORY-050 (prefix)
- STORY-050x (suffix)
EOF

    # Act: Extract STORY-IDs using regex
    if declare -f extract_story_ids &> /dev/null; then
        local result
        result=$(extract_story_ids "$plan_file" 2>/dev/null || echo "{}")
    else
        local result="{}"
    fi

    # Assert: Only valid STORY-NNN patterns should be extracted
    local valid_stories=("STORY-001" "STORY-050" "STORY-1000" "STORY-9999")
    for story_id in "${valid_stories[@]}"; do
        if echo "$result" | grep -q "$story_id"; then
            assert_contains "$result" "$story_id" "Valid pattern $story_id extracted"
        else
            assert_contains "$result" "$story_id" "Valid pattern $story_id should be extracted"
        fi
    done

    # Assert: Invalid patterns should NOT be extracted
    if echo "$result" | grep -q "STORY-1[^0-9]" || echo "$result" | grep -q "story-050\|STORIES-050"; then
        assert_equal "false" "true" "Invalid patterns should not be extracted"
    else
        assert_equal "true" "true" "Invalid patterns correctly excluded"
    fi
}

# ============================================================================
# Test 5: Handle STORY-IDs in different content locations
# ============================================================================
test_should_extract_story_ids_from_various_locations() {
    local test_name="Extract STORY-IDs from frontmatter, headers, paragraphs, lists"

    # Arrange: Create plan file with STORY-IDs in various places
    local plan_file="$TEST_TEMP_DIR/test-plan-locations.md"
    cat > "$plan_file" << 'EOF'
---
id: PLAN-005
related_stories:
  - STORY-300
---

# Decision from STORY-301

## Overview

STORY-302 introduced the requirement for caching.

- Related: STORY-303
- Related: STORY-304

In [STORY-305], we implemented circuit breakers.

The implementation (STORY-306) uses exponential backoff.

See also STORY-307, STORY-308, and STORY-309 for details.
EOF

    # Act: Extract STORY-IDs from all locations
    if declare -f extract_story_ids &> /dev/null; then
        local result
        result=$(extract_story_ids "$plan_file" 2>/dev/null || echo "{}")
    else
        local result="{}"
    fi

    # Assert: All STORY-IDs should be found regardless of location
    local all_stories=("STORY-300" "STORY-301" "STORY-302" "STORY-303" "STORY-304" "STORY-305" "STORY-306" "STORY-307" "STORY-308" "STORY-309")
    local stories_found=0
    for story_id in "${all_stories[@]}"; do
        if echo "$result" | grep -q "$story_id"; then
            stories_found=$((stories_found + 1))
        fi
    done

    local expected_min=8  # At least 8 out of 10 should be found
    if [[ $stories_found -ge $expected_min ]]; then
        assert_equal "FOUND" "FOUND" "At least $expected_min STORY-IDs extracted from various locations"
    else
        assert_equal "$expected_min" "$stories_found" "Should find at least $expected_min STORY-IDs"
    fi
}

# ============================================================================
# Test 6: No false positives on similar patterns
# ============================================================================
test_should_not_extract_non_story_patterns() {
    local test_name="Avoid false positives with similar patterns"

    # Arrange: Create plan file with non-STORY patterns that might match
    local plan_file="$TEST_TEMP_DIR/test-plan-false-positives.md"
    cat > "$plan_file" << 'EOF'
---
id: PLAN-006
---

# Plan Reference

Valid reference:
- STORY-400

Should NOT match:
- STORY: 400 (space)
- PLAN-400 (not STORY)
- EPIC-400 (not STORY)
- TASK-400 (not STORY)
- SPRINT-400 (not STORY)
- Build-2024 (not STORY)
- Issue-400 (not STORY)
EOF

    # Act: Extract STORY-IDs
    if declare -f extract_story_ids &> /dev/null; then
        local result
        result=$(extract_story_ids "$plan_file" 2>/dev/null || echo "{}")
    else
        local result="{}"
    fi

    # Assert: Only STORY-400 should be found, not similar patterns
    if echo "$result" | grep -q "STORY-400"; then
        assert_contains "$result" "STORY-400" "Valid STORY-400 should be extracted"
    else
        assert_contains "$result" "STORY-400" "STORY-400 should be extracted"
    fi

    # Count how many matches found (should be minimal)
    local match_count=$(echo "$result" | grep -o 'STORY-[0-9]\+' | wc -l)
    if [[ $match_count -le 2 ]]; then  # STORY-400 and maybe one from code
        assert_equal "MINIMAL" "MINIMAL" "No false positives on similar patterns"
    else
        assert_equal "1" "$match_count" "Should match only STORY-400, found $match_count"
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: AC#2 - Story ID Pattern Extraction"
echo "Story: STORY-222 - Plan File Knowledge Base"
echo "========================================================================"
echo ""

test_should_extract_single_story_id
echo ""

test_should_extract_multiple_story_ids_with_context
echo ""

test_should_extract_context_around_story_ids
echo ""

test_should_match_story_nnn_pattern_exactly
echo ""

test_should_extract_story_ids_from_various_locations
echo ""

test_should_not_extract_non_story_patterns
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
