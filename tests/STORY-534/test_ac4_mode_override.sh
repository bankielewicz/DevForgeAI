#!/bin/bash
# Test: AC#4 - Explicit Mode Override
# Story: STORY-534
# Generated: 2026-03-04
#
# Verifies the command supports --standalone flag to override auto-detection:
# - Parses --standalone flag from arguments
# - Flag forces standalone mode even when context exists
# - Documents override behavior

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/business-plan.md"

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

echo "=== AC#4: Explicit Mode Override ==="
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo ""
    echo "Results: 0 passed, 1 failed (file missing - expected in RED phase)"
    exit 1
fi

# === Act & Assert ===

# Test 1: Command references --standalone flag
grep -qE "\-\-standalone" "$TARGET_FILE"
run_test "References --standalone flag" $?

# Test 2: Command parses ARGUMENTS or arguments for flag
grep -qiE "ARGUMENTS|arguments.*standalone|\\\$ARGUMENTS" "$TARGET_FILE"
run_test "Parses command arguments for flag" $?

# Test 3: Flag overrides auto-detection
grep -qiE "override.*detect|force.*standalone|skip.*detect|ignore.*context" "$TARGET_FILE"
run_test "Flag overrides auto-detection logic" $?

# Test 4: Documents flag behavior for users
grep -qiE "flag|usage.*standalone|argument.*hint" "$TARGET_FILE"
run_test "Documents flag behavior" $?

# Test 5: YAML frontmatter includes argument-hint for --standalone
grep -qiE "argument.hint.*standalone|standalone.*flag" "$TARGET_FILE"
run_test "Argument hint includes --standalone" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
