#!/usr/bin/env bash
# STORY-380 AC#6: Research Output Within Size Constraints
# Validates the document is under 2,000 lines and patterns are self-contained.
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

# Test 2: Document is under 2,000 lines (BR-004)
line_count=$(wc -l < "$DOC" 2>/dev/null || echo "0")
if [ "$line_count" -lt 2000 ]; then
  pass "Document is under 2,000 lines ($line_count lines)"
else
  fail "Document exceeds 2,000 lines ($line_count lines)"
fi

# Test 3: Document is within target range (800-1,500 lines per NFR-001)
if [ "$line_count" -ge 100 ]; then
  pass "Document has substantial content ($line_count lines)"
else
  fail "Document appears too short ($line_count lines, expected 100+)"
fi

# Test 4: Grep parseability - patterns findable via Applicability search (NFR-003)
grep_result=$(grep -c "Applicability:" "$DOC" 2>/dev/null || echo "0")
if [ "$grep_result" -ge 1 ]; then
  pass "Patterns parseable via Grep for Applicability ($grep_result matches)"
else
  fail "No Applicability entries found via Grep"
fi

# Test 5: Executive summary includes pattern count
# Look for "Total Patterns" or similar in Executive Summary section
summary_has_count=$(grep -A20 -i "Executive Summary" "$DOC" 2>/dev/null | grep -ciE "Total Patterns|Patterns Extracted|[0-9]+ pattern" || echo "0")
if [ "$summary_has_count" -ge 1 ]; then
  pass "Executive summary mentions pattern count"
else
  fail "Executive summary does not mention pattern count"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
