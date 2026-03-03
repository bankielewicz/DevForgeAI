#!/usr/bin/env bash
# STORY-381 AC#4: Patterns Appended Under Tutorial Section with Source References
# Validates patterns are written under "## Tutorial Patterns (Interactive Tutorial)"
# section distinct from "## Course Patterns", each citing Anthropic 1P source.
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
if [ ! -f "$DOC" ]; then
  fail "Research document does not exist at $DOC"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Research document exists"

# Test 2: "## Tutorial Patterns (Interactive Tutorial)" section header exists
if grep -q "^## Tutorial Patterns" "$DOC" 2>/dev/null; then
  pass "Tutorial Patterns section header found"
else
  fail "Tutorial Patterns section header not found"
fi

# Test 3: Tutorial section is distinct from Course Patterns section
tutorial_line=$(grep -n "^## Tutorial Patterns" "$DOC" 2>/dev/null | head -1 | cut -d: -f1 || echo "0")
tutorial_line=$(echo "$tutorial_line" | tr -d '[:space:]')
course_line=$(grep -n "^## Course Patterns" "$DOC" 2>/dev/null | head -1 | cut -d: -f1 || echo "0")
course_line=$(echo "$course_line" | tr -d '[:space:]')

if [ "$tutorial_line" -gt 0 ]; then
  if [ "$course_line" -gt 0 ]; then
    if [ "$tutorial_line" -ne "$course_line" ]; then
      pass "Tutorial and Course Patterns are distinct sections (Tutorial: line $tutorial_line, Course: line $course_line)"
    else
      fail "Tutorial and Course Patterns appear on same line"
    fi
  else
    pass "Tutorial Patterns section exists (Course Patterns section not yet created - STORY-380 dependency)"
  fi
else
  fail "Tutorial Patterns section not found"
fi

# Extract Tutorial Patterns section
tutorial_section=$(sed -n '/^## Tutorial Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1 || echo "")
if [ -z "$tutorial_section" ]; then
  tutorial_section=$(sed -n '/^## Tutorial Patterns/,$p' "$DOC" 2>/dev/null || echo "")
fi

# Test 4: Each pattern cites Anthropic 1P source path
tutorial_pattern_count=$(count_in_var "$tutorial_section" "^#### " "-c")
anthro_source_count=$(count_in_var "$tutorial_section" "Anthropic 1P" "-c")

if [ "$tutorial_pattern_count" -gt 0 ] && [ "$anthro_source_count" -ge "$tutorial_pattern_count" ]; then
  pass "All patterns cite Anthropic 1P source ($anthro_source_count citations for $tutorial_pattern_count patterns)"
else
  fail "Insufficient Anthropic 1P citations ($anthro_source_count for $tutorial_pattern_count patterns)"
fi

# Test 5: Source references include .ipynb notebook filenames
ipynb_count=$(count_in_var "$tutorial_section" '\.ipynb' "-c")
if [ "$ipynb_count" -ge 9 ]; then
  pass "Notebook .ipynb references found ($ipynb_count, need 9+ for all chapters)"
else
  fail "Insufficient .ipynb references ($ipynb_count found, need 9+)"
fi

# Test 6: Source references use correct path prefix
correct_path_count=$(count_in_var "$tutorial_section" "prompt-eng-interactive-tutorial" "-c")
if [ "$correct_path_count" -ge 1 ]; then
  pass "Correct tutorial path prefix found ($correct_path_count references)"
else
  fail "Tutorial path prefix 'prompt-eng-interactive-tutorial' not found in sources"
fi

# Test 7: No AmazonBedrock source references (BR-001)
bedrock_source_count=$(count_in_var "$tutorial_section" "AmazonBedrock" "-ci")
if [ "$bedrock_source_count" -eq 0 ]; then
  pass "No AmazonBedrock source references in Tutorial section"
else
  fail "$bedrock_source_count AmazonBedrock references found (should use Anthropic 1P variant only)"
fi

# Test 8: No duplicate pattern names across entire document (BR-003)
if [ "$tutorial_pattern_count" -gt 0 ]; then
  all_pattern_names=$(grep "^#### " "$DOC" 2>/dev/null | sort || echo "")
  duplicate_count=$(printf '%s\n' "$all_pattern_names" | uniq -d | wc -l || echo "0")
  duplicate_count=$(echo "$duplicate_count" | tr -d '[:space:]')
  if [ "$duplicate_count" -eq 0 ]; then
    pass "No duplicate pattern names across document"
  else
    fail "$duplicate_count duplicate pattern names found across document"
  fi
else
  fail "No tutorial patterns to check for duplicates"
fi

# Test 9: Document under 2000 lines (BR-004)
total_lines=$(wc -l < "$DOC" 2>/dev/null || echo "0")
total_lines=$(echo "$total_lines" | tr -d '[:space:]')
if [ "$total_lines" -lt 2000 ]; then
  pass "Document under 2000 lines ($total_lines lines)"
else
  fail "Document exceeds 2000 lines ($total_lines lines)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
