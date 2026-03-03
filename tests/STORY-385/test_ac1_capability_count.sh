#!/usr/bin/env bash
# STORY-385 AC#1: Minimum Five New Capability Opportunities Documented
# Validates:
#   - Output file exists at devforgeai/specs/research/new-capability-opportunities.md
#   - File has valid YAML frontmatter with required metadata fields
#   - At least 5 distinct capability opportunities documented
#   - Each opportunity describes a component not in current registry
#   - Research artifact from STORY-384 is referenced

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

# ---------------------------------------------------------------------------
# Test 1: Output file exists at expected path
# ---------------------------------------------------------------------------
require_doc "New capabilities document at devforgeai/specs/research/new-capability-opportunities.md"

# ---------------------------------------------------------------------------
# Test 2: File starts with YAML frontmatter delimiters (--- ... ---)
# ---------------------------------------------------------------------------
first_line=$(head -n 1 "$DOC")
if [ "$first_line" = "---" ]; then
  pass "File starts with YAML frontmatter delimiter '---'"
else
  fail "File does not start with YAML frontmatter delimiter (found: '$first_line')"
fi

# Extract YAML frontmatter (between first --- and second ---)
closing_line=$(sed -n '2,$ p' "$DOC" | grep -n "^---$" | head -n 1 | cut -d: -f1)
if [ -n "$closing_line" ] && [ "$closing_line" -gt 1 ]; then
  pass "YAML frontmatter has closing delimiter"
  frontmatter=$(sed -n "2,$((closing_line))p" "$DOC")
else
  fail "YAML frontmatter missing closing delimiter"
  frontmatter=""
fi

# ---------------------------------------------------------------------------
# Test 3: Required YAML frontmatter fields
# ---------------------------------------------------------------------------
REQUIRED_FIELDS=("id" "title" "epic" "status" "created" "story_id")

for field in "${REQUIRED_FIELDS[@]}"; do
  if echo "$frontmatter" | grep -qE "^${field}:" 2>/dev/null; then
    pass "YAML frontmatter contains required field: $field"
  else
    fail "YAML frontmatter missing required field: $field"
  fi
done

# ---------------------------------------------------------------------------
# Test 4: At least 5 distinct capability opportunities documented
# Each opportunity should be a ### OPP-NNN level header within the document
# ---------------------------------------------------------------------------
opportunity_count=$(grep -c "^### OPP-" "$DOC" 2>/dev/null || echo "0")
opportunity_count=$(echo "$opportunity_count" | tr -d '[:space:]')

assert_min_count "$opportunity_count" 5 \
  "Found {actual} capability opportunities (minimum {min} required)" \
  "Only {actual} capability opportunities found (minimum {min} required)"

# ---------------------------------------------------------------------------
# Test 5: Each opportunity has a non-empty name
# Check that ### headers have text content after the number
# ---------------------------------------------------------------------------
empty_names=$(grep -E "^### [0-9]+\.\s*$" "$DOC" 2>/dev/null | wc -l || echo "0")
empty_names=$(echo "$empty_names" | tr -d '[:space:]')
if [ "$empty_names" -eq 0 ]; then
  pass "All opportunity headers have non-empty names"
else
  fail "$empty_names opportunity headers have empty names"
fi

# ---------------------------------------------------------------------------
# Test 6: Document references the STORY-384 research artifact
# ---------------------------------------------------------------------------
if grep -q "prompt-engineering-patterns" "$DOC" 2>/dev/null || \
   grep -q "STORY-384" "$DOC" 2>/dev/null; then
  pass "Document references STORY-384 research artifact"
else
  fail "Document does not reference STORY-384 research artifact"
fi

# ---------------------------------------------------------------------------
# Test 7: Each opportunity has all 7 required fields
# Required: opportunity_name (in header), component_type, description,
#           enabling_patterns, feasibility, priority, estimated_effort
# ---------------------------------------------------------------------------
REQUIRED_OPP_FIELDS=("Component Type" "Description" "Enabling Pattern" "Feasibility" "Priority" "Estimated Effort")

for field in "${REQUIRED_OPP_FIELDS[@]}"; do
  field_count=$(grep -ciE "(^|\*\*)(${field})s?(\*\*)?:" "$DOC" 2>/dev/null || echo "0")
  assert_min_count "$field_count" 5 \
    "Found {actual} '${field}' fields across opportunities (need {min}+)" \
    "Only {actual} '${field}' fields found (need {min}+)"
done

print_results
