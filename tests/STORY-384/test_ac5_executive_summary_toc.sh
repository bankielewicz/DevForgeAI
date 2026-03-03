#!/usr/bin/env bash
# STORY-384 AC#5: Executive Summary and Table of Contents
# Validates:
#   - Executive Summary within first 50 lines
#   - Contains: total pattern count, rating breakdown, top 5 patterns, one-paragraph overview
#   - Table of Contents with anchor links
#   - All ToC entries match actual headings

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "Research document"

# ---------------------------------------------------------------------------
# Test 2: Executive Summary section exists
# ---------------------------------------------------------------------------
exec_start=$(grep -nE "^## Executive Summary" "$DOC" 2>/dev/null | head -n 1 | cut -d: -f1)
if [ -n "$exec_start" ]; then
  pass "Executive Summary section found at line $exec_start"
else
  fail "Executive Summary section not found"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# ---------------------------------------------------------------------------
# Test 3: Executive Summary within first 50 lines
# ---------------------------------------------------------------------------
if [ "$exec_start" -le 50 ]; then
  pass "Executive Summary starts within first 50 lines (line $exec_start)"
else
  fail "Executive Summary starts at line $exec_start (should be within first 50)"
fi

# Extract Executive Summary content
next_section_line=$(tail -n +"$((exec_start + 1))" "$DOC" | grep -nE "^## [^#]" | head -n 1 | cut -d: -f1)
if [ -n "$next_section_line" ]; then
  exec_end=$((exec_start + next_section_line - 1))
else
  exec_end=$(wc -l < "$DOC")
fi
exec_content=$(sed -n "${exec_start},${exec_end}p" "$DOC")

# ---------------------------------------------------------------------------
# Test 4: Executive Summary contains total pattern count
# (Look for a number followed by "pattern" - e.g., "71 patterns" or "Total Patterns: 71")
# ---------------------------------------------------------------------------
if echo "$exec_content" | grep -qiE "[0-9]+ pattern" 2>/dev/null; then
  pass "Executive Summary contains total pattern count"
else
  fail "Executive Summary missing total pattern count"
fi

# ---------------------------------------------------------------------------
# Test 5: Executive Summary contains rating breakdown
# (Must mention High, Medium, Low counts)
# ---------------------------------------------------------------------------
has_high=$(echo "$exec_content" | grep -ciE "high.*[0-9]" 2>/dev/null || echo "0")
has_medium=$(echo "$exec_content" | grep -ciE "medium.*[0-9]" 2>/dev/null || echo "0")
has_low=$(echo "$exec_content" | grep -ciE "low.*[0-9]" 2>/dev/null || echo "0")

if [ "$has_high" -ge 1 ] && [ "$has_medium" -ge 1 ] && [ "$has_low" -ge 1 ]; then
  pass "Executive Summary contains rating breakdown (High/Medium/Low with counts)"
else
  fail "Executive Summary missing rating breakdown (High=$has_high, Medium=$has_medium, Low=$has_low matches)"
fi

# ---------------------------------------------------------------------------
# Test 6: Executive Summary contains top 5 high-priority patterns
# (Look for a list/table with at least 5 pattern references like PE-NNN or numbered items)
# ---------------------------------------------------------------------------
top5_pattern_refs=$(echo "$exec_content" | grep -cE "PE-[0-9]{3}" 2>/dev/null || true)
top5_pattern_refs=$(echo "$top5_pattern_refs" | tr -d '[:space:]')
top5_pattern_refs=${top5_pattern_refs:-0}
top5_list_items=$(echo "$exec_content" | grep -cE "^[0-9]+\." 2>/dev/null || true)
top5_list_items=$(echo "$top5_list_items" | tr -d '[:space:]')
top5_list_items=${top5_list_items:-0}
top5_bullet_items=$(echo "$exec_content" | grep -cE "^- " 2>/dev/null || true)
top5_bullet_items=$(echo "$top5_bullet_items" | tr -d '[:space:]')
top5_bullet_items=${top5_bullet_items:-0}

# Need at least 5 references (PE-NNN IDs, or numbered/bulleted list of top patterns)
top5_total=$top5_pattern_refs
if [ "$top5_list_items" -gt "$top5_total" ]; then
  top5_total=$top5_list_items
fi
if [ "$top5_bullet_items" -gt "$top5_total" ]; then
  top5_total=$top5_bullet_items
fi

assert_min_count "$top5_total" 5 \
  "Executive Summary contains top 5 patterns ({actual} references found)" \
  "Executive Summary missing top 5 patterns ({actual} references, need 5+)"

# ---------------------------------------------------------------------------
# Test 7: Executive Summary contains one-paragraph overview
# (Check for a paragraph of text that's at least 50 characters, not a header/list/table)
# ---------------------------------------------------------------------------
paragraph_found=false
while IFS= read -r line; do
  # Skip headers, list items, table rows, empty lines, bold metadata
  if echo "$line" | grep -qE "^(#|[-*]|\||$|\*\*)" 2>/dev/null; then
    continue
  fi
  # Check line length (real paragraph text)
  line_len=${#line}
  if [ "$line_len" -ge 50 ]; then
    paragraph_found=true
    break
  fi
done <<< "$exec_content"

if [ "$paragraph_found" = true ]; then
  pass "Executive Summary contains overview paragraph"
else
  fail "Executive Summary missing overview paragraph (need 50+ char prose text)"
fi

# ---------------------------------------------------------------------------
# Test 8: Table of Contents section exists
# ---------------------------------------------------------------------------
assert_section_exists "Table of Contents"

# Extract ToC content
toc_content=$(extract_section "Table of Contents")
if [ -z "$toc_content" ]; then
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# ---------------------------------------------------------------------------
# Test 9: Table of Contents contains anchor links (markdown format [text](#anchor))
# ---------------------------------------------------------------------------
anchor_links=$(echo "$toc_content" | grep -cE "\[.*\]\(#.*\)" 2>/dev/null || echo "0")
assert_min_count "$anchor_links" 5 \
  "Table of Contents has {actual} anchor links" \
  "Table of Contents has only {actual} anchor links (need 5+)"

# ---------------------------------------------------------------------------
# Test 10: All ToC anchor links resolve to actual headings
# ---------------------------------------------------------------------------
broken_links=0
while IFS= read -r link; do
  # Extract the anchor part from [text](#anchor)
  anchor=$(echo "$link" | grep -oE "\(#[^)]+\)" | sed 's/(#//;s/)//')
  if [ -z "$anchor" ]; then
    continue
  fi

  # Convert anchor back to heading text pattern:
  # Markdown anchors: lowercase, spaces->hyphens, strip special chars
  # Try to find a heading that would generate this anchor
  # Convert anchor hyphens to spaces for flexible matching
  anchor_as_text=$(echo "$anchor" | tr '-' ' ')

  # Search for a heading containing similar text (case insensitive)
  if grep -qiE "^#{1,4}.*${anchor_as_text}" "$DOC" 2>/dev/null; then
    : # Anchor resolves
  else
    broken_links=$((broken_links + 1))
    echo "  Broken ToC link: #$anchor"
  fi
done < <(echo "$toc_content" | grep -oE "\[.*\]\(#[^)]+\)")

if [ "$broken_links" -eq 0 ]; then
  pass "All ToC anchor links resolve to actual headings"
else
  fail "$broken_links ToC anchor links do not resolve to headings"
fi

print_results
