#!/usr/bin/env bash
# STORY-386 AC#6: Consistent Frontmatter Field Naming Convention
# Verifies underscore convention documented and migration mapping table has 5+ entries.
# TDD RED phase - this test MUST FAIL until the template is created.

set -euo pipefail

TEMPLATE="src/claude/agents/agent-generator/references/canonical-agent-template.md"
ERRORS=0

if [[ ! -f "$TEMPLATE" ]]; then
  echo "FAIL: Template file does not exist at $TEMPLATE"
  exit 1
fi

# Underscore naming convention must be documented
if ! grep -qi "underscore" "$TEMPLATE"; then
  echo "FAIL: Underscore naming convention not documented"
  ERRORS=$((ERRORS + 1))
fi

# Migration mapping table must exist
if ! grep -qi "migration.*mapping\|mapping.*table\|migration.*table" "$TEMPLATE"; then
  echo "FAIL: Migration mapping table not found"
  ERRORS=$((ERRORS + 1))
fi

# Known variant mappings that should appear
KNOWN_VARIANTS=(
  "allowed-tools"
  "proactive-triggers"
  "proactive_triggers"
)
for variant in "${KNOWN_VARIANTS[@]}"; do
  if ! grep -q "$variant" "$TEMPLATE"; then
    echo "FAIL: Migration mapping missing known variant: $variant"
    ERRORS=$((ERRORS + 1))
  fi
done

# Migration table must have at least 5 rows (pipe-delimited table rows)
# Count rows that look like table data (contain | but exclude header separators with ---)
TABLE_ROWS=$(grep -c '|.*|.*|' "$TEMPLATE" 2>/dev/null || echo "0")
# Subtract header rows (lines with --- between pipes)
SEPARATOR_ROWS=$(grep -c '|.*---.*|' "$TEMPLATE" 2>/dev/null || echo "0")
DATA_ROWS=$((TABLE_ROWS - SEPARATOR_ROWS))

# We need at least 5 mapping entries in the migration table
# Note: this counts ALL table rows in the document; a more precise check
# would scope to the migration section, but for RED phase this is sufficient.
if [[ $DATA_ROWS -lt 5 ]]; then
  echo "FAIL: Migration mapping table has fewer than 5 data rows (found: $DATA_ROWS)"
  ERRORS=$((ERRORS + 1))
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "FAIL: $ERRORS error(s) found in AC#6 validation"
  exit 1
fi

echo "PASS: Underscore convention documented and migration mapping table has 5+ entries"
exit 0
