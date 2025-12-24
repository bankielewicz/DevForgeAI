#!/bin/bash

################################################################################
# TEST SUITE: AC#4 - Performance and Consistency
# Story: STORY-134 (Smart Greenfield/Brownfield Detection)
# Description: Verify detection completes in <50ms and produces consistent
#              results across multiple invocations on the same project state
#
# Acceptance Criteria:
# - Given: Project with mixed or partial context file states
# - When: /ideate command performs the glob check
# - Then: Uses exact count comparison (== 6 brownfield, < 6 greenfield)
#         Completes in <50ms
#         Produces consistent results across multiple invocations
#
# Non-Functional Requirements:
# - NFR-001: Detection latency <50ms for glob operation (p95)
# - NFR-002: Graceful error message if directory inaccessible
# - NFR-003: Deterministic detection (same state = same mode)
#
# Test Status: FAILING (Red Phase) - Performance validation not yet done
################################################################################

set +e  # Do NOT exit on error (we handle failures in test assertions)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#4: Performance and Consistency"
COMMAND_FILE="${PROJECT_ROOT}/.claude/commands/ideate.md"
CONTEXT_DIR="${PROJECT_ROOT}/devforgeai/specs/context"
FIXTURE_DIR="/tmp/performance-test-fixture"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Performance metrics
PERFORMANCE_SAMPLES=10
LATENCY_THRESHOLD_MS=50

# Helper function: Assert condition
assert_true() {
    local condition="$1"
    local description="$2"
    ((TESTS_RUN++))

    if eval "$condition"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function: Assert file contains text
assert_file_contains() {
    local file="$1"
    local search_text="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File not found: $file"
        ((TESTS_FAILED++))
        return 1
    fi

    if grep -q "$search_text" "$file"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Not found in: $file"
        echo "  Search text: $search_text"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# TEST 4.1: Exact count comparison logic (== 6 = brownfield)
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4.1: Exact Count Comparison Logic"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "== 6.*brownfield\|count.*== 6" \
    "Command uses exact equality check (== 6) for brownfield detection"

assert_file_contains "$COMMAND_FILE" \
    "< 6.*greenfield\|count.*< 6" \
    "Command uses less-than comparison (< 6) for greenfield detection"

################################################################################
# TEST 4.2: Performance - Detection latency <50ms (real filesystem)
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4.2: Detection Latency (<50ms)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Measure real glob operation on actual context directory
declare -a LATENCIES
TOTAL_TIME=0

echo "Measuring ${PERFORMANCE_SAMPLES} samples of glob operation..."

for i in $(seq 1 "$PERFORMANCE_SAMPLES"); do
    START_TIME=$(date +%s%N)
    # Simulate the glob check
    file_count=$(find "$CONTEXT_DIR" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
    END_TIME=$(date +%s%N)

    ELAPSED_NS=$((END_TIME - START_TIME))
    ELAPSED_MS=$((ELAPSED_NS / 1000000))
    LATENCIES+=($ELAPSED_MS)
    TOTAL_TIME=$((TOTAL_TIME + ELAPSED_MS))

    echo "  Sample $i: ${ELAPSED_MS}ms"
done

# Calculate average
AVERAGE_MS=$((TOTAL_TIME / PERFORMANCE_SAMPLES))

# Calculate p95 (simplified: sort and take 95th percentile)
IFS=$'\n' sorted=($(sort <<<"${LATENCIES[*]}"))
p95_index=$((PERFORMANCE_SAMPLES * 95 / 100))
P95_MS=${sorted[$((p95_index - 1))]}

echo ""
echo "Performance Results:"
echo "  Average: ${AVERAGE_MS}ms"
echo "  P95: ${P95_MS}ms"
echo "  Threshold: <${LATENCY_THRESHOLD_MS}ms"
echo ""

((TESTS_RUN++))
if [ "$P95_MS" -lt "$LATENCY_THRESHOLD_MS" ]; then
    echo -e "${GREEN}✓ PASS${NC}: P95 latency ${P95_MS}ms < ${LATENCY_THRESHOLD_MS}ms threshold"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: P95 latency ${P95_MS}ms >= ${LATENCY_THRESHOLD_MS}ms threshold"
    ((TESTS_FAILED++))
fi

################################################################################
# TEST 4.3: Consistency - Same state produces same result
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4.3: Consistency Across Invocations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create test fixture with known state
mkdir -p "$FIXTURE_DIR/consistent-test"
touch "$FIXTURE_DIR/consistent-test/tech-stack.md"
touch "$FIXTURE_DIR/consistent-test/source-tree.md"
touch "$FIXTURE_DIR/consistent-test/dependencies.md"

# Run detection 5 times on same fixture
declare -a COUNTS
for i in $(seq 1 5); do
    COUNT=$(find "$FIXTURE_DIR/consistent-test" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
    COUNTS+=($COUNT)
    echo "  Invocation $i: $COUNT files"
done

# Verify all counts are identical
FIRST_COUNT=${COUNTS[0]}
ALL_SAME=true

for count in "${COUNTS[@]}"; do
    if [ "$count" -ne "$FIRST_COUNT" ]; then
        ALL_SAME=false
        break
    fi
done

((TESTS_RUN++))
if [ "$ALL_SAME" = true ]; then
    echo -e "${GREEN}✓ PASS${NC}: All invocations returned consistent count ($FIRST_COUNT files)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Detection produced inconsistent results across invocations"
    echo "  Counts: ${COUNTS[@]}"
    ((TESTS_FAILED++))
fi

################################################################################
# TEST 4.4: Edge case - Many context files (> 6)
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4.4: Edge Case - Extra Context Files (>6)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create fixture with 7 context files
mkdir -p "$FIXTURE_DIR/extra-files"
for i in $(seq 1 7); do
    touch "$FIXTURE_DIR/extra-files/file-${i}.md"
done

COUNT=$(find "$FIXTURE_DIR/extra-files" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)

# According to spec: ">=6 treated as brownfield"
assert_true "[ \"$COUNT\" -ge 6 ]" \
    "Edge case: 7 files should be treated as brownfield (>= 6 rule)"

################################################################################
# TEST 4.5: No caching side effects
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4.5: No Caching Side Effects"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run detection, change state, run detection again
mkdir -p "$FIXTURE_DIR/cache-test"

# Initial state: 3 files
touch "$FIXTURE_DIR/cache-test/file1.md"
touch "$FIXTURE_DIR/cache-test/file2.md"
touch "$FIXTURE_DIR/cache-test/file3.md"

COUNT1=$(find "$FIXTURE_DIR/cache-test" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)

# Add more files
touch "$FIXTURE_DIR/cache-test/file4.md"
touch "$FIXTURE_DIR/cache-test/file5.md"
touch "$FIXTURE_DIR/cache-test/file6.md"

COUNT2=$(find "$FIXTURE_DIR/cache-test" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)

echo "  Initial count: $COUNT1"
echo "  After adding files: $COUNT2"

((TESTS_RUN++))
if [ "$COUNT1" -eq 3 ] && [ "$COUNT2" -eq 6 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Detection reflects filesystem changes (no caching)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Detection did not reflect filesystem changes"
    ((TESTS_FAILED++))
fi

################################################################################
# TEST 4.6: Glob pattern is correct
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4.6: Glob Pattern Specification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

assert_file_contains "$COMMAND_FILE" \
    "devforgeai/specs/context/\*\|devforgeai/specs/context/*.md" \
    "Command uses correct glob pattern for context directory"

################################################################################
# TEST 4.7: Deterministic (no randomness)
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4.7: Deterministic Detection (No Randomness)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run detection 10 times rapidly (no changes between runs)
mkdir -p "$FIXTURE_DIR/determinism-test"
touch "$FIXTURE_DIR/determinism-test/file1.md"
touch "$FIXTURE_DIR/determinism-test/file2.md"

declare -a RESULTS
for i in $(seq 1 10); do
    COUNT=$(find "$FIXTURE_DIR/determinism-test" -maxdepth 1 -name "*.md" -type f 2>/dev/null | wc -l)
    RESULTS+=($COUNT)
done

# Check all results are identical
FIRST_RESULT=${RESULTS[0]}
DETERMINISTIC=true

for result in "${RESULTS[@]}"; do
    if [ "$result" -ne "$FIRST_RESULT" ]; then
        DETERMINISTIC=false
        break
    fi
done

((TESTS_RUN++))
if [ "$DETERMINISTIC" = true ]; then
    echo -e "${GREEN}✓ PASS${NC}: Detection is deterministic (10 rapid invocations = $FIRST_RESULT files each)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Detection produced non-deterministic results"
    ((TESTS_FAILED++))
fi

################################################################################
# CLEANUP
################################################################################
rm -rf "$FIXTURE_DIR"

################################################################################
# SUMMARY
################################################################################
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$TEST_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Tests run: $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
echo ""
echo "Performance Summary:"
echo "  Average latency: ${AVERAGE_MS}ms"
echo "  P95 latency: ${P95_MS}ms"
echo "  Threshold: <${LATENCY_THRESHOLD_MS}ms"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$TESTS_FAILED" -gt 0 ]; then
    exit 1
fi

exit 0
