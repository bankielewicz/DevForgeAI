#!/usr/bin/env bash
# STORY-387 AC#4: Reference File Loading Pattern Definition
# Verifies standard Read() hint format with absolute paths, conditional loading prefix,
# no-duplication rule, and standalone readability requirement.
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

echo "=== AC#4: Reference File Loading Pattern Definition ==="
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

# Test 2: Standard Read() hint format with absolute path
echo "Test 2: Standard Read() hint format with .claude/skills/ path"
assert_grep "Read() hint with absolute path" 'Read\(file_path="\.claude/skills/'

# Test 3: Loading hints after section headers
echo "Test 3: Loading hints documented near section headers"
assert_grep "Loading hint placement guidance" "section header|after.*header|immediately"

# Test 4: Conditional loading prefix documented
echo "Test 4: Conditional loading uses 'Load if' prefix"
assert_grep "Conditional loading prefix" "Load if|conditional.*load"

# Test 5: No-duplication rule stated
echo "Test 5: No-duplication rule between SKILL.md and references"
assert_grep "No-duplication rule" "not.*duplicate|no.*duplication|single source|must not duplicate"

# Test 6: Reference files must have H1 title
echo "Test 6: Reference files must have H1 title and purpose"
assert_grep "Reference file standalone readability" "H1.*title|title.*purpose|standalone|purpose statement"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
