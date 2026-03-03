#!/bin/bash
# AC#6: JSON Output Schema Compliance
# Verifies output format matches Appendix A schema

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

# Required JSON fields in output
grep -q "protocol_version" "$AGENT_FILE"
check "JSON field: protocol_version" $?

grep -q "timestamp" "$AGENT_FILE"
check "JSON field: timestamp" $?

grep -q "project" "$AGENT_FILE"
check "JSON field: project" $?

grep -q "layers_found" "$AGENT_FILE"
check "JSON field: layers_found" $?

grep -q "contradictions" "$AGENT_FILE"
check "JSON field: contradictions" $?

grep -q "gaps" "$AGENT_FILE"
check "JSON field: gaps" $?

grep -q "adr_propagation" "$AGENT_FILE"
check "JSON field: adr_propagation" $?

grep -q "summary" "$AGENT_FILE"
check "JSON field: summary" $?

# Overall status values
grep -q "PASS" "$AGENT_FILE"
check "Status value: PASS" $?

grep -q "FINDINGS_DETECTED" "$AGENT_FILE"
check "Status value: FINDINGS_DETECTED" $?

grep -q "CRITICAL_FINDINGS" "$AGENT_FILE"
check "Status value: CRITICAL_FINDINGS" $?

# protocol_version must be "1.0"
grep -qE '"1\.0"' "$AGENT_FILE"
check "protocol_version value is 1.0" $?

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
