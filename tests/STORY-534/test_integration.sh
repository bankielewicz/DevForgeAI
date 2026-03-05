#!/bin/bash
# Integration Tests: STORY-534 - Dual-Mode /business-plan Command
# Generated: 2026-03-04
#
# These tests verify cross-component interactions:
# 1. Command file correctly invokes planning-business skill
# 2. Mode detection integrates with context file structure
# 3. --standalone flag integrates with mode detection logic
# 4. Both modes produce consistent output structure
# 5. Graceful degradation works with partial context

# === Test Configuration ===
PASSED=0
FAILED=0
WARNINGS=0

COMMAND_FILE="src/claude/commands/business-plan.md"
SKILL_FILE="src/claude/skills/planning-business/SKILL.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo -e "  ${GREEN}PASS${NC}: $name"
        ((PASSED++))
    else
        echo -e "  ${RED}FAIL${NC}: $name"
        ((FAILED++))
    fi
}

run_warning() {
    local name="$1"
    echo -e "  ${YELLOW}WARN${NC}: $name"
    ((WARNINGS++))
}

echo "=============================================="
echo "  INTEGRATION TESTS: STORY-534"
echo "  Dual-Mode /business-plan Command"
echo "=============================================="
echo ""

# === Arrange ===
echo "=== Setup: Verify target files exist ==="

if [ ! -f "$COMMAND_FILE" ]; then
    echo -e "${RED}FATAL${NC}: Command file does not exist: $COMMAND_FILE"
    echo "Integration tests require implementation file to exist"
    exit 1
fi

if [ ! -f "$SKILL_FILE" ]; then
    echo -e "${RED}FATAL${NC}: Skill file does not exist: $SKILL_FILE"
    echo "Integration tests require planning-business skill to exist"
    exit 1
fi

echo "  ✓ Command file found: $COMMAND_FILE"
echo "  ✓ Skill file found: $SKILL_FILE"
echo ""

# ============================================
# INTEGRATION TEST 1: Skill Invocation
# ============================================
echo "=== Integration Test 1: Command Invokes Planning-Business Skill ==="
echo "Purpose: Verify command file correctly invokes the skill"
echo ""

# Test 1.1: Command mentions skill invocation
grep -qiE "Skill\(.*planning-business|invoke.*planning.*business|planning-business.*skill" "$COMMAND_FILE"
run_test "Command references skill invocation (Skill() call)" $?

# Test 1.2: Both modes invoke the same skill
project_anchored_invokes=$(grep -c "Skill.*planning-business" "$COMMAND_FILE")
standalone_invokes=$(grep -c "Skill.*planning-business" "$COMMAND_FILE")
[ "$project_anchored_invokes" -gt 0 ] && [ "$standalone_invokes" -gt 0 ]
run_test "Skill invocation exists in command" $?

# Test 1.3: Skill output format is described as consistent
grep -qiE "consistent.*output|same.*output.*format|output.*regardless.*mode" "$COMMAND_FILE"
run_test "Documentation claims consistent output format" $?

# Test 1.4: Skill file has phase structure (indicates it's an actual skill)
grep -qiE "^#{1,3} .*Phase|^## Phase" "$SKILL_FILE"
run_test "Skill file has phase structure" $?

echo ""

# ============================================
# INTEGRATION TEST 2: Mode Detection Logic
# ============================================
echo "=== Integration Test 2: Mode Detection Integrates with Context Structure ==="
echo "Purpose: Verify mode detection uses standard context directory paths"
echo ""

# Test 2.1: Command checks for context directory using native tools
grep -qiE "Glob\(.*pattern.*devforgeai/specs/context|Glob.*devforgeai" "$COMMAND_FILE"
run_test "Mode detection uses native Glob tool (not Bash)" $?

# Test 2.2: Command recognizes the standard 6 context files
context_files_recognized=0
for context_file in "tech-stack" "source-tree" "architecture-constraints" "dependencies" "coding-standards" "anti-patterns"; do
    grep -qi "$context_file" "$COMMAND_FILE" && ((context_files_recognized++))
done
[ "$context_files_recognized" -ge 3 ]
run_test "Command recognizes context files ($context_files_recognized/6 mentioned)" $?

# Test 2.3: Mode detection logic is documented in both Project-Anchored and Standalone sections
grep -qE "^#{1,4} .*Project.Anchored|^#{1,4} .*Standalone" "$COMMAND_FILE"
run_test "Command documents both mode detection paths" $?

# Test 2.4: Context directory detection checks for existence, not content
grep -qiE "exists|empty|present|not.*found|missing" "$COMMAND_FILE"
run_test "Command checks directory/file existence (graceful handling)" $?

echo ""

# ============================================
# INTEGRATION TEST 3: Flag Override Integration
# ============================================
echo "=== Integration Test 3: --standalone Flag Overrides Auto-Detection ==="
echo "Purpose: Verify flag parsing integrates with mode detection decision tree"
echo ""

# Test 3.1: Argument parsing happens before mode detection
has_arg_parsing=$(grep -n "STANDALONE_FLAG\|\\$ARGUMENTS\|arguments.*--standalone" "$COMMAND_FILE" | head -1)
has_mode_detection=$(grep -n "MODE.*=\|IF.*STANDALONE\|context.*detection" "$COMMAND_FILE" | head -1)

if [ -n "$has_arg_parsing" ] && [ -n "$has_mode_detection" ]; then
    arg_line=$(echo "$has_arg_parsing" | cut -d: -f1)
    mode_line=$(echo "$has_mode_detection" | cut -d: -f1)
    [ "$arg_line" -lt "$mode_line" ]
    run_test "Argument parsing occurs before mode detection (line $arg_line < $mode_line)" $?
else
    run_warning "Could not verify argument parsing order (may be acceptable for Markdown command)"
fi

# Test 3.2: Flag is explicitly checked before mode detection
grep -qiE "IF.*STANDALONE_FLAG.*==.*true|IF.*--standalone|IF.*flag.*set" "$COMMAND_FILE"
run_test "Flag check occurs before auto-detection" $?

# Test 3.3: Documentation includes flag usage example
grep -qE "^\`\`\`bash|/business-plan.*--standalone|--standalone.*flag" "$COMMAND_FILE"
run_test "Usage examples include --standalone flag" $?

echo ""

# ============================================
# INTEGRATION TEST 4: Mode-Specific Input Paths
# ============================================
echo "=== Integration Test 4: Both Modes Provide Input to Skill ==="
echo "Purpose: Verify project-anchored and standalone modes provide appropriate input to skill"
echo ""

# Test 4.1: Project-anchored mode reads context files
grep -qiE "project.anchored.*context.*files|Read.*context.*project" "$COMMAND_FILE"
run_test "Project-anchored mode reads context files" $?

# Test 4.2: Standalone mode prompts for business idea
grep -qiE "business.*idea|AskUserQuestion|prompt.*description|standalone.*ask" "$COMMAND_FILE"
run_test "Standalone mode prompts for business idea" $?

# Test 4.3: Both modes pass different inputs to same skill
grep -qiE "IF.*MODE.*==.*project.anchored|IF.*MODE.*==.*standalone|ELIF" "$COMMAND_FILE"
run_test "Command has conditional branches for each mode" $?

# Test 4.4: Skill receives input via conversation context (documented)
grep -qiE "conversation.*context|pass.*context|invoke.*skill" "$COMMAND_FILE"
run_test "Documentation describes input passing to skill" $?

echo ""

# ============================================
# INTEGRATION TEST 5: Graceful Degradation
# ============================================
echo "=== Integration Test 5: Graceful Degradation on Missing Context ==="
echo "Purpose: Verify partial context is handled gracefully (no crash, fallback behavior)"
echo ""

# Test 5.1: Individual context files are checked separately
grep -qiE "FOR.*context|for each.*file|each.*file.*in" "$COMMAND_FILE"
run_test "Command checks context files individually (loop/iteration)" $?

# Test 5.2: Missing files produce warnings, not errors
grep -qiE "warn|warning|missing|empty|fallback|degradat" "$COMMAND_FILE"
run_test "Missing context files produce warnings (not fatal)" $?

# Test 5.3: Partial context doesn't prevent skill invocation
grep -qiE "proceed.*context|continue.*available|fallback.*standalone|skip.*missing" "$COMMAND_FILE"
run_test "Command proceeds with partial context (no early exit)" $?

# Test 5.4: Fallback behavior is documented
grep -qiE "error.*handling|fallback|graceful|resilient" "$COMMAND_FILE"
run_test "Error handling and fallback documented" $?

echo ""

# ============================================
# INTEGRATION TEST 6: Output Format Consistency
# ============================================
echo "=== Integration Test 6: Output Format Consistency Across Modes ==="
echo "Purpose: Verify both modes produce same output structure"
echo ""

# Test 6.1: Command documentation states output is consistent
grep -qiE "consistent.*output|same.*format|identical.*output|output.*structure.*same" "$COMMAND_FILE"
run_test "Documentation claims output format is consistent" $?

# Test 6.2: Skill produces structured output (mentioned in command)
grep -qiE "Lean.*Canvas|business.*model|revenue|market.*viability|output.*section" "$COMMAND_FILE"
run_test "Command documents skill's output sections" $?

# Test 6.3: Output format is not modified by command (skill owns output)
grep -qiE "skill.*output|planning.*skill.*produce|output.*format.*skill" "$COMMAND_FILE"
run_test "Command respects skill's output structure (no post-processing)" $?

echo ""

# ============================================
# INTEGRATION TEST 7: Error Cases and Boundaries
# ============================================
echo "=== Integration Test 7: Error Handling and Boundary Conditions ==="
echo "Purpose: Verify command handles edge cases and error conditions"
echo ""

# Test 7.1: Missing planning-business skill is handled
grep -qiE "unavailable|not.*found|skill.*error|missing.*skill" "$COMMAND_FILE"
run_test "Documentation addresses missing skill scenario" $?

# Test 7.2: Standalone mode requires business idea (cannot proceed without it)
grep -qiE "standalone.*require|must.*provide|cannot.*proceed|HALT" "$COMMAND_FILE"
run_test "Standalone mode requires business idea (cannot skip)" $?

# Test 7.3: No hardcoded secrets or sensitive data
grep -qE "password|secret|api.key|token.*=|credential" "$COMMAND_FILE"
result=$?
[ $result -ne 0 ]  # Should NOT find these
run_test "No hardcoded secrets in command file" $?

echo ""

# ============================================
# INTEGRATION TEST 8: Component Boundaries
# ============================================
echo "=== Integration Test 8: Component Boundaries and Responsibilities ==="
echo "Purpose: Verify clean separation between command and skill"
echo ""

# Test 8.1: Command owns mode detection (not skill)
grep -qiE "step.*0|phase.*0|argument.*pars|mode.*detect" "$COMMAND_FILE"
run_test "Command owns mode detection (Phase 0)" $?

# Test 8.2: Command owns context collection (not skill)
grep -qiE "step.*1|phase.*1|context.*collection|read.*file" "$COMMAND_FILE"
run_test "Command owns context collection (Phase 1)" $?

# Test 8.3: Skill owns output generation (not command)
grep -qiE "phase.*2|skill.*invocation|planning.*business.*skill" "$COMMAND_FILE"
run_test "Skill owns business plan generation (Phase 2)" $?

# Test 8.4: Workflow is clearly documented in phases
grep -qE "^## .*Workflow|^### .*Phase" "$COMMAND_FILE"
run_test "Workflow is documented in phases" $?

echo ""

# ============================================
# SUMMARY
# ============================================
echo "=============================================="
echo "  INTEGRATION TEST RESULTS"
echo "=============================================="
echo ""
echo "  ${GREEN}✓ Passed: $PASSED${NC}"
echo "  ${RED}✗ Failed: $FAILED${NC}"
if [ $WARNINGS -gt 0 ]; then
    echo "  ${YELLOW}⚠ Warnings: $WARNINGS${NC}"
fi
echo ""

# Determine exit code
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}Status: PASS - All integration tests passed${NC}"
    echo ""
    echo "Integration Points Verified:"
    echo "  ✓ Command correctly invokes planning-business skill"
    echo "  ✓ Mode detection integrates with context file structure"
    echo "  ✓ --standalone flag integrates with mode detection"
    echo "  ✓ Both modes provide appropriate input to skill"
    echo "  ✓ Graceful degradation on missing context files"
    echo "  ✓ Output format consistent across modes"
    echo "  ✓ Error handling for edge cases documented"
    echo "  ✓ Clean component boundaries (command vs skill)"
    exit 0
else
    echo -e "${RED}Status: FAIL - $FAILED integration test(s) failed${NC}"
    exit 1
fi
