#!/bin/bash
# Test: AC#1 - File existence verification step using Glob
# Story: STORY-514
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/implementing-stories/phases/phase-02-test-first.md"

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

echo "=== AC#1: File Existence Verification Step ==="

# === Test 1: Glob pattern for snapshot file exists in target ===
grep -q 'Glob.*red-phase-checksums\.json' "$TARGET_FILE"
run_test "Glob command checking for red-phase-checksums.json exists" $?

# === Test 2: Glob references the correct snapshot path ===
grep -q 'devforgeai/qa/snapshots/.*red-phase-checksums\.json' "$TARGET_FILE"
run_test "Glob references correct snapshot path with STORY_ID variable" $?

# === Test 3: HALT instruction exists if file not found ===
grep -q 'HALT.*Snapshot file not created' "$TARGET_FILE"
run_test "HALT instruction present when snapshot file not found" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
