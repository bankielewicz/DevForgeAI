#!/bin/bash
# STORY-112 AC#1: Background Test Execution
# Tests that the development skill runs tests in background with run_in_background=true

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Test files to validate
GREEN_PHASE_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/references/tdd-green-phase.md"
BACKGROUND_EXECUTOR_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/references/background-executor.md"

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
echo "STORY-112 AC#1: Background Test Execution"
echo "=============================================="
echo ""

# Test 1.1: Verify run_in_background=true parameter documented in green phase
assert_pattern_in_file "$GREEN_PHASE_FILE" \
    "run_in_background.*=.*true|run_in_background=true" \
    "Test 1.1: Background execution parameter documented in tdd-green-phase.md"

# Test 1.2: Verify background executor reference file exists
assert_pattern_in_file "$BACKGROUND_EXECUTOR_FILE" \
    "run_in_background" \
    "Test 1.2: Background executor reference file documents run_in_background"

# Test 1.3: Verify Bash command pattern for background execution
assert_pattern_in_file "$BACKGROUND_EXECUTOR_FILE" \
    "Bash.*command.*run_in_background|Bash\(.*run_in_background" \
    "Test 1.3: Bash command with background flag pattern documented"

# Test 1.4: Verify task ID capture for later retrieval
assert_pattern_in_file "$BACKGROUND_EXECUTOR_FILE" \
    "task_id|task\.id|task ID" \
    "Test 1.4: Task ID capture documented for result retrieval"

# Test 1.5: Verify background execution is conditional on duration
assert_pattern_in_file "$GREEN_PHASE_FILE" \
    "Step 4a.*CONDITIONAL|CONDITIONAL.*Step 4a|Background.*CONDITIONAL|Step 4a:.*Background" \
    "Test 1.5: Background execution is conditional (Step 4a)"

echo ""
echo "=============================================="
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
echo "=============================================="

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
fi
exit 0
