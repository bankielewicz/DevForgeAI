#!/bin/bash
###############################################################################
# Run all STORY-219 tests
###############################################################################
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo "============================================================================"
echo "STORY-219: Shared Reference Document Auto-Load Utility"
echo "Running all acceptance criteria tests..."
echo "============================================================================"
echo ""

PASS=0; FAIL=0
for test in "$TEST_DIR"/test-ac*.sh; do
    chmod +x "$test"
    if bash "$test"; then
        ((PASS++))
    else
        ((FAIL++))
    fi
    echo ""
done

echo "============================================================================"
echo -e "SUMMARY: ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC}"
echo "============================================================================"
exit $FAIL
