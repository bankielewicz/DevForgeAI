#!/bin/bash
# Test: AC#7 - Reference file exists at documented path with required sections
# Story: STORY-501
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
REF_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references/diff-regression-detection.md"

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

echo "=== AC#7: Reference File Exists at Documented Path ==="

# === Test 1: File exists ===
[ -f "$REF_FILE" ]
run_test "Reference file exists at .claude/skills/devforgeai-qa/references/diff-regression-detection.md" $?

# === Test 2: Contains detection_patterns section ===
grep -i -q "detection.pattern\|detection_pattern\|Detection Pattern" "$REF_FILE" 2>/dev/null
run_test "Reference file contains detection_patterns section" $?

# === Test 3: Contains severity_rules section ===
grep -i -q "severity.rule\|severity_rule\|Severity Rule\|Severity Classification" "$REF_FILE" 2>/dev/null
run_test "Reference file contains severity_rules section" $?

# === Test 4: Contains exclusion_patterns section ===
grep -i -q "exclusion.pattern\|exclusion_pattern\|Exclusion Pattern\|File Exclusion" "$REF_FILE" 2>/dev/null
run_test "Reference file contains exclusion_patterns section" $?

# === Test 5: File is valid Markdown (has heading) ===
grep -q "^#" "$REF_FILE" 2>/dev/null
run_test "Reference file is valid Markdown with heading" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
