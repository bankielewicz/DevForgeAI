#!/bin/bash
# Test: AC#2 - QA Phase Detects Checksum Mismatch and Blocks Approval
# Story: STORY-502
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
QA_REF="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references/diff-regression-detection.md"

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

echo "=== AC#2: QA Detects Checksum Mismatch and Blocks Approval ==="

# === Test 1: QA reference contains snapshot comparison algorithm ===
grep -q -i "snapshot.comparison.algorithm\|checksum.comparison\|integrity.verification" "$QA_REF" 2>/dev/null
run_test "QA reference contains snapshot comparison algorithm" $?

# === Test 2: Specifies CRITICAL: TEST TAMPERING finding format ===
grep -q "CRITICAL.*TEST.TAMPERING\|TEST.TAMPERING.*CRITICAL" "$QA_REF" 2>/dev/null
run_test "QA reference specifies CRITICAL: TEST TAMPERING finding" $?

# === Test 3: Finding includes expected and actual sha256 ===
grep -q -i "expected.*sha256\|actual.*sha256\|expected_sha256\|actual_sha256" "$QA_REF" 2>/dev/null
run_test "Finding format includes expected and actual sha256" $?

# === Test 4: Overall verdict FAIL on mismatch ===
grep -q -i "overall_verdict.*FAIL\|verdict.*FAIL.*mismatch" "$QA_REF" 2>/dev/null
run_test "Overall verdict set to FAIL on mismatch" $?

# === Test 5: No override mechanism exists ===
grep -q -i "no.override\|cannot.be.deferred\|cannot.be.bypassed\|no.bypass" "$QA_REF" 2>/dev/null
run_test "No override mechanism documented" $?

# === Test 6: New file addition detected as tampering ===
grep -q -i "unauthorized.file\|new.file.*tampering\|file.added" "$QA_REF" 2>/dev/null
run_test "New file addition detected as tampering" $?

# === Test 7: Deleted file detected as tampering ===
grep -q -i "file.deleted\|deleted.*tampering\|missing.file.*critical" "$QA_REF" 2>/dev/null
run_test "Deleted file detected as tampering" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
