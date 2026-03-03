#!/bin/bash
# STORY-319 AC#7: Observation Schema Compliance
# Tests that output schema includes all required fields
# Expected: FAIL (file does not exist yet - TDD Red phase)

set -e

SOURCE_FILE="src/claude/agents/observation-extractor.md"

echo "=== AC#7: Observation Schema Compliance Tests ==="

# Pre-check: File must exist
if [ ! -f "$SOURCE_FILE" ]; then
    echo "FAIL: Source file does not exist: $SOURCE_FILE"
    exit 1
fi

# Test 7.1: Observation ID format documented (obs-{phase}-{sequence})
echo -n "Test 7.1: Observation ID format (obs-{phase}-{sequence}) documented... "
if grep -q "obs-" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Documentation of observation ID format 'obs-{phase}-{sequence}'"
    exit 1
fi

# Test 7.2: Phase field documented
echo -n "Test 7.2: Phase field documented in output schema... "
if grep -q "phase" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: 'phase' field documented in output schema"
    exit 1
fi

# Test 7.3: Category field documented
echo -n "Test 7.3: Category field documented in output schema... "
if grep -q "category" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: 'category' field documented in output schema"
    exit 1
fi

# Test 7.4: All 7 category values documented
echo -n "Test 7.4: All 7 category values documented... "
CATEGORIES_FOUND=0
for cat in "friction" "success" "pattern" "gap" "idea" "bug" "warning"; do
    if grep -qi "$cat" "$SOURCE_FILE"; then
        CATEGORIES_FOUND=$((CATEGORIES_FOUND + 1))
    fi
done
if [ $CATEGORIES_FOUND -ge 7 ]; then
    echo "PASS (found all 7 categories)"
else
    echo "FAIL"
    echo "  Expected: All 7 categories documented (friction, success, pattern, gap, idea, bug, warning)"
    echo "  Found: $CATEGORIES_FOUND categories"
    exit 1
fi

# Test 7.5: Note field documented
echo -n "Test 7.5: Note field documented in output schema... "
if grep -q "note" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: 'note' field documented in output schema"
    exit 1
fi

# Test 7.6: Severity field documented
echo -n "Test 7.6: Severity field documented in output schema... "
if grep -q "severity" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: 'severity' field documented in output schema"
    exit 1
fi

# Test 7.7: Severity values documented (low/medium/high)
echo -n "Test 7.7: Severity values (low/medium/high) documented... "
SEV_FOUND=0
for sev in "low" "medium" "high"; do
    if grep -qi "$sev" "$SOURCE_FILE"; then
        SEV_FOUND=$((SEV_FOUND + 1))
    fi
done
if [ $SEV_FOUND -ge 3 ]; then
    echo "PASS (found all 3 severity levels)"
else
    echo "FAIL"
    echo "  Expected: All 3 severity levels documented (low, medium, high)"
    echo "  Found: $SEV_FOUND severity levels"
    exit 1
fi

# Test 7.8: Files field documented (optional)
echo -n "Test 7.8: Files field documented (optional array)... "
if grep -q "files" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: 'files' field documented in output schema"
    exit 1
fi

echo ""
echo "=== AC#7: All tests passed ==="
exit 0
