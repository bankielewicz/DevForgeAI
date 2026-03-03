#!/bin/bash
# Test: AC#2 - ADR Prerequisite Flagging
# Story: STORY-480
# Generated: 2026-02-23
# State: RED (expects FAIL - Phase N.5 does not yet exist)

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/discovering-requirements/SKILL.md"

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

echo "=== AC#2: ADR Prerequisite Flagging ==="
echo "Target: $TARGET_FILE"
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    exit 1
fi

# Extract Phase N.5 section content (between Constitutional Compliance header and next ### header)
PHASE_CONTENT=$(sed -n '/Constitutional Compliance/,/^### /p' "$TARGET_FILE" 2>/dev/null)

# === Act & Assert ===

# Test 1: Phase references architecture-constraints.md
echo "$PHASE_CONTENT" | grep -q "architecture-constraints.md"
run_test "Phase N.5 references architecture-constraints.md" $?

# Test 2: Phase references context files that trigger ADR requirement
echo "$PHASE_CONTENT" | grep -q "tech-stack.md"
run_test "Phase N.5 references tech-stack.md" $?

# Test 3: Phase mentions ADR prerequisite or Day 0
echo "$PHASE_CONTENT" | grep -q "ADR.*prerequisite\|Day 0\|ADR creation"
run_test "Phase N.5 mentions ADR prerequisite" $?

# Test 4: Phase includes flagging logic for context-file-changing features
echo "$PHASE_CONTENT" | grep -q "flag\|Flag\|WARNING\|warning"
run_test "Phase N.5 includes flagging mechanism" $?

# Test 5: Phase lists affected context files pattern
echo "$PHASE_CONTENT" | grep -q "source-tree.md\|dependencies.md\|coding-standards.md"
run_test "Phase N.5 lists multiple context files" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
