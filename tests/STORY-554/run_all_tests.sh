#!/bin/bash

##############################################################################
# Test Runner: STORY-554 - MVP Launch Checklist
#
# Runs all acceptance criteria test suites for STORY-554
#
# Usage: bash tests/STORY-554/run_all_tests.sh
#
# Story: STORY-554
# Generated: 2026-03-21
##############################################################################

set -uo pipefail

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# Overall counters
SUITES_RUN=0
SUITES_PASSED=0
SUITES_FAILED=0
FAILED_SUITES=""

echo -e "${BOLD}============================================================${NC}"
echo -e "${BOLD}STORY-554: MVP Launch Checklist - Full Test Suite${NC}"
echo -e "${BOLD}============================================================${NC}"
echo ""

# Run each test suite
for test_file in "$TEST_DIR"/test-ac*.sh; do
    if [ ! -f "$test_file" ]; then
        continue
    fi

    suite_name=$(basename "$test_file" .sh)
    SUITES_RUN=$((SUITES_RUN + 1))

    echo -e "\n${YELLOW}--- Running: $suite_name ---${NC}\n"

    if bash "$test_file"; then
        SUITES_PASSED=$((SUITES_PASSED + 1))
        echo -e "\n${GREEN}Suite $suite_name: PASSED${NC}"
    else
        SUITES_FAILED=$((SUITES_FAILED + 1))
        FAILED_SUITES="$FAILED_SUITES  - $suite_name\n"
        echo -e "\n${RED}Suite $suite_name: FAILED${NC}"
    fi
done

##############################################################################
# Overall Summary
##############################################################################

echo ""
echo -e "${BOLD}============================================================${NC}"
echo -e "${BOLD}STORY-554 Overall Results${NC}"
echo -e "${BOLD}============================================================${NC}"
echo -e "Suites run:    $SUITES_RUN"
echo -e "Suites passed: ${GREEN}$SUITES_PASSED${NC}"
echo -e "Suites failed: ${RED}$SUITES_FAILED${NC}"

if [ "$SUITES_FAILED" -gt 0 ]; then
    echo -e "\n${RED}Failed suites:${NC}"
    echo -e "$FAILED_SUITES"
fi

echo -e "${BOLD}============================================================${NC}"

[ "$SUITES_FAILED" -eq 0 ] && exit 0 || exit 1
