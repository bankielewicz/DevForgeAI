#!/bin/bash
###############################################################################
# Test Suite: STORY-176 - AC#6: Zero False Positives
# Purpose: Verify valid Slash Command files generate zero CRITICAL/HIGH/MEDIUM violations
# TDD Phase: RED (tests should FAIL until implementation)
###############################################################################

set -euo pipefail

SCANNER_FILE="src/claude/agents/anti-pattern-scanner.md"
SAMPLE_COMMAND_FILE=".claude/commands/dev.md"
SAMPLE_SKILL_FILE=".claude/skills/devforgeai-development/SKILL.md"
SAMPLE_AGENT_FILE=".claude/agents/test-automator.md"

TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

pass_test() {
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "  PASS: $1"
}

fail_test() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "  FAIL: $1"
}

test_case() {
    TEST_COUNT=$((TEST_COUNT + 1))
    echo ""
    echo "Test $TEST_COUNT: $1"
}

header() {
    echo ""
    echo "================================================================"
    echo "$1"
    echo "================================================================"
}

echo "STORY-176 AC#6: Zero False Positives"
echo "Target: $SCANNER_FILE"
echo "Sample Files: $SAMPLE_COMMAND_FILE, $SAMPLE_SKILL_FILE, $SAMPLE_AGENT_FILE"

if [ ! -f "$SCANNER_FILE" ]; then
    echo ""
    echo "ERROR: Scanner file does not exist: $SCANNER_FILE"
    exit 1
fi

header "AC#6: Zero False Positive Validation"

test_case "Sample command file exists for integration testing"
if [ -f "$SAMPLE_COMMAND_FILE" ]; then
    pass_test "Sample command file exists: $SAMPLE_COMMAND_FILE"
else
    fail_test "Sample command file missing: $SAMPLE_COMMAND_FILE"
fi

test_case "Sample skill file exists for integration testing"
if [ -f "$SAMPLE_SKILL_FILE" ]; then
    pass_test "Sample skill file exists: $SAMPLE_SKILL_FILE"
else
    fail_test "Sample skill file missing: $SAMPLE_SKILL_FILE"
fi

test_case "Sample agent file exists for integration testing"
if [ -f "$SAMPLE_AGENT_FILE" ]; then
    pass_test "Sample agent file exists: $SAMPLE_AGENT_FILE"
else
    fail_test "Sample agent file missing: $SAMPLE_AGENT_FILE"
fi

test_case "Scanner documents zero false positive expectation"
if grep -qi "zero.*false positive\|no.*false positive\|false positive.*zero" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Scanner documents zero false positive expectation"
else
    fail_test "Scanner does not document zero false positive expectation"
fi

test_case "Exclusions prevent structure violations on valid files"
# Check that exclusions are designed to prevent false positives
if grep -qi "exclusion.*prevent\|exclude.*false\|skip.*avoid.*false" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Exclusions explicitly prevent false positives"
else
    fail_test "No explicit connection between exclusions and false positive prevention"
fi

test_case "Valid command files excluded from all inappropriate phases"
# Commands should be excluded from Phase 3 (structure) and Phase 6 code examples
if grep -qi "command.*exclude.*phase 3\|\.claude/commands.*phase 3" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Command files excluded from Phase 3"
else
    fail_test "Command files not explicitly excluded from Phase 3"
fi

test_case "Valid skill files excluded from code smell detection"
if grep -qi "skill.*exclude.*phase 5\|\.claude/skills.*phase 5\|skill.*code.*smell.*exclude" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Skill files excluded from Phase 5 (Code Smells)"
else
    fail_test "Skill files not explicitly excluded from Phase 5"
fi

test_case "Integration test scenario documented"
# Scanner should document how to verify zero false positives
if grep -qi "integration\|test.*scenario\|verify.*exclusion\|validate.*exclusion" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Integration test scenario documented"
else
    fail_test "No integration test scenario for verifying exclusions"
fi

test_case "Expected output for excluded files: zero violations"
if grep -qi "zero.*violation\|no.*violation.*excluded\|excluded.*clean" "$SCANNER_FILE" 2>/dev/null; then
    pass_test "Expected output (zero violations) documented for excluded files"
else
    fail_test "Expected output for excluded files not documented"
fi

header "Integration Verification: Valid File Patterns"

test_case "Command file patterns match actual files"
# Count command files that would match the exclusion pattern
command_count=$(find .claude/commands -name "*.md" -type f 2>/dev/null | wc -l || echo "0")
if [ "$command_count" -gt 0 ]; then
    pass_test "Found $command_count command files matching .claude/commands/*.md"
else
    fail_test "No command files found matching pattern"
fi

test_case "Skill file patterns match actual files"
skill_count=$(find .claude/skills -name "*.md" -type f 2>/dev/null | wc -l || echo "0")
if [ "$skill_count" -gt 0 ]; then
    pass_test "Found $skill_count skill files matching .claude/skills/**/*.md"
else
    fail_test "No skill files found matching pattern"
fi

test_case "Agent file patterns match actual files"
agent_count=$(find .claude/agents -name "*.md" -type f 2>/dev/null | wc -l || echo "0")
if [ "$agent_count" -gt 0 ]; then
    pass_test "Found $agent_count agent files matching .claude/agents/*.md"
else
    fail_test "No agent files found matching pattern"
fi

header "Summary"
echo ""
echo "Total Tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
echo ""

if [ $FAIL_COUNT -gt 0 ]; then
    echo "STATUS: RED PHASE - Tests failing as expected (TDD)"
    exit 1
else
    echo "STATUS: GREEN PHASE - All tests passing"
    exit 0
fi
