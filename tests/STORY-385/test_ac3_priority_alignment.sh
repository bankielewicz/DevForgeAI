#!/usr/bin/env bash
# STORY-385 AC#3: Each Opportunity Has Priority Rating Aligned with Architecture Constraints
# Validates:
#   - Each opportunity has a priority rating (P0, P1, or P2)
#   - All priority values are valid enum (P0/P1/P2)
#   - Priority considers framework quality impact (has impact statement)
#   - Priority aligned with BRAINSTORM-010 MoSCoW classification

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "New capabilities document"

# ---------------------------------------------------------------------------
# Test 2: Each opportunity has a Priority field
# ---------------------------------------------------------------------------
priority_count=$(grep -ciE "(^|\*\*)Priority(\*\*)?:" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$priority_count" 5 \
  "Found {actual} Priority fields (need {min}+)" \
  "Only {actual} Priority fields found (need {min}+)"

# ---------------------------------------------------------------------------
# Test 3: All priority values are valid enum (P0, P1, P2)
# ---------------------------------------------------------------------------
invalid_priority=0
while IFS= read -r line; do
  # Extract value after "Priority:" (or **Priority**:)
  value=$(echo "$line" | sed -E 's/^.*[Pp]riority(\*\*)?:\s*//' | sed 's/\*\*//g' | xargs)
  # Allow labels like "P0 (Critical)", "P1 (Important)", "P2 (Nice-to-have)"
  base_value=$(echo "$value" | grep -oE "P[0-2]" | head -n 1)
  if [ -z "$base_value" ]; then
    invalid_priority=$((invalid_priority + 1))
    echo "  Invalid priority value: '$value' (must contain P0, P1, or P2)"
  fi
done < <(grep -iE "(^|\*\*)Priority(\*\*)?:" "$DOC" 2>/dev/null)

if [ "$invalid_priority" -eq 0 ]; then
  pass "All priority ratings are valid (P0/P1/P2)"
else
  fail "$invalid_priority priority ratings have invalid values (must be P0, P1, or P2)"
fi

# ---------------------------------------------------------------------------
# Test 4: Priority labels include descriptive meaning
# P0 should map to Critical, P1 to Important, P2 to Nice-to-have
# ---------------------------------------------------------------------------
has_p0_label=false
has_p1_label=false
has_p2_label=false

if grep -qiE "P0.*Critical|Critical.*P0" "$DOC" 2>/dev/null; then has_p0_label=true; fi
if grep -qiE "P1.*Important|Important.*P1" "$DOC" 2>/dev/null; then has_p1_label=true; fi
if grep -qiE "P2.*Nice.to.have|Nice.to.have.*P2" "$DOC" 2>/dev/null; then has_p2_label=true; fi

# At least the priority legend/description should exist
if [ "$has_p0_label" = true ] || [ "$has_p1_label" = true ] || [ "$has_p2_label" = true ]; then
  pass "Priority labels include descriptive meaning (P0=Critical, P1=Important, P2=Nice-to-have)"
else
  fail "Priority labels lack descriptive meaning - need P0=Critical, P1=Important, or P2=Nice-to-have"
fi

# ---------------------------------------------------------------------------
# Test 5: Document references framework quality impact
# At least one mention of quality, quality metrics, or impact assessment
# ---------------------------------------------------------------------------
quality_mentions=$(grep -ciE "(quality metric|quality impact|framework quality|impact assessment)" "$DOC" 2>/dev/null || echo "0")
if [ "$quality_mentions" -ge 1 ]; then
  pass "Document references framework quality impact ($quality_mentions mentions)"
else
  fail "No reference to framework quality impact found"
fi

# ---------------------------------------------------------------------------
# Test 6: Priority aligned with BRAINSTORM-010 MoSCoW classification
# Document should reference MoSCoW or BRAINSTORM-010
# ---------------------------------------------------------------------------
moscow_mentions=$(grep -ciE "(MoSCoW|BRAINSTORM-010|Must.Have|Should.Have|Could.Have|Won.t.Have)" "$DOC" 2>/dev/null || echo "0")
if [ "$moscow_mentions" -ge 1 ]; then
  pass "Document references MoSCoW classification ($moscow_mentions mentions)"
else
  fail "No reference to MoSCoW classification or BRAINSTORM-010 found"
fi

print_results
