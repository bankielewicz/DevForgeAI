#!/bin/bash
# Test: AC#4 - Functionality Preservation (No Regression)
# Story: STORY-332 - Refactor session-miner.md with Progressive Disclosure
# Purpose: Verify all session mining features are documented across core + references
#
# Expected: FAIL (Red phase) - Refactored files do not exist yet

# set -e  # Removed to allow all tests to run

# Configuration
CORE_FILE="src/claude/agents/session-miner.md"
REF_DIR="src/claude/agents/session-miner/references"

# Key functionality that MUST be preserved (from original session-miner.md)
REQUIRED_FUNCTIONALITY=(
    "SessionEntry"              # Data model
    "timestamp"                 # SessionEntry field
    "command"                   # SessionEntry field
    "status"                    # SessionEntry field
    "duration_ms"               # SessionEntry field
    "pagination"                # Large file processing
    "error.?categori"           # STORY-229 error categorization
    "ErrorEntry"                # STORY-229 error model
    "N.?gram|bigram|trigram"    # STORY-226 N-gram analysis (extended regex |)
    "anti.?pattern"             # STORY-231 anti-pattern mining
    "JSON.?Lines|jsonl"         # Parsing format (extended regex |)
    "streaming|chunk"           # Large file streaming (extended regex |)
)

FEATURE_DESCRIPTIONS=(
    "SessionEntry data model"
    "timestamp field extraction"
    "command field extraction"
    "status field mapping"
    "duration_ms field"
    "pagination for large files"
    "error categorization (STORY-229)"
    "ErrorEntry model (STORY-229)"
    "N-gram analysis (STORY-226)"
    "anti-pattern mining (STORY-231)"
    "JSON Lines parsing"
    "streaming/chunked processing"
)

# Integration points (downstream stories)
STORY_REFERENCES=(
    "STORY-222"
    "STORY-223"
    "STORY-224"
    "STORY-226"
    "STORY-227"
    "STORY-229"
    "STORY-231"
)

# Test tracking
TESTS_PASSED=0
TESTS_FAILED=0

echo "=============================================="
echo "  AC#4: Functionality Preservation Tests"
echo "  STORY-332 - Progressive Disclosure Refactor"
echo "=============================================="
echo ""

# Test 1: Verify core file exists
echo "Test 1: Core file exists"
if [[ -f "$CORE_FILE" ]]; then
    echo "  PASS: $CORE_FILE exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: $CORE_FILE does not exist"
    ((TESTS_FAILED++))
    echo ""
    echo "=============================================="
    echo "  RESULT: $TESTS_PASSED passed, $TESTS_FAILED failed"
    echo "  STATUS: FAILED (cannot continue without file)"
    echo "=============================================="
    exit 1
fi

# Test 2: Verify references directory exists
echo ""
echo "Test 2: References directory exists"
if [[ -d "$REF_DIR" ]]; then
    echo "  PASS: $REF_DIR exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: $REF_DIR does not exist"
    ((TESTS_FAILED++))
fi

# Test 3: Check all required functionality across core + references
echo ""
echo "Test 3: Required functionality documented (core + references)"

# Combine all files for searching
ALL_CONTENT=$(cat "$CORE_FILE" 2>/dev/null)
if [[ -d "$REF_DIR" ]]; then
    ALL_CONTENT+=$'\n'$(cat "$REF_DIR"/*.md 2>/dev/null || echo "")
fi

FOUND_COUNT=0
MISSING_FUNCTIONALITY=()

for i in "${!REQUIRED_FUNCTIONALITY[@]}"; do
    pattern="${REQUIRED_FUNCTIONALITY[$i]}"
    description="${FEATURE_DESCRIPTIONS[$i]}"

    if echo "$ALL_CONTENT" | grep -qiE "$pattern"; then
        ((FOUND_COUNT++))
    else
        MISSING_FUNCTIONALITY+=("$description")
    fi
done

TOTAL_REQUIRED=${#REQUIRED_FUNCTIONALITY[@]}
if [[ $FOUND_COUNT -eq $TOTAL_REQUIRED ]]; then
    echo "  PASS: All $TOTAL_REQUIRED key features documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Only $FOUND_COUNT/$TOTAL_REQUIRED features documented"
    echo "  Missing functionality:"
    for feature in "${MISSING_FUNCTIONALITY[@]}"; do
        echo "    - $feature"
    done
    ((TESTS_FAILED++))
fi

# Test 4: Verify STORY-229 error categorization preserved
echo ""
echo "Test 4: STORY-229 error categorization preserved"
ERROR_KEYWORDS=(
    "ErrorEntry"
    "classification"
    "severity"
    "recoverable"
)
ERROR_FOUND=0

for keyword in "${ERROR_KEYWORDS[@]}"; do
    if echo "$ALL_CONTENT" | grep -qiE "$keyword"; then
        ((ERROR_FOUND++))
    fi
done

if [[ $ERROR_FOUND -ge 3 ]]; then
    echo "  PASS: Error categorization documentation found ($ERROR_FOUND/4 keywords)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Error categorization incomplete ($ERROR_FOUND/4 keywords)"
    echo "  Expected: ErrorEntry, classification, severity documented"
    ((TESTS_FAILED++))
fi

# Test 5: Verify STORY-226 N-gram analysis preserved
echo ""
echo "Test 5: STORY-226 N-gram analysis preserved"
NGRAM_KEYWORDS=(
    "bigram|bi.gram"
    "trigram|tri.gram"
    "sequence"
    "success.?rate|rate"
)
NGRAM_FOUND=0

for keyword in "${NGRAM_KEYWORDS[@]}"; do
    if echo "$ALL_CONTENT" | grep -qiE "$keyword"; then
        ((NGRAM_FOUND++))
    fi
done

if [[ $NGRAM_FOUND -ge 3 ]]; then
    echo "  PASS: N-gram analysis documentation found ($NGRAM_FOUND/4 keywords)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: N-gram analysis incomplete ($NGRAM_FOUND/4 keywords)"
    echo "  Expected: bigram, trigram, sequence analysis documented"
    ((TESTS_FAILED++))
fi

# Test 6: Verify pagination/streaming for large files
echo ""
echo "Test 6: Large file processing (pagination/streaming) preserved"
LARGE_FILE_KEYWORDS=(
    "pagination|paginate"
    "streaming|stream"
    "chunk"
    "86.*MB|large.?file"
)
LARGE_FOUND=0

for keyword in "${LARGE_FILE_KEYWORDS[@]}"; do
    if echo "$ALL_CONTENT" | grep -qiE "$keyword"; then
        ((LARGE_FOUND++))
    fi
done

if [[ $LARGE_FOUND -ge 2 ]]; then
    echo "  PASS: Large file processing documented ($LARGE_FOUND/4 keywords)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Large file processing incomplete ($LARGE_FOUND/4 keywords)"
    echo "  Expected: pagination, streaming, chunking documented"
    ((TESTS_FAILED++))
fi

# Test 7: Verify integration story references preserved
echo ""
echo "Test 7: Integration story references preserved"
STORY_FOUND=0
MISSING_STORIES=()

for story in "${STORY_REFERENCES[@]}"; do
    if echo "$ALL_CONTENT" | grep -qE "$story"; then
        ((STORY_FOUND++))
    else
        MISSING_STORIES+=("$story")
    fi
done

if [[ $STORY_FOUND -ge 5 ]]; then
    echo "  PASS: Integration story references found ($STORY_FOUND/7)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Missing integration story references"
    echo "  Stories not referenced:"
    for story in "${MISSING_STORIES[@]}"; do
        echo "    - $story"
    done
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "=============================================="
echo "  AC#4 TEST SUMMARY"
echo "=============================================="
echo "  Tests passed: $TESTS_PASSED"
echo "  Tests failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "  STATUS: PASSED - All AC#4 requirements met (no regression)"
    exit 0
else
    echo "  STATUS: FAILED - $TESTS_FAILED requirement(s) not met"
    exit 1
fi
