#!/bin/bash
# Test: AC#2 - SKILL.md Phase 5.5 Insertion
# Story: STORY-475
# Phase: Red (tests should FAIL before implementation)

PASS=0
FAIL=0
SKILL_FILE="src/claude/skills/designing-systems/SKILL.md"

# Test 1: SKILL.md contains "Phase 5.5" header
if grep -q "Phase 5\.5" "$SKILL_FILE" 2>/dev/null; then
  echo "PASS: SKILL.md contains 'Phase 5.5'"
  ((PASS++))
else
  echo "FAIL: SKILL.md does NOT contain 'Phase 5.5'"
  ((FAIL++))
fi

# Test 2: Phase 5.5 header contains "Prompt Alignment"
if grep -q "Phase 5\.5.*Prompt Alignment\|Prompt Alignment.*Phase 5\.5" "$SKILL_FILE" 2>/dev/null; then
  echo "PASS: Phase 5.5 section is titled 'Prompt Alignment'"
  ((PASS++))
else
  echo "FAIL: Phase 5.5 section is NOT titled 'Prompt Alignment'"
  ((FAIL++))
fi

# Test 3: Phase 5.5 appears AFTER Phase 5 and BEFORE Phase 6
PHASE5_LINE=$(grep -n "## Phase 5[^\.56]" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)
PHASE55_LINE=$(grep -n "Phase 5\.5" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)
PHASE6_LINE=$(grep -n "## Phase 6" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)

if [ -n "$PHASE5_LINE" ] && [ -n "$PHASE55_LINE" ] && [ -n "$PHASE6_LINE" ]; then
  if [ "$PHASE5_LINE" -lt "$PHASE55_LINE" ] && [ "$PHASE55_LINE" -lt "$PHASE6_LINE" ]; then
    echo "PASS: Phase 5.5 appears after Phase 5 (line $PHASE5_LINE) and before Phase 6 (line $PHASE6_LINE)"
    ((PASS++))
  else
    echo "FAIL: Phase 5.5 (line $PHASE55_LINE) NOT between Phase 5 (line $PHASE5_LINE) and Phase 6 (line $PHASE6_LINE)"
    ((FAIL++))
  fi
else
  echo "FAIL: Could not locate Phase 5 (line $PHASE5_LINE), Phase 5.5 (line $PHASE55_LINE), or Phase 6 (line $PHASE6_LINE)"
  ((FAIL++))
fi

# Test 4: Contains Read() reference loading instruction for prompt-alignment-workflow.md
if grep -q "prompt-alignment-workflow" "$SKILL_FILE" 2>/dev/null; then
  echo "PASS: SKILL.md references prompt-alignment-workflow.md"
  ((PASS++))
else
  echo "FAIL: SKILL.md does NOT reference prompt-alignment-workflow.md"
  ((FAIL++))
fi

# Test 5: Phase 5.5 section is 30-40 lines
if [ -n "$PHASE55_LINE" ] && [ -n "$PHASE6_LINE" ]; then
  SECTION_LINES=$((PHASE6_LINE - PHASE55_LINE))
  if [ "$SECTION_LINES" -ge 30 ] && [ "$SECTION_LINES" -le 40 ]; then
    echo "PASS: Phase 5.5 section is $SECTION_LINES lines (30-40 required)"
    ((PASS++))
  else
    echo "FAIL: Phase 5.5 section is $SECTION_LINES lines (must be 30-40)"
    ((FAIL++))
  fi
else
  echo "FAIL: Cannot measure Phase 5.5 section size (markers not found)"
  ((FAIL++))
fi

# Test 6: Contains precondition
if grep -qiE "(precondition|pre-condition|pre condition)" "$SKILL_FILE" 2>/dev/null; then
  echo "PASS: SKILL.md contains precondition"
  ((PASS++))
else
  echo "FAIL: SKILL.md does NOT contain precondition"
  ((FAIL++))
fi

# Test 7: Contains postcondition
if grep -qiE "(postcondition|post-condition|post condition)" "$SKILL_FILE" 2>/dev/null; then
  echo "PASS: SKILL.md contains postcondition"
  ((PASS++))
else
  echo "FAIL: SKILL.md does NOT contain postcondition"
  ((FAIL++))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ $FAIL -gt 0 ]; then
  exit 1
fi
