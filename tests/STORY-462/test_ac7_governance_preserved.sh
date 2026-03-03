#!/bin/bash
# Test: AC#7 - Governance, error recovery, and architecture sections preserved
# Story: STORY-462
# Generated: 2026-02-21
# TDD Phase: RED (all tests expected to FAIL before implementation)

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

echo "=== AC#7: Governance sections preserved ==="

ORCHESTRATE_CMD="$PROJECT_ROOT/src/claude/commands/orchestrate.md"
ORCHESTRATE_REFS_DIR="$PROJECT_ROOT/src/claude/commands/references/orchestrate"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/auditing-w3-compliance/SKILL.md"
AUDIT_W3_REFS_DIR="$PROJECT_ROOT/src/claude/skills/auditing-w3-compliance/references"

# Helper: search orchestrate command + references
search_orchestrate() {
    local pattern="$1"
    if [ -f "$ORCHESTRATE_CMD" ] && grep -qi "$pattern" "$ORCHESTRATE_CMD" 2>/dev/null; then
        return 0
    fi
    if [ -d "$ORCHESTRATE_REFS_DIR" ] && grep -rqi "$pattern" "$ORCHESTRATE_REFS_DIR" 2>/dev/null; then
        return 0
    fi
    return 1
}

# Helper: search audit-w3 skill + its references
search_audit_w3() {
    local pattern="$1"
    if [ -f "$SKILL_FILE" ] && grep -qi "$pattern" "$SKILL_FILE" 2>/dev/null; then
        return 0
    fi
    if [ -d "$AUDIT_W3_REFS_DIR" ] && grep -rqi "$pattern" "$AUDIT_W3_REFS_DIR" 2>/dev/null; then
        return 0
    fi
    return 1
}

# === orchestrate governance sections ===

# --- Test 1: "Checkpoint Resume" found in orchestrate command or references ---
search_orchestrate "Checkpoint Resume"
run_test "orchestrate: 'Checkpoint Resume' preserved in command or references" $?

# --- Test 2: "QA Retry" found in orchestrate command or references ---
search_orchestrate "QA Retry"
run_test "orchestrate: 'QA Retry' preserved in command or references" $?

# --- Test 3: "Manual Phase Execution" found in orchestrate command or references ---
search_orchestrate "Manual Phase Execution"
run_test "orchestrate: 'Manual Phase Execution' preserved in command or references" $?

# === audit-w3 governance sections ===

# --- Test 4: "Exclusion" patterns found in audit-w3 skill or its references ---
search_audit_w3 "Exclusion"
run_test "audit-w3 skill: 'Exclusion' patterns preserved in skill or references" $?

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
