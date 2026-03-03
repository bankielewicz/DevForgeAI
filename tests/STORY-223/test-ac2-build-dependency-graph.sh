#!/bin/bash
#
# Test: AC#2 - Build File Dependency Graph
# Story: STORY-223 - Catalog Session File Structure and Relationships
#
# AC#2: Build File Dependency Graph
#   Given: the cataloged files
#   When: analyzing dependencies
#   Then: a dependency graph shows which files reference or depend on others
#
# Technical Requirement: SM-021 - Build file dependency graph
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
TEST_TEMP_DIR="/tmp/test-story-223-ac2-$$"
mkdir -p "$TEST_TEMP_DIR"
trap "rm -rf $TEST_TEMP_DIR" EXIT

# ============================================================================
# Test 1: Dependency graph builder function exists
# ============================================================================
test_dependency_graph_function_should_exist() {
    echo "--- Test 1: build_dependency_graph function should exist ---"

    # Act & Assert: Function should be defined
    assert_function_exists "build_dependency_graph" \
        "build_dependency_graph function should be defined in session_catalog.sh"
}

# ============================================================================
# Test 2: Build dependency graph from cataloged files
# ============================================================================
test_should_build_dependency_graph_structure() {
    echo "--- Test 2: Build dependency graph from cataloged files ---"

    # Arrange: Create mock cataloged files
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test2")

    # Create plan file that references a story
    create_mock_plan_file "$test_dir/plans" "PLAN-GRAPH-001" "STORY-600"

    # Create artifact file referenced by the story
    mkdir -p "$test_dir/artifacts/STORY-600"
    echo '{"result": "pass"}' > "$test_dir/artifacts/STORY-600/test-output.json"

    # Act: Build dependency graph
    local result="{}"
    if declare -f build_dependency_graph &> /dev/null; then
        result=$(build_dependency_graph "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Result should contain dependencies array (per Tech Spec: DependencyEdge[])
    assert_json_has_field "$result" "dependencies" \
        "Result should contain 'dependencies' field (DependencyEdge[])"
}

# ============================================================================
# Test 3: DependencyEdge data model structure
# ============================================================================
test_should_contain_dependency_edge_fields() {
    echo "--- Test 3: DependencyEdge should have source and target fields ---"

    # Arrange: Create files with dependency relationship
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test3")

    # File A references File B
    create_mock_plan_file "$test_dir/plans" "FILE-A" "STORY-700"

    # File B (story file exists and is referenced)
    mkdir -p "$test_dir/stories"
    cat > "$test_dir/stories/STORY-700.md" << 'EOF'
---
id: STORY-700
title: Test Story
---
# Story 700
EOF

    # Act: Build dependency graph
    local result="{}"
    if declare -f build_dependency_graph &> /dev/null; then
        result=$(build_dependency_graph "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Each DependencyEdge should have source, target, type
    if echo "$result" | grep -q '"dependencies"'; then
        # Check for source field (the file that references)
        assert_json_has_field "$result" "source" \
            "DependencyEdge should have 'source' field"

        # Check for target field (the file being referenced)
        assert_json_has_field "$result" "target" \
            "DependencyEdge should have 'target' field"

        # Check for type field (reference, include, depends_on)
        assert_json_has_field "$result" "type" \
            "DependencyEdge should have 'type' field"
    else
        assert_equal "DEPENDENCIES_ARRAY" "MISSING" \
            "Result should contain dependencies array with DependencyEdge objects"
    fi
}

# ============================================================================
# Test 4: Detect file references within content
# ============================================================================
test_should_detect_file_references_in_content() {
    echo "--- Test 4: Detect file references within content ---"

    # Arrange: Create files that reference each other
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test4")

    # Create plan file that mentions another file in its content
    cat > "$test_dir/plans/referencing-plan.md" << 'EOF'
---
id: PLAN-REF
status: approved
---
# Plan Document

This plan references the following:
- See devforgeai/specs/Stories/STORY-800.story.md for requirements
- Implementation details in .claude/agents/session-miner.md
EOF

    # Create the referenced story file
    mkdir -p "$test_dir/specs/Stories"
    echo "# STORY-800" > "$test_dir/specs/Stories/STORY-800.story.md"

    # Act: Build dependency graph
    local result="{}"
    if declare -f build_dependency_graph &> /dev/null; then
        result=$(build_dependency_graph "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Graph should show referencing-plan.md depends on STORY-800.story.md
    # Note: Only detects references to files that exist in the graph
    if echo "$result" | grep -q '"dependencies"'; then
        assert_contains "$result" "STORY-800" \
            "Dependency graph should detect reference to STORY-800.story.md"
        # session-miner.md is referenced but doesn't exist in test dir, so won't be in graph
        # This is correct behavior - graph only contains existing files
        assert_contains "$result" "referencing-plan" \
            "Dependency graph should include the source file"
    else
        assert_equal "CONTENT_REFS" "NOT_DETECTED" \
            "Dependency graph should detect file references in content"
    fi
}

# ============================================================================
# Test 5: Handle circular dependencies gracefully
# ============================================================================
test_should_handle_circular_dependencies() {
    echo "--- Test 5: Handle circular dependencies gracefully ---"

    # Arrange: Create files with circular references (A -> B -> C -> A)
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test5")

    mkdir -p "$test_dir/docs"

    # File A references File B
    cat > "$test_dir/docs/file-a.md" << 'EOF'
# File A
References: file-b.md
EOF

    # File B references File C
    cat > "$test_dir/docs/file-b.md" << 'EOF'
# File B
References: file-c.md
EOF

    # File C references File A (circular!)
    cat > "$test_dir/docs/file-c.md" << 'EOF'
# File C
References: file-a.md
EOF

    # Act: Build dependency graph (should not hang or crash)
    local result="{}"
    local exit_code=0
    if declare -f build_dependency_graph &> /dev/null; then
        result=$(timeout 5 bash -c "build_dependency_graph '$test_dir'" 2>/dev/null) || exit_code=$?
    fi

    # Assert: Should complete without infinite loop
    if [[ $exit_code -eq 0 ]] || [[ -n "$result" ]]; then
        assert_equal "true" "true" "Circular dependency handling: should complete without hanging"
    else
        assert_equal "COMPLETED" "TIMEOUT_OR_ERROR" \
            "Dependency graph builder should handle circular references"
    fi

    # Assert: Should detect/report circular dependency
    if echo "$result" | grep -q '"circular_dependencies"' || echo "$result" | grep -q '"cycles"'; then
        assert_not_empty "true" "Circular dependencies should be detected and reported"
    else
        assert_equal "CIRCULAR_DETECTION" "NOT_IMPLEMENTED" \
            "Should detect and report circular dependencies"
    fi
}

# ============================================================================
# Test 6: Graph should include all file types
# ============================================================================
test_should_include_all_file_types_in_graph() {
    echo "--- Test 6: Graph should include plans, sessions, and artifacts ---"

    # Arrange: Create complete session structure with all file types
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test6")

    # Plan file
    create_mock_plan_file "$test_dir/plans" "PLAN-ALL-TYPES" "STORY-900"

    # Session file
    create_mock_session_file "$test_dir/sessions" "session-001" ""

    # Artifact file
    mkdir -p "$test_dir/artifacts/STORY-900"
    echo '{"coverage": 95}' > "$test_dir/artifacts/STORY-900/coverage.json"

    # Act: Build dependency graph
    local result="{}"
    if declare -f build_dependency_graph &> /dev/null; then
        result=$(build_dependency_graph "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Graph should contain nodes for each file type
    if echo "$result" | grep -q '"nodes"' || echo "$result" | grep -q '"files"'; then
        # Check plan file is included
        assert_contains "$result" "PLAN-ALL-TYPES" \
            "Graph should include plan files"

        # Check session file is included
        assert_contains "$result" "session-001" \
            "Graph should include session files"

        # Check artifact file is included
        assert_contains "$result" "coverage.json" \
            "Graph should include artifact files"
    else
        assert_equal "ALL_FILE_TYPES" "MISSING" \
            "Dependency graph should include all file types (plans, sessions, artifacts)"
    fi
}

# ============================================================================
# Test 7: Edge case - orphaned files (no dependencies)
# ============================================================================
test_should_handle_orphaned_files() {
    echo "--- Test 7: Handle orphaned files (files with no dependencies) ---"

    # Arrange: Create isolated file with no references
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test7")

    # Orphan file - references nothing and is not referenced
    cat > "$test_dir/plans/orphan-plan.md" << 'EOF'
---
id: ORPHAN-PLAN
status: draft
---
# Isolated Plan
This plan has no references to other files.
EOF

    # Act: Build dependency graph
    local result="{}"
    if declare -f build_dependency_graph &> /dev/null; then
        result=$(build_dependency_graph "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Orphan file should still appear in catalog/nodes (just with no edges)
    # Note: File ID is the filename (orphan-plan.md), not the YAML id
    if echo "$result" | grep -q "orphan-plan.md"; then
        assert_equal "true" "true" "Orphaned files should be included in graph (as isolated nodes)"
    else
        assert_equal "ORPHAN_INCLUDED" "MISSING" \
            "Orphaned files should appear in dependency graph as isolated nodes"
    fi
}

# ============================================================================
# Test 8: Dependency type classification
# ============================================================================
test_should_classify_dependency_types() {
    echo "--- Test 8: Classify dependency types (reference, import, include) ---"

    # Arrange: Create files with different dependency types
    local test_dir
    test_dir=$(create_test_session_dir "$TEST_TEMP_DIR/test8")

    # File with explicit reference
    cat > "$test_dir/plans/reference-type.md" << 'EOF'
---
id: REF-TYPE
related_stories:
  - STORY-1000
---
# References in YAML
EOF

    # File with content reference
    cat > "$test_dir/plans/content-type.md" << 'EOF'
---
id: CONTENT-TYPE
---
# Content Reference
See STORY-1001 for details.
EOF

    # Act: Build dependency graph
    local result="{}"
    if declare -f build_dependency_graph &> /dev/null; then
        result=$(build_dependency_graph "$test_dir" 2>/dev/null || echo "{}")
    fi

    # Assert: Dependencies should have type classification
    if echo "$result" | grep -q '"type"'; then
        # Types might include: yaml_reference, content_reference, file_include
        assert_not_empty "$(echo "$result" | grep -o '"type"\s*:\s*"[^"]*"' | head -1)" \
            "Dependencies should have classified types"
    else
        assert_equal "TYPED_DEPS" "MISSING" \
            "DependencyEdge should include type classification"
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: AC#2 - Build File Dependency Graph"
echo "Story: STORY-223 - Catalog Session File Structure and Relationships"
echo "Technical Requirement: SM-021 - Build file dependency graph"
echo "========================================================================"
echo ""

test_dependency_graph_function_should_exist
echo ""

test_should_build_dependency_graph_structure
echo ""

test_should_contain_dependency_edge_fields
echo ""

test_should_detect_file_references_in_content
echo ""

test_should_handle_circular_dependencies
echo ""

test_should_include_all_file_types_in_graph
echo ""

test_should_handle_orphaned_files
echo ""

test_should_classify_dependency_types
echo ""

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "AC#2 Test Results"
exit_with_result
