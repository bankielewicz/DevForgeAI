#!/bin/bash
# AC#4: All 15 Validation Checks Implemented in Matrix
# Verifies all check IDs present with required fields

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
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

if [ ! -f "$MATRIX_FILE" ]; then
  echo "FAIL: Matrix file does not exist: $MATRIX_FILE"
  echo "Results: 0 passed, 1 failed"
  exit 1
fi

# Check all 15 IDs are present
for ID in CC-01 CC-02 CC-03 CC-04 CC-05 CC-06 CC-07 CC-08 CC-09 CC-10 CMP-01 CMP-02 CMP-03 CMP-04 ADR-01; do
  grep -q "$ID" "$MATRIX_FILE"
  check "Check ID $ID present in matrix" $?
done

# Verify 8 required fields exist somewhere in the matrix
for FIELD in "id" "category" "severity" "layer_a" "layer_b" "description" "method" "example_finding"; do
  grep -qi "$FIELD" "$MATRIX_FILE"
  check "Field '$FIELD' found in matrix" $?
done

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
