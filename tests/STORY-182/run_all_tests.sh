#!/bin/bash
##############################################################################
# STORY-182: Run All Tests
#
# Executes all acceptance criteria tests for documentation accuracy validation
##############################################################################

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "STORY-182: Documentation Accuracy Tests"
echo "=========================================="
echo ""

tests_passed=0
tests_failed=0

for test_file in "${SCRIPT_DIR}"/test-ac*.sh; do
    if [ -f "${test_file}" ]; then
        test_name=$(basename "${test_file}")
        echo -e "${YELLOW}Running: ${test_name}${NC}"

        if bash "${test_file}"; then
            ((tests_passed++))
        else
            ((tests_failed++))
        fi
        echo ""
    fi
done

echo "=========================================="
echo "Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}${tests_passed}${NC}"
echo -e "Failed: ${RED}${tests_failed}${NC}"
echo "=========================================="

if [ ${tests_failed} -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}TESTS FAILED${NC}"
    exit 1
fi
