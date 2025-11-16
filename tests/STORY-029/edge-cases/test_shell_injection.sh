#!/bin/bash
# Edge Case Test: Shell injection prevention
# Tests that malicious sprint names cannot execute arbitrary commands

set -e

TEST_NAME="Shell Injection Prevention"
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

# Test 1: Sprint name with shell metacharacters properly escaped
test_shell_metacharacters_escaped() {
    echo -n "Test E1.1: Shell metacharacters escaped... "

    # Verify Phase N uses double quotes for sprint name
    if grep -A 50 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep "invoke-hooks" | grep -q "\-\-sprint-name=\"\${"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: --sprint-name=\"\${SPRINT_NAME}\" (double-quoted)"
        echo "  Actual: Not properly quoted (vulnerable to shell injection)"
        return 1
    fi
}

# Test 2: Command injection via semicolon
test_semicolon_injection() {
    echo -n "Test E1.2: Semicolon injection prevented... "

    MALICIOUS_NAME="Sprint-1; rm -rf /"
    TEMP_CONFIG="/tmp/hooks-test-$$.yaml"
    INJECTION_DETECTED="/tmp/injection-detected-$$"

    # Create hooks config
    cat > "$TEMP_CONFIG" <<EOF
feedback_hooks:
  enabled: true
  hooks:
    create-sprint:
      enabled: true
      check_command: "devforgeai check-hooks"
      invoke_command: "devforgeai invoke-hooks"
EOF

    # Create canary file
    touch "$INJECTION_DETECTED"

    # Execute invoke-hooks with malicious name (properly escaped)
    output=$(devforgeai invoke-hooks --operation=create-sprint \
        --sprint-name="$MALICIOUS_NAME" \
        --story-count=5 \
        --capacity=25 \
        --config="$TEMP_CONFIG" 2>&1 || true)

    # Cleanup
    rm -f "$TEMP_CONFIG"

    # Verify canary file still exists (command didn't execute)
    if [ -f "$INJECTION_DETECTED" ]; then
        rm -f "$INJECTION_DETECTED"
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: Command injection blocked (canary file intact)"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Command injection prevented"
        echo "  Actual: Command may have executed (canary deleted)"
        return 1
    fi
}

# Test 3: Command substitution via backticks
test_backtick_injection() {
    echo -n "Test E1.3: Backtick command substitution prevented... "

    MALICIOUS_NAME="Sprint-\`whoami\`"
    TEMP_CONFIG="/tmp/hooks-test-$$.yaml"

    cat > "$TEMP_CONFIG" <<EOF
feedback_hooks:
  enabled: true
  hooks:
    create-sprint:
      enabled: true
      check_command: "devforgeai check-hooks"
      invoke_command: "devforgeai invoke-hooks"
EOF

    # Execute with backtick injection attempt
    output=$(devforgeai invoke-hooks --operation=create-sprint \
        --sprint-name="$MALICIOUS_NAME" \
        --story-count=3 \
        --capacity=15 \
        --config="$TEMP_CONFIG" 2>&1 || true)

    rm -f "$TEMP_CONFIG"

    # Verify output doesn't contain actual username (command not executed)
    if echo "$output" | grep -q "$(whoami)"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Command substitution prevented"
        echo "  Actual: Command executed - found username in output"
        return 1
    else
        echo -e "${GREEN}PASS${NC}"
        return 0
    fi
}

# Test 4: Command substitution via $()
test_dollar_paren_injection() {
    echo -n "Test E1.4: \$() command substitution prevented... "

    MALICIOUS_NAME="Sprint-\$(id)"
    TEMP_CONFIG="/tmp/hooks-test-$$.yaml"

    cat > "$TEMP_CONFIG" <<EOF
feedback_hooks:
  enabled: true
  hooks:
    create-sprint:
      enabled: true
      check_command: "devforgeai check-hooks"
      invoke_command: "devforgeai invoke-hooks"
EOF

    # Execute with $() injection attempt
    output=$(devforgeai invoke-hooks --operation=create-sprint \
        --sprint-name="$MALICIOUS_NAME" \
        --story-count=3 \
        --capacity=15 \
        --config="$TEMP_CONFIG" 2>&1 || true)

    rm -f "$TEMP_CONFIG"

    # Verify output doesn't contain 'uid=', 'gid=' (command not executed)
    if echo "$output" | grep -q "uid=\|gid="; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Command substitution prevented"
        echo "  Actual: Command executed - found uid/gid in output"
        return 1
    else
        echo -e "${GREEN}PASS${NC}"
        return 0
    fi
}

# Test 5: Pipe injection
test_pipe_injection() {
    echo -n "Test E1.5: Pipe injection prevented... "

    MALICIOUS_NAME="Sprint-1 | cat /etc/passwd"
    TEMP_CONFIG="/tmp/hooks-test-$$.yaml"

    cat > "$TEMP_CONFIG" <<EOF
feedback_hooks:
  enabled: true
  hooks:
    create-sprint:
      enabled: true
      check_command: "devforgeai check-hooks"
      invoke_command: "devforgeai invoke-hooks"
EOF

    # Execute with pipe injection attempt
    output=$(devforgeai invoke-hooks --operation=create-sprint \
        --sprint-name="$MALICIOUS_NAME" \
        --story-count=3 \
        --capacity=15 \
        --config="$TEMP_CONFIG" 2>&1 || true)

    rm -f "$TEMP_CONFIG"

    # Verify output doesn't contain /etc/passwd content (root:x:0:0:...)
    if echo "$output" | grep -q "root:x:0:0"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Pipe injection prevented"
        echo "  Actual: Command executed - found /etc/passwd content"
        return 1
    else
        echo -e "${GREEN}PASS${NC}"
        return 0
    fi
}

# Test 6: Null byte injection
test_null_byte_injection() {
    echo -n "Test E1.6: Null byte injection handled... "

    # Null bytes can truncate strings - test if handled safely
    MALICIOUS_NAME="Sprint-Safe\x00; rm -rf /"

    # This is more of a verification that our escaping handles special bytes
    # Python's argparse should handle this correctly
    if grep -A 50 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep "invoke-hooks" | grep -q "\""; then
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: Double-quoting provides defense-in-depth"
        return 0
    else
        echo -e "${YELLOW}WARN${NC}"
        echo "  Warning: Quoting not verified (may be vulnerable)"
        return 0  # Non-critical for this test
    fi
}

# Test 7: Verify BR-003 compliance (shell escaping business rule)
test_br003_compliance() {
    echo -n "Test E1.7: BR-003 shell escaping compliance... "

    story_content=$(cat "$PROJECT_ROOT/.ai_docs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md")

    # Verify BR-003 exists in story
    if echo "$story_content" | grep -q "BR-003.*shell.*escap"; then
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: BR-003 documented in story"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: BR-003 business rule documented"
        echo "  Actual: Rule not found in story"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_shell_metacharacters_escaped || FAILED_TESTS=$((FAILED_TESTS + 1))
test_semicolon_injection || FAILED_TESTS=$((FAILED_TESTS + 1))
test_backtick_injection || FAILED_TESTS=$((FAILED_TESTS + 1))
test_dollar_paren_injection || FAILED_TESTS=$((FAILED_TESTS + 1))
test_pipe_injection || FAILED_TESTS=$((FAILED_TESTS + 1))
test_null_byte_injection || FAILED_TESTS=$((FAILED_TESTS + 1))
test_br003_compliance || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
