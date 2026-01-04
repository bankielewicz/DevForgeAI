#!/bin/bash

###############################################################################
# TEST FILE: test-insights-command.sh
# Full Test Suite for /insights Command
#
# Story: STORY-224 - Create /insights Command with Query Routing
# Purpose: Verify command file creation, structure, query routing, help, and error handling
#
# Test Framework: Bash shell scripts (DevForgeAI standard)
# Location: /mnt/c/Projects/DevForgeAI2/tests/STORY-224/
#
# TDD Status: RED PHASE (Tests fail before implementation)
# Expected Failures: ALL tests fail (command file does not exist yet)
#
# Acceptance Criteria Covered:
#   AC#1: Command Parameter Support
#   AC#2: Query Routing to Skill
#   AC#3: Help Documentation
#   AC#4: Error Handling
#
# Technical Requirements Covered:
#   CMD-001: Parse $ARGUMENTS for query type and parameters
#   CMD-002: Route to devforgeai-insights skill
#   CMD-003: Display help with --help flag
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
COMMAND_FILE=".claude/commands/insights.md"
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

count_file_lines() {
    local file_path="$1"
    if [[ -f "${PROJECT_ROOT}/${file_path}" ]]; then
        wc -l < "${PROJECT_ROOT}/${file_path}"
    else
        echo "0"
    fi
}

###############################################################################
# SECTION 1: Command File Existence and YAML Frontmatter
# Tests that command file exists at correct location with valid metadata
###############################################################################

test_command_file_exists() {
    test_start "Command file exists at .claude/commands/insights.md"

    if assert_file_exists "${COMMAND_FILE}"; then
        test_pass
    else
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
    fi
}

test_yaml_frontmatter_has_description() {
    test_start "YAML frontmatter contains 'description' field"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    if assert_yaml_field_exists "${COMMAND_FILE}" "description"; then
        test_pass
    else
        test_fail "Missing 'description' field in YAML frontmatter"
    fi
}

test_yaml_frontmatter_has_argument_hint() {
    test_start "YAML frontmatter contains 'argument-hint' field"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    if assert_yaml_field_exists "${COMMAND_FILE}" "argument-hint"; then
        test_pass
    else
        test_fail "Missing 'argument-hint' field in YAML frontmatter"
    fi
}

test_yaml_frontmatter_has_model() {
    test_start "YAML frontmatter contains 'model' field"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    if assert_yaml_field_exists "${COMMAND_FILE}" "model"; then
        test_pass
    else
        test_fail "Missing 'model' field in YAML frontmatter"
    fi
}

test_yaml_frontmatter_has_allowed_tools() {
    test_start "YAML frontmatter contains 'allowed-tools' field"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    if assert_yaml_field_exists "${COMMAND_FILE}" "allowed-tools"; then
        test_pass
    else
        test_fail "Missing 'allowed-tools' field in YAML frontmatter"
    fi
}

###############################################################################
# SECTION 2: AC#1 - Command Parameter Support
# Tests that all query types are documented and supported
###############################################################################

test_ac1_dashboard_query_type() {
    test_start "AC#1.1: /insights (dashboard overview) query type documented"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for dashboard/overview query type
    if assert_file_contains_extended "${COMMAND_FILE}" "(dashboard|overview|/insights\s*\$|/insights\s+\(|default.*dashboard)"; then
        test_pass
    else
        test_fail "Dashboard/overview query type not documented"
    fi
}

test_ac1_workflows_query_type() {
    test_start "AC#1.2: /insights workflows (pattern analysis) query type documented"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for workflows query type
    if assert_file_contains "${COMMAND_FILE}" "workflows"; then
        test_pass
    else
        test_fail "'workflows' query type not documented"
    fi
}

test_ac1_errors_query_type() {
    test_start "AC#1.3: /insights errors (error mining) query type documented"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for errors query type
    if assert_file_contains "${COMMAND_FILE}" "errors"; then
        test_pass
    else
        test_fail "'errors' query type not documented"
    fi
}

test_ac1_decisions_query_type() {
    test_start "AC#1.4: /insights decisions [query] (archive search) query type documented"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for decisions query type
    if assert_file_contains "${COMMAND_FILE}" "decisions"; then
        test_pass
    else
        test_fail "'decisions' query type not documented"
    fi
}

test_ac1_story_query_type() {
    test_start "AC#1.5: /insights story STORY-XXX (story-specific) query type documented"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for story-specific query type
    if assert_file_contains_extended "${COMMAND_FILE}" "(story.*STORY|STORY.*query|/insights story)"; then
        test_pass
    else
        test_fail "Story-specific query type not documented"
    fi
}

test_ac1_argument_parsing_logic() {
    test_start 'AC#1.6 (CMD-001): $ARGUMENTS parsing logic exists'

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for argument parsing (ARGUMENTS variable or args parsing)
    if assert_file_contains_extended "${COMMAND_FILE}" "(\\\$ARGUMENTS|ARG|argument|parse|query.?type)"; then
        test_pass
    else
        test_fail "Argument parsing logic not found"
    fi
}

###############################################################################
# SECTION 3: AC#2 - Query Routing to Skill
# Tests that command routes to devforgeai-insights skill
###############################################################################

test_ac2_skill_invocation_exists() {
    test_start "AC#2.1 (CMD-002): devforgeai-insights skill invocation exists"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for skill invocation pattern
    if assert_file_contains "${COMMAND_FILE}" "devforgeai-insights"; then
        test_pass
    else
        test_fail "devforgeai-insights skill invocation not found"
    fi
}

test_ac2_skill_pattern_correct() {
    test_start "AC#2.2: Skill invocation uses correct pattern (Skill() or Skill command)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for proper skill invocation syntax
    if assert_file_contains_extended "${COMMAND_FILE}" "(Skill\(|Skill command|invoke.*skill|skill.*=|@devforgeai)"; then
        test_pass
    else
        test_fail "Skill invocation does not use correct pattern"
    fi
}

test_ac2_query_type_passed_to_skill() {
    test_start "AC#2.3: Query type is passed to skill as parameter"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for parameter passing to skill
    if assert_file_contains_extended "${COMMAND_FILE}" "(--query|--type|query.*=|type.*=|mode.*=|QUERY_TYPE)"; then
        test_pass
    else
        test_fail "Query type parameter passing not found"
    fi
}

###############################################################################
# SECTION 4: AC#3 - Help Documentation
# Tests that help is properly documented and accessible
###############################################################################

test_ac3_help_flag_documented() {
    test_start "AC#3.1 (CMD-003): --help flag is documented"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for --help flag documentation
    if assert_file_contains "${COMMAND_FILE}" "\-\-help"; then
        test_pass
    else
        test_fail "--help flag not documented"
    fi
}

test_ac3_help_lists_all_query_types() {
    test_start "AC#3.2: Help section lists all query types"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check that all five query types are mentioned in help
    local query_types=("workflows" "errors" "decisions" "story")
    local missing_types=()

    for qtype in "${query_types[@]}"; do
        if ! assert_file_contains "${COMMAND_FILE}" "${qtype}"; then
            missing_types+=("${qtype}")
        fi
    done

    if [[ ${#missing_types[@]} -eq 0 ]]; then
        test_pass
    else
        test_fail "Help missing query types: ${missing_types[*]}"
    fi
}

test_ac3_help_includes_examples() {
    test_start "AC#3.3: Help includes usage examples"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for example commands (code blocks with /insights)
    if assert_file_contains_extended "${COMMAND_FILE}" "(\`/insights|/insights.*example|Example|example)"; then
        test_pass
    else
        test_fail "Usage examples not found in help"
    fi
}

test_ac3_help_describes_parameters() {
    test_start "AC#3.4: Help describes parameter format for each query type"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for parameter descriptions
    if assert_file_contains_extended "${COMMAND_FILE}" "(parameter|argument|STORY-[0-9]|query.*string|\[query\]|\[STORY)"; then
        test_pass
    else
        test_fail "Parameter descriptions not found"
    fi
}

###############################################################################
# SECTION 5: AC#4 - Error Handling
# Tests that invalid input produces clear error messages
###############################################################################

test_ac4_invalid_query_type_error() {
    test_start "AC#4.1: Invalid query type produces error message"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for error handling of invalid query types
    if assert_file_contains_extended "${COMMAND_FILE}" "(invalid|unknown|unrecognized|not.*supported|error|Error)"; then
        test_pass
    else
        test_fail "Invalid query type error handling not found"
    fi
}

test_ac4_error_lists_valid_options() {
    test_start "AC#4.2: Error message includes list of valid query types"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check that error handling references valid options
    if assert_file_contains_extended "${COMMAND_FILE}" "(valid.*options|supported.*types|available|Valid query types)"; then
        test_pass
    else
        test_fail "Error message does not list valid options"
    fi
}

test_ac4_missing_story_id_error() {
    test_start "AC#4.3: '/insights story' without STORY-ID produces error"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for error handling when story ID is missing
    if assert_file_contains_extended "${COMMAND_FILE}" "(STORY.*required|missing.*STORY|story.*ID.*required|requires.*STORY)"; then
        test_pass
    else
        test_fail "Missing STORY-ID error handling not found"
    fi
}

test_ac4_error_message_actionable() {
    test_start "AC#4.4: Error messages provide actionable guidance"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for actionable guidance (usage, help reference)
    if assert_file_contains_extended "${COMMAND_FILE}" "(Usage|usage|try.*--help|see.*help|run.*--help)"; then
        test_pass
    else
        test_fail "Error messages lack actionable guidance"
    fi
}

###############################################################################
# SECTION 6: Technical Requirements - Command Size and Structure
###############################################################################

test_command_under_500_lines() {
    test_start "Command file is under 500 lines (per source-tree.md constraint)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    local line_count=$(count_file_lines "${COMMAND_FILE}")

    if [[ ${line_count} -lt 500 ]]; then
        test_pass
    else
        test_fail "Command file has ${line_count} lines (max 500)"
    fi
}

test_has_yaml_frontmatter_delimiters() {
    test_start "File has proper YAML frontmatter delimiters (---)"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for opening and closing YAML delimiters (handle CRLF line endings)
    local delimiter_count=$(tr -d '\r' < "${PROJECT_ROOT}/${COMMAND_FILE}" | grep -c "^---$" 2>/dev/null || echo "0")

    if [[ ${delimiter_count} -ge 2 ]]; then
        test_pass
    else
        test_fail "Missing YAML frontmatter delimiters (found ${delimiter_count}, need at least 2)"
    fi
}

test_has_markdown_heading() {
    test_start "File has Markdown heading for command"

    if ! assert_file_exists "${COMMAND_FILE}"; then
        test_fail "File not found: ${PROJECT_ROOT}/${COMMAND_FILE}"
        return
    fi

    # Check for level 1 or 2 heading with command name
    if assert_file_contains_extended "${COMMAND_FILE}" "^#{1,2}.*(/insights|insights|Insights)"; then
        test_pass
    else
        test_fail "Missing Markdown heading for command"
    fi
}

###############################################################################
# Test Suite Execution
###############################################################################

main() {
    echo "=============================================================="
    echo "STORY-224 Test Suite: /insights Command with Query Routing"
    echo "Test Framework: Bash shell scripts (DevForgeAI standard)"
    echo "TDD Status: RED PHASE (All tests expected to FAIL)"
    echo "=============================================================="
    echo ""
    echo -e "${CYAN}Section 1: Command File Existence and YAML Frontmatter${NC}"
    echo "--------------------------------------------------------------"

    # Section 1: File existence and YAML frontmatter
    test_command_file_exists
    test_yaml_frontmatter_has_description
    test_yaml_frontmatter_has_argument_hint
    test_yaml_frontmatter_has_model
    test_yaml_frontmatter_has_allowed_tools
    test_has_yaml_frontmatter_delimiters
    test_has_markdown_heading

    echo ""
    echo -e "${CYAN}Section 2: AC#1 - Command Parameter Support${NC}"
    echo "--------------------------------------------------------------"

    # Section 2: AC#1 tests
    test_ac1_dashboard_query_type
    test_ac1_workflows_query_type
    test_ac1_errors_query_type
    test_ac1_decisions_query_type
    test_ac1_story_query_type
    test_ac1_argument_parsing_logic

    echo ""
    echo -e "${CYAN}Section 3: AC#2 - Query Routing to Skill${NC}"
    echo "--------------------------------------------------------------"

    # Section 3: AC#2 tests
    test_ac2_skill_invocation_exists
    test_ac2_skill_pattern_correct
    test_ac2_query_type_passed_to_skill

    echo ""
    echo -e "${CYAN}Section 4: AC#3 - Help Documentation${NC}"
    echo "--------------------------------------------------------------"

    # Section 4: AC#3 tests
    test_ac3_help_flag_documented
    test_ac3_help_lists_all_query_types
    test_ac3_help_includes_examples
    test_ac3_help_describes_parameters

    echo ""
    echo -e "${CYAN}Section 5: AC#4 - Error Handling${NC}"
    echo "--------------------------------------------------------------"

    # Section 5: AC#4 tests
    test_ac4_invalid_query_type_error
    test_ac4_error_lists_valid_options
    test_ac4_missing_story_id_error
    test_ac4_error_message_actionable

    echo ""
    echo -e "${CYAN}Section 6: Technical Requirements${NC}"
    echo "--------------------------------------------------------------"

    # Section 6: Technical requirements
    test_command_under_500_lines

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
        echo "Next step: Create .claude/commands/insights.md to make tests pass."
        return 1
    fi
}

# Run test suite
main "$@"
