#!/bin/bash
# Test: AC#1 - Snapshot Created at Phase 02 Completion
# Story: STORY-502
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
REF_FILE="${PROJECT_ROOT}/src/claude/skills/implementing-stories/references/test-integrity-snapshot.md"

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

echo "=== AC#1: Snapshot Created at Phase 02 Completion ==="

# === Test 1: Reference file exists ===
test -f "$REF_FILE"
run_test "test-integrity-snapshot.md reference file exists" $?

# === Test 2: Contains file discovery patterns section ===
grep -q -i "file.discovery.pattern" "$REF_FILE" 2>/dev/null
run_test "Reference file contains file discovery patterns section" $?

# === Test 3: Contains snapshot creation algorithm section ===
grep -q -i "snapshot.creation.algorithm" "$REF_FILE" 2>/dev/null
run_test "Reference file contains snapshot creation algorithm section" $?

# === Test 4: Contains Phase 02 integration section ===
grep -q -i "phase.02.integration\|phase.2.integration" "$REF_FILE" 2>/dev/null
run_test "Reference file contains Phase 02 integration section" $?

# === Test 5: Documents glob patterns for test frameworks ===
grep -q -i "pytest\|jest\|vitest\|xunit" "$REF_FILE" 2>/dev/null
run_test "Reference file documents test framework glob patterns" $?

# === Test 6: Documents SHA-256 computation ===
grep -q -i "sha.256\|sha256" "$REF_FILE" 2>/dev/null
run_test "Reference file documents SHA-256 computation" $?

# === Test 7: Documents JSON output path ===
grep -q "red-phase-checksums.json" "$REF_FILE" 2>/dev/null
run_test "Reference file documents red-phase-checksums.json output path" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
