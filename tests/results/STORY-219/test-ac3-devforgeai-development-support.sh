#!/bin/bash
###############################################################################
# Test: AC#3 - Supports devforgeai-development (loads tdd-deep-workflow.md)
# EXPECTED: FAIL (TDD Red phase - file doesn't exist yet)
###############################################################################
set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'
TEST_NAME="AC#3: Documents devforgeai-development deep mode reference loading"
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-shared/shared-phase-0-loader.md"

echo "============================================================================"
echo "TEST: $TEST_NAME"
echo "============================================================================"

if [[ ! -f "$TARGET_FILE" ]]; then
    echo -e "  ${RED}FAIL${NC}: Target file does not exist"
    exit 1
fi

# ASSERT: Contains devforgeai-development skill reference
if grep -q "devforgeai-development" "$TARGET_FILE"; then
    echo -e "  ${GREEN}PASS${NC}: devforgeai-development skill documented"
else
    echo -e "  ${RED}FAIL${NC}: devforgeai-development skill NOT documented"
    exit 1
fi

# ASSERT: References tdd-deep-workflow.md
if grep -q "tdd-deep-workflow.md" "$TARGET_FILE"; then
    echo -e "  ${GREEN}PASS${NC}: tdd-deep-workflow.md reference found"
else
    echo -e "  ${RED}FAIL${NC}: tdd-deep-workflow.md reference NOT found"
    exit 1
fi

echo -e "\n${GREEN}RESULT: PASS${NC}"
exit 0
