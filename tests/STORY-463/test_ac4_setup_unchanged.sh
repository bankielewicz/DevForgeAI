#!/bin/bash
# Test: AC#4 - setup-github-actions.md is unchanged (false positive - must not be modified)
# Story: STORY-463
# Generated: 2026-02-21
# TDD Phase: RED (these tests should PASS now - verifying no regression)
# Baseline: 131 lines, checksum 494ad80ed2c95cda17a8a3a55f7164bd

PASSED=0
FAILED=0
TARGET="src/claude/commands/setup-github-actions.md"
BASELINE_CHECKSUM="494ad80ed2c95cda17a8a3a55f7164bd"
BASELINE_LINES=131

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

echo "=== AC#4: setup-github-actions.md Is Unchanged (False Positive Confirmation) ==="
echo "Target: $TARGET"
echo ""

# === Test 1: File exists ===
[ -f "$TARGET" ]
run_test "setup-github-actions.md exists at src/claude/commands/setup-github-actions.md" $?

# === Test 2: File is unchanged (MD5 checksum) ===
if [ -f "$TARGET" ]; then
    ACTUAL_CHECKSUM=$(md5sum "$TARGET" | awk '{print $1}')
    echo "  INFO: Expected checksum = $BASELINE_CHECKSUM"
    echo "  INFO: Actual checksum   = $ACTUAL_CHECKSUM"
    [ "$ACTUAL_CHECKSUM" = "$BASELINE_CHECKSUM" ]
    run_test "File checksum matches baseline (file unchanged)" $?
else
    echo "  SKIP: Checksum check (file missing)"
    ((FAILED++))
fi

# === Test 3: Line count approximately 132 (within 5 lines of 132) ===
if [ -f "$TARGET" ]; then
    LINE_COUNT=$(wc -l < "$TARGET")
    echo "  INFO: Current line count = $LINE_COUNT (expected ~132)"
    # Accept range 127-137 (approximately 132)
    [ "$LINE_COUNT" -ge 127 ] && [ "$LINE_COUNT" -le 137 ]
    run_test "Line count is approximately 132 (actual: $LINE_COUNT, range 127-137)" $?
else
    echo "  SKIP: Line count check (file missing)"
    ((FAILED++))
fi

# === Test 4: No git modifications (verify clean working state for this file) ===
if command -v git &>/dev/null; then
    GIT_STATUS=$(git diff -- "$TARGET" 2>/dev/null)
    [ -z "$GIT_STATUS" ]
    run_test "No uncommitted changes to setup-github-actions.md (git diff clean)" $?
else
    echo "  SKIP: Git diff check (git not available)"
fi

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ $FAILED -eq 0 ] && exit 0 || exit 1
