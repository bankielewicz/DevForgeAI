#!/bin/bash
# Test Suite: STORY-217 Pre-Flight HALT Logic Validation
# Purpose: Verify SKILL.md has RCA-021 compliant HALT patterns in Phases 1-4
# Status: These tests MUST FAIL initially (TDD Red phase)

SKILL_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/SKILL.md"
PASS=0
FAIL=0

echo "=============================================="
echo "STORY-217: Pre-Flight HALT Logic Tests"
echo "Target: $SKILL_FILE"
echo "=============================================="

# AC-1: Phase 1 Pre-Flight Has HALT Logic
test_ac1_phase1_halt() {
    echo -n "AC-1: Phase 1 Pre-Flight HALT logic... "

    # Must contain CRITICAL ERROR for Phase 0
    if grep -q 'CRITICAL ERROR.*Phase 0 not verified complete' "$SKILL_FILE"; then
        echo "PASS"
        ((PASS++))
    else
        echo "FAIL - Missing: CRITICAL ERROR for Phase 0"
        ((FAIL++))
    fi
}

# AC-2: Phase 2 Pre-Flight Has HALT Logic
test_ac2_phase2_halt() {
    echo -n "AC-2: Phase 2 Pre-Flight HALT logic... "

    if grep -q 'CRITICAL ERROR.*Phase 1 not verified complete' "$SKILL_FILE"; then
        echo "PASS"
        ((PASS++))
    else
        echo "FAIL - Missing: CRITICAL ERROR for Phase 1"
        ((FAIL++))
    fi
}

# AC-3: Phase 3 Pre-Flight Has HALT Logic
test_ac3_phase3_halt() {
    echo -n "AC-3: Phase 3 Pre-Flight HALT logic... "

    if grep -q 'CRITICAL ERROR.*Phase 2 not verified complete' "$SKILL_FILE"; then
        echo "PASS"
        ((PASS++))
    else
        echo "FAIL - Missing: CRITICAL ERROR for Phase 2"
        ((FAIL++))
    fi
}

# AC-4: Phase 4 Pre-Flight Has HALT Logic
test_ac4_phase4_halt() {
    echo -n "AC-4: Phase 4 Pre-Flight HALT logic... "

    if grep -q 'CRITICAL ERROR.*Phase 3 not verified complete' "$SKILL_FILE"; then
        echo "PASS"
        ((PASS++))
    else
        echo "FAIL - Missing: CRITICAL ERROR for Phase 3"
        ((FAIL++))
    fi
}

# AC-5: Phase 1 has complete RCA-021 pattern
test_ac5_phase1_complete_pattern() {
    echo -n "AC-5a: Phase 1 complete pattern (HALT message)... "

    if grep -q 'HALT.*Phase 1 cannot execute without Phase 0 completion' "$SKILL_FILE"; then
        echo "PASS"
        ((PASS++))
    else
        echo "FAIL - Missing: HALT with cannot execute message"
        ((FAIL++))
    fi
}

# AC-5: Phase 1 has Display instruction
test_ac5_phase1_display() {
    echo -n "AC-5b: Phase 1 Display instruction... "

    if grep -q 'Display.*Previous phase.*Phase 0.*must complete successfully' "$SKILL_FILE"; then
        echo "PASS"
        ((PASS++))
    else
        echo "FAIL - Missing: Display with previous phase message"
        ((FAIL++))
    fi
}

# AC-5: Phase 1 has Exit code
test_ac5_phase1_exit() {
    echo -n "AC-5c: Phase 1 Exit code... "

    if grep -q 'Exit.*Code 1.*phase sequencing violation' "$SKILL_FILE"; then
        echo "PASS"
        ((PASS++))
    else
        echo "FAIL - Missing: Exit Code 1 for phase sequencing"
        ((FAIL++))
    fi
}

# AC-5: Phase 1 has Instruction
test_ac5_phase1_instruction() {
    echo -n "AC-5d: Phase 1 Instruction step... "

    if grep -q 'Instruction.*Start workflow from Phase 0' "$SKILL_FILE"; then
        echo "PASS"
        ((PASS++))
    else
        echo "FAIL - Missing: Instruction to start from Phase 0"
        ((FAIL++))
    fi
}

# Run all tests
test_ac1_phase1_halt
test_ac2_phase2_halt
test_ac3_phase3_halt
test_ac4_phase4_halt
test_ac5_phase1_complete_pattern
test_ac5_phase1_display
test_ac5_phase1_exit
test_ac5_phase1_instruction

echo "=============================================="
echo "Results: $PASS passed, $FAIL failed"
echo "=============================================="

# Exit with failure if any tests failed
if [ $FAIL -gt 0 ]; then
    exit 1
else
    exit 0
fi
