#!/bin/bash
# Test: AC#4 - DH-03 Triggers on Anti-Pattern Count
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

echo "=== AC#4: DH-03 Triggers on Anti-Pattern Count ==="
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

echo "Checking DH-03 has security-auditor as target agent..."
grep -q "security-auditor" "$TARGET_FILE"
run_test "DH-03 references security-auditor as target agent" $?

echo "Checking DH-03 threshold documents >5 headings..."
grep -qE ">5|> 5|more than 5|5 headings|threshold.*5|5.*heading" "$TARGET_FILE"
run_test "DH-03 documents threshold of greater than 5 headings" $?

echo "Checking DH-03 sources include anti-patterns.md..."
grep -q "anti-patterns.md" "$TARGET_FILE"
run_test "DH-03 sources include anti-patterns.md" $?

echo "Checking DH-03 sources include architecture-constraints.md..."
grep -q "architecture-constraints.md" "$TARGET_FILE"
run_test "DH-03 sources include architecture-constraints.md" $?

echo "Checking DH-03 sources include coding-standards.md..."
grep -q "coding-standards.md" "$TARGET_FILE"
run_test "DH-03 sources include coding-standards.md" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
