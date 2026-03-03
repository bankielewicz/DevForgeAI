#!/bin/bash
# Test: AC#1 - Phase N.5 Step Added to Discovering-Requirements Skill
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

echo "=== AC#1: Phase N.5 Step Exists in SKILL.md ==="
echo "Target: $TARGET_FILE"
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: Phase N.5 or Phase 2.5 section header exists
grep -q "Phase.*[0-9]\.5.*Constitutional Compliance" "$TARGET_FILE"
run_test "Phase N.5 Constitutional Compliance section exists" $?

# Test 2: Phase N.5 appears AFTER Phase 2
PHASE2_LINE=$(grep -n "### Phase 2:" "$TARGET_FILE" | head -1 | cut -d: -f1)
PHASE_N5_LINE=$(grep -n "Constitutional Compliance" "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$PHASE2_LINE" ] && [ -n "$PHASE_N5_LINE" ] && [ "$PHASE_N5_LINE" -gt "$PHASE2_LINE" ]; then
    run_test "Phase N.5 positioned after Phase 2" 0
else
    run_test "Phase N.5 positioned after Phase 2" 1
fi

# Test 3: Phase N.5 appears BEFORE Phase 3
PHASE3_LINE=$(grep -n "### Phase 3:" "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$PHASE3_LINE" ] && [ -n "$PHASE_N5_LINE" ] && [ "$PHASE_N5_LINE" -lt "$PHASE3_LINE" ]; then
    run_test "Phase N.5 positioned before Phase 3" 0
else
    run_test "Phase N.5 positioned before Phase 3" 1
fi

# Test 4: Phase contains reference to context file immutability
grep -q "immutab" "$TARGET_FILE" 2>/dev/null
IMMUTABLE_IN_CONTEXT=$?
grep -A 20 "Constitutional Compliance" "$TARGET_FILE" 2>/dev/null | grep -q "immutab"
run_test "Phase N.5 references immutability rules" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
