#!/bin/bash
# STORY-232: Test AC#1 - Frontmatter Indexing
# Test that build_searchable_index() indexes story ID, status, created date from frontmatter
#
# TDD RED PHASE: These tests should FAIL because the functions don't exist yet
#
# Expected Functions (to be implemented in plan_file_kb.sh):
#   - build_searchable_index(plans_dir, index_dir) - Build searchable index with frontmatter
#
# Tech Stack: Bash scripting (Claude Code native) - per tech-stack.md lines 48-63

# =============================================================================
# Test Configuration
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PLAN_FILE_KB="$PROJECT_ROOT/.claude/scripts/plan_file_kb.sh"
TEST_FIXTURES_DIR="$SCRIPT_DIR/fixtures"

# Source the plan file KB (silently, allowing for missing functions)
if [[ -f "$PLAN_FILE_KB" ]]; then
    source "$PLAN_FILE_KB" 2>/dev/null || true
fi

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# =============================================================================
# Test Helpers
# =============================================================================

pass_test() {
    local test_name="$1"
    echo "[PASS] $test_name"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
}

fail_test() {
    local test_name="$1"
    local reason="$2"
    echo "[FAIL] $test_name"
    echo "       $reason"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
}

# =============================================================================
# Setup Test Fixtures
# =============================================================================
setup_fixtures() {
    mkdir -p "$TEST_FIXTURES_DIR/plans"

    # Fixture 1: Plan file with complete frontmatter
    cat > "$TEST_FIXTURES_DIR/plans/STORY-100-complete.md" << 'PLANEOF'
---
status: completed
created: 2025-01-01
author: claude/opus
related_stories: ["STORY-100", "STORY-101"]
---

# Plan: Complete Frontmatter Test

## Decision

This is a decision section.

## Technical Approach

This is a technical approach section.
PLANEOF

    # Fixture 2: Plan file with partial frontmatter (missing created)
    cat > "$TEST_FIXTURES_DIR/plans/STORY-200-partial.md" << 'PLANEOF'
---
status: in_progress
author: claude/dev
---

# Plan: Partial Frontmatter

## Implementation

Some implementation notes.
PLANEOF

    # Fixture 3: Plan file without frontmatter
    cat > "$TEST_FIXTURES_DIR/plans/no-frontmatter.md" << 'PLANEOF'
# Plan Without Frontmatter

This plan has no YAML frontmatter.

## Decision

Make it work.
PLANEOF

    # Fixture 4: Plan file with story ID in filename but different status
    cat > "$TEST_FIXTURES_DIR/plans/STORY-300-abandoned.md" << 'PLANEOF'
---
status: abandoned
created: 2024-12-15
author: claude/qa
---

# Abandoned Plan

This plan was abandoned.
PLANEOF
}

cleanup_fixtures() {
    rm -rf "$TEST_FIXTURES_DIR"
}

# =============================================================================
# Test Cases for AC#1: Frontmatter Indexing
# =============================================================================

test_build_searchable_index_function_exists() {
    echo ""
    echo "=== Test: build_searchable_index function exists ==="

    if type build_searchable_index &>/dev/null; then
        pass_test "Function build_searchable_index should exist in plan_file_kb.sh"
    else
        fail_test "Function build_searchable_index should exist in plan_file_kb.sh" \
            "Function 'build_searchable_index' does not exist"
    fi
}

test_build_searchable_index_indexes_story_id() {
    echo ""
    echo "=== Test: build_searchable_index indexes story ID from filename ==="

    local index_dir="$TEST_FIXTURES_DIR/index"
    mkdir -p "$index_dir"

    # Call function (should fail until implemented)
    if type build_searchable_index &>/dev/null; then
        local result
        result=$(build_searchable_index "$TEST_FIXTURES_DIR/plans" "$index_dir" 2>&1) || true

        # Index file should exist
        if [[ -f "$index_dir/searchable_index.json" ]]; then
            local index_content
            index_content=$(cat "$index_dir/searchable_index.json")

            if echo "$index_content" | grep -q "STORY-100"; then
                pass_test "Index should contain STORY-100"
            else
                fail_test "Index should contain STORY-100" "STORY-100 not found in index"
            fi

            if echo "$index_content" | grep -q "STORY-200"; then
                pass_test "Index should contain STORY-200"
            else
                fail_test "Index should contain STORY-200" "STORY-200 not found in index"
            fi

            if echo "$index_content" | grep -q "STORY-300"; then
                pass_test "Index should contain STORY-300"
            else
                fail_test "Index should contain STORY-300" "STORY-300 not found in index"
            fi
        else
            fail_test "Index file should be created" "Index file not created at $index_dir/searchable_index.json"
        fi
    else
        fail_test "Index should contain STORY-100" "Function build_searchable_index does not exist"
        fail_test "Index should contain STORY-200" "Function build_searchable_index does not exist"
        fail_test "Index should contain STORY-300" "Function build_searchable_index does not exist"
    fi
}

test_build_searchable_index_indexes_status() {
    echo ""
    echo "=== Test: build_searchable_index indexes status from frontmatter ==="

    local index_dir="$TEST_FIXTURES_DIR/index"
    mkdir -p "$index_dir"

    if type build_searchable_index &>/dev/null; then
        local result
        result=$(build_searchable_index "$TEST_FIXTURES_DIR/plans" "$index_dir" 2>&1) || true

        if [[ -f "$index_dir/searchable_index.json" ]]; then
            local index_content
            index_content=$(cat "$index_dir/searchable_index.json")

            if echo "$index_content" | grep -q "completed"; then
                pass_test "Index should contain status 'completed'"
            else
                fail_test "Index should contain status 'completed'" "Status 'completed' not found"
            fi

            if echo "$index_content" | grep -q "in_progress"; then
                pass_test "Index should contain status 'in_progress'"
            else
                fail_test "Index should contain status 'in_progress'" "Status 'in_progress' not found"
            fi

            if echo "$index_content" | grep -q "abandoned"; then
                pass_test "Index should contain status 'abandoned'"
            else
                fail_test "Index should contain status 'abandoned'" "Status 'abandoned' not found"
            fi
        else
            fail_test "Index should contain status 'completed'" "Index file not created"
            fail_test "Index should contain status 'in_progress'" "Index file not created"
            fail_test "Index should contain status 'abandoned'" "Index file not created"
        fi
    else
        fail_test "Index should contain status 'completed'" "Function build_searchable_index does not exist"
        fail_test "Index should contain status 'in_progress'" "Function build_searchable_index does not exist"
        fail_test "Index should contain status 'abandoned'" "Function build_searchable_index does not exist"
    fi
}

test_build_searchable_index_indexes_created_date() {
    echo ""
    echo "=== Test: build_searchable_index indexes created date from frontmatter ==="

    local index_dir="$TEST_FIXTURES_DIR/index"
    mkdir -p "$index_dir"

    if type build_searchable_index &>/dev/null; then
        local result
        result=$(build_searchable_index "$TEST_FIXTURES_DIR/plans" "$index_dir" 2>&1) || true

        if [[ -f "$index_dir/searchable_index.json" ]]; then
            local index_content
            index_content=$(cat "$index_dir/searchable_index.json")

            if echo "$index_content" | grep -q "2025-01-01"; then
                pass_test "Index should contain created date '2025-01-01'"
            else
                fail_test "Index should contain created date '2025-01-01'" "Date not found"
            fi

            if echo "$index_content" | grep -q "2024-12-15"; then
                pass_test "Index should contain created date '2024-12-15'"
            else
                fail_test "Index should contain created date '2024-12-15'" "Date not found"
            fi
        else
            fail_test "Index should contain created date '2025-01-01'" "Index file not created"
            fail_test "Index should contain created date '2024-12-15'" "Index file not created"
        fi
    else
        fail_test "Index should contain created date '2025-01-01'" "Function build_searchable_index does not exist"
        fail_test "Index should contain created date '2024-12-15'" "Function build_searchable_index does not exist"
    fi
}

test_build_searchable_index_returns_success_status() {
    echo ""
    echo "=== Test: build_searchable_index returns success status JSON ==="

    local index_dir="$TEST_FIXTURES_DIR/index"
    mkdir -p "$index_dir"

    if type build_searchable_index &>/dev/null; then
        local result
        result=$(build_searchable_index "$TEST_FIXTURES_DIR/plans" "$index_dir" 2>&1) || true

        if echo "$result" | grep -q "success"; then
            pass_test "Result should contain 'success' status"
        else
            fail_test "Result should contain 'success' status" "No 'success' in result"
        fi

        if echo "$result" | grep -q "plan_count"; then
            pass_test "Result should contain 'plan_count'"
        else
            fail_test "Result should contain 'plan_count'" "No 'plan_count' in result"
        fi
    else
        fail_test "Result should contain 'success' status" "Function build_searchable_index does not exist"
        fail_test "Result should contain 'plan_count'" "Function build_searchable_index does not exist"
    fi
}

# =============================================================================
# Main Test Runner
# =============================================================================
main() {
    echo "=============================================="
    echo "STORY-232 AC#1: Frontmatter Indexing Tests"
    echo "TDD RED PHASE - Tests expected to FAIL"
    echo "=============================================="
    echo ""

    # Setup
    setup_fixtures

    # Run tests
    test_build_searchable_index_function_exists
    test_build_searchable_index_indexes_story_id
    test_build_searchable_index_indexes_status
    test_build_searchable_index_indexes_created_date
    test_build_searchable_index_returns_success_status

    # Cleanup
    cleanup_fixtures

    # Summary
    echo ""
    echo "=============================================="
    echo "Test Summary: $TESTS_PASSED/$TESTS_TOTAL passed"
    echo "=============================================="

    if [[ $TESTS_FAILED -gt 0 ]]; then
        echo "STATUS: RED (TDD Red Phase - Expected)"
        exit 1
    else
        echo "STATUS: GREEN"
        exit 0
    fi
}

main "$@"
