#!/usr/bin/env bash
# STORY-381 AC#3: Concrete DevForgeAI Examples for High-Applicability Patterns
# Validates that patterns rated "High" have a "DevForgeAI Application"
# subsection naming a specific component file, current fragment, and
# improved fragment.
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

# Extract Tutorial Patterns section
tutorial_section=$(sed -n '/^## Tutorial Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1 || echo "")
if [ -z "$tutorial_section" ]; then
  tutorial_section=$(sed -n '/^## Tutorial Patterns/,$p' "$DOC" 2>/dev/null || echo "")
fi

# Test 2: At least one pattern is rated High
high_count=$(count_in_var "$tutorial_section" '\bHigh\b' "-c")
if [ "$high_count" -ge 1 ]; then
  pass "At least one High-rated pattern exists ($high_count High occurrences)"
else
  fail "No High-rated patterns found"
fi

# Test 3: DevForgeAI Application subsections exist
app_subsection_count=$(count_in_var "$tutorial_section" 'DevForgeAI Application' "-ci")
if [ "$app_subsection_count" -ge 1 ]; then
  pass "DevForgeAI Application subsections found ($app_subsection_count)"
else
  fail "No DevForgeAI Application subsections found"
fi

# Test 4: Application subsections name specific component files (.md)
component_ref_count=$(count_in_var "$tutorial_section" '\.md\b' "-c")
if [ "$component_ref_count" -ge 1 ]; then
  pass "Component file references found in application examples ($component_ref_count)"
else
  fail "No specific component file references (.md) found in application examples"
fi

# Test 5: Application subsections contain "current" fragment marker
current_fragment_count=$(count_in_var "$tutorial_section" 'current\|existing\|before' "-ci")
if [ "$current_fragment_count" -ge 1 ]; then
  pass "Current/existing fragment markers found ($current_fragment_count)"
else
  fail "No current/existing fragment markers found in application examples"
fi

# Test 6: Application subsections contain "improved" fragment marker
improved_fragment_count=$(count_in_var "$tutorial_section" 'improved\|recommended\|after\|enhanced' "-ci")
if [ "$improved_fragment_count" -ge 1 ]; then
  pass "Improved/recommended fragment markers found ($improved_fragment_count)"
else
  fail "No improved/recommended fragment markers found in application examples"
fi

# Test 7: Every High-rated pattern has a DevForgeAI Application subsection
high_patterns=0
high_with_application=0
in_pattern=false
is_high=false
has_application=false

while IFS= read -r line; do
  if printf '%s' "$line" | grep -q "^#### " 2>/dev/null; then
    if [ "$in_pattern" = true ] && [ "$is_high" = true ]; then
      high_patterns=$((high_patterns + 1))
      if [ "$has_application" = true ]; then
        high_with_application=$((high_with_application + 1))
      fi
    fi
    in_pattern=true
    is_high=false
    has_application=false
  fi
  if printf '%s' "$line" | grep -qE "\bHigh\b" 2>/dev/null; then
    is_high=true
  fi
  if printf '%s' "$line" | grep -qiE "DevForgeAI Application" 2>/dev/null; then
    has_application=true
  fi
done <<< "$tutorial_section"
# Check last pattern
if [ "$in_pattern" = true ] && [ "$is_high" = true ]; then
  high_patterns=$((high_patterns + 1))
  if [ "$has_application" = true ]; then
    high_with_application=$((high_with_application + 1))
  fi
fi

if [ "$high_patterns" -gt 0 ] && [ "$high_with_application" -ge "$high_patterns" ]; then
  pass "All $high_patterns High-rated patterns have DevForgeAI Application subsection"
else
  fail "Only $high_with_application of $high_patterns High-rated patterns have Application subsection"
fi

# Test 8: No API keys or credentials in output (NFR-004)
cred_count=$(grep -cE "(%store|API_KEY|ANTHROPIC_API_KEY|sk-ant-)" "$DOC" 2>/dev/null || echo "0")
cred_count=$(echo "$cred_count" | tr -d '[:space:]')
if [ "$cred_count" -eq 0 ]; then
  pass "No API keys or credentials in output"
else
  fail "$cred_count credential patterns found in document"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
