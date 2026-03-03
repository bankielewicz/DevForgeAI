#!/bin/bash
# =============================================================================
# STORY-205: Subagent Design Guidance Document Tests
# =============================================================================
# Test Type: Verification tests for documentation story
# Test Framework: Bash (Claude Code native)
# Target File: .claude/SUBAGENT-DESIGN-GUIDE.md
#
# TDD Phase: RED - These tests MUST fail initially (document doesn't exist yet)
# =============================================================================

set -uo pipefail

# -----------------------------------------------------------------------------
# Test Configuration
# -----------------------------------------------------------------------------
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/.claude/SUBAGENT-DESIGN-GUIDE.md"
TEST_NAME="STORY-205 Subagent Design Guide Tests"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# -----------------------------------------------------------------------------
# Test Helper Functions
# -----------------------------------------------------------------------------

# Print test header
print_header() {
    echo ""
    echo "============================================================================="
    echo "${TEST_NAME}"
    echo "============================================================================="
    echo "Target File: ${TARGET_FILE}"
    echo "Test Run: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "-----------------------------------------------------------------------------"
}

# Print test result
print_result() {
    local test_name="$1"
    local status="$2"
    local details="${3:-}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ "${status}" == "PASS" ]]; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo "[PASS] ${test_name}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo "[FAIL] ${test_name}"
        if [[ -n "${details}" ]]; then
            echo "       Details: ${details}"
        fi
    fi
}

# Print test summary
print_summary() {
    echo ""
    echo "-----------------------------------------------------------------------------"
    echo "Test Summary"
    echo "-----------------------------------------------------------------------------"
    echo "Tests Run:    ${TESTS_RUN}"
    echo "Tests Passed: ${TESTS_PASSED}"
    echo "Tests Failed: ${TESTS_FAILED}"
    echo ""

    if [[ ${TESTS_FAILED} -eq 0 ]]; then
        echo "STATUS: ALL TESTS PASSED"
        return 0
    else
        echo "STATUS: SOME TESTS FAILED"
        return 1
    fi
}

# -----------------------------------------------------------------------------
# AC#1: File Exists at .claude/SUBAGENT-DESIGN-GUIDE.md
# -----------------------------------------------------------------------------

test_ac1_file_exists() {
    local test_name="AC#1: File exists at .claude/SUBAGENT-DESIGN-GUIDE.md"

    if [[ -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "File does not exist: ${TARGET_FILE}"
    fi
}

# -----------------------------------------------------------------------------
# AC#2: Context File Validation Checklist Section
# -----------------------------------------------------------------------------

test_ac2_context_checklist_section_exists() {
    local test_name="AC#2: Contains '## Context File Validation Checklist' section"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    if grep -q "## Context File Validation Checklist" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "Section header not found"
    fi
}

test_ac2_all_subagents_checklist() {
    local test_name="AC#2: Contains ALL subagents checklist"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    # Check for "For ALL subagents" or similar heading
    if grep -qiE "(for all subagents|all subagents)" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "ALL subagents checklist not found"
    fi
}

test_ac2_file_generation_checklist() {
    local test_name="AC#2: Contains File-Generation subagents checklist"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    if grep -qiE "(file-generation|file generation)" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "File-Generation subagents checklist not found"
    fi
}

test_ac2_code_generation_checklist() {
    local test_name="AC#2: Contains Code-Generation subagents checklist"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    if grep -qiE "(code-generation|code generation)" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "Code-Generation subagents checklist not found"
    fi
}

test_ac2_documentation_checklist() {
    local test_name="AC#2: Contains Documentation subagents checklist"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    if grep -qiE "(documentation subagents|specification.*(subagent|documentation))" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "Documentation subagents checklist not found"
    fi
}

# -----------------------------------------------------------------------------
# AC#3: Critical Rule for Write() Operations
# -----------------------------------------------------------------------------

test_ac3_before_any_write_section() {
    local test_name="AC#3: Contains 'Before ANY Write() call' section"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    if grep -qiE "before any write" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "Section 'Before ANY Write() call' not found"
    fi
}

test_ac3_critical_rule_statement() {
    local test_name="AC#3: Contains critical rule statement (ALWAYS read source-tree.md)"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    # Check for critical rule about reading source-tree.md before Write
    if grep -qiE "(always.*read.*source-tree|source-tree.*before.*write)" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "Critical rule about source-tree.md not found"
    fi
}

test_ac3_halt_pattern() {
    local test_name="AC#3: Contains HALT pattern for violations"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    if grep -q "HALT" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "HALT pattern not found"
    fi
}

# -----------------------------------------------------------------------------
# AC#4: Pre-Generation Validation Template
# -----------------------------------------------------------------------------

test_ac4_pre_generation_template() {
    local test_name="AC#4: Contains Pre-Generation Validation template"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    if grep -qiE "pre-generation validation" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "Pre-Generation Validation template not found"
    fi
}

test_ac4_copy_paste_code_block() {
    local test_name="AC#4: Contains copy-paste ready code block with Read()"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    # Check for code block containing Read() call to source-tree.md
    if grep -qE 'Read\(file_path.*source-tree' "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "Copy-paste code block with Read() not found"
    fi
}

# -----------------------------------------------------------------------------
# AC#5: Examples Section
# -----------------------------------------------------------------------------

test_ac5_wrong_example() {
    local test_name="AC#5: Contains wrong example with X marker"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    # Check for wrong example marker (either emoji or text)
    if grep -qE "(Wrong|Incorrect|Bad)" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "Wrong example not found"
    fi
}

test_ac5_correct_example() {
    local test_name="AC#5: Contains correct example with checkmark"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    # Check for correct example marker (either emoji or text)
    if grep -qE "(Correct|Right|Good)" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "Correct example not found"
    fi
}

test_ac5_rca_017_reference() {
    local test_name="AC#5: Contains RCA-017 reference"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    if grep -q "RCA-017" "${TARGET_FILE}"; then
        print_result "${test_name}" "PASS"
    else
        print_result "${test_name}" "FAIL" "RCA-017 reference not found"
    fi
}

# -----------------------------------------------------------------------------
# NFR: Document Under 300 Lines
# -----------------------------------------------------------------------------

test_nfr_document_under_300_lines() {
    local test_name="NFR: Document under 300 lines"

    if [[ ! -f "${TARGET_FILE}" ]]; then
        print_result "${test_name}" "FAIL" "Target file does not exist"
        return
    fi

    local line_count
    line_count=$(wc -l < "${TARGET_FILE}")

    if [[ ${line_count} -lt 300 ]]; then
        print_result "${test_name}" "PASS" "${line_count} lines"
    else
        print_result "${test_name}" "FAIL" "Document has ${line_count} lines (max: 300)"
    fi
}

# -----------------------------------------------------------------------------
# Main Test Execution
# -----------------------------------------------------------------------------

main() {
    print_header

    echo ""
    echo "AC#1: Guidance Document Created"
    echo "---"
    test_ac1_file_exists

    echo ""
    echo "AC#2: Context File Validation Checklist"
    echo "---"
    test_ac2_context_checklist_section_exists
    test_ac2_all_subagents_checklist
    test_ac2_file_generation_checklist
    test_ac2_code_generation_checklist
    test_ac2_documentation_checklist

    echo ""
    echo "AC#3: Critical Rule for Write() Operations"
    echo "---"
    test_ac3_before_any_write_section
    test_ac3_critical_rule_statement
    test_ac3_halt_pattern

    echo ""
    echo "AC#4: Pre-Generation Validation Template"
    echo "---"
    test_ac4_pre_generation_template
    test_ac4_copy_paste_code_block

    echo ""
    echo "AC#5: Examples Section"
    echo "---"
    test_ac5_wrong_example
    test_ac5_correct_example
    test_ac5_rca_017_reference

    echo ""
    echo "NFR: Non-Functional Requirements"
    echo "---"
    test_nfr_document_under_300_lines

    print_summary
}

# Run tests
main "$@"
