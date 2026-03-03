#!/bin/bash
# STORY-334 AC#1: Core File Size Compliance
# Verifies: Core file <= 300 lines with 9 required sections

set -e

CORE_FILE="src/claude/agents/ac-compliance-verifier.md"
MAX_LINES=300

echo "=== AC#1: Core File Size Compliance ==="

# Test 1: File exists
if [[ ! -f "$CORE_FILE" ]]; then
    echo "FAIL: Core file does not exist: $CORE_FILE"
    exit 1
fi
echo "PASS: Core file exists"

# Test 2: Line count <= 300
LINE_COUNT=$(wc -l < "$CORE_FILE")
if [[ $LINE_COUNT -gt $MAX_LINES ]]; then
    echo "FAIL: Core file has $LINE_COUNT lines (max: $MAX_LINES)"
    exit 1
fi
echo "PASS: Line count is $LINE_COUNT (<= $MAX_LINES)"

# Test 3: Required sections present (9 sections)
REQUIRED_SECTIONS=(
    "^---$"
    "## Purpose"
    "## When Invoked"
    "## Fresh-Context Technique"
    "## Core Verification Workflow"
    "## Success Criteria"
    "## Error Handling"
    "## Reference Loading"
    "## Observation Capture"
)

MISSING=0
for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -qE "$section" "$CORE_FILE"; then
        echo "FAIL: Missing section: $section"
        MISSING=$((MISSING + 1))
    fi
done

if [[ $MISSING -gt 0 ]]; then
    echo "FAIL: $MISSING required sections missing"
    exit 1
fi
echo "PASS: All 9 required sections present"

echo "=== AC#1 PASSED ==="
