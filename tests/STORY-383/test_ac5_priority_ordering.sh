#!/usr/bin/env bash
# STORY-383 AC#5: P1 Repos Analyzed Before P2 Repos
# Validates that P1 repos (claude-code-action, claude-code-security-review,
# claude-plugins-official, claude-constitution) appear before P2 repos
# (healthcare, life-sciences, original_performance_takehome, beam) in the document.
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

# Test 3: P1 subsection header exists (e.g., "### P1: Dev Tool Patterns")
if grep -qE "^### P1:" "$DOC" 2>/dev/null; then
  pass "P1 subsection header found"
else
  fail "P1 subsection header not found (expected '### P1: ...')"
fi

# Test 4: P2 subsection header exists (e.g., "### P2: Domain-Specific Patterns")
if grep -qE "^### P2:" "$DOC" 2>/dev/null; then
  pass "P2 subsection header found"
else
  fail "P2 subsection header not found (expected '### P2: ...')"
fi

# Test 5: P1 subsection appears before P2 subsection (line number comparison - BR-002)
p1_line=$(grep -nE "^### P1:" "$DOC" 2>/dev/null | head -1 | cut -d: -f1 || echo "0")
p2_line=$(grep -nE "^### P2:" "$DOC" 2>/dev/null | head -1 | cut -d: -f1 || echo "0")

if [ "$p1_line" -gt 0 ] && [ "$p2_line" -gt 0 ] && [ "$p1_line" -lt "$p2_line" ]; then
  pass "P1 subsection (line $p1_line) appears before P2 subsection (line $p2_line)"
else
  fail "P1 subsection (line $p1_line) does NOT appear before P2 subsection (line $p2_line)"
fi

# Test 6: P1 repos (all 4) appear in P1 subsection (between P1 header and P2 header)
P1_REPOS=(
  "claude-code-action"
  "claude-code-security-review"
  "claude-plugins-official"
  "claude-constitution"
)

# Extract P1 section content (between P1 and P2 headers)
p1_section=$(sed -n '/^### P1:/,/^### P2:/p' "$DOC" 2>/dev/null | head -n -1)

p1_repos_found=0
for repo in "${P1_REPOS[@]}"; do
  if echo "$p1_section" | grep -q "$repo" 2>/dev/null; then
    p1_repos_found=$((p1_repos_found + 1))
  else
    fail "P1 repo '$repo' not found in P1 subsection"
  fi
done

if [ "$p1_repos_found" -ge 4 ]; then
  pass "All 4 P1 repos found in P1 subsection"
fi

# Test 7: P2 repos (all 4) appear in P2 subsection (after P2 header)
P2_REPOS=(
  "healthcare"
  "life-sciences"
  "original_performance_takehome"
  "beam"
)

# Extract P2 section content (from P2 header to next h2 or EOF)
p2_section=$(sed -n '/^### P2:/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$p2_section" ]; then
  p2_section=$(sed -n '/^### P2:/,$p' "$DOC" 2>/dev/null)
fi

p2_repos_found=0
for repo in "${P2_REPOS[@]}"; do
  if echo "$p2_section" | grep -q "$repo" 2>/dev/null; then
    p2_repos_found=$((p2_repos_found + 1))
  else
    fail "P2 repo '$repo' not found in P2 subsection"
  fi
done

if [ "$p2_repos_found" -ge 4 ]; then
  pass "All 4 P2 repos found in P2 subsection"
fi

# Test 8: P1 patterns appear before P2 patterns (pattern ordering within Dev Tools section)
# Since Tests 3-7 validate P1/P2 subsection structure and content,
# Test 8 validates the pattern headers (#### Pattern D) appear in P1 before P2 order
dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$dev_tools_section" ]; then
  dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,$p' "$DOC" 2>/dev/null)
fi

# Check that P1 subsection header line < P2 subsection header line (already validated in Test 5)
# This test validates that D1-D7 patterns appear before D8-D14 patterns
first_d1=$(echo "$dev_tools_section" | grep -n "#### Pattern D1:" 2>/dev/null | head -1 | cut -d: -f1 || echo "0")
first_d8=$(echo "$dev_tools_section" | grep -n "#### Pattern D8:" 2>/dev/null | head -1 | cut -d: -f1 || echo "0")

if [ "$first_d1" -gt 0 ] && [ "$first_d8" -gt 0 ] && [ "$first_d1" -lt "$first_d8" ]; then
  pass "P1 patterns (D1-D7) appear before P2 patterns (D8-D14) - D1 at line $first_d1, D8 at line $first_d8"
else
  fail "P1 patterns do not appear before P2 patterns (D1 at line $first_d1, D8 at line $first_d8)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
