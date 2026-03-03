#!/usr/bin/env bash
# STORY-382 AC#3: Findings Documented in Structured Markdown Format
# Validates the cookbook/quickstart section uses a structured entry format with
# all 5 required fields: pattern name, source, description, applicability, recommendation.
# Section header must be "## Cookbook and Quickstart Patterns" (distinct from Course/Tutorial).
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
if [ ! -f "$DOC" ]; then
  fail "Research document does not exist at $DOC"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Research document exists"

# Test 2: Section header is exactly "## Cookbook and Quickstart Patterns"
if grep -q "^## Cookbook and Quickstart Patterns" "$DOC" 2>/dev/null; then
  pass "Section header '## Cookbook and Quickstart Patterns' found"
else
  fail "Section header '## Cookbook and Quickstart Patterns' not found"
fi

# Test 3: Section is distinct from "## Course Patterns" (STORY-380)
# The document should have BOTH sections if STORY-380 ran
course_section=$(grep -c "^## .*Course\|^## Pattern Catalog" "$DOC" 2>/dev/null | tr -d '[:space:]' || echo "0")
course_section=${course_section:-0}
cookbook_section=$(grep -c "^## Cookbook and Quickstart Patterns" "$DOC" 2>/dev/null | tr -d '[:space:]' || echo "0")
cookbook_section=${cookbook_section:-0}
if [ "$cookbook_section" -ge 1 ]; then
  pass "Cookbook section is distinct from course section"
else
  fail "Cookbook section not found as distinct section"
fi

# Test 4: Section is distinct from "## Tutorial Patterns" (STORY-381)
tutorial_section=$(grep -c "^## Tutorial Patterns" "$DOC" 2>/dev/null | tr -d '[:space:]' || echo "0")
tutorial_section=${tutorial_section:-0}
if [ "$cookbook_section" -ge 1 ]; then
  pass "Cookbook section is distinct from tutorial section"
else
  fail "Cookbook section may overlap with tutorial section"
fi

# Extract cookbook/quickstart section content
section_content=$(sed -n '/^## Cookbook and Quickstart Patterns$/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$section_content" ]; then
  section_content=$(sed -n '/^## Cookbook and Quickstart Patterns$/,$p' "$DOC" 2>/dev/null)
fi

if [ -z "$section_content" ]; then
  fail "Could not extract cookbook/quickstart section content"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# Count pattern entries
pattern_count=$(echo "$section_content" | grep -cE "^###+ Pattern C[0-9]+" 2>/dev/null || echo "0")

# Test 5: Each pattern has Source field
source_count=$(echo "$section_content" | grep -cE "^\*\*Source\*\*:" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$source_count" -ge "$pattern_count" ]; then
  pass "All patterns have Source field ($source_count sources for $pattern_count patterns)"
else
  fail "Source field count ($source_count) < pattern count ($pattern_count)"
fi

# Test 6: Each pattern has Description field
desc_count=$(echo "$section_content" | grep -cE "^\*\*Description\*\*:" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$desc_count" -ge "$pattern_count" ]; then
  pass "All patterns have Description field ($desc_count for $pattern_count patterns)"
else
  fail "Description field count ($desc_count) < pattern count ($pattern_count)"
fi

# Test 7: Each pattern has Applicability field
rating_count=$(echo "$section_content" | grep -cE "^\*\*Applicability\*\*:" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$rating_count" -ge "$pattern_count" ]; then
  pass "All patterns have Applicability field ($rating_count for $pattern_count patterns)"
else
  fail "Applicability field count ($rating_count) < pattern count ($pattern_count)"
fi

# Test 8: Each pattern has DevForgeAI Recommendation field
rec_count=$(echo "$section_content" | grep -cE "^\*\*DevForgeAI Recommendation\*\*:" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$rec_count" -ge "$pattern_count" ]; then
  pass "All patterns have DevForgeAI Recommendation field ($rec_count for $pattern_count patterns)"
else
  fail "Recommendation field count ($rec_count) < pattern count ($pattern_count)"
fi

# Test 9: No duplicate pattern names within cookbook/quickstart section (BR-002)
duplicates=$(echo "$section_content" | grep -E "^###+ Pattern C[0-9]+" 2>/dev/null | sort | uniq -d | wc -l || echo "0")
if [ "$duplicates" -eq 0 ]; then
  pass "No duplicate pattern names in cookbook/quickstart section"
else
  fail "$duplicates duplicate pattern names found"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
