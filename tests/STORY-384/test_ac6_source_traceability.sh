#!/usr/bin/env bash
# STORY-384 AC#6: Source Traceability
# Validates:
#   - Source References section lists all 4 stories (STORY-380, 381, 382, 383)
#   - Each pattern cites at least one source story
#   - Source coverage table with counts per story (all 4 contributing >= 1)
#   - 12 Anthropic repos listed with priority tiers

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "Research document"

# ---------------------------------------------------------------------------
# Test 2: Source References section exists
# ---------------------------------------------------------------------------
assert_section_exists "Source References"

# Extract Source References section
src_ref_section=$(extract_section "Source References")

# ---------------------------------------------------------------------------
# Tests 3-6: Source References lists all 4 source stories
# ---------------------------------------------------------------------------
for story in "STORY-380" "STORY-381" "STORY-382" "STORY-383"; do
  if echo "$src_ref_section" | grep -q "$story" 2>/dev/null; then
    pass "Source References mentions $story"
  else
    fail "Source References missing $story"
  fi
done

# ---------------------------------------------------------------------------
# Test 7: Each pattern cites at least one source story (STORY-38[0-3])
# Check that PE-NNN patterns each have a STORY-38x reference nearby
# ---------------------------------------------------------------------------
patterns_without_source=0
total_patterns=0
in_pattern=false
has_source_story=false

while IFS= read -r line; do
  if echo "$line" | grep -qE "^#{1,4}.*PE-[0-9]{3}:" 2>/dev/null; then
    # Save state of previous pattern
    if [ "$in_pattern" = true ] && [ "$has_source_story" = false ]; then
      patterns_without_source=$((patterns_without_source + 1))
    fi
    in_pattern=true
    has_source_story=false
    total_patterns=$((total_patterns + 1))
  fi
  if [ "$in_pattern" = true ]; then
    if echo "$line" | grep -qE "STORY-38[0-3]" 2>/dev/null; then
      has_source_story=true
    fi
  fi
done < "$DOC"

# Check last pattern
if [ "$in_pattern" = true ] && [ "$has_source_story" = false ]; then
  patterns_without_source=$((patterns_without_source + 1))
fi

if [ "$total_patterns" -eq 0 ]; then
  fail "No PE-NNN patterns found - cannot verify source citations"
elif [ "$patterns_without_source" -eq 0 ]; then
  pass "All $total_patterns patterns cite at least one source story"
else
  fail "$patterns_without_source of $total_patterns patterns lack source story citation"
fi

# ---------------------------------------------------------------------------
# Test 8: Source coverage table exists with counts per story
# (Table should show how many patterns each story contributed)
# ---------------------------------------------------------------------------
has_coverage_table=true
for story in "STORY-380" "STORY-381" "STORY-382" "STORY-383"; do
  if ! echo "$src_ref_section" | grep -qE "\|.*${story}.*\|" 2>/dev/null; then
    has_coverage_table=false
    break
  fi
done

if [ "$has_coverage_table" = true ]; then
  pass "Source coverage table includes all 4 stories"
else
  fail "Source coverage table missing or incomplete (need STORY-380/381/382/383 in table rows)"
fi

# ---------------------------------------------------------------------------
# Test 9: Each story contributes at least 1 pattern (non-zero count in table)
# Check table rows for numeric values > 0
# ---------------------------------------------------------------------------
for story in "STORY-380" "STORY-381" "STORY-382" "STORY-383"; do
  row=$(echo "$src_ref_section" | grep -E "\|.*${story}.*\|" 2>/dev/null)
  if [ -n "$row" ]; then
    # Extract pattern count from row (skip story ID numbers by removing the story reference first)
    count=$(echo "$row" | sed "s/${story}//" | grep -oE "[0-9]+" | head -n 1)
    if [ -n "$count" ] && [ "$count" -ge 1 ]; then
      pass "$story contributes $count patterns"
    else
      fail "$story shows 0 pattern contributions in coverage table"
    fi
  else
    fail "$story not found in coverage table"
  fi
done

# ---------------------------------------------------------------------------
# Test 10: 12 Anthropic repos listed
# ---------------------------------------------------------------------------
ANTHROPIC_REPOS=(
  "anthropic-cookbook"
  "anthropic-quickstarts"
  "anthropic-sdk-python"
  "anthropic-sdk-typescript"
  "courses"
  "prompt-eng-interactive-tutorial"
  "claude-code-action"
  "claude-code-security-review"
  "claude-plugins-official"
  "claude-constitution"
  "healthcare"
  "life-sciences"
)

repos_found=0
for repo in "${ANTHROPIC_REPOS[@]}"; do
  if grep -q "$repo" "$DOC" 2>/dev/null; then
    repos_found=$((repos_found + 1))
  fi
done

if [ "$repos_found" -ge 12 ]; then
  pass "All 12 Anthropic repos referenced ($repos_found found)"
else
  fail "Only $repos_found of 12 Anthropic repos found"
  # List missing repos
  for repo in "${ANTHROPIC_REPOS[@]}"; do
    if ! grep -q "$repo" "$DOC" 2>/dev/null; then
      echo "  Missing repo: $repo"
    fi
  done
fi

# ---------------------------------------------------------------------------
# Test 11: Repos have priority tiers (P1/P2 or High/Medium/Low tier labels)
# ---------------------------------------------------------------------------
tier_labels=$(grep -cE "(P1|P2|Tier [0-9]|Priority:)" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$tier_labels" 2 \
  "Priority tier labels found ({actual} occurrences)" \
  "Priority tier labels not found or insufficient ({actual} occurrences)"

print_results
