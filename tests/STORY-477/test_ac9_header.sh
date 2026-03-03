#!/bin/bash
# Test: AC#9 - Auto-Generation Header in Template
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

echo "=== AC#9: Auto-Generation Header in Template ==="
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

echo "Checking template contains DO NOT EDIT MANUALLY marker..."
grep -q "DO NOT EDIT MANUALLY" "$TARGET_FILE"
run_test "Template contains 'DO NOT EDIT MANUALLY' header marker" $?

echo "Checking template references /audit-alignment --generate-refs command..."
grep -q "/audit-alignment" "$TARGET_FILE"
run_test "Template references /audit-alignment command for regeneration" $?

echo "Checking template references --generate-refs flag..."
grep -q "\-\-generate-refs" "$TARGET_FILE"
run_test "Template references --generate-refs flag" $?

echo "Checking template documents source files list in header..."
grep -qE "Source Files|source files|Generated from" "$TARGET_FILE"
run_test "Template documents source files list in auto-generation header" $?

echo "Checking template documents generation date field..."
grep -qE "Generation Date|Generated:|Generated on|generation.date" "$TARGET_FILE"
run_test "Template documents generation date in auto-generation header" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
