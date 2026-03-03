#!/bin/bash

###############################################################################
# TEST FILE: test-ac1-command-file-creation.sh
# AC#1: Create Command File with YAML Frontmatter
#
# Story: STORY-159 - Create /create-stories-from-rca Command Shell
# Purpose: Verify command file exists and has valid YAML frontmatter
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-159/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: 7 tests fail (file missing, incomplete YAML)
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

assert_yaml_field_exists() {
    local file_path="$1"
    local field_name="$2"

    if grep -q "^${field_name}:" "${PROJECT_ROOT}/${file_path}" 2>/dev/null; then
        return 0
    fi
    return 1
}

assert_yaml_field_value() {
    local file_path="$1"
    local field_name="$2"
    local expected_value="$3"

    local actual_value=$(grep "^${field_name}:" "${PROJECT_ROOT}/${file_path}" 2>/dev/null | sed "s/^${field_name}: *//" | head -1)

    if [[ "${actual_value}" == "${expected_value}" ]]; then
        return 0
    fi
    return 1
}

assert_yaml_field_contains() {
    local file_path="$1"
    local field_name="$2"
    local substring="$3"

    if grep "^${field_name}:" "${PROJECT_ROOT}/${file_path}" 2>/dev/null | grep -q "${substring}"; then
        return 0
    fi
    return 1
}

###############################################################################
# Test Case 1.1: Command file exists at correct location
###############################################################################

test_ac1_command_file_exists() {
    test_start "AC#1.1: Command file exists at .claude/commands/create-stories-from-rca.md"

    if assert_file_exists "${COMMAND_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
    fi
}

###############################################################################
# Test Case 1.2: YAML frontmatter contains required fields
###############################################################################

test_ac1_yaml_frontmatter_valid() {
    test_start "AC#1.2: YAML frontmatter contains required fields (name, description, argument-hint, allowed-tools, model)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    local required_fields=("name" "description" "argument-hint" "allowed-tools" "model")
    local missing_fields=()

    for field in "${required_fields[@]}"; do
        if ! assert_yaml_field_exists "${COMMAND_FILE}" "${field}"; then
            missing_fields+=("${field}")
        fi
    done

    if [[ ${#missing_fields[@]} -eq 0 ]]; then
        test_pass
    else
        test_fail "Missing YAML fields: ${missing_fields[*]}"
    fi
}

###############################################################################
# Test Case 1.3: name field matches command
###############################################################################

test_ac1_name_field_correct() {
    test_start "AC#1.3: name field equals 'create-stories-from-rca'"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    if assert_yaml_field_value "${COMMAND_FILE}" "name" "create-stories-from-rca"; then
        test_pass
    else
        test_fail "name field does not equal 'create-stories-from-rca'"
    fi
}

###############################################################################
# Test Case 1.4: description field is present and non-empty
###############################################################################

test_ac1_description_field_present() {
    test_start "AC#1.4: description field is present and non-empty"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    if ! assert_yaml_field_exists "${COMMAND_FILE}" "description"; then
        test_fail "description field not found"
        return
    fi

    local description=$(grep "^description:" "${PROJECT_ROOT}/${COMMAND_FILE}" | sed 's/^description: *//')

    if [[ -n "${description}" ]]; then
        test_pass
    else
        test_fail "description field is empty"
    fi
}

###############################################################################
# Test Case 1.5: argument-hint field is present
###############################################################################

test_ac1_argument_hint_field_present() {
    test_start "AC#1.5: argument-hint field is present with format hint"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    if assert_yaml_field_exists "${COMMAND_FILE}" "argument-hint"; then
        test_pass
    else
        test_fail "argument-hint field not found"
    fi
}

###############################################################################
# Test Case 1.6: allowed-tools field includes required tools
###############################################################################

test_ac1_allowed_tools_includes_required() {
    test_start "AC#1.6: allowed-tools includes required tools (Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill, TodoWrite)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    if ! assert_yaml_field_exists "${COMMAND_FILE}" "allowed-tools"; then
        test_fail "allowed-tools field not found"
        return
    fi

    local required_tools=("Read" "Write" "Edit" "Glob" "Grep" "AskUserQuestion" "Skill" "TodoWrite")
    local missing_tools=()

    for tool in "${required_tools[@]}"; do
        if ! assert_yaml_field_contains "${COMMAND_FILE}" "allowed-tools" "${tool}"; then
            missing_tools+=("${tool}")
        fi
    done

    if [[ ${#missing_tools[@]} -eq 0 ]]; then
        test_pass
    else
        test_fail "Missing required tools: ${missing_tools[*]}"
    fi
}

###############################################################################
# Test Case 1.7: model field is set to "sonnet"
###############################################################################

test_ac1_model_field_correct() {
    test_start "AC#1.7: model field is set to 'sonnet'"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    if assert_yaml_field_value "${COMMAND_FILE}" "model" "sonnet"; then
        test_pass
    else
        test_fail "model field does not equal 'sonnet'"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-159 Test Suite: AC#1 - Command File Creation"
    echo "Test Framework: Bash shell scripts"
    echo "Expected Status: ALL TESTS FAIL (TDD Red Phase)"
    echo "=============================================================="

    # Run all tests
    test_ac1_command_file_exists
    test_ac1_yaml_frontmatter_valid
    test_ac1_name_field_correct
    test_ac1_description_field_present
    test_ac1_argument_hint_field_present
    test_ac1_allowed_tools_includes_required
    test_ac1_model_field_correct

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
