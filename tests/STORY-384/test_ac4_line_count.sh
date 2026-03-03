#!/usr/bin/env bash
# STORY-384 AC#4: Document Line Count
# Validates:
#   - Total lines < 2000
#   - Executive Summary under 50 lines
#   - Condensed format for N/A patterns if needed

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "Research document"

# ---------------------------------------------------------------------------
# Test 2: Total lines < 2000
# ---------------------------------------------------------------------------
total_lines=$(wc -l < "$DOC")
if [ "$total_lines" -lt 2000 ]; then
  pass "Total line count: $total_lines (under 2000 limit)"
else
  fail "Total line count: $total_lines (exceeds 2000 limit)"
fi

# ---------------------------------------------------------------------------
# Test 3: Executive Summary section under 50 lines
# ---------------------------------------------------------------------------
exec_summary_start=$(grep -nE "^## Executive Summary" "$DOC" 2>/dev/null | head -n 1 | cut -d: -f1)
if [ -z "$exec_summary_start" ]; then
  fail "Executive Summary section not found - cannot check line count"
else
  # Find next ## section header after Executive Summary
  next_section=$(tail -n +"$((exec_summary_start + 1))" "$DOC" | grep -nE "^## [^#]" | head -n 1 | cut -d: -f1)
  if [ -n "$next_section" ]; then
    exec_summary_lines=$((next_section - 1))
  else
    # Executive Summary is last section (unlikely but handle)
    remaining=$(tail -n +"$exec_summary_start" "$DOC" | wc -l)
    exec_summary_lines=$remaining
  fi

  if [ "$exec_summary_lines" -le 50 ]; then
    pass "Executive Summary is $exec_summary_lines lines (under 50 limit)"
  else
    fail "Executive Summary is $exec_summary_lines lines (exceeds 50 limit)"
  fi
fi

# ---------------------------------------------------------------------------
# Test 4: Executive Summary appears within first 50 lines of the document
# ---------------------------------------------------------------------------
if [ -n "$exec_summary_start" ]; then
  if [ "$exec_summary_start" -le 50 ]; then
    pass "Executive Summary starts at line $exec_summary_start (within first 50 lines)"
  else
    fail "Executive Summary starts at line $exec_summary_start (should be within first 50 lines)"
  fi
fi

# ---------------------------------------------------------------------------
# Test 5: N/A patterns use condensed format (shorter than High/Medium patterns)
# Check that N/A pattern entries average fewer lines than High patterns
# ---------------------------------------------------------------------------
# Count lines between consecutive pattern headers to gauge pattern entry size
# This is a structural check: N/A patterns should not be verbose
na_pattern_lines=0
na_pattern_count=0
in_na_pattern=false
lines_in_current=0

while IFS= read -r line; do
  if echo "$line" | grep -qE "^#{1,4}.*PE-[0-9]{3}:" 2>/dev/null; then
    if [ "$in_na_pattern" = true ]; then
      na_pattern_lines=$((na_pattern_lines + lines_in_current))
      na_pattern_count=$((na_pattern_count + 1))
    fi
    in_na_pattern=false
    lines_in_current=0
  fi
  if echo "$line" | grep -qE "^Applicability: N/A" 2>/dev/null; then
    in_na_pattern=true
  fi
  lines_in_current=$((lines_in_current + 1))
done < "$DOC"

# Capture last N/A pattern
if [ "$in_na_pattern" = true ]; then
  na_pattern_lines=$((na_pattern_lines + lines_in_current))
  na_pattern_count=$((na_pattern_count + 1))
fi

if [ "$na_pattern_count" -gt 0 ]; then
  avg_na_lines=$((na_pattern_lines / na_pattern_count))
  if [ "$avg_na_lines" -le 15 ]; then
    pass "N/A patterns average $avg_na_lines lines (condensed, under 15)"
  else
    fail "N/A patterns average $avg_na_lines lines (should be condensed, under 15)"
  fi
else
  fail "No N/A patterns found to check condensed format"
fi

print_results
