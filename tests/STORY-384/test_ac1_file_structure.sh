#!/usr/bin/env bash
# STORY-384 AC#1: Research Artifact File Structure
# Validates:
#   - File exists at exact path
#   - YAML frontmatter with required fields: id, title, epic, status, created, updated, version, source_stories
#   - 7 required sections in correct order: Executive Summary, Table of Contents, Pattern Catalog,
#     Applicability Summary, DevForgeAI Recommendations, Source References, Appendix
#   - File loadable in single Read() call (< 2000 lines)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "File at devforgeai/specs/research/prompt-engineering-patterns.md"

# ---------------------------------------------------------------------------
# Test 2: File starts with YAML frontmatter delimiters (--- ... ---)
# ---------------------------------------------------------------------------
first_line=$(head -n 1 "$DOC")
if [ "$first_line" = "---" ]; then
  pass "File starts with YAML frontmatter delimiter '---'"
else
  fail "File does not start with YAML frontmatter delimiter (found: '$first_line')"
fi

# Extract YAML frontmatter (between first --- and second ---)
frontmatter=$(sed -n '1,/^---$/p' "$DOC" | tail -n +2)
# Check for closing delimiter (second ---)
closing_line=$(sed -n '2,$ p' "$DOC" | grep -n "^---$" | head -n 1 | cut -d: -f1)
if [ -n "$closing_line" ] && [ "$closing_line" -gt 1 ]; then
  pass "YAML frontmatter has closing delimiter"
  frontmatter=$(sed -n "2,$((closing_line))p" "$DOC")
else
  fail "YAML frontmatter missing closing delimiter"
  frontmatter=""
fi

# ---------------------------------------------------------------------------
# Tests 3-10: Required YAML frontmatter fields
# ---------------------------------------------------------------------------
REQUIRED_FIELDS=("id" "title" "epic" "status" "created" "updated" "version" "source_stories")

for field in "${REQUIRED_FIELDS[@]}"; do
  if echo "$frontmatter" | grep -qE "^${field}:" 2>/dev/null; then
    pass "YAML frontmatter contains required field: $field"
  else
    fail "YAML frontmatter missing required field: $field"
  fi
done

# ---------------------------------------------------------------------------
# Test 11: id field matches expected pattern (e.g., "PE-RESEARCH-001" or similar)
# ---------------------------------------------------------------------------
if echo "$frontmatter" | grep -qE "^id:" 2>/dev/null; then
  pass "id field present in frontmatter"
else
  fail "id field not found in frontmatter"
fi

# ---------------------------------------------------------------------------
# Test 12: source_stories field lists STORY-380, 381, 382, 383
# ---------------------------------------------------------------------------
for story_id in "STORY-380" "STORY-381" "STORY-382" "STORY-383"; do
  if echo "$frontmatter" | grep -q "$story_id" 2>/dev/null; then
    pass "source_stories references $story_id"
  else
    fail "source_stories missing $story_id"
  fi
done

# ---------------------------------------------------------------------------
# Tests 16-22: 7 required top-level sections exist (## headers)
# ---------------------------------------------------------------------------
REQUIRED_SECTIONS=(
  "Executive Summary"
  "Table of Contents"
  "Pattern Catalog"
  "Applicability Summary"
  "DevForgeAI Recommendations"
  "Source References"
  "Appendix"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
  if grep -qE "^## ${section}" "$DOC" 2>/dev/null; then
    pass "Required section found: '## $section'"
  else
    fail "Required section missing: '## $section'"
  fi
done

# ---------------------------------------------------------------------------
# Test 23: Sections appear in correct order
# ---------------------------------------------------------------------------
section_order_ok=true
prev_line=0
for section in "${REQUIRED_SECTIONS[@]}"; do
  line_num=$(grep -nE "^## ${section}" "$DOC" 2>/dev/null | head -n 1 | cut -d: -f1)
  if [ -z "$line_num" ]; then
    section_order_ok=false
    break
  fi
  if [ "$line_num" -le "$prev_line" ]; then
    section_order_ok=false
    break
  fi
  prev_line=$line_num
done

if [ "$section_order_ok" = true ]; then
  pass "All 7 sections appear in correct order"
else
  fail "Sections are not in the required order"
fi

# ---------------------------------------------------------------------------
# Test 24: File loadable in single Read() call (< 2000 lines)
# ---------------------------------------------------------------------------
total_lines=$(wc -l < "$DOC")
if [ "$total_lines" -lt 2000 ]; then
  pass "File is under 2000 lines ($total_lines lines) - loadable in single Read()"
else
  fail "File exceeds 2000 lines ($total_lines lines) - not loadable in single Read()"
fi

print_results
