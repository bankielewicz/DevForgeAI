#!/bin/bash
# Test Suite for STORY-155 AC#1: Parse RCA Frontmatter and Extract Metadata
#
# Acceptance Criteria:
# Given an RCA markdown file exists at `devforgeai/RCA/RCA-NNN-*.md` with YAML frontmatter
# When the parser reads the file and extracts frontmatter between opening and closing `---` markers
# Then the parser returns a structured object containing: id, title, date, severity, status, reporter fields

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

assert_not_empty() {
    local value="$1"
    local test_name="$2"

    if [ -n "$value" ]; then
        echo "✓ PASS: $test_name"
        return 0
    else
        echo "✗ FAIL: $test_name"
        echo "  Value was empty but should not be"
        return 1
    fi
}

# Setup: Create test RCA file with valid frontmatter
setup_valid_rca_file() {
    cat > /tmp/test-rca-valid.md <<'EOF'
---
id: RCA-022
title: Database Connection Pool Exhaustion
date: 2025-12-20
severity: CRITICAL
status: OPEN
reporter: Alice Chen
---

# RCA-022: Database Connection Pool Exhaustion

## Summary
Database connections exhausted under high load, causing service degradation.

## Root Cause
Connection pool size was too small for peak load.
EOF
}

# Setup: Create test RCA file with minimal frontmatter
setup_minimal_rca_file() {
    cat > /tmp/test-rca-minimal.md <<'EOF'
---
id: RCA-023
title: Memory Leak
date: 2025-12-21
severity: HIGH
status: RESOLVED
reporter: Bob Smith
---

Content here
EOF
}

# Setup: Create test RCA file without frontmatter
setup_rca_without_frontmatter() {
    cat > /tmp/test-rca-no-frontmatter.md <<'EOF'
# RCA-024: Missing Frontmatter

This RCA has no YAML frontmatter.
EOF
}

# Setup: Create test RCA file with malformed frontmatter
setup_rca_malformed_frontmatter() {
    cat > /tmp/test-rca-malformed.md <<'EOF'
---
id RCA-025
title: Malformed YAML
date 2025-12-22
severity CRITICAL
status: OPEN
reporter: Charlie Davis

Content without closing ---
EOF
}

# Test 1: Parse valid frontmatter and extract id field
test_parse_frontmatter_extracts_id() {
    setup_valid_rca_file

    # Should extract id from frontmatter
    # Expected: id = "RCA-022"

    # This test WILL FAIL until implementation exists
    # The parser should grep for "^id:" line and extract the value

    echo "TEST: test_parse_frontmatter_extracts_id"
    echo "  Scenario: Parse RCA with valid frontmatter"
    echo "  Expected: id field = 'RCA-022'"
    echo "  Implementation needed: grep '^id:' and extract value"
}

# Test 2: Parse valid frontmatter and extract title field
test_parse_frontmatter_extracts_title() {
    setup_valid_rca_file

    # Should extract title from frontmatter
    # Expected: title = "Database Connection Pool Exhaustion"

    echo "TEST: test_parse_frontmatter_extracts_title"
    echo "  Scenario: Parse RCA with valid frontmatter"
    echo "  Expected: title = 'Database Connection Pool Exhaustion'"
    echo "  Implementation needed: grep '^title:' and extract value"
}

# Test 3: Parse valid frontmatter and extract date field
test_parse_frontmatter_extracts_date() {
    setup_valid_rca_file

    # Should extract date from frontmatter
    # Expected: date = "2025-12-20"

    echo "TEST: test_parse_frontmatter_extracts_date"
    echo "  Scenario: Parse RCA with valid frontmatter"
    echo "  Expected: date = '2025-12-20' (YYYY-MM-DD format)"
    echo "  Implementation needed: grep '^date:' and validate format"
}

# Test 4: Parse valid frontmatter and extract severity field
test_parse_frontmatter_extracts_severity() {
    setup_valid_rca_file

    # Should extract severity from frontmatter
    # Expected: severity = "CRITICAL" (enum: CRITICAL, HIGH, MEDIUM, LOW)

    echo "TEST: test_parse_frontmatter_extracts_severity"
    echo "  Scenario: Parse RCA with valid frontmatter"
    echo "  Expected: severity = 'CRITICAL'"
    echo "  Implementation needed: grep '^severity:' and validate enum"
}

# Test 5: Parse valid frontmatter and extract status field
test_parse_frontmatter_extracts_status() {
    setup_valid_rca_file

    # Should extract status from frontmatter
    # Expected: status = "OPEN" (enum: OPEN, IN_PROGRESS, RESOLVED)

    echo "TEST: test_parse_frontmatter_extracts_status"
    echo "  Scenario: Parse RCA with valid frontmatter"
    echo "  Expected: status = 'OPEN'"
    echo "  Implementation needed: grep '^status:' and validate enum"
}

# Test 6: Parse valid frontmatter and extract reporter field
test_parse_frontmatter_extracts_reporter() {
    setup_valid_rca_file

    # Should extract reporter from frontmatter
    # Expected: reporter = "Alice Chen"

    echo "TEST: test_parse_frontmatter_extracts_reporter"
    echo "  Scenario: Parse RCA with valid frontmatter"
    echo "  Expected: reporter = 'Alice Chen'"
    echo "  Implementation needed: grep '^reporter:' and extract value"
}

# Test 7: Handle RCA file with all required fields present
test_frontmatter_with_all_required_fields() {
    setup_valid_rca_file

    # Should return complete RCADocument object with all fields
    # Expected: {id, title, date, severity, status, reporter}

    echo "TEST: test_frontmatter_with_all_required_fields"
    echo "  Scenario: Parse RCA with all required frontmatter fields"
    echo "  Expected: All fields extracted (id, title, date, severity, status, reporter)"
    echo "  Implementation needed: Complete data model assembly"
}

# Test 8: Handle RCA file with minimal fields
test_frontmatter_with_minimal_fields() {
    setup_minimal_rca_file

    # Should still parse with minimal fields
    # Expected: id, title, date, severity, status, reporter (all required per spec)

    echo "TEST: test_frontmatter_with_minimal_fields"
    echo "  Scenario: Parse RCA with minimal required fields only"
    echo "  Expected: Parser extracts all required fields"
    echo "  Implementation needed: Handle sparse YAML"
}

# Test 9: Handle RCA file with missing frontmatter (edge case)
test_frontmatter_missing_frontmatter_markers() {
    setup_rca_without_frontmatter

    # Should handle gracefully - either log warning or extract from filename
    # Expected: Error message OR extract id from filename (RCA-NNN pattern)

    echo "TEST: test_frontmatter_missing_frontmatter_markers"
    echo "  Scenario: RCA file with no YAML frontmatter (edge case)"
    echo "  Expected: Log warning and attempt fallback extraction or raise clear error"
    echo "  Implementation needed: Graceful degradation or error handling"
}

# Test 10: Handle RCA file with malformed frontmatter
test_frontmatter_malformed_yaml() {
    setup_rca_malformed_frontmatter

    # Should detect malformed YAML and report error
    # Expected: Error message indicating YAML syntax error

    echo "TEST: test_frontmatter_malformed_yaml"
    echo "  Scenario: RCA file with malformed YAML frontmatter"
    echo "  Expected: Clear error message about YAML syntax"
    echo "  Implementation needed: YAML validation and error reporting"
}

# Test 11: Validate severity enum values
test_frontmatter_severity_enum_validation() {
    # Should validate that severity is one of: CRITICAL, HIGH, MEDIUM, LOW
    # Expected: Accept valid values, reject invalid ones

    echo "TEST: test_frontmatter_severity_enum_validation"
    echo "  Scenario: Parse RCA with various severity values"
    echo "  Expected: Accept [CRITICAL, HIGH, MEDIUM, LOW], reject others"
    echo "  Implementation needed: Enum validation"
}

# Test 12: Validate status enum values
test_frontmatter_status_enum_validation() {
    # Should validate that status is one of: OPEN, IN_PROGRESS, RESOLVED
    # Expected: Accept valid values, reject invalid ones

    echo "TEST: test_frontmatter_status_enum_validation"
    echo "  Scenario: Parse RCA with various status values"
    echo "  Expected: Accept [OPEN, IN_PROGRESS, RESOLVED], reject others"
    echo "  Implementation needed: Enum validation"
}

# Test 13: Validate date format (YYYY-MM-DD)
test_frontmatter_date_format_validation() {
    # Should validate that date is in YYYY-MM-DD format
    # Expected: Accept valid dates, reject invalid formats

    echo "TEST: test_frontmatter_date_format_validation"
    echo "  Scenario: Parse RCA with various date formats"
    echo "  Expected: Accept YYYY-MM-DD, reject MM/DD/YYYY, DD-MM-YYYY, etc"
    echo "  Implementation needed: Date format validation"
}

# Test 14: Validate id format (RCA-NNN)
test_frontmatter_id_format_validation() {
    # Should validate that id is in RCA-NNN format (RCA- prefix + digits)
    # Expected: Accept "RCA-022", reject "rca-022", "RCA22", etc

    echo "TEST: test_frontmatter_id_format_validation"
    echo "  Scenario: Parse RCA with various id formats"
    echo "  Expected: Only accept RCA-[0-9]+ format"
    echo "  Implementation needed: ID format validation"
}

# Test 15: Handle empty reporter field
test_frontmatter_empty_reporter() {
    cat > /tmp/test-rca-empty-reporter.md <<'EOF'
---
id: RCA-026
title: Test Issue
date: 2025-12-20
severity: MEDIUM
status: OPEN
reporter:
---

Content
EOF

    # Should handle gracefully - either log warning or allow empty
    # Expected: Either empty string or error message

    echo "TEST: test_frontmatter_empty_reporter"
    echo "  Scenario: RCA with empty reporter field"
    echo "  Expected: Parse successfully or log clear warning"
    echo "  Implementation needed: Handle empty fields"
}

# Main test execution
main() {
    echo "=========================================="
    echo "STORY-155 AC#1: Parse RCA Frontmatter"
    echo "=========================================="
    echo ""

    test_parse_frontmatter_extracts_id
    test_parse_frontmatter_extracts_title
    test_parse_frontmatter_extracts_date
    test_parse_frontmatter_extracts_severity
    test_parse_frontmatter_extracts_status
    test_parse_frontmatter_extracts_reporter
    test_frontmatter_with_all_required_fields
    test_frontmatter_with_minimal_fields
    test_frontmatter_missing_frontmatter_markers
    test_frontmatter_malformed_yaml
    test_frontmatter_severity_enum_validation
    test_frontmatter_status_enum_validation
    test_frontmatter_date_format_validation
    test_frontmatter_id_format_validation
    test_frontmatter_empty_reporter

    echo ""
    echo "=========================================="
    echo "All AC#1 tests generated (FAILING)"
    echo "Implementation required for all tests"
    echo "=========================================="
}

main "$@"
