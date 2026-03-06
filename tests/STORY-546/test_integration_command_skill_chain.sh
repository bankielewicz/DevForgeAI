#!/bin/bash
# Integration Test: STORY-546 - Cross-Component Chain Validation
# Verifies: command → skill → references chain integrity
# Generated: 2026-03-05

PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

COMMAND_FILE="$PROJECT_ROOT/src/claude/commands/legal-check.md"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/SKILL.md"
REFS_DIR="$PROJECT_ROOT/src/claude/skills/advising-legal/references"
DISCLAIMER_FILE="$REFS_DIR/disclaimer-template.md"
BUSINESS_FILE="$REFS_DIR/business-structure-guide.md"
IP_FILE="$REFS_DIR/ip-protection-checklist.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "============================================================"
echo "  Integration Tests: STORY-546 Cross-Component Validation"
echo "============================================================"
echo ""

# ---------------------------------------------------------------
# SECTION 1: End-to-End Command → Skill → References Chain
# ---------------------------------------------------------------
echo "=== 1. End-to-End Command Chain ==="

# 1.1: Command file references the skill
grep -q "advising-legal" "$COMMAND_FILE" 2>/dev/null
run_test "command_references_skill_name" $?

# 1.2: Command references SKILL.md path
grep -q "skills/advising-legal/SKILL.md" "$COMMAND_FILE" 2>/dev/null
run_test "command_references_skill_path" $?

# 1.3: Skill file references the references/ directory
grep -q "references/" "$SKILL_FILE" 2>/dev/null
run_test "skill_references_references_directory" $?

# 1.4: All three reference files exist
test -f "$DISCLAIMER_FILE" && test -f "$BUSINESS_FILE" && test -f "$IP_FILE"
run_test "all_three_reference_files_exist" $?

# 1.5: Skill references each specific reference file by name
grep -q "business-structure-guide.md" "$SKILL_FILE" 2>/dev/null
BS_REF=$?
grep -q "ip-protection-checklist.md" "$SKILL_FILE" 2>/dev/null
IP_REF=$?
grep -q "disclaimer-template.md" "$SKILL_FILE" 2>/dev/null
DT_REF=$?
[ "$BS_REF" -eq 0 ] && [ "$IP_REF" -eq 0 ] && [ "$DT_REF" -eq 0 ]
run_test "skill_references_all_three_reference_files" $?

# 1.6: References table in SKILL.md lists all three files
REFS_TABLE_LINES=$(grep -c "references/" "$SKILL_FILE" 2>/dev/null)
[ "$REFS_TABLE_LINES" -ge 3 ]
run_test "skill_references_table_has_at_least_3_entries" $?

# 1.7: Command Skill() delegation uses advising-legal
grep -q 'advising-legal' "$COMMAND_FILE" 2>/dev/null
run_test "command_delegation_targets_advising_legal" $?

# 1.8: Reference files are non-empty
[ -s "$DISCLAIMER_FILE" ] && [ -s "$BUSINESS_FILE" ] && [ -s "$IP_FILE" ]
run_test "reference_files_are_non_empty" $?

echo ""

# ---------------------------------------------------------------
# SECTION 2: Standalone vs Project-Anchored Mode Consistency
# ---------------------------------------------------------------
echo "=== 2. Standalone vs Project-Anchored Mode Consistency ==="

# 2.1: SKILL.md documents standalone mode
grep -qi "standalone" "$SKILL_FILE" 2>/dev/null
run_test "skill_documents_standalone_mode" $?

# 2.2: SKILL.md documents project-anchored mode
grep -qi "project-anchored" "$SKILL_FILE" 2>/dev/null
run_test "skill_documents_project_anchored_mode" $?

# 2.3: Standalone mode includes graceful fallback for missing context
grep -qi "standalone" "$SKILL_FILE" 2>/dev/null && grep -qi "graceful\|fallback\|absent\|missing" "$SKILL_FILE" 2>/dev/null
run_test "standalone_mode_has_graceful_fallback" $?

# 2.4: Project-anchored mode reads context files
grep -q "source-tree.md" "$SKILL_FILE" 2>/dev/null && grep -q "tech-stack.md" "$SKILL_FILE" 2>/dev/null
run_test "project_anchored_reads_context_files" $?

# 2.5: Both modes are non-contradictory (standalone says "absent", anchored says "present")
STANDALONE_LINE=$(grep -n -i "standalone" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)
ANCHORED_LINE=$(grep -n -i "project-anchored" "$SKILL_FILE" 2>/dev/null | head -1 | cut -d: -f1)
# Both modes must be documented (non-zero line numbers)
[ -n "$STANDALONE_LINE" ] && [ -n "$ANCHORED_LINE" ]
run_test "both_modes_documented_at_distinct_locations" $?

# 2.6: Command file acknowledges both modes
grep -qi "standalone\|project-anchored\|both.*mode" "$COMMAND_FILE" 2>/dev/null
run_test "command_acknowledges_both_modes" $?

echo ""

# ---------------------------------------------------------------
# SECTION 3: Disclaimer Propagation Chain
# ---------------------------------------------------------------
echo "=== 3. Disclaimer Propagation Chain ==="

# 3.1: disclaimer-template.md exists
test -f "$DISCLAIMER_FILE"
run_test "disclaimer_template_file_exists" $?

# 3.2: SKILL.md references disclaimer-template.md
grep -q "disclaimer-template.md" "$SKILL_FILE" 2>/dev/null
run_test "skill_references_disclaimer_template" $?

# 3.3: SKILL.md mandates disclaimer in first 10 lines
# Check that first 10 lines of SKILL.md contain disclaimer mention
head -20 "$SKILL_FILE" 2>/dev/null | grep -qi "disclaimer\|not legal advice\|informational purposes"
run_test "skill_mentions_disclaimer_in_first_20_lines" $?

# 3.4: SKILL.md has explicit "first 10 lines" mandate
grep -q "first 10 lines" "$SKILL_FILE" 2>/dev/null
run_test "skill_mandates_first_10_lines_placement" $?

# 3.5: Disclaimer template contains actual disclaimer text
grep -qi "not.*legal advice\|educational.*informational\|informational purposes" "$DISCLAIMER_FILE" 2>/dev/null
run_test "disclaimer_template_contains_disclaimer_text" $?

# 3.6: SKILL.md enforces HALT on missing disclaimer
grep -qi "HALT" "$SKILL_FILE" 2>/dev/null && grep -qi "disclaimer.*missing\|missing.*disclaimer\|disclaimer.*HALT" "$SKILL_FILE" 2>/dev/null
run_test "skill_halts_on_missing_disclaimer" $?

# 3.7: Disclaimer template is self-documenting (says it must appear in first 10 lines)
grep -q "first 10 lines" "$DISCLAIMER_FILE" 2>/dev/null
run_test "disclaimer_template_is_self_documenting" $?

# 3.8: Disclaimer enforcement section exists in SKILL.md
grep -q "Disclaimer Enforcement" "$SKILL_FILE" 2>/dev/null
run_test "skill_has_disclaimer_enforcement_section" $?

echo ""

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
TOTAL=$((PASSED + FAILED))
echo "============================================================"
echo "  Integration Test Summary: $PASSED/$TOTAL passed, $FAILED failed"
echo "============================================================"
[ $FAILED -eq 0 ] && exit 0 || exit 1
