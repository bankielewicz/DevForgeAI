#!/bin/bash
# AC#10: Validation Matrix On-Demand Loading
# Verifies Read() instruction present and no inline check definitions in core

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

# Workflow must contain Read() instruction for validation-matrix.md
grep -qE "Read.*validation-matrix" "$AGENT_FILE"
check "Workflow contains Read() for validation-matrix.md" $?

# Core file must NOT inline CC-01 through CC-10 check definitions
# (A few references are OK, but full definitions with method/example_finding should be in matrix)
CC_COUNT=$(grep -c "CC-0[1-9]\|CC-10" "$AGENT_FILE")
if [ "$CC_COUNT" -le 5 ]; then
  echo "PASS: Core file has $CC_COUNT CC references (≤5, not inlined)"
  PASS=$((PASS + 1))
else
  echo "FAIL: Core file has $CC_COUNT CC references (>5, likely inlined)"
  FAIL=$((FAIL + 1))
fi

# Matrix file must exist and be self-contained
if [ -f "$MATRIX_FILE" ]; then
  MATRIX_CC_COUNT=$(grep -c "CC-0[1-9]\|CC-10" "$MATRIX_FILE")
  if [ "$MATRIX_CC_COUNT" -ge 10 ]; then
    echo "PASS: Matrix file has $MATRIX_CC_COUNT CC references (contains definitions)"
    PASS=$((PASS + 1))
  else
    echo "FAIL: Matrix file has only $MATRIX_CC_COUNT CC references (incomplete)"
    FAIL=$((FAIL + 1))
  fi
else
  echo "FAIL: Matrix file does not exist"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
