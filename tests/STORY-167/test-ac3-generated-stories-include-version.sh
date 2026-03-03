#!/bin/bash
#
# Test: AC#3 - Generated Stories Include Version
# Story: STORY-167 - RCA-012 Story Template Version Tracking
#
# AC#3: Generated Stories Include Version
#   Given: a newly created story
#   When: I check the YAML frontmatter
#   Then: `format_version: "2.5"` should be present
#
# Test Framework: Bash shell script with assertions
# Uses shared test library: test-lib.sh
#

set -euo pipefail

# Import shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

# Create temporary test directory
TEST_TEMP_DIR="/tmp/test-story-167-ac3-$$"
mkdir -p "$TEST_TEMP_DIR"
trap "rm -rf $TEST_TEMP_DIR" EXIT

# ============================================================================
# Test 1: Template contains format_version field
# ============================================================================
test_should_have_format_version_field_in_template() {
    local content=$(get_file_content "$TEMPLATE_FILE")
    assert_contains "$content" "format_version" "Template should contain format_version field for generated stories"
}

# ============================================================================
# Test 2: Template format_version is set to 2.5
# ============================================================================
test_should_set_format_version_to_2_5() {
    local version=$(extract_field "$TEMPLATE_FILE" "format_version")
    assert_equal "2.5" "$version" "Template format_version should be set to 2.5"
}

# ============================================================================
# Test 3: format_version in YAML frontmatter
# ============================================================================
test_should_have_format_version_in_yaml_frontmatter() {
    local frontmatter=$(extract_frontmatter "$TEMPLATE_FILE")
    assert_contains "$frontmatter" "format_version" "format_version should be in YAML frontmatter (between --- delimiters)"
}

# ============================================================================
# Test 4: format_version appears before main story content
# ============================================================================
test_should_have_format_version_in_frontmatter_not_body() {
    local format_version_line=$(grep -n "format_version" "$TEMPLATE_FILE" | head -n 1 | cut -d: -f1)
    local story_title_line=$(grep -n "^# Story:" "$TEMPLATE_FILE" | head -n 1 | cut -d: -f1)

    if [[ -n "$format_version_line" ]] && [[ -n "$story_title_line" ]] && [[ $format_version_line -lt $story_title_line ]]; then
        assert_equal "yes" "yes" "format_version appears before story content"
    else
        assert_equal "before_title" "after_title" "format_version should appear in frontmatter before story title"
    fi
}

# ============================================================================
# Test 5: Generate sample story and check for format_version
# ============================================================================
test_should_generate_story_with_format_version() {
    local test_story="$TEST_TEMP_DIR/STORY-TEST-001.story.md"
    cp "$TEMPLATE_FILE" "$test_story"

    local story_content=$(get_file_content "$test_story")
    assert_contains "$story_content" 'format_version:\s*"2\.5"' "Generated story should include format_version: \"2.5\""
}

# ============================================================================
# Test 6: format_version value is quoted string
# ============================================================================
test_should_have_format_version_as_quoted_string() {
    local version_with_quotes=$(grep -o 'format_version:\s*"[^"]*"' "$TEMPLATE_FILE")
    assert_contains "$version_with_quotes" '"2\.5"' "format_version should be a quoted string like \"2.5\""
}

# ============================================================================
# Test 7: All generated stories have consistent format_version
# ============================================================================
test_should_maintain_consistent_format_version() {
    local template_version=$(extract_field "$TEMPLATE_FILE" "format_version")
    assert_equal "2.5" "$template_version" "Template should specify consistent format_version for all generated stories"
}

# ============================================================================
# Test 8: format_version field is properly formatted YAML
# ============================================================================
test_should_have_properly_formatted_yaml() {
    local format_version_line=$(grep "format_version:" "$TEMPLATE_FILE" | head -n 1)
    assert_contains "$format_version_line" "format_version:\s*\"2\.5\"" "format_version should follow YAML syntax: format_version: \"2.5\""
}

# ============================================================================
# Test 9: format_version is not commented out
# ============================================================================
test_should_have_active_format_version_field() {
    local commented_version=$(grep "^#.*format_version" "$TEMPLATE_FILE" 2>/dev/null | wc -l || echo "0")
    local active_version=$(grep "^format_version" "$TEMPLATE_FILE" 2>/dev/null | wc -l || echo "0")

    if [[ $active_version -gt 0 ]]; then
        assert_equal "yes" "yes" "format_version field is active (uncommented)"
    else
        assert_equal "active" "commented" "format_version field should be uncommented in template"
    fi
}

# ============================================================================
# Test 10: format_version in YAML frontmatter
# ============================================================================
test_should_position_format_version_in_yaml() {
    local frontmatter=$(extract_frontmatter "$TEMPLATE_FILE")
    assert_contains "$frontmatter" "format_version" "format_version should be in YAML frontmatter"
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: AC#3 - Generated Stories Include Version"
echo "Story: STORY-167 - RCA-012 Story Template Version Tracking"
echo "========================================================================"
echo ""

test_should_have_format_version_field_in_template
echo ""

test_should_set_format_version_to_2_5
echo ""

test_should_have_format_version_in_yaml_frontmatter
echo ""

test_should_have_format_version_in_frontmatter_not_body
echo ""

test_should_generate_story_with_format_version
echo ""

test_should_have_format_version_as_quoted_string
echo ""

test_should_maintain_consistent_format_version
echo ""

test_should_have_properly_formatted_yaml
echo ""

test_should_have_active_format_version_field
echo ""

test_should_position_format_version_in_yaml
echo ""

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "Test Results Summary"
exit_with_result
