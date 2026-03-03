#!/bin/bash
# STORY-313 AC#1: Build-time sync copies files automatically
# Test: scripts/sync-mirrors.sh

set -e

# Test Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SYNC_SCRIPT="$PROJECT_ROOT/scripts/sync-mirrors.sh"

# Test Results
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test Helper Functions
pass() {
    echo "[PASS] $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    TESTS_RUN=$((TESTS_RUN + 1))
}

fail() {
    echo "[FAIL] $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    TESTS_RUN=$((TESTS_RUN + 1))
}

# ------------------------------------------------------------------------------
# Test: SCR-000 - Script exists and is executable
# ------------------------------------------------------------------------------
test_script_exists() {
    if [ -f "$SYNC_SCRIPT" ]; then
        pass "SCR-000: Sync script exists at scripts/sync-mirrors.sh"
    else
        fail "SCR-000: Sync script NOT FOUND at scripts/sync-mirrors.sh"
    fi
}

test_script_executable() {
    if [ -x "$SYNC_SCRIPT" ]; then
        pass "SCR-000: Sync script is executable"
    else
        fail "SCR-000: Sync script is NOT executable"
    fi
}

# ------------------------------------------------------------------------------
# Test: SCR-001 - Copy files from src/claude/ to .claude/
# ------------------------------------------------------------------------------
test_src_claude_copy() {
    if [ -f "$SYNC_SCRIPT" ] && grep -q "src/claude" "$SYNC_SCRIPT" && grep -q "\.claude" "$SYNC_SCRIPT"; then
        pass "SCR-001: Script references src/claude to .claude copy"
    else
        fail "SCR-001: Script does not reference src/claude to .claude copy"
    fi
}

# ------------------------------------------------------------------------------
# Test: SCR-002 - Copy files from src/devforgeai/ to devforgeai/
# ------------------------------------------------------------------------------
test_src_devforgeai_copy() {
    if [ -f "$SYNC_SCRIPT" ] && grep -q "src/devforgeai" "$SYNC_SCRIPT" && grep -q "devforgeai" "$SYNC_SCRIPT"; then
        pass "SCR-002: Script references src/devforgeai to devforgeai copy"
    else
        fail "SCR-002: Script does not reference src/devforgeai to devforgeai copy"
    fi
}

# ------------------------------------------------------------------------------
# Test: SCR-003 - Preserve file permissions and timestamps
# ------------------------------------------------------------------------------
test_preserve_permissions() {
    if [ -f "$SYNC_SCRIPT" ]; then
        # Check for rsync -a or cp -p flags
        if grep -qE "(rsync\s+-[a-zA-Z]*a|cp\s+-[a-zA-Z]*p)" "$SYNC_SCRIPT"; then
            pass "SCR-003: Script uses rsync -a or cp -p for permission preservation"
        else
            fail "SCR-003: Script does NOT use rsync -a or cp -p"
        fi
    else
        fail "SCR-003: Script not found, cannot check preservation flags"
    fi
}

# ------------------------------------------------------------------------------
# Test: SCR-004 - Report sync status
# ------------------------------------------------------------------------------
test_sync_status_report() {
    if [ -f "$SYNC_SCRIPT" ]; then
        # Check for echo/printf statements indicating status reporting
        if grep -qE "(echo|printf).*(copied|synced|complete|success|error)" "$SYNC_SCRIPT"; then
            pass "SCR-004: Script reports sync status"
        else
            fail "SCR-004: Script does NOT report sync status"
        fi
    else
        fail "SCR-004: Script not found, cannot check status reporting"
    fi
}

# ------------------------------------------------------------------------------
# Run All Tests
# ------------------------------------------------------------------------------
echo "=========================================="
echo "STORY-313 AC#1: Sync Script Tests"
echo "=========================================="
echo ""

test_script_exists
test_script_executable
test_src_claude_copy
test_src_devforgeai_copy
test_preserve_permissions
test_sync_status_report

echo ""
echo "=========================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=========================================="

if [ $TESTS_FAILED -gt 0 ]; then
    exit 1
fi
exit 0
