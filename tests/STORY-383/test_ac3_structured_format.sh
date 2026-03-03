#!/usr/bin/env bash
# STORY-383 AC#3: Findings Follow STORY-380 Structured Format
# Validates each pattern entry in the Dev Tools section contains:
# pattern name, source repo/file, description, applicability rating,
# DevForgeAI recommendation, and agent/skill mapping.
# Section header must be "## Dev Tools and Domain Patterns".
#
# Expected: FAIL (Dev Tools section does not exist yet - TDD Red phase)

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

# Test 2: Section header is exactly "## Dev Tools and Domain Patterns"
if grep -q "^## Dev Tools and Domain Patterns" "$DOC" 2>/dev/null; then
  pass "Section header '## Dev Tools and Domain Patterns' found"
else
  fail "Section header '## Dev Tools and Domain Patterns' not found"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# Extract Dev Tools section content
dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$dev_tools_section" ]; then
  dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,$p' "$DOC" 2>/dev/null)
fi

# Count patterns in Dev Tools section
pattern_count=$(echo "$dev_tools_section" | grep -c "^#### Pattern D[0-9]" 2>/dev/null || echo "0")

# Test 3: Each pattern has Source field
source_count=$(echo "$dev_tools_section" | grep -cE "^\*\*Source\*\*:" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$source_count" -ge "$pattern_count" ]; then
  pass "All patterns have Source field ($source_count sources for $pattern_count patterns)"
else
  fail "Source field count ($source_count) < pattern count ($pattern_count)"
fi

# Test 4: Each pattern has Description field
desc_count=$(echo "$dev_tools_section" | grep -cE "^\*\*Description\*\*:" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$desc_count" -ge "$pattern_count" ]; then
  pass "All patterns have Description field ($desc_count for $pattern_count patterns)"
else
  fail "Description field count ($desc_count) < pattern count ($pattern_count)"
fi

# Test 5: Each pattern has Applicability field
rating_count=$(echo "$dev_tools_section" | grep -cE "^\*\*Applicability\*\*:" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$rating_count" -ge "$pattern_count" ]; then
  pass "All patterns have Applicability field ($rating_count for $pattern_count patterns)"
else
  fail "Applicability field count ($rating_count) < pattern count ($pattern_count)"
fi

# Test 6: Each pattern has DevForgeAI Recommendation field
rec_count=$(echo "$dev_tools_section" | grep -cE "^\*\*DevForgeAI Recommendation\*\*:" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$rec_count" -ge "$pattern_count" ]; then
  pass "All patterns have Recommendation field ($rec_count for $pattern_count patterns)"
else
  fail "Recommendation field count ($rec_count) < pattern count ($pattern_count)"
fi

# Test 7: Each pattern has Agent/Skill Mapping field (new field for STORY-383)
mapping_count=$(echo "$dev_tools_section" | grep -cE "^\*\*Agent/Skill Mapping\*\*:" 2>/dev/null || echo "0")
if [ "$pattern_count" -gt 0 ] && [ "$mapping_count" -ge "$pattern_count" ]; then
  pass "All patterns have Agent/Skill Mapping field ($mapping_count for $pattern_count patterns)"
else
  fail "Agent/Skill Mapping field count ($mapping_count) < pattern count ($pattern_count)"
fi

# Test 8: No duplicate pattern names within Dev Tools section (BR-003)
duplicates=$(echo "$dev_tools_section" | grep "^#### Pattern D[0-9]" 2>/dev/null | sort | uniq -d | wc -l || echo "0")
if [ "$duplicates" -eq 0 ]; then
  pass "No duplicate pattern names in Dev Tools section"
else
  fail "$duplicates duplicate pattern names found in Dev Tools section"
fi

# Test 9: Pattern entries have at least 6 required bold fields each
# Verify a representative structural check: pattern_count * 6 fields
required_fields=("Source" "Description" "Applicability" "Rationale" "DevForgeAI Recommendation" "Agent/Skill Mapping")
fields_found=0
for field in "${required_fields[@]}"; do
  count=$(echo "$dev_tools_section" | grep -c "^\*\*${field}\*\*:" 2>/dev/null || echo "0")
  if [ "$count" -ge "$pattern_count" ] && [ "$pattern_count" -gt 0 ]; then
    fields_found=$((fields_found + 1))
  fi
done
if [ "$fields_found" -eq 6 ]; then
  pass "All 6 required fields present for every pattern"
else
  fail "Only $fields_found of 6 required field types have sufficient count"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
