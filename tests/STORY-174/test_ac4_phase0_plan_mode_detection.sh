#!/bin/bash
# STORY-174 AC#4: Phase 0 Auto-Exits Plan Mode
#
# Given execution command invoked with `execution-mode: immediate`
# And plan mode is currently active
# When Phase 0 executes
# Then command auto-exits plan mode using ExitPlanMode tool
#
# Test Status: RED (expected to FAIL before implementation)

set -e

TEST_NAME="AC#4: Phase 0 plan mode detection and ExitPlanMode"
COMMANDS_DIR="/mnt/c/Projects/DevForgeAI2/.claude/commands"

echo "=============================================="
echo "TEST: ${TEST_NAME}"
echo "=============================================="

# Test all three execution commands for Phase 0 plan mode detection
COMMANDS=("qa.md" "dev.md" "release.md")
FAILED=0

for CMD in "${COMMANDS[@]}"; do
    COMMAND_FILE="${COMMANDS_DIR}/${CMD}"

    echo ""
    echo "Checking ${CMD}..."

    if [[ ! -f "${COMMAND_FILE}" ]]; then
        echo "  FAIL: Command file not found: ${COMMAND_FILE}"
        FAILED=1
        continue
    fi

    # Check for Phase 0 section that handles plan mode detection
    # Should contain logic to check for execution-mode and call ExitPlanMode

    # Check 1: Command references execution-mode check
    if grep -q "execution-mode" "${COMMAND_FILE}"; then
        echo "  PASS: ${CMD} references execution-mode"
    else
        echo "  FAIL: ${CMD} does NOT reference execution-mode in Phase 0 logic"
        FAILED=1
    fi

    # Check 2: Command references ExitPlanMode tool
    if grep -qi "ExitPlanMode" "${COMMAND_FILE}"; then
        echo "  PASS: ${CMD} references ExitPlanMode tool"
    else
        echo "  FAIL: ${CMD} does NOT reference ExitPlanMode tool"
        FAILED=1
    fi

    # Check 3: Command has plan mode detection logic pattern
    # Looking for patterns like "IF plan mode active" or "check plan mode"
    if grep -qiE "(plan.?mode|plan_mode|planMode)" "${COMMAND_FILE}"; then
        echo "  PASS: ${CMD} has plan mode detection logic"
    else
        echo "  FAIL: ${CMD} does NOT have plan mode detection logic"
        FAILED=1
    fi
done

echo ""
echo "=============================================="
if [[ ${FAILED} -eq 0 ]]; then
    echo "PASS: All execution commands have Phase 0 plan mode detection"
    exit 0
else
    echo "FAIL: One or more execution commands missing Phase 0 plan mode detection"
    exit 1
fi
