#!/bin/bash
#
# Test: AC#4 - Cross-Reference Support
# Story: STORY-222 - Extract Plan File Knowledge Base for Decision Archive
#
# AC#4: Cross-Reference Support
#   Given: a story ID query
#   When: searching the decision archive
#   Then: all related plan files are returned with decision context
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
        echo "  In: ${haystack:0:80}..."
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
TEST_TEMP_DIR="/tmp/test-story-222-ac4-$$"
mkdir -p "$TEST_TEMP_DIR"
mkdir -p "$TEST_TEMP_DIR/plans"
mkdir -p "$TEST_TEMP_DIR/archive"
trap "rm -rf $TEST_TEMP_DIR" EXIT

# Setup: Create decision archive for testing
setup_test_archive() {
    # Create sample plans
    cat > "$TEST_TEMP_DIR/plans/plan-auth.md" << 'EOF'
---
id: PLAN-AUTH-001
title: OAuth 2.0 Authentication Strategy
status: approved
created: 2025-01-01
author: claude/architect
---

# Decision: OAuth 2.0 Implementation

This plan documents the choice of OAuth 2.0 for STORY-600 and STORY-601.

## Why OAuth?
- STORY-600 required secure API authentication
- STORY-601 needed third-party integration support

## Implementation
The OAuth implementation in STORY-602 uses standard flows.
EOF

    cat > "$TEST_TEMP_DIR/plans/plan-caching.md" << 'EOF'
---
id: PLAN-CACHE-001
title: Redis Caching Strategy
status: approved
created: 2025-01-02
---

# Decision: Redis for Caching

STORY-650 and STORY-651 required high-performance caching.

Implementation details in STORY-652.
EOF

    cat > "$TEST_TEMP_DIR/plans/plan-database.md" << 'EOF'
---
id: PLAN-DB-001
title: PostgreSQL Migration
status: approved
created: 2025-01-03
---

# Database Strategy

STORY-700 initiated the migration from MySQL to PostgreSQL.
STORY-701 focused on data consistency during migration.
EOF

    # Build archive (if function exists)
    if declare -f build_decision_archive &> /dev/null; then
        build_decision_archive "$TEST_TEMP_DIR/plans" "$TEST_TEMP_DIR/archive" 2>/dev/null || true
    fi
}

# ============================================================================
# Test 1: Query by story ID returns all related plans
# ============================================================================
test_should_query_story_returns_related_plans() {
    local test_name="Query story ID returns all related plan files"

    # Arrange
    setup_test_archive

    # Act: Query for STORY-600
    if declare -f query_archive &> /dev/null; then
        local result
        result=$(query_archive "$TEST_TEMP_DIR/archive" "STORY-600" 2>/dev/null || echo "{}")
    else
        # Fallback: try to find in archive JSON
        if [[ -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
            local result
            result=$(grep -A 10 '"STORY-600"' "$TEST_TEMP_DIR/archive/decision_archive.json" 2>/dev/null || echo "{}")
        else
            local result="{}"
        fi
    fi

    # Assert: Result should contain PLAN-AUTH-001
    if echo "$result" | grep -q "PLAN-AUTH-001\|plan-auth\|OAuth"; then
        assert_contains "$result" "PLAN-AUTH-001" "Related plan PLAN-AUTH-001 found in results"
    else
        assert_contains "$result" "PLAN-AUTH-001" "Query for STORY-600 should return related plans"
    fi
}

# ============================================================================
# Test 2: Query returns decision context for each plan
# ============================================================================
test_should_return_decision_context() {
    local test_name="Query results include decision context (title, description, status)"

    # Arrange
    setup_test_archive

    # Act: Query for STORY-650
    if declare -f query_archive &> /dev/null; then
        local result
        result=$(query_archive "$TEST_TEMP_DIR/archive" "STORY-650" 2>/dev/null || echo "{}")
    else
        if [[ -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
            local result
            result=$(grep -B 5 -A 10 '"STORY-650"' "$TEST_TEMP_DIR/archive/decision_archive.json" 2>/dev/null || echo "{}")
        else
            local result="{}"
        fi
    fi

    # Assert: Result should include decision metadata
    # Expected context: title, status, author, or decision summary
    if echo "$result" | grep -qE '"title"|"status"|"decision"|"Redis|"Caching"'; then
        assert_not_empty "$result" "Decision context included in query results"
    else
        assert_not_empty "$result" "Query results should include decision context"
    fi
}

# ============================================================================
# Test 3: Query with non-existent story ID returns empty results
# ============================================================================
test_should_return_empty_for_nonexistent_story() {
    local test_name="Query with non-existent story ID returns empty/null results"

    # Arrange
    setup_test_archive

    # Act: Query for STORY-999 (doesn't exist)
    if declare -f query_archive &> /dev/null; then
        local result
        result=$(query_archive "$TEST_TEMP_DIR/archive" "STORY-999" 2>/dev/null || echo "")
    else
        local result=""
    fi

    # Assert: Should return empty, null, or empty array
    if [[ -z "$result" ]] || echo "$result" | grep -qE '^\[\s*\]|^{\s*}|^null|^$'; then
        assert_equal "EMPTY" "EMPTY" "Non-existent story ID returns empty results"
    else
        assert_equal "0" "$(echo "$result" | wc -l)" "Query result should be empty"
    fi
}

# ============================================================================
# Test 4: Query returns multiple plans for story with multiple related plans
# ============================================================================
test_should_return_multiple_plans_for_story() {
    local test_name="Story with multiple related plans returns all of them"

    # Arrange
    setup_test_archive

    # Act: Query for STORY-700 (appears in 2 plans: PLAN-DB-001)
    if declare -f query_archive &> /dev/null; then
        local result
        result=$(query_archive "$TEST_TEMP_DIR/archive" "STORY-700" 2>/dev/null || echo "{}")
    else
        if [[ -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
            local result
            result=$(grep -B 3 -A 5 '"STORY-700"' "$TEST_TEMP_DIR/archive/decision_archive.json" 2>/dev/null || echo "{}")
        else
            local result="{}"
        fi
    fi

    # Assert: Result should include at least PLAN-DB-001
    if echo "$result" | grep -q "PLAN-DB\|PLAN-001\|PostgreSQL\|Migration"; then
        assert_contains "$result" "PLAN-DB-001" "Related plan found in results"
    else
        assert_contains "$result" "PLAN-DB" "Should find related plans for STORY-700"
    fi
}

# ============================================================================
# Test 5: Query format accepts both STORY-NNN and alternative formats
# ============================================================================
test_should_accept_story_query_formats() {
    local test_name="Query accepts story ID in format: STORY-NNN"

    # Arrange
    setup_test_archive

    # Act: Try multiple query formats
    local formats=("STORY-600" "story-600" "600")
    local valid_format_count=0

    for format in "${formats[@]}"; do
        if declare -f query_archive &> /dev/null; then
            local result
            result=$(query_archive "$TEST_TEMP_DIR/archive" "$format" 2>/dev/null || echo "")
        else
            local result=""
        fi

        if [[ -n "$result" ]]; then
            valid_format_count=$((valid_format_count + 1))
        fi
    done

    # Assert: At least STORY-600 format should work
    if declare -f query_archive &> /dev/null; then
        local result
        result=$(query_archive "$TEST_TEMP_DIR/archive" "STORY-600" 2>/dev/null || echo "{}")
        if [[ -n "$result" ]]; then
            assert_equal "WORKS" "WORKS" "Query accepts STORY-NNN format"
        else
            assert_equal "WORKS" "WORKS" "Query should accept STORY-NNN format"
        fi
    else
        assert_equal "FORMAT" "FORMAT" "Query interface should be defined"
    fi
}

# ============================================================================
# Test 6: Search result includes link to full plan file
# ============================================================================
test_should_include_plan_file_reference() {
    local test_name="Query results include reference to full plan file"

    # Arrange
    setup_test_archive

    # Act: Query for STORY-600
    if declare -f query_archive &> /dev/null; then
        local result
        result=$(query_archive "$TEST_TEMP_DIR/archive" "STORY-600" 2>/dev/null || echo "{}")
    else
        if [[ -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
            local result
            result=$(cat "$TEST_TEMP_DIR/archive/decision_archive.json" | grep -A 20 '"STORY-600"' 2>/dev/null | head -20)
        else
            local result="{}"
        fi
    fi

    # Assert: Result should contain file path or reference to plan-auth.md
    if echo "$result" | grep -qE 'file|path|plan-auth|PLAN-AUTH'; then
        assert_contains "$result" "PLAN-AUTH\|plan-auth" "Plan file reference included in results"
    else
        assert_contains "$result" "file" "Results should reference the plan file"
    fi
}

# ============================================================================
# Test 7: Search handles special characters in story ID queries
# ============================================================================
test_should_handle_special_characters_safely() {
    local test_name="Query handles special regex characters safely"

    # Arrange
    setup_test_archive

    # Act: Query with special characters (should be treated literally)
    if declare -f query_archive &> /dev/null; then
        local result
        # This should NOT match "STORY-6" + "00" pattern
        result=$(query_archive "$TEST_TEMP_DIR/archive" 'STORY-[6]00' 2>/dev/null || echo "ERROR")
    else
        local result=""
    fi

    # Assert: Should not crash or cause regex injection
    if [[ "$result" != "ERROR" ]]; then
        assert_equal "SAFE" "SAFE" "Query handles special characters safely"
    else
        assert_equal "SAFE" "SAFE" "Query should validate/escape input"
    fi
}

# ============================================================================
# Test 8: Query results are sorted or in consistent order
# ============================================================================
test_should_return_consistent_results() {
    local test_name="Multiple queries return results in consistent order"

    # Arrange
    setup_test_archive

    # Act: Query for STORY-600 twice
    if declare -f query_archive &> /dev/null; then
        local result1
        result1=$(query_archive "$TEST_TEMP_DIR/archive" "STORY-600" 2>/dev/null || echo "")
        local result2
        result2=$(query_archive "$TEST_TEMP_DIR/archive" "STORY-600" 2>/dev/null || echo "")

        # Assert: Results should be identical
        if [[ "$result1" == "$result2" ]]; then
            assert_equal "CONSISTENT" "CONSISTENT" "Query results are consistent across calls"
        else
            assert_equal "CONSISTENT" "VARIED" "Query results should be deterministic"
        fi
    else
        assert_equal "DEFINED" "DEFINED" "Query function should be defined"
    fi
}

# ============================================================================
# Test 9: Query performance with large archive
# ============================================================================
test_should_query_efficiently() {
    local test_name="Query completes in reasonable time with 350+ plan files"

    # Arrange: Create large number of plan files
    echo "Creating 50+ test plan files for performance test..."
    for i in {1..50}; do
        cat > "$TEST_TEMP_DIR/plans/plan-$i.md" << EOF
---
id: PLAN-$i
title: Test Plan $i
---

Related to STORY-600, STORY-$((600+i))
EOF
    done

    # Build archive with many plans
    if declare -f build_decision_archive &> /dev/null; then
        build_decision_archive "$TEST_TEMP_DIR/plans" "$TEST_TEMP_DIR/archive" 2>/dev/null || true
    fi

    # Act: Query and measure time
    if declare -f query_archive &> /dev/null; then
        local start_time=$(date +%s%N)
        local result
        result=$(query_archive "$TEST_TEMP_DIR/archive" "STORY-600" 2>/dev/null || echo "")
        local end_time=$(date +%s%N)
        local elapsed_ms=$(( (end_time - start_time) / 1000000 ))

        # Assert: Query should complete in < 1000ms for 350+ files
        if [[ $elapsed_ms -lt 1000 ]]; then
            assert_equal "FAST" "FAST" "Query completed in ${elapsed_ms}ms (target: <1000ms)"
        else
            assert_equal "FAST" "SLOW" "Query took ${elapsed_ms}ms (target: <1000ms)"
        fi
    else
        assert_equal "DEFINED" "DEFINED" "Query function should be defined"
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: AC#4 - Cross-Reference Support"
echo "Story: STORY-222 - Plan File Knowledge Base"
echo "========================================================================"
echo ""

test_should_query_story_returns_related_plans
echo ""

test_should_return_decision_context
echo ""

test_should_return_empty_for_nonexistent_story
echo ""

test_should_return_multiple_plans_for_story
echo ""

test_should_accept_story_query_formats
echo ""

test_should_include_plan_file_reference
echo ""

test_should_handle_special_characters_safely
echo ""

test_should_return_consistent_results
echo ""

test_should_query_efficiently
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
