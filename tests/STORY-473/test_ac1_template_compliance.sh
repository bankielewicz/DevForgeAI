#!/bin/bash
# AC#1: Canonical Agent Template v2.0.0 Compliance
# Verifies alignment-auditor.md has all 10 required sections + Validator optional sections

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

# File must exist
if [ ! -f "$AGENT_FILE" ]; then
  echo "FAIL: Agent file does not exist: $AGENT_FILE"
  echo ""
  echo "Results: 0 passed, 1 failed"
  exit 1
fi

# 10 Required sections
grep -q "^---" "$AGENT_FILE"
check "Section 1: YAML Frontmatter present" $?

grep -qE "^# " "$AGENT_FILE"
check "Section 2: Title (H1) present" $?

grep -qE "^## Purpose" "$AGENT_FILE"
check "Section 3: Purpose section present" $?

grep -qE "^## When Invoked" "$AGENT_FILE"
check "Section 4: When Invoked section present" $?

grep -qE "^## Input/Output Specification" "$AGENT_FILE"
check "Section 5: Input/Output Specification present" $?

grep -qE "^## Constraints and Boundaries" "$AGENT_FILE"
check "Section 6: Constraints and Boundaries present" $?

grep -qE "^## Workflow" "$AGENT_FILE"
check "Section 7: Workflow section present" $?

grep -qE "^## Success Criteria" "$AGENT_FILE"
check "Section 8: Success Criteria present" $?

grep -qE "^## Output Format" "$AGENT_FILE"
check "Section 9: Output Format present" $?

grep -qE "^## Examples" "$AGENT_FILE"
check "Section 10: Examples section present" $?

# Validator-category optional sections
grep -qE "^## Validation Rules|^### Validation Rules" "$AGENT_FILE"
check "Validator optional: Validation Rules present" $?

grep -qE "^## Severity Classification|^### Severity Classification" "$AGENT_FILE"
check "Validator optional: Severity Classification present" $?

grep -qE "^## Pass/Fail Criteria|^### Pass/Fail Criteria" "$AGENT_FILE"
check "Validator optional: Pass/Fail Criteria present" $?

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
