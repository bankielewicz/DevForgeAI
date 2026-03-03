#!/bin/bash
# Test AC#6: Template Validated Against Existing Commands
# STORY-388: Design Command Template Variant with 15K Char Budget Compliance
#
# Validates:
# - Template contains validation notes referencing /qa and /dev commands
# - Mapping between template sections and existing command sections documented
# - Template does not introduce contradictory sections
#
# Expected: FAIL initially (TDD Red phase - file does not exist yet)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEMPLATE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md"
QA_CMD="$PROJECT_ROOT/src/claude/commands/qa.md"
DEV_CMD="$PROJECT_ROOT/src/claude/commands/dev.md"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $1"
}

fail_test() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $1: $2"
}

run_test() {
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# ---------------------------------------------------------------------------
# Test 1: Template references /qa command
# ---------------------------------------------------------------------------
test_qa_reference() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "/qa reference" "Template file does not exist"
        return
    fi

    if grep -qiE "/qa|qa\.md|qa command" "$TEMPLATE"; then
        pass_test "/qa command referenced in template"
    else
        fail_test "/qa reference" "No /qa command reference found"
    fi
}

# ---------------------------------------------------------------------------
# Test 2: Template references /dev command
# ---------------------------------------------------------------------------
test_dev_reference() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "/dev reference" "Template file does not exist"
        return
    fi

    if grep -qiE "/dev|dev\.md|dev command" "$TEMPLATE"; then
        pass_test "/dev command referenced in template"
    else
        fail_test "/dev reference" "No /dev command reference found"
    fi
}

# ---------------------------------------------------------------------------
# Test 3: Validation notes section exists
# ---------------------------------------------------------------------------
test_validation_notes() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Validation notes" "Template file does not exist"
        return
    fi

    if grep -qiE "validat.*note|validation|mapping" "$TEMPLATE"; then
        pass_test "Validation notes / mapping section found"
    else
        fail_test "Validation notes" "No validation notes or mapping section"
    fi
}

# ---------------------------------------------------------------------------
# Test 4: At least 2 commands mapped
# ---------------------------------------------------------------------------
test_two_commands_mapped() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Two commands mapped" "Template file does not exist"
        return
    fi

    local cmd_refs=0

    if grep -qiE "/qa|qa\.md" "$TEMPLATE"; then
        cmd_refs=$((cmd_refs + 1))
    fi
    if grep -qiE "/dev|dev\.md" "$TEMPLATE"; then
        cmd_refs=$((cmd_refs + 1))
    fi

    if [ "$cmd_refs" -ge 2 ]; then
        pass_test "At least 2 commands mapped ($cmd_refs)"
    else
        fail_test "Two commands mapped" "Only $cmd_refs command references found (need >= 2)"
    fi
}

# ---------------------------------------------------------------------------
# Test 5: Template does not contradict existing commands
# (Verify template uses same section naming conventions as existing commands)
# ---------------------------------------------------------------------------
test_no_contradictions() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "No contradictions" "Template file does not exist"
        return
    fi

    # Check that template uses Skill() pattern consistent with existing commands
    # Existing commands use Skill(command="devforgeai-...")
    if grep -q 'Skill(command=' "$TEMPLATE" || ! grep -q 'Skill(' "$TEMPLATE"; then
        pass_test "Template consistent with existing command patterns"
    else
        fail_test "No contradictions" "Template uses non-standard Skill() invocation"
    fi
}

# ---------------------------------------------------------------------------
# Test 6: Reference commands exist in src/ tree
# ---------------------------------------------------------------------------
test_reference_commands_exist() {
    local missing=""

    if [ ! -f "$QA_CMD" ]; then
        missing="$missing qa.md"
    fi
    if [ ! -f "$DEV_CMD" ]; then
        missing="$missing dev.md"
    fi

    if [ -z "$missing" ]; then
        pass_test "Reference commands (qa.md, dev.md) exist in src/"
    else
        fail_test "Reference commands exist" "Missing:$missing"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
echo "=============================================="
echo "STORY-388 AC#6: Command Validation Mapping"
echo "=============================================="
echo "Target: $TEMPLATE"
echo "Reference: $QA_CMD, $DEV_CMD"
echo "----------------------------------------------"
echo ""

run_test "1" test_qa_reference
run_test "2" test_dev_reference
run_test "3" test_validation_notes
run_test "4" test_two_commands_mapped
run_test "5" test_no_contradictions
run_test "6" test_reference_commands_exist

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
