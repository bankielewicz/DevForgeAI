#!/bin/bash
# =============================================================================
# STORY-211: Evidence-Verification Gate Tests
# =============================================================================
# TDD Red Phase: All tests should FAIL initially (no implementation exists)
#
# Target File: .claude/skills/devforgeai-story-creation/references/technical-specification-creation.md
#
# Test Strategy:
# - Structural validation of Markdown specification file
# - Grep patterns verify required sections and content exist
# - Tests derived from both Acceptance Criteria AND Technical Specification
#
# Coverage:
# - AC#1-5: Acceptance Criteria tests (60%)
# - CFG-001 to CFG-005: Technical Specification Configuration tests
# - BR-001 to BR-003: Business Rules tests
# =============================================================================

set -uo pipefail

# =============================================================================
# Configuration
# =============================================================================
TARGET_FILE=".claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
FULL_PATH="${PROJECT_ROOT}/${TARGET_FILE}"

# Test counters (use :|| true pattern to avoid set -e issues with (( )) when value is 0)
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Increment function that doesn't fail on 0
incr_run() { TESTS_RUN=$((TESTS_RUN + 1)); }
incr_pass() { TESTS_PASSED=$((TESTS_PASSED + 1)); }
incr_fail() { TESTS_FAILED=$((TESTS_FAILED + 1)); }

# =============================================================================
# Test Library Functions
# =============================================================================

print_header() {
    echo ""
    echo "============================================================================="
    echo "  STORY-211: Evidence-Verification Gate - Test Suite"
    echo "  TDD Red Phase: Tests designed to FAIL before implementation"
    echo "============================================================================="
    echo ""
    echo "Target File: ${TARGET_FILE}"
    echo ""
}

print_test() {
    local test_name="$1"
    echo -n "  [TEST] ${test_name}... "
}

pass() {
    echo "PASS"
    incr_pass
}

fail() {
    local reason="${1:-}"
    if [[ -n "$reason" ]]; then
        echo "FAIL - ${reason}"
    else
        echo "FAIL"
    fi
    incr_fail
}

print_summary() {
    echo ""
    echo "============================================================================="
    echo "  Test Summary"
    echo "============================================================================="
    echo ""
    echo "  Tests Run:    ${TESTS_RUN}"
    echo "  Tests Passed: ${TESTS_PASSED}"
    echo "  Tests Failed: ${TESTS_FAILED}"
    echo ""
    if [[ ${TESTS_FAILED} -eq 0 ]]; then
        echo "  Status: ALL TESTS PASSED"
        exit 0
    else
        echo "  Status: ${TESTS_FAILED} TESTS FAILED (TDD Red Phase Expected)"
        exit 1
    fi
}

# =============================================================================
# Prerequisite Check
# =============================================================================

test_prerequisite_target_file_exists() {
    incr_run
    print_test "Prerequisite: Target file exists"

    if [[ -f "${FULL_PATH}" ]]; then
        pass
    else
        fail "File not found: ${FULL_PATH}"
        echo ""
        echo "CRITICAL: Cannot run tests without target file."
        echo "Ensure the file exists before running test suite."
        exit 2
    fi
}

# =============================================================================
# AC#1: Evidence-Verification Pre-Flight Section Added
# CFG-001: Evidence-Verification Pre-Flight section after line 67
# =============================================================================

test_ac1_section_exists() {
    incr_run
    print_test "AC#1: Evidence-Verification Pre-Flight section exists"

    if grep -q "Evidence-Verification Pre-Flight" "${FULL_PATH}"; then
        pass
    else
        fail "Section 'Evidence-Verification Pre-Flight' not found"
    fi
}

test_ac1_section_header_format() {
    incr_run
    print_test "AC#1: Section has proper Markdown header format (## or ###)"

    if grep -qE "^##+ .*Evidence-Verification Pre-Flight" "${FULL_PATH}"; then
        pass
    else
        fail "Section header format incorrect or missing"
    fi
}

test_ac1_section_before_step_3_0() {
    incr_run
    print_test "AC#1: Section appears before Step 3.0"

    # Get line number of Evidence-Verification section
    local ev_line
    ev_line=$(grep -n "Evidence-Verification Pre-Flight" "${FULL_PATH}" | head -1 | cut -d: -f1)

    # Get line number of Step 3.0 (actual header, not reference in list)
    local step30_line
    step30_line=$(grep -n "^## Step 3.0:" "${FULL_PATH}" | head -1 | cut -d: -f1)

    if [[ -n "${ev_line}" && -n "${step30_line}" ]]; then
        if [[ ${ev_line} -lt ${step30_line} ]]; then
            pass
        else
            fail "Section at line ${ev_line} should be before Step 3.0 at line ${step30_line}"
        fi
    else
        fail "Could not determine line positions"
    fi
}

test_ac1_section_after_line_67() {
    incr_run
    print_test "AC#1/CFG-001: Section added after line 67"

    local ev_line
    ev_line=$(grep -n "Evidence-Verification Pre-Flight" "${FULL_PATH}" | head -1 | cut -d: -f1)

    if [[ -n "${ev_line}" ]]; then
        if [[ ${ev_line} -gt 67 ]]; then
            pass
        else
            fail "Section at line ${ev_line} should be after line 67"
        fi
    else
        fail "Section not found"
    fi
}

# =============================================================================
# AC#2: Target File Identification Step
# CFG-002: Target file identification step (Step 1)
# =============================================================================

test_ac2_step1_documented() {
    incr_run
    print_test "AC#2/CFG-002: Step 1 (Target File Identification) documented"

    if grep -qE "(Step 1|Step EV-1).*[Tt]arget [Ff]ile [Ii]dentification" "${FULL_PATH}"; then
        pass
    else
        fail "Step 1 for target file identification not documented"
    fi
}

test_ac2_target_files_extraction() {
    incr_run
    print_test "AC#2: target_files extraction logic described"

    if grep -q "target_files" "${FULL_PATH}"; then
        pass
    else
        fail "target_files variable/logic not found"
    fi
}

test_ac2_extraction_from_feature_description() {
    incr_run
    print_test "AC#2: Extraction from feature description mentioned"

    if grep -qiE "(feature description|technical scope).*extract|extract.*files" "${FULL_PATH}"; then
        pass
    else
        fail "Feature description extraction not documented"
    fi
}

# =============================================================================
# AC#3: Read and Verify Each Target File
# CFG-003: Read and Verify step (Step 2) with Read() and Grep
# =============================================================================

test_ac3_step2_documented() {
    incr_run
    print_test "AC#3/CFG-003: Step 2 (Read and Verify) documented"

    if grep -qE "(Step 2|Step EV-2).*[Rr]ead.*[Vv]erify" "${FULL_PATH}"; then
        pass
    else
        fail "Step 2 for Read and Verify not documented"
    fi
}

test_ac3_read_tool_usage() {
    incr_run
    print_test "AC#3: Read() tool usage documented"

    # Look for Read(file_path in the Evidence-Verification section context
    if grep -q "Read(file_path" "${FULL_PATH}"; then
        pass
    else
        fail "Read(file_path=...) pattern not found"
    fi
}

test_ac3_grep_tool_usage() {
    incr_run
    print_test "AC#3: Grep tool usage documented"

    # Look for Grep usage for verification
    if grep -qE "Grep\(|grep.*content|search.*file" "${FULL_PATH}"; then
        pass
    else
        fail "Grep verification pattern not found"
    fi
}

test_ac3_halt_for_missing_files() {
    incr_run
    print_test "AC#3: HALT pattern for missing files"

    if grep -qE "HALT.*([Ff]ile not found|missing|does NOT exist)" "${FULL_PATH}"; then
        pass
    else
        fail "HALT pattern for missing files not found"
    fi
}

test_ac3_file_existence_check() {
    incr_run
    print_test "AC#3: File existence check documented"

    if grep -qE "(file.*does NOT exist|file.*not found|IF.*file.*exist)" "${FULL_PATH}"; then
        pass
    else
        fail "File existence check not documented"
    fi
}

# =============================================================================
# AC#4: Evidence Sufficiency Validation
# CFG-004: Evidence sufficiency validation (Step 3) with HALT pattern
# =============================================================================

test_ac4_step3_documented() {
    incr_run
    print_test "AC#4/CFG-004: Step 3 (Evidence Sufficiency) documented"

    if grep -qE "(Step 3|Step EV-3).*[Ee]vidence.*[Ss]ufficiency" "${FULL_PATH}"; then
        pass
    else
        fail "Step 3 for Evidence Sufficiency not documented"
    fi
}

test_ac4_halt_for_unverified_claims() {
    incr_run
    print_test "AC#4: HALT pattern for unverified claims"

    if grep -qE "HALT.*([Cc]annot verify|unverified|claim)" "${FULL_PATH}"; then
        pass
    else
        fail "HALT pattern for unverified claims not found"
    fi
}

test_ac4_every_claim_checked() {
    incr_run
    print_test "AC#4: Every claim verification documented"

    if grep -qiE "(every claim|all claims|each claim).*verif" "${FULL_PATH}"; then
        pass
    else
        fail "Every claim verification requirement not documented"
    fi
}

test_ac4_speculative_claim_guidance() {
    incr_run
    print_test "AC#4: Guidance for speculative claims"

    if grep -qiE "speculative|remove from story" "${FULL_PATH}"; then
        pass
    else
        fail "Speculative claim guidance not found"
    fi
}

# =============================================================================
# AC#5: verified_violations YAML Section Generated
# CFG-005: verified_violations YAML generation (Step 4)
# =============================================================================

test_ac5_step4_documented() {
    incr_run
    print_test "AC#5/CFG-005: Step 4 (verified_violations YAML) documented"

    if grep -qE "(Step 4|Step EV-4).*verified_violations" "${FULL_PATH}"; then
        pass
    else
        fail "Step 4 for verified_violations not documented"
    fi
}

test_ac5_verified_violations_section() {
    incr_run
    print_test "AC#5: verified_violations YAML section template exists"

    if grep -q "verified_violations:" "${FULL_PATH}"; then
        pass
    else
        fail "verified_violations: YAML section not found"
    fi
}

test_ac5_lines_field() {
    incr_run
    print_test "AC#5: Template includes 'lines' field"

    if grep -qE "lines:.*\[" "${FULL_PATH}"; then
        pass
    else
        fail "'lines: [N, M, O]' field format not found"
    fi
}

test_ac5_count_field() {
    incr_run
    print_test "AC#5: Template includes 'count' field"

    if grep -qE "count:.*[0-9]" "${FULL_PATH}"; then
        pass
    else
        fail "'count: N' field not found"
    fi
}

test_ac5_note_field() {
    incr_run
    print_test "AC#5: Template includes 'note' field"

    if grep -qE "note:.*\"" "${FULL_PATH}"; then
        pass
    else
        fail "'note: \"...\"' field not found"
    fi
}

test_ac5_file_field() {
    incr_run
    print_test "AC#5: Template includes 'file' field"

    if grep -qE '\- file:.*"' "${FULL_PATH}"; then
        pass
    else
        fail "'- file: ...' field not found"
    fi
}

# =============================================================================
# Business Rules Tests (from Technical Specification)
# =============================================================================

test_br001_claims_verified_before_creation() {
    incr_run
    print_test "BR-001: All claims verified before story creation documented"

    if grep -qiE "(all.*claims.*verif|verif.*before.*creat|pre-flight.*verif)" "${FULL_PATH}"; then
        pass
    else
        fail "BR-001 requirement not documented"
    fi
}

test_br002_native_tools_only() {
    incr_run
    print_test "BR-002: Native Read() and Grep() tools used (no Bash cat)"

    # Check that Read() is used AND Bash(command="cat is NOT used (actual command, not example text)
    if grep -q "Read(" "${FULL_PATH}" && ! grep -qE 'Bash\(command="cat' "${FULL_PATH}"; then
        pass
    else
        fail "BR-002: Must use native Read()/Grep() tools, not Bash"
    fi
}

test_br003_specific_line_numbers() {
    incr_run
    print_test "BR-003: Specific line numbers required (not generic)"

    if grep -qE "lines:.*\[.*[0-9]" "${FULL_PATH}"; then
        pass
    else
        fail "BR-003: Specific line numbers format not documented"
    fi
}

# =============================================================================
# Integration Tests: Section Coherence
# =============================================================================

test_integration_four_steps_exist() {
    incr_run
    print_test "Integration: All 4 Evidence-Verification steps documented"

    local step_count=0

    # Count Evidence-Verification steps (EV-1 through EV-4 or Step 1 through Step 4)
    if grep -qE "(Step 1|Step EV-1).*[Tt]arget" "${FULL_PATH}"; then step_count=$((step_count + 1)); fi
    if grep -qE "(Step 2|Step EV-2).*[Rr]ead" "${FULL_PATH}"; then step_count=$((step_count + 1)); fi
    if grep -qE "(Step 3|Step EV-3).*[Ee]vidence" "${FULL_PATH}"; then step_count=$((step_count + 1)); fi
    if grep -qE "(Step 4|Step EV-4).*verified_violations" "${FULL_PATH}"; then step_count=$((step_count + 1)); fi

    if [[ ${step_count} -eq 4 ]]; then
        pass
    else
        fail "Only ${step_count}/4 Evidence-Verification steps found"
    fi
}

test_integration_rca020_reference() {
    incr_run
    print_test "Integration: RCA-020 reference included"

    if grep -q "RCA-020" "${FULL_PATH}"; then
        pass
    else
        fail "RCA-020 reference not found in documentation"
    fi
}

test_integration_citation_requirements_reference() {
    incr_run
    print_test "Integration: Citation requirements reference included"

    if grep -qE "(citation-requirements|Read-Quote-Cite-Verify)" "${FULL_PATH}"; then
        pass
    else
        fail "Citation requirements reference not found"
    fi
}

# =============================================================================
# Main Test Execution
# =============================================================================

main() {
    print_header

    # Prerequisite
    echo "--- Prerequisite Checks ---"
    test_prerequisite_target_file_exists

    # AC#1 Tests
    echo ""
    echo "--- AC#1: Evidence-Verification Pre-Flight Section ---"
    test_ac1_section_exists
    test_ac1_section_header_format
    test_ac1_section_before_step_3_0
    test_ac1_section_after_line_67

    # AC#2 Tests
    echo ""
    echo "--- AC#2: Target File Identification Step ---"
    test_ac2_step1_documented
    test_ac2_target_files_extraction
    test_ac2_extraction_from_feature_description

    # AC#3 Tests
    echo ""
    echo "--- AC#3: Read and Verify Each Target File ---"
    test_ac3_step2_documented
    test_ac3_read_tool_usage
    test_ac3_grep_tool_usage
    test_ac3_halt_for_missing_files
    test_ac3_file_existence_check

    # AC#4 Tests
    echo ""
    echo "--- AC#4: Evidence Sufficiency Validation ---"
    test_ac4_step3_documented
    test_ac4_halt_for_unverified_claims
    test_ac4_every_claim_checked
    test_ac4_speculative_claim_guidance

    # AC#5 Tests
    echo ""
    echo "--- AC#5: verified_violations YAML Section ---"
    test_ac5_step4_documented
    test_ac5_verified_violations_section
    test_ac5_lines_field
    test_ac5_count_field
    test_ac5_note_field
    test_ac5_file_field

    # Business Rules Tests
    echo ""
    echo "--- Business Rules (from Tech Spec) ---"
    test_br001_claims_verified_before_creation
    test_br002_native_tools_only
    test_br003_specific_line_numbers

    # Integration Tests
    echo ""
    echo "--- Integration Tests ---"
    test_integration_four_steps_exist
    test_integration_rca020_reference
    test_integration_citation_requirements_reference

    print_summary
}

# Run main
main "$@"
