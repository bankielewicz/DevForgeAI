#!/bin/bash
#
# Test: AC#1 - Template Version in Frontmatter
# Story: STORY-167 - RCA-012 Story Template Version Tracking
#
# AC#1: Template Version in Frontmatter
#   Given: the story template
#   When: I review the header section
#   Then: there should be `template_version` and `last_updated` metadata
#
# Test Framework: Bash shell script with assertions
# Uses shared test library: test-lib.sh
#

set -euo pipefail

# Import shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

# ============================================================================
# Test 1: Template file exists
# ============================================================================
test_should_find_story_template_file() {
    assert_file_exists "$TEMPLATE_FILE" "Template file should exist at expected location"
}

# ============================================================================
# Test 2: Template has template_version metadata in frontmatter
# ============================================================================
test_should_have_template_version_metadata() {
    local frontmatter=$(extract_frontmatter "$TEMPLATE_FILE")
    assert_contains "$frontmatter" "template_version" "Frontmatter should contain 'template_version' field"
}

# ============================================================================
# Test 3: Template has last_updated metadata in frontmatter
# ============================================================================
test_should_have_last_updated_metadata() {
    local frontmatter=$(extract_frontmatter "$TEMPLATE_FILE")
    assert_contains "$frontmatter" "last_updated" "Frontmatter should contain 'last_updated' field"
}

# ============================================================================
# Test 4: Template version follows semantic versioning format
# ============================================================================
test_should_have_valid_template_version_format() {
    local version=$(extract_field "$TEMPLATE_FILE" "template_version")

    if validate_semantic_version "$version"; then
        assert_not_empty "$version" "Template version should be in semantic versioning format"
    else
        assert_equal "[0-9]+\.[0-9]+" "$version" "Template version should follow semantic versioning (e.g., 2.1 or 2.1.0)"
    fi
}

# ============================================================================
# Test 5: last_updated is in ISO 8601 date format
# ============================================================================
test_should_have_valid_last_updated_format() {
    local date=$(extract_field "$TEMPLATE_FILE" "last_updated")

    if validate_iso8601_date "$date"; then
        assert_not_empty "$date" "last_updated should be in YYYY-MM-DD format"
    else
        assert_equal "YYYY-MM-DD" "$date" "last_updated should be in ISO 8601 date format (e.g., 2025-12-31)"
    fi
}

# ============================================================================
# Test 6: Frontmatter starts with --- delimiter
# ============================================================================
test_should_have_valid_frontmatter_delimiters() {
    local first_line=$(head -n 1 "$TEMPLATE_FILE" | tr -d '\r')
    assert_equal "---" "$first_line" "Frontmatter should start with --- delimiter"
}

# ============================================================================
# Test 7: template_version value is not empty
# ============================================================================
test_should_have_non_empty_template_version() {
    local version=$(extract_field "$TEMPLATE_FILE" "template_version")
    assert_not_empty "$version" "template_version should have a value"
}

# ============================================================================
# Test 8: last_updated value is not empty
# ============================================================================
test_should_have_non_empty_last_updated() {
    local date=$(extract_field "$TEMPLATE_FILE" "last_updated")
    assert_not_empty "$date" "last_updated should have a value"
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: AC#1 - Template Version in Frontmatter"
echo "Story: STORY-167 - RCA-012 Story Template Version Tracking"
echo "========================================================================"
echo ""

test_should_find_story_template_file
echo ""

test_should_have_template_version_metadata
echo ""

test_should_have_last_updated_metadata
echo ""

test_should_have_valid_template_version_format
echo ""

test_should_have_valid_last_updated_format
echo ""

test_should_have_valid_frontmatter_delimiters
echo ""

test_should_have_non_empty_template_version
echo ""

test_should_have_non_empty_last_updated
echo ""

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "Test Results Summary"
exit_with_result
