#!/bin/bash
# Test: AC#1 - resume-dev.md command line and block reduction
# Story: STORY-459
# Generated: 2026-02-20
# Phase: TDD Red (tests MUST fail before implementation)
#
# Validates:
# - resume-dev.md contains <=120 lines
# - resume-dev.md contains <=3 code blocks (``` pairs)
# - resume-dev.md contains <=12K characters
# - Zero forbidden patterns: devforgeai-validate, Task(subagent_type="tech-stack-detector",
#   Grep(pattern=, checkpoint reading code

set -uo pipefail

# === Test Configuration ===
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TARGET_FILE="${PROJECT_ROOT}/src/claude/commands/resume-dev.md"
PASSED=0
FAILED=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=========================================="
echo "  AC#1: resume-dev.md Command Lean Tests"
echo "  Story: STORY-459"
echo "=========================================="
echo ""

# --- Pre-condition: File exists ---
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FATAL: Target file not found: $TARGET_FILE"
    exit 1
fi

# === Test 1: Line count <=120 ===
LINE_COUNT=$(wc -l < "$TARGET_FILE")
echo "  [INFO] resume-dev.md line count: $LINE_COUNT"
test "$LINE_COUNT" -le 120
run_test "resume-dev.md has <=120 lines (actual: $LINE_COUNT)" $?

# === Test 2: Code block count <=3 (count ``` opening markers) ===
# Count lines that start with ``` (code fence markers), divide by 2 for pairs
FENCE_COUNT=$(grep -c '^```' "$TARGET_FILE" || true)
BLOCK_COUNT=$((FENCE_COUNT / 2))
echo "  [INFO] Code block count: $BLOCK_COUNT (fence markers: $FENCE_COUNT)"
test "$BLOCK_COUNT" -le 3
run_test "resume-dev.md has <=3 code blocks (actual: $BLOCK_COUNT)" $?

# === Test 3: Character count <=12K (12288 bytes) ===
CHAR_COUNT=$(wc -c < "$TARGET_FILE")
echo "  [INFO] Character count: $CHAR_COUNT"
test "$CHAR_COUNT" -le 12288
run_test "resume-dev.md has <=12K characters (actual: $CHAR_COUNT)" $?

# === Test 4: Zero forbidden pattern - devforgeai-validate ===
FORBIDDEN_1=$(grep -c 'devforgeai-validate' "$TARGET_FILE" || true)
test "$FORBIDDEN_1" -eq 0
run_test "Zero instances of 'devforgeai-validate' in resume-dev.md (found: $FORBIDDEN_1)" $?

# === Test 5: Zero forbidden pattern - Task(subagent_type="tech-stack-detector" ===
FORBIDDEN_2=$(grep -c 'Task(subagent_type="tech-stack-detector"' "$TARGET_FILE" || true)
test "$FORBIDDEN_2" -eq 0
run_test "Zero instances of Task(subagent_type=\"tech-stack-detector\") (found: $FORBIDDEN_2)" $?

# === Test 6: Zero forbidden pattern - Grep(pattern= ===
FORBIDDEN_3=$(grep -c 'Grep(pattern=' "$TARGET_FILE" || true)
test "$FORBIDDEN_3" -eq 0
run_test "Zero instances of 'Grep(pattern=' in resume-dev.md (found: $FORBIDDEN_3)" $?

# === Test 7: Zero forbidden pattern - checkpoint reading code ===
# Checkpoint reading code uses CHECKPOINT_FOUND or read_checkpoint patterns
FORBIDDEN_4=$(grep -c -E '(CHECKPOINT_FOUND|read_checkpoint|checkpoint.*Read\()' "$TARGET_FILE" || true)
test "$FORBIDDEN_4" -eq 0
run_test "Zero instances of checkpoint reading code (found: $FORBIDDEN_4)" $?

# === Summary ===
echo ""
echo "=========================================="
echo "  Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "=========================================="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
