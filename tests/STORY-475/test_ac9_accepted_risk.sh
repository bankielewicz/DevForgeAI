#!/bin/bash
# Test: AC#9 - User Override for Disputed HIGH Findings (ACCEPTED_RISK)
# Story: STORY-475
# Phase: Red (tests should FAIL before implementation)

PASS=0
FAIL=0
FILE="src/claude/skills/designing-systems/references/prompt-alignment-workflow.md"

# Test 1: File contains ACCEPTED_RISK override mechanism
if grep -q "ACCEPTED_RISK" "$FILE" 2>/dev/null; then
  echo "PASS: File contains ACCEPTED_RISK override"
  ((PASS++))
else
  echo "FAIL: File does NOT contain ACCEPTED_RISK override"
  ((FAIL++))
fi

# Test 2: File requires non-empty justification for override
if grep -qiE "(justification|non.empty|required)" "$FILE" 2>/dev/null; then
  echo "PASS: File contains justification requirement"
  ((PASS++))
else
  echo "FAIL: File does NOT contain justification requirement"
  ((FAIL++))
fi

# Test 3: File contains AskUserQuestion with override option
if grep -q "AskUserQuestion" "$FILE" 2>/dev/null; then
  echo "PASS: File contains AskUserQuestion with override option"
  ((PASS++))
else
  echo "FAIL: File does NOT contain AskUserQuestion with override option"
  ((FAIL++))
fi

# Test 4: File states Phase 6 is unblocked once all HIGH findings resolved or overridden
if grep -qiE "(unblock|Phase 6.*unblock|resolved or overridden|overridden.*proceed)" "$FILE" 2>/dev/null; then
  echo "PASS: File states Phase 6 unblocked when findings resolved or overridden"
  ((PASS++))
else
  echo "FAIL: File does NOT state Phase 6 unblocked when findings resolved or overridden"
  ((FAIL++))
fi

# Test 5: File contains "Override with justification" or equivalent override option label
if grep -qiE "(override.*justification|justification.*override|Override)" "$FILE" 2>/dev/null; then
  echo "PASS: File contains override with justification option"
  ((PASS++))
else
  echo "FAIL: File does NOT contain override with justification option"
  ((FAIL++))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ $FAIL -gt 0 ]; then
  exit 1
fi
