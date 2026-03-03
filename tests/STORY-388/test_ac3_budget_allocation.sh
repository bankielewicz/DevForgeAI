#!/bin/bash
# Test AC#3: Character Budget Allocation Guidance Provided
# STORY-388: Design Command Template Variant with 15K Char Budget Compliance
#
# Validates:
# - Budget allocation section exists
# - Per-section allocation targets documented
# - Max allocations sum to <= 15,000 characters
# - Optimal range 6K-12K referenced
#
# Expected: FAIL initially (TDD Red phase - file does not exist yet)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEMPLATE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md"

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
# Test 1: Budget allocation section exists
# ---------------------------------------------------------------------------
test_budget_section_exists() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Budget section exists" "File does not exist"
        return
    fi

    if grep -qEi "^#+ .*(Budget|Character Budget|Budget Allocation)" "$TEMPLATE"; then
        pass_test "Budget allocation section found"
    else
        fail_test "Budget section exists" "No Budget Allocation heading found"
    fi
}

# ---------------------------------------------------------------------------
# Test 2: Per-section allocation targets present
# ---------------------------------------------------------------------------
test_allocation_targets() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Allocation targets" "File does not exist"
        return
    fi

    # Look for numeric ranges in budget section (e.g., 200-400, 600-1200)
    local range_count
    range_count=$(grep -cE "[0-9]+-[0-9]+" "$TEMPLATE" || true)

    if [ "$range_count" -ge 5 ]; then
        pass_test "Per-section allocation ranges found ($range_count)"
    else
        fail_test "Allocation targets" "Only $range_count numeric ranges found (need >= 5)"
    fi
}

# ---------------------------------------------------------------------------
# Test 3: Max allocations sum <= 15,000
# ---------------------------------------------------------------------------
test_budget_sum() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Budget sum <= 15000" "File does not exist"
        return
    fi

    # Extract max values from budget table rows (format: NNN-NNN or | NNN |)
    # Look for the higher number in dash-separated ranges within a table context
    local budget_section
    budget_section=$(sed -n '/[Bb]udget [Aa]llocation/,/^#\+ /p' "$TEMPLATE")

    if [ -z "$budget_section" ]; then
        fail_test "Budget sum <= 15000" "Cannot find budget allocation section"
        return
    fi

    # Extract max values from ranges like "200-400" or "800-1500"
    local sum=0
    while IFS= read -r max_val; do
        if [ -n "$max_val" ] && [ "$max_val" -gt 0 ] 2>/dev/null; then
            sum=$((sum + max_val))
        fi
    done < <(echo "$budget_section" | grep -oE "[0-9]+-([0-9]+)" | grep -oE "[0-9]+$")

    if [ "$sum" -eq 0 ]; then
        fail_test "Budget sum <= 15000" "Could not parse budget values"
        return
    fi

    if [ "$sum" -le 15000 ]; then
        pass_test "Budget max sum $sum <= 15000"
    else
        fail_test "Budget sum <= 15000" "Sum of max allocations is $sum"
    fi
}

# ---------------------------------------------------------------------------
# Test 4: Optimal range 6K-12K referenced
# ---------------------------------------------------------------------------
test_optimal_range_reference() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Optimal range reference" "File does not exist"
        return
    fi

    if grep -qE "6[,.]?000.*12[,.]?000|6K.*12K|6k.*12k" "$TEMPLATE"; then
        pass_test "Optimal range 6K-12K referenced"
    else
        fail_test "Optimal range reference" "No 6K-12K range mention found"
    fi
}

# ---------------------------------------------------------------------------
# Test 5: Lean orchestration pattern referenced
# ---------------------------------------------------------------------------
test_lean_orchestration_reference() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Lean orchestration reference" "File does not exist"
        return
    fi

    if grep -qi "lean orchestration" "$TEMPLATE"; then
        pass_test "Lean orchestration pattern referenced"
    else
        fail_test "Lean orchestration reference" "No 'lean orchestration' mention found"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
echo "=============================================="
echo "STORY-388 AC#3: Budget Allocation Guidance"
echo "=============================================="
echo "Target: $TEMPLATE"
echo "----------------------------------------------"
echo ""

run_test "1" test_budget_section_exists
run_test "2" test_allocation_targets
run_test "3" test_budget_sum
run_test "4" test_optimal_range_reference
run_test "5" test_lean_orchestration_reference

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
