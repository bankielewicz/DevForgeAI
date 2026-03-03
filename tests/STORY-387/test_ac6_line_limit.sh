#!/usr/bin/env bash
# STORY-387 AC#6: 1000-Line Size Constraint Compliance
# Verifies template is under 300 lines, includes line budget guidance,
# and documents 800-line extraction threshold.
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

echo "=== AC#6: 1000-Line Size Constraint Compliance ==="
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

# Test 2: Template under 300 lines
echo "Test 2: Template is under 300 lines"
LINE_COUNT=$(wc -l < "$FILE" 2>/dev/null || echo "0")
if [ "$LINE_COUNT" -le 300 ]; then
  echo "  PASS: Template has $LINE_COUNT lines (<= 300)"
  PASS=$((PASS + 1))
else
  echo "  FAIL: Template has $LINE_COUNT lines (exceeds 300)"
  FAIL=$((FAIL + 1))
fi

# Test 3: Line budget guidance per section
echo "Test 3: Line budget guidance per section documented"
assert_grep "Line budget table or guidance" "line.*budget|budget.*line|Section.*Budget|Budget.*Target"

# Test 4: 800-line extraction guidance
echo "Test 4: 800-line extraction threshold documented"
assert_grep "800-line extraction guidance" "800.*line|exceeding.*800|800.*extract"

# Test 5: 1000-line maximum referenced
echo "Test 5: 1000-line maximum for SKILL.md referenced"
assert_grep "1000-line maximum documented" "1000.*line|1,000.*line|thousand.*line"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
