#!/bin/bash
# STORY-112 AC#4: Long Operation Handling (Threshold-Based Execution)
# Tests that operations > 2 minutes use background, < 30 seconds use foreground

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Test files to validate
BACKGROUND_EXECUTOR_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/references/background-executor.md"
GREEN_PHASE_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/references/tdd-green-phase.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

# Test helper function
assert_pattern_in_file() {
    local file="$1"
    local pattern="$2"
    local description="$3"

    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAIL${NC}: $description"
        echo "       File not found: $file"
        ((TESTS_FAILED++))
        return 1
    fi

    if grep -qE "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "       Pattern not found: $pattern"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "=============================================="
echo "STORY-112 AC#4: Threshold-Based Execution"
echo "=============================================="
echo ""

# Test 4.1: Verify 2-minute background threshold documented
assert_pattern_in_file "$BACKGROUND_EXECUTOR_FILE" \
    "120000|2.*min|> 2|>2" \
    "Test 4.1: 2-minute (120000ms) background threshold documented"

# Test 4.2: Verify 30-second foreground threshold documented
assert_pattern_in_file "$BACKGROUND_EXECUTOR_FILE" \
    "30000|30.*sec|< 30|<30" \
    "Test 4.2: 30-second (30000ms) foreground threshold documented"

# Test 4.3: Verify threshold decision logic
assert_pattern_in_file "$BACKGROUND_EXECUTOR_FILE" \
    "IF.*duration|IF.*threshold|duration.*>|estimated" \
    "Test 4.3: Threshold decision logic documented"

# Test 4.4: Verify foreground execution for short operations
assert_pattern_in_file "$BACKGROUND_EXECUTOR_FILE" \
    "foreground|Foreground|FOREGROUND" \
    "Test 4.4: Foreground execution path documented"

# Test 4.5: Verify background execution for long operations
assert_pattern_in_file "$BACKGROUND_EXECUTOR_FILE" \
    "background|Background|BACKGROUND" \
    "Test 4.5: Background execution path documented"

# Test 4.6: Verify timeout from config integration
assert_pattern_in_file "$BACKGROUND_EXECUTOR_FILE" \
    "timeout_ms|timeout.*config|parallel-orchestration\.yaml|config.*timeout" \
    "Test 4.6: Timeout from config documented"

# Test 4.7: Verify duration estimation
assert_pattern_in_file "$BACKGROUND_EXECUTOR_FILE" \
    "estimat|Estimat|heuristic|Heuristic|historical" \
    "Test 4.7: Duration estimation approach documented"

# Test 4.8: Verify conditional execution in green phase
assert_pattern_in_file "$GREEN_PHASE_FILE" \
    "IF.*duration|IF.*threshold|CONDITIONAL|conditional" \
    "Test 4.8: Conditional execution documented in green phase"

echo ""
echo "=============================================="
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
echo "=============================================="

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
fi
exit 0
