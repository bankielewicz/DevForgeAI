#!/bin/bash
# Test: AC#5 - Agent File Fits Within 500-Line Size Limit
# Story: STORY-393
# Generated: 2026-02-12
# Target: src/claude/agents/requirements-analyst.md

set -uo pipefail

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/agents/requirements-analyst.md"
REF_DIR="/mnt/c/Projects/DevForgeAI2/src/claude/agents/requirements-analyst/references"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#5: Size Limit ==="
echo ""

if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# === Test 1: File has at least 100 lines ===
LINE_COUNT=$(wc -l < "$TARGET_FILE")
[ "$LINE_COUNT" -ge 100 ] && run_test "File has at least 100 lines (actual=$LINE_COUNT)" 0 || run_test "File has at least 100 lines (actual=$LINE_COUNT)" 1

# === Test 2: File has at most 500 lines ===
[ "$LINE_COUNT" -le 500 ] && run_test "File has at most 500 lines (actual=$LINE_COUNT)" 0 || run_test "File has at most 500 lines (actual=$LINE_COUNT)" 1

# === Test 3: If > 400 lines, references/ directory exists ===
if [ "$LINE_COUNT" -gt 400 ]; then
    [ -d "$REF_DIR" ] && run_test "References directory exists (file > 400 lines)" 0 || run_test "References directory exists (file > 400 lines)" 1
else
    echo "  SKIP: File <= 400 lines, reference extraction check not required"
    run_test "File <= 400 lines, no reference extraction required" 0
fi

# === Test 4: If references/ exists, it contains at least one .md file ===
if [ -d "$REF_DIR" ]; then
    REF_COUNT=$(find "$REF_DIR" -name "*.md" | wc -l)
    [ "$REF_COUNT" -ge 1 ] && run_test "References directory contains at least 1 .md file (count=$REF_COUNT)" 0 || run_test "References directory contains at least 1 .md file (count=$REF_COUNT)" 1
else
    if [ "$LINE_COUNT" -le 400 ]; then
        run_test "No references needed (file <= 400 lines)" 0
    else
        run_test "References directory should exist for file > 400 lines" 1
    fi
fi

# === Test 5: Token budget estimate (< 20K tokens for core file) ===
CHAR_COUNT=$(wc -c < "$TARGET_FILE")
TOKEN_ESTIMATE=$((CHAR_COUNT / 4))
[ "$TOKEN_ESTIMATE" -lt 20000 ] && run_test "Core file token estimate < 20K (estimate=$TOKEN_ESTIMATE)" 0 || run_test "Core file token estimate < 20K (estimate=$TOKEN_ESTIMATE)" 1

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
