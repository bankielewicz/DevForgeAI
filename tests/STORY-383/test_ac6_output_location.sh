#!/usr/bin/env bash
# STORY-383 AC#6: Research Output Appended to Shared Document at Correct Location
# Validates the Dev Tools section is appended without overwriting Features 1-3
# content. Existing sections are preserved intact.
#
# Expected: FAIL (Dev Tools section does not exist yet - TDD Red phase)

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

# Test 3: Dev Tools and Domain Patterns section exists (Feature 4 content added)
if grep -q "^## Dev Tools and Domain Patterns" "$DOC" 2>/dev/null; then
  pass "Dev Tools and Domain Patterns section found"
else
  fail "Dev Tools and Domain Patterns section not found (Feature 4 not appended)"
fi

# Test 4: Existing Features 1-3 section headers still present (BR-007)
# Feature 1 (STORY-380): Pattern Catalog or similar
feature1_preserved=false
if grep -qE "^## (Foundational Course Patterns|Pattern Catalog|Prompt Engineering Fundamentals)" "$DOC" 2>/dev/null; then
  feature1_preserved=true
  pass "Feature 1 section header preserved"
else
  # If document was created by STORY-383 first (Features 1-3 not yet written),
  # check for placeholder notes
  if grep -qi "Feature 1\|Features 1-3" "$DOC" 2>/dev/null; then
    feature1_preserved=true
    pass "Feature 1 placeholder notes present"
  else
    fail "Feature 1 section header or placeholder not found (may have been overwritten)"
  fi
fi

# Test 5: Document has at least one h1 or h2 header before Dev Tools section
dev_tools_line=$(grep -n "^## Dev Tools and Domain Patterns" "$DOC" 2>/dev/null | head -1 | cut -d: -f1)
dev_tools_line=${dev_tools_line:-0}
if [ "$dev_tools_line" -gt 0 ]; then
  headers_before=$(head -n "$dev_tools_line" "$DOC" 2>/dev/null | grep -c "^#" | tr -d '[:space:]' || echo "0")
  headers_before=${headers_before:-0}
  if [ "$headers_before" -ge 2 ]; then
    pass "Document has headers before Dev Tools section ($headers_before headers)"
  else
    fail "Too few headers before Dev Tools section ($headers_before found, expected 2+)"
  fi
else
  fail "Cannot check headers before Dev Tools section (section not found)"
fi

# Test 6: File is in the research directory (not elsewhere)
if echo "$DOC" | grep -q "devforgeai/specs/research/"; then
  pass "Document is in devforgeai/specs/research/ directory"
else
  fail "Document is not in the expected directory"
fi

# Test 7: No secrets or credentials in document (NFR-004)
secret_count=$(grep -cE "(api_key|password|token|secret|credential)\s*[=:]\s*['\"]" "$DOC" 2>/dev/null | tr -d '\n' || echo "0")
secret_count=${secret_count:-0}
if [ "$secret_count" -eq 0 ]; then
  pass "No secrets or credentials found in document"
else
  fail "$secret_count potential secret/credential patterns found"
fi

# Test 8: Valid Markdown - no unclosed code fences (NFR-002)
open_fences=$(grep -c '```' "$DOC" 2>/dev/null | tr -d '\n' || echo "0")
open_fences=${open_fences:-0}
remainder=$((open_fences % 2))
if [ "$remainder" -eq 0 ]; then
  pass "All code fences are properly closed ($open_fences fence markers, all paired)"
else
  fail "Unclosed code fences detected ($open_fences fence markers, odd count)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
