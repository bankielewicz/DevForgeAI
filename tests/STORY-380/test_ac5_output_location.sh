#!/usr/bin/env bash
# STORY-380 AC#5: Research Output Stored at Correct Location
# Validates the document exists at the expected path, is readable,
# and has structured section headers.
#
# Expected: FAIL (document does not exist yet - TDD Red phase)

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

# Test 3: File is valid Markdown (has at least one h1 or h2 header)
header_count=$(grep -cE "^#{1,2} " "$DOC" 2>/dev/null || echo "0")
if [ "$header_count" -ge 1 ]; then
  pass "Document has section headers ($header_count found)"
else
  fail "Document has no section headers"
fi

# Test 4: File is in the research directory (not elsewhere)
if echo "$DOC" | grep -q "devforgeai/specs/research/"; then
  pass "Document is in devforgeai/specs/research/ directory"
else
  fail "Document is not in the expected directory"
fi

# Test 5: No secrets or credentials in document (NFR-004)
# Check for actual secret patterns (key assignments, not general text mentions)
secret_count=$(grep -cE "(api_key|password|token|secret|credential)\s*[=:]\s*['\"]" "$DOC" 2>/dev/null | tr -d '\n' || echo "0")
secret_count=${secret_count:-0}
if [ "$secret_count" -eq 0 ]; then
  pass "No secrets or credentials found in document"
else
  fail "$secret_count potential secret/credential patterns found"
fi

# Test 6: Valid Markdown - no unclosed code fences (NFR-002)
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
