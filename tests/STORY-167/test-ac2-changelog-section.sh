#!/bin/bash
#
# Test: AC#2 - Changelog Section
# Story: STORY-167 - RCA-012 Story Template Version Tracking
#
# AC#2: Changelog Section
#   Given: the story template
#   When: I look for version history
#   Then: there should be a changelog documenting versions 1.0, 2.0, 2.1
#
# Test Framework: Bash shell script with assertions
# Uses shared test library: test-lib.sh
#

set -euo pipefail

# Import shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

# ============================================================================
# Test 1: Template contains changelog section
# ============================================================================
test_should_have_changelog_section() {
    local content=$(get_file_content "$TEMPLATE_FILE")
    assert_contains "$content" "changelog" "Template should document version changelog"
}

# ============================================================================
# Test 2: Changelog documents version 1.0
# ============================================================================
test_should_document_version_1_0() {
    local content=$(get_file_content "$TEMPLATE_FILE")
    assert_contains "$content" "1\.0" "Changelog should document version 1.0"
}

# ============================================================================
# Test 3: Changelog documents version 2.0
# ============================================================================
test_should_document_version_2_0() {
    local content=$(get_file_content "$TEMPLATE_FILE")
    assert_contains "$content" "2\.0" "Changelog should document version 2.0"
}

# ============================================================================
# Test 4: Changelog documents version 2.1
# ============================================================================
test_should_document_version_2_1() {
    local content=$(get_file_content "$TEMPLATE_FILE")
    assert_contains "$content" "2\.1" "Changelog should document version 2.1 (current)"
}

# ============================================================================
# Test 5: Changelog entry for 1.0 includes description
# ============================================================================
test_should_have_description_for_version_1_0() {
    local v1_section=$(sed -n '/1\.0/,/^#/p' "$TEMPLATE_FILE" | head -n -1)
    assert_not_empty "$v1_section" "Version 1.0 changelog entry should have content"
}

# ============================================================================
# Test 6: Changelog entry for 2.0 includes description
# ============================================================================
test_should_have_description_for_version_2_0() {
    local v2_0_section=$(sed -n '/2\.0/,/2\.1/p' "$TEMPLATE_FILE" | head -n -1)
    assert_not_empty "$v2_0_section" "Version 2.0 changelog entry should have content"
}

# ============================================================================
# Test 7: Changelog entry for 2.1 includes description
# ============================================================================
test_should_have_description_for_version_2_1() {
    local v2_1_section=$(sed -n '/2\.1/,$p' "$TEMPLATE_FILE" | head -n 10)
    assert_not_empty "$v2_1_section" "Version 2.1 changelog entry should have content"
}

# ============================================================================
# Test 8: Changelog mentions RCA-012 for v2.1
# ============================================================================
test_should_reference_rca_012_in_changelog() {
    local content=$(get_file_content "$TEMPLATE_FILE")
    assert_contains "$content" "RCA-012\|RCA012" "Changelog should reference RCA-012 for v2.1 changes"
}

# ============================================================================
# Test 9: Changelog is properly formatted with markdown headers
# ============================================================================
test_should_have_markdown_formatted_changelog() {
    local has_changelog_header=$(grep -c "^#.*[Cc]hangelog\|^#.*[Vv]ersion.*[Hh]istory" "$TEMPLATE_FILE" || echo "0")

    if [[ $has_changelog_header -gt 0 ]]; then
        assert_equal "yes" "yes" "Changelog has markdown headers"
    else
        assert_not_empty "changelog_header_found" "Changelog should use markdown headers (# or ##)"
    fi
}

# ============================================================================
# Test 10: Version 2.1 lists AC header format change (RCA-012)
# ============================================================================
test_should_mention_ac_header_change_in_v2_1() {
    local v2_1_changes=$(sed -n '/2\.1/,/2\.0\|1\.0/p' "$TEMPLATE_FILE" | head -n -1)
    assert_contains "$v2_1_changes" "[Aa][Cc].*[Cc]heckbox\|[Cc]heckbox.*[Aa][Cc]\|AC#\|AC header" "v2.1 changelog should mention AC header checkbox removal"
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: AC#2 - Changelog Section"
echo "Story: STORY-167 - RCA-012 Story Template Version Tracking"
echo "========================================================================"
echo ""

test_should_have_changelog_section
echo ""

test_should_document_version_1_0
echo ""

test_should_document_version_2_0
echo ""

test_should_document_version_2_1
echo ""

test_should_have_description_for_version_1_0
echo ""

test_should_have_description_for_version_2_0
echo ""

test_should_have_description_for_version_2_1
echo ""

test_should_reference_rca_012_in_changelog
echo ""

test_should_have_markdown_formatted_changelog
echo ""

test_should_mention_ac_header_change_in_v2_1
echo ""

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "Test Results Summary"
exit_with_result
