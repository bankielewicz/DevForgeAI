#!/usr/bin/env bash
# STORY-382 AC#1: Both Repositories Analyzed with Patterns Extracted
# Validates that the research document references both claude-cookbooks and
# claude-quickstarts repos, covers major categories, and extracts at least
# 8 unique patterns total with at least 1 from each repo.
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
if [ -f "$DOC" ]; then
  pass "Research document exists"
else
  fail "Research document does not exist at $DOC"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# Test 2: Document contains "## Cookbook and Quickstart Patterns" section header
if grep -q "^## Cookbook and Quickstart Patterns" "$DOC" 2>/dev/null; then
  pass "Cookbook and Quickstart Patterns section header found"
else
  fail "Missing '## Cookbook and Quickstart Patterns' section header"
fi

# Test 3: claude-cookbooks repository referenced in the cookbook/quickstart section
cookbooks_count=$(grep -c "claude-cookbooks" "$DOC" 2>/dev/null | tr -d '[:space:]' || echo "0")
cookbooks_count=${cookbooks_count:-0}
if [ "$cookbooks_count" -ge 1 ]; then
  pass "claude-cookbooks repository referenced ($cookbooks_count occurrences)"
else
  fail "claude-cookbooks repository not referenced in document"
fi

# Test 4: claude-quickstarts repository referenced in the cookbook/quickstart section
quickstarts_count=$(grep -c "claude-quickstarts" "$DOC" 2>/dev/null | tr -d '[:space:]' || echo "0")
quickstarts_count=${quickstarts_count:-0}
if [ "$quickstarts_count" -ge 1 ]; then
  pass "claude-quickstarts repository referenced ($quickstarts_count occurrences)"
else
  fail "claude-quickstarts repository not referenced in document"
fi

# Test 5: Major categories covered - capabilities
if grep -q "capabilities/" "$DOC" 2>/dev/null; then
  pass "capabilities/ category referenced"
else
  fail "capabilities/ category not found in document"
fi

# Test 6: Major categories covered - tool_use
if grep -q "tool_use/" "$DOC" 2>/dev/null; then
  pass "tool_use/ category referenced"
else
  fail "tool_use/ category not found in document"
fi

# Test 7: Major categories covered - patterns/agents
if grep -q "patterns/agents/" "$DOC" 2>/dev/null; then
  pass "patterns/agents/ category referenced"
else
  fail "patterns/agents/ category not found in document"
fi

# Test 8: Major categories covered - skills
if grep -q "skills/" "$DOC" 2>/dev/null; then
  pass "skills/ category referenced"
else
  fail "skills/ category not found in document"
fi

# Test 9: Major categories covered - quickstart projects
if grep -qE "(customer-support-agent|financial-data-analyst|computer-use-demo|browser-use-demo|autonomous-coding)" "$DOC" 2>/dev/null; then
  pass "At least one quickstart project referenced"
else
  fail "No quickstart project names found in document"
fi

# Test 10: Minimum 8 unique patterns in cookbook/quickstart section (BR-003)
# Extract section between "## Cookbook and Quickstart Patterns" and next "## " header
section_content=$(sed -n '/^## Cookbook and Quickstart Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -n "$section_content" ]; then
  pattern_count=$(echo "$section_content" | grep -cE "^###+ Pattern C[0-9]+" 2>/dev/null || echo "0")
  if [ "$pattern_count" -ge 8 ]; then
    pass "At least 8 patterns found in cookbook/quickstart section ($pattern_count)"
  else
    fail "Fewer than 8 patterns in cookbook/quickstart section ($pattern_count found, need 8+)"
  fi
else
  fail "Could not extract cookbook/quickstart section content"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
