#!/bin/bash
# STORY-232: Test AC#3 - Full-Text Search Support
# Test that search_index() returns matching plan files via keyword search
#
# TDD RED PHASE: These tests should FAIL because the functions don't exist yet
#
# Expected Functions (to be implemented in plan_file_kb.sh):
#   - search_index(index_dir, keyword) - Search index for keyword, return matching plan files
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
    mkdir -p "$TEST_FIXTURES_DIR/index"

    # Create a pre-built index for search tests (simulating build_searchable_index output)
    cat > "$TEST_FIXTURES_DIR/index/searchable_index.json" << 'INDEXEOF'
{
  "plans": {
    "STORY-100-authentication.md": {
      "story_id": "STORY-100",
      "status": "completed",
      "created": "2025-01-01",
      "decision": "We decided to use JWT tokens for authentication. OAuth2 flow will be implemented with refresh tokens.",
      "technical_approach": "1. Implement login endpoint 2. Generate JWT on successful authentication",
      "full_text": "User Authentication JWT tokens OAuth2 refresh tokens login endpoint authentication"
    },
    "STORY-200-database.md": {
      "story_id": "STORY-200",
      "status": "completed",
      "created": "2025-01-02",
      "decision": "PostgreSQL will be used as the primary database. Migration scripts will use Flyway.",
      "technical_approach": "1. Create migration files 2. Run Flyway migrate command",
      "full_text": "Database Migration PostgreSQL Flyway migration files schema changes"
    },
    "STORY-300-caching.md": {
      "story_id": "STORY-300",
      "status": "in_progress",
      "created": "2025-01-03",
      "decision": "Redis will be used for session caching and rate limiting. Authentication tokens will be cached.",
      "technical_approach": "1. Configure Redis connection 2. Implement cache service",
      "full_text": "Redis Caching Layer session caching rate limiting authentication tokens"
    },
    "STORY-400-api.md": {
      "story_id": "STORY-400",
      "status": "draft",
      "created": "2025-01-04",
      "decision": "RESTful API following OpenAPI 3.0 specification.",
      "technical_approach": "1. Define OpenAPI spec 2. Generate API documentation 3. Implement endpoints",
      "full_text": "REST API Design OpenAPI endpoints documentation"
    }
  },
  "keywords": {
    "authentication": ["STORY-100-authentication.md", "STORY-300-caching.md"],
    "jwt": ["STORY-100-authentication.md"],
    "database": ["STORY-200-database.md"],
    "postgresql": ["STORY-200-database.md"],
    "redis": ["STORY-300-caching.md"],
    "caching": ["STORY-300-caching.md"],
    "api": ["STORY-400-api.md"],
    "flyway": ["STORY-200-database.md"],
    "endpoint": ["STORY-100-authentication.md", "STORY-400-api.md"]
  }
}
INDEXEOF
}

cleanup_fixtures() {
    rm -rf "$TEST_FIXTURES_DIR"
}

# =============================================================================
# Test Cases for AC#3: Full-Text Search Support
# =============================================================================

test_search_index_function_exists() {
    echo ""
    echo "=== Test: search_index function exists ==="

    if type search_index &>/dev/null; then
        pass_test "Function search_index should exist in plan_file_kb.sh"
    else
        fail_test "Function search_index should exist in plan_file_kb.sh" \
            "Function 'search_index' does not exist"
    fi
}

test_search_index_finds_single_match() {
    echo ""
    echo "=== Test: search_index finds single keyword match ==="

    if type search_index &>/dev/null; then
        local result
        result=$(search_index "$TEST_FIXTURES_DIR/index" "jwt" 2>&1) || true

        if echo "$result" | grep -q "STORY-100-authentication.md"; then
            pass_test "Search for 'jwt' should find authentication plan"
        else
            fail_test "Search for 'jwt' should find authentication plan" "Not found in results"
        fi

        if echo "$result" | grep -q "STORY-200-database.md"; then
            fail_test "Search for 'jwt' should NOT find database plan" "Database plan incorrectly found"
        else
            pass_test "Search for 'jwt' should NOT find database plan"
        fi
    else
        fail_test "Search for 'jwt' should find authentication plan" "Function search_index does not exist"
        fail_test "Search for 'jwt' should NOT find database plan" "Function search_index does not exist"
    fi
}

test_search_index_finds_multiple_matches() {
    echo ""
    echo "=== Test: search_index finds multiple matches for common keyword ==="

    if type search_index &>/dev/null; then
        local result
        result=$(search_index "$TEST_FIXTURES_DIR/index" "authentication" 2>&1) || true

        if echo "$result" | grep -q "STORY-100-authentication.md"; then
            pass_test "Search for 'authentication' should find auth plan"
        else
            fail_test "Search for 'authentication' should find auth plan" "Not found"
        fi

        if echo "$result" | grep -q "STORY-300-caching.md"; then
            pass_test "Search for 'authentication' should find caching plan"
        else
            fail_test "Search for 'authentication' should find caching plan" "Not found"
        fi
    else
        fail_test "Search for 'authentication' should find auth plan" "Function search_index does not exist"
        fail_test "Search for 'authentication' should find caching plan" "Function search_index does not exist"
    fi
}

test_search_index_returns_json() {
    echo ""
    echo "=== Test: search_index returns JSON format ==="

    if type search_index &>/dev/null; then
        local result
        result=$(search_index "$TEST_FIXTURES_DIR/index" "redis" 2>&1) || true

        if echo "$result" | grep -q '"matches"'; then
            pass_test "Result should have 'matches' JSON field"
        else
            fail_test "Result should have 'matches' JSON field" "Field not found"
        fi

        if echo "$result" | grep -q '"query"'; then
            pass_test "Result should have 'query' JSON field"
        else
            fail_test "Result should have 'query' JSON field" "Field not found"
        fi

        if echo "$result" | grep -q '"count"'; then
            pass_test "Result should have 'count' JSON field"
        else
            fail_test "Result should have 'count' JSON field" "Field not found"
        fi
    else
        fail_test "Result should have 'matches' JSON field" "Function search_index does not exist"
        fail_test "Result should have 'query' JSON field" "Function search_index does not exist"
        fail_test "Result should have 'count' JSON field" "Function search_index does not exist"
    fi
}

test_search_index_returns_empty_for_no_match() {
    echo ""
    echo "=== Test: search_index returns empty for no matches ==="

    if type search_index &>/dev/null; then
        local result
        result=$(search_index "$TEST_FIXTURES_DIR/index" "nonexistentterm123" 2>&1) || true

        if echo "$result" | grep -qE '"count"[[:space:]]*:[[:space:]]*0|"matches"[[:space:]]*:[[:space:]]*\[\]'; then
            pass_test "Returns empty/zero for no matches"
        else
            fail_test "Returns empty/zero for no matches" "Non-empty result returned"
        fi
    else
        fail_test "Returns empty/zero for no matches" "Function search_index does not exist"
    fi
}

test_search_index_searches_decision_content() {
    echo ""
    echo "=== Test: search_index searches within Decision content ==="

    if type search_index &>/dev/null; then
        local result
        result=$(search_index "$TEST_FIXTURES_DIR/index" "flyway" 2>&1) || true

        if echo "$result" | grep -q "STORY-200-database.md"; then
            pass_test "Search for 'flyway' should find database plan"
        else
            fail_test "Search for 'flyway' should find database plan" "Not found"
        fi
    else
        fail_test "Search for 'flyway' should find database plan" "Function search_index does not exist"
    fi
}

test_search_index_searches_technical_approach_content() {
    echo ""
    echo "=== Test: search_index searches within Technical Approach content ==="

    if type search_index &>/dev/null; then
        local result
        result=$(search_index "$TEST_FIXTURES_DIR/index" "endpoint" 2>&1) || true

        if echo "$result" | grep -q "STORY-100-authentication.md"; then
            pass_test "Search for 'endpoint' should find auth plan"
        else
            fail_test "Search for 'endpoint' should find auth plan" "Not found"
        fi

        if echo "$result" | grep -q "STORY-400-api.md"; then
            pass_test "Search for 'endpoint' should find API plan"
        else
            fail_test "Search for 'endpoint' should find API plan" "Not found"
        fi
    else
        fail_test "Search for 'endpoint' should find auth plan" "Function search_index does not exist"
        fail_test "Search for 'endpoint' should find API plan" "Function search_index does not exist"
    fi
}

test_search_index_handles_missing_index() {
    echo ""
    echo "=== Test: search_index handles missing index gracefully ==="

    if type search_index &>/dev/null; then
        local result
        result=$(search_index "$TEST_FIXTURES_DIR/nonexistent" "query" 2>&1) || true

        if echo "$result" | grep -qi "error"; then
            pass_test "Result should contain error for missing index"
        else
            fail_test "Result should contain error for missing index" "No error reported"
        fi
    else
        fail_test "Result should contain error for missing index" "Function search_index does not exist"
    fi
}

test_search_index_handles_empty_query() {
    echo ""
    echo "=== Test: search_index handles empty query ==="

    if type search_index &>/dev/null; then
        local result
        result=$(search_index "$TEST_FIXTURES_DIR/index" "" 2>&1) || true

        if echo "$result" | grep -qiE 'error|"count"[[:space:]]*:[[:space:]]*0'; then
            pass_test "Handles empty query appropriately"
        else
            fail_test "Handles empty query appropriately" "Invalid response"
        fi
    else
        fail_test "Handles empty query appropriately" "Function search_index does not exist"
    fi
}

# =============================================================================
# Main Test Runner
# =============================================================================
main() {
    echo "=============================================="
    echo "STORY-232 AC#3: Full-Text Search Support Tests"
    echo "TDD RED PHASE - Tests expected to FAIL"
    echo "=============================================="
    echo ""

    # Setup
    setup_fixtures

    # Run tests
    test_search_index_function_exists
    test_search_index_finds_single_match
    test_search_index_finds_multiple_matches
    test_search_index_returns_json
    test_search_index_returns_empty_for_no_match
    test_search_index_searches_decision_content
    test_search_index_searches_technical_approach_content
    test_search_index_handles_missing_index
    test_search_index_handles_empty_query

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
