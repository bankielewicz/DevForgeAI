#!/bin/bash
###############################################################################
# Test: AC#5 - Light mode support (no reference files or light-specific reference)
# EXPECTED: FAIL (TDD Red phase - file doesn't exist yet)
###############################################################################
set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'
TEST_NAME="AC#5: Light mode handling documented"
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-shared/shared-phase-0-loader.md"

echo "============================================================================"
echo "TEST: $TEST_NAME"
echo "============================================================================"

if [[ ! -f "$TARGET_FILE" ]]; then
    echo -e "  ${RED}FAIL${NC}: Target file does not exist"
    exit 1
fi

# ASSERT: Contains light mode section or reference
if grep -qiE "(light mode|light.*validation|mode.*light)" "$TARGET_FILE"; then
    echo -e "  ${GREEN}PASS${NC}: Light mode handling documented"
else
    echo -e "  ${RED}FAIL${NC}: Light mode handling NOT documented"
    exit 1
fi

# ASSERT: Explains behavior difference (skip or minimal loading)
if grep -qiE "(skip|no.*reference|minimal|ELSE)" "$TARGET_FILE"; then
    echo -e "  ${GREEN}PASS${NC}: Light mode behavior explained"
else
    echo -e "  ${RED}FAIL${NC}: Light mode behavior NOT explained"
    exit 1
fi

echo -e "\n${GREEN}RESULT: PASS${NC}"
exit 0
