#!/bin/bash
# STORY-112 AC#2: Parallel Phase 0 Context Loading
# Tests that 6 context files are loaded in parallel using single message with 6 Read calls

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Test files to validate
PARALLEL_LOADER_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/references/parallel-context-loader.md"
PREFLIGHT_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-development/references/preflight-validation.md"

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

# Count occurrences helper
assert_count_in_file() {
    local file="$1"
    local pattern="$2"
    local expected_count="$3"
    local description="$4"

    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAIL${NC}: $description"
        echo "       File not found: $file"
        ((TESTS_FAILED++))
        return 1
    fi

    local count
    count=$(grep -cE "$pattern" "$file" 2>/dev/null || echo "0")

    if [[ "$count" -ge "$expected_count" ]]; then
        echo -e "${GREEN}PASS${NC}: $description (found $count, expected >= $expected_count)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}: $description"
        echo "       Found $count occurrences, expected >= $expected_count"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "=============================================="
echo "STORY-112 AC#2: Parallel Phase 0 Context Loading"
echo "=============================================="
echo ""

# Test 2.1: Verify parallel context loader reference file exists with Read pattern
assert_pattern_in_file "$PARALLEL_LOADER_FILE" \
    "Read\(file_path=" \
    "Test 2.1: Parallel context loader documents Read calls"

# Test 2.2: Verify 6 Read calls documented (at least 6 occurrences)
assert_count_in_file "$PARALLEL_LOADER_FILE" \
    "Read\(file_path=" \
    6 \
    "Test 2.2: At least 6 Read calls documented"

# Test 2.3: Verify single message pattern documented
assert_pattern_in_file "$PARALLEL_LOADER_FILE" \
    "single message|single.*message|ONE message" \
    "Test 2.3: Single message pattern documented"

# Test 2.4: Verify all 6 context files are listed
assert_pattern_in_file "$PARALLEL_LOADER_FILE" \
    "tech-stack\.md" \
    "Test 2.4a: tech-stack.md referenced"

assert_pattern_in_file "$PARALLEL_LOADER_FILE" \
    "source-tree\.md" \
    "Test 2.4b: source-tree.md referenced"

assert_pattern_in_file "$PARALLEL_LOADER_FILE" \
    "dependencies\.md" \
    "Test 2.4c: dependencies.md referenced"

assert_pattern_in_file "$PARALLEL_LOADER_FILE" \
    "coding-standards\.md" \
    "Test 2.4d: coding-standards.md referenced"

assert_pattern_in_file "$PARALLEL_LOADER_FILE" \
    "architecture-constraints\.md" \
    "Test 2.4e: architecture-constraints.md referenced"

assert_pattern_in_file "$PARALLEL_LOADER_FILE" \
    "anti-patterns\.md" \
    "Test 2.4f: anti-patterns.md referenced"

# Test 2.5: Verify parallel loading referenced in preflight validation
assert_pattern_in_file "$PREFLIGHT_FILE" \
    "parallel-context-loader\.md|parallel.*context.*load" \
    "Test 2.5: Preflight validation references parallel context loader"

# Test 2.6: Verify time savings documented
assert_pattern_in_file "$PARALLEL_LOADER_FILE" \
    "83%|35.*40%|time.*reduc|Time.*Reduc" \
    "Test 2.6: Time savings documented"

echo ""
echo "=============================================="
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed"
echo "=============================================="

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
fi
exit 0
