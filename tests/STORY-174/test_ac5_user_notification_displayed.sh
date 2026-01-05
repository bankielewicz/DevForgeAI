#!/bin/bash
# STORY-174 AC#5: User Notification Displayed
#
# Given an execution command auto-exits plan mode
# Then notification displayed: "Note: /{command} is an execution command. Exiting plan mode automatically."
#
# Test Status: RED (expected to FAIL before implementation)

set -e

TEST_NAME="AC#5: User notification for plan mode auto-exit"
COMMANDS_DIR="/mnt/c/Projects/DevForgeAI2/.claude/commands"

echo "=============================================="
echo "TEST: ${TEST_NAME}"
echo "=============================================="

# Test all three execution commands for proper notification text
COMMANDS=("qa.md" "dev.md" "release.md")
FAILED=0

# The expected notification pattern (flexible to match command name variations)
# "Note: /{command} is an execution command. Exiting plan mode automatically."
NOTIFICATION_PATTERN="is an execution command.*[Ee]xiting plan mode"

for CMD in "${COMMANDS[@]}"; do
    COMMAND_FILE="${COMMANDS_DIR}/${CMD}"
    CMD_NAME="${CMD%.md}"  # Remove .md extension

    echo ""
    echo "Checking ${CMD}..."

    if [[ ! -f "${COMMAND_FILE}" ]]; then
        echo "  FAIL: Command file not found: ${COMMAND_FILE}"
        FAILED=1
        continue
    fi

    # Check for the notification message in the command file
    # Pattern: "Note: /{command} is an execution command. Exiting plan mode automatically."

    # Check 1: Contains the core notification pattern
    if grep -qiE "${NOTIFICATION_PATTERN}" "${COMMAND_FILE}"; then
        echo "  PASS: ${CMD} contains plan mode exit notification"
    else
        echo "  FAIL: ${CMD} does NOT contain plan mode exit notification"
        echo "  Expected pattern: 'is an execution command...Exiting plan mode'"
        FAILED=1
    fi

    # Check 2: Notification mentions the specific command name
    if grep -qi "/${CMD_NAME}.*execution command" "${COMMAND_FILE}"; then
        echo "  PASS: ${CMD} notification references /${CMD_NAME}"
    else
        echo "  FAIL: ${CMD} notification does NOT reference /${CMD_NAME}"
        FAILED=1
    fi

    # Check 3: Notification uses "Note:" prefix as per AC
    if grep -qi "Note:.*execution command" "${COMMAND_FILE}"; then
        echo "  PASS: ${CMD} notification uses 'Note:' prefix"
    else
        echo "  FAIL: ${CMD} notification does NOT use 'Note:' prefix"
        FAILED=1
    fi
done

echo ""
echo "=============================================="
if [[ ${FAILED} -eq 0 ]]; then
    echo "PASS: All execution commands have proper user notification"
    exit 0
else
    echo "FAIL: One or more execution commands missing proper user notification"
    exit 1
fi
