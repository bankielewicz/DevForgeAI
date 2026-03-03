#!/usr/bin/env bash
# STORY-382 AC#7: Agent Architecture Patterns Explicitly Captured
# Validates at least 3 agent architecture patterns are documented (from the 5 available
# in cookbooks patterns/agents/ plus autonomous-coding quickstart), each with explicit
# mapping to DevForgeAI's orchestration model.
#
# Expected: FAIL (cookbook/quickstart section does not exist yet - TDD Red phase)

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

# Test 2: Cookbook/quickstart section exists
if ! grep -q "^## Cookbook and Quickstart Patterns" "$DOC" 2>/dev/null; then
  fail "Cookbook and Quickstart Patterns section not found"
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi
pass "Cookbook and Quickstart Patterns section exists"

# Extract section content
section_content=$(sed -n '/^## Cookbook and Quickstart Patterns$/,/^## [^#]/p' "$DOC" 2>/dev/null | head -n -1)
if [ -z "$section_content" ]; then
  section_content=$(sed -n '/^## Cookbook and Quickstart Patterns$/,$p' "$DOC" 2>/dev/null)
fi

# Test 3: Agent Architecture Patterns subsection exists
if echo "$section_content" | grep -qi "Agent Architecture Patterns\|Agent Patterns" 2>/dev/null; then
  pass "Agent Architecture Patterns subsection found"
else
  fail "Agent Architecture Patterns subsection not found"
fi

# Test 4: At least 3 agent architecture patterns documented
# Count known agent architecture pattern names from cookbooks
agent_pattern_matches=0
AGENT_PATTERNS=(
  "Prompt Chaining"
  "Routing"
  "Parallelization"
  "Orchestrator"
  "Evaluator"
  "autonomous"
)

for pattern_name in "${AGENT_PATTERNS[@]}"; do
  if echo "$section_content" | grep -qi "$pattern_name" 2>/dev/null; then
    agent_pattern_matches=$((agent_pattern_matches + 1))
  fi
done

if [ "$agent_pattern_matches" -ge 3 ]; then
  pass "At least 3 agent architecture patterns documented ($agent_pattern_matches matches)"
else
  fail "Fewer than 3 agent architecture patterns ($agent_pattern_matches found, need 3+)"
fi

# Test 5: DevForgeAI mapping present for agent patterns
# Look for DevForgeAI-specific terms in agent pattern entries
devforgeai_mapping_count=0
MAPPING_TERMS=(
  "subagent"
  "orchestration"
  "skill"
  "Opus"
  "delegation"
  "workflow"
)

for term in "${MAPPING_TERMS[@]}"; do
  if echo "$section_content" | grep -qi "$term" 2>/dev/null; then
    devforgeai_mapping_count=$((devforgeai_mapping_count + 1))
  fi
done

if [ "$devforgeai_mapping_count" -ge 3 ]; then
  pass "DevForgeAI orchestration mapping terms found ($devforgeai_mapping_count terms)"
else
  fail "Insufficient DevForgeAI mapping terms ($devforgeai_mapping_count found, need 3+)"
fi

# Test 6: patterns/agents/ directory referenced as source
if echo "$section_content" | grep -q "patterns/agents/" 2>/dev/null; then
  pass "patterns/agents/ directory referenced as source"
else
  fail "patterns/agents/ directory not referenced in agent architecture patterns"
fi

# Test 7: Agent patterns reference specific notebook files
agent_notebooks=$(echo "$section_content" | grep -cE "(orchestrator|routing|chaining|parallelization|evaluator|autonomous).*\.(ipynb|py|md)" 2>/dev/null || echo "0")
if [ "$agent_notebooks" -ge 1 ]; then
  pass "Agent patterns reference specific source files ($agent_notebooks references)"
else
  # Also check reverse order (filename then pattern name)
  agent_notebooks_rev=$(echo "$section_content" | grep -cE "\.(ipynb|py|md).*(orchestrator|routing|chaining|parallelization|evaluator|autonomous)" 2>/dev/null || echo "0")
  if [ "$agent_notebooks_rev" -ge 1 ]; then
    pass "Agent patterns reference specific source files ($agent_notebooks_rev references)"
  else
    fail "No specific source files referenced for agent architecture patterns"
  fi
fi

# Test 8: At least one agent pattern has explicit DevForgeAI Recommendation
agent_recommendations=$(echo "$section_content" | grep -A5 -iE "(Prompt Chaining|Routing|Parallelization|Orchestrator|Evaluator)" 2>/dev/null | grep -c "DevForgeAI Recommendation" 2>/dev/null || echo "0")
if [ "$agent_recommendations" -ge 1 ]; then
  pass "Agent patterns include DevForgeAI recommendations ($agent_recommendations found)"
else
  # Broader search - check if DevForgeAI Recommendation exists anywhere in section
  any_recommendations=$(echo "$section_content" | grep -c "DevForgeAI Recommendation" 2>/dev/null || echo "0")
  if [ "$any_recommendations" -ge 3 ]; then
    pass "DevForgeAI Recommendations present in section ($any_recommendations total)"
  else
    fail "Insufficient DevForgeAI Recommendations for agent patterns"
  fi
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
