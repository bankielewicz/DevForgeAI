#!/bin/bash
# Test: AC#1 - .claude/ Paths Auto-Translated to src/claude/
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

echo "=== AC#1: .claude/ Paths Auto-Translated to src/claude/ ==="
echo "Target: ${TARGET_FILE}"
echo ""

# === Act & Assert ===

# Test 1: Verify Dual-Path Translation Rule section exists
grep -q "Dual-Path Translation Rule" "$TARGET_PATH"
run_test "Dual-Path Translation Rule section exists in target file" $?

# Test 2: Verify translation rule describes .claude/ to src/claude/ mapping
grep -q 'src/claude/' "$TARGET_PATH" && grep -q '\.claude/' "$TARGET_PATH" && grep -q 'translat' "$TARGET_PATH"
run_test "Translation rule text mentions .claude/ to src/claude/ translation" $?

# Test 3: Verify auto-translation instruction exists (not just incidental mention)
grep -qi 'auto.*translat\|translat.*auto\|replace.*\.claude/.*src/claude/\|\.claude/.*replaced.*src/claude/' "$TARGET_PATH"
run_test "Auto-translation instruction exists for .claude/ paths" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
