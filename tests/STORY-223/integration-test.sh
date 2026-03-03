#!/bin/bash
#
# Integration Test: Cross-Component Validation for STORY-223
# Tests that all 3 main functions work together correctly
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"
source "$SCRIPT_DIR/../../.claude/scripts/session_catalog.sh"

TEST_TEMP_DIR="/tmp/integration-test-story-223-$$"
mkdir -p "$TEST_TEMP_DIR"
trap "rm -rf $TEST_TEMP_DIR" EXIT

echo "========================================================================"
echo "Integration Test: Cross-Component Validation for STORY-223"
echo "========================================================================"
echo ""

# ============================================================================
# Integration Test 1: All 3 functions work on same directory
# ============================================================================
test_all_functions_on_same_directory() {
    echo "--- Integration Test 1: All 3 functions work on same directory ---"

    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/integration1")

    # Create plan files
    create_mock_plan_file "$test_dir/plans" "PLAN-INT-001" "STORY-INT-100,STORY-INT-101"
    create_mock_plan_file "$test_dir/plans" "PLAN-INT-002" "STORY-INT-100"

    # Create session chain
    create_mock_session_file "$test_dir/sessions" "session-root-int"
    create_mock_session_file "$test_dir/sessions" "session-child-int" "session-root-int"

    # Create artifacts
    mkdir -p "$test_dir/artifacts/STORY-INT-100"
    echo '{"result": "pass"}' > "$test_dir/artifacts/STORY-INT-100/test-output.json"

    # Run all 3 functions
    local catalog_result dep_result chain_result

    catalog_result=$(catalog_session_files "$test_dir")
    dep_result=$(build_dependency_graph "$test_dir")
    chain_result=$(track_session_chains "$test_dir/sessions")

    # Validate catalog result
    assert_json_has_field "$catalog_result" "plan_to_story_map" \
        "catalog_session_files: plan_to_story_map exists"
    assert_json_has_field "$catalog_result" "story_to_artifacts_map" \
        "catalog_session_files: story_to_artifacts_map exists"
    assert_json_has_field "$catalog_result" "files" \
        "catalog_session_files: files exists"

    # Validate dependency graph result
    assert_json_has_field "$dep_result" "dependencies" \
        "build_dependency_graph: dependencies exists"
    assert_json_has_field "$dep_result" "nodes" \
        "build_dependency_graph: nodes exists"

    # Validate session chains result
    assert_json_has_field "$chain_result" "session_chains" \
        "track_session_chains: session_chains exists"
    assert_json_has_field "$chain_result" "root_sessions" \
        "track_session_chains: root_sessions exists"

    echo ""
}

# ============================================================================
# Integration Test 2: Helper functions are exported and accessible
# ============================================================================
test_helper_functions_exported() {
    echo "--- Integration Test 2: Helper functions are exported and accessible ---"

    assert_function_exists "find_files_into_array" \
        "Helper: find_files_into_array is exported"
    assert_function_exists "classify_file_type" \
        "Helper: classify_file_type is exported"
    assert_function_exists "build_json_array" \
        "Helper: build_json_array is exported"

    # Test classify_file_type functionality
    local file_type
    file_type=$(classify_file_type "/path/to/plans/my-plan.md")
    assert_equal "plan" "$file_type" "classify_file_type: plans directory returns 'plan'"

    file_type=$(classify_file_type "/path/to/sessions/session.json")
    assert_equal "session" "$file_type" "classify_file_type: sessions directory returns 'session'"

    file_type=$(classify_file_type "/path/to/artifacts/output.json")
    assert_equal "artifact" "$file_type" "classify_file_type: artifacts directory returns 'artifact'"

    # Test build_json_array functionality
    local json_arr
    json_arr=$(build_json_array "item1" "item2" "item3")
    assert_contains "$json_arr" '"item1"' "build_json_array: contains item1"
    assert_contains "$json_arr" '"item2"' "build_json_array: contains item2"

    echo ""
}

# ============================================================================
# Integration Test 3: JSON output is valid and parseable
# ============================================================================
test_json_output_valid() {
    echo "--- Integration Test 3: JSON output is valid and parseable ---"

    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/integration3")

    create_mock_plan_file "$test_dir/plans" "JSON-TEST-PLAN" "STORY-JSON-100"
    create_mock_session_file "$test_dir/sessions" "json-test-session"

    # Test catalog_session_files JSON validity
    local catalog_result
    catalog_result=$(catalog_session_files "$test_dir")
    if echo "$catalog_result" | jq . > /dev/null 2>&1; then
        assert_equal "true" "true" "catalog_session_files: output is valid JSON"
    else
        assert_equal "VALID_JSON" "INVALID_JSON" "catalog_session_files: output should be valid JSON"
    fi

    # Test build_dependency_graph JSON validity
    local dep_result
    dep_result=$(build_dependency_graph "$test_dir")
    if echo "$dep_result" | jq . > /dev/null 2>&1; then
        assert_equal "true" "true" "build_dependency_graph: output is valid JSON"
    else
        assert_equal "VALID_JSON" "INVALID_JSON" "build_dependency_graph: output should be valid JSON"
    fi

    # Test track_session_chains JSON validity
    local chain_result
    chain_result=$(track_session_chains "$test_dir/sessions")
    if echo "$chain_result" | jq . > /dev/null 2>&1; then
        assert_equal "true" "true" "track_session_chains: output is valid JSON"
    else
        assert_equal "VALID_JSON" "INVALID_JSON" "track_session_chains: output should be valid JSON"
    fi

    echo ""
}

# ============================================================================
# Integration Test 4: Functions handle edge cases consistently
# ============================================================================
test_edge_cases_consistent() {
    echo "--- Integration Test 4: Edge cases handled consistently across functions ---"

    # Test empty directories
    local empty_dir
    empty_dir=$(create_test_session_dir "$TEST_TEMP_DIR/integration4_empty")

    local catalog_empty dep_empty chain_empty
    catalog_empty=$(catalog_session_files "$empty_dir")
    dep_empty=$(build_dependency_graph "$empty_dir")
    chain_empty=$(track_session_chains "$empty_dir/sessions")

    # All should return valid JSON for empty directories
    if echo "$catalog_empty" | jq . > /dev/null 2>&1; then
        assert_equal "true" "true" "Empty directory: catalog_session_files returns valid JSON"
    else
        assert_equal "VALID_JSON" "INVALID" "Empty directory: catalog_session_files should return valid JSON"
    fi

    if echo "$dep_empty" | jq . > /dev/null 2>&1; then
        assert_equal "true" "true" "Empty directory: build_dependency_graph returns valid JSON"
    else
        assert_equal "VALID_JSON" "INVALID" "Empty directory: build_dependency_graph should return valid JSON"
    fi

    if echo "$chain_empty" | jq . > /dev/null 2>&1; then
        assert_equal "true" "true" "Empty directory: track_session_chains returns valid JSON"
    else
        assert_equal "VALID_JSON" "INVALID" "Empty directory: track_session_chains should return valid JSON"
    fi

    # Test orphan handling
    local orphan_dir
    orphan_dir=$(create_test_session_dir "$TEST_TEMP_DIR/integration4_orphan")

    # Create orphan session (parent doesn't exist)
    create_mock_session_file "$orphan_dir/sessions" "orphan-integration" "missing-parent"

    local chain_orphan
    chain_orphan=$(track_session_chains "$orphan_dir/sessions")

    assert_json_has_field "$chain_orphan" "orphan_sessions" \
        "Orphan handling: orphan_sessions field present"
    assert_contains "$chain_orphan" "orphan-integration" \
        "Orphan handling: orphan session is cataloged"

    echo ""
}

# ============================================================================
# Integration Test 5: Data flows correctly between function outputs
# ============================================================================
test_data_flow_consistency() {
    echo "--- Integration Test 5: Data flows correctly between function outputs ---"

    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/integration5")

    # Create interconnected data
    create_mock_plan_file "$test_dir/plans" "FLOW-PLAN" "STORY-FLOW-100"
    create_mock_session_file "$test_dir/sessions" "flow-session"
    mkdir -p "$test_dir/artifacts/STORY-FLOW-100"
    echo '{"flow": "test"}' > "$test_dir/artifacts/STORY-FLOW-100/artifact.json"

    # Get results from all functions
    local catalog_result dep_result
    catalog_result=$(catalog_session_files "$test_dir")
    dep_result=$(build_dependency_graph "$test_dir")

    # Files cataloged should appear in dependency graph nodes
    local catalog_file_count dep_node_count
    catalog_file_count=$(echo "$catalog_result" | jq '.files | length')
    dep_node_count=$(echo "$dep_result" | jq '.nodes | keys | length')

    # Dependency graph should have at least as many nodes as cataloged files
    # (may have more due to directory-level nodes)
    if [[ $dep_node_count -ge $catalog_file_count ]]; then
        assert_equal "true" "true" \
            "Data flow: dependency graph has >= cataloged files ($dep_node_count >= $catalog_file_count)"
    else
        assert_equal ">=$catalog_file_count" "$dep_node_count" \
            "Data flow: dependency graph should include all cataloged files"
    fi

    # PLAN-FLOW should appear in both outputs
    assert_contains "$catalog_result" "FLOW-PLAN" \
        "Data flow: FLOW-PLAN in catalog"
    assert_contains "$dep_result" "FLOW-PLAN" \
        "Data flow: FLOW-PLAN in dependency graph"

    echo ""
}

# ============================================================================
# Run all integration tests
# ============================================================================

test_all_functions_on_same_directory
test_helper_functions_exported
test_json_output_valid
test_edge_cases_consistent
test_data_flow_consistency

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "Integration Test Results"
exit_with_result
