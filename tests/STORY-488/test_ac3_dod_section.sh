#!/bin/bash
# Test: AC#3 - Dual-Path Sync DoD Section Auto-Added
# Story: STORY-488
# Generated: 2026-02-23

# === Test Configuration ===
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

# === Arrange ===
TARGET_FILE="src/claude/skills/devforgeai-story-creation/references/technical-specification-creation.md"
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TARGET_PATH="${PROJECT_ROOT}/${TARGET_FILE}"

echo "=== AC#3: Dual-Path Sync DoD Section Auto-Added ==="
echo "Target: ${TARGET_FILE}"
echo ""

# === Act & Assert ===

# Test 1: Verify DoD subsection template with "Dual-Path Sync" exists
grep -q "Dual-Path Sync" "$TARGET_PATH"
run_test "Dual-Path Sync DoD subsection template exists" $?

# Test 2: Verify DoD template has checkbox for src/claude/ files
grep -q 'src/claude/' "$TARGET_PATH" && grep -q '\- \[ \]' "$TARGET_PATH"
run_test "DoD template has checkbox for src/claude/ file operations" $?

# Test 3: Verify DoD template has checkbox for .claude/ sync
grep -q 'synced to \.claude/' "$TARGET_PATH" || grep -q 'sync.*\.claude/' "$TARGET_PATH"
run_test "DoD template has checkbox for .claude/ sync operations" $?

# Test 4: Verify DoD template has checkbox for tests against src/ tree
grep -q 'Tests run against src/' "$TARGET_PATH" || grep -q 'test.*against.*src/' "$TARGET_PATH"
run_test "DoD template has checkbox for tests against src/ tree" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
