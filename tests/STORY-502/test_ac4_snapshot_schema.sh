#!/bin/bash
# Test: AC#4 - Snapshot JSON Schema Is Valid and Parseable
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

echo "=== AC#4: Snapshot JSON Schema Is Valid and Parseable ==="

# === Test 1: Schema documents story_id field ===
grep -q "story_id" "$REF_FILE" 2>/dev/null
run_test "Schema documents story_id field" $?

# === Test 2: Schema documents timestamp field ===
grep -q "timestamp" "$REF_FILE" 2>/dev/null
run_test "Schema documents timestamp field" $?

# === Test 3: Schema documents snapshot_type field ===
grep -q "snapshot_type" "$REF_FILE" 2>/dev/null
run_test "Schema documents snapshot_type field" $?

# === Test 4: Schema documents files array ===
grep -q -i "files.*array\|\"files\"" "$REF_FILE" 2>/dev/null
run_test "Schema documents files array" $?

# === Test 5: File entry documents path field ===
grep -q -i "\"path\"\|path.*relative" "$REF_FILE" 2>/dev/null
run_test "File entry documents path field" $?

# === Test 6: File entry documents sha256 as 64 hex chars ===
grep -q -i "sha256.*64\|64.*hex\|64.char" "$REF_FILE" 2>/dev/null
run_test "File entry documents sha256 as 64 hex characters" $?

# === Test 7: File entry documents size_bytes as integer >= 0 ===
grep -q -i "size_bytes.*int\|size_bytes.*>= 0\|size_bytes.*non.negative" "$REF_FILE" 2>/dev/null
run_test "File entry documents size_bytes as integer >= 0" $?

# === Test 8: Documents ISO-8601 timestamp format ===
grep -q -i "ISO.8601\|iso8601" "$REF_FILE" 2>/dev/null
run_test "Documents ISO-8601 timestamp format" $?

# === Test 9: Documents STORY-NNN format for story_id ===
grep -q -i "STORY-.*NNN\|STORY-.\{3,\}\|format.*STORY" "$REF_FILE" 2>/dev/null
run_test "Documents STORY-NNN format for story_id" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
