#!/usr/bin/env bash
# STORY-387 AC#7: Backward Compatibility Verification
# Verifies Migration Notes section with tools format, phase numbering,
# and adoption timeline documentation.
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

echo "=== AC#7: Backward Compatibility Verification ==="
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

# Test 2: Migration Notes section present
echo "Test 2: Migration Notes section heading present"
assert_grep "Migration Notes heading" "## Migration Notes|## Migration"

# Test 3: Existing skills not required to immediately adopt
echo "Test 3: Existing skills not required to immediately adopt"
assert_grep "Gradual adoption documented" "not required.*immediately|gradual|existing skills.*continue|not.*mandatory"

# Test 4: tools string format continues to work
echo "Test 4: tools string format backward compatibility noted"
assert_grep "tools string format continues" "tools.*string.*continue|tools.*string.*work|string.*format.*continue"

# Test 5: Unpadded phase numbers continue to function
echo "Test 5: Unpadded phase numbers backward compatibility noted"
assert_grep "Unpadded phase numbers continue" "unpadded.*continue|unpadded.*function|unpadded.*work"

# Test 6: Template applies only to new/updated skills
echo "Test 6: Template scope limited to new and actively updated skills"
assert_grep "Applies to new/updated skills" "new.*skill|actively.*updated|new.*and.*updated"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
