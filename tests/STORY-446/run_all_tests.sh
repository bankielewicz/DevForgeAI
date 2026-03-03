#!/bin/bash
# Run all STORY-446 tests
# Story: STORY-446 - Fix YAML Frontmatter Compliance
# Generated: 2026-02-18

DIR="$(cd "$(dirname "$0")" && pwd)"
TOTAL_PASS=0
TOTAL_FAIL=0

echo "============================================"
echo "  STORY-446: Fix YAML Frontmatter Compliance"
echo "============================================"
echo ""

for test_file in "$DIR"/test-ac*.sh; do
    echo "--- Running: $(basename "$test_file") ---"
    bash "$test_file"
    if [ $? -ne 0 ]; then
        ((TOTAL_FAIL++))
    else
        ((TOTAL_PASS++))
    fi
    echo ""
done

echo "============================================"
echo "  Summary: $TOTAL_PASS test files passed, $TOTAL_FAIL test files failed"
echo "============================================"
[ $TOTAL_FAIL -eq 0 ] && exit 0 || exit 1
