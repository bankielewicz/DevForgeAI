#!/bin/bash
# Test: AC#5 - Heuristic Analysis Runs Only on Mismatch
# Story: STORY-503
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references/test-tampering-heuristics.md"

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

echo "=== AC#5: Conditional Invocation ==="

# === Test 1: Contains integration_protocol section ===
grep -q -i "integration.protocol" "$TARGET_FILE" 2>/dev/null
run_test "Contains integration_protocol section" $?

# === Test 2: Documents conditional invocation on mismatched_files ===
grep -q -i "mismatched.files" "$TARGET_FILE" 2>/dev/null
run_test "Documents analysis only when mismatched_files is non-empty" $?

# === Test 3: Documents zero overhead when no mismatches ===
grep -q -i "zero.*overhead\|not.*invoked\|skip.*heuristic" "$TARGET_FILE" 2>/dev/null
run_test "Documents zero overhead when no mismatches" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
