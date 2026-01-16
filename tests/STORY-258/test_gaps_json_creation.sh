#!/bin/bash
# STORY-258: Test gaps.json Creation Before Status Update
# TDD Red Phase - These tests MUST FAIL before implementation
# Target: .claude/skills/devforgeai-qa/SKILL.md Step 3.4

SKILL_FILE=".claude/skills/devforgeai-qa/SKILL.md"
PASS_COUNT=0
FAIL_COUNT=0

echo "=== STORY-258: gaps.json Creation Tests ==="
echo "Target: $SKILL_FILE"
echo ""

# AC#1: gaps.json Creation BEFORE Status Update
test_ac1_gaps_before_status() {
    echo "TEST: AC#1 - gaps.json created BEFORE status update"
    if grep -qE "gaps\.json.*BEFORE.*status|Create gaps\.json.*prior.*status" "$SKILL_FILE"; then
        echo "  PASS: Pattern found"
        ((PASS_COUNT++))
    else
        echo "  FAIL: Missing gaps.json BEFORE status update pattern"
        ((FAIL_COUNT++))
    fi
}

# AC#1: Verify ordering - Step 3.3.5 exists and comes before Step 3.4
test_ac1_step_ordering() {
    echo "TEST: AC#1 - Step 3.3.5 (gaps.json) exists before Step 3.4 (status update)"
    # Step 3.3.5 must exist and contain Write gaps.json
    # Get line numbers to verify ordering
    local step_335_line=$(grep -n "Step 3.3.5" "$SKILL_FILE" | head -1 | cut -d: -f1)
    local step_34_line=$(grep -n "Step 3.4" "$SKILL_FILE" | head -1 | cut -d: -f1)

    if [ -n "$step_335_line" ] && [ -n "$step_34_line" ] && [ "$step_335_line" -lt "$step_34_line" ]; then
        # Verify Step 3.3.5 contains Write gaps.json
        if grep -A30 "Step 3.3.5" "$SKILL_FILE" | grep -q "Write.*gaps\.json"; then
            echo "  PASS: Step 3.3.5 (line $step_335_line) precedes Step 3.4 (line $step_34_line)"
            ((PASS_COUNT++))
        else
            echo "  FAIL: Step 3.3.5 missing Write gaps.json"
            ((FAIL_COUNT++))
        fi
    else
        echo "  FAIL: Step 3.3.5 not found before Step 3.4"
        ((FAIL_COUNT++))
    fi
}

# AC#2: gaps.json Contains Required Fields
test_ac2_violation_fields() {
    echo "TEST: AC#2 - gaps.json schema includes type, severity, message, remediation"
    local found=0
    grep -qE "type.*severity.*message.*remediation|violations.*\[.*type|Each violation has type" "$SKILL_FILE" && found=1
    if [ $found -eq 1 ]; then
        echo "  PASS: Violation fields documented"
        ((PASS_COUNT++))
    else
        echo "  FAIL: Missing violation field schema (type, severity, message, remediation)"
        ((FAIL_COUNT++))
    fi
}

# AC#2: Correct file path pattern
test_ac2_file_path() {
    echo "TEST: AC#2 - gaps.json path is devforgeai/qa/reports/{STORY-ID}-gaps.json"
    if grep -qE "devforgeai/qa/reports/.*STORY.*gaps\.json" "$SKILL_FILE"; then
        echo "  PASS: Correct path pattern found"
        ((PASS_COUNT++))
    else
        echo "  FAIL: Missing correct gaps.json path pattern"
        ((FAIL_COUNT++))
    fi
}

# AC#3: Confirmation Message
test_ac3_confirmation_message() {
    echo "TEST: AC#3 - Confirmation message displayed after creation"
    if grep -qE "gaps\.json created.*required for QA Failed|Display.*gaps\.json created" "$SKILL_FILE"; then
        echo "  PASS: Confirmation message found"
        ((PASS_COUNT++))
    else
        echo "  FAIL: Missing confirmation message pattern"
        ((FAIL_COUNT++))
    fi
}

# AC#4: Idempotent Overwrite
test_ac4_idempotent() {
    echo "TEST: AC#4 - Idempotent overwrite (not append)"
    if grep -qE "overwrite.*gaps\.json|Write.*gaps\.json.*overwrite|idempotent.*creation" "$SKILL_FILE"; then
        echo "  PASS: Idempotent overwrite documented"
        ((PASS_COUNT++))
    else
        echo "  FAIL: Missing idempotent overwrite behavior"
        ((FAIL_COUNT++))
    fi
}

# RCA-002 Reference
test_rca_reference() {
    echo "TEST: RCA-002 reference in Step 3.4"
    if grep -A100 "Step 3.4" "$SKILL_FILE" | grep -qE "RCA-002"; then
        echo "  PASS: RCA-002 reference found"
        ((PASS_COUNT++))
    else
        echo "  FAIL: Missing RCA-002 reference"
        ((FAIL_COUNT++))
    fi
}

# Run all tests
test_ac1_gaps_before_status
test_ac1_step_ordering
test_ac2_violation_fields
test_ac2_file_path
test_ac3_confirmation_message
test_ac4_idempotent
test_rca_reference

echo ""
echo "=== RESULTS ==="
echo "PASSED: $PASS_COUNT"
echo "FAILED: $FAIL_COUNT"
echo ""

if [ $FAIL_COUNT -gt 0 ]; then
    echo "STATUS: TDD RED - Tests failing as expected (before implementation)"
    exit 1
else
    echo "STATUS: TDD GREEN - All tests pass"
    exit 0
fi
