#!/usr/bin/env bash
# =============================================================================
# STORY-392 AC#5: Read-Only Tool Constraint Preserved
#
# Verifies the updated src/claude/agents/ac-compliance-verifier.md:
# 1. Tools field exactly [Read, Grep, Glob] in YAML frontmatter
# 2. READ-ONLY stated in Constraints section
# 3. Refusal pattern present for write operations
# 4. No instructions requiring write access
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/ac-compliance-verifier.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

# --- Test Helper ---
run_test() {
    local test_name="$1"
    local test_result="$2"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ "$test_result" -eq 0 ]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "  PASS: ${test_name}"
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        echo "  FAIL: ${test_name}"
    fi
}

echo "================================================================"
echo "STORY-392 AC#5: Read-Only Tool Constraint Tests"
echo "Target: ${AGENT_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$AGENT_FILE" ]; then
    echo "FATAL: Agent file not found at ${AGENT_FILE}"
    exit 1
fi

# =============================================================================
# Test 1: Tools field exactly [Read, Grep, Glob] in YAML frontmatter
# =============================================================================
echo "--- Tools Field in Frontmatter ---"

# Extract frontmatter block
FRONTMATTER_BLOCK=$(awk 'BEGIN{n=0} /^---$/{n++; next} n==1{print}' "$AGENT_FILE")

# Check tools field exists
HAS_TOOLS=$(echo "$FRONTMATTER_BLOCK" | grep -c '^tools:' || true)
run_test "Frontmatter contains 'tools' field" "$( [ "$HAS_TOOLS" -ge 1 ] && echo 0 || echo 1 )"

# Check tools field is exactly [Read, Grep, Glob]
TOOLS_LINE=$(echo "$FRONTMATTER_BLOCK" | grep '^tools:' || true)
HAS_EXACT_TOOLS=$(echo "$TOOLS_LINE" | grep -c '\[Read, Grep, Glob\]' || true)
run_test "Tools field is exactly [Read, Grep, Glob]" "$( [ "$HAS_EXACT_TOOLS" -ge 1 ] && echo 0 || echo 1 )"

# Verify NO Write in tools
HAS_WRITE_TOOL=$(echo "$TOOLS_LINE" | grep -ci 'Write' || true)
run_test "Tools field does NOT contain Write (found: ${HAS_WRITE_TOOL}, want 0)" "$( [ "$HAS_WRITE_TOOL" -eq 0 ] && echo 0 || echo 1 )"

# Verify NO Edit in tools
HAS_EDIT_TOOL=$(echo "$TOOLS_LINE" | grep -ci 'Edit' || true)
run_test "Tools field does NOT contain Edit (found: ${HAS_EDIT_TOOL}, want 0)" "$( [ "$HAS_EDIT_TOOL" -eq 0 ] && echo 0 || echo 1 )"

# Verify NO Bash in tools
HAS_BASH_TOOL=$(echo "$TOOLS_LINE" | grep -ci 'Bash' || true)
run_test "Tools field does NOT contain Bash (found: ${HAS_BASH_TOOL}, want 0)" "$( [ "$HAS_BASH_TOOL" -eq 0 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: READ-ONLY stated in Constraints section
# =============================================================================
echo ""
echo "--- READ-ONLY in Constraints ---"

# Constraints and Boundaries section must exist
HAS_CONSTRAINTS=$(grep -c '^## Constraints and Boundaries' "$AGENT_FILE" || true)
run_test "Constraints and Boundaries section exists" "$( [ "$HAS_CONSTRAINTS" -ge 1 ] && echo 0 || echo 1 )"

# Extract Constraints section content
CONSTRAINTS_CONTENT=$(sed -n '/^## Constraints and Boundaries/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

# Must state READ-ONLY in Constraints section
HAS_READONLY_CONSTRAINT=$(echo "$CONSTRAINTS_CONTENT" | grep -ci 'READ.ONLY' || true)
run_test "READ-ONLY stated in Constraints section (found: ${HAS_READONLY_CONSTRAINT})" "$( [ "$HAS_READONLY_CONSTRAINT" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Refusal pattern present for write operations
# =============================================================================
echo ""
echo "--- Refusal Pattern ---"

# Agent must contain a refusal pattern for write operations
# The current agent has: "AC Compliance Verifier is read-only. I can verify and report..."
HAS_REFUSAL=$(grep -ci 'read.only.*must NOT modify\|cannot.*write\|must NOT modify\|will NOT modify\|refuse.*write\|read.only.*I can verify' "$AGENT_FILE" || true)
run_test "Refusal pattern for write operations present (found: ${HAS_REFUSAL})" "$( [ "$HAS_REFUSAL" -ge 1 ] && echo 0 || echo 1 )"

# Refusal must be a quotable response (in blockquote or code format)
HAS_QUOTABLE_REFUSAL=$(grep -c '^>' "$AGENT_FILE" || true)
run_test "Refusal pattern is in blockquote format (found: ${HAS_QUOTABLE_REFUSAL})" "$( [ "$HAS_QUOTABLE_REFUSAL" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: No instructions requiring write access
# =============================================================================
echo ""
echo "--- No Write Instructions ---"

# Agent must NOT contain Write() tool calls
HAS_WRITE_CALL=$(grep -c 'Write(' "$AGENT_FILE" || true)
# Note: Write() may appear in documentation about orchestrator persistence path
# but must NOT appear as an instruction for the agent to execute
# Check if Write appears outside of "orchestrator will" context
WRITE_OUTSIDE_ORCHESTRATOR=$(grep 'Write(' "$AGENT_FILE" | grep -cv 'orchestrator\|Phase 4\.5\|Phase 5\.5\|will extract\|will call' || true)
run_test "No Write() instructions for agent to execute (found: ${WRITE_OUTSIDE_ORCHESTRATOR}, want 0)" "$( [ "$WRITE_OUTSIDE_ORCHESTRATOR" -eq 0 ] && echo 0 || echo 1 )"

# Agent must NOT contain Edit() tool calls
HAS_EDIT_CALL=$(grep -c 'Edit(' "$AGENT_FILE" || true)
run_test "No Edit() instructions present (found: ${HAS_EDIT_CALL}, want 0)" "$( [ "$HAS_EDIT_CALL" -eq 0 ] && echo 0 || echo 1 )"

# Agent must NOT contain Bash() tool calls
HAS_BASH_CALL=$(grep -c 'Bash(' "$AGENT_FILE" || true)
run_test "No Bash() instructions present (found: ${HAS_BASH_CALL}, want 0)" "$( [ "$HAS_BASH_CALL" -eq 0 ] && echo 0 || echo 1 )"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
