#!/bin/bash
# Test Suite for /create-agent Command
# Tests argument validation, mode detection, and framework integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ /create-agent Command Test Suite"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo "Test $TOTAL_TESTS: $test_name"

    if eval "$test_command"; then
        echo "  ✅ PASSED"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo "  ❌ FAILED"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    echo ""
}

echo "Category 1: Structure and Format Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Command file exists
run_test "Command file exists" \
    "test -f '$PROJECT_ROOT/.claude/commands/create-agent.md'"

# Test 2: YAML frontmatter valid
run_test "YAML frontmatter present and valid" \
    "head -10 '$PROJECT_ROOT/.claude/commands/create-agent.md' | grep -q 'description:' && \
     head -10 '$PROJECT_ROOT/.claude/commands/create-agent.md' | grep -q 'argument-hint:' && \
     head -10 '$PROJECT_ROOT/.claude/commands/create-agent.md' | grep -q 'model:' && \
     head -10 '$PROJECT_ROOT/.claude/commands/create-agent.md' | grep -q 'allowed-tools:'"

# Test 3: Character budget compliance
run_test "Character budget under 15K limit" \
    "char_count=\$(wc -c < '$PROJECT_ROOT/.claude/commands/create-agent.md'); test \$char_count -lt 15000"

# Test 4: Has all required phases
run_test "All 5 phases present (Phase 0-4)" \
    "grep -q 'Phase 0:' '$PROJECT_ROOT/.claude/commands/create-agent.md' && \
     grep -q 'Phase 1:' '$PROJECT_ROOT/.claude/commands/create-agent.md' && \
     grep -q 'Phase 2:' '$PROJECT_ROOT/.claude/commands/create-agent.md' && \
     grep -q 'Phase 3:' '$PROJECT_ROOT/.claude/commands/create-agent.md' && \
     grep -q 'Phase 4:' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

echo "Category 2: Framework Integration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 5: Invokes claude-code-terminal-expert skill
run_test "Invokes claude-code-terminal-expert skill" \
    "grep -q 'claude-code-terminal-expert' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

# Test 6: Invokes agent-generator subagent
run_test "Invokes agent-generator subagent" \
    "grep -q 'agent-generator' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

# Test 7: Lean orchestration pattern
run_test "Follows lean orchestration (delegates to skill/subagent)" \
    "grep -q 'Skill(command=' '$PROJECT_ROOT/.claude/commands/create-agent.md' && \
     grep -q 'Task(' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

echo "Category 3: Mode Support"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 8: Guided mode documented
run_test "Guided mode documented" \
    "grep -q 'guided' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

# Test 9: Template mode documented
run_test "Template mode documented" \
    "grep -q 'template' '$PROJECT_ROOT/.claude/commands/create-agent.md' && \
     grep -q '\-\-template=' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

# Test 10: Domain mode documented
run_test "Domain mode documented" \
    "grep -q 'domain' '$PROJECT_ROOT/.claude/commands/create-agent.md' && \
     grep -q '\-\-domain=' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

# Test 11: Custom spec mode documented
run_test "Custom spec mode documented" \
    "grep -q '\-\-spec=' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

echo "Category 4: Template Library"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 12: Templates directory exists
run_test "Templates directory exists" \
    "test -d '$PROJECT_ROOT/.claude/skills/agent-generator/templates'"

# Test 13: All 5 templates exist
run_test "All 5 templates present" \
    "test -f '$PROJECT_ROOT/.claude/skills/agent-generator/templates/code-reviewer.md' && \
     test -f '$PROJECT_ROOT/.claude/skills/agent-generator/templates/test-automator.md' && \
     test -f '$PROJECT_ROOT/.claude/skills/agent-generator/templates/documentation-writer.md' && \
     test -f '$PROJECT_ROOT/.claude/skills/agent-generator/templates/deployment-coordinator.md' && \
     test -f '$PROJECT_ROOT/.claude/skills/agent-generator/templates/requirements-analyst.md'"

echo "Category 5: Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 14: CLAUDE.md updated
run_test "CLAUDE.md includes /create-agent" \
    "grep -q '/create-agent' '$PROJECT_ROOT/CLAUDE.md'"

# Test 15: commands-reference.md updated
run_test "commands-reference.md includes /create-agent documentation" \
    "grep -q '### /create-agent' '$PROJECT_ROOT/.claude/memory/commands-reference.md'"

# Test 16: README.md updated
run_test "README.md includes /create-agent in command list" \
    "grep -q '/create-agent' '$PROJECT_ROOT/README.md'"

echo "Category 6: Error Handling"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 17: Invalid name handling
run_test "Invalid name error handling present" \
    "grep -q 'Invalid.*[Nn]ame' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

# Test 18: Template not found handling
run_test "Template not found error handling present" \
    "grep -q 'Template.*not found' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

# Test 19: Domain validation handling
run_test "Invalid domain error handling present" \
    "grep -q 'Unknown domain\|Invalid domain' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

# Test 20: Generation failure handling
run_test "Generation failure error handling present" \
    "grep -q 'Generation failed\|generation failed' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

echo "Category 7: Performance Specs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 21: Token efficiency documented
run_test "Token efficiency targets documented" \
    "grep -q '[Tt]oken' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

# Test 22: Execution time documented
run_test "Execution time estimates provided" \
    "grep -q 'min\|minute' '$PROJECT_ROOT/.claude/commands/create-agent.md'"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Test Results Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Total Tests:  $TOTAL_TESTS"
echo "Passed:       $PASSED_TESTS ✅"
echo "Failed:       $FAILED_TESTS"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo "🎉 All tests passed! /create-agent command is ready for production."
    echo ""
    exit 0
else
    echo "⚠️ Some tests failed. Review failures above."
    echo ""
    exit 1
fi
