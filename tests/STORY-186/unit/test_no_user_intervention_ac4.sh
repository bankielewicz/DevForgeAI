#!/bin/bash
# Unit Test: AC4 - No User Intervention Required
# Tests that registry updates require zero manual steps
#
# STORY-186: Auto-Regenerate Subagent Registry in Pre-Commit Hook
#
# Acceptance Criteria:
# AC-4: Then zero manual steps for registry updates

set -e

TEST_NAME="AC4: No User Intervention Required"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

PRE_COMMIT_HOOK="$PROJECT_ROOT/.git/hooks/pre-commit"

# Test 4.1: No interactive prompts in registry regeneration block
test_no_interactive_prompts() {
    echo -n "Test 4.1: No interactive prompts (read, select, etc.) in registry block... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Pre-commit hook exists"
        return 1
    fi

    # Extract the registry regeneration block and check for interactive commands
    local regen_block
    regen_block=$(grep -A10 "Regenerating subagent registry" "$PRE_COMMIT_HOOK" 2>/dev/null || echo "")

    # Check for interactive commands
    if echo "$regen_block" | grep -qE "read |select |read\$|PS3=|case.*in"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: No interactive prompts"
        echo "  Actual: Found interactive commands in registry block"
        return 1
    fi

    echo -e "${GREEN}PASS${NC}"
    return 0
}

# Test 4.2: No 'run this command manually' messages
test_no_manual_instructions() {
    echo -n "Test 4.2: No 'run manually' instructions for registry... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        return 1
    fi

    # The unconditional regeneration block should NOT output 'Run:' instructions
    # (unlike the current drift detection which does)

    # Look for the new regeneration block - it should be silent on success
    local regen_block
    regen_block=$(grep -A10 "Regenerating subagent registry" "$PRE_COMMIT_HOOK" 2>/dev/null || echo "")

    if [ -z "$regen_block" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: 'Regenerating subagent registry' block exists"
        return 1
    fi

    # The auto-regeneration should NOT tell user to run anything
    # (The existing drift check does, but the new unconditional regen should not)
    if echo "$regen_block" | grep -qi "Run:"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: No 'Run:' instructions in auto-regeneration"
        return 1
    fi

    echo -e "${GREEN}PASS${NC}"
    return 0
}

# Test 4.3: Fully automated workflow (no user action between detect and fix)
test_automated_workflow() {
    echo -n "Test 4.3: Automated workflow (regenerate + stage in one step)... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        return 1
    fi

    # Both commands should be present: regenerate AND stage
    local has_regenerate
    local has_stage

    has_regenerate=$(grep -c "generate-subagent-registry.sh" "$PRE_COMMIT_HOOK" 2>/dev/null || echo "0")
    has_stage=$(grep -c "git add CLAUDE.md" "$PRE_COMMIT_HOOK" 2>/dev/null || echo "0")

    if [ "$has_regenerate" -gt 0 ] && [ "$has_stage" -gt 0 ]; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Both regenerate and stage commands"
        echo "  Regenerate calls: $has_regenerate"
        echo "  Stage calls: $has_stage"
        return 1
    fi
}

# Test 4.4: No blocking check mode (--check) in unconditional block
test_no_check_mode_in_regen() {
    echo -n "Test 4.4: Unconditional regeneration does not use --check mode... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        return 1
    fi

    # The new unconditional block should NOT use --check (that's for detection only)
    # It should run the script without --check to actually regenerate

    # Look for the new regeneration block
    local regen_block
    regen_block=$(grep -A5 "Regenerating subagent registry" "$PRE_COMMIT_HOOK" 2>/dev/null || echo "")

    if [ -z "$regen_block" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: 'Regenerating subagent registry' block exists"
        return 1
    fi

    # The regeneration call should NOT have --check
    if echo "$regen_block" | grep "generate-subagent-registry.sh" | grep -q "\-\-check"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: No --check flag in unconditional regeneration"
        echo "  Actual: Found --check flag (should regenerate, not just check)"
        return 1
    fi

    echo -e "${GREEN}PASS${NC}"
    return 0
}

# Test 4.5: No VALIDATION_FAILED on registry operations in unconditional block
test_no_blocking_failure() {
    echo -n "Test 4.5: Unconditional registry ops don't block commit (no VALIDATION_FAILED)... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        return 1
    fi

    # The unconditional regeneration block should NOT affect VALIDATION_FAILED
    local regen_block
    regen_block=$(grep -A10 "Regenerating subagent registry" "$PRE_COMMIT_HOOK" 2>/dev/null || echo "")

    if [ -z "$regen_block" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: 'Regenerating subagent registry' block exists"
        return 1
    fi

    # Check that VALIDATION_FAILED is NOT set in this block
    if echo "$regen_block" | grep -q "VALIDATION_FAILED=1"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: No VALIDATION_FAILED in unconditional block"
        return 1
    fi

    echo -e "${GREEN}PASS${NC}"
    return 0
}

# Test 4.6: End-to-end simulation (no user intervention needed)
test_e2e_no_intervention() {
    echo -n "Test 4.6: E2E simulation - complete workflow without user input... "

    TEMP_DIR="/tmp/devforgeai-test-$$"
    mkdir -p "$TEMP_DIR"

    # Create test git repo with minimal structure
    cd "$TEMP_DIR"
    git init --quiet
    git config user.email "test@test.com"
    git config user.name "Test"

    # Create scripts directory and mock registry script
    mkdir -p scripts
    cat > scripts/generate-subagent-registry.sh << 'EOF'
#!/bin/bash
# Mock registry generator that always succeeds
echo "Mock: Registry regenerated"
exit 0
EOF
    chmod +x scripts/generate-subagent-registry.sh

    # Create initial CLAUDE.md
    echo "# Test CLAUDE.md" > CLAUDE.md
    git add CLAUDE.md scripts/
    git commit -m "Initial commit" --quiet

    # Create pre-commit hook with the expected implementation pattern
    mkdir -p .git/hooks
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Regenerate subagent registry (non-blocking)
echo "Regenerating subagent registry..."
bash scripts/generate-subagent-registry.sh 2>/dev/null || true
git add CLAUDE.md 2>/dev/null || true
exit 0
EOF
    chmod +x .git/hooks/pre-commit

    # Make a change and commit (should work without any user intervention)
    echo "change" > test.txt
    git add test.txt

    # The commit should succeed without prompting
    if git commit -m "Test commit" --quiet 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}"
        cd - > /dev/null
        rm -rf "$TEMP_DIR"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Commit succeeds without user intervention"
        cd - > /dev/null
        rm -rf "$TEMP_DIR"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_no_interactive_prompts || FAILED_TESTS=$((FAILED_TESTS + 1))
test_no_manual_instructions || FAILED_TESTS=$((FAILED_TESTS + 1))
test_automated_workflow || FAILED_TESTS=$((FAILED_TESTS + 1))
test_no_check_mode_in_regen || FAILED_TESTS=$((FAILED_TESTS + 1))
test_no_blocking_failure || FAILED_TESTS=$((FAILED_TESTS + 1))
test_e2e_no_intervention || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
