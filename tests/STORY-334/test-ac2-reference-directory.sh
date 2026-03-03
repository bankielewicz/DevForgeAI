#!/bin/bash
# STORY-334 AC#2: Reference Directory Structure
# Verifies: references/ directory with 4-6 files

set -e

REF_DIR="src/claude/agents/ac-compliance-verifier/references"
MIN_FILES=4
MAX_FILES=6

echo "=== AC#2: Reference Directory Structure ==="

# Test 1: Directory exists
if [[ ! -d "$REF_DIR" ]]; then
    echo "FAIL: Reference directory does not exist: $REF_DIR"
    exit 1
fi
echo "PASS: Reference directory exists"

# Test 2: File count between 4-6
FILE_COUNT=$(ls -1 "$REF_DIR"/*.md 2>/dev/null | wc -l)
if [[ $FILE_COUNT -lt $MIN_FILES || $FILE_COUNT -gt $MAX_FILES ]]; then
    echo "FAIL: Reference directory has $FILE_COUNT files (expected: $MIN_FILES-$MAX_FILES)"
    exit 1
fi
echo "PASS: Reference file count is $FILE_COUNT ($MIN_FILES-$MAX_FILES)"

# Test 3: Required reference files exist
REQUIRED_REFS=(
    "xml-parsing-protocol.md"
    "verification-workflow.md"
    "scoring-methodology.md"
    "report-generation.md"
)

MISSING=0
for ref in "${REQUIRED_REFS[@]}"; do
    if [[ ! -f "$REF_DIR/$ref" ]]; then
        echo "FAIL: Missing required reference: $ref"
        MISSING=$((MISSING + 1))
    fi
done

if [[ $MISSING -gt 0 ]]; then
    echo "FAIL: $MISSING required reference files missing"
    exit 1
fi
echo "PASS: All required reference files present"

# Test 4: Lowercase-hyphen naming convention
BAD_NAMES=$(ls -1 "$REF_DIR" | grep -vE '^[a-z][a-z0-9-]*\.md$' | wc -l)
if [[ $BAD_NAMES -gt 0 ]]; then
    echo "FAIL: $BAD_NAMES files do not follow lowercase-hyphen naming"
    exit 1
fi
echo "PASS: All files follow naming convention"

echo "=== AC#2 PASSED ==="
