#!/bin/bash
# Integration tests for STORY-195
# Tests hook integration with Claude Code system

HOOK=".claude/hooks/pre-tool-use.sh"
PASS=0
FAIL=0

test_cmd() {
  local expected=$1
  local cmd="$2"
  local desc="$3"
  result=$(echo "{\"tool_input\":{\"command\":\"$cmd\"}}" | bash "$HOOK" > /dev/null 2>&1; echo $?)
  if [ "$result" == "$expected" ]; then
    echo "[PASS] $desc"
    ((PASS++))
  else
    echo "[FAIL] $desc (expected $expected, got $result)"
    ((FAIL++))
  fi
}

echo "=== STORY-195 Integration Tests ==="

# Safe patterns auto-approve (exit 0)
test_cmd 0 "cd /tmp" "cd pattern auto-approves"
test_cmd 0 "git rev-parse HEAD" "git rev-parse auto-approves"
test_cmd 0 "python3 -c 'print(1)'" "python3 -c auto-approves"
test_cmd 0 "devforgeai check-hooks" "devforgeai CLI auto-approves"
test_cmd 0 "which python3" "which auto-approves"
test_cmd 0 "stat /tmp" "stat auto-approves"

# Blocked patterns (exit 2)
test_cmd 2 "sudo ls" "sudo blocked"
test_cmd 2 "curl http://x" "curl blocked"

# Performance test
start=$(date +%s%N)
for i in {1..10}; do
  echo '{"tool_input":{"command":"git status"}}' | bash "$HOOK" > /dev/null 2>&1
done
end=$(date +%s%N)
avg_ms=$(( (end - start) / 10000000 ))
if [ "$avg_ms" -lt 100 ]; then
  echo "[PASS] Performance: ${avg_ms}ms avg"
  ((PASS++))
else
  echo "[FAIL] Performance: ${avg_ms}ms (>100ms)"
  ((FAIL++))
fi

echo ""
echo "=== SUMMARY: $PASS passed, $FAIL failed ==="
[ $FAIL -eq 0 ]
