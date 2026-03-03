#!/usr/bin/env bash
# STORY-384 AC#3: Applicability Ratings and Recommendations

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "Research document"

# Test 2: All ratings are valid enum values
valid_ratings=0
invalid_ratings=0
while IFS= read -r line; do
  rating=$(echo "$line" | sed -E 's/^Applicability: //' | xargs)
  case "$rating" in
    High|Medium|Low|N/A)
      valid_ratings=$((valid_ratings + 1))
      ;;
    *)
      invalid_ratings=$((invalid_ratings + 1))
      echo "  Invalid rating found: '$rating'"
      ;;
  esac
done < <(grep -E "^Applicability:" "$DOC" 2>/dev/null)

if [ "$invalid_ratings" -eq 0 ] && [ "$valid_ratings" -gt 0 ]; then
  pass "All $valid_ratings ratings are valid (High/Medium/Low/N/A)"
else
  fail "$invalid_ratings invalid ratings found out of $((valid_ratings + invalid_ratings)) total"
fi

# Tests 3-6: Count patterns per rating tier
high_count=$(grep -cE "^Applicability: High" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$high_count" 10 "High-rated patterns: {actual} (minimum {min} required)" \
  "High-rated patterns: {actual} (minimum {min} required)"

medium_count=$(grep -cE "^Applicability: Medium" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$medium_count" 10 "Medium-rated patterns: {actual} (minimum {min} required)" \
  "Medium-rated patterns: {actual} (minimum {min} required)"

low_count=$(grep -cE "^Applicability: Low" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$low_count" 5 "Low-rated patterns: {actual} (minimum {min} required)" \
  "Low-rated patterns: {actual} (minimum {min} required)"

na_count=$(grep -cE "^Applicability: N/A" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$na_count" 2 "N/A-rated patterns: {actual} (minimum {min} required)" \
  "N/A-rated patterns: {actual} (minimum {min} required)"

# Test 7: Applicability Summary section exists
assert_section_exists "Applicability Summary"

# Test 8: Summary table contains count for each rating
summary_section=$(extract_section "Applicability Summary")
for rating in "High" "Medium" "Low" "N/A"; do
  if echo "$summary_section" | grep -q "$rating" 2>/dev/null; then
    pass "Summary table includes '$rating' rating row"
  else
    fail "Summary table missing '$rating' rating row"
  fi
done

# Test 9: High/Medium patterns reference DevForgeAI components
known_components="subagent|skill|devforgeai|test-automator|backend-architect|code-reviewer|qa|development|architecture|orchestration|ideation|feedback|release|analyzer|scanner|designer|automator|validator|writer|interpreter|planner|auditor|specialist|reviewer|requirements-analyst|frontmatter|phase-state|phase|xml|workflow|conventions|rubric|guide|template"
high_medium_without_component=0
in_high_medium=false
while IFS= read -r line; do
  if echo "$line" | grep -qE "^Applicability: (High|Medium)"; then
    in_high_medium=true
  elif echo "$line" | grep -qE "^DevForgeAI Recommendation:"; then
    if [ "$in_high_medium" = true ]; then
      rec_text=$(echo "$line" | sed 's/^DevForgeAI Recommendation: //')
      if echo "$rec_text" | grep -qiE "$known_components" 2>/dev/null; then
        : # good
      else
        high_medium_without_component=$((high_medium_without_component + 1))
      fi
      in_high_medium=false
    fi
  elif echo "$line" | grep -qE "^Applicability:"; then
    in_high_medium=false
  fi
done < "$DOC"

if [ "$high_medium_without_component" -eq 0 ]; then
  pass "All High/Medium patterns reference specific DevForgeAI components"
else
  fail "$high_medium_without_component High/Medium patterns lack DevForgeAI component references"
fi

# Test 10: N/A patterns have justification
na_without_justification=0
in_na=false
while IFS= read -r line; do
  if echo "$line" | grep -qE "^Applicability: N/A"; then
    in_na=true
  elif echo "$line" | grep -qE "^Rationale:"; then
    if [ "$in_na" = true ]; then
      rationale=$(echo "$line" | sed 's/^Rationale: //')
      if [ -n "$rationale" ] && [ "$rationale" != " " ]; then
        : # good
      else
        na_without_justification=$((na_without_justification + 1))
      fi
      in_na=false
    fi
  elif echo "$line" | grep -qE "^Applicability:"; then
    in_na=false
  fi
done < "$DOC"

if [ "$na_without_justification" -eq 0 ]; then
  pass "All N/A patterns have justification in Rationale field"
else
  fail "$na_without_justification N/A patterns lack justification"
fi

print_results
