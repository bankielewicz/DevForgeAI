#!/bin/bash
# AC#9: Exact Text Matching (No Semantic Similarity)
# Verifies agent uses exact matching and prohibits semantic similarity

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_FILE="$PROJECT_ROOT/src/claude/agents/alignment-auditor.md"
MATRIX_FILE="$PROJECT_ROOT/src/claude/agents/alignment-auditor/references/validation-matrix.md"

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

# Agent must state "exact text matching"
grep -qi "exact text matching" "$AGENT_FILE"
check "Agent states exact text matching" $?

# Agent must prohibit semantic similarity
grep -qiE "no semantic|prohibit.*semantic|never.*semantic|not.*semantic" "$AGENT_FILE"
check "Agent prohibits semantic similarity" $?

# Validation matrix should reference Grep with literal patterns
if [ -f "$MATRIX_FILE" ]; then
  grep -qi "Grep" "$MATRIX_FILE"
  check "Matrix references Grep for method" $?
else
  echo "FAIL: Matrix file not found for Grep check"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
