#!/usr/bin/env bash
# STORY-381 AC#1: All 9 Chapters Analyzed with Patterns Extracted
# Validates the research document contains patterns from each of the 9
# interactive tutorial chapters with required fields: pattern name, source
# chapter, description (2-4 sentences), and before/after prompt example.
#
# Expected: FAIL (document does not exist yet - TDD Red phase)

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
DOC="$PROJECT_ROOT/devforgeai/specs/research/prompt-engineering-patterns.md"

PASS=0
FAIL=0

fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }
pass() { echo "PASS: $1"; PASS=$((PASS + 1)); }

# Helper: count grep matches in a variable, returns clean integer
count_in_var() {
  local content="$1"
  local pattern="$2"
  local flags="${3:--c}"
  local result
  result=$(printf '%s\n' "$content" | { grep $flags "$pattern" 2>/dev/null || true; })
  result=$(echo "$result" | tr -d '[:space:]')
  [ -z "$result" ] && result=0
  echo "$result"
}

# Test 1: Document exists
if [ -f "$DOC" ]; then
  pass "Research document exists"
else
  fail "Research document does not exist at $DOC"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# Test 2: Tutorial Patterns section exists (distinct from Course Patterns)
if grep -q "^## Tutorial Patterns" "$DOC" 2>/dev/null; then
  pass "Tutorial Patterns section header found"
else
  fail "Tutorial Patterns section header not found (expected '## Tutorial Patterns')"
fi

# Test 3-11: Each of the 9 chapters referenced
CHAPTERS=(
  "Chapter 01|Chapter 1[^0-9]"
  "Chapter 02|Chapter 2[^0-9]"
  "Chapter 03|Chapter 3[^0-9]"
  "Chapter 04|Chapter 4[^0-9]"
  "Chapter 05|Chapter 5[^0-9]"
  "Chapter 06|Chapter 6[^0-9]"
  "Chapter 07|Chapter 7[^0-9]"
  "Chapter 08|Chapter 8[^0-9]"
  "Chapter 09|Chapter 9"
)

CHAPTER_NAMES=(
  "Chapter 01 (Basic Prompt Structure)"
  "Chapter 02 (Being Clear and Direct)"
  "Chapter 03 (Assigning Roles)"
  "Chapter 04 (Separating Data from Instructions)"
  "Chapter 05 (Formatting Output)"
  "Chapter 06 (Chain of Thought)"
  "Chapter 07 (Few-Shot Examples)"
  "Chapter 08 (Avoiding Hallucinations)"
  "Chapter 09 (Complex Prompts)"
)

# Extract Tutorial Patterns section content for chapter searching
tutorial_section=$(sed -n '/^## Tutorial Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1 || echo "")
if [ -z "$tutorial_section" ]; then
  tutorial_section=$(sed -n '/^## Tutorial Patterns/,$p' "$DOC" 2>/dev/null || echo "")
fi

for i in "${!CHAPTERS[@]}"; do
  chapter_pattern="${CHAPTERS[$i]}"
  chapter_name="${CHAPTER_NAMES[$i]}"
  if printf '%s\n' "$tutorial_section" | grep -qE "$chapter_pattern" 2>/dev/null; then
    pass "$chapter_name referenced in Tutorial Patterns section"
  else
    fail "$chapter_name not found in Tutorial Patterns section"
  fi
done

# Test 12: Minimum 9 patterns total (at least 1 per chapter)
tutorial_pattern_count=$(count_in_var "$tutorial_section" "^#### " "-c")
if [ "$tutorial_pattern_count" -ge 9 ]; then
  pass "At least 9 tutorial patterns found ($tutorial_pattern_count)"
else
  fail "Fewer than 9 tutorial patterns ($tutorial_pattern_count found, need 9+)"
fi

# Test 13: Each pattern has a description (2-4 sentences)
desc_count=$(count_in_var "$tutorial_section" '^\*\*Description\*\*:' "-cE")
if [ "$desc_count" -ge 9 ]; then
  pass "At least 9 pattern descriptions found ($desc_count)"
else
  fail "Fewer than 9 descriptions ($desc_count found, need 9+)"
fi

# Test 14: Each pattern has a before/after example
before_count=$(count_in_var "$tutorial_section" "before\|bad example\|without" "-ci")
after_count=$(count_in_var "$tutorial_section" "after\|good example\|improved\|with pattern" "-ci")
if [ "$before_count" -ge 9 ] && [ "$after_count" -ge 9 ]; then
  pass "Before/after examples found (before: $before_count, after: $after_count)"
else
  fail "Insufficient before/after examples (before: $before_count, after: $after_count, need 9+ each)"
fi

# Test 15: No exercise placeholder text (BR-002)
placeholder_count=$(grep -c "\[Replace this text\]" "$DOC" 2>/dev/null || echo "0")
placeholder_count=$(echo "$placeholder_count" | tr -d '[:space:]')
if [ "$placeholder_count" -eq 0 ]; then
  pass "No exercise placeholder text found"
else
  fail "$placeholder_count exercise placeholder occurrences found"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
