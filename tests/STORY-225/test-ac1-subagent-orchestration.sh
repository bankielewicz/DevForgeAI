#!/bin/bash

###############################################################################
# TEST FILE: test-ac1-subagent-orchestration.sh
# AC#1: Subagent Orchestration Tests
#
# Story: STORY-225 - Implement devforgeai-insights Skill for Mining Orchestration
# Purpose: Verify skill invokes session-miner subagent with appropriate prompts
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-225/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: ALL tests fail (skill does not exist yet)
#
# Acceptance Criteria Covered:
#   AC#1: Given a query request from /insights command,
#         When the skill processes the query,
#         Then it invokes session-miner subagent with appropriate prompts.
#
# Technical Requirements Covered:
#   SKL-001: Invoke session-miner subagent
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

###############################################################################
# AC#1: Subagent Orchestration Tests
###############################################################################

test_skill_file_exists() {
    test_start "Skill file exists at .claude/skills/devforgeai-insights/SKILL.md"

    if assert_file_exists "${SKILL_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
    fi
}

test_skill_has_yaml_frontmatter() {
    test_start "Skill file has YAML frontmatter with required fields"

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

test_skill_has_name_field() {
    test_start "YAML frontmatter contains 'name' field"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    if grep -q "^name:" "${PROJECT_ROOT}/${SKILL_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Missing 'name' field in YAML frontmatter"
    fi
}

test_skill_has_description_field() {
    test_start "YAML frontmatter contains 'description' field"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    if grep -q "^description:" "${PROJECT_ROOT}/${SKILL_FILE}" 2>/dev/null; then
        test_pass
    else
        test_fail "Missing 'description' field in YAML frontmatter"
    fi
}

test_session_miner_subagent_reference() {
    test_start "SKL-001: Skill references session-miner subagent"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    if assert_file_contains "${SKILL_FILE}" "session-miner"; then
        test_pass
    else
        test_fail "session-miner subagent not referenced in skill"
    fi
}

test_task_invocation_pattern() {
    test_start "SKL-001: Skill uses Task() invocation pattern for subagent"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for Task invocation syntax with session-miner
    if assert_file_contains_extended "${SKILL_FILE}" "(Task\(|subagent_type.*=.*session-miner|Task.*session-miner)"; then
        test_pass
    else
        test_fail "Task() invocation pattern for session-miner not found"
    fi
}

test_query_type_parameter_passing() {
    test_start "SKL-001: Skill passes query type to session-miner"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for query type parameter handling
    if assert_file_contains_extended "${SKILL_FILE}" "(query_type|query-type|QUERY_TYPE|queryType)"; then
        test_pass
    else
        test_fail "Query type parameter handling not found"
    fi
}

test_prompt_generation_for_dashboard() {
    test_start "SKL-001: Skill generates prompts for dashboard query type"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for dashboard query handling
    if assert_file_contains_extended "${SKILL_FILE}" "(dashboard|overview|summary)"; then
        test_pass
    else
        test_fail "Dashboard query type handling not found"
    fi
}

test_prompt_generation_for_workflows() {
    test_start "SKL-001: Skill generates prompts for workflows query type"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for workflows query handling
    if assert_file_contains "${SKILL_FILE}" "workflows"; then
        test_pass
    else
        test_fail "Workflows query type handling not found"
    fi
}

test_prompt_generation_for_errors() {
    test_start "SKL-001: Skill generates prompts for errors query type"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for errors query handling
    if assert_file_contains "${SKILL_FILE}" "errors"; then
        test_pass
    else
        test_fail "Errors query type handling not found"
    fi
}

test_prompt_generation_for_decisions() {
    test_start "SKL-001: Skill generates prompts for decisions query type"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for decisions query handling
    if assert_file_contains "${SKILL_FILE}" "decisions"; then
        test_pass
    else
        test_fail "Decisions query type handling not found"
    fi
}

test_prompt_generation_for_story() {
    test_start "SKL-001: Skill generates prompts for story-specific query type"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for story-specific query handling
    if assert_file_contains_extended "${SKILL_FILE}" "(story.*STORY|STORY-[0-9]+|story_id)"; then
        test_pass
    else
        test_fail "Story-specific query type handling not found"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-225 Test Suite: AC#1 - Subagent Orchestration"
    echo "Technical Requirement: SKL-001 (Invoke session-miner)"
    echo "Test Framework: Bash shell scripts (DevForgeAI standard)"
    echo "TDD Status: RED PHASE (All tests expected to FAIL)"
    echo "=============================================================="
    echo ""
    echo -e "${CYAN}Section: Skill File Structure${NC}"
    echo "--------------------------------------------------------------"

    # Skill file structure tests
    test_skill_file_exists
    test_skill_has_yaml_frontmatter
    test_skill_has_name_field
    test_skill_has_description_field

    echo ""
    echo -e "${CYAN}Section: Subagent Invocation (SKL-001)${NC}"
    echo "--------------------------------------------------------------"

    # Subagent invocation tests
    test_session_miner_subagent_reference
    test_task_invocation_pattern
    test_query_type_parameter_passing

    echo ""
    echo -e "${CYAN}Section: Query Type Prompt Generation${NC}"
    echo "--------------------------------------------------------------"

    # Query type handling tests
    test_prompt_generation_for_dashboard
    test_prompt_generation_for_workflows
    test_prompt_generation_for_errors
    test_prompt_generation_for_decisions
    test_prompt_generation_for_story

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
