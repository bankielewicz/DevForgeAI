#!/bin/bash
# AC#2: Model and Tool Configuration
# Verifies frontmatter: model=haiku, tools=[Read, Glob, Grep], name=alignment-auditor, version semver

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

# Extract frontmatter (between first two --- markers)
FRONTMATTER=$(sed -n '/^---$/,/^---$/p' "$AGENT_FILE")

# model: haiku
echo "$FRONTMATTER" | grep -qE "^model:\s*haiku"
check "model field is haiku" $?

# name: alignment-auditor
echo "$FRONTMATTER" | grep -qE "^name:\s*alignment-auditor"
check "name field is alignment-auditor" $?

# version in semver format
echo "$FRONTMATTER" | grep -qE "^version:\s*\"?[0-9]+\.[0-9]+\.[0-9]+\"?"
check "version field in semver format" $?

# tools array contains Read
echo "$FRONTMATTER" | grep -qE "^\s*-\s*Read"
check "tools array contains Read" $?

# tools array contains Glob
echo "$FRONTMATTER" | grep -qE "^\s*-\s*Glob"
check "tools array contains Glob" $?

# tools array contains Grep
echo "$FRONTMATTER" | grep -qE "^\s*-\s*Grep"
check "tools array contains Grep" $?

# tools array must NOT contain Write
echo "$FRONTMATTER" | grep -qE "^\s*-\s*Write"
if [ $? -ne 0 ]; then
  echo "PASS: tools array does NOT contain Write"
  PASS=$((PASS + 1))
else
  echo "FAIL: tools array contains Write (forbidden)"
  FAIL=$((FAIL + 1))
fi

# tools array must NOT contain Edit
echo "$FRONTMATTER" | grep -qE "^\s*-\s*Edit"
if [ $? -ne 0 ]; then
  echo "PASS: tools array does NOT contain Edit"
  PASS=$((PASS + 1))
else
  echo "FAIL: tools array contains Edit (forbidden)"
  FAIL=$((FAIL + 1))
fi

# tools array must NOT contain Bash
echo "$FRONTMATTER" | grep -qE "^\s*-\s*Bash"
if [ $? -ne 0 ]; then
  echo "PASS: tools array does NOT contain Bash"
  PASS=$((PASS + 1))
else
  echo "FAIL: tools array contains Bash (forbidden)"
  FAIL=$((FAIL + 1))
fi

# Exactly 3 tools
TOOL_COUNT=$(echo "$FRONTMATTER" | grep -cE "^\s*-\s*(Read|Glob|Grep|Write|Edit|Bash|WebFetch|WebSearch|AskUserQuestion)")
if [ "$TOOL_COUNT" -eq 3 ]; then
  echo "PASS: Exactly 3 tools in array"
  PASS=$((PASS + 1))
else
  echo "FAIL: Expected 3 tools, found $TOOL_COUNT"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
