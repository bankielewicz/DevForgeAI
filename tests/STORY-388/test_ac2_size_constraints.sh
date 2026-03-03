#!/bin/bash
# Test AC#2: Template Fits Within 500-Line / 15K Char Constraints
# STORY-388: Design Command Template Variant with 15K Char Budget Compliance
#
# Validates:
# - Template is under 500 lines
# - Template is under 15,000 characters
# - Template is within optimal range (6,000-12,000 chars per NFR-001)
#
# Expected: FAIL initially (TDD Red phase - file does not exist yet)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEMPLATE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md"
MAX_LINES=500
MAX_CHARS=15000
OPTIMAL_MIN=6000
OPTIMAL_MAX=12000

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $1"
}

fail_test() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $1: $2"
}

run_test() {
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# ---------------------------------------------------------------------------
# Test 1: File exists
# ---------------------------------------------------------------------------
test_file_exists() {
    if [ -f "$TEMPLATE" ]; then
        pass_test "Template file exists"
    else
        fail_test "Template file exists" "Not found: $TEMPLATE"
    fi
}

# ---------------------------------------------------------------------------
# Test 2: Line count under 500
# ---------------------------------------------------------------------------
test_line_count() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Line count <= $MAX_LINES" "File does not exist"
        return
    fi

    local count
    count=$(wc -l < "$TEMPLATE")

    if [ "$count" -le "$MAX_LINES" ]; then
        pass_test "Line count $count <= $MAX_LINES"
    else
        fail_test "Line count <= $MAX_LINES" "Actual: $count lines"
    fi
}

# ---------------------------------------------------------------------------
# Test 3: Character count under 15,000
# ---------------------------------------------------------------------------
test_char_count() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Char count <= $MAX_CHARS" "File does not exist"
        return
    fi

    local count
    count=$(wc -c < "$TEMPLATE")

    if [ "$count" -le "$MAX_CHARS" ]; then
        pass_test "Char count $count <= $MAX_CHARS"
    else
        fail_test "Char count <= $MAX_CHARS" "Actual: $count characters"
    fi
}

# ---------------------------------------------------------------------------
# Test 4: Within optimal range (6K-12K)
# ---------------------------------------------------------------------------
test_optimal_range() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Optimal range ($OPTIMAL_MIN-$OPTIMAL_MAX)" "File does not exist"
        return
    fi

    local count
    count=$(wc -c < "$TEMPLATE")

    if [ "$count" -ge "$OPTIMAL_MIN" ] && [ "$count" -le "$OPTIMAL_MAX" ]; then
        pass_test "Char count $count within optimal range ($OPTIMAL_MIN-$OPTIMAL_MAX)"
    elif [ "$count" -ge "$OPTIMAL_MIN" ] && [ "$count" -le "$MAX_CHARS" ]; then
        # Above optimal but below max -- acceptable
        pass_test "Char count $count above optimal range but within max (acceptable)"
    else
        fail_test "Optimal range" "Actual: $count chars (optimal: $OPTIMAL_MIN-$OPTIMAL_MAX)"
    fi
}

# ---------------------------------------------------------------------------
# Test 5: Non-empty file (minimum viable content)
# ---------------------------------------------------------------------------
test_non_empty() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Non-empty file" "File does not exist"
        return
    fi

    local count
    count=$(wc -c < "$TEMPLATE")

    if [ "$count" -gt 500 ]; then
        pass_test "File is non-trivial ($count chars)"
    else
        fail_test "Non-empty file" "File too small ($count chars), likely incomplete"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
echo "=============================================="
echo "STORY-388 AC#2: Size Constraints"
echo "=============================================="
echo "Target: $TEMPLATE"
echo "Max lines: $MAX_LINES | Max chars: $MAX_CHARS"
echo "----------------------------------------------"
echo ""

run_test "1" test_file_exists
run_test "2" test_line_count
run_test "3" test_char_count
run_test "4" test_optimal_range
run_test "5" test_non_empty

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
