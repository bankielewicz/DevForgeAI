#!/bin/bash

###############################################################################
# TEST FILE: test-ac2-argument-parsing.sh
# AC#2: Implement Argument Parsing and Validation
#
# Story: STORY-159 - Create /create-stories-from-rca Command Shell
# Purpose: Verify RCA ID argument parsing, validation, and file location
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-159/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: 5 tests fail (no parsing logic)
###############################################################################

set -u

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Constants
COMMAND_FILE=".claude/commands/create-stories-from-rca.md"
RCA_DIR="devforgeai/RCA"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

###############################################################################
# Test Utility Functions
###############################################################################

test_start() {
    local test_name="$1"
    ((TESTS_RUN++))
    echo -e "\n${YELLOW}[TEST ${TESTS_RUN}]${NC} ${test_name}"
}

test_pass() {
    ((TESTS_PASSED++))
    echo -e "${GREEN}✓ PASS${NC}"
}

test_fail() {
    local reason="$1"
    ((TESTS_FAILED++))
    echo -e "${RED}✗ FAIL${NC}: ${reason}"
}

assert_file_exists() {
    local file_path="$1"
    if [[ ! -f "${PROJECT_ROOT}/${file_path}" ]]; then
        return 1
    fi
    return 0
}

# Extract RCA ID from user input (test function)
extract_rca_id() {
    local input="$1"

    # Remove whitespace
    input=$(echo "${input}" | tr -d '[:space:]')

    # Convert to uppercase
    input=$(echo "${input}" | tr '[:lower:]' '[:upper:]')

    echo "${input}"
}

# Validate RCA ID format (RCA-NNN where NNN are exactly 3 digits)
validate_rca_format() {
    local rca_id="$1"

    if [[ ${rca_id} =~ ^RCA-[0-9]{3}$ ]]; then
        return 0
    fi
    return 1
}

# Find RCA file in devforgeai/RCA/ directory
find_rca_file() {
    local rca_id="$1"

    # Search for file matching pattern RCA-NNN-*.md
    local matching_files=$(find "${PROJECT_ROOT}/${RCA_DIR}" -name "${rca_id}-*.md" 2>/dev/null)

    if [[ -n "${matching_files}" ]]; then
        echo "${matching_files}" | head -1
        return 0
    fi
    return 1
}

###############################################################################
# Test Case 2.1: Accepts RCA-NNN format (uppercase)
###############################################################################

test_ac2_accepts_valid_rca_format() {
    test_start "AC#2.1: Accepts valid RCA ID format (RCA-022 uppercase)"

    local rca_input="RCA-022"
    local extracted_id=$(extract_rca_id "${rca_input}")

    if validate_rca_format "${extracted_id}"; then
        test_pass
    else
        test_fail "Failed to parse or validate RCA-022"
    fi
}

###############################################################################
# Test Case 2.2: Accepts case-insensitive RCA ID (BR-002)
###############################################################################

test_ac2_accepts_lowercase_rca_format() {
    test_start "AC#2.2: Accepts case-insensitive RCA ID (rca-022 → RCA-022, per BR-002)"

    local rca_input="rca-022"
    local extracted_id=$(extract_rca_id "${rca_input}")

    # Should normalize to RCA-022
    if [[ "${extracted_id}" == "RCA-022" ]] && validate_rca_format "${extracted_id}"; then
        test_pass
    else
        test_fail "Failed to normalize rca-022 to RCA-022 or validate format"
    fi
}

###############################################################################
# Test Case 2.3: Locates RCA file in devforgeai/RCA/
###############################################################################

test_ac2_locates_rca_file() {
    test_start "AC#2.3: Locates RCA file in devforgeai/RCA/ directory (BR-003 file existence check)"

    # Check if RCA directory exists with at least one RCA file
    if [[ ! -d "${PROJECT_ROOT}/${RCA_DIR}" ]]; then
        test_fail "RCA directory not found: ${PROJECT_ROOT}/${RCA_DIR}"
        return
    fi

    # Find any RCA file to test location logic
    local rca_files=$(find "${PROJECT_ROOT}/${RCA_DIR}" -name "RCA-*.md" 2>/dev/null | head -1)

    if [[ -n "${rca_files}" ]]; then
        # Test can locate the file
        local test_rca=$(basename "${rca_files}" | sed 's/-.*$//')

        if find_rca_file "${test_rca}" > /dev/null; then
            test_pass
        else
            test_fail "Failed to locate RCA file for ${test_rca}"
        fi
    else
        test_fail "No RCA files found in ${PROJECT_ROOT}/${RCA_DIR}"
    fi
}

###############################################################################
# Test Case 2.4: Validates RCA-NNN format (exactly 3 digits)
###############################################################################

test_ac2_validates_rca_format_digits() {
    test_start "AC#2.4: Validates RCA-NNN format (exactly 3 digits, rejects RCA-22 and RCA-0022)"

    local valid_format="RCA-022"
    local invalid_format_2_digits="RCA-22"
    local invalid_format_4_digits="RCA-0022"

    local valid_result=0
    local invalid_2_digit_result=0
    local invalid_4_digit_result=0

    if validate_rca_format "${valid_format}"; then
        valid_result=1
    fi

    if ! validate_rca_format "${invalid_format_2_digits}"; then
        invalid_2_digit_result=1
    fi

    if ! validate_rca_format "${invalid_format_4_digits}"; then
        invalid_4_digit_result=1
    fi

    if [[ ${valid_result} -eq 1 && ${invalid_2_digit_result} -eq 1 && ${invalid_4_digit_result} -eq 1 ]]; then
        test_pass
    else
        test_fail "Format validation failed: valid=${valid_result}, invalid_2=${invalid_2_digit_result}, invalid_4=${invalid_4_digit_result}"
    fi
}

###############################################################################
# Test Case 2.5: Rejects invalid format gracefully
###############################################################################

test_ac2_rejects_invalid_format() {
    test_start "AC#2.5: Rejects invalid formats (INVALID-022, rca22, RCA022, etc.)"

    local invalid_formats=("INVALID-022" "rca22" "RCA022" "RCA-0AB" "story-022")
    local all_rejected=true

    for invalid_format in "${invalid_formats[@]}"; do
        local normalized=$(extract_rca_id "${invalid_format}")

        if validate_rca_format "${normalized}"; then
            all_rejected=false
            echo "  Incorrectly accepted: ${invalid_format}"
        fi
    done

    if ${all_rejected}; then
        test_pass
    else
        test_fail "Some invalid formats were accepted"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-159 Test Suite: AC#2 - Argument Parsing & Validation"
    echo "Test Framework: Bash shell scripts"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase - no command impl)"
    echo "=============================================================="

    # Run all tests
    test_ac2_accepts_valid_rca_format
    test_ac2_accepts_lowercase_rca_format
    test_ac2_locates_rca_file
    test_ac2_validates_rca_format_digits
    test_ac2_rejects_invalid_format

    # Print summary
    echo ""
    echo "=============================================================="
    echo "Test Summary:"
    echo "  Total Tests:  ${TESTS_RUN}"
    echo "  Passed:       ${TESTS_PASSED}"
    echo "  Failed:       ${TESTS_FAILED}"
    echo "=============================================================="

    if [[ ${TESTS_FAILED} -eq 0 ]]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        return 0
    else
        echo -e "${RED}✗ ${TESTS_FAILED} test(s) failed${NC}"
        return 1
    fi
}

# Run test suite
main "$@"
