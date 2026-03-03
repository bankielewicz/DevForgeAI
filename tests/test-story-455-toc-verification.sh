#!/bin/bash
# Test: STORY-455 - Table of Contents for Large Reference Files
# Story: STORY-455
# Generated: 2026-02-19
# Phase: Red (all TOC-required tests should FAIL until TOCs are added)
#
# Run from project root:
#   bash tests/test-story-455-toc-verification.sh

set -uo pipefail

# === Configuration ===
BASE="src/claude/skills/discovering-requirements/references"
PASSED=0
FAILED=0

# === Helpers ===
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

# Check if file contains a TOC header. Returns 0=found, 1=not found.
check_has_toc() {
    local file="$1"
    local rc=0
    grep -q "^## Table of Contents" "$file" || rc=$?
    return $rc
}

# Check for duplicate TOC headers. Returns 0=duplicate found, 1=no duplicate.
check_duplicate_toc() {
    local file="$1"
    local count rc=0
    count=$(grep -c "^## Table of Contents" "$file" 2>/dev/null) || true
    if [ "${count:-0}" -gt 1 ]; then
        return 0
    fi
    return 1
}

# Check that TOC appears within first 30 lines of file.
check_toc_within_30_lines() {
    local file="$1"
    local line_num rc=0
    line_num=$(grep -n "^## Table of Contents" "$file" 2>/dev/null | head -1 | cut -d: -f1) || true
    if [ -n "${line_num:-}" ] && [ "$line_num" -le 30 ]; then
        return 0
    fi
    return 1
}

# Check that at least one TOC link matches "- [Text](#anchor)" format.
check_toc_format() {
    local file="$1"
    local rc=0
    awk '/^## Table of Contents/{found=1; next} found && /^## /{exit} found{print}' "$file" \
        | grep -q "^\- \[.\+\](#.\+)" || rc=$?
    return $rc
}

# Check that all TOC anchor links resolve to headings in the file.
# Returns 0=all resolve, 1=unresolved anchor found.
check_toc_anchors_resolve() {
    local file="$1"
    local anchors anchor heading_text slug found_any=0 all_ok=0

    anchors=$(awk '/^## Table of Contents/{found=1; next} found && /^## /{exit} found{print}' "$file" \
        | grep -o '(#[^)]\+)' | tr -d '()#' 2>/dev/null) || true

    if [ -z "${anchors:-}" ]; then
        # No anchors means no TOC links — fail
        return 1
    fi

    while IFS= read -r anchor; do
        [ -z "$anchor" ] && continue
        found_any=1
        local found_match=1
        while IFS= read -r heading_line; do
            heading_text=$(echo "$heading_line" | sed 's/^#\+ //')
            slug=$(echo "$heading_text" \
                | tr '[:upper:]' '[:lower:]' \
                | tr ' ' '-' \
                | sed 's/[^a-z0-9-]//g' \
                | sed 's/--*/-/g' \
                | sed 's/^-//;s/-$//')
            if [ "$slug" = "$anchor" ]; then
                found_match=0
                break
            fi
        done < <(grep "^#" "$file")
        if [ "$found_match" -ne 0 ]; then
            all_ok=1
        fi
    done <<< "$anchors"

    [ "$found_any" -eq 0 ] && return 1
    return $all_ok
}

# Get line count for a file
get_line_count() {
    wc -l < "$1"
}

# ============================================================
# AC#1 Tests — Batch 1 (8 largest files needing TOC)
# All should FAIL in Red phase (no TOC yet)
# ============================================================
echo ""
echo "=== AC#1: Batch 1 Files — TOC Required ==="

BATCH1_FILES=(
    "validation-checklists.md"
    "user-interaction-patterns.md"
    "brainstorm-handoff-workflow.md"
    "resume-logic.md"
    "requirements-elicitation-workflow.md"
    "output-templates.md"
    "discovery-workflow.md"
    "examples.md"
)

for f in "${BATCH1_FILES[@]}"; do
    filepath="${BASE}/${f}"
    rc=0; check_has_toc "$filepath" || rc=$?
    run_test "AC#1: ${f} has ## Table of Contents" "$rc"
done

# ============================================================
# AC#2 Tests — Batch 2 (13 remaining files needing TOC)
# All should FAIL in Red phase (no TOC yet)
# ============================================================
echo ""
echo "=== AC#2: Batch 2 Files — TOC Required ==="

BATCH2_FILES=(
    "self-validation-workflow.md"
    "artifact-generation.md"
    "error-type-4-validation-failures.md"
    "user-input-integration-guide.md"
    "error-type-5-constraint-conflicts.md"
    "command-error-handling.md"
    "error-type-3-complexity-errors.md"
    "error-type-6-directory-issues.md"
    "error-type-2-artifact-failures.md"
    "error-type-1-incomplete-answers.md"
    "checkpoint-protocol.md"
    "checkpoint-resume.md"
    "error-handling-index.md"
)

for f in "${BATCH2_FILES[@]}"; do
    filepath="${BASE}/${f}"
    rc=0; check_has_toc "$filepath" || rc=$?
    run_test "AC#2: ${f} has ## Table of Contents" "$rc"
done

# ============================================================
# AC#3 Tests — Quality and format checks
# Most should FAIL in Red phase (TOC not present yet)
# ============================================================
echo ""
echo "=== AC#3: TOC Quality and Format Checks ==="

ALL_TOC_REQUIRED=(
    "validation-checklists.md"
    "user-interaction-patterns.md"
    "brainstorm-handoff-workflow.md"
    "resume-logic.md"
    "requirements-elicitation-workflow.md"
    "output-templates.md"
    "discovery-workflow.md"
    "examples.md"
    "self-validation-workflow.md"
    "artifact-generation.md"
    "error-type-4-validation-failures.md"
    "user-input-integration-guide.md"
    "error-type-5-constraint-conflicts.md"
    "command-error-handling.md"
    "error-type-3-complexity-errors.md"
    "error-type-6-directory-issues.md"
    "error-type-2-artifact-failures.md"
    "error-type-1-incomplete-answers.md"
    "checkpoint-protocol.md"
    "checkpoint-resume.md"
    "error-handling-index.md"
)

ALL_MD_FILES=(
    "validation-checklists.md"
    "user-interaction-patterns.md"
    "brainstorm-handoff-workflow.md"
    "resume-logic.md"
    "requirements-elicitation-workflow.md"
    "output-templates.md"
    "discovery-workflow.md"
    "examples.md"
    "self-validation-workflow.md"
    "artifact-generation.md"
    "error-type-4-validation-failures.md"
    "user-input-integration-guide.md"
    "error-type-5-constraint-conflicts.md"
    "command-error-handling.md"
    "error-type-3-complexity-errors.md"
    "error-type-6-directory-issues.md"
    "error-type-2-artifact-failures.md"
    "error-type-1-incomplete-answers.md"
    "checkpoint-protocol.md"
    "checkpoint-resume.md"
    "error-handling-index.md"
    "user-input-guidance.md"
    "completion-handoff.md"
    "brainstorm-data-mapping.md"
    "domain-specific-patterns.md"
    "requirements-elicitation-guide.md"
)

# AC#3.1: No duplicate ## Table of Contents in any file (all 26 .md files)
echo ""
echo "  --- AC#3.1: No duplicate TOC headers ---"
for f in "${ALL_MD_FILES[@]}"; do
    filepath="${BASE}/${f}"
    if check_duplicate_toc "$filepath"; then
        run_test "AC#3.1: ${f} has no duplicate TOC headers" 1
    else
        run_test "AC#3.1: ${f} has no duplicate TOC headers" 0
    fi
done

# AC#3.2: TOC uses consistent format "- [Heading Text](#anchor-link)"
echo ""
echo "  --- AC#3.2: TOC uses consistent link format ---"
for f in "${ALL_TOC_REQUIRED[@]}"; do
    filepath="${BASE}/${f}"
    rc=0; check_toc_format "$filepath" || rc=$?
    run_test "AC#3.2: ${f} TOC uses - [Text](#anchor) format" "$rc"
done

# AC#3.3: TOC appears within first 30 lines
echo ""
echo "  --- AC#3.3: TOC appears within first 30 lines ---"
for f in "${ALL_TOC_REQUIRED[@]}"; do
    filepath="${BASE}/${f}"
    rc=0; check_toc_within_30_lines "$filepath" || rc=$?
    run_test "AC#3.3: ${f} TOC within first 30 lines" "$rc"
done

# AC#3.4: Anchor links in TOC resolve to actual headings
echo ""
echo "  --- AC#3.4: All TOC anchor links resolve to headings ---"
for f in "${ALL_TOC_REQUIRED[@]}"; do
    filepath="${BASE}/${f}"
    rc=0; check_toc_anchors_resolve "$filepath" || rc=$?
    run_test "AC#3.4: ${f} TOC anchors resolve to headings" "$rc"
done

# AC#3.5: All .md files >100 lines have TOC (21 new + 5 existing)
echo ""
echo "  --- AC#3.5: All .md files >100 lines have TOC ---"
for f in "${ALL_MD_FILES[@]}"; do
    filepath="${BASE}/${f}"
    line_count=$(get_line_count "$filepath")
    if [ "$line_count" -gt 100 ]; then
        rc=0; check_has_toc "$filepath" || rc=$?
        run_test "AC#3.5: ${f} (${line_count} lines) has TOC" "$rc"
    else
        run_test "AC#3.5: ${f} (${line_count} lines) skipped — under 100 lines" 0
    fi
done

# ============================================================
# Negative Tests — Pre-existing TOC files (should PASS now)
# ============================================================
echo ""
echo "=== Negative Tests: Pre-existing TOC files (should PASS now) ==="

EXISTING_TOC_FILES=(
    "user-input-guidance.md"
    "completion-handoff.md"
    "brainstorm-data-mapping.md"
    "domain-specific-patterns.md"
    "requirements-elicitation-guide.md"
)

for f in "${EXISTING_TOC_FILES[@]}"; do
    filepath="${BASE}/${f}"
    rc=0; check_has_toc "$filepath" || rc=$?
    run_test "Negative: ${f} already has TOC (pre-existing)" "$rc"
done

# ============================================================
# Negative Test — YAML file must NOT have TOC
# ============================================================
echo ""
echo "=== Negative Test: checkpoint-schema.yaml must NOT have TOC ==="

YAML_FILE="${BASE}/checkpoint-schema.yaml"
yaml_has_toc=0
grep -q "## Table of Contents" "$YAML_FILE" 2>/dev/null && yaml_has_toc=1 || true
if [ "$yaml_has_toc" -eq 1 ]; then
    run_test "Negative: checkpoint-schema.yaml has no TOC (YAML file)" 1
else
    run_test "Negative: checkpoint-schema.yaml has no TOC (YAML file)" 0
fi

# ============================================================
# Summary
# ============================================================
echo ""
echo "======================================"
echo "  STORY-455 TOC Verification Results"
echo "======================================"
echo "  Passed: ${PASSED}"
echo "  Failed: ${FAILED}"
TOTAL=$((PASSED + FAILED))
echo "  Total:  ${TOTAL}"
echo "======================================"

if [ "$FAILED" -eq 0 ]; then
    echo "  STATUS: ALL TESTS PASSED"
    exit 0
else
    echo "  STATUS: ${FAILED} TEST(S) FAILED"
    exit 1
fi
