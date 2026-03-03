#!/bin/bash
# STORY-233: Test AC#1 - Search by Story ID
# Test that search_by_story_id() returns all decisions for a given story ID
#
# TDD RED PHASE: These tests should FAIL because the functions don't exist yet
#
# Expected Functions (to be implemented in plan_file_kb.sh):
#   - search_by_story_id(index_dir, story_id) - Search decisions by story ID
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

    # Create a pre-built index for search tests (simulating build_searchable_index output)
    cat > "$TEST_FIXTURES_DIR/index/searchable_index.json" << 'INDEXEOF'
{
  "plans": {
    "STORY-100-auth-plan.md": {
      "story_id": "STORY-100",
      "status": "completed",
      "created": "2025-01-01",
      "decision": "Use JWT tokens for authentication with refresh token rotation.",
      "technical_approach": "1. Implement token service 2. Add refresh endpoint 3. Secure storage",
      "rationale": "JWT provides stateless auth suitable for microservices architecture.",
      "outcome": "Successfully implemented. All auth tests passing."
    },
    "STORY-100-security-addon.md": {
      "story_id": "STORY-100",
      "status": "completed",
      "created": "2025-01-05",
      "decision": "Add MFA support using TOTP for additional security layer.",
      "technical_approach": "1. Generate TOTP secrets 2. Add verification endpoint 3. Update login flow",
      "rationale": "MFA reduces account compromise risk by 99.9%.",
      "outcome": "MFA optional for all users, mandatory for admin accounts."
    },
    "STORY-200-database.md": {
      "story_id": "STORY-200",
      "status": "completed",
      "created": "2025-01-02",
      "decision": "PostgreSQL as primary database with read replicas.",
      "technical_approach": "1. Configure master 2. Setup replication 3. Add connection pooling",
      "rationale": "PostgreSQL offers best balance of features and performance.",
      "outcome": "Database deployed with 3 read replicas."
    },
    "STORY-300-caching.md": {
      "story_id": "STORY-300",
      "status": "in_progress",
      "created": "2025-01-03",
      "decision": "Redis for session caching and rate limiting.",
      "technical_approach": "1. Deploy Redis cluster 2. Implement cache service 3. Add TTL policies",
      "rationale": "Redis provides sub-millisecond latency for cache operations.",
      "outcome": ""
    }
  },
  "story_index": {
    "STORY-100": ["STORY-100-auth-plan.md", "STORY-100-security-addon.md"],
    "STORY-200": ["STORY-200-database.md"],
    "STORY-300": ["STORY-300-caching.md"]
  }
}
INDEXEOF
}

cleanup_fixtures() {
    rm -rf "$TEST_FIXTURES_DIR"
}

# =============================================================================
# Test Cases for AC#1: Search by Story ID
# =============================================================================

test_search_by_story_id_function_exists() {
    echo ""
    echo "=== Test: search_by_story_id function exists ==="

    if type search_by_story_id &>/dev/null; then
        pass_test "Function search_by_story_id should exist in plan_file_kb.sh"
    else
        fail_test "Function search_by_story_id should exist in plan_file_kb.sh" \
            "Function 'search_by_story_id' does not exist"
    fi
}

test_search_by_story_id_returns_valid_json() {
    echo ""
    echo "=== Test: search_by_story_id returns valid JSON ==="

    if type search_by_story_id &>/dev/null; then
        local result
        result=$(search_by_story_id "$TEST_FIXTURES_DIR/index" "STORY-100" 2>&1) || true

        # Check for valid JSON structure
        if echo "$result" | grep -qE '^\{.*\}$'; then
            pass_test "Result should be valid JSON"
        else
            fail_test "Result should be valid JSON" "Invalid JSON structure"
        fi
    else
        fail_test "Result should be valid JSON" "Function search_by_story_id does not exist"
    fi
}

test_search_by_story_id_returns_all_decisions_for_story() {
    echo ""
    echo "=== Test: search_by_story_id returns all decisions for a story ==="

    if type search_by_story_id &>/dev/null; then
        local result
        result=$(search_by_story_id "$TEST_FIXTURES_DIR/index" "STORY-100" 2>&1) || true

        # STORY-100 has 2 plan files
        if echo "$result" | grep -q "STORY-100-auth-plan.md"; then
            pass_test "Result should contain auth plan for STORY-100"
        else
            fail_test "Result should contain auth plan for STORY-100" "auth plan not found"
        fi

        if echo "$result" | grep -q "STORY-100-security-addon.md"; then
            pass_test "Result should contain security addon for STORY-100"
        else
            fail_test "Result should contain security addon for STORY-100" "security addon not found"
        fi

        # Should NOT contain other stories
        if echo "$result" | grep -q "STORY-200-database.md"; then
            fail_test "Result should NOT contain STORY-200 plans" "STORY-200 incorrectly included"
        else
            pass_test "Result should NOT contain STORY-200 plans"
        fi
    else
        fail_test "Result should contain auth plan for STORY-100" "Function search_by_story_id does not exist"
        fail_test "Result should contain security addon for STORY-100" "Function search_by_story_id does not exist"
        fail_test "Result should NOT contain STORY-200 plans" "Function search_by_story_id does not exist"
    fi
}

test_search_by_story_id_includes_decision_details() {
    echo ""
    echo "=== Test: search_by_story_id includes decision details ==="

    if type search_by_story_id &>/dev/null; then
        local result
        result=$(search_by_story_id "$TEST_FIXTURES_DIR/index" "STORY-100" 2>&1) || true

        if echo "$result" | grep -q "JWT tokens"; then
            pass_test "Result should include decision content"
        else
            fail_test "Result should include decision content" "decision content not found"
        fi

        if echo "$result" | grep -q "MFA support"; then
            pass_test "Result should include all decision content"
        else
            fail_test "Result should include all decision content" "MFA decision not found"
        fi
    else
        fail_test "Result should include decision content" "Function search_by_story_id does not exist"
        fail_test "Result should include all decision content" "Function search_by_story_id does not exist"
    fi
}

test_search_by_story_id_returns_count() {
    echo ""
    echo "=== Test: search_by_story_id returns count of decisions ==="

    if type search_by_story_id &>/dev/null; then
        local result
        result=$(search_by_story_id "$TEST_FIXTURES_DIR/index" "STORY-100" 2>&1) || true

        if echo "$result" | grep -qE '"count"[[:space:]]*:[[:space:]]*2'; then
            pass_test "Result should show count of 2 for STORY-100"
        else
            fail_test "Result should show count of 2 for STORY-100" "count field incorrect or missing"
        fi
    else
        fail_test "Result should show count of 2 for STORY-100" "Function search_by_story_id does not exist"
    fi
}

test_search_by_story_id_single_result() {
    echo ""
    echo "=== Test: search_by_story_id works with single result ==="

    if type search_by_story_id &>/dev/null; then
        local result
        result=$(search_by_story_id "$TEST_FIXTURES_DIR/index" "STORY-200" 2>&1) || true

        if echo "$result" | grep -q "STORY-200-database.md"; then
            pass_test "Result should find STORY-200 plan"
        else
            fail_test "Result should find STORY-200 plan" "plan not found"
        fi

        if echo "$result" | grep -qE '"count"[[:space:]]*:[[:space:]]*1'; then
            pass_test "Result should show count of 1 for STORY-200"
        else
            fail_test "Result should show count of 1 for STORY-200" "count field incorrect"
        fi
    else
        fail_test "Result should find STORY-200 plan" "Function search_by_story_id does not exist"
        fail_test "Result should show count of 1 for STORY-200" "Function search_by_story_id does not exist"
    fi
}

test_search_by_story_id_empty_for_nonexistent_story() {
    echo ""
    echo "=== Test: search_by_story_id returns empty for nonexistent story ==="

    if type search_by_story_id &>/dev/null; then
        local result
        result=$(search_by_story_id "$TEST_FIXTURES_DIR/index" "STORY-999" 2>&1) || true

        if echo "$result" | grep -qE '"count"[[:space:]]*:[[:space:]]*0|"decisions"[[:space:]]*:[[:space:]]*\[\]'; then
            pass_test "Returns empty/zero for nonexistent story"
        else
            fail_test "Returns empty/zero for nonexistent story" "Non-empty result returned"
        fi
    else
        fail_test "Returns empty/zero for nonexistent story" "Function search_by_story_id does not exist"
    fi
}

test_search_by_story_id_handles_invalid_story_format() {
    echo ""
    echo "=== Test: search_by_story_id handles invalid story ID format ==="

    if type search_by_story_id &>/dev/null; then
        local result
        result=$(search_by_story_id "$TEST_FIXTURES_DIR/index" "invalid-format" 2>&1) || true

        if echo "$result" | grep -qiE 'error|"count"[[:space:]]*:[[:space:]]*0'; then
            pass_test "Handles invalid story ID format appropriately"
        else
            fail_test "Handles invalid story ID format appropriately" "No error or empty result"
        fi
    else
        fail_test "Handles invalid story ID format appropriately" "Function search_by_story_id does not exist"
    fi
}

test_search_by_story_id_handles_missing_index() {
    echo ""
    echo "=== Test: search_by_story_id handles missing index directory ==="

    if type search_by_story_id &>/dev/null; then
        local result
        result=$(search_by_story_id "$TEST_FIXTURES_DIR/nonexistent" "STORY-100" 2>&1) || true

        if echo "$result" | grep -qi "error"; then
            pass_test "Returns error for missing index directory"
        else
            fail_test "Returns error for missing index directory" "No error reported"
        fi
    else
        fail_test "Returns error for missing index directory" "Function search_by_story_id does not exist"
    fi
}

# =============================================================================
# Main Test Runner
# =============================================================================
main() {
    echo "=============================================="
    echo "STORY-233 AC#1: Search by Story ID Tests"
    echo "TDD RED PHASE - Tests expected to FAIL"
    echo "=============================================="
    echo ""

    # Setup
    setup_fixtures

    # Run tests
    test_search_by_story_id_function_exists
    test_search_by_story_id_returns_valid_json
    test_search_by_story_id_returns_all_decisions_for_story
    test_search_by_story_id_includes_decision_details
    test_search_by_story_id_returns_count
    test_search_by_story_id_single_result
    test_search_by_story_id_empty_for_nonexistent_story
    test_search_by_story_id_handles_invalid_story_format
    test_search_by_story_id_handles_missing_index

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
