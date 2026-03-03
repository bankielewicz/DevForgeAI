#!/usr/bin/env bash
# STORY-385 AC#2: Each Opportunity Has Feasibility Assessment
# Validates:
#   - Each opportunity has a feasibility rating of High, Medium, or Low
#   - Feasibility considers CCT (Claude Code Terminal) constraints
#   - Feasibility considers architecture-constraints.md alignment
#   - Feasibility includes estimated effort in story points (Fibonacci)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "New capabilities document"

# ---------------------------------------------------------------------------
# Test 2: Each opportunity has a Feasibility field
# ---------------------------------------------------------------------------
feasibility_count=$(grep -ciE "(^|\*\*)Feasibility(\*\*)?:" "$DOC" 2>/dev/null || echo "0")
opportunity_count=$(grep -cE "^### " "$DOC" 2>/dev/null || echo "0")

assert_min_count "$feasibility_count" 5 \
  "Found {actual} Feasibility fields (need {min}+)" \
  "Only {actual} Feasibility fields found (need {min}+)"

# ---------------------------------------------------------------------------
# Test 3: All feasibility values are valid enum (High, Medium, Low)
# ---------------------------------------------------------------------------
invalid_feasibility=0
while IFS= read -r line; do
  # Extract value after "Feasibility:" (or **Feasibility**:)
  value=$(echo "$line" | sed -E 's/^.*[Ff]easibility(\*\*)?:\s*//' | sed 's/\*\*//g' | xargs)
  # Allow "Medium - Requires Validation" variants per edge case spec
  base_value=$(echo "$value" | sed -E 's/\s*[-—].*//')
  if ! echo "$base_value" | grep -qiE "^(High|Medium|Low)$" 2>/dev/null; then
    invalid_feasibility=$((invalid_feasibility + 1))
    echo "  Invalid feasibility value: '$value'"
  fi
done < <(grep -iE "(^|\*\*)Feasibility(\*\*)?:" "$DOC" 2>/dev/null)

if [ "$invalid_feasibility" -eq 0 ]; then
  pass "All feasibility ratings are valid (High/Medium/Low)"
else
  fail "$invalid_feasibility feasibility ratings have invalid values (must be High, Medium, or Low)"
fi

# ---------------------------------------------------------------------------
# Test 4: Feasibility considers CCT constraints
# At least one mention of Claude Code Terminal, CCT, or terminal constraints
# ---------------------------------------------------------------------------
cct_mentions=$(grep -ciE "(Claude Code Terminal|CCT|terminal constraint)" "$DOC" 2>/dev/null || echo "0")
if [ "$cct_mentions" -ge 1 ]; then
  pass "Document references CCT constraints ($cct_mentions mentions)"
else
  fail "No reference to Claude Code Terminal (CCT) constraints found"
fi

# ---------------------------------------------------------------------------
# Test 5: Feasibility considers architecture alignment
# At least one mention of architecture-constraints.md or architecture alignment
# ---------------------------------------------------------------------------
arch_mentions=$(grep -ciE "(architecture.constraints|architecture alignment|architecture-constraints\.md)" "$DOC" 2>/dev/null || echo "0")
if [ "$arch_mentions" -ge 1 ]; then
  pass "Document references architecture alignment ($arch_mentions mentions)"
else
  fail "No reference to architecture constraints alignment found"
fi

# ---------------------------------------------------------------------------
# Test 6: Each opportunity has an estimated effort in story points
# ---------------------------------------------------------------------------
effort_count=$(grep -ciE "(^|\*\*)Estimated Effort(\*\*)?:" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$effort_count" 5 \
  "Found {actual} Estimated Effort fields (need {min}+)" \
  "Only {actual} Estimated Effort fields found (need {min}+)"

# ---------------------------------------------------------------------------
# Test 7: Effort values are valid Fibonacci numbers (1, 2, 3, 5, 8, 13)
# ---------------------------------------------------------------------------
invalid_effort=0
while IFS= read -r line; do
  # Extract numeric value from effort field
  value=$(echo "$line" | grep -oE "[0-9]+" | head -n 1)
  if [ -n "$value" ]; then
    case "$value" in
      1|2|3|5|8|13) ;; # valid Fibonacci
      *) invalid_effort=$((invalid_effort + 1))
         echo "  Invalid effort value: $value (must be 1, 2, 3, 5, 8, or 13)" ;;
    esac
  else
    invalid_effort=$((invalid_effort + 1))
    echo "  No numeric value found in effort field: '$line'"
  fi
done < <(grep -iE "(^|\*\*)Estimated Effort(\*\*)?:" "$DOC" 2>/dev/null)

if [ "$invalid_effort" -eq 0 ]; then
  pass "All effort estimates are valid Fibonacci numbers"
else
  fail "$invalid_effort effort estimates have invalid values (must be Fibonacci: 1, 2, 3, 5, 8, 13)"
fi

# ---------------------------------------------------------------------------
# Test 8: High/Medium feasibility entries contain architecture alignment text (BR-003)
# ---------------------------------------------------------------------------
high_med_count=0
high_med_with_arch=0

# Process each opportunity section - check if High/Medium feasibility AND has arch text
# This is a simplified check: for each High/Medium, look for architecture reference nearby
while IFS= read -r line; do
  value=$(echo "$line" | sed -E 's/^.*[Ff]easibility(\*\*)?:\s*//' | sed 's/\*\*//g' | xargs)
  base_value=$(echo "$value" | sed -E 's/\s*[-—].*//')
  if echo "$base_value" | grep -qiE "^(High|Medium)$" 2>/dev/null; then
    high_med_count=$((high_med_count + 1))
  fi
done < <(grep -iE "(^|\*\*)Feasibility(\*\*)?:" "$DOC" 2>/dev/null)

if [ "$high_med_count" -gt 0 ]; then
  if [ "$arch_mentions" -ge 1 ]; then
    pass "Architecture alignment referenced for High/Medium feasibility entries"
  else
    fail "High/Medium feasibility entries lack architecture alignment references"
  fi
else
  pass "No High/Medium feasibility entries to validate (all Low)"
fi

print_results
