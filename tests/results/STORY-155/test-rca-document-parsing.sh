#!/bin/bash

###############################################################################
# STORY-155: RCA Document Parsing - Failing Test Suite
# Purpose: Test-Driven Development (TDD) Red Phase
# Test Framework: Bash (native to DevForgeAI command execution)
#
# This test file contains FAILING tests that define the behavior expected
# from the RCA document parser before implementation begins.
#
# Pattern: test_<function>_<scenario>_<expected>
###############################################################################

set -euo pipefail

# Color output for readability
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_FAILED=0
TESTS_PASSED=0

# Test utilities
assert_equals() {
    local actual="$1"
    local expected="$2"
    local message="$3"

    if [[ "$actual" == "$expected" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: $message"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $message"
        echo "  Expected: $expected"
        echo "  Actual:   $actual"
        ((TESTS_FAILED++))
    fi
    ((TESTS_RUN++))
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="$3"

    if [[ "$haystack" == *"$needle"* ]]; then
        echo -e "${GREEN}✓ PASS${NC}: $message"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $message"
        echo "  Expected to contain: $needle"
        echo "  Actual: $haystack"
        ((TESTS_FAILED++))
    fi
    ((TESTS_RUN++))
}

assert_not_empty() {
    local value="$1"
    local message="$2"

    if [[ -n "$value" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: $message"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $message (value is empty)"
        ((TESTS_FAILED++))
    fi
    ((TESTS_RUN++))
}

assert_array_length() {
    local array_output="$1"
    local expected_length="$2"
    local message="$3"

    # Count lines in output (simple approximation)
    local actual_length=$(echo "$array_output" | grep -c . || echo "0")

    if [[ "$actual_length" == "$expected_length" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: $message"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $message"
        echo "  Expected length: $expected_length"
        echo "  Actual length: $actual_length"
        ((TESTS_FAILED++))
    fi
    ((TESTS_RUN++))
}

assert_exit_code_zero() {
    local exit_code="$1"
    local message="$2"

    if [[ "$exit_code" == "0" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: $message"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: $message (exit code: $exit_code)"
        ((TESTS_FAILED++))
    fi
    ((TESTS_RUN++))
}

###############################################################################
# TEST FIXTURES: Sample RCA files for testing
###############################################################################

create_valid_rca_file() {
    cat > /tmp/RCA-001-test.md << 'EOF'
---
id: RCA-001
title: Test RCA Document
date: 2025-12-25
severity: HIGH
status: OPEN
reporter: test-engineer
---

# Root Cause Analysis: Test RCA

This is a test RCA document for validation.

### REC-1: CRITICAL - Implement Critical Feature

This recommendation addresses a critical system issue that must be resolved immediately.

**Effort Estimate:** 8 hours

**Success Criteria:**
- [ ] Core feature implemented
- [ ] Tests passing
- [ ] Performance validated

### REC-2: HIGH - Add Documentation

This recommendation improves documentation quality and developer experience.

**Effort Estimate:** 3 story points

**Success Criteria:**
- [ ] Documentation written
- [ ] Examples provided

### REC-3: MEDIUM - Refactor Legacy Code

This recommendation improves code quality through refactoring.

**Effort Estimate:** 5 hours

**Success Criteria:**
- [ ] Refactoring complete
- [ ] Tests still passing
- [ ] No performance regression

### REC-4: LOW - Minor Optimization

This is a low-priority optimization task.

**Effort Estimate:** 1 hour

EOF
    echo "/tmp/RCA-001-test.md"
}

create_rca_with_missing_frontmatter() {
    cat > /tmp/RCA-002-no-frontmatter.md << 'EOF'
# Root Cause Analysis Without Frontmatter

This RCA document has no YAML frontmatter.

### REC-1: HIGH - Some Recommendation

This is a test recommendation.

**Effort Estimate:** 2 hours

EOF
    echo "/tmp/RCA-002-no-frontmatter.md"
}

create_rca_with_no_recommendations() {
    cat > /tmp/RCA-003-no-recs.md << 'EOF'
---
id: RCA-003
title: RCA With No Recommendations
date: 2025-12-25
severity: MEDIUM
status: OPEN
reporter: test-engineer
---

# Root Cause Analysis: No Recommendations

This RCA document has no recommendation sections, only analysis.

This document provides an analysis of the issue but does not include specific recommendations.

EOF
    echo "/tmp/RCA-003-no-recs.md"
}

create_rca_with_missing_effort() {
    cat > /tmp/RCA-004-no-effort.md << 'EOF'
---
id: RCA-004
title: RCA With Missing Effort Estimates
date: 2025-12-25
severity: HIGH
status: OPEN
reporter: test-engineer
---

# Root Cause Analysis: Missing Effort

### REC-1: HIGH - Recommendation Without Effort

This recommendation has no effort estimate specified.

No effort estimate provided for this task.

**Success Criteria:**
- [ ] Task completed

### REC-2: CRITICAL - Another Task With Effort

This one has effort.

**Effort Estimate:** 4 hours

**Success Criteria:**
- [ ] Done

EOF
    echo "/tmp/RCA-004-no-effort.md"
}

create_rca_with_malformed_priority() {
    cat > /tmp/RCA-005-malformed-priority.md << 'EOF'
---
id: RCA-005
title: RCA With Malformed Priority
date: 2025-12-25
severity: HIGH
status: OPEN
reporter: test-engineer
---

# Root Cause Analysis: Malformed Priority

### REC-1: INVALID_PRIORITY - Bad Priority

This recommendation has an invalid priority value.

**Effort Estimate:** 2 hours

### REC-2: URGENT - Non-Standard Priority

This uses a priority not in the enum.

**Effort Estimate:** 3 hours

EOF
    echo "/tmp/RCA-005-malformed-priority.md"
}

create_rca_with_special_characters() {
    cat > /tmp/RCA-006-special-chars.md << 'EOF'
---
id: RCA-006
title: RCA with **Special** Characters & Symbols
date: 2025-12-25
severity: CRITICAL
status: OPEN
reporter: test-engineer
---

# Root Cause Analysis: Special Characters

### REC-1: CRITICAL - Fix *Critical* Bug in `Parser.ts`

This recommendation has markdown formatting in the title.

**Effort Estimate:** 6 hours

**Success Criteria:**
- [ ] Bug fixed in `Parser.ts` module
- [ ] Tests in `tests/parser.test.ts` passing

EOF
    echo "/tmp/RCA-006-special-chars.md"
}

###############################################################################
# AC#1 TESTS: Parse RCA Frontmatter and Extract Metadata
###############################################################################

echo -e "\n${YELLOW}=== AC#1: Parse RCA Frontmatter and Extract Metadata ===${NC}"

test_parse_rca_frontmatter_extracts_id() {
    local rca_file=$(create_valid_rca_file)
    # This test would call the actual parser function
    # For now, we assume a function called parse_rca_metadata exists
    # local result=$(parse_rca_metadata "$rca_file" | grep '"id"')
    # The function doesn't exist yet, so this test FAILS
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Parse RCA frontmatter should extract id field"
    echo "  Reason: parse_rca_metadata() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_parse_rca_frontmatter_extracts_title() {
    local rca_file=$(create_valid_rca_file)
    # Test that parser extracts title from YAML frontmatter
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Parse RCA frontmatter should extract title field"
    echo "  Reason: parse_rca_metadata() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_parse_rca_frontmatter_extracts_date() {
    local rca_file=$(create_valid_rca_file)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Parse RCA frontmatter should extract date field (YYYY-MM-DD)"
    echo "  Reason: parse_rca_metadata() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_parse_rca_frontmatter_extracts_severity() {
    local rca_file=$(create_valid_rca_file)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Parse RCA frontmatter should extract severity (CRITICAL/HIGH/MEDIUM/LOW)"
    echo "  Reason: parse_rca_metadata() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_parse_rca_frontmatter_extracts_status() {
    local rca_file=$(create_valid_rca_file)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Parse RCA frontmatter should extract status (OPEN/IN_PROGRESS/RESOLVED)"
    echo "  Reason: parse_rca_metadata() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_parse_rca_frontmatter_extracts_reporter() {
    local rca_file=$(create_valid_rca_file)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Parse RCA frontmatter should extract reporter field"
    echo "  Reason: parse_rca_metadata() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_parse_rca_frontmatter_missing_frontmatter_extracts_id_from_filename() {
    local rca_file=$(create_rca_with_missing_frontmatter)
    # Edge case: Extract ID from filename when frontmatter missing
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Parse RCA should extract ID from filename when frontmatter missing"
    echo "  Reason: parse_rca_metadata() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_parse_rca_frontmatter_missing_frontmatter_logs_warning() {
    local rca_file=$(create_rca_with_missing_frontmatter)
    # Edge case: Log warning when frontmatter missing
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Parser should log warning when RCA frontmatter is missing"
    echo "  Reason: parse_rca_metadata() and logging not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

###############################################################################
# AC#2 TESTS: Extract Recommendations with Priority Levels
###############################################################################

echo -e "\n${YELLOW}=== AC#2: Extract Recommendations with Priority Levels ===${NC}"

test_extract_recommendations_identifies_all_rec_sections() {
    local rca_file=$(create_valid_rca_file)
    # Should extract all ### REC-N: sections
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract recommendations should identify all ### REC-N: sections"
    echo "  Reason: extract_recommendations() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_recommendations_extracts_recommendation_id() {
    local rca_file=$(create_valid_rca_file)
    # Should extract REC-1, REC-2, REC-3, REC-4 from headers
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract recommendations should extract recommendation ID (REC-N)"
    echo "  Reason: extract_recommendations() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_recommendations_extracts_priority() {
    local rca_file=$(create_valid_rca_file)
    # Should extract CRITICAL, HIGH, MEDIUM, LOW from headers
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract recommendations should extract priority from header"
    echo "  Reason: extract_recommendations() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_recommendations_extracts_title() {
    local rca_file=$(create_valid_rca_file)
    # Should extract title after priority in header
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract recommendations should extract title after priority"
    echo "  Reason: extract_recommendations() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_recommendations_extracts_description() {
    local rca_file=$(create_valid_rca_file)
    # Should extract description from recommendation body
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract recommendations should extract description from body"
    echo "  Reason: extract_recommendations() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_recommendations_returns_document_order() {
    local rca_file=$(create_valid_rca_file)
    # Should return recommendations in document order (REC-1, REC-2, REC-3, REC-4)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract recommendations should return in document order"
    echo "  Reason: extract_recommendations() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_recommendations_no_recommendations_returns_empty_array() {
    local rca_file=$(create_rca_with_no_recommendations)
    # Edge case: No ### REC-N: sections should return empty array
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract recommendations should return empty array when no REC sections"
    echo "  Reason: extract_recommendations() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

###############################################################################
# AC#3 TESTS: Extract Effort Estimates
###############################################################################

echo -e "\n${YELLOW}=== AC#3: Extract Effort Estimates ===${NC}"

test_extract_effort_parses_hours() {
    local rca_file=$(create_valid_rca_file)
    # Should parse "**Effort Estimate:** 8 hours" as 8
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract effort should parse hours from effort estimate"
    echo "  Reason: extract_effort() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_effort_parses_story_points() {
    local rca_file=$(create_valid_rca_file)
    # Should parse "**Effort Estimate:** 3 story points" as 3 points
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract effort should parse story points from effort estimate"
    echo "  Reason: extract_effort() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_effort_converts_points_to_hours() {
    # Should convert 3 story points to 12 hours (3 * 4)
    # REC-2 in valid RCA has "3 story points" → should become 12 hours
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract effort should convert story points to hours (1pt=4hrs)"
    echo "  Reason: extract_effort() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_effort_returns_effort_hours_integer() {
    local rca_file=$(create_valid_rca_file)
    # Should return effort_hours as integer
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract effort should return effort_hours as integer"
    echo "  Reason: extract_effort() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_effort_returns_effort_points_integer() {
    local rca_file=$(create_valid_rca_file)
    # Should return effort_points as integer when provided
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract effort should return effort_points as integer when provided"
    echo "  Reason: extract_effort() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_effort_missing_effort_returns_null() {
    local rca_file=$(create_rca_with_missing_effort)
    # Edge case: No effort estimate → return null for effort_hours
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract effort should return null when effort estimate missing"
    echo "  Reason: extract_effort() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_effort_missing_effort_handles_gracefully() {
    local rca_file=$(create_rca_with_missing_effort)
    # Edge case: No effort estimate → should not crash, return null
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract effort should handle missing estimates gracefully"
    echo "  Reason: extract_effort() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

###############################################################################
# AC#4 TESTS: Extract Success Criteria
###############################################################################

echo -e "\n${YELLOW}=== AC#4: Extract Success Criteria ===${NC}"

test_extract_success_criteria_identifies_subsection() {
    local rca_file=$(create_valid_rca_file)
    # Should identify **Success Criteria:** subsections
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract success criteria should identify **Success Criteria:** subsections"
    echo "  Reason: extract_success_criteria() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_success_criteria_parses_checklist_items() {
    local rca_file=$(create_valid_rca_file)
    # Should parse "- [ ] item" format checklist items
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract success criteria should parse checklist items (- [ ] format)"
    echo "  Reason: extract_success_criteria() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_success_criteria_extracts_clean_text() {
    local rca_file=$(create_valid_rca_file)
    # Should extract clean text without "- [ ] " prefix
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract success criteria should extract clean text items"
    echo "  Reason: extract_success_criteria() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_success_criteria_associates_with_parent() {
    local rca_file=$(create_valid_rca_file)
    # Should associate criteria with parent recommendation
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract success criteria should associate with parent recommendation"
    echo "  Reason: extract_success_criteria() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_success_criteria_returns_list() {
    local rca_file=$(create_valid_rca_file)
    # Should return criteria as array/list
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract success criteria should return as array"
    echo "  Reason: extract_success_criteria() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_extract_success_criteria_multiple_items() {
    local rca_file=$(create_valid_rca_file)
    # REC-1 has 3 success criteria items, should extract all
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Extract success criteria should handle multiple items"
    echo "  Reason: extract_success_criteria() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

###############################################################################
# AC#5 TESTS: Filter Recommendations by Effort Threshold
###############################################################################

echo -e "\n${YELLOW}=== AC#5: Filter Recommendations by Effort Threshold ===${NC}"

test_filter_recommendations_applies_threshold() {
    local rca_file=$(create_valid_rca_file)
    # Filter with threshold=2 should exclude REC-4 (1 hour < 2)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Filter recommendations should apply effort threshold"
    echo "  Reason: filter_recommendations() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_filter_recommendations_includes_equal_threshold() {
    local rca_file=$(create_valid_rca_file)
    # Filter with threshold=1 should include REC-4 (effort=1 >= 1)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Filter recommendations should include recommendations equal to threshold"
    echo "  Reason: filter_recommendations() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_filter_recommendations_excludes_below_threshold() {
    local rca_file=$(create_valid_rca_file)
    # Filter with threshold=2 should exclude REC-4 (1 hour < 2)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Filter recommendations should exclude recommendations below threshold"
    echo "  Reason: filter_recommendations() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_filter_recommendations_sorts_by_priority() {
    local rca_file=$(create_valid_rca_file)
    # Should sort: CRITICAL > HIGH > MEDIUM > LOW
    # Order should be: REC-1 (CRITICAL), REC-2 (HIGH), REC-3 (MEDIUM)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Filter recommendations should sort by priority (CRITICAL > HIGH > MEDIUM > LOW)"
    echo "  Reason: filter_recommendations() and sort_by_priority() functions not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_filter_recommendations_critical_first() {
    local rca_file=$(create_valid_rca_file)
    # CRITICAL priority should come first
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Filter recommendations should place CRITICAL priority first"
    echo "  Reason: filter_recommendations() sorting not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_filter_recommendations_high_second() {
    local rca_file=$(create_valid_rca_file)
    # HIGH priority should come after CRITICAL
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Filter recommendations should place HIGH priority second"
    echo "  Reason: filter_recommendations() sorting not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_filter_recommendations_medium_third() {
    local rca_file=$(create_valid_rca_file)
    # MEDIUM priority should come after HIGH
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Filter recommendations should place MEDIUM priority third"
    echo "  Reason: filter_recommendations() sorting not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_filter_recommendations_low_last() {
    local rca_file=$(create_valid_rca_file)
    # LOW priority should come last
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Filter recommendations should place LOW priority last"
    echo "  Reason: filter_recommendations() sorting not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_filter_recommendations_with_story_points() {
    local rca_file=$(create_valid_rca_file)
    # REC-2 has 3 story points = 12 hours
    # Filter with threshold=2 should include REC-2 (12 >= 2)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Filter recommendations should convert story points for threshold comparison"
    echo "  Reason: filter_recommendations() and conversion not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

###############################################################################
# BUSINESS RULE TESTS
###############################################################################

echo -e "\n${YELLOW}=== Business Rule Tests ===${NC}"

test_br001_effort_threshold_filter() {
    local rca_file=$(create_valid_rca_file)
    # BR-001: Only recommendations with effort >= threshold returned
    # With threshold=2: Should exclude REC-4 (1 hour)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: BR-001: Effort threshold filter should exclude effort < threshold"
    echo "  Reason: Business rule enforcement not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_br002_priority_sorting() {
    local rca_file=$(create_valid_rca_file)
    # BR-002: Results sorted by priority (CRITICAL > HIGH > MEDIUM > LOW)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: BR-002: Priority sorting should order CRITICAL > HIGH > MEDIUM > LOW"
    echo "  Reason: Business rule enforcement not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_br003_story_point_conversion() {
    # BR-003: Convert story points to hours using 1 point = 4 hours
    # REC-2 has "3 story points" → should become 12 hours for threshold
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: BR-003: Story point conversion (1pt=4hrs) should apply"
    echo "  Reason: Business rule enforcement not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

###############################################################################
# EDGE CASE TESTS
###############################################################################

echo -e "\n${YELLOW}=== Edge Case Tests ===${NC}"

test_edge_case_missing_frontmatter() {
    local rca_file=$(create_rca_with_missing_frontmatter)
    # Edge case 1: Extract ID from filename when frontmatter missing
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Edge case: Missing frontmatter should extract ID from filename (RCA-002)"
    echo "  Reason: Edge case handling not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_edge_case_no_recommendations() {
    local rca_file=$(create_rca_with_no_recommendations)
    # Edge case 2: No recommendations should return empty array
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Edge case: No recommendations should return empty array"
    echo "  Reason: Edge case handling not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_edge_case_missing_effort_estimate() {
    local rca_file=$(create_rca_with_missing_effort)
    # Edge case 3: Missing effort should return null, not crash
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Edge case: Missing effort estimate should return null gracefully"
    echo "  Reason: Edge case handling not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_edge_case_malformed_priority_defaults_medium() {
    local rca_file=$(create_rca_with_malformed_priority)
    # Edge case 4: Invalid priority should default to MEDIUM
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Edge case: Malformed priority should default to MEDIUM"
    echo "  Reason: Edge case handling not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_edge_case_malformed_priority_logs_warning() {
    local rca_file=$(create_rca_with_malformed_priority)
    # Edge case 4: Malformed priority should log warning
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Edge case: Malformed priority should log warning message"
    echo "  Reason: Logging not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_edge_case_special_characters_in_title() {
    local rca_file=$(create_rca_with_special_characters)
    # Edge case 6: Title with markdown formatting should extract clean text
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Edge case: Special characters in title should extract clean text"
    echo "  Reason: Text extraction not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_edge_case_code_references_in_success_criteria() {
    local rca_file=$(create_rca_with_special_characters)
    # Edge case: Code references like `Parser.ts` in success criteria
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: Edge case: Code references in success criteria should preserve formatting"
    echo "  Reason: Text extraction not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

###############################################################################
# NON-FUNCTIONAL REQUIREMENT TESTS
###############################################################################

echo -e "\n${YELLOW}=== Non-Functional Requirement Tests ===${NC}"

test_nfr_performance_parse_under_500ms() {
    local rca_file=$(create_valid_rca_file)
    # NFR: Parse time <500ms per RCA file
    local start_time=$(date +%s%N)
    # local result=$(parse_rca_document "$rca_file")
    local end_time=$(date +%s%N)
    local elapsed_ms=$(( (end_time - start_time) / 1000000 ))

    echo -e "${RED}✗ FAIL${NC}: NFR: Parse should complete in <500ms (parser not implemented)"
    echo "  Reason: parse_rca_document() function not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

test_nfr_reliability_handles_malformed_sections() {
    local rca_file=$(create_rca_with_missing_effort)
    # NFR: Graceful degradation on malformed sections (partial results with warnings)
    local result=""  # Parser function not implemented yet

    echo -e "${RED}✗ FAIL${NC}: NFR: Parser should handle malformed sections gracefully"
    echo "  Reason: Error handling not implemented"
    ((TESTS_FAILED++))
    ((TESTS_RUN++))
}

###############################################################################
# TEST SUMMARY AND RESULTS
###############################################################################

echo -e "\n${YELLOW}=== TEST SUMMARY ===${NC}"
echo "Total tests run: $TESTS_RUN"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo -e "\nExpected: All $TESTS_RUN tests FAIL (TDD Red Phase)"
echo "Reason: RCA parser functions not yet implemented"

# Exit with non-zero status (all tests should fail in TDD Red phase)
if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "\n${GREEN}✓ SUCCESS: All tests failed as expected in TDD Red phase${NC}"
    echo "Next: Implement RCA parser to make tests pass (TDD Green phase)"
    exit 0  # Report success since we expected failures
else
    echo -e "\n${RED}✗ FAILURE: Tests did not fail as expected${NC}"
    exit 1
fi
