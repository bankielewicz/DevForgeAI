#!/usr/bin/env bash
# STORY-380 AC#3: Findings Documented in Structured Markdown Format
# Validates each pattern entry contains: pattern name, source course,
# description, applicability rating, and DevForgeAI recommendation.
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

# Test 2: Document has Table of Contents
if grep -qi "Table of Contents" "$DOC" 2>/dev/null; then
  pass "Table of Contents section found"
else
  fail "Table of Contents section missing"
fi

# Test 3: Document has Executive Summary
if grep -qi "Executive Summary" "$DOC" 2>/dev/null; then
  pass "Executive Summary section found"
else
  fail "Executive Summary section missing"
fi

# Test 4: Document has Pattern Catalog section
if grep -qi "Pattern Catalog\|## Patterns\|## Pattern" "$DOC" 2>/dev/null; then
  pass "Pattern Catalog section found"
else
  fail "Pattern Catalog section missing"
fi

# Test 5: Each pattern has required 5 fields
# Count patterns (h4 headers starting with "Pattern N:")
pattern_count=$(grep -c "^#### Pattern [0-9]" "$DOC" 2>/dev/null || echo "0")

# Check for Source field (bold format)
source_count=$(grep -cE "^\*\*Source\*\*:" "$DOC" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$source_count" -ge "$pattern_count" ]; then
  pass "All patterns have Source field ($source_count sources for $pattern_count patterns)"
else
  fail "Source field count ($source_count) < pattern count ($pattern_count)"
fi

# Test 6: Each pattern has Description field
desc_count=$(grep -cE "^\*\*Description\*\*:" "$DOC" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$desc_count" -ge "$pattern_count" ]; then
  pass "All patterns have Description field ($desc_count for $pattern_count patterns)"
else
  fail "Description field count ($desc_count) < pattern count ($pattern_count)"
fi

# Test 7: Each pattern has Applicability field
rating_count=$(grep -cE "^\*\*Applicability\*\*:" "$DOC" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$rating_count" -ge "$pattern_count" ]; then
  pass "All patterns have Applicability field ($rating_count for $pattern_count patterns)"
else
  fail "Applicability field count ($rating_count) < pattern count ($pattern_count)"
fi

# Test 8: Each pattern has Recommendation field
rec_count=$(grep -cE "^\*\*DevForgeAI Recommendation\*\*:" "$DOC" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$rec_count" -ge "$pattern_count" ]; then
  pass "All patterns have Recommendation field ($rec_count for $pattern_count patterns)"
else
  fail "Recommendation field count ($rec_count) < pattern count ($pattern_count)"
fi

# Test 9: No duplicate pattern names (BR-002)
duplicates=$(grep "^#### Pattern [0-9]" "$DOC" 2>/dev/null | sort | uniq -d | wc -l || echo "0")
if [ "$duplicates" -eq 0 ]; then
  pass "No duplicate pattern names"
else
  fail "$duplicates duplicate pattern names found"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
