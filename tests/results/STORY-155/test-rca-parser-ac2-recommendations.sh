#!/bin/bash
# Test Suite for STORY-155 AC#2: Extract Recommendations with Priority Levels
#
# Acceptance Criteria:
# Given an RCA file contains multiple recommendations under section headers (e.g., `### REC-N: PRIORITY - Title`)
# When the parser scans the markdown body and identifies all recommendation sections
# Then the parser extracts each recommendation as: id (REC-N), priority, title, description,
# and returns them in document order

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

assert_array_length() {
    local expected_count="$1"
    local actual_count="$2"
    local test_name="$3"

    if [ "$expected_count" -eq "$actual_count" ]; then
        echo "✓ PASS: $test_name"
        return 0
    else
        echo "✗ FAIL: $test_name"
        echo "  Expected count: $expected_count"
        echo "  Actual count: $actual_count"
        return 1
    fi
}

# Setup: Create RCA file with multiple recommendations
setup_rca_with_multiple_recommendations() {
    cat > /tmp/test-rca-recommendations.md <<'EOF'
---
id: RCA-022
title: Database Connection Pool Exhaustion
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

# RCA-022: Database Connection Pool Exhaustion

## Root Cause Analysis
The connection pool was misconfigured for peak loads.

## Recommendations

### REC-1: CRITICAL - Increase Connection Pool Size
The current pool size of 10 is insufficient for peak load of 100 concurrent requests.
Increase to minimum 50 connections immediately.

This is an urgent fix to prevent service degradation.

### REC-2: HIGH - Implement Connection Pool Monitoring
Add metrics to track pool utilization, available connections, and wait times.
Create alerts when utilization exceeds 80%.

### REC-3: MEDIUM - Load Testing Before Deployment
Establish load testing procedures to validate pool configuration.
Test with realistic concurrent load patterns.

### REC-4: LOW - Document Connection Pool Configuration
Create runbooks for connection pool tuning and troubleshooting.
Add comments to configuration file explaining each setting.
EOF
}

# Setup: Create RCA with single recommendation
setup_rca_with_single_recommendation() {
    cat > /tmp/test-rca-single-rec.md <<'EOF'
---
id: RCA-025
title: Single Recommendation Test
date: 2025-12-21
severity: MEDIUM
status: OPEN
reporter: Bob Smith
---

## Recommendations

### REC-1: MEDIUM - Fix This Issue
Description of the fix.
EOF
}

# Setup: Create RCA with no recommendations
setup_rca_with_no_recommendations() {
    cat > /tmp/test-rca-no-recommendations.md <<'EOF'
---
id: RCA-026
title: No Recommendations
date: 2025-12-22
severity: LOW
status: RESOLVED
reporter: Charlie Davis
---

# RCA-026: No Recommendations

This RCA has no recommendations section.
EOF
}

# Setup: Create RCA with recommendations in wrong format
setup_rca_malformed_recommendations() {
    cat > /tmp/test-rca-malformed-recs.md <<'EOF'
---
id: RCA-027
title: Malformed Recommendations
date: 2025-12-23
severity: HIGH
status: OPEN
reporter: Diana Prince
---

## Recommendations

REC-1: CRITICAL - Missing Markdown Header
This recommendation uses wrong format (no ### markdown header).

#### REC-2: HIGH - Wrong Header Level
This uses #### instead of ### (wrong header level).

### REC-3 CRITICAL Missing Colon
This is missing the colon after REC-3.

### REC-4: INVALID - Unknown Priority
This has an invalid priority value (not CRITICAL/HIGH/MEDIUM/LOW).
EOF
}

# Setup: Create RCA with duplicate recommendation IDs
setup_rca_duplicate_rec_ids() {
    cat > /tmp/test-rca-duplicate-ids.md <<'EOF'
---
id: RCA-028
title: Duplicate Recommendation IDs
date: 2025-12-24
severity: MEDIUM
status: OPEN
reporter: Eve Wilson
---

## Recommendations

### REC-1: CRITICAL - First Issue
First recommendation.

### REC-1: HIGH - Duplicate ID
Second recommendation with same ID (should be REC-2).
EOF
}

# Test 1: Extract single recommendation with all fields
test_extract_recommendation_with_all_fields() {
    setup_rca_with_single_recommendation

    # Should extract: id=REC-1, priority=MEDIUM, title=Fix This Issue, description=...
    # Expected: All fields present

    echo "TEST: test_extract_recommendation_with_all_fields"
    echo "  Scenario: Parse recommendation with complete information"
    echo "  Expected: Extract id, priority, title, description fields"
    echo "  Implementation needed: Markdown header parsing and field extraction"
}

# Test 2: Extract multiple recommendations
test_extract_multiple_recommendations() {
    setup_rca_with_multiple_recommendations

    # Should extract 4 recommendations in document order
    # Expected: recommendations array with 4 items

    echo "TEST: test_extract_multiple_recommendations"
    echo "  Scenario: RCA with 4 recommendations (CRITICAL, HIGH, MEDIUM, LOW)"
    echo "  Expected: Extract all 4 recommendations in order (REC-1, REC-2, REC-3, REC-4)"
    echo "  Implementation needed: Loop through markdown headers and collect recommendations"
}

# Test 3: Maintain document order for recommendations
test_extract_recommendations_in_document_order() {
    setup_rca_with_multiple_recommendations

    # Should return recommendations in exact document order
    # Expected: [REC-1, REC-2, REC-3, REC-4] (not sorted by priority yet)

    echo "TEST: test_extract_recommendations_in_document_order"
    echo "  Scenario: Extract multiple recommendations"
    echo "  Expected: Return in document order (REC-1 first, then REC-2, REC-3, REC-4)"
    echo "  Implementation needed: Preserve order while parsing"
}

# Test 4: Extract recommendation ID correctly
test_extract_recommendation_id() {
    setup_rca_with_single_recommendation

    # Should extract "REC-1" from header
    # Expected: id = "REC-1"

    echo "TEST: test_extract_recommendation_id"
    echo "  Scenario: Parse recommendation header for ID"
    echo "  Expected: Extract 'REC-1' from '### REC-1: MEDIUM - Fix This Issue'"
    echo "  Implementation needed: Regex to extract REC-N pattern"
}

# Test 5: Extract recommendation priority correctly
test_extract_recommendation_priority() {
    setup_rca_with_multiple_recommendations

    # Should extract priority from header
    # REC-1: CRITICAL, REC-2: HIGH, REC-3: MEDIUM, REC-4: LOW
    # Expected: priority values match header

    echo "TEST: test_extract_recommendation_priority"
    echo "  Scenario: Parse priority from recommendation header"
    echo "  Expected: Extract [CRITICAL, HIGH, MEDIUM, LOW] from headers"
    echo "  Implementation needed: Extract enum value from header format"
}

# Test 6: Extract recommendation title correctly
test_extract_recommendation_title() {
    setup_rca_with_multiple_recommendations

    # Should extract title from header after priority
    # REC-1: CRITICAL - "Increase Connection Pool Size"
    # Expected: title = "Increase Connection Pool Size"

    echo "TEST: test_extract_recommendation_title"
    echo "  Scenario: Extract title from recommendation header"
    echo "  Expected: Extract 'Increase Connection Pool Size' from header"
    echo "  Implementation needed: Parse title after '- ' separator"
}

# Test 7: Extract recommendation description (body)
test_extract_recommendation_description() {
    setup_rca_with_multiple_recommendations

    # Should extract all lines after header until next recommendation
    # Expected: Multi-line description text

    echo "TEST: test_extract_recommendation_description"
    echo "  Scenario: Extract multi-line description"
    echo "  Expected: Collect all text between header and next REC header"
    echo "  Implementation needed: Read until next ### REC- or EOF"
}

# Test 8: Handle RCA with no recommendations
test_extract_no_recommendations() {
    setup_rca_with_no_recommendations

    # Should return empty array or appropriate signal
    # Expected: recommendations = []

    echo "TEST: test_extract_no_recommendations"
    echo "  Scenario: RCA file with no recommendations section"
    echo "  Expected: Return empty recommendations array []"
    echo "  Implementation needed: Handle missing section gracefully"
}

# Test 9: Validate recommendation ID format (REC-N)
test_validate_recommendation_id_format() {
    setup_rca_with_multiple_recommendations

    # Should validate that recommendation ID is REC-N (where N is digits)
    # Expected: Accept "REC-1", "REC-2", "REC-100", reject "rec-1", "REC-A", "RECOMMENDATION-1"

    echo "TEST: test_validate_recommendation_id_format"
    echo "  Scenario: Validate recommendation ID format"
    echo "  Expected: Accept REC-[0-9]+, reject others"
    echo "  Implementation needed: Regex validation for ID format"
}

# Test 10: Validate recommendation priority enum
test_validate_recommendation_priority_enum() {
    setup_rca_malformed_recommendations

    # Should validate priority is one of: CRITICAL, HIGH, MEDIUM, LOW
    # Expected: Accept valid values, error on invalid

    echo "TEST: test_validate_recommendation_priority_enum"
    echo "  Scenario: Validate priority values"
    echo "  Expected: Accept [CRITICAL, HIGH, MEDIUM, LOW], reject INVALID"
    echo "  Implementation needed: Enum validation"
}

# Test 11: Handle malformed recommendation headers
test_handle_malformed_recommendation_headers() {
    setup_rca_malformed_recommendations

    # Should handle gracefully:
    # - Wrong header level (#### instead of ###)
    # - Missing colon
    # - Missing separator (-)
    # Expected: Skip or log error

    echo "TEST: test_handle_malformed_recommendation_headers"
    echo "  Scenario: RCA with malformed recommendation headers"
    echo "  Expected: Skip malformed headers or log clear errors"
    echo "  Implementation needed: Robust header parsing"
}

# Test 12: Detect duplicate recommendation IDs
test_detect_duplicate_recommendation_ids() {
    setup_rca_duplicate_rec_ids

    # Should detect when same REC-N appears twice
    # Expected: Error or warning about duplicates

    echo "TEST: test_detect_duplicate_recommendation_ids"
    echo "  Scenario: RCA with duplicate REC IDs"
    echo "  Expected: Detect and report duplicate ID 'REC-1'"
    echo "  Implementation needed: Track seen IDs and validate uniqueness"
}

# Test 13: Handle very long recommendation description
test_extract_long_recommendation_description() {
    cat > /tmp/test-rca-long-desc.md <<'EOF'
---
id: RCA-030
title: Long Description Test
date: 2025-12-25
severity: MEDIUM
status: OPEN
reporter: Frank Miller
---

## Recommendations

### REC-1: MEDIUM - Long Description
First paragraph of description.

Second paragraph of description with more detail.

Third paragraph with even more information.

- Bullet point 1
- Bullet point 2
- Bullet point 3

Final paragraph.

### REC-2: HIGH - Next Recommendation
This starts a new recommendation.
EOF

    # Should capture all text including blank lines and bullets
    # Expected: Multi-paragraph description preserved

    echo "TEST: test_extract_long_recommendation_description"
    echo "  Scenario: Recommendation with long multi-paragraph description"
    echo "  Expected: Preserve all text and formatting"
    echo "  Implementation needed: Multi-line capture until next header"
}

# Test 14: Handle recommendation with special characters in title
test_extract_recommendation_with_special_characters() {
    cat > /tmp/test-rca-special-chars.md <<'EOF'
---
id: RCA-031
title: Special Characters Test
date: 2025-12-26
severity: MEDIUM
status: OPEN
reporter: Grace Lee
---

## Recommendations

### REC-1: MEDIUM - Fix SQL "Injection" & XSS Issues (OWASP A-01)
Description here with special chars: & < > " '
EOF

    # Should handle special characters in title
    # Expected: Title extracted with special chars intact

    echo "TEST: test_extract_recommendation_with_special_characters"
    echo "  Scenario: Recommendation title with special chars"
    echo "  Expected: Extract title with &, <, >, \", ' characters preserved"
    echo "  Implementation needed: Safe character handling"
}

# Test 15: Extract recommendations in correct order from real RCA
test_extract_recommendations_real_order() {
    setup_rca_with_multiple_recommendations

    # Should verify exact order: REC-1, REC-2, REC-3, REC-4
    # Expected: [REC-1, REC-2, REC-3, REC-4]

    echo "TEST: test_extract_recommendations_real_order"
    echo "  Scenario: Verify order of extracted recommendations"
    echo "  Expected: Exact order [REC-1, REC-2, REC-3, REC-4]"
    echo "  Implementation needed: Maintain parsing order"
}

# Main test execution
main() {
    echo "=========================================="
    echo "STORY-155 AC#2: Extract Recommendations"
    echo "=========================================="
    echo ""

    test_extract_recommendation_with_all_fields
    test_extract_multiple_recommendations
    test_extract_recommendations_in_document_order
    test_extract_recommendation_id
    test_extract_recommendation_priority
    test_extract_recommendation_title
    test_extract_recommendation_description
    test_extract_no_recommendations
    test_validate_recommendation_id_format
    test_validate_recommendation_priority_enum
    test_handle_malformed_recommendation_headers
    test_detect_duplicate_recommendation_ids
    test_extract_long_recommendation_description
    test_extract_recommendation_with_special_characters
    test_extract_recommendations_real_order

    echo ""
    echo "=========================================="
    echo "All AC#2 tests generated (FAILING)"
    echo "Implementation required for all tests"
    echo "=========================================="
}

main "$@"
