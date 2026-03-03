#!/bin/bash
# Test: AC#2 - Legacy Marker Files Deleted
# Story: STORY-519
# Generated: 2026-03-01
# Tests run against src/ tree per CLAUDE.md

PASSED=0
FAILED=0
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

SKILL_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-qa/SKILL.md"
REF_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-qa/references/phase-4-cleanup-workflow.md"

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

echo "=== AC#2: Legacy Marker Files Deleted ==="
echo ""

# --- Arrange ---
if [ ! -f "$SKILL_FILE" ]; then
    echo "  FAIL: SKILL.md not found at $SKILL_FILE"
    exit 1
fi
if [ ! -f "$REF_FILE" ]; then
    echo "  FAIL: Reference file not found at $REF_FILE"
    exit 1
fi

# --- Act & Assert ---

# Test 1: Reference file contains delete instruction for .qa-phase-N.marker files
grep -q "DELETE.*\.qa-phase.*\.marker\|delete.*\.qa-phase.*\.marker\|rm.*\.qa-phase.*\.marker" "$REF_FILE"
run_test "Reference file contains delete instruction for .qa-phase-N.marker" $?

# Test 2: Reference file identifies markers as legacy
grep -qi "legacy.*\.qa-phase.*\.marker\|\.qa-phase.*\.marker.*legacy" "$REF_FILE"
run_test "Reference file identifies .qa-phase-N.marker as legacy" $?

# Test 3: SKILL.md contains delete instruction for .qa-phase-N.marker files
grep -q "DELETE.*\.qa-phase.*\.marker\|delete.*\.qa-phase.*\.marker\|rm.*\.qa-phase.*\.marker" "$SKILL_FILE"
run_test "SKILL.md contains delete instruction for .qa-phase-N.marker" $?

# Test 4: Reference file distinguishes between preserve (state) and delete (markers)
grep -qi "preserve.*qa-phase-state.*delete.*marker\|qa-phase-state.*preserve.*marker.*delete" "$REF_FILE"
run_test "Reference file distinguishes preserve state vs delete markers" $?

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
