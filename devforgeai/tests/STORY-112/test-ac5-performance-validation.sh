#!/bin/bash
# STORY-112 AC#5: Time Reduction Validation
# Tests that 50-80% reduction in perceived test wait time is documented

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Test files to validate
BACKGROUND_EXECUTOR_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/references/background-executor.md"
PARALLEL_LOADER_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/references/parallel-context-loader.md"
RESULT_AGGREGATION_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/references/task-result-aggregation.md"

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

# Check any of multiple files for pattern
assert_pattern_in_any_file() {
    local pattern="$1"
    local description="$2"
    shift 2
    local files=("$@")

    for file in "${files[@]}"; do
        if [[ -f "$file" ]] && grep -qiE "$pattern" "$file" 2>/dev/null; then
            echo -e "${GREEN}PASS${NC}: $description (found in $(basename "$file"))"
            ((TESTS_PASSED++))
            return 0
        fi
    done

    echo -e "${RED}FAIL${NC}: $description"
    echo "       Pattern not found in any reference file: $pattern"
    ((TESTS_FAILED++))
    return 1
}

echo "=============================================="
echo "STORY-112 AC#5: Time Reduction Validation"
echo "=============================================="
echo ""

# Test 5.1: Verify 50-80% target range documented
assert_pattern_in_any_file \
    "50.*80%|50-80%|50%.*80%|50 to 80" \
    "Test 5.1: 50-80% performance target documented" \
    "$BACKGROUND_EXECUTOR_FILE" "$PARALLEL_LOADER_FILE" "$RESULT_AGGREGATION_FILE"

# Test 5.2: Verify baseline measurement concept
assert_pattern_in_any_file \
    "baseline|Baseline|sequential|Sequential" \
    "Test 5.2: Baseline/sequential measurement documented" \
    "$BACKGROUND_EXECUTOR_FILE" "$PARALLEL_LOADER_FILE"

# Test 5.3: Verify time savings for context loading (83% from STORY-111)
assert_pattern_in_file "$PARALLEL_LOADER_FILE" \
    "83%|35.*40%|time.*sav|Time.*Sav|reduction" \
    "Test 5.3: Context loading time savings documented (83% or 35-40%)"

# Test 5.4: Verify performance calculation formula concept
assert_pattern_in_any_file \
    "Reduction.*=|reduction.*calculation|improvement|Improvement" \
    "Test 5.4: Performance improvement documented" \
    "$BACKGROUND_EXECUTOR_FILE" "$PARALLEL_LOADER_FILE"

# Test 5.5: Verify zero additional token consumption goal
assert_pattern_in_any_file \
    "zero.*token|same.*token|token.*overhead|no.*additional" \
    "Test 5.5: Zero additional token consumption documented" \
    "$BACKGROUND_EXECUTOR_FILE" "$RESULT_AGGREGATION_FILE"

# Test 5.6: Verify wait time reduction benefit documented
assert_pattern_in_any_file \
    "wait.*time|Wait.*time|perceived.*time|terminal.*block|not.*block" \
    "Test 5.6: Wait time reduction benefit documented" \
    "$BACKGROUND_EXECUTOR_FILE" "$RESULT_AGGREGATION_FILE"

echo ""
echo "=============================================="
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
echo "=============================================="

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
fi
exit 0
