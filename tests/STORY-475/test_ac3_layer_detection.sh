#!/bin/bash
# Test: AC#3 - Configuration Layer Detection and Graceful Handling
# Story: STORY-475
# Phase: Red (tests should FAIL before implementation)

PASS=0
FAIL=0
FILE="src/claude/skills/designing-systems/references/prompt-alignment-workflow.md"

# Test 1: Step 1 is "Detect Configuration Layers" or similar
if grep -qiE "Step 1.*[Dd]etect|Step 1.*[Cc]onfiguration [Ll]ayer|[Dd]etect.*[Cc]onfiguration [Ll]ayer" "$FILE" 2>/dev/null; then
  echo "PASS: File contains Step 1 for detecting configuration layers"
  ((PASS++))
else
  echo "FAIL: File does NOT contain Step 1 for detecting configuration layers"
  ((FAIL++))
fi

# Test 2: Contains handling for missing CLAUDE.md
if grep -q "CLAUDE\.md" "$FILE" 2>/dev/null; then
  echo "PASS: File references CLAUDE.md handling"
  ((PASS++))
else
  echo "FAIL: File does NOT reference CLAUDE.md handling"
  ((FAIL++))
fi

# Test 3: Contains handling for missing system-prompt-core.md
if grep -q "system-prompt-core\.md\|system-prompt-core" "$FILE" 2>/dev/null; then
  echo "PASS: File references system-prompt-core.md handling"
  ((PASS++))
else
  echo "FAIL: File does NOT reference system-prompt-core.md handling"
  ((FAIL++))
fi

# Test 4: Contains graceful or informational handling when neither exists
if grep -qiE "(graceful|informational|not blocking|non.blocking|proceed)" "$FILE" 2>/dev/null; then
  echo "PASS: File contains graceful/informational handling language"
  ((PASS++))
else
  echo "FAIL: File does NOT contain graceful/informational handling language"
  ((FAIL++))
fi

# Test 5: File states Phase 6 is NOT blocked when neither config layer exists
if grep -qiE "(Phase 6.*not block|not block.*Phase 6|proceed.*Phase 6|Phase 6.*proceed)" "$FILE" 2>/dev/null; then
  echo "PASS: File states Phase 6 is not blocked when neither config layer exists"
  ((PASS++))
else
  echo "FAIL: File does NOT state Phase 6 is not blocked when neither config layer exists"
  ((FAIL++))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ $FAIL -gt 0 ]; then
  exit 1
fi
