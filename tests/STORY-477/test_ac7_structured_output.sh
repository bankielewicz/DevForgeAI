#!/bin/bash
# Test: AC#7 - Structured Output with Triggered Heuristics
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

echo "=== AC#7: Structured Output with Triggered Heuristics ==="
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

echo "Checking output format documents heuristic ID field..."
grep -qE "heuristic.id|heuristic_id|Heuristic ID|triggered.heuristic" "$TARGET_FILE"
run_test "Output format documents heuristic ID field" $?

echo "Checking output format documents target agent field..."
grep -qE "target.agent|target_agent|Target Agent|agent:" "$TARGET_FILE"
run_test "Output format documents target agent field" $?

echo "Checking output format documents output file path field..."
grep -qE "output.file|output_file|Output File|output.path|output_path" "$TARGET_FILE"
run_test "Output format documents output file path field" $?

echo "Checking output format documents source files field..."
grep -qE "source.files|source_files|Source Files|sources:" "$TARGET_FILE"
run_test "Output format documents source files field" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
