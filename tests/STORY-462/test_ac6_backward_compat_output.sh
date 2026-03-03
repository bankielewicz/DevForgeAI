#!/bin/bash
# Test: AC#6 - Backward-compatible output preserved
# Story: STORY-462
# Generated: 2026-02-21
# TDD Phase: RED (all tests expected to FAIL before implementation)
# Checks that scanning logic, error messages, and display formats are preserved
# in the new skill / trimmed commands or their references.

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#6: Backward-compatible output preserved ==="

SKILL_FILE="$PROJECT_ROOT/src/claude/skills/auditing-w3-compliance/SKILL.md"
ORCHESTRATE_CMD="$PROJECT_ROOT/src/claude/commands/orchestrate.md"
ORCHESTRATE_REFS_DIR="$PROJECT_ROOT/src/claude/commands/references/orchestrate"
RCA_CMD="$PROJECT_ROOT/src/claude/commands/create-stories-from-rca.md"

# === audit-w3 skill: 4 scanning phases must be present ===

# --- Test 1: CRITICAL scanning section in skill ---
if [ -f "$SKILL_FILE" ]; then
    grep -qi "CRITICAL" "$SKILL_FILE"
    run_test "audit-w3 skill contains CRITICAL scanning section" $?
else
    echo "  FAIL: auditing-w3-compliance/SKILL.md does not exist"
    ((FAILED++))
fi

# --- Test 2: HIGH scanning section in skill ---
if [ -f "$SKILL_FILE" ]; then
    grep -qi "HIGH" "$SKILL_FILE"
    run_test "audit-w3 skill contains HIGH scanning section" $?
else
    echo "  FAIL: auditing-w3-compliance/SKILL.md does not exist"
    ((FAILED++))
fi

# --- Test 3: MEDIUM scanning section in skill ---
if [ -f "$SKILL_FILE" ]; then
    grep -qi "MEDIUM" "$SKILL_FILE"
    run_test "audit-w3 skill contains MEDIUM scanning section" $?
else
    echo "  FAIL: auditing-w3-compliance/SKILL.md does not exist"
    ((FAILED++))
fi

# --- Test 4: INFO scanning section in skill ---
if [ -f "$SKILL_FILE" ]; then
    grep -qi "INFO" "$SKILL_FILE"
    run_test "audit-w3 skill contains INFO scanning section" $?
else
    echo "  FAIL: auditing-w3-compliance/SKILL.md does not exist"
    ((FAILED++))
fi

# === orchestrate: governance sections preserved in command or references ===
# Search command + any reference files in orchestration skill references directory

search_orchestrate() {
    local pattern="$1"
    # Search command file
    if [ -f "$ORCHESTRATE_CMD" ] && grep -qi "$pattern" "$ORCHESTRATE_CMD" 2>/dev/null; then
        return 0
    fi
    # Search references directory if it exists
    if [ -d "$ORCHESTRATE_REFS_DIR" ]; then
        if grep -rqi "$pattern" "$ORCHESTRATE_REFS_DIR" 2>/dev/null; then
            return 0
        fi
    fi
    return 1
}

# --- Test 5: "Checkpoint Resume" found in orchestrate command or references ---
search_orchestrate "Checkpoint Resume"
run_test "orchestrate: 'Checkpoint Resume' found in command or references" $?

# --- Test 6: "QA Retry" found in orchestrate command or references ---
search_orchestrate "QA Retry"
run_test "orchestrate: 'QA Retry' found in command or references" $?

# --- Test 7: "Manual Phase Execution" found in orchestrate command or references ---
search_orchestrate "Manual Phase Execution"
run_test "orchestrate: 'Manual Phase Execution' found in command or references" $?

# === create-stories-from-rca: Help, Error, Business Rules preserved ===

search_rca_all() {
    local pattern="$1"
    # Search command file
    if [ -f "$RCA_CMD" ] && grep -qi "$pattern" "$RCA_CMD" 2>/dev/null; then
        return 0
    fi
    # Search command references directory for create-stories-from-rca
    local rca_refs="$PROJECT_ROOT/src/claude/commands/references/create-stories-from-rca"
    if [ -d "$rca_refs" ] && grep -rqi "$pattern" "$rca_refs" 2>/dev/null; then
        return 0
    fi
    return 1
}

# --- Test 8: Help text or help content preserved ---
search_rca_all "Help"
run_test "create-stories-from-rca: 'Help' content preserved in command or references" $?

# --- Test 9: Error messages or templates preserved ---
search_rca_all "Error"
run_test "create-stories-from-rca: 'Error' content preserved in command or references" $?

# --- Test 10: Business Rules preserved ---
search_rca_all "Business Rule"
run_test "create-stories-from-rca: 'Business Rule' content preserved in command or references" $?

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
