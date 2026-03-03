#!/bin/bash
# Test: AC#3 - Non-Blocking Warning Output
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

echo "=== AC#3: Non-Blocking Warning Output ==="
echo "Target: $TARGET_FILE"
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    exit 1
fi

# Extract Phase N.5 section content
PHASE_CONTENT=$(sed -n '/Constitutional Compliance/,/^### /p' "$TARGET_FILE" 2>/dev/null)

# === Act & Assert ===

# Test 1: Phase specifies non-blocking behavior (warning, not halt)
echo "$PHASE_CONTENT" | grep -qi "non-blocking\|warning.*not.*block\|does not halt\|continue.*workflow"
run_test "Phase N.5 specifies non-blocking warning behavior" $?

# Test 2: Phase includes summary/display output format
echo "$PHASE_CONTENT" | grep -qi "summary\|display\|output.*format\|report"
run_test "Phase N.5 includes summary output specification" $?

# Test 3: Phase mentions ADR topic in warning output
echo "$PHASE_CONTENT" | grep -qi "ADR topic\|required ADR\|ADR.*needed"
run_test "Phase N.5 warning includes ADR topic reference" $?

# Test 4: Phase explicitly states workflow continues after warnings
echo "$PHASE_CONTENT" | grep -qi "proceed\|continue\|workflow.*continues\|not.*halt\|non-blocking"
run_test "Phase N.5 confirms workflow continues after warnings" $?

# Test 5: Phase includes example or template for warning format
echo "$PHASE_CONTENT" | grep -qi "example\|template\|format.*warning\|WARNING:"
run_test "Phase N.5 includes warning format example" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
