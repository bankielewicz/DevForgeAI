#!/bin/bash
# =============================================================================
# STORY-212: Add Citation Validation to devforgeai-story-creation Phase 7
# =============================================================================
# Test Suite: TDD Red Phase - All tests MUST FAIL initially
#
# Target File: .claude/skills/devforgeai-story-creation/references/story-validation-workflow.md
#
# Acceptance Criteria Coverage:
#   AC#1: Citation Compliance Validation section added
#   AC#2: Five validation checklist items documented
#   AC#3: HALT trigger with error message template
#   AC#4: Skip logic for documentation-only stories
#   AC#5: Integration with existing Phase 7 validation
#
# Technical Requirements Coverage:
#   CFG-001: Section header
#   CFG-002: Reference to citation-requirements.md
#   CFG-003: 5 validation checklist items
#   CFG-004: Detection logic pseudocode with FOR loop
#   CFG-005: HALT keyword and error template
#   CFG-006: Fix instructions table with 5 violation types
#   CFG-007: Skip condition for documentation stories
#   CFG-008: Position before Final Validation Summary
# =============================================================================

set -euo pipefail

# =============================================================================
# Test Configuration
# =============================================================================

TARGET_FILE="src/claude/skills/devforgeai-story-creation/references/story-validation-workflow.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_PATH="$PROJECT_ROOT/$TARGET_FILE"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# =============================================================================
# Test Utilities
# =============================================================================

log_test_start() {
    local test_name="$1"
    echo ""
    echo "----------------------------------------"
    echo "TEST: $test_name"
    echo "----------------------------------------"
}

log_pass() {
    echo "[PASS] $1"
    ((TESTS_PASSED++))
}

log_fail() {
    echo "[FAIL] $1"
    ((TESTS_FAILED++))
}

assert_file_exists() {
    if [[ -f "$1" ]]; then
        return 0
    else
        return 1
    fi
}

assert_contains() {
    local file="$1"
    local pattern="$2"
    grep -qE "$pattern" "$file" 2>/dev/null
}

assert_contains_count() {
    local file="$1"
    local pattern="$2"
    local expected_count="$3"
    local actual_count
    actual_count=$(grep -cE "$pattern" "$file" 2>/dev/null | head -1 || echo "0")
    # Handle multi-line output from grep -c
    actual_count=$(echo "$actual_count" | tr -d '[:space:]')
    [[ "$actual_count" -ge "$expected_count" ]]
}

assert_pattern_before() {
    # Check if pattern1 appears before pattern2 in file
    local file="$1"
    local pattern1="$2"
    local pattern2="$3"

    local line1 line2
    line1=$(grep -nE "$pattern1" "$file" 2>/dev/null | head -1 | cut -d: -f1)
    line2=$(grep -nE "$pattern2" "$file" 2>/dev/null | head -1 | cut -d: -f1)

    if [[ -n "$line1" && -n "$line2" && "$line1" -lt "$line2" ]]; then
        return 0
    else
        return 1
    fi
}

# =============================================================================
# PRE-FLIGHT: Target File Existence
# =============================================================================

test_target_file_exists() {
    log_test_start "test_target_file_exists"
    ((TESTS_RUN++))

    if assert_file_exists "$TARGET_PATH"; then
        log_pass "Target file exists: $TARGET_FILE"
    else
        log_fail "Target file does not exist: $TARGET_FILE"
        echo "  Expected: File should exist at $TARGET_PATH"
        echo "  Actual: File not found"
        return 1
    fi
}

# =============================================================================
# AC#1: Citation Compliance Validation Section Added
# =============================================================================

# CFG-001: Section header "## Citation Compliance Validation" or "### Citation Compliance Validation"
test_cfg001_section_header_exists() {
    log_test_start "test_cfg001_section_header_exists"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "^##+\s*Citation Compliance Validation"; then
        log_pass "CFG-001: Citation Compliance Validation section header found"
    else
        log_fail "CFG-001: Citation Compliance Validation section header NOT found"
        echo "  Expected: '## Citation Compliance Validation' or '### Citation Compliance Validation'"
        echo "  Actual: Section header not present in file"
        return 1
    fi
}

# CFG-002: Reference to .claude/rules/core/citation-requirements.md
test_cfg002_citation_requirements_reference() {
    log_test_start "test_cfg002_citation_requirements_reference"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "\.claude/rules/core/citation-requirements\.md"; then
        log_pass "CFG-002: Reference to citation-requirements.md found"
    else
        log_fail "CFG-002: Reference to citation-requirements.md NOT found"
        echo "  Expected: '.claude/rules/core/citation-requirements.md' reference"
        echo "  Actual: Reference not present in file"
        return 1
    fi
}

# AC#1: Purpose statement includes Read-Quote-Cite-Verify protocol reference
test_ac1_purpose_statement_rqcv_protocol() {
    log_test_start "test_ac1_purpose_statement_rqcv_protocol"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "[Rr]ead-[Qq]uote-[Cc]ite-[Vv]erify"; then
        log_pass "AC#1: Read-Quote-Cite-Verify protocol reference found"
    else
        log_fail "AC#1: Read-Quote-Cite-Verify protocol reference NOT found"
        echo "  Expected: Reference to 'Read-Quote-Cite-Verify' protocol"
        echo "  Actual: Protocol reference not present"
        return 1
    fi
}

# =============================================================================
# AC#2: Five Validation Checklist Items Documented
# =============================================================================

# CFG-003: 5 validation checklist items
test_cfg003_five_validation_items() {
    log_test_start "test_cfg003_five_validation_items"
    ((TESTS_RUN++))

    # Count items matching "Item 1:", "Item 2:", etc. or numbered validation items
    if assert_contains_count "$TARGET_PATH" "(Item [1-5]:|Validation Item [1-5]|\*\*Item [1-5]\*\*)" 5; then
        log_pass "CFG-003: At least 5 validation checklist items found"
    else
        log_fail "CFG-003: 5 validation checklist items NOT found"
        echo "  Expected: At least 5 items (Item 1 through Item 5)"
        echo "  Actual: Fewer than 5 validation items present"
        return 1
    fi
}

# AC#2 Item 1: verified_violations section check
test_ac2_item1_verified_violations_check() {
    log_test_start "test_ac2_item1_verified_violations_check"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "verified_violations"; then
        log_pass "AC#2 Item 1: verified_violations check documented"
    else
        log_fail "AC#2 Item 1: verified_violations check NOT documented"
        echo "  Expected: Reference to 'verified_violations' section check"
        echo "  Actual: Not found in validation items"
        return 1
    fi
}

# AC#2 Item 2: Line number format validation
test_ac2_item2_line_number_format() {
    log_test_start "test_ac2_item2_line_number_format"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "lines:.*\[.*\]|line.?numbers?.*format|array of integers"; then
        log_pass "AC#2 Item 2: Line number format validation documented"
    else
        log_fail "AC#2 Item 2: Line number format validation NOT documented"
        echo "  Expected: Line number format validation (array of integers)"
        echo "  Actual: Not found in validation items"
        return 1
    fi
}

# AC#2 Item 3: Generic descriptions check
test_ac2_item3_generic_descriptions() {
    log_test_start "test_ac2_item3_generic_descriptions"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "[Gg]eneric.*(description|claim)|specific.*count.*line"; then
        log_pass "AC#2 Item 3: Generic descriptions check documented"
    else
        log_fail "AC#2 Item 3: Generic descriptions check NOT documented"
        echo "  Expected: Check for generic descriptions requiring specific count and lines"
        echo "  Actual: Not found in validation items"
        return 1
    fi
}

# AC#2 Item 4: File path validation
test_ac2_item4_file_path_validation() {
    log_test_start "test_ac2_item4_file_path_validation"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "file.*path.*valid|validated_files_cache|file.*exist"; then
        log_pass "AC#2 Item 4: File path validation documented"
    else
        log_fail "AC#2 Item 4: File path validation NOT documented"
        echo "  Expected: File path existence validation"
        echo "  Actual: Not found in validation items"
        return 1
    fi
}

# AC#2 Item 5: Placeholder values check
test_ac2_item5_placeholder_check() {
    log_test_start "test_ac2_item5_placeholder_check"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "[Pp]laceholder|TBD|TODO"; then
        log_pass "AC#2 Item 5: Placeholder values check documented"
    else
        log_fail "AC#2 Item 5: Placeholder values check NOT documented"
        echo "  Expected: Check for placeholder values (TBD, TODO, PLACEHOLDER)"
        echo "  Actual: Not found in validation items"
        return 1
    fi
}

# CFG-004: Detection logic pseudocode with FOR loop
test_cfg004_detection_logic_for_loop() {
    log_test_start "test_cfg004_detection_logic_for_loop"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "FOR.*each.*component|for.*component.*in"; then
        log_pass "CFG-004: Detection logic with FOR loop found"
    else
        log_fail "CFG-004: Detection logic with FOR loop NOT found"
        echo "  Expected: FOR loop iterating over components in detection logic"
        echo "  Actual: FOR loop pattern not present"
        return 1
    fi
}

# =============================================================================
# AC#3: HALT Trigger for Validation Failures
# =============================================================================

# CFG-005: HALT keyword and error template
test_cfg005_halt_keyword() {
    log_test_start "test_cfg005_halt_keyword"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "HALT"; then
        log_pass "CFG-005: HALT keyword found"
    else
        log_fail "CFG-005: HALT keyword NOT found"
        echo "  Expected: 'HALT' keyword for validation failures"
        echo "  Actual: HALT keyword not present"
        return 1
    fi
}

# CFG-005: Error message template
test_cfg005_error_message_template() {
    log_test_start "test_cfg005_error_message_template"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "Citation Compliance.*Violation|Violation.*Detected"; then
        log_pass "CFG-005: Error message template found"
    else
        log_fail "CFG-005: Error message template NOT found"
        echo "  Expected: Error message template with 'Citation Compliance Violation' or similar"
        echo "  Actual: Error template not present"
        return 1
    fi
}

# AC#3: Error message contains violation type field
test_ac3_error_has_violation_type() {
    log_test_start "test_ac3_error_has_violation_type"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "\*\*Violation\*\*:|Violation:"; then
        log_pass "AC#3: Error message contains violation type field"
    else
        log_fail "AC#3: Error message violation type field NOT found"
        echo "  Expected: '**Violation:**' or 'Violation:' field in error template"
        echo "  Actual: Violation type field not present"
        return 1
    fi
}

# AC#3: Error message contains component name field
test_ac3_error_has_component_name() {
    log_test_start "test_ac3_error_has_component_name"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "\*\*Component\*\*:|Component:"; then
        log_pass "AC#3: Error message contains component name field"
    else
        log_fail "AC#3: Error message component name field NOT found"
        echo "  Expected: '**Component:**' or 'Component:' field in error template"
        echo "  Actual: Component name field not present"
        return 1
    fi
}

# AC#3: Error message contains reason field
test_ac3_error_has_reason() {
    log_test_start "test_ac3_error_has_reason"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "\*\*Reason\*\*:|Reason:"; then
        log_pass "AC#3: Error message contains reason field"
    else
        log_fail "AC#3: Error message reason field NOT found"
        echo "  Expected: '**Reason:**' or 'Reason:' field in error template"
        echo "  Actual: Reason field not present"
        return 1
    fi
}

# CFG-006: Fix instructions table with 5 violation types
test_cfg006_fix_instructions_table() {
    log_test_start "test_cfg006_fix_instructions_table"
    ((TESTS_RUN++))

    # Check for table structure with violation types and fixes
    if assert_contains "$TARGET_PATH" "\|.*Violation.*\|.*Fix|\|.*Item 1.*\||\|.*Item [1-5].*\|"; then
        log_pass "CFG-006: Fix instructions table found"
    else
        log_fail "CFG-006: Fix instructions table NOT found"
        echo "  Expected: Markdown table with violation types and fix instructions"
        echo "  Actual: Table not present"
        return 1
    fi
}

# CFG-006: Table has 5 rows for violation types
test_cfg006_table_five_violation_rows() {
    log_test_start "test_cfg006_table_five_violation_rows"
    ((TESTS_RUN++))

    # Count table rows containing Item 1-5 or violation type references
    if assert_contains_count "$TARGET_PATH" "\|.*Item [1-5].*\|" 5; then
        log_pass "CFG-006: Fix instructions table has 5 violation type rows"
    else
        log_fail "CFG-006: Fix instructions table does NOT have 5 violation type rows"
        echo "  Expected: 5 rows for Item 1 through Item 5 violations"
        echo "  Actual: Fewer than 5 violation rows in table"
        return 1
    fi
}

# =============================================================================
# AC#4: Validation Skipped for Stories Without Claims
# =============================================================================

# CFG-007: Skip condition for documentation stories
test_cfg007_skip_condition() {
    log_test_start "test_cfg007_skip_condition"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "[Ss]kip.*validation|validation.*skipped|documentation.*stor"; then
        log_pass "CFG-007: Skip condition for documentation stories documented"
    else
        log_fail "CFG-007: Skip condition for documentation stories NOT documented"
        echo "  Expected: Skip logic for documentation-only stories"
        echo "  Actual: Skip condition not present"
        return 1
    fi
}

# AC#4: Log message for skipped validation
test_ac4_skip_log_message() {
    log_test_start "test_ac4_skip_log_message"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "Log:.*skip|skipped.*log|no modification claims"; then
        log_pass "AC#4: Log message for skipped validation documented"
    else
        log_fail "AC#4: Log message for skipped validation NOT documented"
        echo "  Expected: Log message when citation validation is skipped"
        echo "  Actual: Skip log message not present"
        return 1
    fi
}

# =============================================================================
# AC#5: Integration with Existing Phase 7 Validation
# =============================================================================

# CFG-008: Position before "## Final Validation Summary"
test_cfg008_position_before_final_summary() {
    log_test_start "test_cfg008_position_before_final_summary"
    ((TESTS_RUN++))

    # Check if Citation Compliance section appears before Final Validation Summary
    # Note: Current file has "## Reference Files Used" near end, not "Final Validation Summary"
    # Test should check position relative to existing final sections
    if assert_pattern_before "$TARGET_PATH" "Citation Compliance Validation" "(Final Validation|Reference Files Used|## Output)"; then
        log_pass "CFG-008: Citation Compliance section positioned correctly"
    else
        log_fail "CFG-008: Citation Compliance section NOT positioned before final sections"
        echo "  Expected: Citation Compliance Validation appears before final summary/output sections"
        echo "  Actual: Section not found or positioned incorrectly"
        return 1
    fi
}

# AC#5: Integration with YAML structure validation (runs after)
test_ac5_runs_after_yaml_validation() {
    log_test_start "test_ac5_runs_after_yaml_validation"
    ((TESTS_RUN++))

    # Citation validation should run after YAML structure validation (Step 7.1)
    if assert_pattern_before "$TARGET_PATH" "YAML.*[Ff]rontmatter|Step 7\.1" "Citation Compliance"; then
        log_pass "AC#5: Citation validation runs after YAML structure validation"
    else
        log_fail "AC#5: Citation validation does NOT run after YAML structure validation"
        echo "  Expected: Citation Compliance section appears after YAML frontmatter validation"
        echo "  Actual: Order not correct or Citation section not found"
        return 1
    fi
}

# AC#5: Uses cached file validation from Phase 3
test_ac5_uses_phase3_cache() {
    log_test_start "test_ac5_uses_phase3_cache"
    ((TESTS_RUN++))

    if assert_contains "$TARGET_PATH" "cache|Phase 3|validated_files"; then
        log_pass "AC#5: References Phase 3 cache for file validation"
    else
        log_fail "AC#5: Phase 3 cache reference NOT found"
        echo "  Expected: Reference to using cached file validation from Phase 3"
        echo "  Actual: Cache/Phase 3 reference not present"
        return 1
    fi
}

# =============================================================================
# Test Runner
# =============================================================================

run_all_tests() {
    echo "============================================================================="
    echo "STORY-212: Citation Validation Phase 7 - Test Suite"
    echo "============================================================================="
    echo "Target: $TARGET_FILE"
    echo "Running TDD Red Phase tests (all should FAIL initially)"
    echo "============================================================================="

    # Pre-flight
    test_target_file_exists || true

    # AC#1: Citation Compliance Validation Section Added
    test_cfg001_section_header_exists || true
    test_cfg002_citation_requirements_reference || true
    test_ac1_purpose_statement_rqcv_protocol || true

    # AC#2: Five Validation Checklist Items Documented
    test_cfg003_five_validation_items || true
    test_ac2_item1_verified_violations_check || true
    test_ac2_item2_line_number_format || true
    test_ac2_item3_generic_descriptions || true
    test_ac2_item4_file_path_validation || true
    test_ac2_item5_placeholder_check || true
    test_cfg004_detection_logic_for_loop || true

    # AC#3: HALT Trigger for Validation Failures
    test_cfg005_halt_keyword || true
    test_cfg005_error_message_template || true
    test_ac3_error_has_violation_type || true
    test_ac3_error_has_component_name || true
    test_ac3_error_has_reason || true
    test_cfg006_fix_instructions_table || true
    test_cfg006_table_five_violation_rows || true

    # AC#4: Validation Skipped for Stories Without Claims
    test_cfg007_skip_condition || true
    test_ac4_skip_log_message || true

    # AC#5: Integration with Existing Phase 7 Validation
    test_cfg008_position_before_final_summary || true
    test_ac5_runs_after_yaml_validation || true
    test_ac5_uses_phase3_cache || true

    # Summary
    echo ""
    echo "============================================================================="
    echo "TEST SUMMARY"
    echo "============================================================================="
    echo "Tests Run:    $TESTS_RUN"
    echo "Tests Passed: $TESTS_PASSED"
    echo "Tests Failed: $TESTS_FAILED"
    echo "============================================================================="

    # TDD Red Phase: Tests should fail
    if [[ $TESTS_FAILED -gt 0 ]]; then
        echo ""
        echo "TDD RED PHASE: $TESTS_FAILED tests failing as expected."
        echo "Proceed to GREEN phase to implement Citation Compliance Validation."
        exit 0
    else
        echo ""
        echo "WARNING: All tests passed! This indicates:"
        echo "  1. Feature may already be implemented, OR"
        echo "  2. Tests may need adjustment"
        exit 0
    fi
}

# =============================================================================
# Main Execution
# =============================================================================

run_all_tests
