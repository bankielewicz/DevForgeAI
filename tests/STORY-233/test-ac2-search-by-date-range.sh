#!/bin/bash
# STORY-233: Test AC#2 - Search by Date Range
# Test that search_by_date_range() returns decisions created in a given date range
#
# TDD RED PHASE: These tests should FAIL because the functions don't exist yet
#
# Expected Functions (to be implemented in plan_file_kb.sh):
#   - search_by_date_range(index_dir, start_date, end_date) - Search by date range
#
# Tech Stack: Bash scripting (Claude Code native) - per tech-stack.md lines 48-63

# =============================================================================
# Test Configuration
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PLAN_FILE_KB="$PROJECT_ROOT/src/claude/scripts/plan_file_kb.sh"
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
    mkdir -p "$TEST_FIXTURES_DIR/index"

    # Create a pre-built index with various dates
    cat > "$TEST_FIXTURES_DIR/index/searchable_index.json" << 'INDEXEOF'
{
  "plans": {
    "plan-2024-12-15.md": {
      "story_id": "STORY-050",
      "status": "completed",
      "created": "2024-12-15",
      "decision": "Initial architecture decision from December 2024.",
      "technical_approach": "Legacy approach using older patterns.",
      "rationale": "Based on requirements at the time.",
      "outcome": "Deployed successfully."
    },
    "plan-2025-01-01.md": {
      "story_id": "STORY-100",
      "status": "completed",
      "created": "2025-01-01",
      "decision": "New year decision - authentication system.",
      "technical_approach": "Modern JWT-based authentication.",
      "rationale": "Industry standard for 2025.",
      "outcome": "Implemented in Q1."
    },
    "plan-2025-01-05.md": {
      "story_id": "STORY-110",
      "status": "completed",
      "created": "2025-01-05",
      "decision": "Mid-January decision - caching layer.",
      "technical_approach": "Redis cluster with failover.",
      "rationale": "Performance requirements.",
      "outcome": "Reduced latency by 80%."
    },
    "plan-2025-01-10.md": {
      "story_id": "STORY-120",
      "status": "in_progress",
      "created": "2025-01-10",
      "decision": "Late January decision - API gateway.",
      "technical_approach": "Kong API gateway with custom plugins.",
      "rationale": "Centralized API management needed.",
      "outcome": ""
    },
    "plan-2025-01-15.md": {
      "story_id": "STORY-130",
      "status": "draft",
      "created": "2025-01-15",
      "decision": "Mid-month decision - monitoring stack.",
      "technical_approach": "Prometheus + Grafana + AlertManager.",
      "rationale": "Observability requirements.",
      "outcome": ""
    }
  },
  "date_index": {
    "2024-12-15": ["plan-2024-12-15.md"],
    "2025-01-01": ["plan-2025-01-01.md"],
    "2025-01-05": ["plan-2025-01-05.md"],
    "2025-01-10": ["plan-2025-01-10.md"],
    "2025-01-15": ["plan-2025-01-15.md"]
  }
}
INDEXEOF
}

cleanup_fixtures() {
    rm -rf "$TEST_FIXTURES_DIR"
}

# =============================================================================
# Test Cases for AC#2: Search by Date Range
# =============================================================================

test_search_by_date_range_function_exists() {
    echo ""
    echo "=== Test: search_by_date_range function exists ==="

    if type search_by_date_range &>/dev/null; then
        pass_test "Function search_by_date_range should exist in plan_file_kb.sh"
    else
        fail_test "Function search_by_date_range should exist in plan_file_kb.sh" \
            "Function 'search_by_date_range' does not exist"
    fi
}

test_search_by_date_range_returns_valid_json() {
    echo ""
    echo "=== Test: search_by_date_range returns valid JSON ==="

    if type search_by_date_range &>/dev/null; then
        local result
        result=$(search_by_date_range "$TEST_FIXTURES_DIR/index" "2025-01-01" "2025-01-31" 2>&1) || true

        if echo "$result" | grep -qE '^\{.*\}$'; then
            pass_test "Result should be valid JSON"
        else
            fail_test "Result should be valid JSON" "Invalid JSON structure"
        fi
    else
        fail_test "Result should be valid JSON" "Function search_by_date_range does not exist"
    fi
}

test_search_by_date_range_finds_decisions_in_range() {
    echo ""
    echo "=== Test: search_by_date_range finds decisions in date range ==="

    if type search_by_date_range &>/dev/null; then
        local result
        result=$(search_by_date_range "$TEST_FIXTURES_DIR/index" "2025-01-01" "2025-01-10" 2>&1) || true

        # Should find plans from Jan 1, 5, and 10
        if echo "$result" | grep -q "plan-2025-01-01.md"; then
            pass_test "Result should contain Jan 1 plan"
        else
            fail_test "Result should contain Jan 1 plan" "Jan 1 plan not found"
        fi

        if echo "$result" | grep -q "plan-2025-01-05.md"; then
            pass_test "Result should contain Jan 5 plan"
        else
            fail_test "Result should contain Jan 5 plan" "Jan 5 plan not found"
        fi

        if echo "$result" | grep -q "plan-2025-01-10.md"; then
            pass_test "Result should contain Jan 10 plan"
        else
            fail_test "Result should contain Jan 10 plan" "Jan 10 plan not found"
        fi

        # Should NOT find Jan 15 plan (outside range)
        if echo "$result" | grep -q "plan-2025-01-15.md"; then
            fail_test "Result should NOT contain Jan 15 plan" "Jan 15 incorrectly included"
        else
            pass_test "Result should NOT contain Jan 15 plan"
        fi

        # Should NOT find Dec 15 plan (outside range)
        if echo "$result" | grep -q "plan-2024-12-15.md"; then
            fail_test "Result should NOT contain Dec 15 plan" "Dec 15 incorrectly included"
        else
            pass_test "Result should NOT contain Dec 15 plan"
        fi
    else
        fail_test "Result should contain Jan 1 plan" "Function search_by_date_range does not exist"
        fail_test "Result should contain Jan 5 plan" "Function search_by_date_range does not exist"
        fail_test "Result should contain Jan 10 plan" "Function search_by_date_range does not exist"
        fail_test "Result should NOT contain Jan 15 plan" "Function search_by_date_range does not exist"
        fail_test "Result should NOT contain Dec 15 plan" "Function search_by_date_range does not exist"
    fi
}

test_search_by_date_range_inclusive_boundaries() {
    echo ""
    echo "=== Test: search_by_date_range includes boundary dates ==="

    if type search_by_date_range &>/dev/null; then
        local result
        result=$(search_by_date_range "$TEST_FIXTURES_DIR/index" "2025-01-05" "2025-01-05" 2>&1) || true

        # Single day range should find exact match
        if echo "$result" | grep -q "plan-2025-01-05.md"; then
            pass_test "Single day range should find exact date match"
        else
            fail_test "Single day range should find exact date match" "Exact date not found"
        fi

        if echo "$result" | grep -qE '"count"[[:space:]]*:[[:space:]]*1'; then
            pass_test "Single day should return count of 1"
        else
            fail_test "Single day should return count of 1" "count incorrect"
        fi
    else
        fail_test "Single day range should find exact date match" "Function search_by_date_range does not exist"
        fail_test "Single day should return count of 1" "Function search_by_date_range does not exist"
    fi
}

test_search_by_date_range_returns_count() {
    echo ""
    echo "=== Test: search_by_date_range returns count of decisions ==="

    if type search_by_date_range &>/dev/null; then
        local result
        result=$(search_by_date_range "$TEST_FIXTURES_DIR/index" "2025-01-01" "2025-01-10" 2>&1) || true

        if echo "$result" | grep -qE '"count"[[:space:]]*:[[:space:]]*3'; then
            pass_test "Result should show count of 3 for Jan 1-10 range"
        else
            fail_test "Result should show count of 3 for Jan 1-10 range" "count field incorrect"
        fi
    else
        fail_test "Result should show count of 3 for Jan 1-10 range" "Function search_by_date_range does not exist"
    fi
}

test_search_by_date_range_cross_year() {
    echo ""
    echo "=== Test: search_by_date_range works across year boundary ==="

    if type search_by_date_range &>/dev/null; then
        local result
        result=$(search_by_date_range "$TEST_FIXTURES_DIR/index" "2024-12-01" "2025-01-05" 2>&1) || true

        # Should find Dec 15 2024 and Jan 1, 5 2025
        if echo "$result" | grep -q "plan-2024-12-15.md"; then
            pass_test "Cross-year range should find Dec 2024 plan"
        else
            fail_test "Cross-year range should find Dec 2024 plan" "Dec plan not found"
        fi

        if echo "$result" | grep -q "plan-2025-01-01.md"; then
            pass_test "Cross-year range should find Jan 2025 plan"
        else
            fail_test "Cross-year range should find Jan 2025 plan" "Jan 1 plan not found"
        fi
    else
        fail_test "Cross-year range should find Dec 2024 plan" "Function search_by_date_range does not exist"
        fail_test "Cross-year range should find Jan 2025 plan" "Function search_by_date_range does not exist"
    fi
}

test_search_by_date_range_empty_for_no_matches() {
    echo ""
    echo "=== Test: search_by_date_range returns empty for no matches ==="

    if type search_by_date_range &>/dev/null; then
        local result
        result=$(search_by_date_range "$TEST_FIXTURES_DIR/index" "2023-01-01" "2023-12-31" 2>&1) || true

        if echo "$result" | grep -qE '"count"[[:space:]]*:[[:space:]]*0|"decisions"[[:space:]]*:[[:space:]]*\[\]'; then
            pass_test "Returns empty/zero for range with no decisions"
        else
            fail_test "Returns empty/zero for range with no decisions" "Non-empty result returned"
        fi
    else
        fail_test "Returns empty/zero for range with no decisions" "Function search_by_date_range does not exist"
    fi
}

test_search_by_date_range_handles_invalid_date_format() {
    echo ""
    echo "=== Test: search_by_date_range handles invalid date format ==="

    if type search_by_date_range &>/dev/null; then
        local result
        result=$(search_by_date_range "$TEST_FIXTURES_DIR/index" "invalid-date" "2025-01-31" 2>&1) || true

        if echo "$result" | grep -qi "error"; then
            pass_test "Returns error for invalid date format"
        else
            fail_test "Returns error for invalid date format" "No error reported"
        fi
    else
        fail_test "Returns error for invalid date format" "Function search_by_date_range does not exist"
    fi
}

test_search_by_date_range_handles_reversed_dates() {
    echo ""
    echo "=== Test: search_by_date_range handles reversed date range ==="

    if type search_by_date_range &>/dev/null; then
        local result
        result=$(search_by_date_range "$TEST_FIXTURES_DIR/index" "2025-01-31" "2025-01-01" 2>&1) || true

        # Should either error or auto-correct (either is acceptable)
        if echo "$result" | grep -qiE 'error|"count"[[:space:]]*:[[:space:]]*0|"count"[[:space:]]*:[[:space:]]*4'; then
            pass_test "Handles reversed date range appropriately"
        else
            fail_test "Handles reversed date range appropriately" "Unexpected response"
        fi
    else
        fail_test "Handles reversed date range appropriately" "Function search_by_date_range does not exist"
    fi
}

test_search_by_date_range_handles_missing_index() {
    echo ""
    echo "=== Test: search_by_date_range handles missing index directory ==="

    if type search_by_date_range &>/dev/null; then
        local result
        result=$(search_by_date_range "$TEST_FIXTURES_DIR/nonexistent" "2025-01-01" "2025-01-31" 2>&1) || true

        if echo "$result" | grep -qi "error"; then
            pass_test "Returns error for missing index directory"
        else
            fail_test "Returns error for missing index directory" "No error reported"
        fi
    else
        fail_test "Returns error for missing index directory" "Function search_by_date_range does not exist"
    fi
}

test_search_by_date_range_includes_date_range_in_response() {
    echo ""
    echo "=== Test: search_by_date_range includes query dates in response ==="

    if type search_by_date_range &>/dev/null; then
        local result
        result=$(search_by_date_range "$TEST_FIXTURES_DIR/index" "2025-01-01" "2025-01-10" 2>&1) || true

        if echo "$result" | grep -q '"start_date"'; then
            pass_test "Response should include start_date field"
        else
            fail_test "Response should include start_date field" "start_date not found"
        fi

        if echo "$result" | grep -q '"end_date"'; then
            pass_test "Response should include end_date field"
        else
            fail_test "Response should include end_date field" "end_date not found"
        fi
    else
        fail_test "Response should include start_date field" "Function search_by_date_range does not exist"
        fail_test "Response should include end_date field" "Function search_by_date_range does not exist"
    fi
}

# =============================================================================
# Main Test Runner
# =============================================================================
main() {
    echo "=============================================="
    echo "STORY-233 AC#2: Search by Date Range Tests"
    echo "TDD RED PHASE - Tests expected to FAIL"
    echo "=============================================="
    echo ""

    # Setup
    setup_fixtures

    # Run tests
    test_search_by_date_range_function_exists
    test_search_by_date_range_returns_valid_json
    test_search_by_date_range_finds_decisions_in_range
    test_search_by_date_range_inclusive_boundaries
    test_search_by_date_range_returns_count
    test_search_by_date_range_cross_year
    test_search_by_date_range_empty_for_no_matches
    test_search_by_date_range_handles_invalid_date_format
    test_search_by_date_range_handles_reversed_dates
    test_search_by_date_range_handles_missing_index
    test_search_by_date_range_includes_date_range_in_response

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
