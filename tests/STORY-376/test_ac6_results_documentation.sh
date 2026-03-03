#!/bin/sh
# STORY-376 AC#6: Test Results Documented
# Validates:
#   - Test results file created at tests/results/EPIC-059/STORY-376-integration-test-results.md
#   - Contains: total tests, pass/fail breakdown, platform, Treelint version,
#     execution timestamp, failure details, overall PASS/FAIL verdict
#
# Exit code: 0 = all pass, 1 = any failure
# POSIX-compatible shell syntax for cross-platform support

set -e

# Source shared helpers (DRY: helpers, counters, config)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "${SCRIPT_DIR}/test_helpers.sh"
init_test_env

RESULTS_DIR="${PROJECT_ROOT}/tests/results/EPIC-059"
RESULTS_FILE="${RESULTS_DIR}/STORY-376-integration-test-results.md"

# -------------------------------------------------------------------
# Test 1: Results directory exists
# -------------------------------------------------------------------
printf "=== AC#6 Test 1: Results directory exists ===\n"
if [ -d "$RESULTS_DIR" ]; then
    pass_test "Results directory exists: ${RESULTS_DIR}"
else
    fail_test "Results directory NOT found: ${RESULTS_DIR}"
fi

# -------------------------------------------------------------------
# Test 2: Results file exists
# -------------------------------------------------------------------
printf "\n=== AC#6 Test 2: Results file exists ===\n"
if [ -f "$RESULTS_FILE" ]; then
    pass_test "Results file exists: ${RESULTS_FILE}"
else
    fail_test "Results file NOT found: ${RESULTS_FILE}"
fi

# -------------------------------------------------------------------
# Test 3: Results file contains required fields
# -------------------------------------------------------------------
printf "\n=== AC#6 Test 3: Required fields present in results ===\n"
if [ ! -f "$RESULTS_FILE" ]; then
    fail_test "Cannot check fields - results file does not exist"
    fail_test "Cannot check fields - results file does not exist (total tests)"
    fail_test "Cannot check fields - results file does not exist (pass/fail)"
    fail_test "Cannot check fields - results file does not exist (platform)"
    fail_test "Cannot check fields - results file does not exist (version)"
    fail_test "Cannot check fields - results file does not exist (timestamp)"
    fail_test "Cannot check fields - results file does not exist (verdict)"
else
    # Check for total tests executed
    if grep -qi "total.*test\|tests.*total\|test.*count" "$RESULTS_FILE" 2>/dev/null; then
        pass_test "Results contain total tests field"
    else
        fail_test "Results MISSING total tests field"
    fi

    # Check for pass/fail breakdown
    if grep -qi "pass\|fail" "$RESULTS_FILE" 2>/dev/null; then
        pass_test "Results contain pass/fail breakdown"
    else
        fail_test "Results MISSING pass/fail breakdown"
    fi

    # Check for platform information
    if grep -qi "platform\|linux\|macos\|windows\|wsl" "$RESULTS_FILE" 2>/dev/null; then
        pass_test "Results contain platform information"
    else
        fail_test "Results MISSING platform information"
    fi

    # Check for Treelint version
    if grep -qi "treelint.*version\|version.*treelint\|v0\." "$RESULTS_FILE" 2>/dev/null; then
        pass_test "Results contain Treelint version"
    else
        fail_test "Results MISSING Treelint version"
    fi

    # Check for execution timestamp
    if grep -qi "timestamp\|date\|time\|executed.*at\|run.*at" "$RESULTS_FILE" 2>/dev/null; then
        pass_test "Results contain execution timestamp"
    else
        fail_test "Results MISSING execution timestamp"
    fi

    # Check for overall verdict
    if grep -qi "verdict\|overall.*result\|final.*result\|PASS\|FAIL" "$RESULTS_FILE" 2>/dev/null; then
        pass_test "Results contain overall verdict"
    else
        fail_test "Results MISSING overall verdict"
    fi
fi

# -------------------------------------------------------------------
# Test 4: Results file contains per-AC breakdown
# -------------------------------------------------------------------
printf "\n=== AC#6 Test 4: Per-AC breakdown in results ===\n"
if [ ! -f "$RESULTS_FILE" ]; then
    fail_test "Cannot check AC breakdown - results file does not exist"
else
    ac_found=0
    for ac_num in 1 2 3 4 5 6; do
        if grep -qi "AC.*${ac_num}\|AC#${ac_num}\|acceptance.*criteria.*${ac_num}" "$RESULTS_FILE" 2>/dev/null; then
            ac_found=$((ac_found + 1))
        fi
    done
    if [ "$ac_found" -ge 6 ]; then
        pass_test "Results contain breakdown for all 6 ACs"
    else
        fail_test "Results contain breakdown for only ${ac_found}/6 ACs"
    fi
fi

# -------------------------------------------------------------------
# Test 5: Results file contains failure details section
# -------------------------------------------------------------------
printf "\n=== AC#6 Test 5: Failure details section ===\n"
if [ ! -f "$RESULTS_FILE" ]; then
    fail_test "Cannot check failure details - results file does not exist"
else
    if grep -qi "failure.*detail\|failed.*test\|error.*detail" "$RESULTS_FILE" 2>/dev/null; then
        pass_test "Results contain failure details section"
    else
        fail_test "Results MISSING failure details section"
    fi
fi

# -------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------
print_summary_and_exit "AC#6"
