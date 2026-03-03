#!/usr/bin/env bash
# STORY-383 AC#2: Each Pattern Has DevForgeAI Applicability Rating with Agent/Skill Mapping
# Validates every pattern entry in the Dev Tools section has exactly one valid
# rating (High/Medium/Low/N/A) with rationale and an agent/skill mapping field.
#
# Expected: FAIL (Dev Tools section does not exist yet - TDD Red phase)

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

# Test 2: Dev Tools section exists
if ! grep -q "^## Dev Tools and Domain Patterns" "$DOC" 2>/dev/null; then
  fail "Dev Tools and Domain Patterns section not found"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Dev Tools and Domain Patterns section found"

# Extract Dev Tools section content
dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$dev_tools_section" ]; then
  dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,$p' "$DOC" 2>/dev/null)
fi

# Test 3: Every pattern has an Applicability line with valid rating
pattern_count=$(echo "$dev_tools_section" | grep -c "^#### Pattern D[0-9]" 2>/dev/null || echo "0")
rating_count=$(echo "$dev_tools_section" | grep -cE "^\*\*Applicability\*\*:.*(High|Medium|Low|N/A)" 2>/dev/null || echo "0")

if [ "$pattern_count" -gt 0 ] && [ "$rating_count" -ge "$pattern_count" ]; then
  pass "All $pattern_count patterns have applicability ratings ($rating_count ratings found)"
else
  fail "Rating count ($rating_count) does not match pattern count ($pattern_count)"
fi

# Test 4: No invalid rating values (only High, Medium, Low, N/A allowed - BR-001)
invalid_ratings=$(echo "$dev_tools_section" | grep -E "^\*\*Applicability\*\*:" 2>/dev/null | grep -cvE "(High|Medium|Low|N/A)" | tr -d '\n' || echo "0")
invalid_ratings=${invalid_ratings:-0}
if [ "$invalid_ratings" -eq 0 ]; then
  pass "No invalid rating values found"
else
  fail "$invalid_ratings entries have invalid rating values"
fi

# Test 5: Each rating has a Rationale section
rationale_count=$(echo "$dev_tools_section" | grep -c "^\*\*Rationale\*\*:" 2>/dev/null || echo "0")
if [ "$rationale_count" -ge "$pattern_count" ]; then
  pass "All ratings have rationale sections ($rationale_count found)"
else
  fail "Not enough rationale sections ($rationale_count found, need $pattern_count)"
fi

# Test 6: Each pattern has Agent/Skill Mapping field
mapping_count=$(echo "$dev_tools_section" | grep -cE "^\*\*Agent/Skill Mapping\*\*:" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$mapping_count" -ge "$pattern_count" ]; then
  pass "All patterns have Agent/Skill Mapping field ($mapping_count for $pattern_count patterns)"
else
  fail "Agent/Skill Mapping field count ($mapping_count) < pattern count ($pattern_count)"
fi

# Test 7: High/Medium patterns have non-empty agent mapping (not "N/A" or empty)
high_medium_count=$(echo "$dev_tools_section" | grep -cE "^\*\*Applicability\*\*:.*(High|Medium)" 2>/dev/null || echo "0")
# Count agent mappings that reference actual agents (contain a hyphenated agent name)
non_empty_mappings=$(echo "$dev_tools_section" | grep -E "^\*\*Agent/Skill Mapping\*\*:" 2>/dev/null | grep -cE "[a-z]+-[a-z]+" || echo "0")
if [ "$high_medium_count" -eq 0 ] || [ "$non_empty_mappings" -ge "$high_medium_count" ]; then
  pass "High/Medium patterns have specific agent mappings ($non_empty_mappings mappings for $high_medium_count High/Medium patterns)"
else
  fail "Not all High/Medium patterns have specific agent mappings ($non_empty_mappings of $high_medium_count)"
fi

# Test 8: No patterns without any rating (scan pattern by pattern)
patterns_without_rating=0
in_pattern=false
has_rating=false
while IFS= read -r line; do
  if echo "$line" | grep -q "^#### Pattern D[0-9]"; then
    if [ "$in_pattern" = true ] && [ "$has_rating" = false ]; then
      patterns_without_rating=$((patterns_without_rating + 1))
    fi
    in_pattern=true
    has_rating=false
  fi
  if echo "$line" | grep -qE "^\*\*Applicability\*\*:.*(High|Medium|Low|N/A)"; then
    has_rating=true
  fi
done <<< "$dev_tools_section"
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
