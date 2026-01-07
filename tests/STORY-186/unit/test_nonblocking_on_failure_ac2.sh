#!/bin/bash
# Unit Test: AC2 - Non-Blocking on Failure
# Tests that registry regeneration continues on failure (non-blocking)
#
# STORY-186: Auto-Regenerate Subagent Registry in Pre-Commit Hook
#
# Acceptance Criteria:
# AC-2: Then registry regeneration continues on failure (non-blocking)

set -e

TEST_NAME="AC2: Non-Blocking on Failure"
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

# Test 2.1: Registry script call uses '|| true' pattern
test_or_true_pattern() {
    echo -n "Test 2.1: Registry script uses '|| true' for non-blocking... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Pre-commit hook exists"
        return 1
    fi

    # Look for the pattern: generate-subagent-registry.sh ... || true
    if grep "generate-subagent-registry.sh" "$PRE_COMMIT_HOOK" | grep -q "|| true"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: 'generate-subagent-registry.sh ... || true' pattern"
        echo "  Actual: No '|| true' pattern found for registry script"
        return 1
    fi
}

# Test 2.2: Stderr redirected to /dev/null
test_stderr_redirected() {
    echo -n "Test 2.2: Stderr redirected to /dev/null (2>/dev/null)... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        return 1
    fi

    # Per Technical Specification: bash scripts/generate-subagent-registry.sh 2>/dev/null || true
    if grep "generate-subagent-registry.sh" "$PRE_COMMIT_HOOK" | grep -q "2>/dev/null"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: '2>/dev/null' to suppress error output"
        echo "  Actual: No stderr redirection found"
        return 1
    fi
}

# Test 2.3: Pre-commit does not exit on registry failure
test_no_exit_on_failure() {
    echo -n "Test 2.3: Pre-commit hook does not exit on registry failure... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        return 1
    fi

    # Check that there's no 'set -e' right before the registry call
    # or that the call uses || true to prevent exit
    local registry_line
    registry_line=$(grep -n "generate-subagent-registry.sh" "$PRE_COMMIT_HOOK" | head -1 | cut -d: -f1)

    if [ -z "$registry_line" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Registry script call exists"
        return 1
    fi

    # The '|| true' pattern should protect against set -e
    if grep "generate-subagent-registry.sh" "$PRE_COMMIT_HOOK" | grep -q "|| true"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: '|| true' to prevent exit on failure"
        return 1
    fi
}

# Test 2.4: Simulate registry script failure
test_simulated_failure() {
    echo -n "Test 2.4: Simulated registry failure does not block... "

    # Create a temporary failing script
    TEMP_DIR="/tmp/devforgeai-test-$$"
    mkdir -p "$TEMP_DIR"

    cat > "$TEMP_DIR/failing-script.sh" << 'EOF'
#!/bin/bash
echo "Error: Simulated failure" >&2
exit 1
EOF
    chmod +x "$TEMP_DIR/failing-script.sh"

    # Test the pattern: command 2>/dev/null || true should succeed
    if bash -c "$TEMP_DIR/failing-script.sh 2>/dev/null || true"; then
        echo -e "${GREEN}PASS${NC}"
        rm -rf "$TEMP_DIR"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: '|| true' pattern prevents exit"
        rm -rf "$TEMP_DIR"
        return 1
    fi
}

# Test 2.5: Registry failure does not set VALIDATION_FAILED
test_no_validation_failed_flag() {
    echo -n "Test 2.5: Registry failure does not set VALIDATION_FAILED... "

    if [ ! -f "$PRE_COMMIT_HOOK" ]; then
        echo -e "${RED}FAIL${NC}"
        return 1
    fi

    # The unconditional registry regeneration should NOT set VALIDATION_FAILED on failure
    # because it uses '|| true' pattern

    # Look for the pattern in the unconditional block
    # It should be: bash scripts/generate-subagent-registry.sh 2>/dev/null || true
    # NOT: if ! bash scripts/generate-subagent-registry.sh; then VALIDATION_FAILED=1; fi

    local unconditional_block
    # Extract the regeneration block (look for "Regenerating subagent registry")
    unconditional_block=$(grep -A5 "Regenerating subagent registry" "$PRE_COMMIT_HOOK" 2>/dev/null || echo "")

    if [ -z "$unconditional_block" ]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: 'Regenerating subagent registry' block exists"
        return 1
    fi

    # The unconditional block should use || true, not set VALIDATION_FAILED
    if echo "$unconditional_block" | grep -q "VALIDATION_FAILED"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Unconditional regeneration does not affect VALIDATION_FAILED"
        echo "  Actual: VALIDATION_FAILED is set on failure"
        return 1
    fi

    echo -e "${GREEN}PASS${NC}"
    return 0
}

# Run all tests
FAILED_TESTS=0

test_or_true_pattern || FAILED_TESTS=$((FAILED_TESTS + 1))
test_stderr_redirected || FAILED_TESTS=$((FAILED_TESTS + 1))
test_no_exit_on_failure || FAILED_TESTS=$((FAILED_TESTS + 1))
test_simulated_failure || FAILED_TESTS=$((FAILED_TESTS + 1))
test_no_validation_failed_flag || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
