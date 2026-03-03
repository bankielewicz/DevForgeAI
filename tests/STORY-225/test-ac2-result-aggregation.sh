#!/bin/bash

###############################################################################
# TEST FILE: test-ac2-result-aggregation.sh
# AC#2: Result Aggregation Tests
#
# Story: STORY-225 - Implement devforgeai-insights Skill for Mining Orchestration
# Purpose: Verify skill aggregates, filters, and ranks results by relevance
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-225/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: ALL tests fail (skill does not exist yet)
#
# Acceptance Criteria Covered:
#   AC#2: Given raw data from session-miner,
#         When the skill processes results,
#         Then data is aggregated, filtered, and ranked by relevance.
#
# Technical Requirements Covered:
#   SKL-002: Aggregate and filter session-miner results
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
# AC#2: Result Aggregation Tests
###############################################################################

test_skill_file_exists() {
    test_start "Skill file exists at .claude/skills/devforgeai-insights/SKILL.md"

    if assert_file_exists "${SKILL_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
    fi
}

test_aggregation_section_exists() {
    test_start "SKL-002: Skill contains aggregation section or workflow"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for aggregation section/workflow
    if assert_file_contains_extended "${SKILL_FILE}" "(aggregat|Aggregat|combine|Combine|consolidat|Consolidat)"; then
        test_pass
    else
        test_fail "Aggregation section not found in skill"
    fi
}

test_filtering_logic_exists() {
    test_start "SKL-002: Skill contains filtering logic"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for filtering logic
    if assert_file_contains_extended "${SKILL_FILE}" "(filter|Filter|exclude|Exclude|include|Include)"; then
        test_pass
    else
        test_fail "Filtering logic not found in skill"
    fi
}

test_ranking_mechanism_exists() {
    test_start "SKL-002: Skill contains ranking or relevance mechanism"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for ranking/relevance mechanism
    if assert_file_contains_extended "${SKILL_FILE}" "(rank|Rank|relevance|Relevance|score|Score|priorit|sort|Sort|order)"; then
        test_pass
    else
        test_fail "Ranking mechanism not found in skill"
    fi
}

test_data_transformation_workflow() {
    test_start "SKL-002: Skill documents data transformation workflow"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for transformation/processing workflow
    if assert_file_contains_extended "${SKILL_FILE}" "(transform|Transform|process|Process|pipeline|Pipeline|workflow|Workflow)"; then
        test_pass
    else
        test_fail "Data transformation workflow not documented"
    fi
}

test_handles_raw_session_data() {
    test_start "SKL-002: Skill handles raw SessionEntry data from session-miner"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for SessionEntry or raw data handling
    if assert_file_contains_extended "${SKILL_FILE}" "(SessionEntry|entries|raw.*data|session.*data)"; then
        test_pass
    else
        test_fail "Raw session data handling not documented"
    fi
}

test_group_by_functionality() {
    test_start "SKL-002: Skill supports grouping results (e.g., by command, status, project)"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for grouping functionality
    if assert_file_contains_extended "${SKILL_FILE}" "(group|Group|categoriz|Categoriz|cluster|bucket)"; then
        test_pass
    else
        test_fail "Grouping functionality not documented"
    fi
}

test_count_and_metrics() {
    test_start "SKL-002: Skill calculates counts and metrics from aggregated data"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for count/metrics calculation
    if assert_file_contains_extended "${SKILL_FILE}" "(count|Count|metric|Metric|statistic|total|Total|sum|Sum|average|Average)"; then
        test_pass
    else
        test_fail "Count/metrics calculation not documented"
    fi
}

test_time_based_filtering() {
    test_start "SKL-002: Skill supports time-based filtering (date ranges)"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for time-based filtering
    if assert_file_contains_extended "${SKILL_FILE}" "(time|Time|date|Date|period|Period|range|Range|timestamp|recent)"; then
        test_pass
    else
        test_fail "Time-based filtering not documented"
    fi
}

test_error_filtering() {
    test_start "SKL-002: Skill can filter for error entries"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for error filtering capability
    if assert_file_contains_extended "${SKILL_FILE}" "(error|Error|fail|Fail|status.*error)"; then
        test_pass
    else
        test_fail "Error filtering capability not documented"
    fi
}

test_success_filtering() {
    test_start "SKL-002: Skill can filter for success entries"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for success filtering capability
    if assert_file_contains_extended "${SKILL_FILE}" "(success|Success|pass|Pass|status.*success|complete)"; then
        test_pass
    else
        test_fail "Success filtering capability not documented"
    fi
}

test_relevance_scoring_documented() {
    test_start "SKL-002: Skill documents how relevance scoring works"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for relevance scoring documentation
    if assert_file_contains_extended "${SKILL_FILE}" "(relevance|Relevance|weight|Weight|importance|important|priority|Priority)"; then
        test_pass
    else
        test_fail "Relevance scoring documentation not found"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-225 Test Suite: AC#2 - Result Aggregation"
    echo "Technical Requirement: SKL-002 (Aggregate and filter)"
    echo "Test Framework: Bash shell scripts (DevForgeAI standard)"
    echo "TDD Status: RED PHASE (All tests expected to FAIL)"
    echo "=============================================================="
    echo ""
    echo -e "${CYAN}Section: Skill File Existence${NC}"
    echo "--------------------------------------------------------------"

    test_skill_file_exists

    echo ""
    echo -e "${CYAN}Section: Aggregation Logic (SKL-002)${NC}"
    echo "--------------------------------------------------------------"

    test_aggregation_section_exists
    test_data_transformation_workflow
    test_handles_raw_session_data
    test_group_by_functionality
    test_count_and_metrics

    echo ""
    echo -e "${CYAN}Section: Filtering Logic (SKL-002)${NC}"
    echo "--------------------------------------------------------------"

    test_filtering_logic_exists
    test_time_based_filtering
    test_error_filtering
    test_success_filtering

    echo ""
    echo -e "${CYAN}Section: Ranking and Relevance (SKL-002)${NC}"
    echo "--------------------------------------------------------------"

    test_ranking_mechanism_exists
    test_relevance_scoring_documented

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
