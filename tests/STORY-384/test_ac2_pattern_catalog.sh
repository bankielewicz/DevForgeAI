#!/usr/bin/env bash
# STORY-384 AC#2: Pattern Catalog Contains 30+ Patterns with Metadata
# Validates:
#   - Minimum 30 unique PE-NNN identifiers
#   - Each pattern has 5 required fields: Pattern Name, Source Repo, Description (2+ sentences),
#     Applicability Rating, DevForgeAI Recommendation
#   - Organized by category
#   - No duplicate PE-NNN IDs

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "Research document"

# ---------------------------------------------------------------------------
# Test 2: Pattern Catalog section exists
# ---------------------------------------------------------------------------
assert_section_exists "Pattern Catalog"

# ---------------------------------------------------------------------------
# Test 3: Minimum 30 unique PE-NNN identifiers
# ---------------------------------------------------------------------------
pe_ids=$(grep -oE "PE-[0-9]{3}" "$DOC" 2>/dev/null | sort -u || true)
if [ -z "$pe_ids" ]; then
  pe_count=0
else
  pe_count=$(echo "$pe_ids" | wc -l | tr -d '[:space:]')
fi

assert_min_count "$pe_count" 30 \
  "Found {actual} unique PE-NNN identifiers (minimum {min} required)" \
  "Only {actual} unique PE-NNN identifiers found (minimum {min} required)"

# ---------------------------------------------------------------------------
# Test 4: No duplicate PE-NNN IDs
# ---------------------------------------------------------------------------
all_pe_ids=$(grep -oE "PE-[0-9]{3}" "$DOC" 2>/dev/null | sort)
unique_pe_ids=$(echo "$all_pe_ids" | sort -u)
all_count=$(echo "$all_pe_ids" | grep -c "PE-" 2>/dev/null || echo "0")
unique_count=$(echo "$unique_pe_ids" | grep -c "PE-" 2>/dev/null || echo "0")

# Check for IDs that appear in pattern headers more than once
# PE-NNN may appear in both header and body text, so check header-level duplicates
header_pe_ids=$(grep -E "^#{1,4}.*PE-[0-9]{3}" "$DOC" 2>/dev/null | grep -oE "PE-[0-9]{3}" | sort || true)
if [ -z "$header_pe_ids" ]; then
  header_dupes=0
else
  header_dupes=$(echo "$header_pe_ids" | uniq -d | wc -l | tr -d '[:space:]')
fi

if [ "$header_dupes" -eq 0 ]; then
  pass "No duplicate PE-NNN identifiers in pattern headers"
else
  fail "$header_dupes duplicate PE-NNN identifiers found in pattern headers"
fi

# ---------------------------------------------------------------------------
# Test 5: Each PE-NNN pattern has Pattern Name (in header line with PE-NNN)
# ---------------------------------------------------------------------------
# Pattern headers should look like: "#### PE-001: Pattern Name Here"
pattern_headers=$(grep -cE "^#{1,4}.*PE-[0-9]{3}:.*[A-Z]" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$pattern_headers" 30 \
  "Found {actual} pattern headers with names (PE-NNN: Name format)" \
  "Only {actual} pattern headers with names found (need 30+)"

# ---------------------------------------------------------------------------
# Test 6: Each pattern has Source Repo field
# ---------------------------------------------------------------------------
source_count=$(grep -cE "^(\*\*)?Source( Repo)?(\*\*)?:" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$source_count" 30 \
  "Found {actual} Source/Source Repo fields (need 30+)" \
  "Only {actual} Source/Source Repo fields found (need 30+)"

# ---------------------------------------------------------------------------
# Test 7: Each pattern has Description field
# ---------------------------------------------------------------------------
desc_count=$(grep -cE "^(\*\*)?Description(\*\*)?:" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$desc_count" 30 \
  "Found {actual} Description fields (need 30+)" \
  "Only {actual} Description fields found (need 30+)"

# ---------------------------------------------------------------------------
# Test 8: Descriptions have 2+ sentences (check for at least 2 periods in description lines)
# Each description should contain at least 2 sentence-ending periods
# ---------------------------------------------------------------------------
# Extract description content lines (the line starting with **Description**: and continuing)
short_descs=0
total_descs=0
while IFS= read -r line; do
  total_descs=$((total_descs + 1))
  # Remove the "Description: " prefix
  desc_text="${line#*Description: }"
  # Count sentence-ending periods (rough heuristic: periods followed by space or end-of-line)
  period_count=$(echo "$desc_text" | grep -oE "\. |\.( |$)" | wc -l || echo "0")
  # Also count period at end of line
  ends_with_period=$(echo "$desc_text" | grep -c "\.$" || echo "0")
  total_periods=$((period_count + ends_with_period))
  if [ "$total_periods" -lt 2 ]; then
    short_descs=$((short_descs + 1))
  fi
done < <(grep -E "^Description:" "$DOC" 2>/dev/null)

if [ "$short_descs" -eq 0 ] && [ "$total_descs" -ge 30 ]; then
  pass "All $total_descs descriptions contain 2+ sentences"
elif [ "$total_descs" -lt 30 ]; then
  fail "Only $total_descs descriptions found (need 30+)"
else
  fail "$short_descs descriptions have fewer than 2 sentences"
fi

# ---------------------------------------------------------------------------
# Test 9: Each pattern has Applicability Rating field
# ---------------------------------------------------------------------------
rating_count=$(grep -cE "^(\*\*)?Applicability( Rating)?(\*\*)?:" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$rating_count" 30 \
  "Found {actual} Applicability fields (need 30+)" \
  "Only {actual} Applicability fields found (need 30+)"

# ---------------------------------------------------------------------------
# Test 10: Each pattern has DevForgeAI Recommendation field
# ---------------------------------------------------------------------------
rec_count=$(grep -cE "^(\*\*)?DevForgeAI Recommendation(\*\*)?:" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$rec_count" 30 \
  "Found {actual} DevForgeAI Recommendation fields (need 30+)" \
  "Only {actual} DevForgeAI Recommendation fields found (need 30+)"

# ---------------------------------------------------------------------------
# Test 11: Patterns organized by category (at least 3 ### category headers under Pattern Catalog)
# ---------------------------------------------------------------------------
# Extract Pattern Catalog section
catalog_section=$(extract_section "Pattern Catalog")

category_count=$(echo "$catalog_section" | grep -cE "^### " 2>/dev/null || echo "0")
assert_min_count "$category_count" 3 \
  "Pattern Catalog organized by {actual} categories (need 3+)" \
  "Pattern Catalog has only {actual} categories (need 3+)"

print_results
