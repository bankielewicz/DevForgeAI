#!/bin/bash
# Test: AC#4 - alignment-auditor Subagent Invocation
# Story: STORY-475
# Phase: Red (tests should FAIL before implementation)

PASS=0
FAIL=0
FILE="src/claude/skills/designing-systems/references/prompt-alignment-workflow.md"

# Test 1: File contains Task() invocation pattern
if grep -qE "Task\(" "$FILE" 2>/dev/null; then
  echo "PASS: File contains Task() invocation"
  ((PASS++))
else
  echo "FAIL: File does NOT contain Task() invocation"
  ((FAIL++))
fi

# Test 2: File contains alignment-auditor subagent reference
if grep -q "alignment-auditor" "$FILE" 2>/dev/null; then
  echo "PASS: File references alignment-auditor subagent"
  ((PASS++))
else
  echo "FAIL: File does NOT reference alignment-auditor subagent"
  ((FAIL++))
fi

# Test 3: File contains subagent_type="alignment-auditor" invocation
if grep -qE 'subagent_type.*alignment-auditor|alignment-auditor.*subagent_type' "$FILE" 2>/dev/null; then
  echo "PASS: File contains subagent_type=\"alignment-auditor\" pattern"
  ((PASS++))
else
  echo "FAIL: File does NOT contain subagent_type=\"alignment-auditor\" pattern"
  ((FAIL++))
fi

# Test 4: Contains structured JSON output reference
if grep -qiE "(JSON|json|structured output|contradictions|gaps)" "$FILE" 2>/dev/null; then
  echo "PASS: File references structured JSON output"
  ((PASS++))
else
  echo "FAIL: File does NOT reference structured JSON output"
  ((FAIL++))
fi

# Test 5: Contains context file passing to subagent
if grep -qiE "(context files|context_files|6 context|all.*context)" "$FILE" 2>/dev/null; then
  echo "PASS: File references passing context files to subagent"
  ((PASS++))
else
  echo "FAIL: File does NOT reference passing context files to subagent"
  ((FAIL++))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ $FAIL -gt 0 ]; then
  exit 1
fi
