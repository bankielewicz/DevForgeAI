#!/bin/bash
# STORY-112 AC#3: Background Task Result Retrieval
# Tests that TaskOutput is used with block=true before phase transitions

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Test files to validate
RESULT_AGGREGATION_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/references/task-result-aggregation.md"
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
echo "STORY-112 AC#3: Background Task Result Retrieval"
echo "=============================================="
echo ""

# Test 3.1: Verify TaskOutput pattern documented
assert_pattern_in_file "$RESULT_AGGREGATION_FILE" \
    "TaskOutput" \
    "Test 3.1: TaskOutput pattern documented in result aggregation"

# Test 3.2: Verify block=true parameter documented
assert_pattern_in_file "$RESULT_AGGREGATION_FILE" \
    "block.*=.*true|block=true" \
    "Test 3.2: block=true parameter documented"

# Test 3.3: Verify blocking retrieval before phase transition
assert_pattern_in_file "$RESULT_AGGREGATION_FILE" \
    "phase.*transition|checkpoint|before.*proceed|BEFORE.*PHASE" \
    "Test 3.3: Blocking retrieval before phase transition documented"

# Test 3.4: Verify task_id usage in TaskOutput
assert_pattern_in_file "$RESULT_AGGREGATION_FILE" \
    "task_id|task\.id" \
    "Test 3.4: task_id parameter usage documented"

# Test 3.5: Verify result aggregation pattern exists
assert_pattern_in_file "$RESULT_AGGREGATION_FILE" \
    "aggregate|result.*aggregat|Result.*Aggregat" \
    "Test 3.5: Result aggregation pattern documented"

# Test 3.6: Verify error status handling
assert_pattern_in_file "$RESULT_AGGREGATION_FILE" \
    "error|timeout|failure|Error|Timeout|Failure" \
    "Test 3.6: Error/timeout/failure handling documented"

# Test 3.7: Verify TaskOutput referenced in green phase
assert_pattern_in_file "$GREEN_PHASE_FILE" \
    "TaskOutput|task.*result|background.*result" \
    "Test 3.7: TaskOutput or result retrieval referenced in green phase"

# Test 3.8: Verify wait/block before phase checkpoint
assert_pattern_in_file "$GREEN_PHASE_FILE" \
    "wait.*background|Wait.*background|block.*true|WAIT" \
    "Test 3.8: Wait for background documented in green phase"

echo ""
echo "=============================================="
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
echo "=============================================="

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
fi
exit 0
