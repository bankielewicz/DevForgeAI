#!/bin/bash
# Test: AC#2 - gap_type field present in observation output schema
# Story: STORY-483
# Generated: 2026-02-23
# TDD Phase: RED (tests must FAIL before implementation)

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/agents/integration-tester.md"

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

echo "=== AC#2: Observation Output Schema Contains gap_type Field ==="
echo "Target: $TARGET_FILE"
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "ERROR: Target file not found: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: gap_type field present in the file
grep -q "gap_type" "$TARGET_FILE"
run_test "Field 'gap_type' exists in integration-tester.md" $?

# Test 2: gap_type appears in a schema or output context (near observation or schema keywords)
grep -A 5 "gap_type" "$TARGET_FILE" | grep -q "gap_type"
run_test "gap_type field has surrounding schema context" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
