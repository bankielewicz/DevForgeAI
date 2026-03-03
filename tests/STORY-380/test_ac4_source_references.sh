#!/usr/bin/env bash
# STORY-380 AC#4: Patterns Include Source References
# Validates each pattern cites course name and specific notebook/lesson filename.
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
if [ ! -f "$DOC" ]; then
  fail "Research document does not exist at $DOC"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Research document exists"

# Test 2: Source references include notebook/lesson filenames (.ipynb or .md)
file_ref_count=$(grep -cE "\.(ipynb|md)" "$DOC" 2>/dev/null || echo "0")
if [ "$file_ref_count" -ge 1 ]; then
  pass "Source references include notebook/lesson filenames ($file_ref_count references)"
else
  fail "No notebook/lesson filenames (.ipynb/.md) found in source references"
fi

# Test 3: Each Source line contains a course name
COURSES=(
  "anthropic_api_fundamentals"
  "prompt_engineering_interactive_tutorial"
  "real_world_prompting"
  "prompt_evaluations"
  "tool_use"
)

# Count bold Source lines
source_lines=$(grep -cE "^\*\*Source\*\*:" "$DOC" 2>/dev/null || echo "0")
sources_with_course=0

for course in "${COURSES[@]}"; do
  course_in_source=$(grep -E "^\*\*Source\*\*:" "$DOC" 2>/dev/null | grep -c "$course" || echo "0")
  sources_with_course=$((sources_with_course + course_in_source))
done

if [ "$sources_with_course" -ge "$source_lines" ] && [ "$source_lines" -gt 0 ]; then
  pass "All source lines reference a known course name ($sources_with_course of $source_lines)"
else
  fail "Not all source lines contain a course name ($sources_with_course of $source_lines)"
fi

# Test 4: Pattern Source lines have specific filenames
# Exclude document metadata line (first Source line) - only count patterns (24 total)
pattern_source_lines=$(grep -E "^\*\*Source\*\*:" "$DOC" 2>/dev/null | grep -cE "/(.*)\.(ipynb|md)" || echo "0")
# We expect 24 patterns, allow for some sources citing multiple files
if [ "$pattern_source_lines" -ge 20 ]; then
  pass "Pattern source lines include specific filenames ($pattern_source_lines patterns cite notebooks)"
else
  fail "Not enough source lines include specific filenames ($pattern_source_lines found, need 20+)"
fi

# Test 5: No AmazonBedrock/boto3 references in source lines (BR-005)
bedrock_count=$(grep -ciE "AmazonBedrock|boto3" "$DOC" 2>/dev/null | tr -d '\n' || echo "0")
bedrock_count=${bedrock_count:-0}
if [ "$bedrock_count" -eq 0 ]; then
  pass "No AmazonBedrock/boto3 references in document"
else
  fail "$bedrock_count AmazonBedrock/boto3 references found (should use Anthropic variant)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
