#!/bin/bash
# AC#3: Core Agent File Size Limit
# Verifies alignment-auditor.md ≤500 lines and validation-matrix.md exists separately

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

# Core file ≤ 500 lines
LINE_COUNT=$(wc -l < "$AGENT_FILE")
if [ "$LINE_COUNT" -le 500 ]; then
  echo "PASS: Core file is $LINE_COUNT lines (≤500)"
  PASS=$((PASS + 1))
else
  echo "FAIL: Core file is $LINE_COUNT lines (exceeds 500)"
  FAIL=$((FAIL + 1))
fi

# Validation matrix reference file exists
if [ -f "$MATRIX_FILE" ]; then
  echo "PASS: validation-matrix.md exists"
  PASS=$((PASS + 1))
else
  echo "FAIL: validation-matrix.md does not exist at $MATRIX_FILE"
  FAIL=$((FAIL + 1))
fi

# Matrix file is non-empty
if [ -f "$MATRIX_FILE" ] && [ -s "$MATRIX_FILE" ]; then
  echo "PASS: validation-matrix.md is non-empty"
  PASS=$((PASS + 1))
else
  echo "FAIL: validation-matrix.md is empty or missing"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
