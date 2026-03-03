#!/bin/bash
# Test: AC#12 - project-*.md Naming Convention
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

echo "=== AC#12: project-*.md Naming Convention ==="
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

echo "Checking file documents project-*.md naming convention..."
grep -q "project-" "$TARGET_FILE"
run_test "File documents project- prefix naming convention" $?

echo "Checking file references project-domain.md as naming example..."
grep -q "project-domain.md" "$TARGET_FILE"
run_test "File includes project-domain.md as naming convention example" $?

echo "Checking file references project-testing.md as naming example..."
grep -q "project-testing.md" "$TARGET_FILE"
run_test "File includes project-testing.md as naming convention example" $?

echo "Checking file documents naming pattern with .md extension..."
grep -qE "project-[a-z]+\.md" "$TARGET_FILE"
run_test "File documents project-[domain].md naming pattern with .md extension" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
