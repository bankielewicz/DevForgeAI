#!/usr/bin/env bash
# STORY-383 AC#7: Combined Document Remains Under 2,000 Lines
# Validates the research document with Features 1-4 content combined
# is under the 2,000-line limit per EPIC-060 constraint.
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

# Test 2: Dev Tools section exists (confirming Feature 4 was added)
if ! grep -q "^## Dev Tools and Domain Patterns" "$DOC" 2>/dev/null; then
  fail "Dev Tools and Domain Patterns section not found (Feature 4 not yet added)"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Dev Tools section present in document"

# Test 3: Document is under 2,000 lines (BR-006)
line_count=$(wc -l < "$DOC" 2>/dev/null || echo "0")
if [ "$line_count" -lt 2000 ]; then
  pass "Document is under 2,000 lines ($line_count lines)"
else
  fail "Document exceeds 2,000 lines ($line_count lines)"
fi

# Test 4: Document has substantial content (not trivially small)
if [ "$line_count" -ge 100 ]; then
  pass "Document has substantial content ($line_count lines)"
else
  fail "Document appears too short ($line_count lines, expected 100+)"
fi

# Test 5: Dev Tools section itself has meaningful content (not just header)
dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$dev_tools_section" ]; then
  dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,$p' "$DOC" 2>/dev/null)
fi
dev_tools_lines=$(echo "$dev_tools_section" | wc -l || echo "0")

if [ "$dev_tools_lines" -ge 30 ]; then
  pass "Dev Tools section has meaningful content ($dev_tools_lines lines)"
else
  fail "Dev Tools section too short ($dev_tools_lines lines, expected 30+)"
fi

# Test 6: Grep parseability - Dev Tools patterns findable via Applicability search (NFR-003)
# Pattern uses **Applicability**: format
grep_result=$(echo "$dev_tools_section" | grep -cE "\*\*Applicability\*\*:" 2>/dev/null | tr -d '\n' || echo "0")
grep_result=${grep_result:-0}
if [ "$grep_result" -ge 1 ]; then
  pass "Dev Tools patterns parseable via Grep for Applicability ($grep_result matches)"
else
  fail "No Applicability entries found via Grep in Dev Tools section"
fi

# Test 7: Loadable in single Read() call (NFR-001) - under 2000 lines
if [ "$line_count" -lt 2000 ]; then
  pass "Document loadable in single Read() call ($line_count lines < 2000 limit)"
else
  fail "Document too large for single Read() call ($line_count lines >= 2000 limit)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
