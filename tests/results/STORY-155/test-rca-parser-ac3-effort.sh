#!/bin/bash
# Test Suite for STORY-155 AC#3: Extract Effort Estimates
#
# Acceptance Criteria:
# Given a recommendation section contains an effort estimate (e.g., `**Effort Estimate:** X hours` or `**Effort Estimate:** Y story points`)
# When the parser identifies the effort field
# Then the parser returns effort_hours (integer) and effort_points (integer, optional),
# converting story points to hours using 1 point = 4 hours

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

# Setup: Create RCA with effort in hours
setup_rca_effort_hours() {
    cat > /tmp/test-rca-effort-hours.md <<'EOF'
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
Description here.

**Effort Estimate:** 8 hours

More description.

### REC-2: HIGH - Monitoring
Description.

**Effort Estimate:** 20 hours

Next content.
EOF
}

# Setup: Create RCA with effort in story points
setup_rca_effort_story_points() {
    cat > /tmp/test-rca-effort-story-points.md <<'EOF'
---
id: RCA-022
title: Test RCA
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

## Recommendations

### REC-1: CRITICAL - Design System
Description.

**Effort Estimate:** 5 story points

More info.

### REC-2: MEDIUM - Documentation
Description.

**Effort Estimate:** 3 story points

Next.
EOF
}

# Setup: Create RCA with effort in both hours and points
setup_rca_effort_both() {
    cat > /tmp/test-rca-effort-both.md <<'EOF'
---
id: RCA-022
title: Test RCA
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

## Recommendations

### REC-1: CRITICAL - Complex Task
Description.

**Effort Estimate:** 5 story points (20 hours)

More info.
EOF
}

# Setup: Create RCA with missing effort fields
setup_rca_no_effort() {
    cat > /tmp/test-rca-no-effort.md <<'EOF'
---
id: RCA-022
title: Test RCA
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

## Recommendations

### REC-1: CRITICAL - No Effort
No effort estimate provided for this recommendation.

### REC-2: HIGH - Also No Effort
This one also lacks effort estimate.
EOF
}

# Setup: Create RCA with malformed effort fields
setup_rca_malformed_effort() {
    cat > /tmp/test-rca-malformed-effort.md <<'EOF'
---
id: RCA-022
title: Test RCA
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

## Recommendations

### REC-1: CRITICAL - Bad Hours Format
Description.

**Effort Estimate:** eight hours

Next.

### REC-2: HIGH - Bad Points Format
Description.

**Effort Estimate:** five story points

Next.

### REC-3: MEDIUM - Negative Hours
Description.

**Effort Estimate:** -5 hours

### REC-4: LOW - Zero Hours
Description.

**Effort Estimate:** 0 hours
EOF
}

# Setup: Create RCA with decimal effort values
setup_rca_decimal_effort() {
    cat > /tmp/test-rca-decimal-effort.md <<'EOF'
---
id: RCA-022
title: Test RCA
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

## Recommendations

### REC-1: CRITICAL - Decimal Hours
Description.

**Effort Estimate:** 2.5 hours

Next.

### REC-2: HIGH - Decimal Points
Description.

**Effort Estimate:** 1.5 story points

Next.
EOF
}

# Setup: Create RCA with effort in variations of format
setup_rca_effort_variations() {
    cat > /tmp/test-rca-effort-variations.md <<'EOF'
---
id: RCA-022
title: Test RCA
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

## Recommendations

### REC-1: CRITICAL - Hour Singular
Description.

**Effort Estimate:** 1 hour

Next.

### REC-2: HIGH - Points Singular
Description.

**Effort Estimate:** 1 point

Next.

### REC-3: MEDIUM - Whitespace Variations
Description.

**Effort Estimate:**  8   hours

Next.

### REC-4: LOW - Different Case
Description.

**Effort Estimate:** 4 Story Points

Next.
EOF
}

# Test 1: Extract effort in hours
test_extract_effort_hours() {
    setup_rca_effort_hours

    # Should extract "8 hours" and return effort_hours=8
    # Expected: effort_hours = 8

    echo "TEST: test_extract_effort_hours"
    echo "  Scenario: Parse '**Effort Estimate:** 8 hours'"
    echo "  Expected: effort_hours = 8"
    echo "  Implementation needed: Regex to extract number and 'hours' keyword"
}

# Test 2: Extract effort in story points
test_extract_effort_story_points() {
    setup_rca_effort_story_points

    # Should extract "5 story points" and return effort_points=5
    # Expected: effort_points = 5

    echo "TEST: test_extract_effort_story_points"
    echo "  Scenario: Parse '**Effort Estimate:** 5 story points'"
    echo "  Expected: effort_points = 5"
    echo "  Implementation needed: Regex to extract number and 'story points' keyword"
}

# Test 3: Convert story points to hours (1 point = 4 hours)
test_convert_story_points_to_hours() {
    setup_rca_effort_story_points

    # Should convert story points to hours: 5 points * 4 = 20 hours
    # Expected: effort_hours = 20 (calculated), effort_points = 5 (original)

    echo "TEST: test_convert_story_points_to_hours"
    echo "  Scenario: Parse '5 story points' and convert to hours"
    echo "  Expected: effort_points = 5, effort_hours = 20 (5 * 4)"
    echo "  Implementation needed: BR-003 Story Point Conversion (1 point = 4 hours)"
}

# Test 4: Handle both hours and points in single field
test_extract_effort_both_hours_and_points() {
    setup_rca_effort_both

    # Should extract both: 5 story points AND 20 hours
    # Expected: effort_points = 5, effort_hours = 20

    echo "TEST: test_extract_effort_both_hours_and_points"
    echo "  Scenario: Parse '**Effort Estimate:** 5 story points (20 hours)'"
    echo "  Expected: effort_points = 5, effort_hours = 20"
    echo "  Implementation needed: Extract both from combined format"
}

# Test 5: Handle missing effort estimate (optional field)
test_extract_missing_effort_estimate() {
    setup_rca_no_effort

    # Should handle gracefully - return null/empty for effort fields
    # Expected: effort_hours = null, effort_points = null

    echo "TEST: test_extract_missing_effort_estimate"
    echo "  Scenario: Recommendation with no effort estimate field"
    echo "  Expected: effort_hours = null, effort_points = null (no error)"
    echo "  Implementation needed: Handle optional field gracefully"
}

# Test 6: Validate effort values are positive integers
test_validate_effort_positive() {
    setup_rca_malformed_effort

    # Should validate effort >= 1
    # Expected: Accept positive values, reject 0 and negative

    echo "TEST: test_validate_effort_positive"
    echo "  Scenario: Validate effort values are positive integers"
    echo "  Expected: Accept 1, 2, 3..., reject -5, 0"
    echo "  Implementation needed: Range validation (minimum: 1)"
}

# Test 7: Handle decimal hour values
test_handle_decimal_hours() {
    setup_rca_decimal_effort

    # Should handle 2.5 hours - either round or accept decimals
    # Expected: effort_hours = 2 or 3 (rounded) OR 2.5 (if decimals allowed)

    echo "TEST: test_handle_decimal_hours"
    echo "  Scenario: Parse '2.5 hours' (decimal)"
    echo "  Expected: Accept decimal or round to integer"
    echo "  Implementation needed: Decimal handling strategy"
}

# Test 8: Handle decimal story point values
test_handle_decimal_story_points() {
    setup_rca_decimal_effort

    # Should handle 1.5 story points - typically not allowed
    # Expected: Either reject or convert to hours (1.5 * 4 = 6)

    echo "TEST: test_handle_decimal_story_points"
    echo "  Scenario: Parse '1.5 story points' (decimal)"
    echo "  Expected: Convert to hours (6) or validate that points should be integer"
    echo "  Implementation needed: Decimal handling for points"
}

# Test 9: Handle singular/plural variations ("hour" vs "hours")
test_handle_singular_hour_format() {
    setup_rca_effort_variations

    # Should handle "1 hour" (singular) as well as "8 hours"
    # Expected: effort_hours = 1 from "1 hour"

    echo "TEST: test_handle_singular_hour_format"
    echo "  Scenario: Parse '1 hour' (singular form)"
    echo "  Expected: effort_hours = 1"
    echo "  Implementation needed: Case-insensitive regex supporting singular/plural"
}

# Test 10: Handle singular/plural variations ("point" vs "points")
test_handle_singular_point_format() {
    setup_rca_effort_variations

    # Should handle "1 point" (singular) as well as "5 story points"
    # Expected: effort_points = 1 from "1 point"

    echo "TEST: test_handle_singular_point_format"
    echo "  Scenario: Parse '1 point' (singular form)"
    echo "  Expected: effort_points = 1"
    echo "  Implementation needed: Case-insensitive regex supporting singular/plural"
}

# Test 11: Handle extra whitespace in effort field
test_handle_whitespace_in_effort() {
    setup_rca_effort_variations

    # Should handle "  8   hours" (extra whitespace)
    # Expected: effort_hours = 8 (whitespace trimmed)

    echo "TEST: test_handle_whitespace_in_effort"
    echo "  Scenario: Parse '  8   hours' (extra whitespace)"
    echo "  Expected: effort_hours = 8 (trim whitespace)"
    echo "  Implementation needed: Trim whitespace before parsing"
}

# Test 12: Handle case-insensitive matching
test_handle_case_insensitive_effort() {
    setup_rca_effort_variations

    # Should handle "Story Points" with capital S and P
    # Expected: effort_points = 4 (case-insensitive match)

    echo "TEST: test_handle_case_insensitive_effort"
    echo "  Scenario: Parse '4 Story Points' (capital S and P)"
    echo "  Expected: effort_points = 4 (case-insensitive)"
    echo "  Implementation needed: Case-insensitive regex"
}

# Test 13: Handle text with non-numeric characters
test_handle_malformed_numeric_effort() {
    setup_rca_malformed_effort

    # Should handle "eight hours" (spelled out) - either error or reject
    # Expected: Either error message or skip field

    echo "TEST: test_handle_malformed_numeric_effort"
    echo "  Scenario: Parse 'eight hours' (spelled out, not numeric)"
    echo "  Expected: Clear error or skip field"
    echo "  Implementation needed: Validate numeric format"
}

# Test 14: Validate conversion calculation (5 points = 20 hours)
test_conversion_calculation() {
    # Multiple conversions to verify math
    # 1 point = 4 hours
    # 3 points = 12 hours
    # 5 points = 20 hours
    # 10 points = 40 hours

    echo "TEST: test_conversion_calculation"
    echo "  Scenario: Verify BR-003 conversion: 1 point = 4 hours"
    echo "  Expected: 1->4, 3->12, 5->20, 10->40 hours"
    echo "  Implementation needed: Correct multiplication (BR-003)"
}

# Test 15: Extract effort from recommendation with effort BEFORE description
test_effort_field_location() {
    cat > /tmp/test-rca-effort-location.md <<'EOF'
---
id: RCA-022
title: Test RCA
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

## Recommendations

### REC-1: CRITICAL - Field at Top
**Effort Estimate:** 8 hours

Description comes after effort field.
This is the main description.

### REC-2: HIGH - Field in Middle
First paragraph of description.

**Effort Estimate:** 12 hours

Second paragraph after effort field.

### REC-3: MEDIUM - Field at End
Description here.

**Effort Estimate:** 4 hours
EOF

    # Should find effort field regardless of position in recommendation
    # Expected: Extract effort from top, middle, or end of recommendation

    echo "TEST: test_effort_field_location"
    echo "  Scenario: Effort field in different positions within recommendation"
    echo "  Expected: Extract effort from any position (top, middle, end)"
    echo "  Implementation needed: Search entire recommendation block for effort line"
}

# Main test execution
main() {
    echo "=========================================="
    echo "STORY-155 AC#3: Extract Effort Estimates"
    echo "=========================================="
    echo ""

    test_extract_effort_hours
    test_extract_effort_story_points
    test_convert_story_points_to_hours
    test_extract_effort_both_hours_and_points
    test_extract_missing_effort_estimate
    test_validate_effort_positive
    test_handle_decimal_hours
    test_handle_decimal_story_points
    test_handle_singular_hour_format
    test_handle_singular_point_format
    test_handle_whitespace_in_effort
    test_handle_case_insensitive_effort
    test_handle_malformed_numeric_effort
    test_conversion_calculation
    test_effort_field_location

    echo ""
    echo "=========================================="
    echo "All AC#3 tests generated (FAILING)"
    echo "Implementation required for all tests"
    echo "=========================================="
}

main "$@"
