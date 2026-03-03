#!/bin/bash
# Test: STORY-448 - Extract Command Error Handling and Simplify Phase 0
# Story: STORY-448
# Generated: 2026-02-18
# Mode: TDD Red Phase - all tests MUST FAIL until implementation is complete
#
# Tests validate structural requirements against src/ tree per CLAUDE.md

# === Test Configuration ===
PASSED=0
FAILED=0

SRC_IDEATE="src/claude/commands/ideate.md"
SRC_ERROR_HANDLING="src/claude/skills/discovering-requirements/references/command-error-handling.md"
SRC_BRAINSTORM_HANDOFF="src/claude/skills/discovering-requirements/references/brainstorm-handoff-workflow.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo ""
echo "=== STORY-448: Extract Command Error Handling and Simplify Phase 0 ==="
echo "=== Testing against src/ tree ==="
echo ""

# ─────────────────────────────────────────────────────────────────────────────
# AC#1: Error Handling Extracted to Skill Reference
# ─────────────────────────────────────────────────────────────────────────────
echo "--- AC#1: command-error-handling.md exists with required content ---"

# Test: New reference file exists
[ -f "$SRC_ERROR_HANDLING" ]; run_test "command-error-handling.md file exists at expected path" $?

# Test: Contains error categorization taxonomy
grep -qi "error categor" "$SRC_ERROR_HANDLING" 2>/dev/null
run_test "command-error-handling.md contains error categorization taxonomy" $?

# Test: Contains pattern matching section
grep -qi "pattern match" "$SRC_ERROR_HANDLING" 2>/dev/null
run_test "command-error-handling.md contains pattern matching content" $?

# Test: Contains recovery actions section
grep -qi "recovery action" "$SRC_ERROR_HANDLING" 2>/dev/null
run_test "command-error-handling.md contains recovery actions content" $?

# Test: Contains session continuity logic
grep -qi "session continuity" "$SRC_ERROR_HANDLING" 2>/dev/null
run_test "command-error-handling.md contains session continuity logic" $?

# Test: File has substantive content (at least 20 lines)
LINE_COUNT=$(wc -l "$SRC_ERROR_HANDLING" 2>/dev/null | awk '{print $1}' || echo 0)
[ "${LINE_COUNT:-0}" -ge 20 ]; run_test "command-error-handling.md has at least 20 lines of content" $?

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# AC#2: Command Error Handling Reduced to Reference Pointer
# ─────────────────────────────────────────────────────────────────────────────
echo "--- AC#2: ideate.md error handling section <= 20 lines with reference pointer ---"

# Count lines in the error handling section (from "## ... Error" heading to next ## heading)
ERROR_SECTION_LINES=$(awk '
    /^## .*[Ee]rror/ { in_section=1; count=0; next }
    in_section && /^## / { exit }
    in_section { count++ }
    END { print count+0 }
' "$SRC_IDEATE" 2>/dev/null || echo 999)

echo "  (error section line count: $ERROR_SECTION_LINES)"
[ "$ERROR_SECTION_LINES" -le 20 ]; run_test "ideate.md error handling section is 20 lines or fewer" $?

# Test: Contains reference pointer to command-error-handling.md
grep -q "command-error-handling" "$SRC_IDEATE" 2>/dev/null
run_test "ideate.md contains reference pointer to command-error-handling.md" $?

# Test: No inline error type taxonomy headings (belong in reference file)
TAXONOMY_HEADINGS=$(grep -cE "^#+\s+(Error Type [0-9]|Type [0-9]+:)" "$SRC_IDEATE" 2>/dev/null | tr -d '[:space:]' || echo 0)
[ "${TAXONOMY_HEADINGS:-0}" -eq 0 ]; run_test "ideate.md has no inline error type taxonomy headings" $?

# Test: No extensive inline error pattern matching (fewer than 3 occurrences)
PATTERN_COUNT=$(grep -ciE "error.*pattern|pattern.*error" "$SRC_IDEATE" 2>/dev/null | tr -d '[:space:]' || echo 0)
[ "${PATTERN_COUNT:-0}" -lt 3 ]; run_test "ideate.md has minimal inline error pattern matching (< 3 occurrences)" $?

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# AC#3: Phase 0 Brainstorm Detection Simplified
# ─────────────────────────────────────────────────────────────────────────────
echo "--- AC#3: Phase 0 simplified - detect files, ask user, pass path only ---"

# Extract Phase 0 block to a temp file for targeted checks
PHASE0_CONTENT=$(awk '/^#+ Phase 0/,/^#+ Phase [1-9]/' "$SRC_IDEATE" 2>/dev/null || true)

# Test: Phase 0 has no YAML frontmatter parsing
if echo "$PHASE0_CONTENT" | grep -qiE "frontmatter|yaml.*pars|pars.*yaml" 2>/dev/null; then
    run_test "Phase 0 contains no YAML frontmatter parsing" 1
else
    run_test "Phase 0 contains no YAML frontmatter parsing" 0
fi

# Test: Phase 0 has no field extraction
if echo "$PHASE0_CONTENT" | grep -qiE "extract.*field|field.*extract|\.session_type|\.project_name|\.project_description" 2>/dev/null; then
    run_test "Phase 0 contains no field extraction logic" 1
else
    run_test "Phase 0 contains no field extraction logic" 0
fi

# Test: Phase 0 has no context variable construction
if echo "$PHASE0_CONTENT" | grep -qE "CONTEXT_|context_var|SESSION_CONTEXT|brainstorm_context\s*=" 2>/dev/null; then
    run_test "Phase 0 contains no context variable construction" 1
else
    run_test "Phase 0 contains no context variable construction" 0
fi

# Test: Phase 0 still has brainstorm file detection
echo "$PHASE0_CONTENT" | grep -qi "brainstorm" 2>/dev/null
run_test "Phase 0 still contains brainstorm file detection" $?

# Test: Phase 0 passes file path to skill layer
echo "$PHASE0_CONTENT" | grep -qiE "file.path|path.*file|selected.*file|file.*select" 2>/dev/null
run_test "Phase 0 passes file path to skill layer" $?

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# AC#4: YAML Parsing Moved to Skill Reference (brainstorm-handoff-workflow.md)
# ─────────────────────────────────────────────────────────────────────────────
echo "--- AC#4: brainstorm-handoff-workflow.md handles YAML parsing and field extraction ---"

# Test: brainstorm-handoff-workflow.md contains YAML parsing
grep -qiE "yaml|frontmatter|pars" "$SRC_BRAINSTORM_HANDOFF" 2>/dev/null
run_test "brainstorm-handoff-workflow.md contains YAML parsing content" $?

# Test: brainstorm-handoff-workflow.md contains field extraction
grep -qiE "field.extract|extract.field|session_type|project_name|project_description" \
    "$SRC_BRAINSTORM_HANDOFF" 2>/dev/null
run_test "brainstorm-handoff-workflow.md contains field extraction logic" $?

# Test: brainstorm-handoff-workflow.md contains context variable construction
grep -qiE "context.variable|construct.*context|context.*construct|build.*context" \
    "$SRC_BRAINSTORM_HANDOFF" 2>/dev/null
run_test "brainstorm-handoff-workflow.md contains context variable construction" $?

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# AC#5: Command Line Count Reduced to <= 400 lines
# ─────────────────────────────────────────────────────────────────────────────
echo "--- AC#5: ideate.md total line count <= 400 lines ---"

TOTAL_LINES=$(wc -l < "$SRC_IDEATE" 2>/dev/null || echo 9999)
echo "  (current total line count: $TOTAL_LINES)"
[ "$TOTAL_LINES" -le 400 ]; run_test "ideate.md total line count is 400 lines or fewer" $?

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# AC#6: No Functional Regression
# ─────────────────────────────────────────────────────────────────────────────
echo "--- AC#6: No functional regression - all 3 modes, brainstorm detection, error recovery ---"

# Test: Brainstorm mode keyword still present in ideate.md
grep -qi "brainstorm" "$SRC_IDEATE" 2>/dev/null
run_test "Brainstorm mode keyword still present in ideate.md" $?

# Test: Fresh/new mode keyword still present in ideate.md
grep -qiE "fresh|new project|mode.*fresh|fresh.*mode|no brainstorm" "$SRC_IDEATE" 2>/dev/null
run_test "Fresh/new mode keyword still present in ideate.md" $?

# Test: Project/existing-project mode still present in ideate.md
grep -qiE "existing.project|project.mode|mode.*project" "$SRC_IDEATE" 2>/dev/null
run_test "Project/existing-project mode still referenced in ideate.md" $?

# Test: Error recovery reference preserved in ideate.md (not deleted)
grep -qiE "error.*recov|recov.*error|error.handling" "$SRC_IDEATE" 2>/dev/null
run_test "Error recovery reference preserved in ideate.md" $?

# Test: Extracted reference file contains recovery logic (not lost in extraction)
grep -qiE "recov" "$SRC_ERROR_HANDLING" 2>/dev/null
run_test "command-error-handling.md contains recovery logic (not deleted)" $?

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────
echo "=== Test Results ==="
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo "  Total:  $((PASSED + FAILED))"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo "ALL TESTS PASSED"
    exit 0
else
    echo "TESTS FAILED: $FAILED test(s) failed"
    echo "(Expected in TDD Red phase - implementation not yet complete)"
    exit 1
fi
