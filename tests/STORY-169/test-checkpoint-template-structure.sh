#!/bin/bash

# STORY-169: RCA-013 Phase Validation Checkpoint
# Integration Test: Checkpoint Template Structure Validation
# Status: TDD Red (should FAIL - checkpoint template not yet added per Technical Specification)
#
# This test validates that the checkpoint template defined in the Technical Specification
# is correctly implemented in SKILL.md:
#
# ### Phase X Validation Checkpoint
#
# Before marking Phase X complete, verify:
# - [ ] {Subagent 1} invoked (check for Task() call in conversation)
# - [ ] {Subagent 2} invoked (check for Task() call in conversation)
#
# IF any check fails:
#   Display: "Phase X incomplete: {missing items}"
#   HALT (do not proceed to Phase X+1)
#   Prompt: "Complete missing items before proceeding"
#
# IF all checks pass:
#   Display: "Phase X validation passed - all mandatory steps completed"
#   Proceed to Phase X+1

set -e

# Load test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "STORY-169: Checkpoint Template Structure Validation (Integration)"
echo "========================================================================"
echo ""

# Read SKILL.md content
SKILL_CONTENT=$(cat "$SKILL_FILE" 2>/dev/null || echo "")

# Test 1: Checkpoint template section header exists in SKILL.md
echo "Test 1: Checkpoint template documentation exists in SKILL.md"
if echo "$SKILL_CONTENT" | grep -qE "### Phase.*Validation Checkpoint|## Phase.*Validation Checkpoint"; then
    echo -e "${GREEN}PASS${NC} Phase Validation Checkpoint section exists"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase Validation Checkpoint section not found"
    echo "  Expected: '### Phase X Validation Checkpoint' section header"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2: Template includes "check for Task() call" instruction
echo ""
echo "Test 2: Template includes Task() call verification instruction"
if echo "$SKILL_CONTENT" | grep -qiE "check.*for.*Task\(\).*call|Task\(\).*call.*in.*conversation"; then
    echo -e "${GREEN}PASS${NC} Template includes Task() call verification"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Template missing Task() call verification instruction"
    echo "  Expected: 'check for Task() call in conversation'"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Template has both HALT and PASS branches
echo ""
echo "Test 3: Template has both HALT (fail) and PASS (success) branches"
HAS_HALT=$(echo "$SKILL_CONTENT" | grep -ciE "IF.*any.*check.*fails|IF.*check.*fails")
HAS_PASS=$(echo "$SKILL_CONTENT" | grep -ciE "IF.*all.*checks.*pass")

if [[ "$HAS_HALT" -gt 0 ]] && [[ "$HAS_PASS" -gt 0 ]]; then
    echo -e "${GREEN}PASS${NC} Template has both HALT and PASS branches"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Template missing conditional branches"
    echo "  Found HALT branches: $HAS_HALT (expected >= 1)"
    echo "  Found PASS branches: $HAS_PASS (expected >= 1)"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 4: Subagent Verification Logic section exists per Technical Specification
echo ""
echo "Test 4: Subagent Verification Logic section exists"
# Per Technical Spec:
# FOR required_subagent in phase_required_subagents:
#   IF conversation contains Task(subagent_type="{required_subagent}"):
#     mark_verified(required_subagent)
#   ELSE:
#     add_to_missing(required_subagent)
if echo "$SKILL_CONTENT" | grep -qiE "Subagent Verification Logic|FOR.*required_subagent|Task\(subagent_type"; then
    echo -e "${GREEN}PASS${NC} Subagent Verification Logic section exists"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Subagent Verification Logic section not found"
    echo "  Expected: Logic to iterate and verify subagent Task() calls"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 5: Required Subagents Per Phase table is accurate
echo ""
echo "Test 5: Required Subagents Per Phase table contains all required subagents"
# Check Phase 03 subagents (backend-architect OR frontend-developer, context-validator)
# Check Phase 04 subagents (refactoring-specialist, code-reviewer)
# Check Phase 05 subagents (integration-tester)

PHASE_03_OK=false
PHASE_04_OK=false
PHASE_05_OK=false

# Phase 03 check
if echo "$SKILL_CONTENT" | grep -qE "03.*backend-architect.*OR.*frontend-developer|03.*context-validator"; then
    PHASE_03_OK=true
fi

# Phase 04 check
if echo "$SKILL_CONTENT" | grep -qE "04.*refactoring-specialist|04.*code-reviewer"; then
    PHASE_04_OK=true
fi

# Phase 05 check
if echo "$SKILL_CONTENT" | grep -qE "05.*integration-tester"; then
    PHASE_05_OK=true
fi

if $PHASE_03_OK && $PHASE_04_OK && $PHASE_05_OK; then
    echo -e "${GREEN}PASS${NC} Required Subagents table is complete"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Required Subagents table is incomplete"
    echo "  Phase 03 subagents listed: $PHASE_03_OK"
    echo "  Phase 04 subagents listed: $PHASE_04_OK"
    echo "  Phase 05 subagents listed: $PHASE_05_OK"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 6: Both .claude/ and src/claude/ versions should be updated (per DoD)
echo ""
echo "Test 6: Checking for src/claude/ version (if exists)"
SRC_SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-development/SKILL.md"
if [[ -f "$SRC_SKILL_FILE" ]]; then
    SRC_CONTENT=$(cat "$SRC_SKILL_FILE" 2>/dev/null || echo "")
    if echo "$SRC_CONTENT" | grep -qE "Phase.*Validation Checkpoint"; then
        echo -e "${GREEN}PASS${NC} src/claude/ version also has Phase Validation Checkpoint"
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC} src/claude/ version missing Phase Validation Checkpoint"
        echo "  Both .claude/ and src/claude/ versions must be updated per DoD"
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
else
    echo -e "${YELLOW}SKIP${NC} src/claude/ version not found (may not exist yet)"
    # Don't count as failure - src/claude/ might not exist
fi

# Print summary
print_test_summary "Checkpoint Template Structure Tests"
exit_with_result
