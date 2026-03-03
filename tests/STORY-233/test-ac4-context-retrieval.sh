#!/bin/bash
# STORY-233: Test AC#4 - Context Retrieval
# Test that retrieve_decision_context() returns decision text, rationale, and outcome
#
# TDD RED PHASE: These tests should FAIL because the functions don't exist yet
#
# Expected Functions (to be implemented in plan_file_kb.sh):
#   - retrieve_decision_context(index_dir, plan_file) - Get full decision context
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

    # Create a comprehensive index with all context fields
    cat > "$TEST_FIXTURES_DIR/index/searchable_index.json" << 'INDEXEOF'
{
  "plans": {
    "complete-context.md": {
      "story_id": "STORY-100",
      "status": "completed",
      "created": "2025-01-01",
      "decision": "Implement JWT authentication with OAuth2 flow for secure user authentication across microservices.",
      "technical_approach": "1. Create authentication service 2. Implement token generation 3. Add middleware validation 4. Setup refresh token rotation",
      "rationale": "JWT provides stateless authentication suitable for distributed systems. OAuth2 is industry standard for authorization. Refresh tokens improve security without impacting UX.",
      "outcome": "Successfully deployed to production. Authentication latency <50ms. Zero security incidents in first month. User feedback positive on SSO experience."
    },
    "partial-context.md": {
      "story_id": "STORY-200",
      "status": "in_progress",
      "created": "2025-01-02",
      "decision": "Use PostgreSQL with read replicas for database layer.",
      "technical_approach": "1. Configure master database 2. Setup streaming replication 3. Add connection pooling",
      "rationale": "PostgreSQL offers ACID compliance and excellent performance for our read-heavy workload.",
      "outcome": ""
    },
    "minimal-context.md": {
      "story_id": "STORY-300",
      "status": "draft",
      "created": "2025-01-03",
      "decision": "Evaluate caching strategies for performance optimization.",
      "technical_approach": "",
      "rationale": "",
      "outcome": ""
    }
  }
}
INDEXEOF
}

cleanup_fixtures() {
    rm -rf "$TEST_FIXTURES_DIR"
}

# =============================================================================
# Test Cases for AC#4: Context Retrieval
# =============================================================================

test_retrieve_decision_context_function_exists() {
    echo ""
    echo "=== Test: retrieve_decision_context function exists ==="

    if type retrieve_decision_context &>/dev/null; then
        pass_test "Function retrieve_decision_context should exist in plan_file_kb.sh"
    else
        fail_test "Function retrieve_decision_context should exist in plan_file_kb.sh" \
            "Function 'retrieve_decision_context' does not exist"
    fi
}

test_retrieve_decision_context_returns_valid_json() {
    echo ""
    echo "=== Test: retrieve_decision_context returns valid JSON ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/index" "complete-context.md" 2>&1) || true

        if echo "$result" | grep -qE '^\{.*\}$'; then
            pass_test "Result should be valid JSON"
        else
            fail_test "Result should be valid JSON" "Invalid JSON structure"
        fi
    else
        fail_test "Result should be valid JSON" "Function retrieve_decision_context does not exist"
    fi
}

test_retrieve_decision_context_includes_decision_text() {
    echo ""
    echo "=== Test: retrieve_decision_context includes decision text ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/index" "complete-context.md" 2>&1) || true

        if echo "$result" | grep -q '"decision"'; then
            pass_test "Result should have 'decision' field"
        else
            fail_test "Result should have 'decision' field" "decision field not found"
        fi

        if echo "$result" | grep -q "JWT authentication"; then
            pass_test "Decision text should contain actual content"
        else
            fail_test "Decision text should contain actual content" "decision content not found"
        fi
    else
        fail_test "Result should have 'decision' field" "Function retrieve_decision_context does not exist"
        fail_test "Decision text should contain actual content" "Function retrieve_decision_context does not exist"
    fi
}

test_retrieve_decision_context_includes_rationale() {
    echo ""
    echo "=== Test: retrieve_decision_context includes rationale ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/index" "complete-context.md" 2>&1) || true

        if echo "$result" | grep -q '"rationale"'; then
            pass_test "Result should have 'rationale' field"
        else
            fail_test "Result should have 'rationale' field" "rationale field not found"
        fi

        if echo "$result" | grep -q "stateless authentication"; then
            pass_test "Rationale should contain actual reasoning"
        else
            fail_test "Rationale should contain actual reasoning" "rationale content not found"
        fi
    else
        fail_test "Result should have 'rationale' field" "Function retrieve_decision_context does not exist"
        fail_test "Rationale should contain actual reasoning" "Function retrieve_decision_context does not exist"
    fi
}

test_retrieve_decision_context_includes_outcome() {
    echo ""
    echo "=== Test: retrieve_decision_context includes outcome ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/index" "complete-context.md" 2>&1) || true

        if echo "$result" | grep -q '"outcome"'; then
            pass_test "Result should have 'outcome' field"
        else
            fail_test "Result should have 'outcome' field" "outcome field not found"
        fi

        if echo "$result" | grep -q "Successfully deployed"; then
            pass_test "Outcome should contain deployment results"
        else
            fail_test "Outcome should contain deployment results" "outcome content not found"
        fi

        if echo "$result" | grep -q "Zero security incidents"; then
            pass_test "Outcome should contain metrics"
        else
            fail_test "Outcome should contain metrics" "metrics not found in outcome"
        fi
    else
        fail_test "Result should have 'outcome' field" "Function retrieve_decision_context does not exist"
        fail_test "Outcome should contain deployment results" "Function retrieve_decision_context does not exist"
        fail_test "Outcome should contain metrics" "Function retrieve_decision_context does not exist"
    fi
}

test_retrieve_decision_context_includes_technical_approach() {
    echo ""
    echo "=== Test: retrieve_decision_context includes technical approach ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/index" "complete-context.md" 2>&1) || true

        if echo "$result" | grep -q '"technical_approach"'; then
            pass_test "Result should have 'technical_approach' field"
        else
            fail_test "Result should have 'technical_approach' field" "technical_approach field not found"
        fi

        if echo "$result" | grep -q "token generation"; then
            pass_test "Technical approach should contain implementation steps"
        else
            fail_test "Technical approach should contain implementation steps" "steps not found"
        fi
    else
        fail_test "Result should have 'technical_approach' field" "Function retrieve_decision_context does not exist"
        fail_test "Technical approach should contain implementation steps" "Function retrieve_decision_context does not exist"
    fi
}

test_retrieve_decision_context_includes_metadata() {
    echo ""
    echo "=== Test: retrieve_decision_context includes metadata ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/index" "complete-context.md" 2>&1) || true

        if echo "$result" | grep -q '"story_id"'; then
            pass_test "Result should have 'story_id' field"
        else
            fail_test "Result should have 'story_id' field" "story_id field not found"
        fi

        if echo "$result" | grep -q '"status"'; then
            pass_test "Result should have 'status' field"
        else
            fail_test "Result should have 'status' field" "status field not found"
        fi

        if echo "$result" | grep -q '"created"'; then
            pass_test "Result should have 'created' field"
        else
            fail_test "Result should have 'created' field" "created field not found"
        fi
    else
        fail_test "Result should have 'story_id' field" "Function retrieve_decision_context does not exist"
        fail_test "Result should have 'status' field" "Function retrieve_decision_context does not exist"
        fail_test "Result should have 'created' field" "Function retrieve_decision_context does not exist"
    fi
}

test_retrieve_decision_context_handles_partial_context() {
    echo ""
    echo "=== Test: retrieve_decision_context handles partial context ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/index" "partial-context.md" 2>&1) || true

        # Should still return valid JSON even with empty outcome
        if echo "$result" | grep -qE '^\{.*\}$'; then
            pass_test "Returns valid JSON for partial context"
        else
            fail_test "Returns valid JSON for partial context" "Invalid JSON"
        fi

        if echo "$result" | grep -q '"outcome"'; then
            pass_test "Includes outcome field even when empty"
        else
            fail_test "Includes outcome field even when empty" "outcome field missing"
        fi
    else
        fail_test "Returns valid JSON for partial context" "Function retrieve_decision_context does not exist"
        fail_test "Includes outcome field even when empty" "Function retrieve_decision_context does not exist"
    fi
}

test_retrieve_decision_context_handles_minimal_context() {
    echo ""
    echo "=== Test: retrieve_decision_context handles minimal context ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/index" "minimal-context.md" 2>&1) || true

        # Should handle plan with only decision (no rationale/outcome/approach)
        if echo "$result" | grep -q "caching strategies"; then
            pass_test "Returns decision for minimal context"
        else
            fail_test "Returns decision for minimal context" "decision not found"
        fi

        # Empty fields should be present but empty
        if echo "$result" | grep -qE '"rationale"[[:space:]]*:[[:space:]]*""'; then
            pass_test "Empty rationale returns empty string"
        else
            fail_test "Empty rationale returns empty string" "rationale field incorrect"
        fi
    else
        fail_test "Returns decision for minimal context" "Function retrieve_decision_context does not exist"
        fail_test "Empty rationale returns empty string" "Function retrieve_decision_context does not exist"
    fi
}

test_retrieve_decision_context_handles_nonexistent_plan() {
    echo ""
    echo "=== Test: retrieve_decision_context handles nonexistent plan file ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/index" "nonexistent.md" 2>&1) || true

        if echo "$result" | grep -qi "error"; then
            pass_test "Returns error for nonexistent plan file"
        else
            fail_test "Returns error for nonexistent plan file" "No error reported"
        fi
    else
        fail_test "Returns error for nonexistent plan file" "Function retrieve_decision_context does not exist"
    fi
}

test_retrieve_decision_context_handles_missing_index() {
    echo ""
    echo "=== Test: retrieve_decision_context handles missing index directory ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/nonexistent" "complete-context.md" 2>&1) || true

        if echo "$result" | grep -qi "error"; then
            pass_test "Returns error for missing index directory"
        else
            fail_test "Returns error for missing index directory" "No error reported"
        fi
    else
        fail_test "Returns error for missing index directory" "Function retrieve_decision_context does not exist"
    fi
}

test_retrieve_decision_context_includes_plan_filename() {
    echo ""
    echo "=== Test: retrieve_decision_context includes plan filename in response ==="

    if type retrieve_decision_context &>/dev/null; then
        local result
        result=$(retrieve_decision_context "$TEST_FIXTURES_DIR/index" "complete-context.md" 2>&1) || true

        if echo "$result" | grep -qE '"plan_file"|"filename"'; then
            pass_test "Response should include plan filename"
        else
            fail_test "Response should include plan filename" "plan_file/filename field not found"
        fi
    else
        fail_test "Response should include plan filename" "Function retrieve_decision_context does not exist"
    fi
}

# =============================================================================
# Main Test Runner
# =============================================================================
main() {
    echo "=============================================="
    echo "STORY-233 AC#4: Context Retrieval Tests"
    echo "TDD RED PHASE - Tests expected to FAIL"
    echo "=============================================="
    echo ""

    # Setup
    setup_fixtures

    # Run tests
    test_retrieve_decision_context_function_exists
    test_retrieve_decision_context_returns_valid_json
    test_retrieve_decision_context_includes_decision_text
    test_retrieve_decision_context_includes_rationale
    test_retrieve_decision_context_includes_outcome
    test_retrieve_decision_context_includes_technical_approach
    test_retrieve_decision_context_includes_metadata
    test_retrieve_decision_context_handles_partial_context
    test_retrieve_decision_context_handles_minimal_context
    test_retrieve_decision_context_handles_nonexistent_plan
    test_retrieve_decision_context_handles_missing_index
    test_retrieve_decision_context_includes_plan_filename

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
