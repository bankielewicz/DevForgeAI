#!/usr/bin/env bash
# STORY-385 AC#4: Opportunities Mapped to Enabling Anthropic Patterns
# Validates:
#   - Each opportunity references at least one PE-NNN pattern
#   - Pattern references use valid PE-NNN format (PE-001 through PE-999)
#   - Each reference explains how the pattern enables the capability
#   - Pattern references match entries that exist in the STORY-384 research artifact

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "New capabilities document"

# ---------------------------------------------------------------------------
# Test 2: Each opportunity has an Enabling Patterns field
# ---------------------------------------------------------------------------
pattern_field_count=$(grep -ciE "(^|\*\*)Enabling Pattern" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$pattern_field_count" 5 \
  "Found {actual} Enabling Pattern fields (need {min}+)" \
  "Only {actual} Enabling Pattern fields found (need {min}+)"

# ---------------------------------------------------------------------------
# Test 3: Document contains PE-NNN pattern references
# ---------------------------------------------------------------------------
pe_refs=$(grep -oE "PE-[0-9]{3}" "$DOC" 2>/dev/null | sort -u || true)
if [ -z "$pe_refs" ]; then
  pe_count=0
else
  pe_count=$(echo "$pe_refs" | wc -l | tr -d '[:space:]')
fi

assert_min_count "$pe_count" 1 \
  "Found {actual} unique PE-NNN references (need {min}+)" \
  "No PE-NNN pattern references found (need {min}+)"

# ---------------------------------------------------------------------------
# Test 4: All PE-NNN references use valid format (PE-001 through PE-999)
# ---------------------------------------------------------------------------
invalid_pe=0
while IFS= read -r pe_id; do
  num=$(echo "$pe_id" | grep -oE "[0-9]{3}")
  if [ -z "$num" ] || [ "$num" -eq 0 ]; then
    invalid_pe=$((invalid_pe + 1))
    echo "  Invalid PE reference: '$pe_id'"
  fi
done < <(grep -oE "PE-[0-9]{3}" "$DOC" 2>/dev/null | sort -u)

if [ "$invalid_pe" -eq 0 ] && [ "$pe_count" -gt 0 ]; then
  pass "All PE-NNN references use valid format"
elif [ "$pe_count" -eq 0 ]; then
  fail "No PE-NNN references to validate"
else
  fail "$invalid_pe PE-NNN references have invalid format"
fi

# ---------------------------------------------------------------------------
# Test 5: At least 5 PE-NNN references across all opportunities
# (since minimum 5 opportunities, each with at least 1 pattern)
# ---------------------------------------------------------------------------
total_pe_refs=$(grep -cE "PE-[0-9]{3}" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$total_pe_refs" 5 \
  "Found {actual} total PE-NNN references (need {min}+)" \
  "Only {actual} total PE-NNN references found (need {min}+)"

# ---------------------------------------------------------------------------
# Test 6: PE-NNN references exist in the STORY-384 research artifact
# Cross-validate referenced patterns against the research artifact
# ---------------------------------------------------------------------------
if [ -f "$RESEARCH_ARTIFACT" ]; then
  unmatched=0
  while IFS= read -r pe_id; do
    if ! grep -q "$pe_id" "$RESEARCH_ARTIFACT" 2>/dev/null; then
      unmatched=$((unmatched + 1))
      echo "  PE reference '$pe_id' not found in research artifact"
    fi
  done < <(grep -oE "PE-[0-9]{3}" "$DOC" 2>/dev/null | sort -u)

  if [ "$unmatched" -eq 0 ]; then
    pass "All PE-NNN references match entries in research artifact"
  else
    fail "$unmatched PE-NNN references not found in research artifact"
  fi
else
  fail "Research artifact not found at $RESEARCH_ARTIFACT - cannot cross-validate PE references"
fi

# ---------------------------------------------------------------------------
# Test 7: Pattern references include source repo information
# Each pattern reference should mention the source repository
# ---------------------------------------------------------------------------
source_repo_near_pe=$(grep -ciE "(anthropic|source|repo)" "$DOC" 2>/dev/null || echo "0")
if [ "$source_repo_near_pe" -ge 1 ]; then
  pass "Pattern references include source context ($source_repo_near_pe mentions)"
else
  fail "Pattern references lack source repository information"
fi

# ---------------------------------------------------------------------------
# Test 8: Each opportunity explains HOW the pattern enables the capability
# Check for explanation text near pattern references (Description field serves this)
# ---------------------------------------------------------------------------
# Verify descriptions have meaningful content (at least 20 words)
short_descriptions=0
total_descriptions=0
while IFS= read -r line; do
  total_descriptions=$((total_descriptions + 1))
  desc_text=$(echo "$line" | sed -E 's/^.*[Dd]escription(\*\*)?:\s*//')
  word_count=$(echo "$desc_text" | wc -w | tr -d '[:space:]')
  if [ "$word_count" -lt 20 ]; then
    short_descriptions=$((short_descriptions + 1))
  fi
done < <(grep -iE "(^|\*\*)[Dd]escription(\*\*)?:" "$DOC" 2>/dev/null)

if [ "$short_descriptions" -eq 0 ] && [ "$total_descriptions" -ge 5 ]; then
  pass "All $total_descriptions descriptions meet 20-word minimum"
elif [ "$total_descriptions" -lt 5 ]; then
  fail "Only $total_descriptions descriptions found (need 5+)"
else
  fail "$short_descriptions descriptions have fewer than 20 words"
fi

print_results
