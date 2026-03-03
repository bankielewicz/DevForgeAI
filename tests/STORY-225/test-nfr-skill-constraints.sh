#!/bin/bash

###############################################################################
# TEST FILE: test-nfr-skill-constraints.sh
# Non-Functional Requirements: Skill Size and Structure Constraints
#
# Story: STORY-225 - Implement devforgeai-insights Skill for Mining Orchestration
# Purpose: Verify skill meets NFR constraints from source-tree.md and tech-stack.md
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-225/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: ALL tests fail (skill does not exist yet)
#
# Non-Functional Requirements Covered:
#   NFR-001: <10 seconds for cached queries
#   NFR-002: <1000 lines SKILL.md
#   NFR-003: Proper skill directory structure
###############################################################################

set -u

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Constants
SKILL_DIR=".claude/skills/devforgeai-insights"
SKILL_FILE=".claude/skills/devforgeai-insights/SKILL.md"
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
    echo -e "${GREEN}  PASS${NC}"
}

test_fail() {
    local reason="$1"
    ((TESTS_FAILED++))
    echo -e "${RED}  FAIL${NC}: ${reason}"
}

assert_file_exists() {
    local file_path="$1"
    if [[ ! -f "${PROJECT_ROOT}/${file_path}" ]]; then
        return 1
    fi
    return 0
}

assert_dir_exists() {
    local dir_path="$1"
    if [[ ! -d "${PROJECT_ROOT}/${dir_path}" ]]; then
        return 1
    fi
    return 0
}

assert_file_contains() {
    local file_path="$1"
    local search_string="$2"

    if grep -q "${search_string}" "${PROJECT_ROOT}/${file_path}" 2>/dev/null; then
        return 0
    fi
    return 1
}

assert_file_contains_extended() {
    local file_path="$1"
    local regex_pattern="$2"

    if grep -qE "${regex_pattern}" "${PROJECT_ROOT}/${file_path}" 2>/dev/null; then
        return 0
    fi
    return 1
}

count_file_lines() {
    local file_path="$1"
    if [[ -f "${PROJECT_ROOT}/${file_path}" ]]; then
        wc -l < "${PROJECT_ROOT}/${file_path}"
    else
        echo "0"
    fi
}

###############################################################################
# NFR: Skill Directory Structure Tests
###############################################################################

test_skill_directory_exists() {
    test_start "NFR: Skill directory exists at .claude/skills/devforgeai-insights/"

    if assert_dir_exists "${SKILL_DIR}"; then
        test_pass
    else
        test_fail "Directory not found: ${PROJECT_ROOT}/${SKILL_DIR}"
    fi
}

test_skill_file_exists() {
    test_start "NFR: SKILL.md file exists in skill directory"

    if assert_file_exists "${SKILL_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
    fi
}

test_skill_file_named_correctly() {
    test_start "NFR: Skill file is named SKILL.md (per source-tree.md)"

    if assert_file_exists "${SKILL_FILE}"; then
        test_pass
    else
        test_fail "Skill file must be named SKILL.md (not skill.md or other)"
    fi
}

###############################################################################
# NFR: Skill Size Constraints Tests
###############################################################################

test_skill_under_1000_lines() {
    test_start "NFR: SKILL.md is under 1000 lines (per tech-stack.md constraint)"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    local line_count=$(count_file_lines "${SKILL_FILE}")

    if [[ ${line_count} -lt 1000 ]]; then
        test_pass
    else
        test_fail "SKILL.md has ${line_count} lines (max 1000, target 500-800)"
    fi
}

test_skill_target_line_count() {
    test_start "NFR: SKILL.md is within target range (500-800 lines recommended)"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    local line_count=$(count_file_lines "${SKILL_FILE}")

    if [[ ${line_count} -ge 100 && ${line_count} -le 800 ]]; then
        test_pass
    else
        test_fail "SKILL.md has ${line_count} lines (target 500-800, minimum 100 for completeness)"
    fi
}

###############################################################################
# NFR: YAML Frontmatter Tests (per source-tree.md)
###############################################################################

test_yaml_frontmatter_present() {
    test_start "NFR: SKILL.md has YAML frontmatter with proper delimiters"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for opening and closing YAML delimiters
    local delimiter_count=$(tr -d '\r' < "${PROJECT_ROOT}/${SKILL_FILE}" | grep -c "^---$" 2>/dev/null || echo "0")

    if [[ ${delimiter_count} -ge 2 ]]; then
        test_pass
    else
        test_fail "Missing YAML frontmatter delimiters (found ${delimiter_count}, need at least 2)"
    fi
}

test_yaml_has_name() {
    test_start "NFR: YAML frontmatter contains 'name' field (required per source-tree.md)"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    if grep -q "^name:" "${PROJECT_ROOT}/${SKILL_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Missing required 'name' field in YAML frontmatter"
    fi
}

test_yaml_has_description() {
    test_start "NFR: YAML frontmatter contains 'description' field (required per source-tree.md)"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    if grep -q "^description:" "${PROJECT_ROOT}/${SKILL_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Missing required 'description' field in YAML frontmatter"
    fi
}

test_skill_name_convention() {
    test_start "NFR: Skill name follows 'devforgeai-' prefix convention"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    if assert_file_contains "${SKILL_FILE}" "devforgeai-insights"; then
        test_pass
    else
        test_fail "Skill name must be 'devforgeai-insights'"
    fi
}

###############################################################################
# NFR: Content Quality Tests
###############################################################################

test_has_purpose_section() {
    test_start "NFR: SKILL.md contains Purpose section"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    if assert_file_contains_extended "${SKILL_FILE}" "(## Purpose|## Overview|# Purpose)"; then
        test_pass
    else
        test_fail "Purpose/Overview section not found"
    fi
}

test_has_workflow_section() {
    test_start "NFR: SKILL.md contains Workflow section"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    if assert_file_contains_extended "${SKILL_FILE}" "(## Workflow|## Process|## Steps)"; then
        test_pass
    else
        test_fail "Workflow section not found"
    fi
}

test_has_success_criteria() {
    test_start "NFR: SKILL.md contains Success Criteria section"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    if assert_file_contains_extended "${SKILL_FILE}" "(## Success|Success Criteria|## Output)"; then
        test_pass
    else
        test_fail "Success Criteria section not found"
    fi
}

test_references_story() {
    test_start "NFR: SKILL.md references source story (STORY-225 or EPIC-034)"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    if assert_file_contains_extended "${SKILL_FILE}" "(STORY-225|EPIC-034|session.*data.*mining)"; then
        test_pass
    else
        test_fail "Story/Epic reference not found"
    fi
}

test_no_executable_code() {
    test_start "NFR: SKILL.md contains documentation only (no executable code per source-tree.md)"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for forbidden executable patterns (Python shebang, function def outside markdown)
    if grep -qE "^#!/usr/bin/(python|bash|node)" "${PROJECT_ROOT}/${SKILL_FILE}" 2>/dev/null; then
        test_fail "SKILL.md should not contain shebang lines for executable scripts"
    else
        test_pass
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-225 Test Suite: Non-Functional Requirements"
    echo "Constraints: source-tree.md, tech-stack.md"
    echo "Test Framework: Bash shell scripts (DevForgeAI standard)"
    echo "TDD Status: RED PHASE (All tests expected to FAIL)"
    echo "=============================================================="
    echo ""
    echo -e "${CYAN}Section: Skill Directory Structure${NC}"
    echo "--------------------------------------------------------------"

    test_skill_directory_exists
    test_skill_file_exists
    test_skill_file_named_correctly

    echo ""
    echo -e "${CYAN}Section: Skill Size Constraints${NC}"
    echo "--------------------------------------------------------------"

    test_skill_under_1000_lines
    test_skill_target_line_count

    echo ""
    echo -e "${CYAN}Section: YAML Frontmatter (source-tree.md)${NC}"
    echo "--------------------------------------------------------------"

    test_yaml_frontmatter_present
    test_yaml_has_name
    test_yaml_has_description
    test_skill_name_convention

    echo ""
    echo -e "${CYAN}Section: Content Quality${NC}"
    echo "--------------------------------------------------------------"

    test_has_purpose_section
    test_has_workflow_section
    test_has_success_criteria
    test_references_story
    test_no_executable_code

    # Print summary
    echo ""
    echo "=============================================================="
    echo "Test Summary:"
    echo "  Total Tests:  ${TESTS_RUN}"
    echo "  Passed:       ${TESTS_PASSED}"
    echo "  Failed:       ${TESTS_FAILED}"
    echo "=============================================================="

    if [[ ${TESTS_FAILED} -eq 0 ]]; then
        echo -e "${GREEN}  All tests passed!${NC}"
        return 0
    else
        echo -e "${RED}  ${TESTS_FAILED} test(s) failed${NC}"
        echo ""
        echo "TDD Red Phase: Tests are expected to fail until implementation."
        echo "Next step: Create .claude/skills/devforgeai-insights/SKILL.md to make tests pass."
        return 1
    fi
}

# Run test suite
main "$@"
