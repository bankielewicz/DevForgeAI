#!/usr/bin/env bash
# STORY-386 AC#5: Template Fits Within 500-Line Subagent Size Limit
# Verifies the template documents that a populated agent should be 100-500 lines.
# Also checks the template reference document itself is under 800 lines.
# TDD RED phase - this test MUST FAIL until the template is created.

set -euo pipefail

TEMPLATE="src/claude/agents/agent-generator/references/canonical-agent-template.md"
ERRORS=0

if [[ ! -f "$TEMPLATE" ]]; then
  echo "FAIL: Template file does not exist at $TEMPLATE"
  exit 1
fi

# Template reference document should be under 800 lines
LINE_COUNT=$(wc -l < "$TEMPLATE")
if [[ $LINE_COUNT -gt 800 ]]; then
  echo "FAIL: Template reference document exceeds 800 lines (found: $LINE_COUNT)"
  ERRORS=$((ERRORS + 1))
fi

# Template must mention the 100-500 line range for populated agents
if ! grep -q "100" "$TEMPLATE" || ! grep -q "500" "$TEMPLATE"; then
  echo "FAIL: Template does not document 100-500 line range for populated agents"
  ERRORS=$((ERRORS + 1))
fi

# Template should mention size guidance or line count constraints
if ! grep -qi "line.*limit\|size.*guidance\|line.*count\|line.*range\|size.*limit" "$TEMPLATE"; then
  echo "FAIL: No size guidance section found in template"
  ERRORS=$((ERRORS + 1))
fi

if [[ $ERRORS -gt 0 ]]; then
  echo "FAIL: $ERRORS error(s) found in AC#5 validation"
  exit 1
fi

echo "PASS: Template documents 100-500 line range and is under 800 lines ($LINE_COUNT lines)"
exit 0
