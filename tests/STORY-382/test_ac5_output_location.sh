#!/usr/bin/env bash
# STORY-382 AC#5: Research Output Appended to Correct Location Without Corrupting Existing Sections
# Validates the cookbook/quickstart section is written to the correct file,
# existing STORY-380/381 sections are not corrupted, and section is distinct.
#
# Expected: FAIL (cookbook/quickstart section does not exist yet - TDD Red phase)

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
DOC="$PROJECT_ROOT/devforgeai/specs/research/prompt-engineering-patterns.md"

PASS=0
FAIL=0

fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }
pass() { echo "PASS: $1"; PASS=$((PASS + 1)); }

# Test 1: File exists at the specified path
if [ -f "$DOC" ]; then
  pass "Document exists at devforgeai/specs/research/prompt-engineering-patterns.md"
else
  fail "Document does not exist at devforgeai/specs/research/prompt-engineering-patterns.md"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# Test 2: File is non-empty
if [ -s "$DOC" ]; then
  pass "Document is non-empty"
else
  fail "Document is empty"
fi

# Test 3: Cookbook and Quickstart section exists
if grep -q "^## Cookbook and Quickstart Patterns" "$DOC" 2>/dev/null; then
  pass "Cookbook and Quickstart Patterns section found"
else
  fail "Cookbook and Quickstart Patterns section not found"
fi

# Test 4: Document has a header (h1 title)
if grep -q "^# " "$DOC" 2>/dev/null; then
  pass "Document has h1 title header"
else
  fail "Document missing h1 title header"
fi

# Test 5: Existing Course Patterns section not corrupted (STORY-380)
# Check that the Pattern Catalog section (from STORY-380) still has content
if grep -q "^## Pattern Catalog" "$DOC" 2>/dev/null; then
  # Count course patterns in the Pattern Catalog section
  catalog_patterns=$(sed -n '/^## Pattern Catalog/,/^## [^#]/p' "$DOC" 2>/dev/null | grep -c "^#### Pattern [0-9]" || echo "0")
  if [ "$catalog_patterns" -ge 10 ]; then
    pass "STORY-380 Course Patterns section intact ($catalog_patterns patterns preserved)"
  else
    fail "STORY-380 Course Patterns section may be corrupted ($catalog_patterns patterns, expected 10+)"
  fi
else
  # If STORY-380 has not run yet, this is acceptable (soft dependency)
  pass "STORY-380 section check skipped (Pattern Catalog not found - soft dependency)"
fi

# Test 6: Existing Tutorial Patterns section not corrupted (STORY-381)
if grep -q "^## Tutorial Patterns" "$DOC" 2>/dev/null; then
  # Check that tutorial section still has content
  tutorial_line_count=$(sed -n '/^## Tutorial Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | wc -l || echo "0")
  if [ "$tutorial_line_count" -ge 10 ]; then
    pass "STORY-381 Tutorial Patterns section intact ($tutorial_line_count lines preserved)"
  else
    fail "STORY-381 Tutorial Patterns section may be corrupted ($tutorial_line_count lines, expected 10+)"
  fi
else
  # If STORY-381 has not run yet, this is acceptable (soft dependency)
  pass "STORY-381 section check skipped (Tutorial Patterns not found - soft dependency)"
fi

# Test 7: No secrets or credentials in document (NFR-004)
secret_count=$(grep -cE "(api_key|password|token|secret|credential)\s*[=:]\s*['\"]" "$DOC" 2>/dev/null | tr -d '[:space:]' || echo "0")
secret_count=${secret_count:-0}
if [ "$secret_count" -eq 0 ]; then
  pass "No secrets or credentials found in document"
else
  fail "$secret_count potential secret/credential patterns found"
fi

# Test 8: Valid Markdown - no unclosed code fences (NFR-002)
open_fences=$(grep -c '```' "$DOC" 2>/dev/null || echo "0")
open_fences=${open_fences:-0}
remainder=$((open_fences % 2))
if [ "$remainder" -eq 0 ]; then
  pass "All code fences are properly closed ($open_fences fence markers, all paired)"
else
  fail "Unclosed code fences detected ($open_fences fence markers, odd count)"
fi

# Test 9: File is in the research directory (not elsewhere)
if echo "$DOC" | grep -q "devforgeai/specs/research/"; then
  pass "Document is in devforgeai/specs/research/ directory"
else
  fail "Document is not in the expected directory"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
