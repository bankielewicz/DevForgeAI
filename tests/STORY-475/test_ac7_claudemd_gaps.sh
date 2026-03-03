#!/bin/bash
# Test: AC#7 - CLAUDE.md Gap Processing
# Story: STORY-475
# Phase: Red (tests should FAIL before implementation)

PASS=0
FAIL=0
FILE="src/claude/skills/designing-systems/references/prompt-alignment-workflow.md"

# Test 1: File contains CLAUDE.md gap processing
if grep -q "CLAUDE\.md" "$FILE" 2>/dev/null; then
  echo "PASS: File references CLAUDE.md gap processing"
  ((PASS++))
else
  echo "FAIL: File does NOT reference CLAUDE.md gap processing"
  ((FAIL++))
fi

# Test 2: File contains draft/approval pattern
if grep -qiE "(draft|drafts|draft missing)" "$FILE" 2>/dev/null; then
  echo "PASS: File contains draft pattern for CLAUDE.md gaps"
  ((PASS++))
else
  echo "FAIL: File does NOT contain draft pattern for CLAUDE.md gaps"
  ((FAIL++))
fi

# Test 3: File contains AskUserQuestion for CLAUDE.md approval before applying
if grep -q "AskUserQuestion" "$FILE" 2>/dev/null; then
  echo "PASS: File contains AskUserQuestion for CLAUDE.md gap approval"
  ((PASS++))
else
  echo "FAIL: File does NOT contain AskUserQuestion for CLAUDE.md gap approval"
  ((FAIL++))
fi

# Test 4: File references deriving gap content from context files
if grep -qiE "(context files|from context|context file)" "$FILE" 2>/dev/null; then
  echo "PASS: File references deriving CLAUDE.md gaps from context files"
  ((PASS++))
else
  echo "FAIL: File does NOT reference deriving CLAUDE.md gaps from context files"
  ((FAIL++))
fi

# Test 5: File references missing sections (build commands or architecture)
if grep -qiE "(build command|architecture overview|missing section)" "$FILE" 2>/dev/null; then
  echo "PASS: File references missing CLAUDE.md sections (build commands/architecture)"
  ((PASS++))
else
  echo "FAIL: File does NOT reference missing CLAUDE.md sections"
  ((FAIL++))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ $FAIL -gt 0 ]; then
  exit 1
fi
