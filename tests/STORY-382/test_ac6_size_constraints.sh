#!/usr/bin/env bash
# STORY-382 AC#6: Document Remains Within Size Constraints
# Validates the total document is under 2,000 lines and the cookbook/quickstart
# section alone does not exceed 500 lines. Also checks pattern entries are
# self-contained and parseable via Grep.
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

# Test 2: Total document is under 2,000 lines
total_lines=$(wc -l < "$DOC" 2>/dev/null || echo "0")
if [ "$total_lines" -lt 2000 ]; then
  pass "Total document is under 2,000 lines ($total_lines lines)"
else
  fail "Total document exceeds 2,000 lines ($total_lines lines)"
fi

# Test 3: Cookbook/quickstart section exists
if ! grep -q "^## Cookbook and Quickstart Patterns" "$DOC" 2>/dev/null; then
  fail "Cookbook and Quickstart Patterns section not found - cannot measure size"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Cookbook and Quickstart Patterns section exists"

# Test 4: Cookbook/quickstart section is under 500 lines (BR-004)
section_lines=$(sed -n '/^## Cookbook and Quickstart Patterns$/,/^## [^#]/p' "$DOC" 2>/dev/null | wc -l || echo "0")
# If section is the last in the document, try alternative extraction
if [ "$section_lines" -le 1 ]; then
  section_lines=$(sed -n '/^## Cookbook and Quickstart Patterns$/,$p' "$DOC" 2>/dev/null | wc -l || echo "0")
fi

if [ "$section_lines" -le 500 ]; then
  pass "Cookbook/quickstart section is under 500 lines ($section_lines lines)"
else
  fail "Cookbook/quickstart section exceeds 500 lines ($section_lines lines, max 500)"
fi

# Test 5: Section has substantial content (not a stub)
if [ "$section_lines" -ge 50 ]; then
  pass "Section has substantial content ($section_lines lines)"
else
  fail "Section appears too short ($section_lines lines, expected at least 50)"
fi

# Test 6: Grep parseability - patterns findable via Applicability search (NFR-003)
section_content=$(sed -n '/^## Cookbook and Quickstart Patterns$/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$section_content" ]; then
  section_content=$(sed -n '/^## Cookbook and Quickstart Patterns$/,$p' "$DOC" 2>/dev/null)
fi

grep_result=$(echo "$section_content" | grep -cE "\*\*Applicability\*\*:" 2>/dev/null || true)
grep_result=${grep_result:-0}
if [ "$grep_result" -ge 1 ]; then
  pass "Patterns parseable via Grep for Applicability ($grep_result matches)"
else
  fail "No Applicability entries found via Grep in cookbook/quickstart section"
fi

# Test 7: Pattern entries are self-contained (each has name + description)
pattern_count=$(echo "$section_content" | grep -cE "^###+ Pattern C[0-9]+" 2>/dev/null || echo "0")
desc_count=$(echo "$section_content" | grep -cE "^\*\*Description\*\*:" 2>/dev/null || echo "0")

if [ "$pattern_count" -gt 0 ] && [ "$desc_count" -ge "$pattern_count" ]; then
  pass "All pattern entries are self-contained ($pattern_count patterns, $desc_count descriptions)"
else
  fail "Not all pattern entries have descriptions ($desc_count descriptions for $pattern_count patterns)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
