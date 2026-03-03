#!/bin/bash
# STORY-233: Test AC#3 - Search by Keywords
# Test that search_by_keywords() returns decisions with relevance ranking
#
# TDD RED PHASE: These tests should FAIL because the functions don't exist yet
#
# Expected Functions (to be implemented in plan_file_kb.sh):
#   - search_by_keywords(index_dir, keywords) - Search with relevance ranking
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

    # Create index with keyword-rich content for relevance testing
    cat > "$TEST_FIXTURES_DIR/index/searchable_index.json" << 'INDEXEOF'
{
  "plans": {
    "auth-primary.md": {
      "story_id": "STORY-100",
      "status": "completed",
      "created": "2025-01-01",
      "decision": "JWT authentication with OAuth2 flow. Authentication tokens are rotated every hour. Authentication service handles all auth requests.",
      "technical_approach": "Authentication middleware validates tokens. Authentication errors return 401.",
      "rationale": "Secure authentication is critical for user data protection.",
      "outcome": "Authentication system deployed.",
      "full_text": "JWT authentication OAuth2 tokens authentication service middleware validate 401"
    },
    "auth-secondary.md": {
      "story_id": "STORY-101",
      "status": "completed",
      "created": "2025-01-02",
      "decision": "Add MFA to existing authentication. Users can enable authentication app or SMS.",
      "technical_approach": "TOTP-based authentication verification.",
      "rationale": "Enhanced security for authentication.",
      "outcome": "MFA authentication available.",
      "full_text": "MFA authentication TOTP verification SMS security"
    },
    "database-design.md": {
      "story_id": "STORY-200",
      "status": "completed",
      "created": "2025-01-03",
      "decision": "PostgreSQL for ACID compliance. Database sharding for scale.",
      "technical_approach": "Database migrations via Flyway. Database backups daily.",
      "rationale": "Reliable database foundation.",
      "outcome": "Database operational.",
      "full_text": "PostgreSQL ACID database sharding Flyway migrations backups"
    },
    "caching-layer.md": {
      "story_id": "STORY-300",
      "status": "in_progress",
      "created": "2025-01-04",
      "decision": "Redis for caching and session storage. Cache authentication tokens.",
      "technical_approach": "Distributed cache with TTL policies.",
      "rationale": "Performance optimization via caching.",
      "outcome": "",
      "full_text": "Redis caching session storage authentication tokens TTL distributed"
    },
    "api-gateway.md": {
      "story_id": "STORY-400",
      "status": "draft",
      "created": "2025-01-05",
      "decision": "Kong API gateway for routing and rate limiting.",
      "technical_approach": "Gateway plugins for authentication and logging.",
      "rationale": "Centralized API management.",
      "outcome": "",
      "full_text": "Kong API gateway routing rate limiting authentication plugins"
    }
  },
  "keywords": {
    "authentication": ["auth-primary.md", "auth-secondary.md", "caching-layer.md", "api-gateway.md"],
    "database": ["database-design.md"],
    "postgresql": ["database-design.md"],
    "redis": ["caching-layer.md"],
    "caching": ["caching-layer.md"],
    "jwt": ["auth-primary.md"],
    "mfa": ["auth-secondary.md"],
    "api": ["api-gateway.md"],
    "gateway": ["api-gateway.md"],
    "oauth2": ["auth-primary.md"]
  },
  "keyword_counts": {
    "auth-primary.md": {"authentication": 6, "jwt": 1, "oauth2": 1, "tokens": 2},
    "auth-secondary.md": {"authentication": 4, "mfa": 1, "security": 1},
    "database-design.md": {"database": 3, "postgresql": 1, "flyway": 1},
    "caching-layer.md": {"caching": 2, "redis": 1, "authentication": 1, "tokens": 1},
    "api-gateway.md": {"api": 1, "gateway": 2, "authentication": 1, "routing": 1}
  }
}
INDEXEOF
}

cleanup_fixtures() {
    rm -rf "$TEST_FIXTURES_DIR"
}

# =============================================================================
# Test Cases for AC#3: Search by Keywords
# =============================================================================

test_search_by_keywords_function_exists() {
    echo ""
    echo "=== Test: search_by_keywords function exists ==="

    if type search_by_keywords &>/dev/null; then
        pass_test "Function search_by_keywords should exist in plan_file_kb.sh"
    else
        fail_test "Function search_by_keywords should exist in plan_file_kb.sh" \
            "Function 'search_by_keywords' does not exist"
    fi
}

test_search_by_keywords_returns_valid_json() {
    echo ""
    echo "=== Test: search_by_keywords returns valid JSON ==="

    if type search_by_keywords &>/dev/null; then
        local result
        result=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "authentication" 2>&1) || true

        if echo "$result" | grep -qE '^\{.*\}$'; then
            pass_test "Result should be valid JSON"
        else
            fail_test "Result should be valid JSON" "Invalid JSON structure"
        fi
    else
        fail_test "Result should be valid JSON" "Function search_by_keywords does not exist"
    fi
}

test_search_by_keywords_finds_matching_decisions() {
    echo ""
    echo "=== Test: search_by_keywords finds all matching decisions ==="

    if type search_by_keywords &>/dev/null; then
        local result
        result=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "authentication" 2>&1) || true

        # "authentication" appears in 4 plan files
        if echo "$result" | grep -q "auth-primary.md"; then
            pass_test "Result should contain auth-primary plan"
        else
            fail_test "Result should contain auth-primary plan" "auth-primary not found"
        fi

        if echo "$result" | grep -q "auth-secondary.md"; then
            pass_test "Result should contain auth-secondary plan"
        else
            fail_test "Result should contain auth-secondary plan" "auth-secondary not found"
        fi

        if echo "$result" | grep -q "caching-layer.md"; then
            pass_test "Result should contain caching-layer plan"
        else
            fail_test "Result should contain caching-layer plan" "caching-layer not found"
        fi

        if echo "$result" | grep -q "api-gateway.md"; then
            pass_test "Result should contain api-gateway plan"
        else
            fail_test "Result should contain api-gateway plan" "api-gateway not found"
        fi
    else
        fail_test "Result should contain auth-primary plan" "Function search_by_keywords does not exist"
        fail_test "Result should contain auth-secondary plan" "Function search_by_keywords does not exist"
        fail_test "Result should contain caching-layer plan" "Function search_by_keywords does not exist"
        fail_test "Result should contain api-gateway plan" "Function search_by_keywords does not exist"
    fi
}

test_search_by_keywords_includes_relevance_ranking() {
    echo ""
    echo "=== Test: search_by_keywords includes relevance ranking ==="

    if type search_by_keywords &>/dev/null; then
        local result
        result=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "authentication" 2>&1) || true

        # Check for relevance/score field (accepts relevance_score, relevance, score, or rank)
        if echo "$result" | grep -qE '"relevance_score"|"relevance"|"score"|"rank"'; then
            pass_test "Result should include relevance/score field"
        else
            fail_test "Result should include relevance/score field" "No relevance field found"
        fi
    else
        fail_test "Result should include relevance/score field" "Function search_by_keywords does not exist"
    fi
}

test_search_by_keywords_ranks_by_frequency() {
    echo ""
    echo "=== Test: search_by_keywords ranks higher-frequency matches first ==="

    if type search_by_keywords &>/dev/null; then
        local result
        result=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "authentication" 2>&1) || true

        # auth-primary.md has "authentication" 6 times, should rank highest
        # Check if results are ordered (auth-primary should appear first)
        local first_match
        first_match=$(echo "$result" | grep -oE 'auth-[a-z]+\.md' | head -1)

        if [[ "$first_match" == "auth-primary.md" ]]; then
            pass_test "Highest frequency match should rank first"
        else
            fail_test "Highest frequency match should rank first" "First match was: $first_match"
        fi
    else
        fail_test "Highest frequency match should rank first" "Function search_by_keywords does not exist"
    fi
}

test_search_by_keywords_multiple_keywords() {
    echo ""
    echo "=== Test: search_by_keywords supports multiple keywords ==="

    if type search_by_keywords &>/dev/null; then
        local result
        result=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "authentication tokens" 2>&1) || true

        # Plans with both keywords should rank higher
        if echo "$result" | grep -q "auth-primary.md"; then
            pass_test "Multiple keyword search finds matching plans"
        else
            fail_test "Multiple keyword search finds matching plans" "No matches found"
        fi

        if echo "$result" | grep -q "caching-layer.md"; then
            pass_test "Multiple keyword search finds all relevant plans"
        else
            fail_test "Multiple keyword search finds all relevant plans" "caching-layer not found"
        fi
    else
        fail_test "Multiple keyword search finds matching plans" "Function search_by_keywords does not exist"
        fail_test "Multiple keyword search finds all relevant plans" "Function search_by_keywords does not exist"
    fi
}

test_search_by_keywords_returns_count() {
    echo ""
    echo "=== Test: search_by_keywords returns match count ==="

    if type search_by_keywords &>/dev/null; then
        local result
        result=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "database" 2>&1) || true

        if echo "$result" | grep -qE '"count"[[:space:]]*:[[:space:]]*1'; then
            pass_test "Result should show count of 1 for 'database' keyword"
        else
            fail_test "Result should show count of 1 for 'database' keyword" "count field incorrect"
        fi
    else
        fail_test "Result should show count of 1 for 'database' keyword" "Function search_by_keywords does not exist"
    fi
}

test_search_by_keywords_case_insensitive() {
    echo ""
    echo "=== Test: search_by_keywords is case-insensitive ==="

    if type search_by_keywords &>/dev/null; then
        local result_lower result_upper result_mixed
        result_lower=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "redis" 2>&1) || true
        result_upper=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "REDIS" 2>&1) || true
        result_mixed=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "Redis" 2>&1) || true

        # All variants should find the same plan
        if echo "$result_lower" | grep -q "caching-layer.md" && \
           echo "$result_upper" | grep -q "caching-layer.md" && \
           echo "$result_mixed" | grep -q "caching-layer.md"; then
            pass_test "Search should be case-insensitive"
        else
            fail_test "Search should be case-insensitive" "Case variants produced different results"
        fi
    else
        fail_test "Search should be case-insensitive" "Function search_by_keywords does not exist"
    fi
}

test_search_by_keywords_empty_for_no_matches() {
    echo ""
    echo "=== Test: search_by_keywords returns empty for no matches ==="

    if type search_by_keywords &>/dev/null; then
        local result
        result=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "nonexistentkeyword123" 2>&1) || true

        if echo "$result" | grep -qE '"count"[[:space:]]*:[[:space:]]*0|"matches"[[:space:]]*:[[:space:]]*\[\]'; then
            pass_test "Returns empty/zero for no keyword matches"
        else
            fail_test "Returns empty/zero for no keyword matches" "Non-empty result returned"
        fi
    else
        fail_test "Returns empty/zero for no keyword matches" "Function search_by_keywords does not exist"
    fi
}

test_search_by_keywords_handles_empty_query() {
    echo ""
    echo "=== Test: search_by_keywords handles empty query ==="

    if type search_by_keywords &>/dev/null; then
        local result
        result=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "" 2>&1) || true

        if echo "$result" | grep -qiE 'error|"count"[[:space:]]*:[[:space:]]*0'; then
            pass_test "Handles empty query appropriately"
        else
            fail_test "Handles empty query appropriately" "Invalid response"
        fi
    else
        fail_test "Handles empty query appropriately" "Function search_by_keywords does not exist"
    fi
}

test_search_by_keywords_handles_missing_index() {
    echo ""
    echo "=== Test: search_by_keywords handles missing index directory ==="

    if type search_by_keywords &>/dev/null; then
        local result
        result=$(search_by_keywords "$TEST_FIXTURES_DIR/nonexistent" "authentication" 2>&1) || true

        if echo "$result" | grep -qi "error"; then
            pass_test "Returns error for missing index directory"
        else
            fail_test "Returns error for missing index directory" "No error reported"
        fi
    else
        fail_test "Returns error for missing index directory" "Function search_by_keywords does not exist"
    fi
}

test_search_by_keywords_includes_query_in_response() {
    echo ""
    echo "=== Test: search_by_keywords includes query in response ==="

    if type search_by_keywords &>/dev/null; then
        local result
        result=$(search_by_keywords "$TEST_FIXTURES_DIR/index" "database" 2>&1) || true

        if echo "$result" | grep -qE '"query"|"keywords"'; then
            pass_test "Response should include query/keywords field"
        else
            fail_test "Response should include query/keywords field" "query field not found"
        fi
    else
        fail_test "Response should include query/keywords field" "Function search_by_keywords does not exist"
    fi
}

# =============================================================================
# Main Test Runner
# =============================================================================
main() {
    echo "=============================================="
    echo "STORY-233 AC#3: Search by Keywords Tests"
    echo "TDD RED PHASE - Tests expected to FAIL"
    echo "=============================================="
    echo ""

    # Setup
    setup_fixtures

    # Run tests
    test_search_by_keywords_function_exists
    test_search_by_keywords_returns_valid_json
    test_search_by_keywords_finds_matching_decisions
    test_search_by_keywords_includes_relevance_ranking
    test_search_by_keywords_ranks_by_frequency
    test_search_by_keywords_multiple_keywords
    test_search_by_keywords_returns_count
    test_search_by_keywords_case_insensitive
    test_search_by_keywords_empty_for_no_matches
    test_search_by_keywords_handles_empty_query
    test_search_by_keywords_handles_missing_index
    test_search_by_keywords_includes_query_in_response

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
