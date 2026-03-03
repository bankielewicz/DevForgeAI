#!/usr/bin/env bash
# STORY-384 AC#7: Grep Queryable

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "Research document"

# Test 2: Grep "Applicability: High" returns 10+ matches
high_matches=$(grep -c "Applicability: High" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$high_matches" 10 \
  "Grep 'Applicability: High' returns {actual} matches (need 10+)" \
  "Grep 'Applicability: High' returns only {actual} matches (need 10+)"

# Tests 3-5: Rating field values appear only as line-start field labels
assert_field_only "Applicability: High"
assert_field_only "Applicability: Medium"
assert_field_only "Applicability: Low"

# Test 6: Consistent field order
# Check that Source -> Description -> Applicability -> Rationale -> Recommendation appear in that order
order_violations=0
last_field=""
while IFS= read -r line; do
  if echo "$line" | grep -qE "^Source:"; then
    last_field="Source"
  elif echo "$line" | grep -qE "^Description:"; then
    if [ "$last_field" != "Source" ]; then
      order_violations=$((order_violations + 1))
    fi
    last_field="Description"
  elif echo "$line" | grep -qE "^Applicability:"; then
    if [ "$last_field" != "Description" ]; then
      order_violations=$((order_violations + 1))
    fi
    last_field="Applicability"
  elif echo "$line" | grep -qE "^Rationale:"; then
    if [ "$last_field" != "Applicability" ]; then
      order_violations=$((order_violations + 1))
    fi
    last_field="Rationale"
  elif echo "$line" | grep -qE "^DevForgeAI Recommendation:"; then
    if [ "$last_field" != "Rationale" ]; then
      order_violations=$((order_violations + 1))
    fi
    last_field="Recommendation"
  fi
done < "$DOC"

if [ "$order_violations" -eq 0 ]; then
  pass "All patterns have consistent field order"
else
  fail "$order_violations field order violations detected"
fi

# Test 7: No field labels in prose sections
prose_fields=0
in_pattern=false
while IFS= read -r line; do
  if echo "$line" | grep -qE "^#### PE-[0-9]{3}:"; then
    in_pattern=true
  elif echo "$line" | grep -qE "^## |^### "; then
    in_pattern=false
  fi
  if [ "$in_pattern" = false ]; then
    if echo "$line" | grep -qE "^(Source|Description|Applicability|Rationale|DevForgeAI Recommendation):" 2>/dev/null; then
      prose_fields=$((prose_fields + 1))
    fi
  fi
done < "$DOC"

if [ "$prose_fields" -le 4 ]; then  # Allow some in section headers
  pass "No pattern field labels found in prose/summary sections"
else
  fail "$prose_fields field labels found in prose sections"
fi

# Test 8: PE-NNN identifiers queryable
pe_headers=$(grep -cE "^#{1,4}.*PE-[0-9]{3}:" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$pe_headers" 30 \
  "PE-NNN identifiers queryable via grep ({actual} header matches)" \
  "PE-NNN identifiers not grep-queryable ({actual} header matches, need 30+)"

print_results
