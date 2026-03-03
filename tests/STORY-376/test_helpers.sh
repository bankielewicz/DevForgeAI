#!/bin/sh
# STORY-376: Shared test helper functions and configuration
# Sourced by all AC test scripts to enforce DRY principle
#
# Usage:
#   SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
#   . "${SCRIPT_DIR}/test_helpers.sh"
#   init_test_env
# POSIX-compatible shell syntax for cross-platform support

# -------------------------------------------------------------------
# Path resolution (call once per script via init_test_env)
# Requires SCRIPT_DIR to be set by the calling script before sourcing.
# -------------------------------------------------------------------
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

init_test_env() {
    # SCRIPT_DIR must be set by the calling script before sourcing this file
    PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
    SUBAGENT_DIR="${PROJECT_ROOT}/src/claude/agents"
    TEST_DIR="${PROJECT_ROOT}/tests/STORY-376"
    TECH_STACK="${PROJECT_ROOT}/devforgeai/specs/context/tech-stack.md"
}

# -------------------------------------------------------------------
# The 7 subagents updated for Treelint support (BR-003: single definition)
# -------------------------------------------------------------------
SUBAGENTS="test-automator code-reviewer backend-architect security-auditor refactoring-specialist coverage-analyzer anti-pattern-scanner"

# -------------------------------------------------------------------
# All AC test scripts (used by AC#5 and runner)
# -------------------------------------------------------------------
TEST_SCRIPTS="test_helpers.sh test_ac1_subagent_treelint_integration.sh test_ac2_hybrid_fallback_logic.sh test_ac3_advanced_features.sh test_ac4_error_scenarios.sh test_ac5_platform_compatibility.sh test_ac6_results_documentation.sh"

# -------------------------------------------------------------------
# Canonical supported extensions from tech-stack.md (Treelint Language Support)
# -------------------------------------------------------------------
SUPPORTED_EXTENSIONS=".py .ts .tsx .js .jsx .rs .md"

# -------------------------------------------------------------------
# Test result helpers
# -------------------------------------------------------------------
pass_test() {
    PASS_COUNT=$((PASS_COUNT + 1))
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    printf "  PASS: %s\n" "$1"
}

fail_test() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    printf "  FAIL: %s\n" "$1"
}

# -------------------------------------------------------------------
# Print summary and exit with appropriate code
# -------------------------------------------------------------------
print_summary_and_exit() {
    ac_label="${1:-Test}"
    printf "\n=== %s Summary ===\n" "$ac_label"
    printf "Total: %d | Pass: %d | Fail: %d\n" "$TOTAL_TESTS" "$PASS_COUNT" "$FAIL_COUNT"

    if [ "$FAIL_COUNT" -gt 0 ]; then
        printf "RESULT: FAIL\n"
        exit 1
    else
        printf "RESULT: PASS\n"
        exit 0
    fi
}

# -------------------------------------------------------------------
# Resolve agent file path from agent name
# -------------------------------------------------------------------
agent_file_path() {
    echo "${SUBAGENT_DIR}/${1}.md"
}

# -------------------------------------------------------------------
# Check if agent file exists, fail the test if not, return exit status
# Usage: assert_agent_exists "agent-name" "context message"
# Returns: 0 if exists, 1 if not (and records a FAIL)
# -------------------------------------------------------------------
assert_agent_exists() {
    _agent_name="$1"
    _context="${2:-file check}"
    _path="${SUBAGENT_DIR}/${_agent_name}.md"
    if [ ! -f "$_path" ]; then
        fail_test "${_agent_name}.md not found - cannot check ${_context}"
        return 1
    fi
    return 0
}

# -------------------------------------------------------------------
# Check if all treelint invocations in a file include --format json
# Avoids POSIX subshell variable scope bug by using a temp file
# Usage: check_treelint_json_flag "file_path" "label"
# Returns: 0 if all invocations have --format json, 1 otherwise
# -------------------------------------------------------------------
check_treelint_json_flag() {
    _file="$1"
    _label="$2"
    _pattern="${3:-treelint search\|treelint map\|treelint deps}"

    _treelint_lines=$(grep -n "$_pattern" "$_file" 2>/dev/null || true)
    if [ -z "$_treelint_lines" ]; then
        return 2  # No treelint invocations found
    fi

    # Use a temp file to avoid POSIX subshell variable scope issue
    _tmpfile=$(mktemp 2>/dev/null || echo "/tmp/treelint_check_$$")
    echo "0" > "$_tmpfile"

    echo "$_treelint_lines" | while IFS= read -r _line; do
        # Skip prose/header lines -- only check actual CLI invocations
        # CLI invocations contain patterns like: Bash(command=, backtick-wrapped, or --flag syntax
        _is_invocation=false
        if echo "$_line" | grep -q 'Bash(command=\|`treelint\|command="treelint' 2>/dev/null; then
            _is_invocation=true
        fi
        if [ "$_is_invocation" = "true" ]; then
            if ! echo "$_line" | grep -q "\-\-format json"; then
                echo "1" > "$_tmpfile"
            fi
        fi
    done

    _result=$(cat "$_tmpfile")
    rm -f "$_tmpfile" 2>/dev/null
    return "$_result"
}
