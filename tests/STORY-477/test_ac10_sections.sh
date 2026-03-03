#!/bin/bash
# Test: AC#10 - Template Contains All Required Sections
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

echo "=== AC#10: Template Contains All Required Sections ==="
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

echo "Checking template contains 'When to Load' section..."
grep -q "When to Load" "$TARGET_FILE"
run_test "Template contains 'When to Load' section" $?

echo "Checking template contains 'Domain Constraints' section..."
grep -q "Domain Constraints" "$TARGET_FILE"
run_test "Template contains 'Domain Constraints' section" $?

echo "Checking template contains 'Forbidden Patterns' section..."
grep -q "Forbidden Patterns" "$TARGET_FILE"
run_test "Template contains 'Forbidden Patterns' section" $?

echo "Checking template contains 'Language Patterns' section..."
grep -q "Language Patterns" "$TARGET_FILE"
run_test "Template contains 'Language Patterns' section" $?

echo "Checking template contains 'Build Commands' section..."
grep -q "Build Commands" "$TARGET_FILE"
run_test "Template contains 'Build Commands' section" $?

echo "Verifying all 5 required sections present (count check)..."
SECTION_COUNT=0
grep -q "When to Load" "$TARGET_FILE" && ((SECTION_COUNT++))
grep -q "Domain Constraints" "$TARGET_FILE" && ((SECTION_COUNT++))
grep -q "Forbidden Patterns" "$TARGET_FILE" && ((SECTION_COUNT++))
grep -q "Language Patterns" "$TARGET_FILE" && ((SECTION_COUNT++))
grep -q "Build Commands" "$TARGET_FILE" && ((SECTION_COUNT++))
[ "$SECTION_COUNT" -eq 5 ]
run_test "All 5 required template sections present (count: $SECTION_COUNT/5)" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
