#!/bin/bash
# Test: AC#4 - Exempt Paths Not Translated
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

echo "=== AC#4: Exempt Paths Not Translated ==="
echo "Target: ${TARGET_FILE}"
echo ""

# === Act & Assert ===

# Test 1: Verify exempt_prefixes or exempt paths list exists
grep -qi "exempt" "$TARGET_PATH"
run_test "Exempt paths list exists in target file" $?

# Test 2: Verify devforgeai/specs is listed as exempt
grep -q "devforgeai/specs" "$TARGET_PATH" && grep -qi "exempt" "$TARGET_PATH"
run_test "devforgeai/specs listed as exempt path" $?

# Test 3: Verify CLAUDE.md is listed as exempt
grep -q "CLAUDE.md" "$TARGET_PATH" && grep -qi "exempt" "$TARGET_PATH"
run_test "CLAUDE.md listed as exempt path" $?

# Test 4: Verify README.md is listed as exempt
grep -q "README.md" "$TARGET_PATH" && grep -qi "exempt" "$TARGET_PATH"
run_test "README.md listed as exempt path" $?

# Test 5: Verify tests/ is listed as exempt
grep -q "tests/" "$TARGET_PATH" && grep -qi "exempt" "$TARGET_PATH"
run_test "tests/ listed as exempt path" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
