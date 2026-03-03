#!/usr/bin/env bash
# STORY-386 AC#2: YAML Frontmatter Schema Fully Specified
# Verifies the template specifies all 9 frontmatter fields with type and required/optional.
# TDD RED phase - this test MUST FAIL until the template is created.

set -euo pipefail

TEMPLATE="src/claude/agents/agent-generator/references/canonical-agent-template.md"
ERRORS=0

if [[ ! -f "$TEMPLATE" ]]; then
  echo "FAIL: Template file does not exist at $TEMPLATE"
  exit 1
fi

# 9 frontmatter fields that must be documented
FIELDS=(
  "name"
  "description"
  "tools"
  "model"
  "color"
  "permissionMode"
  "skills"
  "proactive_triggers"
  "version"
)

for field in "${FIELDS[@]}"; do
  if ! grep -q "$field" "$TEMPLATE"; then
    echo "FAIL: Missing frontmatter field definition: $field"
    ERRORS=$((ERRORS + 1))
  fi
done

# Each field should have a type annotation (string, array, enum, etc.)
TYPE_KEYWORDS="string\|array\|enum\|boolean\|semver"
for field in "${FIELDS[@]}"; do
  # Search for the field name near a type keyword (within 3 lines)
  if ! grep -A3 "$field" "$TEMPLATE" | grep -qi "$TYPE_KEYWORDS"; then
    echo "FAIL: Field '$field' missing type annotation (string/array/enum/boolean/semver)"
    ERRORS=$((ERRORS + 1))
  fi
done

# Check for required/optional designation
if ! grep -qi "required" "$TEMPLATE"; then
  echo "FAIL: No 'required' designation found in schema"
  ERRORS=$((ERRORS + 1))
fi

if ! grep -qi "optional" "$TEMPLATE"; then
  echo "FAIL: No 'optional' designation found in schema"
  ERRORS=$((ERRORS + 1))
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "FAIL: $ERRORS error(s) found in AC#2 validation"
  exit 1
fi

echo "PASS: All 9 frontmatter fields fully specified with type and required/optional"
exit 0
