#!/bin/bash
# STORY-184: Run all acceptance criteria tests
# Tests verify response constraints are added to parallel-validation.md

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

cd "${PROJECT_ROOT}"

echo "========================================"
echo "STORY-184: Reduce Validator Token Overhead"
echo "========================================"
echo ""

PASSED=0
FAILED=0
TOTAL=5

run_test() {
    local test_file="$1"
    echo "----------------------------------------"
    if bash "${test_file}"; then
        ((PASSED++))
    else
        ((FAILED++))
    fi
    echo ""
}

run_test "${SCRIPT_DIR}/test_ac1_test_automator_constraints.sh"
run_test "${SCRIPT_DIR}/test_ac2_code_reviewer_constraints.sh"
run_test "${SCRIPT_DIR}/test_ac3_security_auditor_constraints.sh"
run_test "${SCRIPT_DIR}/test_ac4_response_format_defined.sh"
run_test "${SCRIPT_DIR}/test_ac5_exclusions_documented.sh"

echo "========================================"
echo "Results: ${PASSED}/${TOTAL} passed, ${FAILED}/${TOTAL} failed"
echo "========================================"

if [[ ${FAILED} -gt 0 ]]; then
    echo "STATUS: FAILING (TDD Red Phase - Expected)"
    exit 1
else
    echo "STATUS: PASSING"
    exit 0
fi
