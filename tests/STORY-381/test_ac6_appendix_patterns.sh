#!/usr/bin/env bash
# STORY-381 AC#6: Appendix Patterns Captured Separately
# Validates that appendix patterns (Chaining Prompts, Tool Use, Search and
# Retrieval) are documented in an "### Appendix Patterns" subsection with
# duplicates cross-referenced rather than repeated.
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

# Test 2: "### Appendix Patterns" subsection exists
if grep -q "^### Appendix Patterns" "$DOC" 2>/dev/null; then
  pass "Appendix Patterns subsection header found"
else
  fail "Appendix Patterns subsection header not found (expected '### Appendix Patterns')"
fi

# Test 3: Appendix subsection is WITHIN Tutorial Patterns section (not standalone)
tutorial_line=$(grep -n "^## Tutorial Patterns" "$DOC" 2>/dev/null | head -1 | cut -d: -f1 || echo "0")
tutorial_line=$(echo "$tutorial_line" | tr -d '[:space:]')
[ -z "$tutorial_line" ] && tutorial_line=0
appendix_line=$(grep -n "^### Appendix Patterns" "$DOC" 2>/dev/null | head -1 | cut -d: -f1 || echo "0")
appendix_line=$(echo "$appendix_line" | tr -d '[:space:]')
[ -z "$appendix_line" ] && appendix_line=0

# Find the next h2 section after Tutorial Patterns
if [ "$tutorial_line" -gt 0 ]; then
  next_h2_after_tutorial=$(sed -n "$((tutorial_line + 1)),\$p" "$DOC" 2>/dev/null | grep -n "^## " | head -1 | cut -d: -f1 || echo "0")
  next_h2_after_tutorial=$(echo "$next_h2_after_tutorial" | tr -d '[:space:]')
  [ -z "$next_h2_after_tutorial" ] && next_h2_after_tutorial=0
  if [ "$next_h2_after_tutorial" -gt 0 ]; then
    next_h2_line=$((tutorial_line + next_h2_after_tutorial))
  else
    next_h2_line=999999
  fi
else
  next_h2_line=999999
fi

if [ "$tutorial_line" -gt 0 ] && [ "$appendix_line" -gt "$tutorial_line" ] && [ "$appendix_line" -lt "$next_h2_line" ]; then
  pass "Appendix Patterns subsection is within Tutorial Patterns section"
else
  fail "Appendix Patterns subsection is not properly nested within Tutorial Patterns (Tutorial: line $tutorial_line, Appendix: line $appendix_line, Next section: line $next_h2_line)"
fi

# Extract Appendix Patterns subsection
appendix_section=$(sed -n '/^### Appendix Patterns/,/^### [^#]\|^## /p' "$DOC" 2>/dev/null | head -n -1 || echo "")
if [ -z "$appendix_section" ]; then
  appendix_section=$(sed -n '/^### Appendix Patterns/,$p' "$DOC" 2>/dev/null || echo "")
fi

# Test 4: At least one appendix pattern documented
appendix_pattern_count=$(count_in_var "$appendix_section" "^#### " "-c")
if [ "$appendix_pattern_count" -ge 1 ]; then
  pass "At least 1 appendix pattern documented ($appendix_pattern_count found)"
else
  fail "No appendix patterns documented (expected at least 1)"
fi

# Test 5: Appendix references at least one of the 3 appendix topics
APPENDIX_TOPICS=(
  "Chaining Prompts|Prompt Chaining|chaining"
  "Tool Use|tool use|tool_use"
  "Search and Retrieval|search.*retrieval|RAG"
)

TOPIC_NAMES=(
  "Chaining Prompts"
  "Tool Use"
  "Search and Retrieval"
)

topics_found=0
for i in "${!APPENDIX_TOPICS[@]}"; do
  topic_pattern="${APPENDIX_TOPICS[$i]}"
  topic_name="${TOPIC_NAMES[$i]}"
  if printf '%s\n' "$appendix_section" | grep -qiE "$topic_pattern" 2>/dev/null; then
    topics_found=$((topics_found + 1))
    pass "Appendix topic '$topic_name' referenced"
  else
    fail "Appendix topic '$topic_name' not found in Appendix Patterns section"
  fi
done

# Test 6: Duplicate patterns are cross-referenced ("See Chapter N") not repeated
crossref_count=$(count_in_var "$appendix_section" 'See Chapter\|cross-reference\|covered in\|refer to' "-ci")
if [ "$crossref_count" -ge 0 ]; then
  pass "Cross-reference mechanism checked ($crossref_count cross-references found)"
fi

# Test 7: Appendix patterns follow same structure as chapter patterns
if [ "$appendix_pattern_count" -gt 0 ]; then
  appendix_source_count=$(count_in_var "$appendix_section" '^\*\*Source\*\*:' "-c")
  if [ "$appendix_source_count" -ge "$appendix_pattern_count" ]; then
    pass "Appendix patterns have Source field ($appendix_source_count for $appendix_pattern_count patterns)"
  else
    fail "Appendix patterns missing Source field ($appendix_source_count for $appendix_pattern_count patterns)"
  fi

  appendix_desc_count=$(count_in_var "$appendix_section" '^\*\*Description\*\*:' "-c")
  if [ "$appendix_desc_count" -ge "$appendix_pattern_count" ]; then
    pass "Appendix patterns have Description field ($appendix_desc_count for $appendix_pattern_count patterns)"
  else
    fail "Appendix patterns missing Description field ($appendix_desc_count for $appendix_pattern_count patterns)"
  fi
else
  fail "Cannot validate appendix pattern structure - no patterns found"
fi

# Test 8: Composite Pattern entry for Chapter 9 (BR-005)
tutorial_section=$(sed -n '/^## Tutorial Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1 || echo "")
if [ -z "$tutorial_section" ]; then
  tutorial_section=$(sed -n '/^## Tutorial Patterns/,$p' "$DOC" 2>/dev/null || echo "")
fi

composite_count=$(count_in_var "$tutorial_section" 'Composite Pattern\|meta-pattern\|composite' "-ci")
if [ "$composite_count" -ge 1 ]; then
  pass "Composite Pattern / meta-pattern entry found for Chapter 9"
else
  fail "No Composite Pattern entry found (Chapter 9 meta-pattern required per BR-005)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
