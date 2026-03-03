#!/usr/bin/env bash
# STORY-381 AC#2: Each Pattern Mapped to DevForgeAI Component Types
# Validates every tutorial pattern has Agent/Skill/Command applicability
# mapping with High/Medium/Low/N/A ratings, and at least one High/Medium
# per pattern.
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

# Test 2: Tutorial patterns have Agent rating column/field
agent_rating_count=$(count_in_var "$tutorial_section" 'Agent[s]\?.*:.*\(High\|Medium\|Low\|N/A\)' "-ci")
if [ "$agent_rating_count" -ge 9 ]; then
  pass "Agent ratings found for patterns ($agent_rating_count)"
else
  fail "Insufficient Agent ratings ($agent_rating_count found, need 9+)"
fi

# Test 3: Tutorial patterns have Skill rating column/field
skill_rating_count=$(count_in_var "$tutorial_section" 'Skill[s]\?.*:.*\(High\|Medium\|Low\|N/A\)' "-ci")
if [ "$skill_rating_count" -ge 9 ]; then
  pass "Skill ratings found for patterns ($skill_rating_count)"
else
  fail "Insufficient Skill ratings ($skill_rating_count found, need 9+)"
fi

# Test 4: Tutorial patterns have Command rating column/field
command_rating_count=$(count_in_var "$tutorial_section" 'Command[s]\?.*:.*\(High\|Medium\|Low\|N/A\)' "-ci")
if [ "$command_rating_count" -ge 9 ]; then
  pass "Command ratings found for patterns ($command_rating_count)"
else
  fail "Insufficient Command ratings ($command_rating_count found, need 9+)"
fi

# Test 5: Only valid rating values used (High/Medium/Low/N/A)
# Match only explicit rating lines (start with "- Agents:" or "- Skills:" or "- Commands:")
# Avoids false positives from prose containing "agent" or "command" incidentally
invalid_count=0
while IFS= read -r line; do
  if printf '%s' "$line" | grep -qE "^- (Agents?|Skills?|Commands?):" 2>/dev/null; then
    if ! printf '%s' "$line" | grep -qE "\b(High|Medium|Low|N/A)\b" 2>/dev/null; then
      invalid_count=$((invalid_count + 1))
    fi
  fi
done <<< "$tutorial_section"

if [ "$invalid_count" -eq 0 ]; then
  pass "All rating values are valid (High/Medium/Low/N/A)"
else
  fail "$invalid_count invalid rating values found"
fi

# Test 6: Each pattern has at least one High or Medium rating
tutorial_pattern_count=$(count_in_var "$tutorial_section" "^#### " "-c")
patterns_with_high_medium=0
in_pattern=false
has_high_medium=false

while IFS= read -r line; do
  if printf '%s' "$line" | grep -q "^#### " 2>/dev/null; then
    if [ "$in_pattern" = true ] && [ "$has_high_medium" = true ]; then
      patterns_with_high_medium=$((patterns_with_high_medium + 1))
    fi
    in_pattern=true
    has_high_medium=false
  fi
  if printf '%s' "$line" | grep -qE "\b(High|Medium)\b" 2>/dev/null; then
    has_high_medium=true
  fi
done <<< "$tutorial_section"
# Check last pattern
if [ "$in_pattern" = true ] && [ "$has_high_medium" = true ]; then
  patterns_with_high_medium=$((patterns_with_high_medium + 1))
fi

if [ "$tutorial_pattern_count" -gt 0 ] && [ "$patterns_with_high_medium" -ge "$tutorial_pattern_count" ]; then
  pass "All $tutorial_pattern_count patterns have at least one High/Medium rating"
else
  fail "Only $patterns_with_high_medium of $tutorial_pattern_count patterns have High/Medium rating"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
