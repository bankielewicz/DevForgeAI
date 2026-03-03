#!/usr/bin/env bash
# STORY-380 AC#1: All 5 Courses Analyzed with Patterns Extracted
# Validates that the research document references all 5 Anthropic courses
# and extracts at least 1 pattern from each.
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
if [ -f "$DOC" ]; then
  pass "Research document exists"
else
  fail "Research document does not exist at $DOC"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# Test 2-6: Each of the 5 courses is referenced with at least 1 pattern
COURSES=(
  "anthropic_api_fundamentals"
  "prompt_engineering_interactive_tutorial"
  "real_world_prompting"
  "prompt_evaluations"
  "tool_use"
)

for course in "${COURSES[@]}"; do
  count=$(grep -c "$course" "$DOC" 2>/dev/null || echo "0")
  if [ "$count" -ge 1 ]; then
    pass "Course '$course' referenced in document ($count occurrences)"
  else
    fail "Course '$course' not found in document"
  fi
done

# Test 7: At least 5 distinct course sections (one per course)
section_count=0
for course in "${COURSES[@]}"; do
  if grep -q "$course" "$DOC" 2>/dev/null; then
    section_count=$((section_count + 1))
  fi
done

if [ "$section_count" -ge 5 ]; then
  pass "All 5 courses have entries ($section_count found)"
else
  fail "Not all 5 courses represented ($section_count of 5 found)"
fi

# Test 8: Minimum 10 patterns total (BR-003)
# Patterns are marked as "#### Pattern N:" in the document
pattern_count=$(grep -c "^#### Pattern [0-9]" "$DOC" 2>/dev/null || echo "0")
if [ "$pattern_count" -ge 10 ]; then
  pass "At least 10 patterns found ($pattern_count)"
else
  fail "Fewer than 10 patterns ($pattern_count found, need 10+)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
