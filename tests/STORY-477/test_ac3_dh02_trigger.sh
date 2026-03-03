#!/bin/bash
# Test: AC#3 - DH-02 Triggers on Multi-Language/Build-System
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

echo "=== AC#3: DH-02 Triggers on Multi-Language/Build-System ==="
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

echo "Checking DH-02 has test-automator as target agent..."
grep -q "test-automator" "$TARGET_FILE"
run_test "DH-02 references test-automator as target agent" $?

echo "Checking DH-02 sources include tech-stack.md..."
grep -q "tech-stack.md" "$TARGET_FILE"
run_test "DH-02 sources include tech-stack.md" $?

echo "Checking DH-02 sources include source-tree.md..."
grep -q "source-tree.md" "$TARGET_FILE"
run_test "DH-02 sources include source-tree.md" $?

echo "Checking DH-02 sources include coding-standards.md..."
grep -q "coding-standards.md" "$TARGET_FILE"
run_test "DH-02 sources include coding-standards.md" $?

echo "Checking DH-02 mentions multi-language or build-system trigger context..."
grep -qiE "multi-language|build.system|Multi-Language|Build-System" "$TARGET_FILE"
run_test "DH-02 documents multi-language or build-system trigger condition" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
