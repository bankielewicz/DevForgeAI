#!/bin/bash
# AC#8: Mutability-Respecting Resolutions
# Verifies resolutions never target IMMUTABLE context files

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

# Must mention mutability rules
grep -qiE "mutab|IMMUTABLE|MUTABLE" "$AGENT_FILE"
check "Agent mentions mutability rules" $?

# Must mention APPEND-ONLY for ADRs
grep -q "APPEND-ONLY" "$AGENT_FILE"
check "Agent mentions APPEND-ONLY for ADRs" $?

# Must NOT contain resolution text targeting context files
# Search for forbidden patterns in resolution contexts
grep -q "Update devforgeai/specs/context/" "$AGENT_FILE"
if [ $? -ne 0 ]; then
  echo "PASS: No resolution targets IMMUTABLE context files"
  PASS=$((PASS + 1))
else
  echo "FAIL: Found resolution targeting IMMUTABLE context files"
  FAIL=$((FAIL + 1))
fi

# Must NOT contain resolution text editing ADRs
grep -q "Edit devforgeai/specs/adrs/" "$AGENT_FILE"
if [ $? -ne 0 ]; then
  echo "PASS: No resolution edits existing ADRs"
  PASS=$((PASS + 1))
else
  echo "FAIL: Found resolution editing existing ADRs"
  FAIL=$((FAIL + 1))
fi

# Must mention "Create new ADR" for ADR drift
grep -qiE "create.*new.*ADR|new ADR" "$AGENT_FILE"
check "Agent recommends creating new ADR (not editing)" $?

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
