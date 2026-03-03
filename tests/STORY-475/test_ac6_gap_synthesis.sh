#!/bin/bash
# Test: AC#6 - System Prompt Gap Synthesis
# Story: STORY-475
# Phase: Red (tests should FAIL before implementation)

PASS=0
FAIL=0
FILE="src/claude/skills/designing-systems/references/prompt-alignment-workflow.md"

# Test 1: File contains <project_context> template
if grep -q "<project_context>" "$FILE" 2>/dev/null; then
  echo "PASS: File contains <project_context> template"
  ((PASS++))
else
  echo "FAIL: File does NOT contain <project_context> template"
  ((FAIL++))
fi

# Test 2: File contains "Platform Constraint" section
if grep -qiE "Platform Constraint" "$FILE" 2>/dev/null; then
  echo "PASS: File contains 'Platform Constraint' section"
  ((PASS++))
else
  echo "FAIL: File does NOT contain 'Platform Constraint' section"
  ((FAIL++))
fi

# Test 3: File contains "Build System Routing" section
if grep -qiE "Build System Routing" "$FILE" 2>/dev/null; then
  echo "PASS: File contains 'Build System Routing' section"
  ((PASS++))
else
  echo "FAIL: File does NOT contain 'Build System Routing' section"
  ((FAIL++))
fi

# Test 4: File contains "Subagent Routing" section
if grep -qiE "Subagent Routing" "$FILE" 2>/dev/null; then
  echo "PASS: File contains 'Subagent Routing' section"
  ((PASS++))
else
  echo "FAIL: File does NOT contain 'Subagent Routing' section"
  ((FAIL++))
fi

# Test 5: File contains "Current State" section
if grep -qiE "Current State" "$FILE" 2>/dev/null; then
  echo "PASS: File contains 'Current State' section"
  ((PASS++))
else
  echo "FAIL: File does NOT contain 'Current State' section"
  ((FAIL++))
fi

# Test 6: File contains AskUserQuestion for approval of gap synthesis
if grep -q "AskUserQuestion" "$FILE" 2>/dev/null; then
  echo "PASS: File contains AskUserQuestion for gap approval"
  ((PASS++))
else
  echo "FAIL: File does NOT contain AskUserQuestion for gap approval"
  ((FAIL++))
fi

# Summary
echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ $FAIL -gt 0 ]; then
  exit 1
fi
