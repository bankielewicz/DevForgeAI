#!/bin/bash
# Test: STORY-449 - Add Chain-of-Thought Guidance and Feedback Loops
# Story: STORY-449
# Generated: 2026-02-18
# TDD Phase: RED (all tests expected to FAIL)

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=============================================="
echo "STORY-449: CoT Guidance and Feedback Loops"
echo "=============================================="

# === AC#1: Complexity Assessment CoT Instructions ===
echo ""
echo "--- AC#1: Complexity Assessment CoT Instructions ---"

DISCOVERY_WORKFLOW="$PROJECT_ROOT/src/claude/skills/discovering-requirements/references/discovery-workflow.md"

# Test 1: File contains <thinking> tag instructions for complexity scoring
grep -q '<thinking>' "$DISCOVERY_WORKFLOW" 2>/dev/null
run_test "discovery-workflow.md contains thinking tag instructions" $?

# Test 2: Contains scoring for scope dimension
grep -qi 'scope' "$DISCOVERY_WORKFLOW" 2>/dev/null && \
grep -qi 'technical risk' "$DISCOVERY_WORKFLOW" 2>/dev/null && \
grep -qi 'integration surface' "$DISCOVERY_WORKFLOW" 2>/dev/null && \
grep -qi 'domain novelty' "$DISCOVERY_WORKFLOW" 2>/dev/null
run_test "discovery-workflow.md references all 4 dimensions (scope, technical risk, integration surface, domain novelty)" $?

# Test 3: CoT instructions direct agent to score each dimension with explicit reasoning
grep -q 'score.*dimension\|scoring.*reasoning\|explicit reasoning' "$DISCOVERY_WORKFLOW" 2>/dev/null
run_test "discovery-workflow.md contains explicit reasoning instructions for dimension scoring" $?

# === AC#2: Guided Reasoning Between Question Batches ===
echo ""
echo "--- AC#2: Guided Reasoning Between Question Batches ---"

# Test 4: Contains guided reasoning step text
grep -q 'Before asking the next question' "$DISCOVERY_WORKFLOW" 2>/dev/null
run_test "discovery-workflow.md contains guided reasoning step trigger text" $?

# Test 5: Contains ambiguity identification instruction
grep -q 'biggest remaining ambiguity' "$DISCOVERY_WORKFLOW" 2>/dev/null
run_test "discovery-workflow.md contains ambiguity identification instruction" $?

# Test 6: Contains think-through instruction
grep -q 'think through what you.*learned' "$DISCOVERY_WORKFLOW" 2>/dev/null
run_test "discovery-workflow.md contains think-through instruction" $?

# === AC#3: Live-Updated Success Criteria Checklist ===
echo ""
echo "--- AC#3: Live-Updated Success Criteria Checklist ---"

SKILL_MD="$PROJECT_ROOT/src/claude/skills/discovering-requirements/SKILL.md"

# Test 7: Success criteria section contains live-checklist prefix
grep -q 'Copy this checklist into your response at phase start' "$SKILL_MD" 2>/dev/null
run_test "SKILL.md contains live-checklist copy instruction" $?

# Test 8: Contains update instruction
grep -q 'Update checkboxes as you complete each item' "$SKILL_MD" 2>/dev/null
run_test "SKILL.md contains checkbox update instruction" $?

# === AC#4: Validate-Fix-Repeat Feedback Loop ===
echo ""
echo "--- AC#4: Validate-Fix-Repeat Feedback Loop ---"

COMPLETION_HANDOFF="$PROJECT_ROOT/src/claude/skills/discovering-requirements/references/completion-handoff.md"

# Test 9: Contains validate-fix-repeat pattern
grep -qi 'validate-fix-repeat\|validate.*fix.*repeat' "$COMPLETION_HANDOFF" 2>/dev/null
run_test "completion-handoff.md contains validate-fix-repeat pattern" $?

# Test 10: Contains auto-fix instruction
grep -qi 'auto-fix\|auto.fix\|automatically fix' "$COMPLETION_HANDOFF" 2>/dev/null
run_test "completion-handoff.md contains auto-fix instruction" $?

# Test 11: Contains re-validate instruction
grep -qi 're-validate after.*fix\|revalidate after.*fix\|validate again after.*fix\|fix.*then.*re-validate\|fix.*then.*revalidate' "$COMPLETION_HANDOFF" 2>/dev/null
run_test "completion-handoff.md contains re-validate-after-fix instruction" $?

# Test 12: Still halts on unfixable critical failures
grep -qi 'halt.*unfixable\|unfixable.*halt\|critical.*halt\|halt.*critical' "$COMPLETION_HANDOFF" 2>/dev/null
run_test "completion-handoff.md still HALTs on unfixable critical failures" $?

# Test 13: Replaces validate-halt pattern (should NOT contain standalone validate-halt as primary pattern)
# This test checks the loop replaces the old pattern - presence of feedback loop keyword
grep -qi 'feedback loop\|loop.*validate\|repeat.*loop' "$COMPLETION_HANDOFF" 2>/dev/null
run_test "completion-handoff.md implements feedback loop pattern" $?

# === Summary ===
echo ""
echo "=============================================="
echo "Results: $PASSED passed, $FAILED failed"
echo "Total:   $((PASSED + FAILED)) tests"
echo "=============================================="
[ $FAILED -eq 0 ] && exit 0 || exit 1
