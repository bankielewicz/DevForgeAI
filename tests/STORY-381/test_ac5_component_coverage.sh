#!/usr/bin/env bash
# STORY-381 AC#5: Component Mapping Covers All 3 DevForgeAI Component Types
# Validates at least 2 patterns rated High for agents, at least 2 rated
# High for skills, and at least 1 rated High or Medium for commands.
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

# Test 2: At least 2 patterns rated High for Agents
agent_high_count=$(count_in_var "$tutorial_section" 'Agent[s]*.*:.*\bHigh\b' "-c")
if [ "$agent_high_count" -ge 2 ]; then
  pass "At least 2 patterns rated High for Agents ($agent_high_count found)"
else
  fail "Fewer than 2 patterns rated High for Agents ($agent_high_count found, need 2+)"
fi

# Test 3: At least 2 patterns rated High for Skills
skill_high_count=$(count_in_var "$tutorial_section" 'Skill[s]*.*:.*\bHigh\b' "-c")
if [ "$skill_high_count" -ge 2 ]; then
  pass "At least 2 patterns rated High for Skills ($skill_high_count found)"
else
  fail "Fewer than 2 patterns rated High for Skills ($skill_high_count found, need 2+)"
fi

# Test 4: At least 1 pattern rated High or Medium for Commands
command_high_medium_count=$(count_in_var "$tutorial_section" 'Command[s]*.*:.*\(High\|Medium\)' "-c")
if [ "$command_high_medium_count" -ge 1 ]; then
  pass "At least 1 pattern rated High/Medium for Commands ($command_high_medium_count found)"
else
  fail "No patterns rated High/Medium for Commands ($command_high_medium_count found, need 1+)"
fi

# Test 5: No component type completely neglected (all 3 have at least 1 rating)
agent_any=$(count_in_var "$tutorial_section" 'Agent[s]*.*:.*\(High\|Medium\|Low\|N/A\)' "-ci")
skill_any=$(count_in_var "$tutorial_section" 'Skill[s]*.*:.*\(High\|Medium\|Low\|N/A\)' "-ci")
command_any=$(count_in_var "$tutorial_section" 'Command[s]*.*:.*\(High\|Medium\|Low\|N/A\)' "-ci")

if [ "$agent_any" -ge 1 ] && [ "$skill_any" -ge 1 ] && [ "$command_any" -ge 1 ]; then
  pass "All 3 component types have ratings (Agents: $agent_any, Skills: $skill_any, Commands: $command_any)"
else
  fail "Component type missing ratings (Agents: $agent_any, Skills: $skill_any, Commands: $command_any)"
fi

# Test 6: Coverage summary - total High ratings across all component types
command_high_only=$(count_in_var "$tutorial_section" 'Command[s]*.*:.*\bHigh\b' "-c")
total_high=$((agent_high_count + skill_high_count + command_high_only))

if [ "$total_high" -ge 5 ]; then
  pass "Good overall High coverage across component types ($total_high total High ratings)"
else
  fail "Low overall High coverage ($total_high total, expected 5+ across agents+skills+commands)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
