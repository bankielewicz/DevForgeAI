#!/bin/bash
# Test: AC#2 - DH-01 Triggers on Hardware/Platform Keywords
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

echo "=== AC#2: DH-01 Triggers on Hardware/Platform Keywords ==="
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

echo "Checking DH-01 has backend-architect as target agent..."
grep -q "backend-architect" "$TARGET_FILE"
run_test "DH-01 references backend-architect as target agent" $?

echo "Checking DH-01 has GPU keyword..."
grep -q "GPU" "$TARGET_FILE"
run_test "DH-01 includes GPU as hardware keyword" $?

echo "Checking DH-01 has CUDA keyword..."
grep -q "CUDA" "$TARGET_FILE"
run_test "DH-01 includes CUDA as hardware keyword" $?

echo "Checking DH-01 has FPGA keyword..."
grep -q "FPGA" "$TARGET_FILE"
run_test "DH-01 includes FPGA as hardware keyword" $?

echo "Checking DH-01 has embedded keyword..."
grep -q "embedded" "$TARGET_FILE"
run_test "DH-01 includes embedded as hardware keyword" $?

echo "Checking DH-01 sources include architecture-constraints.md..."
grep -q "architecture-constraints.md" "$TARGET_FILE"
run_test "DH-01 sources include architecture-constraints.md" $?

echo "Checking DH-01 sources include anti-patterns.md..."
grep -q "anti-patterns.md" "$TARGET_FILE"
run_test "DH-01 sources include anti-patterns.md" $?

echo "Checking DH-01 sources include coding-standards.md..."
grep -q "coding-standards.md" "$TARGET_FILE"
run_test "DH-01 sources include coding-standards.md" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
