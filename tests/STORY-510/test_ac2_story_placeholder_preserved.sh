#!/bin/bash
# Test: AC#2 - STORY-NNN Placeholders Left Intact
# Story: STORY-510
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/designing-systems/references/artifact-generation.md"

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

echo "=== AC#2: STORY-NNN Placeholders Left Intact ==="
echo ""

# Verify target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file not found: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# Test 1: Step explicitly mentions STORY-NNN should be left as-is
grep -qi "STORY-NNN.*left\|STORY-NNN.*as-is\|STORY-NNN.*preserv\|leave.*STORY-NNN\|do not.*replace.*STORY" "$TARGET_FILE"
run_test "Step explicitly states STORY-NNN placeholders left as-is" $?

# Test 2: Rationale provided - stories not yet created at epic time
grep -qi "stories.*not.*created\|not.*created.*at.*epic\|stories.*do not exist" "$TARGET_FILE"
run_test "Rationale provided: stories not yet created at epic time" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
