#!/bin/sh
# STORY-376 AC#2: Integration Tests Cover Hybrid Fallback Logic
# Validates:
#   (a) Supported extensions trigger Treelint invocation patterns
#   (b) Unsupported extensions trigger Grep fallback patterns
#   (c) Fallback occurs without error messages or workflow interruption
#   (d) Supported language list matches canonical list in tech-stack.md
#
# Exit code: 0 = all pass, 1 = any failure
# POSIX-compatible shell syntax for cross-platform support

set -e

# Source shared helpers (DRY: helpers, counters, config)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "${SCRIPT_DIR}/test_helpers.sh"
init_test_env

# -------------------------------------------------------------------
# Test 1: tech-stack.md contains the canonical supported language list
# -------------------------------------------------------------------
printf "=== AC#2 Test 1: Canonical language list in tech-stack.md ===\n"
if [ ! -f "$TECH_STACK" ]; then
    fail_test "tech-stack.md not found at ${TECH_STACK}"
else
    # Verify each supported extension is documented in tech-stack.md
    for ext in $SUPPORTED_EXTENSIONS; do
        ext_pattern=$(echo "$ext" | sed 's/\./\\./g')
        if grep -q "\`${ext_pattern}\`" "$TECH_STACK" 2>/dev/null; then
            pass_test "Extension ${ext} documented in tech-stack.md"
        else
            fail_test "Extension ${ext} NOT documented in tech-stack.md"
        fi
    done
fi

# -------------------------------------------------------------------
# Test 2: Subagents reference supported extensions for Treelint
# At least one subagent must mention supported extensions in context
# -------------------------------------------------------------------
printf "\n=== AC#2 Test 2: Supported extensions trigger Treelint ===\n"
found_supported=0
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi
    # Check if the subagent mentions supported languages/extensions alongside treelint
    if grep -qi "\.py\|\.ts\|\.tsx\|\.js\|\.jsx\|\.rs\|\.md" "$agent_file" 2>/dev/null && \
       grep -qi "treelint" "$agent_file" 2>/dev/null; then
        found_supported=$((found_supported + 1))
    fi
done

if [ "$found_supported" -gt 0 ]; then
    pass_test "At least ${found_supported} subagent(s) reference supported extensions with Treelint"
else
    fail_test "No subagents reference supported extensions alongside Treelint"
fi

# -------------------------------------------------------------------
# Test 3: Subagents define Grep fallback for unsupported extensions
# -------------------------------------------------------------------
printf "\n=== AC#2 Test 3: Unsupported extensions trigger Grep fallback ===\n"
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if ! assert_agent_exists "$agent" "unsupported extension handling"; then continue; fi
    # Check for fallback/grep patterns indicating unsupported language handling
    if grep -qi "unsupported\|fallback.*grep\|grep.*fallback\|fall back" "$agent_file" 2>/dev/null; then
        pass_test "${agent}.md contains unsupported extension fallback logic"
    else
        fail_test "${agent}.md does NOT contain unsupported extension fallback logic"
    fi
done

# -------------------------------------------------------------------
# Test 4: Fallback is silent (no HALT, no error, warning-level only)
# Validates: fallback occurs without workflow interruption
# -------------------------------------------------------------------
printf "\n=== AC#2 Test 4: Fallback is non-blocking (no HALT on fallback) ===\n"
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if ! assert_agent_exists "$agent" "non-blocking fallback"; then continue; fi
    # Check for evidence that fallback does not halt the workflow
    if grep -qi "fallback" "$agent_file" 2>/dev/null; then
        # If fallback is mentioned, check it doesn't mandate HALT on fallback
        fallback_halt=$(grep -n "fallback" "$agent_file" 2>/dev/null | grep -ic "HALT" 2>/dev/null || echo "0")
        if [ "$fallback_halt" = "0" ] || grep -qi "never HALT\|do NOT HALT\|non-blocking" "$agent_file" 2>/dev/null; then
            pass_test "${agent}.md fallback does not trigger HALT"
        else
            fail_test "${agent}.md fallback may trigger HALT (blocking)"
        fi
    else
        # No fallback mentioned at all - this is a gap
        fail_test "${agent}.md has no fallback logic to evaluate"
    fi
done

# -------------------------------------------------------------------
# Test 5: Language list consistency across subagents
# At least 3 subagents should reference the same supported language set
# -------------------------------------------------------------------
printf "\n=== AC#2 Test 5: Language list consistency across subagents ===\n"
py_count=0
ts_count=0
for agent in $SUBAGENTS; do
    agent_file=$(agent_file_path "$agent")
    if [ ! -f "$agent_file" ]; then continue; fi
    if grep -q "\.py" "$agent_file" 2>/dev/null; then
        py_count=$((py_count + 1))
    fi
    if grep -q "\.ts" "$agent_file" 2>/dev/null; then
        ts_count=$((ts_count + 1))
    fi
done

if [ "$py_count" -ge 3 ]; then
    pass_test "Python (.py) referenced by ${py_count} subagents (consistency >= 3)"
else
    fail_test "Python (.py) referenced by only ${py_count} subagents (expected >= 3)"
fi

if [ "$ts_count" -ge 2 ]; then
    pass_test "TypeScript (.ts) referenced by ${ts_count} subagents (consistency >= 2)"
else
    fail_test "TypeScript (.ts) referenced by only ${ts_count} subagents (expected >= 2)"
fi

# -------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------
print_summary_and_exit "AC#2"
