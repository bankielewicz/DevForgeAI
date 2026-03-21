#!/bin/bash

##############################################################################
# Test Suite: STORY-554 AC#3 - Output Format Compliance
#
# AC#3: Output Format Compliance
# Given: a checklist has been generated for the user's business model
# When: the output is written
# Then: the file devforgeai/specs/business/operations/launch-checklist.md is
#       created with GitHub-flavored markdown checkboxes (- [ ] format),
#       grouped by domain with section headers, and each item includes a
#       one-line description of why it matters
#
# Primary target: src/claude/skills/operating-business/references/mvp-launch-checklist.md
# Output artifact: devforgeai/specs/business/operations/launch-checklist.md
#
# TDD Phase: RED - All tests expected to FAIL (target files do not exist)
# Story: STORY-554
# Generated: 2026-03-21
##############################################################################

set -euo pipefail

TEST_NAME="AC#3: Output Format Compliance"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../" && pwd)"
REFERENCE_FILE="src/claude/skills/operating-business/references/mvp-launch-checklist.md"
OUTPUT_FILE="devforgeai/specs/business/operations/launch-checklist.md"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}  PASS${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}  FAIL${NC}"
    fi
}

##############################################################################
# TEST 1: Reference file exists
##############################################################################

test_reference_file_exists() {
    local file="$PROJECT_ROOT/$REFERENCE_FILE"

    if [ -f "$file" ]; then
        echo "  Reference file found: $REFERENCE_FILE"
        return 0
    else
        echo "  ERROR: Reference file not found at $REFERENCE_FILE"
        return 1
    fi
}

##############################################################################
# TEST 2: Reference file specifies output path
##############################################################################

test_reference_specifies_output_path() {
    local file="$PROJECT_ROOT/$REFERENCE_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $REFERENCE_FILE"
        return 1
    fi

    if grep -q "devforgeai/specs/business/operations/launch-checklist.md" "$file"; then
        echo "  Output path specified in reference file"
        return 0
    else
        echo "  ERROR: Output path not specified in reference file"
        return 1
    fi
}

##############################################################################
# TEST 3: Reference file uses GitHub-flavored markdown checkboxes
##############################################################################

test_uses_github_checkboxes() {
    local file="$PROJECT_ROOT/$REFERENCE_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $REFERENCE_FILE"
        return 1
    fi

    local checkbox_count
    checkbox_count=$(grep -c "^- \[ \]" "$file" 2>/dev/null || echo "0")

    if [ "$checkbox_count" -ge 15 ]; then
        echo "  Found $checkbox_count GitHub-flavored checkboxes (minimum 15 expected)"
        return 0
    else
        echo "  ERROR: Found only $checkbox_count checkboxes (minimum 15 expected for 5 domains x 3 items)"
        return 1
    fi
}

##############################################################################
# TEST 4: Items grouped by domain with section headers
##############################################################################

test_items_grouped_by_domain_headers() {
    local file="$PROJECT_ROOT/$REFERENCE_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $REFERENCE_FILE"
        return 1
    fi

    # Check for markdown section headers (## or ###) containing domain names
    local header_count=0

    for domain in "legal" "financ" "marketing" "technical" "operat"; do
        if grep -qiE "^#{1,3} .*$domain" "$file"; then
            header_count=$((header_count + 1))
        fi
    done

    if [ "$header_count" -ge 5 ]; then
        echo "  All 5 domains have section headers"
        return 0
    else
        echo "  ERROR: Only $header_count of 5 domain section headers found"
        return 1
    fi
}

##############################################################################
# TEST 5: Each checklist item has a description (why it matters)
##############################################################################

test_each_item_has_description() {
    local file="$PROJECT_ROOT/$REFERENCE_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $REFERENCE_FILE"
        return 1
    fi

    # Count total checkbox items
    local total_items
    total_items=$(grep -c "^- \[ \]" "$file" 2>/dev/null || echo "0")

    # Count checkbox items with a description separator (dash, colon, or pipe after item name)
    local items_with_desc
    items_with_desc=$(grep -cE "^- \[ \] .+( - | -- |: ).+" "$file" 2>/dev/null || echo "0")

    if [ "$total_items" -eq 0 ]; then
        echo "  ERROR: No checklist items found"
        return 1
    fi

    # At least 90% should have descriptions
    local threshold=$((total_items * 90 / 100))

    if [ "$items_with_desc" -ge "$threshold" ]; then
        echo "  $items_with_desc of $total_items items have descriptions (>= 90%)"
        return 0
    else
        echo "  ERROR: Only $items_with_desc of $total_items items have descriptions (< 90%)"
        return 1
    fi
}

##############################################################################
# TEST 6: No mixed checkbox formats (consistency)
##############################################################################

test_consistent_checkbox_format() {
    local file="$PROJECT_ROOT/$REFERENCE_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $REFERENCE_FILE"
        return 1
    fi

    # Check for non-standard checkbox formats that would break GFM rendering
    local bad_formats
    bad_formats=$(grep -cE "^- \[[xX]\]|^\* \[ \]|^[0-9]+\. \[ \]" "$file" 2>/dev/null || echo "0")

    local good_formats
    good_formats=$(grep -c "^- \[ \]" "$file" 2>/dev/null || echo "0")

    if [ "$good_formats" -gt 0 ] && [ "$bad_formats" -eq 0 ]; then
        echo "  Consistent checkbox format: $good_formats items, all using '- [ ]'"
        return 0
    elif [ "$good_formats" -eq 0 ]; then
        echo "  ERROR: No standard checkboxes found"
        return 1
    else
        echo "  ERROR: Found $bad_formats non-standard checkbox formats"
        return 1
    fi
}

##############################################################################
# TEST 7: File is valid markdown (no broken syntax)
##############################################################################

test_valid_markdown_structure() {
    local file="$PROJECT_ROOT/$REFERENCE_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $REFERENCE_FILE"
        return 1
    fi

    # Check for basic markdown structure: at least one H1 or H2 header
    local header_count
    header_count=$(grep -c "^#" "$file" 2>/dev/null || echo "0")

    if [ "$header_count" -ge 6 ]; then
        echo "  Valid markdown structure: $header_count headers found"
        return 0
    else
        echo "  ERROR: Insufficient markdown structure: only $header_count headers (expected >= 6)"
        return 1
    fi
}

##############################################################################
# TEST 8: Checklist items are not empty (have meaningful text)
##############################################################################

test_checklist_items_not_empty() {
    local file="$PROJECT_ROOT/$REFERENCE_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $REFERENCE_FILE"
        return 1
    fi

    # Check for empty checkbox items (just "- [ ]" with no text after)
    local empty_items
    empty_items=$(grep -cE "^- \[ \]\s*$" "$file" 2>/dev/null || echo "0")

    if [ "$empty_items" -eq 0 ]; then
        echo "  All checklist items have meaningful text"
        return 0
    else
        echo "  ERROR: Found $empty_items empty checklist items"
        return 1
    fi
}

##############################################################################
# TEST 9: File has a title header
##############################################################################

test_file_has_title_header() {
    local file="$PROJECT_ROOT/$REFERENCE_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $REFERENCE_FILE"
        return 1
    fi

    # Check for H1 header containing launch/checklist
    if grep -qiE "^# .*launch.*checklist|^# .*mvp.*launch|^# .*checklist" "$file"; then
        echo "  Title header found"
        return 0
    else
        echo "  ERROR: No title header with 'launch checklist' found"
        return 1
    fi
}

##############################################################################
# TEST 10: Items include why-it-matters description
##############################################################################

test_items_explain_why_it_matters() {
    local file="$PROJECT_ROOT/$REFERENCE_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $REFERENCE_FILE"
        return 1
    fi

    # Each item should have a description explaining WHY it matters
    # Look for items with at least 20 characters of description text
    local total_items
    total_items=$(grep -c "^- \[ \]" "$file" 2>/dev/null || echo "0")

    local descriptive_items
    descriptive_items=$(grep -cE "^- \[ \] .{20,}" "$file" 2>/dev/null || echo "0")

    if [ "$total_items" -eq 0 ]; then
        echo "  ERROR: No checklist items found"
        return 1
    fi

    if [ "$descriptive_items" -ge "$total_items" ]; then
        echo "  All $total_items items have substantive descriptions (20+ chars)"
        return 0
    else
        echo "  ERROR: Only $descriptive_items of $total_items items have substantive descriptions"
        return 1
    fi
}

##############################################################################
# Run all tests
##############################################################################

echo "============================================================"
echo "STORY-554 | $TEST_NAME"
echo "Reference: $REFERENCE_FILE"
echo "Output:    $OUTPUT_FILE"
echo "============================================================"

run_test "Reference file exists" test_reference_file_exists
run_test "Reference specifies output path" test_reference_specifies_output_path
run_test "Uses GitHub-flavored markdown checkboxes" test_uses_github_checkboxes
run_test "Items grouped by domain with section headers" test_items_grouped_by_domain_headers
run_test "Each item has a description" test_each_item_has_description
run_test "Consistent checkbox format" test_consistent_checkbox_format
run_test "Valid markdown structure" test_valid_markdown_structure
run_test "Checklist items are not empty" test_checklist_items_not_empty
run_test "File has title header" test_file_has_title_header
run_test "Items explain why it matters" test_items_explain_why_it_matters

##############################################################################
# Summary
##############################################################################

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed out of $TESTS_RUN tests"
echo "============================================================"

[ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
