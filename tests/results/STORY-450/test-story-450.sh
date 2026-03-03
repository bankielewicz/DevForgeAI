#!/bin/bash
# Test: STORY-450 - Reference File Cleanup and Consistency Fixes
# Story: STORY-450
# Generated: 2026-02-19
# Phase: TDD Red - All tests should FAIL against current file state

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_DIR="$PROJECT_ROOT/src/claude/skills/discovering-requirements"

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=============================================="
echo "  STORY-450: Reference File Cleanup Tests"
echo "  TDD Red Phase - Expecting FAILURES"
echo "=============================================="
echo ""

# =============================================
# AC#1: Remove Duplicate error-handling.md
# =============================================
echo "--- AC#1: Remove Duplicate error-handling.md ---"

# Test 1.1: error-handling.md should be either deleted or a thin redirect index
# Current state: 1062-line file exists with full duplicate content
# After fix: file is either deleted OR is a thin index (under 100 lines)
LINES=$(wc -l < "$SKILL_DIR/references/error-handling.md" 2>/dev/null)
if [ -z "$LINES" ]; then
    # File deleted = pass
    run_test "AC1: error-handling.md deleted or reduced to thin index" 0
elif [ "$LINES" -le 100 ]; then
    # Thin index (100 lines or fewer) = pass
    run_test "AC1: error-handling.md deleted or reduced to thin index" 0
else
    # Still a large file = fail
    run_test "AC1: error-handling.md deleted or reduced to thin index" 1
fi

# Test 1.2: If error-handling.md still exists, it should NOT contain full error procedure content
# (i.e., it should not have detailed recovery steps - only redirect pointers)
if [ -f "$SKILL_DIR/references/error-handling.md" ]; then
    # Full duplicate content includes detailed recovery procedures
    grep -q "Recovery Procedure" "$SKILL_DIR/references/error-handling.md"
    FOUND_FULL_CONTENT=$?
    if [ "$FOUND_FULL_CONTENT" -eq 0 ]; then
        # Still has full content = fail (should be thin index)
        run_test "AC1: error-handling.md does not contain full duplicate procedures" 1
    else
        run_test "AC1: error-handling.md does not contain full duplicate procedures" 0
    fi
else
    # File deleted = pass
    run_test "AC1: error-handling.md does not contain full duplicate procedures" 0
fi

echo ""

# =============================================
# AC#2: Complete Error Type List in SKILL.md
# =============================================
echo "--- AC#2: Complete Error Type List in SKILL.md ---"

# Test 2.1: SKILL.md error handling section should list error type 3 (complexity errors)
# Current state: SKILL.md lists types 1, 2, 4, 6 but is missing type 3
grep -q "error-type-3" "$SKILL_DIR/SKILL.md"
run_test "AC2: SKILL.md lists error-type-3 (complexity errors)" $?

# Test 2.2: SKILL.md error handling section should list error type 5 (constraint conflicts)
# Current state: SKILL.md lists types 1, 2, 4, 6 but is missing type 5
grep -q "error-type-5" "$SKILL_DIR/SKILL.md"
run_test "AC2: SKILL.md lists error-type-5 (constraint conflicts)" $?

# Test 2.3: SKILL.md should reference all 6 error types total
# Current state: says "4 error types" instead of "6 error types"
grep -q "6 error types" "$SKILL_DIR/SKILL.md"
run_test "AC2: SKILL.md states 6 error types (not 4)" $?

echo ""

# =============================================
# AC#3: Fix Stale Phase Reference
# =============================================
echo "--- AC#3: Fix Stale Phase Reference ---"

# Test 3.1: self-validation-workflow.md should NOT contain "Step 6.4"
# Current state: line 251 contains "## References Used in Step 6.4"
grep -q "Step 6\.4" "$SKILL_DIR/references/self-validation-workflow.md"
FOUND_STALE=$?
if [ "$FOUND_STALE" -eq 0 ]; then
    # Found stale reference = fail
    run_test "AC3: self-validation-workflow.md does not contain stale Step 6.4 reference" 1
else
    run_test "AC3: self-validation-workflow.md does not contain stale Step 6.4 reference" 0
fi

# Test 3.2: The references section header should reference "Phase 3.3" not "Step 6.4"
# Current state: line 251 says "## References Used in Step 6.4" - needs to say "Phase 3.3"
# The file title already contains "Phase 3.3" so we check the specific references section header
grep -q "References Used in Phase 3\.3" "$SKILL_DIR/references/self-validation-workflow.md"
run_test "AC3: references section header updated to Phase 3.3 (not Step 6.4)" $?

echo ""

# =============================================
# AC#4: Add Table of Contents to Large Reference Files
# =============================================
echo "--- AC#4: Add Table of Contents to Large Reference Files ---"

# Test 4.1: brainstorm-data-mapping.md should contain a Table of Contents
# Current state: no TOC section exists
grep -qi "Table of Contents" "$SKILL_DIR/references/brainstorm-data-mapping.md"
run_test "AC4: brainstorm-data-mapping.md has Table of Contents" $?

# Test 4.2: user-input-guidance.md should contain a Table of Contents section
# Current state: has "Quick Links" but not a formal "Table of Contents" section
# Note: "Quick Links" with inline links is different from a proper TOC section
grep -qi "## Table of Contents" "$SKILL_DIR/references/user-input-guidance.md"
run_test "AC4: user-input-guidance.md has Table of Contents section" $?

# Test 4.3: completion-handoff.md should contain a Table of Contents
# Current state: no TOC section exists
grep -qi "Table of Contents" "$SKILL_DIR/references/completion-handoff.md"
run_test "AC4: completion-handoff.md has Table of Contents" $?

echo ""

# =============================================
# AC#5: Standardize Model Field Format
# =============================================
echo "--- AC#5: Standardize Model Field Format ---"

# Test 5.1: SKILL.md model field should use quoted format for consistency
# Current state: model: opus (unquoted)
# Standard YAML format should be: model: "opus" (quoted, matching other fields)
grep -q '^model: "' "$SKILL_DIR/SKILL.md"
run_test "AC5: SKILL.md model field uses quoted format for consistency" $?

echo ""

# =============================================
# AC#6: Add Concrete Error Recovery Examples
# =============================================
echo "--- AC#6: Add Concrete Error Recovery Examples ---"

# Test 6.1: user-interaction-patterns.md should contain concrete end-to-end conversation examples
# Current state: has abstract recovery patterns but no concrete conversation examples
# A concrete example would show: User message -> Agent diagnosis -> Fix -> Confirmation
grep -q "User:" "$SKILL_DIR/references/user-interaction-patterns.md"
FOUND_USER=$?
grep -q "Agent:" "$SKILL_DIR/references/user-interaction-patterns.md"
FOUND_AGENT=$?
if [ "$FOUND_USER" -eq 0 ] && [ "$FOUND_AGENT" -eq 0 ]; then
    run_test "AC6: user-interaction-patterns.md has concrete conversation examples (User/Agent)" 0
else
    run_test "AC6: user-interaction-patterns.md has concrete conversation examples (User/Agent)" 1
fi

# Test 6.2: Error recovery section should contain end-to-end example showing diagnosis and fix
# Current state: only has template patterns, not concrete end-to-end scenarios
grep -qi "end-to-end" "$SKILL_DIR/references/user-interaction-patterns.md"
run_test "AC6: user-interaction-patterns.md has end-to-end recovery example" $?

# Test 6.3: Error recovery examples should show a full conversation flow
# A complete concrete example has a diagnosis step followed by confirmation
# Current state: only abstract recovery templates exist, no concrete multi-turn conversation
grep -qi "diagnosis.*fix\|diagnos.*confirm\|recovery confirmed\|issue resolved" "$SKILL_DIR/references/user-interaction-patterns.md"
FOUND_FLOW=$?
if [ "$FOUND_FLOW" -eq 0 ]; then
    run_test "AC6: error recovery examples show diagnosis-to-confirmation flow" 0
else
    run_test "AC6: error recovery examples show diagnosis-to-confirmation flow" 1
fi

echo ""

# =============================================
# Summary
# =============================================
echo "=============================================="
echo "  Results: $PASSED passed, $FAILED failed (of $TOTAL total)"
echo "=============================================="

if [ "$FAILED" -eq 0 ]; then
    echo "  STATUS: ALL TESTS PASS"
    exit 0
else
    echo "  STATUS: $FAILED TESTS FAILING (TDD Red phase expected)"
    exit 1
fi
