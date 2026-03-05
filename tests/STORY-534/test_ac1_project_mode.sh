#!/bin/bash
# Test: AC#1 - Project-Anchored Mode Detection
# Story: STORY-534
# Generated: 2026-03-04
#
# Verifies the command file contains project-anchored mode detection logic:
# - Detects devforgeai/specs/context/ directory
# - Reads context files when present
# - Labels this as project-anchored mode

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

echo "=== AC#1: Project-Anchored Mode Detection ==="
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo ""
    echo "Results: 0 passed, 1 failed (file missing - expected in RED phase)"
    exit 1
fi

# === Act & Assert ===

# Test 1: Command references devforgeai/specs/context/ directory for detection
grep -qiE "devforgeai/specs/context" "$TARGET_FILE"
run_test "References devforgeai/specs/context/ directory" $?

# Test 2: Command includes Glob or directory detection for context path
grep -qiE "(Glob|directory|exists|detect).*context" "$TARGET_FILE"
run_test "Contains context directory detection logic" $?

# Test 3: Command reads context files (tech-stack, source-tree, etc.)
grep -qiE "Read.*tech-stack|Read.*source-tree|Read.*context/" "$TARGET_FILE"
run_test "Reads context files when detected" $?

# Test 4: Command labels this as project-anchored mode
grep -qiE "project.anchored|project.mode|anchored.mode" "$TARGET_FILE"
run_test "Labels project-anchored mode" $?

# Test 5: Command reads at least 3 context files
count=$(grep -ciE "Read.*devforgeai/specs/context/" "$TARGET_FILE" 2>/dev/null || echo "0")
[ "$count" -ge 3 ]
run_test "Reads at least 3 context files (found: $count)" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
