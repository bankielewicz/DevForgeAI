#!/bin/bash
###############################################################################
# Test: AC#1 - Utility file created at correct location
# EXPECTED: FAIL (TDD Red phase - file doesn't exist yet)
###############################################################################
set -e
RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'
TEST_NAME="AC#1: Utility file exists at .claude/skills/devforgeai-shared/shared-phase-0-loader.md"
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-shared/shared-phase-0-loader.md"

echo "============================================================================"
echo "TEST: $TEST_NAME"
echo "============================================================================"

# ASSERT: File exists
if [[ -f "$TARGET_FILE" ]]; then
    echo -e "  ${GREEN}PASS${NC}: File exists at $TARGET_FILE"
    exit 0
else
    echo -e "  ${RED}FAIL${NC}: File NOT found at $TARGET_FILE"
    exit 1
fi
