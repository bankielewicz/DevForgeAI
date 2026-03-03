#!/bin/bash
# Test: AC#1 - create-sprint.md reduced to lean orchestration pattern
# Story: STORY-458
# Generated: 2026-02-20
# Expected: FAIL (TDD Red phase - refactoring not yet done)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

TARGET_FILE="${PROJECT_ROOT}/src/claude/commands/create-sprint.md"

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

echo "=============================================="
echo "  AC#1: create-sprint.md Lean Orchestration"
echo "  Story: STORY-458"
echo "=============================================="
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FATAL: Target file not found: $TARGET_FILE"
    echo ""
    echo "Results: 0 passed, 5 failed out of 5 tests"
    exit 1
fi

# === Test 1: Line count <=100 ===
LINE_COUNT=$(wc -l < "$TARGET_FILE")
test_result=0
if [ "$LINE_COUNT" -le 100 ]; then
    test_result=0
else
    test_result=1
fi
run_test "Line count <= 100 (actual: ${LINE_COUNT})" "$test_result"

# === Test 2: Character count <=12000 ===
CHAR_COUNT=$(wc -c < "$TARGET_FILE")
test_result=0
if [ "$CHAR_COUNT" -le 12000 ]; then
    test_result=0
else
    test_result=1
fi
run_test "Character count <= 12000 (actual: ${CHAR_COUNT})" "$test_result"

# === Test 3: Code blocks <=3 before Skill() invocation ===
# Count ``` occurrences that appear BEFORE the first Skill(command= line
SKILL_LINE=$(grep -n 'Skill(command=' "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -z "$SKILL_LINE" ]; then
    # No Skill() invocation found at all - count all code blocks
    BLOCKS_BEFORE_SKILL=$(grep -c '```' "$TARGET_FILE" || true)
    # Divide by 2 since each code block has opening and closing ```
    BLOCKS_BEFORE_SKILL=$(( BLOCKS_BEFORE_SKILL / 2 ))
    run_test "Code blocks <= 3 before Skill() (no Skill() found, ${BLOCKS_BEFORE_SKILL} total blocks)" 1
else
    BLOCKS_BEFORE_SKILL=$(head -n "$((SKILL_LINE - 1))" "$TARGET_FILE" | grep -c '```' || true)
    # Divide by 2 since each code block has opening and closing ```
    BLOCKS_BEFORE_SKILL=$(( BLOCKS_BEFORE_SKILL / 2 ))
    test_result=0
    if [ "$BLOCKS_BEFORE_SKILL" -le 3 ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "Code blocks <= 3 before Skill() (actual: ${BLOCKS_BEFORE_SKILL})" "$test_result"
fi

# === Test 4: Contains exactly 1 Skill() invocation ===
SKILL_COUNT=$(grep -c 'Skill(command=' "$TARGET_FILE" || true)
test_result=0
if [ "$SKILL_COUNT" -eq 1 ]; then
    test_result=0
else
    test_result=1
fi
run_test "Contains exactly 1 Skill() invocation (actual: ${SKILL_COUNT})" "$test_result"

# === Test 5: Contains DO NOT guardrail section ===
test_result=0
if grep -q 'DO NOT' "$TARGET_FILE"; then
    test_result=0
else
    test_result=1
fi
run_test "Contains DO NOT guardrail section" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
