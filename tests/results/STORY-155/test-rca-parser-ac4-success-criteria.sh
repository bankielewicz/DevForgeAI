#!/bin/bash
# Test Suite for STORY-155 AC#4: Extract Success Criteria
#
# Acceptance Criteria:
# Given a recommendation section contains a `**Success Criteria:**` subsection with checklist items
# When the parser identifies success criteria blocks
# Then the parser extracts all success criteria items as a list and associates them with the parent recommendation

set -e

# Test utility functions
assert_equals() {
    local expected="$1"
    local actual="$2"
    local test_name="$3"

    if [ "$expected" = "$actual" ]; then
        echo "✓ PASS: $test_name"
        return 0
    else
        echo "✗ FAIL: $test_name"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        return 1
    fi
}

# Setup: Create RCA with success criteria
setup_rca_with_success_criteria() {
    cat > /tmp/test-rca-success-criteria.md <<'EOF'
---
id: RCA-022
title: Test RCA
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

## Recommendations

### REC-1: CRITICAL - Increase Pool Size
Description of the fix.

**Effort Estimate:** 8 hours

**Success Criteria:**
- [ ] Connection pool size increased to 50
- [ ] No connection timeouts under 100 concurrent load
- [ ] Performance metrics improve by at least 20%

### REC-2: HIGH - Monitoring
Add monitoring for pool utilization.

**Effort Estimate:** 12 hours

**Success Criteria:**
- [ ] Dashboard created showing pool metrics
- [ ] Alerts configured for 80% utilization
- [ ] Runbook updated with troubleshooting steps

### REC-3: MEDIUM - Load Testing
Setup load testing.

No success criteria defined.
EOF
}

# Setup: Create RCA with single success criterion
setup_rca_single_success_criterion() {
    cat > /tmp/test-rca-single-criterion.md <<'EOF'
---
id: RCA-023
title: Single Criterion Test
date: 2025-12-21
severity: MEDIUM
status: OPEN
reporter: Bob Smith
---

## Recommendations

### REC-1: MEDIUM - Single Success Item
Description.

**Effort Estimate:** 4 hours

**Success Criteria:**
- [ ] Fix implemented and deployed
EOF
}

# Setup: Create RCA with many success criteria
setup_rca_many_success_criteria() {
    cat > /tmp/test-rca-many-criteria.md <<'EOF'
---
id: RCA-024
title: Many Criteria Test
date: 2025-12-22
severity: MEDIUM
status: OPEN
reporter: Charlie Davis
---

## Recommendations

### REC-1: MEDIUM - Complex Task
Description.

**Effort Estimate:** 20 hours

**Success Criteria:**
- [ ] Requirement 1 met
- [ ] Requirement 2 met
- [ ] Requirement 3 met
- [ ] Requirement 4 met
- [ ] Requirement 5 met
- [ ] Requirement 6 met
- [ ] Requirement 7 met
- [ ] Requirement 8 met
EOF
}

# Setup: Create RCA with success criteria using different checkbox formats
setup_rca_checkbox_variations() {
    cat > /tmp/test-rca-checkbox-variations.md <<'EOF'
---
id: RCA-025
title: Checkbox Variations
date: 2025-12-23
severity: MEDIUM
status: OPEN
reporter: Diana Prince
---

## Recommendations

### REC-1: MEDIUM - Various Formats
Description.

**Success Criteria:**
- [ ] Unchecked item
- [x] Checked item
- [ ]No space after bracket
- [ ] Proper format with space
- Normal bullet without checkbox
- [ ] Another unchecked
EOF
}

# Setup: Create RCA with success criteria using alternative list formats
setup_rca_alternative_list_formats() {
    cat > /tmp/test-rca-alternative-formats.md <<'EOF'
---
id: RCA-026
title: Alternative List Formats
date: 2025-12-24
severity: MEDIUM
status: OPEN
reporter: Eve Wilson
---

## Recommendations

### REC-1: MEDIUM - Different List Formats
Description.

**Success Criteria:**
1. Numbered item instead of bullet
2. Another numbered item
3. A third numbered item

### REC-2: LOW - Indented Bullets
Description.

**Success Criteria:**
- [ ] Main item
  - [ ] Sub-item 1
  - [ ] Sub-item 2
- [ ] Another main item
EOF
}

# Setup: Create RCA with success criteria having special characters
setup_rca_success_criteria_special_chars() {
    cat > /tmp/test-rca-special-chars.md <<'EOF'
---
id: RCA-027
title: Special Characters
date: 2025-12-25
severity: MEDIUM
status: OPEN
reporter: Frank Miller
---

## Recommendations

### REC-1: MEDIUM - Special Characters in Criteria
Description.

**Success Criteria:**
- [ ] Fix SQL "Injection" vulnerability (OWASP A-01)
- [ ] XSS prevention & input validation
- [ ] Database <schema> updated
- [ ] Performance > 95% baseline
- [ ] Tests passing: 100% (98/98)
EOF
}

# Setup: Create RCA without success criteria
setup_rca_no_success_criteria() {
    cat > /tmp/test-rca-no-criteria.md <<'EOF'
---
id: RCA-028
title: No Success Criteria
date: 2025-12-26
severity: LOW
status: RESOLVED
reporter: Grace Lee
---

## Recommendations

### REC-1: LOW - No Success Criteria
This recommendation has no success criteria section.
Just a description.

### REC-2: MEDIUM - Also None
No success criteria here either.
EOF
}

# Setup: Create RCA with success criteria in wrong format
setup_rca_malformed_success_criteria() {
    cat > /tmp/test-rca-malformed-criteria.md <<'EOF'
---
id: RCA-029
title: Malformed Criteria
date: 2025-12-27
severity: MEDIUM
status: OPEN
reporter: Henry Wu
---

## Recommendations

### REC-1: MEDIUM - Malformed Criteria Header
Description.

Success Criteria:
- [ ] Missing bold markers

### REC-2: HIGH - Wrong Level Header
Description.

#### Success Criteria:
- [ ] Wrong header level

### REC-3: LOW - No Colon
Description.

**Success Criteria**
- [ ] Missing colon after header
EOF
}

# Test 1: Extract success criteria from recommendation
test_extract_success_criteria_basic() {
    setup_rca_with_success_criteria

    # Should extract success criteria list from REC-1
    # Expected: [
    #   "Connection pool size increased to 50",
    #   "No connection timeouts under 100 concurrent load",
    #   "Performance metrics improve by at least 20%"
    # ]

    echo "TEST: test_extract_success_criteria_basic"
    echo "  Scenario: Extract success criteria checklist from recommendation"
    echo "  Expected: Extract all 3 items as list"
    echo "  Implementation needed: Parse **Success Criteria:** and bullet items"
}

# Test 2: Associate success criteria with parent recommendation
test_associate_criteria_with_recommendation() {
    setup_rca_with_success_criteria

    # Should link success criteria to REC-1 object
    # Expected: recommendation.success_criteria = [...]

    echo "TEST: test_associate_criteria_with_recommendation"
    echo "  Scenario: Link success criteria to parent recommendation"
    echo "  Expected: REC-1.success_criteria array populated"
    echo "  Implementation needed: Associate criteria with parent recommendation ID"
}

# Test 3: Handle recommendation without success criteria
test_handle_missing_success_criteria() {
    setup_rca_with_success_criteria

    # REC-3 has no success criteria
    # Should handle gracefully - return null or empty array
    # Expected: recommendation.success_criteria = [] or null

    echo "TEST: test_handle_missing_success_criteria"
    echo "  Scenario: Recommendation without success criteria section"
    echo "  Expected: success_criteria = [] (empty) or null"
    echo "  Implementation needed: Handle optional section gracefully"
}

# Test 4: Extract single success criterion
test_extract_single_success_criterion() {
    setup_rca_single_success_criterion

    # Should extract the one success criterion
    # Expected: [
    #   "Fix implemented and deployed"
    # ]

    echo "TEST: test_extract_single_success_criterion"
    echo "  Scenario: Recommendation with single success criterion"
    echo "  Expected: Extract single item in array"
    echo "  Implementation needed: Handle 1-item lists"
}

# Test 5: Extract many success criteria
test_extract_many_success_criteria() {
    setup_rca_many_success_criteria

    # Should extract all 8 criteria
    # Expected: Array with 8 items

    echo "TEST: test_extract_many_success_criteria"
    echo "  Scenario: Recommendation with 8 success criteria"
    echo "  Expected: Extract all 8 items in order"
    echo "  Implementation needed: Handle large lists"
}

# Test 6: Strip checkbox markers from criteria text
test_strip_checkbox_markers() {
    setup_rca_with_success_criteria

    # Should extract "Connection pool size increased to 50" (no "- [ ]" prefix)
    # Expected: Clean text without checkbox markers

    echo "TEST: test_strip_checkbox_markers"
    echo "  Scenario: Remove '- [ ]' checkbox markers from criteria text"
    echo "  Expected: 'Connection pool size increased to 50' (no prefix)"
    echo "  Implementation needed: Strip '- [ ]' or '- [x]' from line"
}

# Test 7: Handle both checked and unchecked checkboxes
test_handle_checked_and_unchecked() {
    setup_rca_checkbox_variations

    # Should extract all items regardless of checked status
    # Expected: Both [x] and [ ] items included

    echo "TEST: test_handle_checked_and_unchecked"
    echo "  Scenario: Success criteria with mixed checkbox states"
    echo "  Expected: Include both [ ] (unchecked) and [x] (checked) items"
    echo "  Implementation needed: Extract regardless of checkbox state"
}

# Test 8: Handle success criteria in correct order
test_success_criteria_order() {
    setup_rca_with_success_criteria

    # Should maintain order of criteria
    # Expected: [
    #   "Connection pool size increased to 50",
    #   "No connection timeouts under 100 concurrent load",
    #   "Performance metrics improve by at least 20%"
    # ]

    echo "TEST: test_success_criteria_order"
    echo "  Scenario: Maintain order of extracted success criteria"
    echo "  Expected: Items in exact document order"
    echo "  Implementation needed: Preserve parsing order"
}

# Test 9: Skip non-checkbox bullets in success criteria
test_skip_non_checkbox_bullets() {
    setup_rca_checkbox_variations

    # Should skip "Normal bullet without checkbox"
    # Expected: Skip items without [ ] or [x]

    echo "TEST: test_skip_non_checkbox_bullets"
    echo "  Scenario: Success criteria section with mixed bullet types"
    echo "  Expected: Skip bullets without checkbox markers"
    echo "  Implementation needed: Filter for checkbox format"
}

# Test 10: Handle success criteria with special characters
test_success_criteria_special_characters() {
    setup_rca_success_criteria_special_chars

    # Should preserve special chars in criteria text
    # Expected: Include quotes, ampersand, angle brackets, etc.

    echo "TEST: test_success_criteria_special_characters"
    echo "  Scenario: Criteria with special characters (quotes, &, <>, etc)"
    echo "  Expected: Preserve special characters in extracted text"
    echo "  Implementation needed: Safe character handling"
}

# Test 11: Handle success criteria with markdown formatting
test_success_criteria_with_markdown_formatting() {
    cat > /tmp/test-rca-markdown-criteria.md <<'EOF'
---
id: RCA-030
title: Markdown in Criteria
date: 2025-12-28
severity: MEDIUM
status: OPEN
reporter: Iris Brown
---

## Recommendations

### REC-1: MEDIUM - With Markdown
Description.

**Success Criteria:**
- [ ] Tests passing: `npm test` should exit with 0
- [ ] **All** critical bugs fixed
- [ ] Performance improved by *at least* 20%
- [ ] Code follows [style guide](https://example.com)
EOF

    # Should handle markdown in criteria text
    # Expected: Extract text with markdown syntax

    echo "TEST: test_success_criteria_with_markdown_formatting"
    echo "  Scenario: Success criteria containing markdown (**bold**, *italic*, \`code\`)"
    echo "  Expected: Preserve markdown formatting or extract clean text"
    echo "  Implementation needed: Handle markdown in criteria"
}

# Test 12: Handle numbered list as success criteria
test_numbered_list_success_criteria() {
    setup_rca_alternative_list_formats

    # REC-1 uses numbered list (1. 2. 3.)
    # Should accept numbered lists as alternative to bullets
    # Expected: Extract 3 items from numbered list

    echo "TEST: test_numbered_list_success_criteria"
    echo "  Scenario: Success criteria as numbered list (1. 2. 3.)"
    echo "  Expected: Extract all 3 items from numbered format"
    echo "  Implementation needed: Support both bullet and numbered lists"
}

# Test 13: Handle indented sub-items in success criteria
test_indented_sub_items_success_criteria() {
    setup_rca_alternative_list_formats

    # REC-2 has indented sub-items
    # Should flatten or handle hierarchical criteria
    # Expected: Include sub-items in criteria list

    echo "TEST: test_indented_sub_items_success_criteria"
    echo "  Scenario: Success criteria with indented sub-items"
    echo "  Expected: Include parent and child items (flatten or preserve structure)"
    echo "  Implementation needed: Handle hierarchical criteria"
}

# Test 14: Detect malformed success criteria headers
test_detect_malformed_criteria_headers() {
    setup_rca_malformed_success_criteria

    # Should handle:
    # - Missing bold markers: "Success Criteria:"
    # - Wrong header level: "#### Success Criteria:"
    # - Missing colon: "**Success Criteria**"
    # Expected: Skip or log error for malformed headers

    echo "TEST: test_detect_malformed_criteria_headers"
    echo "  Scenario: Various malformed success criteria headers"
    echo "  Expected: Handle gracefully - skip or error on malformed format"
    echo "  Implementation needed: Strict header format validation"
}

# Test 15: Extract success criteria from RCA with multiple recommendations
test_success_criteria_multiple_recommendations() {
    setup_rca_with_success_criteria

    # Should extract criteria for REC-1, REC-2, and null for REC-3
    # Expected: Each recommendation associated with correct criteria

    echo "TEST: test_success_criteria_multiple_recommendations"
    echo "  Scenario: RCA with multiple recommendations, each with different criteria"
    echo "  Expected: Each recommendation linked to its own criteria set"
    echo "  Implementation needed: Correctly associate criteria with parent recommendation"
}

# Main test execution
main() {
    echo "=========================================="
    echo "STORY-155 AC#4: Extract Success Criteria"
    echo "=========================================="
    echo ""

    test_extract_success_criteria_basic
    test_associate_criteria_with_recommendation
    test_handle_missing_success_criteria
    test_extract_single_success_criterion
    test_extract_many_success_criteria
    test_strip_checkbox_markers
    test_handle_checked_and_unchecked
    test_success_criteria_order
    test_skip_non_checkbox_bullets
    test_success_criteria_special_characters
    test_success_criteria_with_markdown_formatting
    test_numbered_list_success_criteria
    test_indented_sub_items_success_criteria
    test_detect_malformed_criteria_headers
    test_success_criteria_multiple_recommendations

    echo ""
    echo "=========================================="
    echo "All AC#4 tests generated (FAILING)"
    echo "Implementation required for all tests"
    echo "=========================================="
}

main "$@"
