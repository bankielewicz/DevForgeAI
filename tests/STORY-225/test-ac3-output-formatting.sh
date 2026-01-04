#!/bin/bash

###############################################################################
# TEST FILE: test-ac3-output-formatting.sh
# AC#3: Output Formatting Tests
#
# Story: STORY-225 - Implement devforgeai-insights Skill for Mining Orchestration
# Purpose: Verify skill formats results as user-friendly markdown
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-225/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: ALL tests fail (skill does not exist yet)
#
# Acceptance Criteria Covered:
#   AC#3: Given aggregated results,
#         When the skill prepares output,
#         Then results are formatted as user-friendly markdown with tables,
#         summaries, and recommendations.
#
# Technical Requirements Covered:
#   SKL-003: Format output as markdown with tables, summaries, recommendations
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
# AC#3: Output Formatting Tests
###############################################################################

test_skill_file_exists() {
    test_start "Skill file exists at .claude/skills/devforgeai-insights/SKILL.md"

    if assert_file_exists "${SKILL_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
    fi
}

test_output_section_exists() {
    test_start "SKL-003: Skill contains output formatting section"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for output formatting section
    if assert_file_contains_extended "${SKILL_FILE}" "(output|Output|format|Format|display|Display|render|Render)"; then
        test_pass
    else
        test_fail "Output formatting section not found in skill"
    fi
}

test_markdown_format_specified() {
    test_start "SKL-003: Skill specifies markdown as output format"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for markdown format specification
    if assert_file_contains_extended "${SKILL_FILE}" "(markdown|Markdown|\.md|MD)"; then
        test_pass
    else
        test_fail "Markdown format not specified"
    fi
}

test_table_formatting_documented() {
    test_start "SKL-003: Skill documents table formatting for results"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for table formatting documentation (markdown table syntax or table keyword)
    if assert_file_contains_extended "${SKILL_FILE}" "(table|Table|\|.*\||\|---\|)"; then
        test_pass
    else
        test_fail "Table formatting not documented"
    fi
}

test_summary_section_documented() {
    test_start "SKL-003: Skill documents summary section in output"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for summary documentation
    if assert_file_contains_extended "${SKILL_FILE}" "(summary|Summary|overview|Overview|highlights|Highlights)"; then
        test_pass
    else
        test_fail "Summary section not documented"
    fi
}

test_recommendations_section_documented() {
    test_start "SKL-003: Skill documents recommendations section in output"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for recommendations documentation
    if assert_file_contains_extended "${SKILL_FILE}" "(recommend|Recommend|suggest|Suggest|action|Action|insight|Insight)"; then
        test_pass
    else
        test_fail "Recommendations section not documented"
    fi
}

test_user_friendly_language() {
    test_start "SKL-003: Skill emphasizes user-friendly output"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for user-friendly emphasis
    if assert_file_contains_extended "${SKILL_FILE}" "(user|User|friendly|clear|Clear|readable|human)"; then
        test_pass
    else
        test_fail "User-friendly output emphasis not found"
    fi
}

test_output_template_exists() {
    test_start "SKL-003: Skill contains output template or example"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for template or example output
    if assert_file_contains_extended "${SKILL_FILE}" "(template|Template|example|Example|sample|Sample)"; then
        test_pass
    else
        test_fail "Output template not found"
    fi
}

test_dashboard_output_format() {
    test_start "SKL-003: Skill defines dashboard output format"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for dashboard-specific output
    if assert_file_contains_extended "${SKILL_FILE}" "(dashboard|Dashboard|metrics|Metrics|KPI|kpi)"; then
        test_pass
    else
        test_fail "Dashboard output format not defined"
    fi
}

test_workflows_output_format() {
    test_start "SKL-003: Skill defines workflows output format"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for workflows-specific output
    if assert_file_contains_extended "${SKILL_FILE}" "(workflow|Workflow|pattern|Pattern|sequence|Sequence)"; then
        test_pass
    else
        test_fail "Workflows output format not defined"
    fi
}

test_errors_output_format() {
    test_start "SKL-003: Skill defines errors output format"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for errors-specific output
    if assert_file_contains_extended "${SKILL_FILE}" "(error|Error|failure|Failure|issue|Issue)"; then
        test_pass
    else
        test_fail "Errors output format not defined"
    fi
}

test_decisions_output_format() {
    test_start "SKL-003: Skill defines decisions output format"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for decisions-specific output
    if assert_file_contains "${SKILL_FILE}" "decision"; then
        test_pass
    else
        test_fail "Decisions output format not defined"
    fi
}

test_story_output_format() {
    test_start "SKL-003: Skill defines story-specific output format"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for story-specific output
    if assert_file_contains_extended "${SKILL_FILE}" "(story|Story|STORY-[0-9]+)"; then
        test_pass
    else
        test_fail "Story-specific output format not defined"
    fi
}

test_heading_structure() {
    test_start "SKL-003: Skill output uses proper markdown headings"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for markdown heading usage (# headings)
    if assert_file_contains_extended "${SKILL_FILE}" "^#+ "; then
        test_pass
    else
        test_fail "Markdown heading structure not found"
    fi
}

test_list_formatting() {
    test_start "SKL-003: Skill output uses markdown lists"

    if ! assert_file_exists "${SKILL_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${SKILL_FILE}"
        return
    fi

    # Check for markdown list usage (- or * or numbered)
    if assert_file_contains_extended "${SKILL_FILE}" "^[\-\*] |^[0-9]+\."; then
        test_pass
    else
        test_fail "Markdown list formatting not found"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-225 Test Suite: AC#3 - Output Formatting"
    echo "Technical Requirement: SKL-003 (Markdown format with tables, summaries)"
    echo "Test Framework: Bash shell scripts (DevForgeAI standard)"
    echo "TDD Status: RED PHASE (All tests expected to FAIL)"
    echo "=============================================================="
    echo ""
    echo -e "${CYAN}Section: Skill File Existence${NC}"
    echo "--------------------------------------------------------------"

    test_skill_file_exists

    echo ""
    echo -e "${CYAN}Section: Output Format Specification (SKL-003)${NC}"
    echo "--------------------------------------------------------------"

    test_output_section_exists
    test_markdown_format_specified
    test_user_friendly_language
    test_output_template_exists

    echo ""
    echo -e "${CYAN}Section: Output Components (SKL-003)${NC}"
    echo "--------------------------------------------------------------"

    test_table_formatting_documented
    test_summary_section_documented
    test_recommendations_section_documented
    test_heading_structure
    test_list_formatting

    echo ""
    echo -e "${CYAN}Section: Query Type Output Formats (SKL-003)${NC}"
    echo "--------------------------------------------------------------"

    test_dashboard_output_format
    test_workflows_output_format
    test_errors_output_format
    test_decisions_output_format
    test_story_output_format

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
