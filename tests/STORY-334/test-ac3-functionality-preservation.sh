#!/bin/bash
# STORY-334 AC#3: Functionality Preservation (No Regression)
# Verifies: All original functionality preserved across core + references

set -e

CORE_FILE="src/claude/agents/ac-compliance-verifier.md"
REF_DIR="src/claude/agents/ac-compliance-verifier/references"

echo "=== AC#3: Functionality Preservation ==="

# Test 1: Fresh-context technique documented (core file)
if ! grep -q "fresh-context" "$CORE_FILE"; then
    echo "FAIL: Fresh-context technique not documented in core"
    exit 1
fi
echo "PASS: Fresh-context technique documented"

# Test 2: XML parsing protocol documented
if [[ ! -f "$REF_DIR/xml-parsing-protocol.md" ]]; then
    echo "FAIL: XML parsing protocol reference missing"
    exit 1
fi
if ! grep -qE "(given|when|then)" "$REF_DIR/xml-parsing-protocol.md"; then
    echo "FAIL: XML parsing protocol missing given/when/then extraction"
    exit 1
fi
echo "PASS: XML parsing protocol documented"

# Test 3: Verification workflow documented
if [[ ! -f "$REF_DIR/verification-workflow.md" ]]; then
    echo "FAIL: Verification workflow reference missing"
    exit 1
fi
if ! grep -qE "(Phase 4\.5|Phase 5\.5)" "$REF_DIR/verification-workflow.md"; then
    echo "FAIL: Verification workflow missing Phase 4.5/5.5 integration"
    exit 1
fi
echo "PASS: Verification workflow documented"

# Test 4: Scoring methodology documented
if [[ ! -f "$REF_DIR/scoring-methodology.md" ]]; then
    echo "FAIL: Scoring methodology reference missing"
    exit 1
fi
if ! grep -qE "(confidence|evidence)" "$REF_DIR/scoring-methodology.md"; then
    echo "FAIL: Scoring methodology missing confidence/evidence evaluation"
    exit 1
fi
echo "PASS: Scoring methodology documented"

# Test 5: Report generation documented
if [[ ! -f "$REF_DIR/report-generation.md" ]]; then
    echo "FAIL: Report generation reference missing"
    exit 1
fi
if ! grep -qE "(JSON|json)" "$REF_DIR/report-generation.md"; then
    echo "FAIL: Report generation missing JSON format documentation"
    exit 1
fi
echo "PASS: Report generation documented"

echo "=== AC#3 PASSED ==="
