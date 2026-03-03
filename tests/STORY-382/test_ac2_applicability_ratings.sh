#!/usr/bin/env bash
# STORY-382 AC#2: Each Pattern Has DevForgeAI Applicability Rating
# Validates every pattern entry in the cookbook/quickstart section has exactly
# one valid rating (High/Medium/Low/N/A) with a rationale.
#
# Expected: FAIL (cookbook/quickstart section does not exist yet - TDD Red phase)

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
DOC="$PROJECT_ROOT/devforgeai/specs/research/prompt-engineering-patterns.md"

PASS=0
FAIL=0

fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }
pass() { echo "PASS: $1"; PASS=$((PASS + 1)); }

# Test 1: Document exists
if [ ! -f "$DOC" ]; then
  fail "Research document does not exist at $DOC"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Research document exists"

# Test 2: Cookbook/quickstart section exists
if ! grep -q "^## Cookbook and Quickstart Patterns" "$DOC" 2>/dev/null; then
  fail "Cookbook and Quickstart Patterns section not found"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Cookbook and Quickstart Patterns section exists"

# Extract the cookbook/quickstart section content
section_content=$(sed -n '/^## Cookbook and Quickstart Patterns$/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$section_content" ]; then
  # If section is the last one in the document, sed won't match the end delimiter
  section_content=$(sed -n '/^## Cookbook and Quickstart Patterns$/,$p' "$DOC" 2>/dev/null)
fi

# Test 3: Every pattern has an Applicability line with valid rating
pattern_count=$(echo "$section_content" | grep -cE "^###+ Pattern C[0-9]+" 2>/dev/null || echo "0")
rating_count=$(echo "$section_content" | grep -cE "^\*\*Applicability\*\*:.*(High|Medium|Low|N/A)" 2>/dev/null || echo "0")

if [ "$pattern_count" -gt 0 ] && [ "$rating_count" -ge "$pattern_count" ]; then
  pass "All $pattern_count patterns have applicability ratings ($rating_count ratings found)"
else
  fail "Rating count ($rating_count) does not match pattern count ($pattern_count)"
fi

# Test 4: No invalid rating values (only High, Medium, Low, N/A allowed)
invalid_ratings=$(echo "$section_content" | grep -E "^\*\*Applicability\*\*:" 2>/dev/null | grep -cvE "(High|Medium|Low|N/A)" 2>/dev/null || true)
invalid_ratings=${invalid_ratings:-0}
if [ "$invalid_ratings" -eq 0 ]; then
  pass "No invalid rating values found"
else
  fail "$invalid_ratings entries have invalid rating values"
fi

# Test 5: Each rating has a Rationale section
rationale_count=$(echo "$section_content" | grep -c "^\*\*Rationale\*\*:" 2>/dev/null || echo "0")
if [ "$rationale_count" -ge "$pattern_count" ]; then
  pass "All ratings have rationale sections ($rationale_count found)"
else
  fail "Not enough rationale sections ($rationale_count found, need $pattern_count)"
fi

# Test 6: No patterns without any rating (BR-001)
patterns_without_rating=0
in_pattern=false
has_rating=false
while IFS= read -r line; do
  if echo "$line" | grep -qE "^#{3,4} Pattern C[0-9]+"; then
    if [ "$in_pattern" = true ] && [ "$has_rating" = false ]; then
      patterns_without_rating=$((patterns_without_rating + 1))
    fi
    in_pattern=true
    has_rating=false
  fi
  if echo "$line" | grep -qE "^\*\*Applicability\*\*:.*(High|Medium|Low|N/A)"; then
    has_rating=true
  fi
done <<< "$section_content"
# Check last pattern
if [ "$in_pattern" = true ] && [ "$has_rating" = false ]; then
  patterns_without_rating=$((patterns_without_rating + 1))
fi

if [ "$patterns_without_rating" -eq 0 ] && [ "$pattern_count" -gt 0 ]; then
  pass "No patterns missing applicability rating"
else
  fail "$patterns_without_rating patterns missing applicability rating"
fi

# Test 7: Claude Code Terminal limitations mentioned in at least one rationale
terminal_mentions=$(echo "$section_content" | grep -ciE "Claude Code Terminal|terminal constraint|terminal limitation" 2>/dev/null || echo "0")
if [ "$terminal_mentions" -ge 1 ]; then
  pass "Claude Code Terminal limitations noted in rationale ($terminal_mentions mentions)"
else
  fail "No Claude Code Terminal limitation notes found in any rationale"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
