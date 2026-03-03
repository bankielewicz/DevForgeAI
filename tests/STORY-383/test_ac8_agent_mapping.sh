#!/usr/bin/env bash
# STORY-383 AC#8: Domain-Specific Agent/Skill Mapping Identifies Improvement Targets
# Validates that an agent mapping summary table exists at the end of the Dev Tools
# section, listing agents/skills with pattern counts. Agent/skill names must match
# the framework registry.
#
# Expected: FAIL (Dev Tools section does not exist yet - TDD Red phase)

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
DOC="$PROJECT_ROOT/devforgeai/specs/research/prompt-engineering-patterns.md"
AGENTS_DIR="$PROJECT_ROOT/.claude/agents"
SKILLS_DIR="$PROJECT_ROOT/.claude/skills"

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

# Test 2: Dev Tools section exists
if ! grep -q "^## Dev Tools and Domain Patterns" "$DOC" 2>/dev/null; then
  fail "Dev Tools and Domain Patterns section not found"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Dev Tools and Domain Patterns section found"

# Extract Dev Tools section content
dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$dev_tools_section" ]; then
  dev_tools_section=$(sed -n '/^## Dev Tools and Domain Patterns/,$p' "$DOC" 2>/dev/null)
fi

# Test 3: Agent mapping summary table exists
# Look for "### Agent Mapping Summary Table" header
if echo "$dev_tools_section" | grep -q "### Agent Mapping Summary Table" 2>/dev/null; then
  pass "Agent mapping summary table section found"
else
  fail "Agent mapping summary table section not found (expected '### Agent Mapping Summary Table' header)"
fi

# Test 4: Summary table has data rows with agent/skill names
# Look for table rows containing known subagent patterns (hyphenated names)
agent_table_rows=$(echo "$dev_tools_section" | grep -cE "^\|\s*[a-z]+-[a-z]+" 2>/dev/null | tr -d '\n' || echo "0")
agent_table_rows=${agent_table_rows:-0}
if [ "$agent_table_rows" -ge 1 ]; then
  pass "Agent mapping table has data rows ($agent_table_rows rows with agent/skill names)"
else
  fail "Agent mapping table has no data rows with agent/skill names"
fi

# Test 5: Table contains pattern counts (numbers in cells)
table_with_numbers=$(echo "$dev_tools_section" | grep -E "^\|" 2>/dev/null | grep -cE "\|\s*[0-9]+" | tr -d '\n' || echo "0")
table_with_numbers=${table_with_numbers:-0}
if [ "$table_with_numbers" -ge 1 ]; then
  pass "Agent mapping table contains pattern counts ($table_with_numbers rows with numbers)"
else
  fail "Agent mapping table has no pattern counts"
fi

# Test 6: Agent/skill names in table reference known framework components (BR-005)
# Check that table rows contain recognizable agent/skill names (hyphenated names)
# Note: Some rows may have composite names like "devforgeai-development skill" or "All subagents"
agent_name_count=$(echo "$dev_tools_section" | grep -E "^\|" 2>/dev/null | grep -cE "[a-z]+-[a-z]+" | tr -d '\n' || echo "0")
agent_name_count=${agent_name_count:-0}
if [ "$agent_name_count" -ge 10 ]; then
  pass "Agent mapping table references framework agents ($agent_name_count rows with agent/skill names)"
else
  fail "Agent mapping table has insufficient agent references ($agent_name_count found, expected 10+)"
fi

# Test 7: High/Medium rated patterns each map to at least 1 agent (not just N/A)
high_medium_with_mapping=0
high_medium_total=0
in_pattern=false
current_rating=""

while IFS= read -r line; do
  if echo "$line" | grep -q "^#### Pattern D[0-9]"; then
    in_pattern=true
    current_rating=""
  fi
  if echo "$line" | grep -qE "^\*\*Applicability\*\*:.*(High|Medium)"; then
    current_rating="high_medium"
    high_medium_total=$((high_medium_total + 1))
  fi
  if [ "$current_rating" = "high_medium" ] && echo "$line" | grep -qE "^\*\*Agent/Skill Mapping\*\*:" 2>/dev/null; then
    # Check that it maps to a real agent (contains hyphenated name, not just "N/A")
    if echo "$line" | grep -qE "[a-z]+-[a-z]+" 2>/dev/null; then
      high_medium_with_mapping=$((high_medium_with_mapping + 1))
    fi
    current_rating=""
  fi
done <<< "$dev_tools_section"

if [ "$high_medium_total" -eq 0 ] || [ "$high_medium_with_mapping" -ge "$high_medium_total" ]; then
  pass "All High/Medium patterns have specific agent mapping ($high_medium_with_mapping of $high_medium_total)"
else
  fail "Not all High/Medium patterns have agent mapping ($high_medium_with_mapping of $high_medium_total)"
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
