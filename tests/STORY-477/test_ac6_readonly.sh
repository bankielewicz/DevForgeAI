#!/bin/bash
# Test: AC#6 - Heuristics Are Read-Only
# Story: STORY-477
# Generated: 2026-02-23
# Module Under Test: src/claude/skills/designing-systems/references/domain-reference-generation.md

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/designing-systems/references/domain-reference-generation.md"

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

echo "=== AC#6: Heuristics Are Read-Only ==="
echo "Target: $TARGET_FILE"
echo ""

# === Pre-condition: File must exist ===
echo "Checking file exists..."
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo ""
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# === Act & Assert ===

echo "Checking file documents Read-only constraint..."
grep -qE "Read-only|read-only|Read only|read only" "$TARGET_FILE"
run_test "File documents read-only constraint for heuristics" $?

echo "Checking file references Read() tool as allowed operation..."
grep -q "Read()" "$TARGET_FILE"
run_test "File references Read() as permitted tool operation" $?

echo "Checking file references Grep as allowed operation..."
grep -q "Grep" "$TARGET_FILE"
run_test "File references Grep as permitted tool operation" $?

echo "Checking file documents no Write operations for heuristics..."
grep -qiE "no Write|Read.*Grep.*only|only.*Read.*Grep|Read and Grep only" "$TARGET_FILE"
run_test "File documents that only Read and Grep operations are permitted" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
