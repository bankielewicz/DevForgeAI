#!/bin/bash
# Test: AC#11 - Derivation Purity
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

echo "=== AC#11: Derivation Purity ==="
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

echo "Checking file states 100% context-derived content..."
grep -qE "100%|100 percent|purely derived|context-derived|derived from context" "$TARGET_FILE"
run_test "File documents 100% context-derived content requirement" $?

echo "Checking file explicitly prohibits hardcoded content..."
grep -qiE "no hardcoded|not hardcoded|no hard.coded|prohibit.*hardcode|hardcode.*forbidden" "$TARGET_FILE"
run_test "File prohibits hardcoded content in generated references" $?

echo "Checking file documents purity constraint (derivation from context files only)..."
grep -qiE "derivation purity|pure derivation|context files only|only.*context.files|derived.*context" "$TARGET_FILE"
run_test "File documents derivation purity constraint" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
