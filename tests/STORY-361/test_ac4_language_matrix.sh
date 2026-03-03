#!/usr/bin/env bash
# =============================================================================
# STORY-361 AC#4: Language Support Matrix with File Extension Mapping
# =============================================================================
# Validates that:
#   1. Reference file exists
#   2. Contains a markdown table with 5 required columns:
#      Language | File Extensions | Treelint Support Status | Fallback Strategy | Notes
#   3. 5 supported languages listed: Python, TypeScript, JavaScript, Rust, Markdown
#   4. 4+ unsupported languages listed: C#, Java, Go, Other
#   5. Total rows >= 9 (5 supported + 4 unsupported)
#   6. Table uses standard markdown format (pipe-delimited with header separator)
#
# TDD Phase: RED - Target file does not exist yet.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/references/treelint-search-patterns.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  PASS: $1"
}

fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  FAIL: $1"
}

echo "=============================================="
echo "  AC#4: Language Support Matrix"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "Reference file exists"
else
    fail "Reference file does not exist at src/claude/agents/references/treelint-search-patterns.md"
    echo ""
    echo "=============================================="
    echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains Language Support Matrix section heading
# -----------------------------------------------------------------------------
echo "--- Test 2: Language Support Matrix Section ---"
if grep -qiE '^#{1,3} .*Language Support Matrix' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'Language Support Matrix' section heading"
else
    fail "Missing 'Language Support Matrix' section heading"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Table has required columns
# Look for the header row containing all 5 column names
# Columns: Language | File Extensions | (Treelint) Support Status | Fallback Strategy | Notes
# -----------------------------------------------------------------------------
echo "--- Test 3: Required Table Columns ---"

if grep -qiE 'Language.*\|.*File Extension' "$TARGET_FILE" 2>/dev/null; then
    pass "Table header contains 'Language' and 'File Extensions' columns"
else
    fail "Missing 'Language' and/or 'File Extensions' column headers"
fi

if grep -qiE 'Support.*Status\|.*Fallback' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE 'Fallback.*\|.*Notes' "$TARGET_FILE" 2>/dev/null; then
    pass "Table header contains 'Support Status', 'Fallback Strategy', and/or 'Notes' columns"
else
    fail "Missing 'Support Status', 'Fallback Strategy', and/or 'Notes' column headers"
fi

# Check for markdown table separator row (|---|---|...)
if grep -qE '^\|[-: ]+\|[-: ]+\|' "$TARGET_FILE" 2>/dev/null; then
    pass "Table has markdown separator row (|---|---|...)"
else
    fail "Missing markdown table separator row"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: 5 supported languages present
# Python, TypeScript, JavaScript, Rust, Markdown
# -----------------------------------------------------------------------------
echo "--- Test 4: Supported Languages (5 required) ---"
supported_count=0

if grep -qE '\|.*Python.*\|' "$TARGET_FILE" 2>/dev/null; then
    pass "Python listed in language matrix"
    supported_count=$((supported_count + 1))
else
    fail "Python not found in language matrix"
fi

if grep -qE '\|.*TypeScript.*\|' "$TARGET_FILE" 2>/dev/null; then
    pass "TypeScript listed in language matrix"
    supported_count=$((supported_count + 1))
else
    fail "TypeScript not found in language matrix"
fi

if grep -qE '\|.*JavaScript.*\|' "$TARGET_FILE" 2>/dev/null; then
    pass "JavaScript listed in language matrix"
    supported_count=$((supported_count + 1))
else
    fail "JavaScript not found in language matrix"
fi

if grep -qE '\|.*Rust.*\|' "$TARGET_FILE" 2>/dev/null; then
    pass "Rust listed in language matrix"
    supported_count=$((supported_count + 1))
else
    fail "Rust not found in language matrix"
fi

if grep -qE '\|.*Markdown.*\|' "$TARGET_FILE" 2>/dev/null; then
    pass "Markdown listed in language matrix"
    supported_count=$((supported_count + 1))
else
    fail "Markdown not found in language matrix"
fi

echo "  Supported languages found: ${supported_count}/5"
echo ""

# -----------------------------------------------------------------------------
# Test 5: 4+ unsupported languages present
# C#, Java, Go, Other (minimum)
# -----------------------------------------------------------------------------
echo "--- Test 5: Unsupported Languages (4+ required) ---"
unsupported_count=0

if grep -qE '\|.*C#.*\|' "$TARGET_FILE" 2>/dev/null; then
    pass "C# listed in language matrix"
    unsupported_count=$((unsupported_count + 1))
else
    fail "C# not found in language matrix"
fi

if grep -qE '\|.*Java\b.*\|' "$TARGET_FILE" 2>/dev/null; then
    pass "Java listed in language matrix"
    unsupported_count=$((unsupported_count + 1))
else
    fail "Java not found in language matrix"
fi

if grep -qE '\|.*Go\b.*\|' "$TARGET_FILE" 2>/dev/null; then
    pass "Go listed in language matrix"
    unsupported_count=$((unsupported_count + 1))
else
    fail "Go not found in language matrix"
fi

if grep -qiE '\|.*Other.*\|' "$TARGET_FILE" 2>/dev/null; then
    pass "Other/catch-all listed in language matrix"
    unsupported_count=$((unsupported_count + 1))
else
    fail "Other/catch-all not found in language matrix"
fi

echo "  Unsupported languages found: ${unsupported_count}/4"
echo ""

# -----------------------------------------------------------------------------
# Test 6: Total table rows >= 9
# Count pipe-delimited rows that look like table data (exclude header and separator)
# Table rows have format: | value | value | ...
# Exclude header row (contains "Language") and separator row (contains ---)
# -----------------------------------------------------------------------------
echo "--- Test 6: Minimum 9 Table Rows ---"
# Count all pipe-delimited rows, subtract header and separator
total_table_rows=$(grep -cE '^\|[^-]' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$total_table_rows" ]]; then total_table_rows=0; fi

# Subtract 1 for the header row to get data rows
data_rows=$((total_table_rows - 1))
if [[ "$data_rows" -lt 0 ]]; then data_rows=0; fi

if [[ "$data_rows" -ge 9 ]]; then
    pass "Language matrix has ${data_rows} data rows (>= 9 required)"
else
    fail "Language matrix has ${data_rows} data rows (>= 9 required)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: File extension mappings present for supported languages
# Verify .py, .ts, .tsx, .js, .jsx, .rs, .md extensions appear
# -----------------------------------------------------------------------------
echo "--- Test 7: File Extension Mappings ---"
extensions_found=0
for ext in '.py' '.ts' '.js' '.rs' '.md'; do
    if grep -q "$ext" "$TARGET_FILE" 2>/dev/null; then
        extensions_found=$((extensions_found + 1))
    fi
done

if [[ "$extensions_found" -ge 5 ]]; then
    pass "All 5 primary file extensions documented (.py, .ts, .js, .rs, .md)"
else
    fail "Only ${extensions_found}/5 primary file extensions documented"
fi

# Check for secondary extensions (.tsx, .jsx)
secondary_found=0
for ext in '.tsx' '.jsx'; do
    if grep -q "$ext" "$TARGET_FILE" 2>/dev/null; then
        secondary_found=$((secondary_found + 1))
    fi
done

if [[ "$secondary_found" -ge 2 ]]; then
    pass "Secondary extensions documented (.tsx, .jsx)"
else
    fail "Missing secondary extensions (found ${secondary_found}/2: .tsx, .jsx)"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
