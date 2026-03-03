#!/bin/bash
# tests/STORY-195/test-safe-patterns.sh
# Test suite for STORY-195: Common Command Composition Patterns
# Tests the 15 new safe patterns added per RCA-015

set -euo pipefail

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HOOK_SCRIPT="$PROJECT_ROOT/.claude/hooks/pre-tool-use.sh"

# Test counters
PASS=0
FAIL=0
TOTAL=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test helper functions
log_test() {
  echo -e "${YELLOW}TEST:${NC} $1"
}

log_pass() {
  echo -e "${GREEN}PASS:${NC} $1"
  ((PASS++))
  ((TOTAL++))
}

log_fail() {
  echo -e "${RED}FAIL:${NC} $1"
  ((FAIL++))
  ((TOTAL++))
}

# Core test function: test a command against expected exit code
# Exit codes: 0=auto-approve, 1=ask user, 2=block
test_command() {
  local expected_exit=$1
  local command="$2"
  local description="$3"

  log_test "$description"

  # Create JSON input for the hook
  local json_input='{"tool_input":{"command":"'"$command"'"}}'

  # Run hook script with JSON input, capture exit code
  echo "$json_input" | bash "$HOOK_SCRIPT" > /dev/null 2>&1
  local actual_exit=$?

  if [ $actual_exit -eq $expected_exit ]; then
    log_pass "$description (exit $actual_exit)"
    return 0
  else
    log_fail "$description - expected exit $expected_exit, got $actual_exit"
    return 1
  fi
}

# Verify pattern exists in SAFE_PATTERNS array
test_pattern_exists() {
  local pattern="$1"
  local description="$2"

  log_test "$description"

  if grep -qF "\"$pattern\"" "$HOOK_SCRIPT"; then
    log_pass "$description"
    return 0
  else
    log_fail "$description - pattern '$pattern' not found in SAFE_PATTERNS"
    return 1
  fi
}

# Verify comment exists
test_comment_exists() {
  local comment_pattern="$1"
  local description="$2"

  log_test "$description"

  if grep -qE "$comment_pattern" "$HOOK_SCRIPT"; then
    log_pass "$description"
    return 0
  else
    log_fail "$description - comment pattern '$comment_pattern' not found"
    return 1
  fi
}

# Count patterns in SAFE_PATTERNS array
count_safe_patterns() {
  # Count lines between SAFE_PATTERNS=( and the closing )
  # Exclude comments and empty lines
  local count=$(sed -n '/^SAFE_PATTERNS=(/,/^)/p' "$HOOK_SCRIPT" | \
                grep -E '^\s*"[^"]+"\s*$|^\s*"[^"]+"\s*#' | \
                wc -l)
  echo "$count"
}

echo "=============================================="
echo "STORY-195: Common Command Composition Patterns"
echo "Test Suite for pre-tool-use.sh Hook"
echo "=============================================="
echo ""
echo "Hook script: $HOOK_SCRIPT"
echo ""

# Verify hook script exists
if [ ! -f "$HOOK_SCRIPT" ]; then
  echo -e "${RED}ERROR:${NC} Hook script not found at $HOOK_SCRIPT"
  exit 1
fi

# Verify hook script is executable
if [ ! -x "$HOOK_SCRIPT" ]; then
  echo -e "${YELLOW}WARNING:${NC} Hook script is not executable, making it executable"
  chmod +x "$HOOK_SCRIPT"
fi

echo "=============================================="
echo "AC#1: Common Pattern Addition Verification"
echo "=============================================="
echo ""

# Test: RCA-015 comment header exists
test_comment_exists "RCA-015.*reduces.*approval friction" \
  "AC#1.1: RCA-015 comment header exists"

# Test: All 15 new patterns are present
test_pattern_exists "cd " \
  "AC#1.2: Pattern 'cd ' exists"

test_pattern_exists "python3 -c " \
  "AC#1.3: Pattern 'python3 -c ' exists"

test_pattern_exists "python3 << 'EOF'" \
  "AC#1.4: Pattern 'python3 << EOF' exists"

test_pattern_exists "python << 'EOF'" \
  "AC#1.5: Pattern 'python << EOF' exists"

test_pattern_exists "devforgeai " \
  "AC#1.6: Pattern 'devforgeai ' exists"

test_pattern_exists "git rev-parse" \
  "AC#1.7: Pattern 'git rev-parse' exists"

test_pattern_exists "git branch" \
  "AC#1.8: Pattern 'git branch' exists"

test_pattern_exists "git --version" \
  "AC#1.9: Pattern 'git --version' exists"

test_pattern_exists "git rev-list" \
  "AC#1.10: Pattern 'git rev-list' exists"

test_pattern_exists "which " \
  "AC#1.11: Pattern 'which ' exists"

test_pattern_exists "command -v" \
  "AC#1.12: Pattern 'command -v' exists"

test_pattern_exists "type " \
  "AC#1.13: Pattern 'type ' exists"

test_pattern_exists "stat " \
  "AC#1.14: Pattern 'stat ' exists"

test_pattern_exists "file " \
  "AC#1.15: Pattern 'file ' exists"

test_pattern_exists "basename " \
  "AC#1.16: Pattern 'basename ' exists"

# Test: Original patterns preserved (count should be 65+ patterns)
echo ""
log_test "AC#1.17: Original patterns preserved (65+ total patterns)"
PATTERN_COUNT=$(count_safe_patterns)
if [ "$PATTERN_COUNT" -ge 65 ]; then
  log_pass "AC#1.17: Total patterns count is $PATTERN_COUNT (>= 65)"
else
  log_fail "AC#1.17: Expected >= 65 patterns, found $PATTERN_COUNT"
fi

echo ""
echo "=============================================="
echo "AC#2: Directory Change Pattern Support"
echo "=============================================="
echo ""

# Test: cd /tmp should auto-approve (exit 0)
test_command 0 "cd /tmp" \
  "AC#2.1: 'cd /tmp' should auto-approve"

# Test: cd /mnt/c/Projects && ls should auto-approve
test_command 0 "cd /mnt/c/Projects && ls" \
  "AC#2.2: 'cd /mnt/c/Projects && ls' should auto-approve"

# Test: cd with relative path
test_command 0 "cd .." \
  "AC#2.3: 'cd ..' should auto-approve"

# Test: cd with quoted path containing spaces
test_command 0 "cd '/path/with spaces'" \
  "AC#2.4: 'cd /path/with spaces' should auto-approve"

# Test: cd to home directory
test_command 0 "cd ~" \
  "AC#2.5: 'cd ~' should auto-approve"

# Verify log output mentions matched pattern
echo ""
log_test "AC#2.6: Log shows matched pattern 'cd '"
# Run the command and check log file
LOG_FILE="$PROJECT_ROOT/devforgeai/logs/pre-tool-use.log"
echo '{"tool_input":{"command":"cd /tmp"}}' | bash "$HOOK_SCRIPT" > /dev/null 2>&1
if grep -q "MATCHED safe pattern: 'cd '" "$LOG_FILE" 2>/dev/null; then
  log_pass "AC#2.6: Log shows 'MATCHED safe pattern: cd '"
else
  log_fail "AC#2.6: Log does not show expected pattern match"
fi

echo ""
echo "=============================================="
echo "AC#3: Python Inline Script Pattern Support"
echo "=============================================="
echo ""

# Test: python3 -c 'print(1)' should auto-approve
test_command 0 "python3 -c 'print(1)'" \
  "AC#3.1: 'python3 -c print(1)' should auto-approve"

# Test: python3 -c with more complex script
test_command 0 "python3 -c 'import sys; print(sys.version)'" \
  "AC#3.2: 'python3 -c import sys' should auto-approve"

# Test: python3 HERE-document
test_command 0 "python3 << 'EOF'
print(1)
EOF" \
  "AC#3.3: 'python3 << EOF' HERE-doc should auto-approve"

# Test: python (Python 2) HERE-document
test_command 0 "python << 'EOF'
print 1
EOF" \
  "AC#3.4: 'python << EOF' HERE-doc should auto-approve"

# Test: python3 -c with JSON processing
test_command 0 "python3 -c 'import json; print(json.dumps({\"key\": \"value\"}))'" \
  "AC#3.5: 'python3 -c' with JSON processing should auto-approve"

echo ""
echo "=============================================="
echo "AC#4: Framework CLI Pattern Support"
echo "=============================================="
echo ""

# Test: devforgeai check-hooks should auto-approve
test_command 0 "devforgeai check-hooks" \
  "AC#4.1: 'devforgeai check-hooks' should auto-approve"

# Test: devforgeai validate-context should auto-approve
test_command 0 "devforgeai validate-context" \
  "AC#4.2: 'devforgeai validate-context' should auto-approve"

# Test: devforgeai with subcommand and flags
test_command 0 "devforgeai phase-init STORY-195 --project-root=." \
  "AC#4.3: 'devforgeai phase-init' with args should auto-approve"

# Test: devforgeai-validate (hyphenated variant)
test_command 0 "devforgeai phase-status STORY-195" \
  "AC#4.4: 'devforgeai phase-status' should auto-approve"

echo ""
echo "=============================================="
echo "AC#5: Git Introspection Pattern Support"
echo "=============================================="
echo ""

# Test: git rev-parse HEAD should auto-approve
test_command 0 "git rev-parse HEAD" \
  "AC#5.1: 'git rev-parse HEAD' should auto-approve"

# Test: git rev-parse --abbrev-ref HEAD
test_command 0 "git rev-parse --abbrev-ref HEAD" \
  "AC#5.2: 'git rev-parse --abbrev-ref HEAD' should auto-approve"

# Test: git branch -a should auto-approve
test_command 0 "git branch -a" \
  "AC#5.3: 'git branch -a' should auto-approve"

# Test: git branch (list only)
test_command 0 "git branch" \
  "AC#5.4: 'git branch' should auto-approve"

# Test: git --version should auto-approve
test_command 0 "git --version" \
  "AC#5.5: 'git --version' should auto-approve"

# Test: git rev-list HEAD --count should auto-approve
test_command 0 "git rev-list HEAD --count" \
  "AC#5.6: 'git rev-list HEAD --count' should auto-approve"

# Test: git rev-list with range
test_command 0 "git rev-list main..HEAD" \
  "AC#5.7: 'git rev-list main..HEAD' should auto-approve"

echo ""
echo "=============================================="
echo "AC#6: Utility Command Pattern Support"
echo "=============================================="
echo ""

# Test: which command
test_command 0 "which python3" \
  "AC#6.1: 'which python3' should auto-approve"

# Test: command -v
test_command 0 "command -v git" \
  "AC#6.2: 'command -v git' should auto-approve"

# Test: type command
test_command 0 "type bash" \
  "AC#6.3: 'type bash' should auto-approve"

# Test: stat command
test_command 0 "stat /tmp" \
  "AC#6.4: 'stat /tmp' should auto-approve"

# Test: file command
test_command 0 "file /bin/bash" \
  "AC#6.5: 'file /bin/bash' should auto-approve"

# Test: basename command
test_command 0 "basename /path/to/file.txt" \
  "AC#6.6: 'basename /path/to/file.txt' should auto-approve"

echo ""
echo "=============================================="
echo "AC#7: Composition and Edge Cases"
echo "=============================================="
echo ""

# Test: cd with piped command (safe base + pipe)
test_command 0 "cd /tmp && ls -la" \
  "AC#7.1: 'cd /tmp && ls -la' composition should auto-approve"

# Test: git rev-parse with pipe
test_command 0 "git rev-parse --show-toplevel | head -1" \
  "AC#7.2: 'git rev-parse | head' composition should auto-approve"

# Test: which with command substitution usage context
test_command 0 "which python3" \
  "AC#7.3: 'which' for path discovery should auto-approve"

# Test: stat with redirect (should check redirect safety)
test_command 0 "stat /tmp > /dev/null" \
  "AC#7.4: 'stat > /dev/null' safe redirect should auto-approve"

# Test: Multiple cd commands chained
test_command 0 "cd /tmp && cd /var && pwd" \
  "AC#7.5: Multiple 'cd' commands chained should auto-approve"

echo ""
echo "=============================================="
echo "AC#8: Negative Tests (Should NOT Auto-Approve)"
echo "=============================================="
echo ""

# These tests verify that dangerous commands are still blocked
# even when combined with safe patterns

# Test: rm -rf should be blocked (exit 2)
test_command 2 "rm -rf /tmp/test" \
  "AC#8.1: 'rm -rf' should be BLOCKED (exit 2)"

# Test: sudo should be blocked
test_command 2 "sudo ls" \
  "AC#8.2: 'sudo' should be BLOCKED (exit 2)"

# Test: git push should be blocked
test_command 2 "git push origin main" \
  "AC#8.3: 'git push' should be BLOCKED (exit 2)"

# Test: curl should be blocked
test_command 2 "curl https://example.com" \
  "AC#8.4: 'curl' should be BLOCKED (exit 2)"

# Test: wget should be blocked
test_command 2 "wget https://example.com/file" \
  "AC#8.5: 'wget' should be BLOCKED (exit 2)"

# Test: npm publish should be blocked
test_command 2 "npm publish" \
  "AC#8.6: 'npm publish' should be BLOCKED (exit 2)"

# Test: Safe base with dangerous pipe should be blocked
test_command 2 "cd /tmp | rm -rf /var" \
  "AC#8.7: Safe base with 'rm -rf' in pipe should be BLOCKED"

echo ""
echo "=============================================="
echo "AC#9: System Directory Redirect Protection"
echo "=============================================="
echo ""

# Test: Redirect to /etc should be blocked
test_command 2 "echo test > /etc/passwd" \
  "AC#9.1: Redirect to /etc/ should be BLOCKED"

# Test: Redirect to /usr should be blocked
test_command 2 "echo test > /usr/local/test" \
  "AC#9.2: Redirect to /usr/ should be BLOCKED"

# Test: Redirect to /sys should be blocked
test_command 2 "echo test > /sys/test" \
  "AC#9.3: Redirect to /sys/ should be BLOCKED"

echo ""
echo "=============================================="
echo "AC#10: Pre-existing Patterns Still Work"
echo "=============================================="
echo ""

# Verify some original patterns still work
test_command 0 "git status" \
  "AC#10.1: Original 'git status' pattern works"

test_command 0 "git diff" \
  "AC#10.2: Original 'git diff' pattern works"

test_command 0 "npm run test" \
  "AC#10.3: Original 'npm run test' pattern works"

test_command 0 "dotnet test" \
  "AC#10.4: Original 'dotnet test' pattern works"

test_command 0 "pytest" \
  "AC#10.5: Original 'pytest' pattern works"

test_command 0 "ls -la" \
  "AC#10.6: Original 'ls -la' pattern works"

echo ""
echo "=============================================="
echo "TEST SUMMARY"
echo "=============================================="
echo ""
echo -e "Total tests: ${TOTAL}"
echo -e "${GREEN}Passed: ${PASS}${NC}"
echo -e "${RED}Failed: ${FAIL}${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
  echo -e "${GREEN}ALL TESTS PASSED${NC}"
  exit 0
else
  echo -e "${RED}SOME TESTS FAILED${NC}"
  exit 1
fi
