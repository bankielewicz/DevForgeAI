#!/bin/bash
# STORY-232: Test AC#2 - Decision Section Extraction
# Test that extract_decision_sections() captures ## Decision, ## Technical Approach sections
#
# TDD RED PHASE: These tests should FAIL because the functions don't exist yet
#
# Expected Functions (to be implemented in plan_file_kb.sh):
#   - extract_decision_sections(plan_file) - Extract ## Decision, ## Technical Approach sections
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

    # Fixture 1: Plan file with both Decision and Technical Approach sections
    cat > "$TEST_FIXTURES_DIR/plans/both-sections.md" << 'PLANEOF'
---
status: completed
created: 2025-01-01
---

# Plan: Both Sections Test

## Context

Some context information.

## Decision

We decided to use Bash for implementation because:
1. It is Claude Code native
2. No external dependencies
3. Works with Grep patterns

## Technical Approach

The implementation will follow these steps:
1. Parse frontmatter using awk
2. Build JSON index
3. Support full-text search

## Implementation Notes

Additional notes here.
PLANEOF

    # Fixture 2: Plan file with only Decision section
    cat > "$TEST_FIXTURES_DIR/plans/decision-only.md" << 'PLANEOF'
---
status: in_progress
---

# Plan: Decision Only

## Decision

This plan only has a Decision section.
We will implement feature X using approach Y.

## Notes

Some notes that are not technical approach.
PLANEOF

    # Fixture 3: Plan file with only Technical Approach section
    cat > "$TEST_FIXTURES_DIR/plans/technical-only.md" << 'PLANEOF'
---
status: draft
---

# Plan: Technical Approach Only

## Technical Approach

This plan only has a Technical Approach section.
Steps:
- Step 1: Do this
- Step 2: Then that
- Step 3: Finally this

## References

Some references.
PLANEOF

    # Fixture 4: Plan file with neither section
    cat > "$TEST_FIXTURES_DIR/plans/no-decision-sections.md" << 'PLANEOF'
---
status: backlog
---

# Plan: No Decision Sections

## Overview

This plan has no decision or technical approach sections.

## Implementation

Some implementation notes.

## Testing

Testing strategy.
PLANEOF
}

cleanup_fixtures() {
    rm -rf "$TEST_FIXTURES_DIR"
}

# =============================================================================
# Test Cases for AC#2: Decision Section Extraction
# =============================================================================

test_extract_decision_sections_function_exists() {
    echo ""
    echo "=== Test: extract_decision_sections function exists ==="

    if type extract_decision_sections &>/dev/null; then
        pass_test "Function extract_decision_sections should exist in plan_file_kb.sh"
    else
        fail_test "Function extract_decision_sections should exist in plan_file_kb.sh" \
            "Function 'extract_decision_sections' does not exist"
    fi
}

test_extract_decision_sections_captures_decision() {
    echo ""
    echo "=== Test: extract_decision_sections captures ## Decision section ==="

    if type extract_decision_sections &>/dev/null; then
        local result
        result=$(extract_decision_sections "$TEST_FIXTURES_DIR/plans/both-sections.md" 2>&1) || true

        if echo "$result" | grep -q "We decided to use Bash"; then
            pass_test "Result should contain Decision section content"
        else
            fail_test "Result should contain Decision section content" "Decision content not found"
        fi

        if echo "$result" | grep -q "Claude Code native"; then
            pass_test "Result should capture full Decision content"
        else
            fail_test "Result should capture full Decision content" "Full content not found"
        fi
    else
        fail_test "Result should contain Decision section content" "Function extract_decision_sections does not exist"
        fail_test "Result should capture full Decision content" "Function extract_decision_sections does not exist"
    fi
}

test_extract_decision_sections_captures_technical_approach() {
    echo ""
    echo "=== Test: extract_decision_sections captures ## Technical Approach section ==="

    if type extract_decision_sections &>/dev/null; then
        local result
        result=$(extract_decision_sections "$TEST_FIXTURES_DIR/plans/both-sections.md" 2>&1) || true

        if echo "$result" | grep -q "implementation will follow"; then
            pass_test "Result should contain Technical Approach section content"
        else
            fail_test "Result should contain Technical Approach section content" "Content not found"
        fi

        if echo "$result" | grep -q "Parse frontmatter using awk"; then
            pass_test "Result should capture full Technical Approach content"
        else
            fail_test "Result should capture full Technical Approach content" "Full content not found"
        fi
    else
        fail_test "Result should contain Technical Approach section content" "Function extract_decision_sections does not exist"
        fail_test "Result should capture full Technical Approach content" "Function extract_decision_sections does not exist"
    fi
}

test_extract_decision_sections_returns_json() {
    echo ""
    echo "=== Test: extract_decision_sections returns JSON format ==="

    if type extract_decision_sections &>/dev/null; then
        local result
        result=$(extract_decision_sections "$TEST_FIXTURES_DIR/plans/both-sections.md" 2>&1) || true

        if echo "$result" | grep -q '"decision"'; then
            pass_test "Result should have 'decision' JSON field"
        else
            fail_test "Result should have 'decision' JSON field" "Field not found"
        fi

        if echo "$result" | grep -q '"technical_approach"'; then
            pass_test "Result should have 'technical_approach' JSON field"
        else
            fail_test "Result should have 'technical_approach' JSON field" "Field not found"
        fi
    else
        fail_test "Result should have 'decision' JSON field" "Function extract_decision_sections does not exist"
        fail_test "Result should have 'technical_approach' JSON field" "Function extract_decision_sections does not exist"
    fi
}

test_extract_decision_sections_handles_decision_only() {
    echo ""
    echo "=== Test: extract_decision_sections handles file with only Decision ==="

    if type extract_decision_sections &>/dev/null; then
        local result
        result=$(extract_decision_sections "$TEST_FIXTURES_DIR/plans/decision-only.md" 2>&1) || true

        if echo "$result" | grep -q "This plan only has a Decision section"; then
            pass_test "Result should contain Decision section"
        else
            fail_test "Result should contain Decision section" "Content not found"
        fi
    else
        fail_test "Result should contain Decision section" "Function extract_decision_sections does not exist"
    fi
}

test_extract_decision_sections_handles_technical_only() {
    echo ""
    echo "=== Test: extract_decision_sections handles file with only Technical Approach ==="

    if type extract_decision_sections &>/dev/null; then
        local result
        result=$(extract_decision_sections "$TEST_FIXTURES_DIR/plans/technical-only.md" 2>&1) || true

        if echo "$result" | grep -q "This plan only has a Technical Approach section"; then
            pass_test "Result should contain Technical Approach section"
        else
            fail_test "Result should contain Technical Approach section" "Content not found"
        fi
    else
        fail_test "Result should contain Technical Approach section" "Function extract_decision_sections does not exist"
    fi
}

test_extract_decision_sections_handles_no_sections() {
    echo ""
    echo "=== Test: extract_decision_sections handles file with no decision sections ==="

    if type extract_decision_sections &>/dev/null; then
        local result
        result=$(extract_decision_sections "$TEST_FIXTURES_DIR/plans/no-decision-sections.md" 2>&1) || true

        # Should return valid JSON even for files without decision sections
        if echo "$result" | grep -qE '^\{.*\}$'; then
            pass_test "Returns valid JSON for file with no decision sections"
        else
            fail_test "Returns valid JSON for file with no decision sections" "Invalid JSON returned"
        fi
    else
        fail_test "Returns valid JSON for file with no decision sections" "Function extract_decision_sections does not exist"
    fi
}

test_extract_decision_sections_handles_missing_file() {
    echo ""
    echo "=== Test: extract_decision_sections handles missing file ==="

    if type extract_decision_sections &>/dev/null; then
        local result
        result=$(extract_decision_sections "$TEST_FIXTURES_DIR/plans/nonexistent.md" 2>&1) || true

        if echo "$result" | grep -qi "error"; then
            pass_test "Result should contain error for missing file"
        else
            fail_test "Result should contain error for missing file" "No error reported"
        fi
    else
        fail_test "Result should contain error for missing file" "Function extract_decision_sections does not exist"
    fi
}

# =============================================================================
# Main Test Runner
# =============================================================================
main() {
    echo "=============================================="
    echo "STORY-232 AC#2: Decision Section Extraction Tests"
    echo "TDD RED PHASE - Tests expected to FAIL"
    echo "=============================================="
    echo ""

    # Setup
    setup_fixtures

    # Run tests
    test_extract_decision_sections_function_exists
    test_extract_decision_sections_captures_decision
    test_extract_decision_sections_captures_technical_approach
    test_extract_decision_sections_returns_json
    test_extract_decision_sections_handles_decision_only
    test_extract_decision_sections_handles_technical_only
    test_extract_decision_sections_handles_no_sections
    test_extract_decision_sections_handles_missing_file

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
