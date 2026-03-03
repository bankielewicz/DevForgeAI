#!/bin/bash
# Test AC#1: Hardcoded WSL Absolute Path Replaced with Relative Path
# STORY-452 - Portability Fix
#
# Verifies:
# 1. No occurrence of /mnt/c/Projects/DevForgeAI2 in user-input-guidance.md
# 2. Relative path .claude/skills/discovering-requirements/references/user-input-guidance.md present

set -euo pipefail

TARGET_FILE="src/claude/skills/discovering-requirements/references/user-input-guidance.md"
HARDCODED_PATH="/mnt/c/Projects/DevForgeAI2"
RELATIVE_PATH='.claude/skills/discovering-requirements/references/user-input-guidance.md'

PASS=0
FAIL=0

# Test 1: No hardcoded absolute path
echo "Test 1: No hardcoded absolute path in file"
if grep -q "$HARDCODED_PATH" "$TARGET_FILE"; then
    echo "  FAIL: Found hardcoded path '$HARDCODED_PATH' in $TARGET_FILE"
    FAIL=$((FAIL + 1))
else
    echo "  PASS: No hardcoded absolute path found"
    PASS=$((PASS + 1))
fi

# Test 2: Relative path present in Integration Instructions
echo "Test 2: Relative path present in Integration Instructions block"
if grep -q "Read(file_path=\"$RELATIVE_PATH\")" "$TARGET_FILE"; then
    echo "  PASS: Relative path found"
    PASS=$((PASS + 1))
else
    echo "  FAIL: Relative path not found in file"
    FAIL=$((FAIL + 1))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
    echo "OVERALL: FAIL"
    exit 1
else
    echo "OVERALL: PASS"
    exit 0
fi
