#!/bin/bash
###############################################################################
# Test: AC#4 - Consistent pattern documented (IF skill == "devforgeai-{X}" AND mode == "deep")
# EXPECTED: FAIL (TDD Red phase - file doesn't exist yet)
###############################################################################
set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'
TEST_NAME="AC#4: Consistent pattern template documented"
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-shared/shared-phase-0-loader.md"

echo "============================================================================"
echo "TEST: $TEST_NAME"
echo "============================================================================"

if [[ ! -f "$TARGET_FILE" ]]; then
    echo -e "  ${RED}FAIL${NC}: Target file does not exist"
    exit 1
fi

# ASSERT: Contains pattern structure (IF/WHEN condition)
if grep -qE "(IF|WHEN).*mode.*deep" "$TARGET_FILE"; then
    echo -e "  ${GREEN}PASS${NC}: Conditional deep mode pattern found"
else
    echo -e "  ${RED}FAIL${NC}: Conditional deep mode pattern NOT found"
    exit 1
fi

# ASSERT: Contains skill mapping table or structured list
if grep -qE "^\|.*Skill.*\|.*Reference" "$TARGET_FILE"; then
    echo -e "  ${GREEN}PASS${NC}: Skill-to-reference mapping table found"
else
    echo -e "  ${RED}FAIL${NC}: Skill-to-reference mapping table NOT found"
    exit 1
fi

echo -e "\n${GREEN}RESULT: PASS${NC}"
exit 0
