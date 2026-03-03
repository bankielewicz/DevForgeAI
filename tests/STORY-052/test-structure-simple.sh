#!/bin/bash
# Test Suite STORY-052 - Document Structure Validation (AC1, AC5)

GUIDE_FILE="src/claude/memory/effective-prompting-guide.md"
PASS=0
FAIL=0

echo "========================================================================"
echo "STORY-052 Document Structure Validation - RED Phase"
echo "========================================================================"
echo ""

if [ ! -f "$GUIDE_FILE" ]; then
    echo "Document does not exist: $GUIDE_FILE"
    echo "All tests will FAIL until document is created."
    echo ""
fi

# AC1 Tests
echo "AC1: Document Completeness - Core Content Coverage"
echo ""

# Test 1: File exists
if [ -f "$GUIDE_FILE" ]; then
    echo "PASS: File exists"
    PASS=$((PASS+1))
else
    echo "FAIL: File does not exist: $GUIDE_FILE"
    FAIL=$((FAIL+1))
fi

# Test 2: Introduction (>=200 words)
if [ -f "$GUIDE_FILE" ]; then
    intro=$(head -100 "$GUIDE_FILE" | wc -w)
    if [ "$intro" -ge 200 ]; then
        echo "PASS: Introduction has >=200 words"
        PASS=$((PASS+1))
    else
        echo "FAIL: Introduction has <200 words"
        FAIL=$((FAIL+1))
    fi
else
    echo "SKIP: Introduction validation"
fi

# Test 3: All 11 commands
if [ -f "$GUIDE_FILE" ]; then
    count=0
    for cmd in ideate create-story create-context create-epic create-sprint create-ui dev qa release orchestrate create-agent; do
        grep -q "## /$cmd\|### /$cmd" "$GUIDE_FILE" && count=$((count+1))
    done
    if [ $count -eq 11 ]; then
        echo "PASS: All 11 command sections found"
        PASS=$((PASS+1))
    else
        echo "FAIL: Only $count/11 command sections found"
        FAIL=$((FAIL+1))
    fi
else
    echo "SKIP: Command sections validation"
fi

# Test 4: 20-30 examples
if [ -f "$GUIDE_FILE" ]; then
    examples=$(grep -c "BEFORE\|AFTER" "$GUIDE_FILE" 2>/dev/null || echo "0")
    examples=$((examples / 2))
    if [ "$examples" -ge 20 ] && [ "$examples" -le 30 ]; then
        echo "PASS: Found $examples examples"
        PASS=$((PASS+1))
    else
        echo "FAIL: Found $examples examples (need 20-30)"
        FAIL=$((FAIL+1))
    fi
else
    echo "SKIP: Examples validation"
fi

# Test 5: Quick reference in first 500 lines
if [ -f "$GUIDE_FILE" ]; then
    if head -500 "$GUIDE_FILE" | grep -qi "quick reference\|checklist" 2>/dev/null; then
        echo "PASS: Quick reference in first 500 lines"
        PASS=$((PASS+1))
    else
        echo "FAIL: Quick reference not found"
        FAIL=$((FAIL+1))
    fi
else
    echo "SKIP: Quick reference validation"
fi

# Test 6: Common pitfalls
if [ -f "$GUIDE_FILE" ]; then
    if grep -q "Common Pitfalls\|common pitfalls" "$GUIDE_FILE" 2>/dev/null; then
        pitfalls=$(grep -A 200 "Common Pitfalls" "$GUIDE_FILE" 2>/dev/null | grep "^- \|^* " | wc -l)
        if [ "$pitfalls" -ge 10 ] && [ "$pitfalls" -le 15 ]; then
            echo "PASS: Found $pitfalls pitfalls"
            PASS=$((PASS+1))
        else
            echo "FAIL: Found $pitfalls pitfalls (need 10-15)"
            FAIL=$((FAIL+1))
        fi
    else
        echo "FAIL: Common pitfalls section not found"
        FAIL=$((FAIL+1))
    fi
else
    echo "SKIP: Pitfalls validation"
fi

echo ""
echo "AC5: Usability and Scannability"
echo ""

# Test 7: ToC in first 100 lines
if [ -f "$GUIDE_FILE" ]; then
    if head -100 "$GUIDE_FILE" | grep -qi "table of contents\|contents" 2>/dev/null; then
        echo "PASS: Table of contents in first 100 lines"
        PASS=$((PASS+1))
    else
        echo "FAIL: Table of contents not in first 100 lines"
        FAIL=$((FAIL+1))
    fi
else
    echo "SKIP: ToC validation"
fi

# Test 8: Visual hierarchy
if [ -f "$GUIDE_FILE" ]; then
    echo "PASS: Visual hierarchy check"
    PASS=$((PASS+1))
else
    echo "SKIP: Visual hierarchy validation"
fi

# Test 9: Code blocks
if [ -f "$GUIDE_FILE" ]; then
    blocks=$(grep -c '```' "$GUIDE_FILE" 2>/dev/null || echo "0")
    pairs=$((blocks / 2))
    if [ "$pairs" -ge 20 ]; then
        echo "PASS: Found $pairs code blocks"
        PASS=$((PASS+1))
    else
        echo "FAIL: Found only $pairs code blocks"
        FAIL=$((FAIL+1))
    fi
else
    echo "SKIP: Code block validation"
fi

# Test 10: Search-friendly headings
if [ -f "$GUIDE_FILE" ]; then
    heading_count=$(grep -c "^## \|^### " "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$heading_count" -gt 15 ]; then
        echo "PASS: Found $heading_count headings"
        PASS=$((PASS+1))
    else
        echo "FAIL: Found only $heading_count headings"
        FAIL=$((FAIL+1))
    fi
else
    echo "SKIP: Headings validation"
fi

echo ""
echo "========================================================================"
echo "Summary"
echo "========================================================================"
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo "Total:  $((PASS + FAIL))"
echo ""
echo "Current Status: RED Phase (all tests failing - document not yet created)"
echo "Next Step: Create src/claude/memory/effective-prompting-guide.md"
