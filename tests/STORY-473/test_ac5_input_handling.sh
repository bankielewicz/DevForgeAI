#!/bin/bash
# AC#5: Required vs Optional Input Handling
# Verifies HALT on missing context files, SKIP/GAP on missing optional inputs

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_FILE="$PROJECT_ROOT/src/claude/agents/alignment-auditor.md"

PASS=0
FAIL=0

check() {
  local desc="$1" result="$2"
  if [ "$result" -eq 0 ]; then
    echo "PASS: $desc"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $desc"
    FAIL=$((FAIL + 1))
  fi
}

if [ ! -f "$AGENT_FILE" ]; then
  echo "FAIL: Agent file does not exist: $AGENT_FILE"
  echo "Results: 0 passed, 1 failed"
  exit 1
fi

# Must mention HALT when context files missing
grep -qi "HALT" "$AGENT_FILE"
check "Agent mentions HALT behavior" $?

# Must reference 6 context files as required
grep -q "context" "$AGENT_FILE"
check "Agent references context files" $?

# Must mention SKIP or GAP for optional inputs
grep -qiE "SKIP|GAP" "$AGENT_FILE"
check "Agent mentions SKIP or GAP for optional inputs" $?

# Must mention CLAUDE.md as optional
grep -q "CLAUDE.md" "$AGENT_FILE"
check "Agent references CLAUDE.md" $?

# Must mention system-prompt as optional
grep -qE "system-prompt|system_prompt" "$AGENT_FILE"
check "Agent references system-prompt" $?

# Must mention LOW severity for missing optional inputs
grep -q "LOW" "$AGENT_FILE"
check "Agent mentions LOW severity for missing optional" $?

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
