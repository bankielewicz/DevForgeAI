#!/bin/bash
# Test: AC#5 - DH-04 Triggers on Multi-Language Coding Standards
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

echo "=== AC#5: DH-04 Triggers on Multi-Language Coding Standards ==="
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

echo "Checking DH-04 has code-reviewer as target agent..."
grep -q "code-reviewer" "$TARGET_FILE"
run_test "DH-04 references code-reviewer as target agent" $?

echo "Checking DH-04 documents 2+ languages trigger condition..."
grep -qE "2\+|2 or more|two or more|multiple languages|2\+ languages" "$TARGET_FILE"
run_test "DH-04 documents trigger condition of 2+ languages" $?

echo "Checking DH-04 sources include anti-patterns.md..."
grep -q "anti-patterns.md" "$TARGET_FILE"
run_test "DH-04 sources include anti-patterns.md" $?

echo "Checking DH-04 sources include coding-standards.md..."
grep -q "coding-standards.md" "$TARGET_FILE"
run_test "DH-04 sources include coding-standards.md" $?

echo "Checking DH-04 sources include dependencies.md..."
grep -q "dependencies.md" "$TARGET_FILE"
run_test "DH-04 sources include dependencies.md" $?

echo "Checking DH-04 sources include architecture-constraints.md..."
grep -q "architecture-constraints.md" "$TARGET_FILE"
run_test "DH-04 sources include architecture-constraints.md" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
