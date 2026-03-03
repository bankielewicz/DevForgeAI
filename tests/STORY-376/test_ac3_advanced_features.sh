#!/bin/sh
# STORY-376 AC#3: Integration Tests Cover Advanced Features
# Validates:
#   (a) treelint deps invocation patterns in applicable subagents
#   (b) treelint map invocation patterns in applicable subagents
#   (c) JSON output parsing for advanced feature invocations
#   (d) Fallback behavior for each advanced feature when Treelint unavailable
#
# Exit code: 0 = all pass, 1 = any failure
# POSIX-compatible shell syntax for cross-platform support

set -e

# Source shared helpers (DRY: helpers, counters, config)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "${SCRIPT_DIR}/test_helpers.sh"
init_test_env

# Subagents expected to use treelint deps (dependency analysis)
DEPS_SUBAGENTS="code-reviewer refactoring-specialist"

# Subagents expected to use treelint map (repository map)
MAP_SUBAGENTS="refactoring-specialist"

# -------------------------------------------------------------------
# Test 1: treelint deps invocation patterns in applicable subagents
# -------------------------------------------------------------------
printf "=== AC#3 Test 1: treelint deps invocation patterns ===\n"
deps_found_count=0
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi
    if grep -q "treelint deps" "$agent_file" 2>/dev/null; then
        deps_found_count=$((deps_found_count + 1))
        pass_test "${agent}.md contains treelint deps invocation"
    fi
done

if [ "$deps_found_count" -eq 0 ]; then
    fail_test "No subagent files contain treelint deps invocation patterns"
fi

# Verify expected subagents specifically have deps
for agent in $DEPS_SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if ! assert_agent_exists "$agent" "treelint deps"; then continue; fi
    if grep -q "treelint deps" "$agent_file" 2>/dev/null; then
        pass_test "${agent}.md specifically contains treelint deps (expected)"
    else
        fail_test "${agent}.md does NOT contain treelint deps (expected for this subagent)"
    fi
done

# -------------------------------------------------------------------
# Test 2: treelint map invocation patterns in applicable subagents
# -------------------------------------------------------------------
printf "\n=== AC#3 Test 2: treelint map invocation patterns ===\n"
map_found_count=0
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi
    if grep -q "treelint map" "$agent_file" 2>/dev/null; then
        map_found_count=$((map_found_count + 1))
        pass_test "${agent}.md contains treelint map invocation"
    fi
done

if [ "$map_found_count" -eq 0 ]; then
    fail_test "No subagent files contain treelint map invocation patterns"
fi

# Verify expected subagents specifically have map
for agent in $MAP_SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if ! assert_agent_exists "$agent" "treelint map"; then continue; fi
    if grep -q "treelint map" "$agent_file" 2>/dev/null; then
        pass_test "${agent}.md specifically contains treelint map (expected)"
    else
        fail_test "${agent}.md does NOT contain treelint map (expected for this subagent)"
    fi
done

# -------------------------------------------------------------------
# Test 3: JSON output parsing for advanced features
# All treelint deps/map invocations must include --format json
# Uses check_treelint_json_flag helper to avoid POSIX subshell bug
# -------------------------------------------------------------------
printf "\n=== AC#3 Test 3: JSON parsing for advanced features ===\n"
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi

    check_result=0
    check_treelint_json_flag "$agent_file" "$agent" "treelint deps\|treelint map" || check_result=$?

    if [ "$check_result" -eq 2 ]; then
        continue  # No advanced feature invocations in this file
    elif [ "$check_result" -eq 0 ]; then
        pass_test "${agent}.md: all advanced feature invocations include --format json"
    else
        fail_test "${agent}.md: some advanced feature invocations MISSING --format json"
    fi
done

# -------------------------------------------------------------------
# Test 4: Fallback behavior defined for advanced features
# Check that subagents with deps/map also have fallback patterns
# -------------------------------------------------------------------
printf "\n=== AC#3 Test 4: Fallback behavior for advanced features ===\n"
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi
    if grep -q "treelint deps\|treelint map" "$agent_file" 2>/dev/null; then
        if grep -qi "fallback\|fall back\|unavailable" "$agent_file" 2>/dev/null; then
            pass_test "${agent}.md has fallback defined for advanced features"
        else
            fail_test "${agent}.md uses advanced features but has NO fallback defined"
        fi
    fi
done

# -------------------------------------------------------------------
# Test 5: Shared reference file contains advanced feature patterns
# -------------------------------------------------------------------
printf "\n=== AC#3 Test 5: Shared reference file has advanced feature patterns ===\n"
shared_ref="${SUBAGENT_DIR}/references/treelint-search-patterns.md"
if [ -f "$shared_ref" ]; then
    if grep -q "treelint deps" "$shared_ref" 2>/dev/null; then
        pass_test "Shared reference contains treelint deps patterns"
    else
        fail_test "Shared reference MISSING treelint deps patterns"
    fi
    if grep -q "treelint map" "$shared_ref" 2>/dev/null; then
        pass_test "Shared reference contains treelint map patterns"
    else
        fail_test "Shared reference MISSING treelint map patterns"
    fi
else
    fail_test "Shared reference file not found at ${shared_ref}"
fi

# -------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------
print_summary_and_exit "AC#3"
