#!/bin/bash

##############################################################################
# Test Suite: STORY-390 AC#4 - Version History Accessible for Audit
# Purpose: Verify history subcommand reads VERSION-HISTORY.md, displays
#          Markdown table with Version/Date/Before Hash/After Hash/Type/Reason
#          columns, supports single component and "all" mode
#
# Implementation: src/claude/commands/prompt-version.md (Slash Command)
# Test Type: Structural + Pattern (Markdown Command Testing Pattern)
#
# All tests MUST FAIL (TDD RED) until implementation exists.
##############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
IMPL_FILE="${PROJECT_ROOT}/src/claude/commands/prompt-version.md"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>/dev/null; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "  ${GREEN}PASS${NC}: $test_name"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "  ${RED}FAIL${NC}: $test_name"
    fi
}

##############################################################################
# AC#4 Tests: Version History Accessible for Audit
##############################################################################

# --- Structural Tests ---

test_implementation_file_exists() {
    [ -f "$IMPL_FILE" ]
}

test_has_history_subcommand_section() {
    # Must have a section documenting the history subcommand
    grep -qiE "^#{1,3}.*[Hh]istory" "$IMPL_FILE"
}

# --- Pattern Tests: VERSION-HISTORY.md Reading ---

test_history_reads_version_history_file() {
    # History must read VERSION-HISTORY.md for specified component
    grep -qiE "(Read\(.*VERSION-HISTORY|VERSION-HISTORY\.md.*Read)" "$IMPL_FILE"
}

test_history_reads_from_prompt_versions_dir() {
    # History must read from devforgeai/specs/prompt-versions/ directory
    grep -q "devforgeai/specs/prompt-versions/" "$IMPL_FILE"
}

# --- Pattern Tests: Table Display Columns ---

test_table_has_version_column() {
    # Display table must have Version column
    grep -qiE "(\|.*[Vv]ersion.*\||Version.*column)" "$IMPL_FILE"
}

test_table_has_date_column() {
    # Display table must have Date column
    grep -qiE "(\|.*[Dd]ate.*\||Date.*column)" "$IMPL_FILE"
}

test_table_has_before_hash_column() {
    # Display table must have Before Hash column (first 8 chars)
    grep -qiE "([Bb]efore.*[Hh]ash.*8|first.*8.*char.*before)" "$IMPL_FILE"
}

test_table_has_after_hash_column() {
    # Display table must have After Hash column (first 8 chars)
    grep -qiE "([Aa]fter.*[Hh]ash.*8|first.*8.*char.*after)" "$IMPL_FILE"
}

test_table_has_type_column() {
    # Display table must have Type column (migration|rollback|update)
    grep -qiE "(\|.*[Tt]ype.*\||migration.*rollback.*update)" "$IMPL_FILE"
}

test_table_has_reason_column() {
    # Display table must have Reason column
    grep -qiE "(\|.*[Rr]eason.*\||reason.*column)" "$IMPL_FILE"
}

test_hash_display_truncated_8_chars() {
    # Hash display must show first 8 characters only
    grep -qiE "(first.*8|8.*char|truncat.*8|\[:8\])" "$IMPL_FILE"
}

# --- Pattern Tests: "all" Mode ---

test_history_supports_all_mode() {
    # History must support "all" keyword for full audit across all components
    grep -qiE '("all"|all.*mode|all.*component)' "$IMPL_FILE"
}

test_all_mode_groups_by_component() {
    # "all" mode must group entries by component
    grep -qiE "(group.*by.*component|component.*group|per.*component)" "$IMPL_FILE"
}

test_all_mode_shows_component_type() {
    # "all" mode must show component_type headers
    grep -qiE "(component_type.*header|type.*header|header.*component_type)" "$IMPL_FILE"
}

test_all_mode_shows_file_path() {
    # "all" mode must show file_path per component
    grep -qiE "(file_path.*header|header.*file_path|path.*per.*component)" "$IMPL_FILE"
}

# --- Pattern Tests: Counts ---

test_shows_version_count_per_component() {
    # History must show total version count per component
    grep -qiE "(total.*version.*count|version.*count|count.*per.*component)" "$IMPL_FILE"
}

test_shows_overall_count() {
    # History must show overall total count
    grep -qiE "(overall.*total|total.*overall|total.*count)" "$IMPL_FILE"
}

# --- Pattern Tests: Output Format ---

test_output_in_markdown_format() {
    # Output must be in Markdown table format
    grep -qiE "([Mm]arkdown.*table|table.*format|\|.*---.*\|)" "$IMPL_FILE"
}

# --- Pattern Tests: Glob for Component Discovery ---

test_uses_glob_for_component_discovery() {
    # "all" mode must use Glob to discover component directories
    grep -qiE "(Glob\(|glob.*pattern|discover.*component)" "$IMPL_FILE"
}

# --- Edge Case Tests ---

test_handles_empty_version_history() {
    # Must handle component with no version history
    grep -qiE "(no.*version.*history|empty.*history|no.*entries)" "$IMPL_FILE"
}

test_handles_corrupted_snapshot() {
    # Must handle corrupted or missing snapshot files gracefully
    grep -qiE "(snapshot.*unavailable|corrupted.*snapshot|WARNING.*snapshot)" "$IMPL_FILE"
}

test_handles_nonexistent_component() {
    # Must handle history request for component that does not exist
    grep -qiE "(component.*not.*found|no.*such.*component|unknown.*component)" "$IMPL_FILE"
}

##############################################################################
# Test Execution
##############################################################################

echo "=============================================="
echo "  STORY-390 AC#4: Version History Audit"
echo "  TDD Phase: RED (tests must fail)"
echo "=============================================="

# Structural Tests
run_test "Implementation file exists" test_implementation_file_exists
run_test "Has history subcommand section" test_has_history_subcommand_section

# Pattern Tests: Reading
run_test "History reads VERSION-HISTORY.md" test_history_reads_version_history_file
run_test "History reads from prompt-versions dir" test_history_reads_from_prompt_versions_dir

# Pattern Tests: Table Columns
run_test "Table has Version column" test_table_has_version_column
run_test "Table has Date column" test_table_has_date_column
run_test "Table has Before Hash column" test_table_has_before_hash_column
run_test "Table has After Hash column" test_table_has_after_hash_column
run_test "Table has Type column" test_table_has_type_column
run_test "Table has Reason column" test_table_has_reason_column
run_test "Hash display truncated to 8 chars" test_hash_display_truncated_8_chars

# Pattern Tests: "all" mode
run_test "History supports 'all' mode" test_history_supports_all_mode
run_test "All mode groups by component" test_all_mode_groups_by_component
run_test "All mode shows component_type" test_all_mode_shows_component_type
run_test "All mode shows file_path" test_all_mode_shows_file_path

# Pattern Tests: Counts
run_test "Shows version count per component" test_shows_version_count_per_component
run_test "Shows overall count" test_shows_overall_count

# Pattern Tests: Output Format
run_test "Output in Markdown format" test_output_in_markdown_format

# Pattern Tests: Glob
run_test "Uses Glob for component discovery" test_uses_glob_for_component_discovery

# Edge Case Tests
run_test "Handles empty version history" test_handles_empty_version_history
run_test "Handles corrupted snapshot" test_handles_corrupted_snapshot
run_test "Handles nonexistent component" test_handles_nonexistent_component

##############################################################################
# Summary
##############################################################################

echo ""
echo "=============================================="
echo "  AC#4 Test Results"
echo "=============================================="
echo -e "  Total:  ${TESTS_RUN}"
echo -e "  Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "  Failed: ${RED}${TESTS_FAILED}${NC}"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo -e "${RED}RESULT: FAIL${NC} - $TESTS_FAILED test(s) failed (TDD RED confirmed)"
    exit 1
else
    echo -e "${GREEN}RESULT: PASS${NC} - All tests passed"
    exit 0
fi
