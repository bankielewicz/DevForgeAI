#!/usr/bin/env bash
# STORY-387 AC#1: YAML Frontmatter Field Standardization
# Verifies the skill template specifies required fields (name, description, model)
# and optional fields (allowed-tools, version, status), with allowed-tools as canonical format.
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

echo "=== AC#1: YAML Frontmatter Field Standardization ==="
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

# Test 2: Required field - name
echo "Test 2: Required field 'name' documented"
assert_grep "name is listed as required" "name.*required|required.*name"

# Test 3: Required field - description
echo "Test 3: Required field 'description' documented"
assert_grep "description is listed as required" "description.*required|required.*description"

# Test 4: Required field - model
echo "Test 4: Required field 'model' documented"
assert_grep "model.*required|required.*model" "model.*required|required.*model"

# Test 5: Optional field - allowed-tools
echo "Test 5: Optional field 'allowed-tools' documented"
assert_grep "allowed-tools is listed as optional" "allowed-tools.*optional|optional.*allowed-tools"

# Test 6: Optional field - version
echo "Test 6: Optional field 'version' documented"
assert_grep "version is listed as optional" "version.*optional|optional.*version"

# Test 7: Optional field - status
echo "Test 7: Optional field 'status' documented"
assert_grep "status is listed as optional" "status.*optional|optional.*status"

# Test 8: allowed-tools is canonical format (array)
echo "Test 8: allowed-tools specified as array format"
assert_grep "allowed-tools uses array format" "allowed-tools.*array|array.*allowed-tools"

# Test 9: tools string format documented as deprecated alias
echo "Test 9: tools string format noted as deprecated"
assert_grep "tools string is deprecated alias" "tools.*deprecated|deprecated.*tools"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
