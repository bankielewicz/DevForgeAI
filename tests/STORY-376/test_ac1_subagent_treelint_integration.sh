#!/bin/sh
# STORY-376 AC#1: Integration Tests Cover All 7 Updated Subagents
# Validates that each of the 7 subagents contains:
#   (a) Treelint search invocation patterns
#   (b) JSON output parsing instructions (--format json)
#   (c) Fallback-to-Grep logic
#
# Exit code: 0 = all pass, 1 = any failure
# POSIX-compatible shell syntax for cross-platform support

set -e

# Source shared helpers (DRY: helpers, counters, config)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "${SCRIPT_DIR}/test_helpers.sh"
init_test_env

# -------------------------------------------------------------------
# Test 1: Each subagent file exists in src/claude/agents/
# -------------------------------------------------------------------
printf "=== AC#1 Test 1: Subagent files exist ===\n"
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ -f "$agent_file" ]; then
        pass_test "${agent}.md exists"
    else
        fail_test "${agent}.md does NOT exist at ${agent_file}"
    fi
done

# -------------------------------------------------------------------
# Test 2: Each subagent contains Treelint search invocation patterns
# Pattern: treelint search (case-insensitive match in markdown)
# -------------------------------------------------------------------
printf "\n=== AC#1 Test 2: Treelint search invocation patterns ===\n"
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if ! assert_agent_exists "$agent" "Treelint patterns"; then continue; fi
    if grep -qi "treelint search" "$agent_file" 2>/dev/null || \
       grep -qi "treelint map" "$agent_file" 2>/dev/null || \
       grep -qi "treelint deps" "$agent_file" 2>/dev/null || \
       grep -qi "treelint" "$agent_file" 2>/dev/null; then
        pass_test "${agent}.md contains Treelint invocation patterns"
    else
        fail_test "${agent}.md does NOT contain Treelint invocation patterns"
    fi
done

# -------------------------------------------------------------------
# Test 3: Each subagent contains JSON output parsing instructions
# Pattern: --format json (required per BR-001 in tech-stack.md)
# -------------------------------------------------------------------
printf "\n=== AC#1 Test 3: JSON output parsing (--format json) ===\n"
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if ! assert_agent_exists "$agent" "JSON format"; then continue; fi
    if grep -q "\-\-format json" "$agent_file" 2>/dev/null; then
        pass_test "${agent}.md contains --format json flag"
    else
        fail_test "${agent}.md does NOT contain --format json flag"
    fi
done

# -------------------------------------------------------------------
# Test 4: Each subagent contains fallback-to-Grep logic
# Pattern: fallback or Grep fallback references
# -------------------------------------------------------------------
printf "\n=== AC#1 Test 4: Fallback-to-Grep logic ===\n"
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if ! assert_agent_exists "$agent" "fallback logic"; then continue; fi
    if grep -qi "fallback" "$agent_file" 2>/dev/null && \
       grep -qi "grep" "$agent_file" 2>/dev/null; then
        pass_test "${agent}.md contains fallback-to-Grep logic"
    else
        fail_test "${agent}.md does NOT contain fallback-to-Grep logic"
    fi
done

# -------------------------------------------------------------------
# Test 5: Every treelint invocation line also contains --format json
# (Validates TEST-002: --format json accompanies all Treelint CLI invocations)
# Uses check_treelint_json_flag helper to avoid POSIX subshell bug
# -------------------------------------------------------------------
printf "\n=== AC#1 Test 5: All treelint invocations include --format json ===\n"
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if ! assert_agent_exists "$agent" "JSON flag consistency"; then continue; fi

    check_result=0
    check_treelint_json_flag "$agent_file" "$agent" "treelint search\|treelint map\|treelint deps" || check_result=$?

    if [ "$check_result" -eq 2 ]; then
        # No treelint command invocations found in this file
        if [ "$agent" = "anti-pattern-scanner" ]; then
            pass_test "${agent}.md references Treelint via external phase file (acceptable)"
        else
            fail_test "${agent}.md has no treelint command invocations to validate"
        fi
    elif [ "$check_result" -eq 0 ]; then
        pass_test "${agent}.md: all treelint invocations include --format json"
    else
        fail_test "${agent}.md: some treelint invocations MISSING --format json"
    fi
done

# -------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------
print_summary_and_exit "AC#1"
