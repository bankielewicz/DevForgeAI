#!/bin/sh
# STORY-376 AC#4: Integration Tests Cover Error Scenarios
# Validates:
#   (a) Binary missing from PATH - graceful fallback to Grep
#   (b) Daemon crashed/unresponsive - starts it or falls back
#   (c) Corrupted/missing index - re-indexing or Grep fallback
#   (d) No unhandled exceptions, no workflow halts, proper fallback
#
# Exit code: 0 = all pass, 1 = any failure
# POSIX-compatible shell syntax for cross-platform support

set -e

# Source shared helpers (DRY: helpers, counters, config)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "${SCRIPT_DIR}/test_helpers.sh"
init_test_env

# Shared reference path (used across multiple tests)
shared_ref="${SUBAGENT_DIR}/references/treelint-search-patterns.md"

# -------------------------------------------------------------------
# Test 1: Binary missing from PATH - graceful fallback
# Subagents must handle treelint command not found (exit code 127)
# Pattern: "command -v", "not found", "exit 127", "binary not found"
# -------------------------------------------------------------------
printf "=== AC#4 Test 1: Binary missing from PATH - graceful fallback ===\n"
binary_missing_count=0
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if ! assert_agent_exists "$agent" "binary-missing handling"; then continue; fi
    # Check for error handling patterns related to binary not found
    if grep -qi "command -v\|not found\|exit.*127\|binary.*missing\|not installed\|unavailable" "$agent_file" 2>/dev/null && \
       grep -qi "fallback\|fall back" "$agent_file" 2>/dev/null; then
        binary_missing_count=$((binary_missing_count + 1))
        pass_test "${agent}.md handles binary-missing scenario with fallback"
    else
        fail_test "${agent}.md does NOT handle binary-missing scenario"
    fi
done

if [ "$binary_missing_count" -lt 3 ]; then
    fail_test "Fewer than 3 subagents handle binary-missing scenario (found: ${binary_missing_count})"
fi

# -------------------------------------------------------------------
# Test 2: Daemon crashed/unresponsive - starts it or falls back
# Pattern: "daemon", "unresponsive", "crashed", "socket", "ECONNREFUSED"
# -------------------------------------------------------------------
printf "\n=== AC#4 Test 2: Daemon crash/unresponsive handling ===\n"
daemon_handling_count=0

# Check shared reference file for daemon handling patterns
if [ -f "$shared_ref" ]; then
    if grep -qi "daemon\|socket\|ECONNREFUSED\|connection.*refused\|unresponsive" "$shared_ref" 2>/dev/null; then
        daemon_handling_count=$((daemon_handling_count + 1))
        pass_test "Shared reference handles daemon crash scenario"
    else
        fail_test "Shared reference does NOT handle daemon crash scenario"
    fi
else
    fail_test "Shared reference file not found"
fi

# Check individual subagents
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi
    if grep -qi "daemon\|socket\|ECONNREFUSED\|connection.*refused" "$agent_file" 2>/dev/null; then
        daemon_handling_count=$((daemon_handling_count + 1))
    fi
done

if [ "$daemon_handling_count" -gt 0 ]; then
    pass_test "Daemon crash handling found in ${daemon_handling_count} file(s)"
else
    fail_test "No daemon crash handling found in any subagent or reference"
fi

# -------------------------------------------------------------------
# Test 3: Corrupted/missing index - re-indexing or Grep fallback
# Pattern: "index", "corrupted", "re-index", "index.db", "missing index"
# -------------------------------------------------------------------
printf "\n=== AC#4 Test 3: Corrupted/missing index handling ===\n"
index_handling_count=0

# Check shared reference file
if [ -f "$shared_ref" ]; then
    if grep -qi "index\|re-index\|corrupted\|index\.db\|rebuild" "$shared_ref" 2>/dev/null; then
        index_handling_count=$((index_handling_count + 1))
        pass_test "Shared reference handles corrupted/missing index scenario"
    else
        fail_test "Shared reference does NOT handle corrupted/missing index"
    fi
fi

# Check individual subagents for index handling
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi
    if grep -qi "index\|re-index\|corrupted" "$agent_file" 2>/dev/null; then
        index_handling_count=$((index_handling_count + 1))
    fi
done

if [ "$index_handling_count" -gt 0 ]; then
    pass_test "Index error handling found in ${index_handling_count} file(s)"
else
    fail_test "No index error handling found in any subagent or reference"
fi

# -------------------------------------------------------------------
# Test 4: No unhandled exceptions - workflow continues on error
# Pattern: "continue", "non-blocking", "warning", "never HALT"
# -------------------------------------------------------------------
printf "\n=== AC#4 Test 4: No unhandled exceptions (non-blocking errors) ===\n"
non_blocking_count=0
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi
    if grep -qi "non-blocking\|never HALT\|do NOT HALT\|warning.*level\|continue.*workflow\|workflow.*continue" "$agent_file" 2>/dev/null; then
        non_blocking_count=$((non_blocking_count + 1))
    fi
done

# Also check shared reference
if [ -f "$shared_ref" ]; then
    if grep -qi "non-blocking\|never HALT\|do NOT HALT\|warning" "$shared_ref" 2>/dev/null; then
        non_blocking_count=$((non_blocking_count + 1))
    fi
fi

if [ "$non_blocking_count" -ge 2 ]; then
    pass_test "Non-blocking error handling found in ${non_blocking_count} file(s)"
else
    fail_test "Insufficient non-blocking error handling (found: ${non_blocking_count}, expected >= 2)"
fi

# -------------------------------------------------------------------
# Test 5: Version check handling (edge case from story)
# Pattern: version, v0.12.0, minimum version
# -------------------------------------------------------------------
printf "\n=== AC#4 Test 5: Version check handling ===\n"
version_check_count=0

# Check shared reference
if [ -f "$shared_ref" ]; then
    if grep -qi "version\|v0\.12" "$shared_ref" 2>/dev/null; then
        version_check_count=$((version_check_count + 1))
        pass_test "Shared reference contains version checking patterns"
    else
        fail_test "Shared reference MISSING version checking patterns"
    fi
fi

# Check subagents
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi
    if grep -qi "version.*0\.12\|v0\.12\|minimum.*version\|version.*check" "$agent_file" 2>/dev/null; then
        version_check_count=$((version_check_count + 1))
    fi
done

if [ "$version_check_count" -gt 0 ]; then
    pass_test "Version checking found in ${version_check_count} file(s)"
else
    fail_test "No version checking patterns found"
fi

# -------------------------------------------------------------------
# Test 6: Exit code distinction (exit 0 with empty != failure)
# Pattern: "exit 0", "empty results", "exit code 0"
# -------------------------------------------------------------------
printf "\n=== AC#4 Test 6: Exit code distinction (empty != failure) ===\n"
exit_code_count=0

if [ -f "$shared_ref" ]; then
    if grep -qi "exit.*0.*empty\|empty.*result\|exit code 0" "$shared_ref" 2>/dev/null; then
        exit_code_count=$((exit_code_count + 1))
    fi
fi

for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi
    if grep -qi "exit.*0.*empty\|empty.*result\|exit code 0.*not.*failure\|NOT failure" "$agent_file" 2>/dev/null; then
        exit_code_count=$((exit_code_count + 1))
    fi
done

if [ "$exit_code_count" -gt 0 ]; then
    pass_test "Exit code distinction documented in ${exit_code_count} file(s)"
else
    fail_test "No exit code distinction (empty results vs failure) documented"
fi

# -------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------
print_summary_and_exit "AC#4"
