#!/bin/bash
# STORY-334 AC#4: Reference Loading Pattern Implementation
# Verifies: Core file contains Read() calls for each reference

set -e

CORE_FILE="src/claude/agents/ac-compliance-verifier.md"

echo "=== AC#4: Reference Loading Pattern ==="

# Test 1: Reference Loading section exists
if ! grep -q "## Reference Loading" "$CORE_FILE"; then
    echo "FAIL: Reference Loading section not found"
    exit 1
fi
echo "PASS: Reference Loading section exists"

# Test 2: Read() calls present for references
READ_CALLS=$(grep -c 'Read(file_path=' "$CORE_FILE" || echo "0")
if [[ $READ_CALLS -lt 4 ]]; then
    echo "FAIL: Found $READ_CALLS Read() calls (expected >= 4)"
    exit 1
fi
echo "PASS: Found $READ_CALLS Read() calls"

# Test 3: Each required reference has a Read() instruction
REQUIRED_REFS=(
    "xml-parsing-protocol"
    "verification-workflow"
    "scoring-methodology"
    "report-generation"
)

MISSING=0
for ref in "${REQUIRED_REFS[@]}"; do
    if ! grep -qE "Read.*$ref" "$CORE_FILE"; then
        echo "FAIL: No Read() call for: $ref"
        MISSING=$((MISSING + 1))
    fi
done

if [[ $MISSING -gt 0 ]]; then
    echo "FAIL: $MISSING references missing Read() calls"
    exit 1
fi
echo "PASS: All required references have Read() calls"

echo "=== AC#4 PASSED ==="
