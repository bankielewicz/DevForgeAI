#!/usr/bin/env bash
# STORY-387 AC#3: Progressive Disclosure Structure Definition
# Verifies content allocation table with SKILL.md, references/, phases/, assets/ entries
# and 100-line extraction threshold.
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

echo "=== AC#3: Progressive Disclosure Structure Definition ==="
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

# Test 2: Content allocation table present
echo "Test 2: Content allocation table present"
assert_grep "Content allocation table exists" "Content.*Location|Location.*Content|allocation"

# Test 3: SKILL.md entry in allocation
echo "Test 3: SKILL.md entry in content allocation"
assert_grep "SKILL.md content allocation defined" "SKILL\.md"

# Test 4: references/ entry in allocation
echo "Test 4: references/ entry in content allocation"
assert_grep "references/ content allocation defined" "references/"

# Test 5: phases/ entry in allocation (optional directory)
echo "Test 5: phases/ entry documented (optional)"
assert_grep "phases/ documented as optional" "phases/"

# Test 6: assets/ entry in allocation
echo "Test 6: assets/templates/ entry in content allocation"
assert_grep "assets/ content allocation defined" "assets/"

# Test 7: 100-line extraction threshold documented
echo "Test 7: 100-line extraction threshold documented"
assert_grep "100-line extraction threshold" "100.line|100 line|exceed.*100"

# Test 8: Decision matrix for when to extract to references
echo "Test 8: Decision matrix for extraction"
assert_grep "Decision matrix or extraction guidance" "decision.*matrix|when.*extract|extraction.*threshold"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
