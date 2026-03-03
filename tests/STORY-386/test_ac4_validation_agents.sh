#!/usr/bin/env bash
# STORY-386 AC#4: Template Validated Against 3+ Diverse Existing Agents
# Verifies gap analysis appendix exists for test-automator, code-reviewer, security-auditor.
# TDD RED phase - this test MUST FAIL until the template is created.

set -euo pipefail

TEMPLATE="src/claude/agents/agent-generator/references/canonical-agent-template.md"
ERRORS=0

if [[ ! -f "$TEMPLATE" ]]; then
  echo "FAIL: Template file does not exist at $TEMPLATE"
  exit 1
fi

# Gap analysis appendix must exist
if ! grep -qi "gap analysis\|appendix" "$TEMPLATE"; then
  echo "FAIL: No gap analysis appendix section found"
  ERRORS=$((ERRORS + 1))
fi

# 3 agent names must appear in the gap analysis
AGENTS=("test-automator" "code-reviewer" "security-auditor")
for agent in "${AGENTS[@]}"; do
  if ! grep -qi "$agent" "$TEMPLATE"; then
    echo "FAIL: Gap analysis missing agent: $agent"
    ERRORS=$((ERRORS + 1))
  fi
done

# Gap analysis should contain table structure (pipes for markdown tables)
if ! grep -q "|" "$TEMPLATE"; then
  echo "FAIL: No markdown table found (expected gap analysis table)"
  ERRORS=$((ERRORS + 1))
fi

# Each agent gap analysis should indicate present/absent for sections
if ! grep -qi "present\|absent\|yes\|no\|Y/N\|gap" "$TEMPLATE"; then
  echo "FAIL: Gap analysis table missing present/absent indicators"
  ERRORS=$((ERRORS + 1))
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "FAIL: $ERRORS error(s) found in AC#4 validation"
  exit 1
fi

echo "PASS: Gap analysis appendix present for all 3 agents"
exit 0
