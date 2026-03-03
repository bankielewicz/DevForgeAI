#!/bin/bash
# Test: AC#1 - Four Detection Heuristics Implemented
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

echo "=== AC#1: Four Detection Heuristics Implemented ==="
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

echo "Checking DH-01 is defined..."
grep -q "DH-01" "$TARGET_FILE"
run_test "DH-01 heuristic identifier defined in file" $?

echo "Checking DH-02 is defined..."
grep -q "DH-02" "$TARGET_FILE"
run_test "DH-02 heuristic identifier defined in file" $?

echo "Checking DH-03 is defined..."
grep -q "DH-03" "$TARGET_FILE"
run_test "DH-03 heuristic identifier defined in file" $?

echo "Checking DH-04 is defined..."
grep -q "DH-04" "$TARGET_FILE"
run_test "DH-04 heuristic identifier defined in file" $?

echo "Checking all four heuristics appear (count >= 4)..."
COUNT=$(grep -c "DH-0[1-4]" "$TARGET_FILE" 2>/dev/null || echo 0)
[ "$COUNT" -ge 4 ]
run_test "At least four DH-0N heuristic identifiers present" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
