#!/usr/bin/env bash
# STORY-380 AC#2: Each Pattern Has DevForgeAI Applicability Rating
# Validates every pattern entry has exactly one valid rating (High/Medium/Low/N/A)
# with a 1-2 sentence rationale.
#
# Expected: FAIL (document does not exist yet - TDD Red phase)

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

# Test 2: Every pattern has an Applicability line with valid rating
# Count pattern entries (h4 headers starting with "Pattern N:")
pattern_count=$(grep -c "^#### Pattern [0-9]" "$DOC" 2>/dev/null || echo "0")
rating_count=$(grep -cE "^\*\*Applicability\*\*:.*(High|Medium|Low|N/A)" "$DOC" 2>/dev/null || echo "0")

if [ "$pattern_count" -gt 0 ] && [ "$rating_count" -ge "$pattern_count" ]; then
  pass "All $pattern_count patterns have applicability ratings ($rating_count ratings found)"
else
  fail "Rating count ($rating_count) does not match pattern count ($pattern_count)"
fi

# Test 3: No invalid rating values (only High, Medium, Low, N/A allowed)
invalid_ratings=$(grep -E "^\*\*Applicability\*\*:" "$DOC" 2>/dev/null | grep -cvE "(High|Medium|Low|N/A)" | tr -d '\n' || echo "0")
invalid_ratings=${invalid_ratings:-0}
if [ "$invalid_ratings" -eq 0 ]; then
  pass "No invalid rating values found"
else
  fail "$invalid_ratings entries have invalid rating values"
fi

# Test 4: Each rating has a Rationale section below it
rationale_count=$(grep -c "^\*\*Rationale\*\*:" "$DOC" 2>/dev/null || echo "0")
if [ "$rationale_count" -ge "$pattern_count" ]; then
  pass "All ratings have rationale sections ($rationale_count found)"
else
  fail "Not enough rationale sections ($rationale_count found, need $pattern_count)"
fi

# Test 5: No patterns without any rating (BR-001)
patterns_without_rating=0
in_pattern=false
has_rating=false
while IFS= read -r line; do
  if echo "$line" | grep -q "^#### Pattern [0-9]"; then
    if [ "$in_pattern" = true ] && [ "$has_rating" = false ]; then
      patterns_without_rating=$((patterns_without_rating + 1))
    fi
    in_pattern=true
    has_rating=false
  fi
  if echo "$line" | grep -qE "^\*\*Applicability\*\*:.*(High|Medium|Low|N/A)"; then
    has_rating=true
  fi
done < "$DOC"
# Check last pattern
if [ "$in_pattern" = true ] && [ "$has_rating" = false ]; then
  patterns_without_rating=$((patterns_without_rating + 1))
fi

if [ "$patterns_without_rating" -eq 0 ]; then
  pass "No patterns missing applicability rating"
else
  fail "$patterns_without_rating patterns missing applicability rating"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
