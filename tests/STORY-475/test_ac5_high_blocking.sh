#!/bin/bash
# Test: AC#5 - HIGH Contradictions Block Phase 6
# Story: STORY-475
# Phase: Red (tests should FAIL before implementation)

PASS=0
FAIL=0
FILE="src/claude/skills/designing-systems/references/prompt-alignment-workflow.md"

# Test 1: File contains HIGH contradiction blocking logic
if grep -qiE "HIGH.*block|block.*HIGH|HIGH.*contradiction" "$FILE" 2>/dev/null; then
  echo "PASS: File contains HIGH contradiction blocking logic"
  ((PASS++))
else
  echo "FAIL: File does NOT contain HIGH contradiction blocking logic"
  ((FAIL++))
fi

# Test 2: File contains AskUserQuestion for presenting contradictions
if grep -q "AskUserQuestion" "$FILE" 2>/dev/null; then
  echo "PASS: File contains AskUserQuestion for contradictions"
  ((PASS++))
else
  echo "FAIL: File does NOT contain AskUserQuestion for contradictions"
  ((FAIL++))
fi

# Test 3: File contains Phase 6 blocking condition
if grep -qiE "Phase 6.*block|block.*Phase 6" "$FILE" 2>/dev/null; then
  echo "PASS: File contains Phase 6 blocking condition"
  ((PASS++))
else
  echo "FAIL: File does NOT contain Phase 6 blocking condition"
  ((FAIL++))
fi

# Test 4: File contains MEDIUM/LOW deferral handling
if grep -qiE "MEDIUM|LOW" "$FILE" 2>/dev/null; then
  echo "PASS: File contains MEDIUM/LOW severity handling"
  ((PASS++))
else
  echo "FAIL: File does NOT contain MEDIUM/LOW severity handling"
  ((FAIL++))
fi

# Test 5: File references resolution options (Apply fix / Skip / Edit manually or similar)
if grep -qiE "(Apply fix|Skip|Edit manually|resolution option|override)" "$FILE" 2>/dev/null; then
  echo "PASS: File contains contradiction resolution options"
  ((PASS++))
else
  echo "FAIL: File does NOT contain contradiction resolution options"
  ((FAIL++))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ $FAIL -gt 0 ]; then
  exit 1
fi
