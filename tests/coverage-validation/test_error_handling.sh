#!/bin/bash

##############################################################################
# Test Suite: STORY-089 - Error Handling Tests (AC#3-4)
# Purpose: Test malformed epic handling and orphaned story detection
#
# Acceptance Criteria #3: Malformed Epic File Error Handling
# - Clear error message identifying the specific issue
# - Line number where error was detected
# - Fix suggestion with example of correct format
# - Non-blocking continuation for other valid epic files
#
# Acceptance Criteria #4: Orphaned Story Detection and Reporting
# - Identify stories with invalid epic_id references
# - Report as warnings (not blocking)
# - Provide suggested actions
##############################################################################

set -o pipefail

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
TEST_LOG="/tmp/story-089-error-handling.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
ERROR_HANDLER="${PROJECT_ROOT}/devforgeai/traceability/error-handler.sh"
FIXTURES_DIR="${SCRIPT_DIR}/fixtures"

# Initialize log
echo "=== STORY-089 Error Handling Test Suite ===" > "$TEST_LOG"
echo "Started: $(date)" >> "$TEST_LOG"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>> "$TEST_LOG"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓${NC} PASSED"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗${NC} FAILED"
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String should contain substring}"

    if [[ "$haystack" == *"$needle"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "String: $haystack"
        echo "Should contain: $needle"
        return 1
    fi
}

assert_exit_code() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Exit code mismatch}"

    if [[ "$expected" -eq "$actual" ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "Expected exit code: $expected"
        echo "Actual exit code: $actual"
        return 1
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String should not contain substring}"

    if [[ "$haystack" != *"$needle"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "String: $haystack"
        echo "Should NOT contain: $needle"
        return 1
    fi
}

##############################################################################
# Setup: Create Malformed Epic Fixtures
##############################################################################

setup_malformed_fixtures() {
    # Create malformed YAML epic
    cat > "${FIXTURES_DIR}/epic-malformed-yaml.md" << 'EOF'
---
epic_id: EPIC-TEST-MALFORMED
title: Malformed YAML Epic
status: Planning
priority: Medium
  invalid_indent: this is wrong
---

# Epic: Malformed YAML

## Features

### Feature 1: Test Feature

Valid feature description for testing purposes.
EOF

    # Create epic with invalid frontmatter delimiter
    cat > "${FIXTURES_DIR}/epic-no-frontmatter.md" << 'EOF'
# Epic: No Frontmatter

This epic has no YAML frontmatter delimiters.

## Features

### Feature 1: Test Feature

Valid feature description.
EOF

    # Create epic with truncated YAML
    cat > "${FIXTURES_DIR}/epic-truncated-yaml.md" << 'EOF'
---
epic_id: EPIC-TEST-TRUNCATED
title: Truncated YAML
status: Planning
EOF

    # Create story with invalid epic reference
    cat > "${FIXTURES_DIR}/story-orphaned.md" << 'EOF'
---
id: STORY-ORPHAN-001
title: Orphaned Story
epic: EPIC-999
status: Backlog
---

# Story: Orphaned Story

This story references a non-existent epic.
EOF

    # Create story with typo in epic reference
    cat > "${FIXTURES_DIR}/story-typo-epic.md" << 'EOF'
---
id: STORY-TYPO-001
title: Typo Epic Reference
epic: EPCI-015
status: Backlog
---

# Story: Typo Epic Reference

This story has a typo in epic reference (EPCI instead of EPIC).
EOF
}

# Run setup
setup_malformed_fixtures

##############################################################################
# AC#3.1: Clear Error Messages
##############################################################################

test_provides_clear_error_for_malformed_yaml() {
    # AC#3: Clear error message identifying the specific issue

    local result
    result=$("$ERROR_HANDLER" --validate "${FIXTURES_DIR}/epic-malformed-yaml.md" 2>&1)

    assert_contains "$result" "YAML" "Should mention YAML error" || return 1
    assert_contains "$result" "invalid" "Should indicate invalid content" || return 1
}

test_provides_clear_error_for_missing_frontmatter() {
    # AC#3: Clear error for missing frontmatter

    local result
    result=$("$ERROR_HANDLER" --validate "${FIXTURES_DIR}/epic-no-frontmatter.md" 2>&1)

    assert_contains "$result" "frontmatter" "Should mention missing frontmatter" || return 1
}

test_provides_clear_error_for_truncated_yaml() {
    # AC#3: Clear error for truncated YAML

    local result
    result=$("$ERROR_HANDLER" --validate "${FIXTURES_DIR}/epic-truncated-yaml.md" 2>&1)

    assert_contains "$result" "delimiter" "Should mention missing closing delimiter" || return 1
}

##############################################################################
# AC#3.2: Line Number Reporting
##############################################################################

test_reports_line_number_for_yaml_error() {
    # AC#3: Line number where error was detected

    local result
    result=$("$ERROR_HANDLER" --validate "${FIXTURES_DIR}/epic-malformed-yaml.md" 2>&1)

    # Should contain line number (e.g., "line 6" or ":6:")
    if [[ "$result" =~ [Ll]ine[[:space:]]*[0-9]+ ]] || [[ "$result" =~ :[0-9]+: ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should include line number"
        echo "Output: $result"
        return 1
    fi
}

test_reports_accurate_line_number() {
    # AC#3: Line number should be accurate to actual error location

    local result
    result=$("$ERROR_HANDLER" --validate "${FIXTURES_DIR}/epic-malformed-yaml.md" 2>&1)

    # The malformed YAML has error on line 6 (invalid_indent)
    if [[ "$result" =~ [Ll]ine[[:space:]]*[5-7] ]] || [[ "$result" =~ :[5-7]: ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Line number should be around 5-7"
        echo "Output: $result"
        return 1
    fi
}

##############################################################################
# AC#3.3: Fix Suggestions
##############################################################################

test_provides_fix_suggestion() {
    # AC#3: Fix suggestion with example of correct format

    local result
    result=$("$ERROR_HANDLER" --validate "${FIXTURES_DIR}/epic-malformed-yaml.md" 2>&1)

    # Should suggest how to fix (case-insensitive check)
    local result_lower="${result,,}"
    if [[ "$result_lower" == *"suggestion"* ]] || [[ "$result_lower" == *"fix"* ]] || [[ "$result_lower" == *"example"* ]] || [[ "$result_lower" == *"should be"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should include fix suggestion"
        echo "Output: $result"
        return 1
    fi
}

test_provides_correct_format_example() {
    # AC#3: Example of correct format

    local result
    result=$("$ERROR_HANDLER" --validate "${FIXTURES_DIR}/epic-no-frontmatter.md" 2>&1)

    # Should show correct frontmatter format
    if [[ "$result" == *"---"* ]] || [[ "$result" == *"epic_id:"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should show correct format example"
        echo "Output: $result"
        return 1
    fi
}

##############################################################################
# AC#3.4: Non-Blocking Continuation
##############################################################################

test_continues_after_malformed_file() {
    # AC#3: Non-blocking continuation for other valid epic files

    local result
    local exit_code

    # Validate directory with mixed valid/invalid files
    result=$("$ERROR_HANDLER" --validate-dir "${FIXTURES_DIR}" 2>&1)
    exit_code=$?

    # Should not exit with error code 3 (fatal error)
    if [[ $exit_code -ne 3 ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should not have fatal error exit"
        return 1
    fi
}

test_reports_count_of_valid_files() {
    # AC#3: Reports how many files validated successfully

    local result
    result=$("$ERROR_HANDLER" --validate-dir "${FIXTURES_DIR}" 2>&1)

    # Should show count of validated files
    if [[ "$result" =~ [0-9]+[[:space:]]*(valid|success|passed) ]] || [[ "$result" == *"validated"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should report count of valid files"
        echo "Output: $result"
        return 1
    fi
}

test_reports_count_of_invalid_files() {
    # AC#3: Reports how many files had errors

    local result
    result=$("$ERROR_HANDLER" --validate-dir "${FIXTURES_DIR}" 2>&1)

    # Should show count of errored files
    if [[ "$result" =~ [0-9]+[[:space:]]*(invalid|error|failed) ]] || [[ "$result" == *"error"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should report count of invalid files"
        echo "Output: $result"
        return 1
    fi
}

##############################################################################
# AC#4.1: Orphaned Story Detection
##############################################################################

test_detects_orphaned_story() {
    # AC#4: Identify stories with invalid epic_id references

    local result
    result=$("$ERROR_HANDLER" --detect-orphans "${FIXTURES_DIR}" 2>&1)

    assert_contains "$result" "STORY-ORPHAN-001" "Should identify orphaned story" || return 1
}

test_reports_invalid_epic_reference() {
    # AC#4: Report the invalid epic_id

    local result
    result=$("$ERROR_HANDLER" --detect-orphans "${FIXTURES_DIR}" 2>&1)

    assert_contains "$result" "EPIC-999" "Should report invalid epic reference" || return 1
}

test_detects_typo_in_epic_reference() {
    # AC#4: Detect typo like EPCI-015 vs EPIC-015

    local result
    result=$("$ERROR_HANDLER" --detect-orphans "${FIXTURES_DIR}" 2>&1)

    assert_contains "$result" "EPCI-015" "Should detect typo in epic reference" || return 1
}

##############################################################################
# AC#4.2: Warning (Not Blocking)
##############################################################################

test_orphans_are_warnings_not_blocking() {
    # AC#4: Report as warnings (not blocking)

    local result
    local exit_code

    result=$("$ERROR_HANDLER" --detect-orphans "${FIXTURES_DIR}" 2>&1)
    exit_code=$?

    # Exit code 1 = warnings, not 2 (blocking)
    assert_exit_code 1 "$exit_code" "Orphans should warn (exit 1), not block" || return 1

    # Case-insensitive check for "warning"
    local result_lower="${result,,}"
    if [[ "$result_lower" != *"warning"* ]]; then
        echo "ASSERTION FAILED: Should indicate warning level"
        echo "Output: $result"
        return 1
    fi
}

test_workflow_continues_with_orphans() {
    # AC#4: Workflow continues despite orphans

    local result
    local exit_code

    result=$("$ERROR_HANDLER" --validate-and-continue "${FIXTURES_DIR}" 2>&1)
    exit_code=$?

    # Should not block (exit 2) or error (exit 3)
    if [[ $exit_code -lt 2 ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Workflow should continue with orphans"
        return 1
    fi
}

##############################################################################
# AC#4.3: Suggested Actions
##############################################################################

test_suggests_actions_for_orphans() {
    # AC#4: Provide suggested actions

    local result
    result=$("$ERROR_HANDLER" --detect-orphans "${FIXTURES_DIR}" 2>&1)

    # Should suggest creating epic or updating story
    if [[ "$result" == *"create"* ]] || [[ "$result" == *"update"* ]] || [[ "$result" == *"fix"* ]] || [[ "$result" == *"action"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should suggest actions for orphans"
        echo "Output: $result"
        return 1
    fi
}

test_suggests_similar_epic_for_typo() {
    # AC#4: Suggest similar epic for typos (EPCI -> EPIC)

    local result
    result=$("$ERROR_HANDLER" --detect-orphans "${FIXTURES_DIR}" --suggest-similar 2>&1)

    # Should suggest EPIC-015 for EPCI-015 typo
    if [[ "$result" == *"EPIC-"* ]] || [[ "$result" == *"similar"* ]] || [[ "$result" == *"did you mean"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should suggest similar epic name"
        echo "Output: $result"
        return 1
    fi
}

##############################################################################
# AC#3+4: Combined Tests
##############################################################################

test_handles_mixed_errors_gracefully() {
    # Combined: Both malformed epics and orphaned stories in same run

    local result
    local exit_code

    result=$("$ERROR_HANDLER" --full-validation "${FIXTURES_DIR}" 2>&1)
    exit_code=$?

    # Should report both types of issues
    assert_contains "$result" "error" "Should report errors" || return 1

    # Should not have fatal exit
    if [[ $exit_code -ne 3 ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should handle mixed errors gracefully"
        return 1
    fi
}

test_summary_includes_all_issues() {
    # Combined: Summary should list all issues found

    local result
    result=$("$ERROR_HANDLER" --full-validation "${FIXTURES_DIR}" 2>&1)

    # Should have summary section
    if [[ "$result" == *"Summary"* ]] || [[ "$result" == *"summary"* ]] || [[ "$result" == *"Total"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should include summary of all issues"
        echo "Output: $result"
        return 1
    fi
}

##############################################################################
# Test Execution
##############################################################################

echo ""
echo "=========================================="
echo " STORY-089: Error Handling Tests"
echo " Acceptance Criteria #3-4"
echo "=========================================="
echo ""

# Check if error handler exists (will fail in RED phase)
if [[ ! -f "$ERROR_HANDLER" ]]; then
    echo -e "${YELLOW}WARNING:${NC} Error handler not found: $ERROR_HANDLER"
    echo -e "${YELLOW}This is expected during TDD RED phase${NC}"
    echo ""
fi

# AC#3: Malformed Epic Error Handling
echo -e "\n${YELLOW}--- AC#3: Clear Error Messages ---${NC}"
run_test "Provides clear error for malformed YAML" test_provides_clear_error_for_malformed_yaml
run_test "Provides clear error for missing frontmatter" test_provides_clear_error_for_missing_frontmatter
run_test "Provides clear error for truncated YAML" test_provides_clear_error_for_truncated_yaml

echo -e "\n${YELLOW}--- AC#3: Line Number Reporting ---${NC}"
run_test "Reports line number for YAML error" test_reports_line_number_for_yaml_error
run_test "Reports accurate line number" test_reports_accurate_line_number

echo -e "\n${YELLOW}--- AC#3: Fix Suggestions ---${NC}"
run_test "Provides fix suggestion" test_provides_fix_suggestion
run_test "Provides correct format example" test_provides_correct_format_example

echo -e "\n${YELLOW}--- AC#3: Non-Blocking Continuation ---${NC}"
run_test "Continues after malformed file" test_continues_after_malformed_file
run_test "Reports count of valid files" test_reports_count_of_valid_files
run_test "Reports count of invalid files" test_reports_count_of_invalid_files

# AC#4: Orphaned Story Detection
echo -e "\n${YELLOW}--- AC#4: Orphaned Story Detection ---${NC}"
run_test "Detects orphaned story" test_detects_orphaned_story
run_test "Reports invalid epic reference" test_reports_invalid_epic_reference
run_test "Detects typo in epic reference" test_detects_typo_in_epic_reference

echo -e "\n${YELLOW}--- AC#4: Warning (Not Blocking) ---${NC}"
run_test "Orphans are warnings not blocking" test_orphans_are_warnings_not_blocking
run_test "Workflow continues with orphans" test_workflow_continues_with_orphans

echo -e "\n${YELLOW}--- AC#4: Suggested Actions ---${NC}"
run_test "Suggests actions for orphans" test_suggests_actions_for_orphans
run_test "Suggests similar epic for typo" test_suggests_similar_epic_for_typo

# Combined Tests
echo -e "\n${YELLOW}--- Combined Error Handling ---${NC}"
run_test "Handles mixed errors gracefully" test_handles_mixed_errors_gracefully
run_test "Summary includes all issues" test_summary_includes_all_issues

# Summary
echo ""
echo "=========================================="
echo " Test Summary"
echo "=========================================="
echo -e "Tests Run:    ${TESTS_RUN}"
echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. See log: $TEST_LOG${NC}"
    exit 1
fi
