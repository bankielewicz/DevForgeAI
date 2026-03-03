#!/bin/bash
# STORY-334 AC#6: Operational Copy Synchronization
# Verifies: src/ and .claude/ copies are identical

set -e

SRC_CORE="src/claude/agents/ac-compliance-verifier.md"
OPS_CORE=".claude/agents/ac-compliance-verifier.md"
SRC_REF="src/claude/agents/ac-compliance-verifier/references"
OPS_REF=".claude/agents/ac-compliance-verifier/references"

echo "=== AC#6: Operational Copy Synchronization ==="

# Test 1: Source core file exists
if [[ ! -f "$SRC_CORE" ]]; then
    echo "FAIL: Source core file missing: $SRC_CORE"
    exit 1
fi
echo "PASS: Source core file exists"

# Test 2: Operational core file exists
if [[ ! -f "$OPS_CORE" ]]; then
    echo "FAIL: Operational core file missing: $OPS_CORE"
    exit 1
fi
echo "PASS: Operational core file exists"

# Test 3: Core files are identical
if ! diff -q "$SRC_CORE" "$OPS_CORE" > /dev/null 2>&1; then
    echo "FAIL: Core files differ between src/ and .claude/"
    exit 1
fi
echo "PASS: Core files are identical"

# Test 4: Source reference directory exists
if [[ ! -d "$SRC_REF" ]]; then
    echo "FAIL: Source reference directory missing: $SRC_REF"
    exit 1
fi
echo "PASS: Source reference directory exists"

# Test 5: Operational reference directory exists
if [[ ! -d "$OPS_REF" ]]; then
    echo "FAIL: Operational reference directory missing: $OPS_REF"
    exit 1
fi
echo "PASS: Operational reference directory exists"

# Test 6: Reference directories are identical
if ! diff -rq "$SRC_REF" "$OPS_REF" > /dev/null 2>&1; then
    echo "FAIL: Reference directories differ between src/ and .claude/"
    exit 1
fi
echo "PASS: Reference directories are identical"

echo "=== AC#6 PASSED ==="
