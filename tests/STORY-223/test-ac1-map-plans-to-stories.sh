#!/bin/bash
#
# Test: AC#1 - Map Plans to Stories to Artifacts
# Story: STORY-223 - Catalog Session File Structure and Relationships
#
# AC#1: Map Plans to Stories to Artifacts
#   Given: session data directories
#   When: session-miner catalogs files
#   Then: a mapping is created: plan files -> story references -> associated artifacts
#
# Technical Requirement: SM-020 - Catalog files across session directories
#
# Test Framework: Bash shell script with assertions
# Status: FAILING (TDD Red Phase - no implementation exists yet)
#

set -euo pipefail

# Source the shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

# Source the session catalog functions (expected implementation)
# This will fail until the implementation exists
source "$SCRIPT_DIR/../../.claude/scripts/session_catalog.sh" 2>/dev/null || true

# Create temporary test directory
TEST_TEMP_DIR="/tmp/test-story-223-ac1-$$"
mkdir -p "$TEST_TEMP_DIR"
trap "rm -rf $TEST_TEMP_DIR" EXIT

# ============================================================================
# Test 1: Catalog function exists
# ============================================================================
test_catalog_function_should_exist() {
    echo "--- Test 1: catalog_session_files function should exist ---"

    # Act & Assert: Function should be defined
    assert_function_exists "catalog_session_files" \
        "catalog_session_files function should be defined in session_catalog.sh"
}

# ============================================================================
# Test 2: Map plan files to story references
# ============================================================================
test_should_map_plan_files_to_story_references() {
    echo "--- Test 2: Map plan files to story references ---"

    # Arrange: Create mock session data structure
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test2")

    # Create mock plan files with story references
    create_mock_plan_file "$test_dir/plans" "PLAN-001" "STORY-100,STORY-101"
    create_mock_plan_file "$test_dir/plans" "PLAN-002" "STORY-102"
    create_mock_plan_file "$test_dir/plans" "PLAN-003" "STORY-100,STORY-103,STORY-104"

    # Act: Call catalog function (STUB - function doesn't exist yet)
    local result="{}"
    if declare -f catalog_session_files &> /dev/null; then
        result=$(catalog_session_files "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Result should contain mapping structure
    assert_json_has_field "$result" "plan_to_story_map" \
        "Result should contain plan_to_story_map field"

    # Assert: PLAN-001 should map to STORY-100 and STORY-101
    if echo "$result" | grep -q '"PLAN-001"'; then
        assert_contains "$result" "STORY-100" \
            "PLAN-001 should reference STORY-100"
        assert_contains "$result" "STORY-101" \
            "PLAN-001 should reference STORY-101"
    else
        assert_equal "PLAN-001_EXISTS" "MISSING" \
            "PLAN-001 should be in the plan_to_story_map"
    fi
}

# ============================================================================
# Test 3: Map story references to associated artifacts
# ============================================================================
test_should_map_stories_to_artifacts() {
    echo "--- Test 3: Map story references to associated artifacts ---"

    # Arrange: Create mock session data with artifacts
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test3")

    # Create mock plan file
    create_mock_plan_file "$test_dir/plans" "PLAN-001" "STORY-200"

    # Create mock artifacts associated with STORY-200
    mkdir -p "$test_dir/artifacts/STORY-200"
    echo "Test artifact 1" > "$test_dir/artifacts/STORY-200/test-results.json"
    echo "Test artifact 2" > "$test_dir/artifacts/STORY-200/coverage-report.html"

    # Act: Call catalog function
    local result="{}"
    if declare -f catalog_session_files &> /dev/null; then
        result=$(catalog_session_files "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Result should contain story_to_artifacts_map
    assert_json_has_field "$result" "story_to_artifacts_map" \
        "Result should contain story_to_artifacts_map field"

    # Assert: STORY-200 should have associated artifacts
    if echo "$result" | grep -q '"STORY-200"'; then
        assert_contains "$result" "test-results.json" \
            "STORY-200 should be associated with test-results.json artifact"
    else
        assert_equal "STORY-200_EXISTS" "MISSING" \
            "STORY-200 should be in the story_to_artifacts_map"
    fi
}

# ============================================================================
# Test 4: Complete mapping chain (plan -> story -> artifact)
# ============================================================================
test_should_create_complete_mapping_chain() {
    echo "--- Test 4: Complete mapping chain (plan -> story -> artifact) ---"

    # Arrange: Create complete mock session data
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test4")

    # Create plan with story references
    create_mock_plan_file "$test_dir/plans" "PLAN-COMPLETE" "STORY-300,STORY-301"

    # Create artifacts for referenced stories
    mkdir -p "$test_dir/artifacts/STORY-300"
    echo "Artifact for 300" > "$test_dir/artifacts/STORY-300/qa-report.md"

    mkdir -p "$test_dir/artifacts/STORY-301"
    echo "Artifact for 301" > "$test_dir/artifacts/STORY-301/dev-output.log"

    # Act: Call catalog function
    local result="{}"
    if declare -f catalog_session_files &> /dev/null; then
        result=$(catalog_session_files "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Complete chain should be traceable
    # 1. Plan to Story mapping exists
    assert_json_has_field "$result" "plan_to_story_map" \
        "Complete chain: plan_to_story_map should exist"

    # 2. Story to Artifact mapping exists
    assert_json_has_field "$result" "story_to_artifacts_map" \
        "Complete chain: story_to_artifacts_map should exist"

    # 3. Catalog metadata exists
    assert_json_has_field "$result" "files" \
        "Complete chain: files catalog should exist"
}

# ============================================================================
# Test 5: Handle empty session directories
# ============================================================================
test_should_handle_empty_directories() {
    echo "--- Test 5: Handle empty session directories ---"

    # Arrange: Create empty session structure
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test5")
    # Directories are empty - no files

    # Act: Call catalog function
    local result="{}"
    if declare -f catalog_session_files &> /dev/null; then
        result=$(catalog_session_files "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Should return valid structure with empty mappings
    assert_json_has_field "$result" "plan_to_story_map" \
        "Empty directories: should still return plan_to_story_map field"

    # Assert: files array should be empty or contain no entries
    if echo "$result" | grep -q '"files"\s*:\s*\[\]'; then
        assert_equal "true" "true" "Empty directories: files array should be empty"
    else
        assert_equal "EMPTY_ARRAY" "NOT_EMPTY" \
            "Empty directories: files array should be empty"
    fi
}

# ============================================================================
# Test 6: Catalog multiple plan files with overlapping story references
# ============================================================================
test_should_handle_overlapping_story_references() {
    echo "--- Test 6: Handle overlapping story references ---"

    # Arrange: Create plans with overlapping story references
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test6")

    # PLAN-A references STORY-400, STORY-401
    create_mock_plan_file "$test_dir/plans" "PLAN-A" "STORY-400,STORY-401"

    # PLAN-B also references STORY-401 (overlap) plus STORY-402
    create_mock_plan_file "$test_dir/plans" "PLAN-B" "STORY-401,STORY-402"

    # Act: Call catalog function
    local result="{}"
    if declare -f catalog_session_files &> /dev/null; then
        result=$(catalog_session_files "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Both plans should be cataloged
    if echo "$result" | grep -q '"PLAN-A"' && echo "$result" | grep -q '"PLAN-B"'; then
        assert_equal "true" "true" "Both PLAN-A and PLAN-B should be cataloged"
    else
        assert_equal "BOTH_PLANS" "MISSING" \
            "Both PLAN-A and PLAN-B should be present in catalog"
    fi

    # Assert: STORY-401 should be referenced by multiple plans
    # (Implementation should track reverse mapping)
    if echo "$result" | grep -q '"story_to_plans_map"'; then
        assert_contains "$result" "STORY-401" \
            "STORY-401 should appear in story_to_plans_map with multiple plan references"
    else
        assert_equal "story_to_plans_map" "MISSING" \
            "Catalog should include story_to_plans_map for reverse lookups"
    fi
}

# ============================================================================
# Test 7: Catalog FileEntry data model fields
# ============================================================================
test_should_populate_file_entry_fields() {
    echo "--- Test 7: Populate FileEntry data model fields ---"

    # Arrange: Create a session data directory with a plan file
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test7")
    create_mock_plan_file "$test_dir/plans" "PLAN-FILE-TEST" "STORY-500"

    # Act: Call catalog function
    local result="{}"
    if declare -f catalog_session_files &> /dev/null; then
        result=$(catalog_session_files "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: FileEntry structure should contain required fields per Tech Spec
    # DataModel SessionCatalog has: files: FileEntry[]
    if echo "$result" | grep -q '"files"'; then
        # Check for expected FileEntry fields
        assert_json_has_field "$result" "path" \
            "FileEntry should have 'path' field"
        assert_json_has_field "$result" "type" \
            "FileEntry should have 'type' field (plan/session/artifact)"
    else
        assert_equal "FILES_ARRAY" "MISSING" \
            "Catalog should contain files array with FileEntry objects"
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: AC#1 - Map Plans to Stories to Artifacts"
echo "Story: STORY-223 - Catalog Session File Structure and Relationships"
echo "Technical Requirement: SM-020 - Catalog files across session directories"
echo "========================================================================"
echo ""

test_catalog_function_should_exist
echo ""

test_should_map_plan_files_to_story_references
echo ""

test_should_map_stories_to_artifacts
echo ""

test_should_create_complete_mapping_chain
echo ""

test_should_handle_empty_directories
echo ""

test_should_handle_overlapping_story_references
echo ""

test_should_populate_file_entry_fields
echo ""

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "AC#1 Test Results"
exit_with_result
