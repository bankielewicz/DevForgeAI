#!/bin/bash
################################################################################
# STORY-528: Integration E2E Test - Phase Completion Gate Hook
#
# Tests the full end-to-end flow:
#   1. Incomplete phases -> hook blocks (exit 2)
#   2. All phases complete -> hook allows (exit 0)
#   3. Counter integration: 3 blocks then allow on 4th
#
# Self-contained: creates temp directories, cleans up on exit.
################################################################################

set -euo pipefail

# Resolve hook path relative to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HOOK_PATH="$PROJECT_ROOT/src/claude/hooks/phase-completion-gate.sh"
PASS=0
FAIL=0
TOTAL=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

##############################################################################
# Helpers
##############################################################################

setup_mock_project() {
    local tmpdir
    tmpdir=$(mktemp -d)
    # Create minimal project structure
    echo "# CLAUDE.md" > "$tmpdir/CLAUDE.md"
    mkdir -p "$tmpdir/devforgeai/workflows"
    mkdir -p "$tmpdir/tmp/STORY-528"
    echo "$tmpdir"
}

cleanup() {
    if [ -n "${TEST_PROJECT_ROOT:-}" ] && [ -d "$TEST_PROJECT_ROOT" ]; then
        rm -rf "$TEST_PROJECT_ROOT"
    fi
}
trap cleanup EXIT

create_phase_state() {
    local dir="$1"
    local story_id="$2"
    local all_complete="$3"  # "true" or "false"

    local completed_val="false"
    local status_val="pending"
    if [ "$all_complete" = "true" ]; then
        completed_val="true"
        status_val="completed"
    fi

    cat > "$dir/devforgeai/workflows/${story_id}-phase-state.json" <<JSONEOF
{
    "story_id": "$story_id",
    "workflow": "dev",
    "phases": {
        "01": { "name": "Pre-Flight", "completed": $completed_val, "status": "$status_val" },
        "02": { "name": "Red", "completed": $completed_val, "status": "$status_val" },
        "03": { "name": "Green", "completed": $completed_val, "status": "$status_val" },
        "04": { "name": "Refactor", "completed": $completed_val, "status": "$status_val" }
    }
}
JSONEOF
}

run_hook() {
    local project_root="$1"
    local input="${2:-'{}'}"
    local exit_code=0

    # Run hook with CLAUDE_PROJECT_DIR set to our mock project
    CLAUDE_PROJECT_DIR="$project_root" \
        bash "$HOOK_PATH" <<< "$input" 2>/dev/null || exit_code=$?
    return $exit_code
}

run_hook_capture_stderr() {
    local project_root="$1"
    local input="${2:-'{}'}"
    local exit_code=0

    CLAUDE_PROJECT_DIR="$project_root" \
        bash "$HOOK_PATH" <<< "$input" 2>&1 || exit_code=$?
    echo "EXIT:$exit_code"
}

assert_exit() {
    local test_name="$1"
    local expected="$2"
    local actual="$3"
    TOTAL=$((TOTAL + 1))

    if [ "$actual" -eq "$expected" ]; then
        echo -e "${GREEN}PASS${NC}: $test_name (exit=$actual)"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}FAIL${NC}: $test_name (expected exit=$expected, got exit=$actual)"
        FAIL=$((FAIL + 1))
    fi
}

assert_contains() {
    local test_name="$1"
    local needle="$2"
    local haystack="$3"
    TOTAL=$((TOTAL + 1))

    if echo "$haystack" | grep -q "$needle"; then
        echo -e "${GREEN}PASS${NC}: $test_name (output contains '$needle')"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}FAIL${NC}: $test_name (output missing '$needle')"
        FAIL=$((FAIL + 1))
    fi
}

##############################################################################
# Test 1: Incomplete phases -> hook blocks (exit 2)
##############################################################################
echo ""
echo "=== Test 1: Incomplete phases block stop ==="

TEST_PROJECT_ROOT=$(setup_mock_project)
create_phase_state "$TEST_PROJECT_ROOT" "STORY-999" "false"

# Clear any counter
rm -f "$TEST_PROJECT_ROOT/tmp/STORY-528/stop-hook-counter"

exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{}' || exit_code=$?
assert_exit "Incomplete phases should block (exit 2)" 2 "$exit_code"

# Capture stderr for phase details
output=$(run_hook_capture_stderr "$TEST_PROJECT_ROOT" '{}')
assert_contains "Stderr shows incomplete phase info" "Incomplete phases" "$output"
assert_contains "Stderr shows story ID" "STORY-999" "$output"

rm -rf "$TEST_PROJECT_ROOT"

##############################################################################
# Test 2: All phases complete -> hook allows (exit 0)
##############################################################################
echo ""
echo "=== Test 2: Complete phases allow stop ==="

TEST_PROJECT_ROOT=$(setup_mock_project)
create_phase_state "$TEST_PROJECT_ROOT" "STORY-888" "true"

exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{}' || exit_code=$?
assert_exit "All phases complete should allow (exit 0)" 0 "$exit_code"

rm -rf "$TEST_PROJECT_ROOT"

##############################################################################
# Test 3: Counter integration - 3 blocks then allow on 4th
##############################################################################
echo ""
echo "=== Test 3: Counter integration (3 blocks, 4th allows) ==="

TEST_PROJECT_ROOT=$(setup_mock_project)
create_phase_state "$TEST_PROJECT_ROOT" "STORY-777" "false"

# Clear counter
rm -f "$TEST_PROJECT_ROOT/tmp/STORY-528/stop-hook-counter"

# Run 1: should block (exit 2), counter -> 1
exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{}' || exit_code=$?
assert_exit "Run 1: should block (counter=1)" 2 "$exit_code"

# Run 2: should block (exit 2), counter -> 2
exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{}' || exit_code=$?
assert_exit "Run 2: should block (counter=2)" 2 "$exit_code"

# Run 3: should block (exit 2), counter -> 3
exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{}' || exit_code=$?
assert_exit "Run 3: should block (counter=3)" 2 "$exit_code"

# Run 4: counter=3 >= MAX_RETRIGGERS=3, should allow (exit 0)
exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{}' || exit_code=$?
assert_exit "Run 4: should allow (counter>=3)" 0 "$exit_code"

# Verify counter file value
counter_val=$(cat "$TEST_PROJECT_ROOT/tmp/STORY-528/stop-hook-counter" 2>/dev/null || echo "MISSING")
TOTAL=$((TOTAL + 1))
if [ "$counter_val" = "3" ]; then
    echo -e "${GREEN}PASS${NC}: Counter file holds value 3 after 3 increments"
    PASS=$((PASS + 1))
else
    echo -e "${RED}FAIL${NC}: Counter file expected '3', got '$counter_val'"
    FAIL=$((FAIL + 1))
fi

rm -rf "$TEST_PROJECT_ROOT"

##############################################################################
# Test 4: Transition from incomplete to complete
##############################################################################
echo ""
echo "=== Test 4: Transition incomplete -> complete ==="

TEST_PROJECT_ROOT=$(setup_mock_project)
create_phase_state "$TEST_PROJECT_ROOT" "STORY-666" "false"
rm -f "$TEST_PROJECT_ROOT/tmp/STORY-528/stop-hook-counter"

# First run: blocks
exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{}' || exit_code=$?
assert_exit "Before fix: should block" 2 "$exit_code"

# Now mark all phases complete
create_phase_state "$TEST_PROJECT_ROOT" "STORY-666" "true"

# Second run: allows (phases complete, counter irrelevant)
exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{}' || exit_code=$?
assert_exit "After fix: should allow" 0 "$exit_code"

rm -rf "$TEST_PROJECT_ROOT"

##############################################################################
# Test 5: stop_hook_active=true bypasses everything
##############################################################################
echo ""
echo "=== Test 5: stop_hook_active=true bypass ==="

TEST_PROJECT_ROOT=$(setup_mock_project)
create_phase_state "$TEST_PROJECT_ROOT" "STORY-555" "false"
rm -f "$TEST_PROJECT_ROOT/tmp/STORY-528/stop-hook-counter"

exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{"stop_hook_active": true}' || exit_code=$?
assert_exit "stop_hook_active=true should allow (exit 0)" 0 "$exit_code"

rm -rf "$TEST_PROJECT_ROOT"

##############################################################################
# Test 6: No workflows directory -> allow
##############################################################################
echo ""
echo "=== Test 6: No workflows directory ==="

TEST_PROJECT_ROOT=$(setup_mock_project)
rm -rf "$TEST_PROJECT_ROOT/devforgeai/workflows"

exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{}' || exit_code=$?
assert_exit "No workflows dir should allow (exit 0)" 0 "$exit_code"

rm -rf "$TEST_PROJECT_ROOT"

##############################################################################
# Test 7: QA phase-state files are excluded
##############################################################################
echo ""
echo "=== Test 7: QA phase-state files excluded ==="

TEST_PROJECT_ROOT=$(setup_mock_project)
# Only create a QA phase-state (should be ignored)
cat > "$TEST_PROJECT_ROOT/devforgeai/workflows/STORY-444-qa-phase-state.json" <<'JSONEOF'
{
    "story_id": "STORY-444",
    "workflow": "qa",
    "phases": {
        "00": { "name": "Setup", "completed": false, "status": "pending" }
    }
}
JSONEOF

exit_code=0
run_hook "$TEST_PROJECT_ROOT" '{}' || exit_code=$?
assert_exit "QA-only workflows should allow (exit 0)" 0 "$exit_code"

rm -rf "$TEST_PROJECT_ROOT"

##############################################################################
# Summary
##############################################################################
echo ""
echo "=========================================="
echo "Integration E2E Results: $PASS/$TOTAL passed, $FAIL failed"
echo "=========================================="

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
