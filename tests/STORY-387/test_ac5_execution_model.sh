#!/usr/bin/env bash
# STORY-387 AC#5: Execution Model Declaration Standardization
# Verifies copy-paste block with 4-point numbered list and 3+ Do NOT items.
#
# TDD Phase: RED - These tests MUST fail until the template is created.
set -uo pipefail

TEMPLATE="src/claude/skills/devforgeai-subagent-creation/assets/templates/skill-template.md"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
FILE="$PROJECT_ROOT/$TEMPLATE"
PASS=0
FAIL=0

assert_grep() {
  local description="$1"
  local pattern="$2"
  if grep -qiP "$pattern" "$FILE" 2>/dev/null; then
    echo "  PASS: $description"
    PASS=$((PASS + 1))
  else
    echo "  FAIL: $description"
    FAIL=$((FAIL + 1))
  fi
}

count_matches() {
  local pattern="$1"
  grep -ciP "$pattern" "$FILE" 2>/dev/null || echo "0"
}

echo "=== AC#5: Execution Model Declaration Standardization ==="
echo ""

# Test 1: File exists
echo "Test 1: Template file exists"
if [ -f "$FILE" ]; then
  echo "  PASS: Template file exists"
  PASS=$((PASS + 1))
else
  echo "  FAIL: Template file does not exist at $TEMPLATE"
  FAIL=$((FAIL + 1))
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# Test 2: Execution Model heading present
echo "Test 2: Execution Model heading present"
assert_grep "Execution Model heading" "## Execution Model"

# Test 3: Inline expansion explanation (4-line numbered list)
echo "Test 3: 4-point numbered list for inline expansion"
NUMBERED_COUNT=$(grep -cP '^\d+\.' "$FILE" 2>/dev/null || echo "0")
if [ "$NUMBERED_COUNT" -ge 4 ]; then
  echo "  PASS: Found $NUMBERED_COUNT numbered list items (>= 4)"
  PASS=$((PASS + 1))
else
  echo "  FAIL: Found $NUMBERED_COUNT numbered list items (need >= 4)"
  FAIL=$((FAIL + 1))
fi

# Test 4: Do NOT anti-pattern list (minimum 3 items)
echo "Test 4: At least 3 'Do NOT' items"
DO_NOT_COUNT=$(grep -ciP "do not" "$FILE" 2>/dev/null || echo "0")
if [ "$DO_NOT_COUNT" -ge 3 ]; then
  echo "  PASS: Found $DO_NOT_COUNT 'Do NOT' items (>= 3)"
  PASS=$((PASS + 1))
else
  echo "  FAIL: Found $DO_NOT_COUNT 'Do NOT' items (need >= 3)"
  FAIL=$((FAIL + 1))
fi

# Test 5: "Proceed to" directive
echo "Test 5: 'Proceed to' directive present"
assert_grep "'Proceed to' directive" "Proceed to"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
