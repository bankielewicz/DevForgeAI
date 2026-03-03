#!/usr/bin/env bash
# STORY-385 AC#6: Gap Analysis Covers All Three Component Types
# Validates:
#   - At least one proposed new Agent opportunity
#   - At least one proposed new Skill opportunity (or skill enhancement)
#   - At least one proposed new Command opportunity (or command enhancement)
#   - Component Type field uses valid enum (Agent, Skill, Command)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test_helpers.sh"

require_doc "New capabilities document"

# ---------------------------------------------------------------------------
# Test 2: Component Type fields exist for all opportunities
# ---------------------------------------------------------------------------
component_type_count=$(grep -ciE "(^|\*\*)Component Type(\*\*)?:" "$DOC" 2>/dev/null || echo "0")
assert_min_count "$component_type_count" 5 \
  "Found {actual} Component Type fields (need {min}+)" \
  "Only {actual} Component Type fields found (need {min}+)"

# ---------------------------------------------------------------------------
# Test 3: All Component Type values are valid enum (Agent, Skill, Command)
# ---------------------------------------------------------------------------
invalid_component=0
while IFS= read -r line; do
  value=$(echo "$line" | sed -E 's/^.*[Cc]omponent [Tt]ype(\*\*)?:\s*//' | sed 's/\*\*//g' | xargs)
  if ! echo "$value" | grep -qiE "^(Agent|Skill|Command)$" 2>/dev/null; then
    invalid_component=$((invalid_component + 1))
    echo "  Invalid Component Type: '$value'"
  fi
done < <(grep -iE "(^|\*\*)Component Type(\*\*)?:" "$DOC" 2>/dev/null)

if [ "$invalid_component" -eq 0 ]; then
  pass "All Component Type values are valid (Agent/Skill/Command)"
else
  fail "$invalid_component Component Type values are invalid (must be Agent, Skill, or Command)"
fi

# ---------------------------------------------------------------------------
# Test 4: At least one Agent opportunity
# Pattern matches: **Component Type:** Agent (with markdown bold)
# ---------------------------------------------------------------------------
agent_count=$(grep -i "Component Type.*Agent" "$DOC" 2>/dev/null | grep -v "^|" | wc -l || echo "0")
agent_count=$(echo "$agent_count" | tr -d '[:space:]')
if [ "$agent_count" -ge 1 ]; then
  pass "At least one Agent opportunity found ($agent_count)"
else
  fail "No Agent opportunity found (need at least 1)"
fi

# ---------------------------------------------------------------------------
# Test 5: At least one Skill opportunity
# ---------------------------------------------------------------------------
skill_count=$(grep -i "Component Type.*Skill" "$DOC" 2>/dev/null | grep -v "^|" | wc -l || echo "0")
skill_count=$(echo "$skill_count" | tr -d '[:space:]')
if [ "$skill_count" -ge 1 ]; then
  pass "At least one Skill opportunity found ($skill_count)"
else
  fail "No Skill opportunity found (need at least 1)"
fi

# ---------------------------------------------------------------------------
# Test 6: At least one Command opportunity
# ---------------------------------------------------------------------------
command_count=$(grep -i "Component Type.*Command" "$DOC" 2>/dev/null | grep -v "^|" | wc -l || echo "0")
command_count=$(echo "$command_count" | tr -d '[:space:]')
if [ "$command_count" -ge 1 ]; then
  pass "At least one Command opportunity found ($command_count)"
else
  fail "No Command opportunity found (need at least 1)"
fi

# ---------------------------------------------------------------------------
# Test 7: Component type distribution summary
# Verify all 3 types are present (not concentrated in 1 type)
# ---------------------------------------------------------------------------
types_present=0
if [ "$agent_count" -ge 1 ]; then types_present=$((types_present + 1)); fi
if [ "$skill_count" -ge 1 ]; then types_present=$((types_present + 1)); fi
if [ "$command_count" -ge 1 ]; then types_present=$((types_present + 1)); fi

if [ "$types_present" -eq 3 ]; then
  pass "All 3 component types represented (Agent: $agent_count, Skill: $skill_count, Command: $command_count)"
else
  fail "Only $types_present of 3 component types represented (need all 3: Agent, Skill, Command)"
fi

# ---------------------------------------------------------------------------
# Test 8: Opportunities reference existing component directories
# Check that document mentions .claude/agents/, .claude/skills/, .claude/commands/
# ---------------------------------------------------------------------------
dir_refs=0
if grep -qE "\.claude/agents/" "$DOC" 2>/dev/null; then dir_refs=$((dir_refs + 1)); fi
if grep -qE "\.claude/skills/" "$DOC" 2>/dev/null; then dir_refs=$((dir_refs + 1)); fi
if grep -qE "\.claude/commands/" "$DOC" 2>/dev/null; then dir_refs=$((dir_refs + 1)); fi

if [ "$dir_refs" -ge 1 ]; then
  pass "Document references component directories ($dir_refs directory references)"
else
  fail "Document does not reference any component directories (.claude/agents/, .claude/skills/, .claude/commands/)"
fi

print_results
