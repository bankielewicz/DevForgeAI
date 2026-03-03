#!/bin/bash
# STORY-334 AC#5: Observation Capture Section (EPIC-052 Compliance)
# Verifies: Observation Capture section with 7 categories

set -e

CORE_FILE="src/claude/agents/ac-compliance-verifier.md"

echo "=== AC#5: Observation Capture Section ==="

# Test 1: Observation Capture section exists
if ! grep -q "## Observation Capture" "$CORE_FILE"; then
    echo "FAIL: Observation Capture section not found"
    exit 1
fi
echo "PASS: Observation Capture section exists"

# Test 2: All 7 categories present
CATEGORIES=(
    "friction"
    "success"
    "pattern"
    "gap"
    "idea"
    "bug"
    "warning"
)

MISSING=0
for cat in "${CATEGORIES[@]}"; do
    if ! grep -q "$cat" "$CORE_FILE"; then
        echo "FAIL: Missing category: $cat"
        MISSING=$((MISSING + 1))
    fi
done

if [[ $MISSING -gt 0 ]]; then
    echo "FAIL: $MISSING categories missing"
    exit 1
fi
echo "PASS: All 7 categories present"

# Test 3: Severity levels present
SEVERITIES=("low" "medium" "high")
for sev in "${SEVERITIES[@]}"; do
    if ! grep -q "$sev" "$CORE_FILE"; then
        echo "FAIL: Missing severity level: $sev"
        exit 1
    fi
done
echo "PASS: All severity levels present"

# Test 4: Write() instruction for observations
if ! grep -qE "Write\(" "$CORE_FILE"; then
    echo "FAIL: No Write() instruction for observation persistence"
    exit 1
fi
echo "PASS: Write() instruction present"

echo "=== AC#5 PASSED ==="
