#!/bin/bash
#
# Test Execution Script for STORY-071: Wizard-Driven Interactive UI
#
# Purpose:
# - Execute test suite in TDD Red phase (all tests should fail)
# - Generate coverage report
# - Display test pyramid distribution
# - Validate test quality
#
# Usage:
#   bash tests/npm-package/run-tests.sh [options]
#
# Options:
#   --unit          Run only unit tests
#   --integration   Run only integration tests
#   --e2e           Run only E2E tests
#   --coverage      Generate coverage report
#   --watch         Watch mode for TDD
#   --verbose       Verbose output
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Parse arguments
TEST_TYPE="all"
COVERAGE=false
WATCH=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --unit)
      TEST_TYPE="unit"
      shift
      ;;
    --integration)
      TEST_TYPE="integration"
      shift
      ;;
    --e2e)
      TEST_TYPE="e2e"
      shift
      ;;
    --coverage)
      COVERAGE=true
      shift
      ;;
    --watch)
      WATCH=true
      shift
      ;;
    --verbose)
      VERBOSE=true
      shift
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Change to project root
cd "$PROJECT_ROOT"

# Display header
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}STORY-071: Wizard-Driven Interactive UI${NC}"
echo -e "${BLUE}Test Suite Execution (TDD Red Phase)${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Build test command
JEST_CMD="jest --config=tests/npm-package/jest.config.js"

# Add test type filter
case $TEST_TYPE in
  unit)
    JEST_CMD="$JEST_CMD --testPathPattern=unit"
    echo -e "${YELLOW}Running UNIT tests only...${NC}"
    ;;
  integration)
    JEST_CMD="$JEST_CMD --testPathPattern=integration"
    echo -e "${YELLOW}Running INTEGRATION tests only...${NC}"
    ;;
  e2e)
    JEST_CMD="$JEST_CMD --testPathPattern=e2e"
    echo -e "${YELLOW}Running E2E tests only...${NC}"
    ;;
  *)
    echo -e "${YELLOW}Running ALL tests...${NC}"
    ;;
esac

# Add coverage flag
if [ "$COVERAGE" = true ]; then
  JEST_CMD="$JEST_CMD --coverage"
  echo -e "${YELLOW}Coverage reporting enabled${NC}"
fi

# Add watch flag
if [ "$WATCH" = true ]; then
  JEST_CMD="$JEST_CMD --watch"
  echo -e "${YELLOW}Watch mode enabled${NC}"
fi

# Add verbose flag
if [ "$VERBOSE" = true ]; then
  JEST_CMD="$JEST_CMD --verbose"
  echo -e "${YELLOW}Verbose output enabled${NC}"
fi

echo ""
echo -e "${BLUE}Command: ${JEST_CMD}${NC}"
echo ""

# Execute tests
set +e
$JEST_CMD
TEST_EXIT_CODE=$?
set -e

# Display results
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Test Execution Complete${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if [ "$TEST_EXIT_CODE" -eq 0 ]; then
  echo -e "${GREEN}✓ All tests PASSED${NC}"
  echo ""
  echo -e "${RED}⚠ WARNING: Tests should FAIL in TDD Red phase!${NC}"
  echo -e "${RED}   Implementation does not exist yet.${NC}"
  exit 0
else
  echo -e "${RED}✗ Tests FAILED (Expected in TDD Red phase)${NC}"
  echo ""
  echo -e "${GREEN}✓ This is correct! Tests fail before implementation.${NC}"
  echo ""
  echo -e "${YELLOW}Next Steps:${NC}"
  echo -e "${YELLOW}1. Implement InstallWizard service${NC}"
  echo -e "${YELLOW}2. Implement PromptService${NC}"
  echo -e "${YELLOW}3. Implement ProgressService${NC}"
  echo -e "${YELLOW}4. Implement OutputFormatter${NC}"
  echo -e "${YELLOW}5. Implement SignalHandler${NC}"
  echo -e "${YELLOW}6. Re-run tests until all pass (TDD Green phase)${NC}"
  echo ""
fi

# Display coverage summary if generated
if [ "$COVERAGE" = true ]; then
  echo ""
  echo -e "${BLUE}Coverage Report: tests/coverage/npm-package/index.html${NC}"
  echo ""
fi

# Display test pyramid distribution
if [ "$TEST_TYPE" = "all" ]; then
  echo ""
  echo -e "${BLUE}========================================${NC}"
  echo -e "${BLUE}Test Pyramid Distribution${NC}"
  echo -e "${BLUE}========================================${NC}"
  echo ""

  UNIT_COUNT=$(find tests/npm-package/unit -name "*.test.js" 2>/dev/null | wc -l)
  INTEGRATION_COUNT=$(find tests/npm-package/integration -name "*.test.js" 2>/dev/null | wc -l)
  E2E_COUNT=$(find tests/npm-package/e2e -name "*.test.js" 2>/dev/null | wc -l)
  TOTAL_COUNT=$((UNIT_COUNT + INTEGRATION_COUNT + E2E_COUNT))

  if [ "$TOTAL_COUNT" -gt 0 ]; then
    UNIT_PERCENT=$((UNIT_COUNT * 100 / TOTAL_COUNT))
    INTEGRATION_PERCENT=$((INTEGRATION_COUNT * 100 / TOTAL_COUNT))
    E2E_PERCENT=$((E2E_COUNT * 100 / TOTAL_COUNT))

    echo -e "Unit Tests:        ${UNIT_COUNT} files (${UNIT_PERCENT}%) ${GREEN}[Target: 70%]${NC}"
    echo -e "Integration Tests: ${INTEGRATION_COUNT} file (${INTEGRATION_PERCENT}%) ${GREEN}[Target: 20%]${NC}"
    echo -e "E2E Tests:         ${E2E_COUNT} file (${E2E_PERCENT}%) ${GREEN}[Target: 10%]${NC}"
    echo -e "Total:             ${TOTAL_COUNT} files"
    echo ""

    if [ "$UNIT_PERCENT" -ge 70 ] && [ "$INTEGRATION_PERCENT" -ge 10 ] && [ "$E2E_PERCENT" -ge 10 ]; then
      echo -e "${GREEN}✓ Test pyramid distribution meets targets${NC}"
    else
      echo -e "${YELLOW}⚠ Test pyramid distribution needs adjustment${NC}"
    fi
  fi
  echo ""
fi

exit $TEST_EXIT_CODE
