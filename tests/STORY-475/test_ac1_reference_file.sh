#!/bin/bash
# Test: AC#1 - Phase 5.5 Reference File Creation
# Story: STORY-475
# Phase: Red (tests should FAIL before implementation)

PASS=0
FAIL=0
FILE="src/claude/skills/designing-systems/references/prompt-alignment-workflow.md"

# Test 1: File exists at correct path
if [ -f "$FILE" ]; then
  echo "PASS: Reference file exists at $FILE"
  ((PASS++))
else
  echo "FAIL: Reference file NOT found at $FILE"
  ((FAIL++))
fi

# Test 2: Title contains "Prompt Alignment"
if grep -q "Prompt Alignment" "$FILE" 2>/dev/null; then
  echo "PASS: Title contains 'Prompt Alignment'"
  ((PASS++))
else
  echo "FAIL: Title does NOT contain 'Prompt Alignment'"
  ((FAIL++))
fi

# Test 3: File is at least 150 lines
LINE_COUNT=$(wc -l < "$FILE" 2>/dev/null || echo 0)
if [ "$LINE_COUNT" -ge 150 ]; then
  echo "PASS: File has $LINE_COUNT lines (>= 150)"
  ((PASS++))
else
  echo "FAIL: File has $LINE_COUNT lines (must be >= 150)"
  ((FAIL++))
fi

# Test 4: File is at most 250 lines
if [ "$LINE_COUNT" -le 250 ]; then
  echo "PASS: File has $LINE_COUNT lines (<= 250)"
  ((PASS++))
else
  echo "FAIL: File has $LINE_COUNT lines (must be <= 250)"
  ((FAIL++))
fi

# Test 5: File follows progressive disclosure pattern (references on-demand loading)
if grep -qiE "(on.demand|progressive disclosure|loaded on demand|load on demand)" "$FILE" 2>/dev/null; then
  echo "PASS: File references progressive disclosure pattern"
  ((PASS++))
else
  echo "FAIL: File does NOT reference progressive disclosure pattern"
  ((FAIL++))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ $FAIL -gt 0 ]; then
  exit 1
fi
