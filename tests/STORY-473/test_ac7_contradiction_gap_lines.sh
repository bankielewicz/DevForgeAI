#!/bin/bash
# AC#7: Contradiction vs Gap Distinction and Line Numbers
# Verifies output structure for contradictions and gaps

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

# Contradictions must have layer_a and layer_b
grep -q "layer_a" "$AGENT_FILE"
check "Contradictions have layer_a field" $?

grep -q "layer_b" "$AGENT_FILE"
check "Contradictions have layer_b field" $?

# Layer objects must have file, line, text
grep -qE '"file"' "$AGENT_FILE"
check "Layer objects have file field" $?

grep -qE '"line"' "$AGENT_FILE"
check "Layer objects have line field" $?

grep -qE '"text"' "$AGENT_FILE"
check "Layer objects have text field" $?

# Gaps must have layer, missing, source_of_truth
grep -qE '"missing"' "$AGENT_FILE"
check "Gaps have missing field" $?

grep -q "source_of_truth" "$AGENT_FILE"
check "Gaps have source_of_truth field" $?

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
