#!/bin/bash
# Test: AC#2 - dual_path_sync Block Auto-Generated
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

echo "=== AC#2: dual_path_sync Block Auto-Generated ==="
echo "Target: ${TARGET_FILE}"
echo ""

# === Act & Assert ===

# Test 1: Verify dual_path_sync YAML template/example exists
grep -q "dual_path_sync" "$TARGET_PATH"
run_test "dual_path_sync YAML template exists in target file" $?

# Test 2: Verify template includes source_paths key
grep -q "source_paths" "$TARGET_PATH"
run_test "dual_path_sync template includes source_paths key" $?

# Test 3: Verify template includes operational_paths key
grep -q "operational_paths" "$TARGET_PATH"
run_test "dual_path_sync template includes operational_paths key" $?

# Test 4: Verify template includes test_against key
grep -q "test_against" "$TARGET_PATH"
run_test "dual_path_sync template includes test_against key" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
