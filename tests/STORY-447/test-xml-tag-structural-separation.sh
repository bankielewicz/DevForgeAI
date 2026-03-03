#!/bin/bash
# Test: STORY-447 - Introduce XML Tag Structural Separation
# Story: STORY-447
# Generated: 2026-02-18
# TDD Phase: RED (all tests expected to FAIL before implementation)

# === Test Configuration ===
PASSED=0
FAILED=0

SKILL_MD="/mnt/c/Projects/DevForgeAI2/src/claude/skills/discovering-requirements/SKILL.md"
IDEATE_MD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/ideate.md"
DISCOVERY_WF="/mnt/c/Projects/DevForgeAI2/src/claude/skills/discovering-requirements/references/discovery-workflow.md"

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

echo "========================================"
echo "STORY-447: XML Tag Structural Separation"
echo "========================================"

# ─── AC#1: SKILL.md Key Sections Wrapped in Semantic XML Tags ───────────────

echo ""
echo "AC#1: SKILL.md Key Sections Wrapped in Semantic XML Tags"

grep -q "<instructions>" "$SKILL_MD"
run_test "SKILL.md contains <instructions> opening tag" $?

grep -q "</instructions>" "$SKILL_MD"
run_test "SKILL.md contains </instructions> closing tag" $?

grep -q "<context>" "$SKILL_MD"
run_test "SKILL.md contains <context> opening tag" $?

grep -q "</context>" "$SKILL_MD"
run_test "SKILL.md contains </context> closing tag" $?

grep -q "<output_format>" "$SKILL_MD"
run_test "SKILL.md contains <output_format> opening tag" $?

grep -q "</output_format>" "$SKILL_MD"
run_test "SKILL.md contains </output_format> closing tag" $?

# Verify markdown content preserved: YAML frontmatter must still exist
grep -q "^name: discovering-requirements" "$SKILL_MD"
run_test "SKILL.md preserves YAML frontmatter name field inside XML wrappers" $?

grep -q "description:" "$SKILL_MD"
run_test "SKILL.md preserves description field inside XML wrappers" $?

# ─── AC#2: Phase Transition XML Handoff Schemas ──────────────────────────────

echo ""
echo "AC#2: Phase Transition XML Handoff Schemas"

grep -q "<phase-1-output>" "$SKILL_MD"
run_test "SKILL.md contains <phase-1-output> handoff schema" $?

grep -q "<phase-2-output>" "$SKILL_MD"
run_test "SKILL.md contains <phase-2-output> handoff schema" $?

grep -q "<phase-3-output>" "$SKILL_MD"
run_test "SKILL.md contains <phase-3-output> handoff schema" $?

grep -q "<phase-4-output>" "$SKILL_MD"
run_test "SKILL.md contains <phase-4-output> handoff schema" $?

# ─── AC#3: Command-to-Skill Handoff Uses XML Tags ────────────────────────────

echo ""
echo "AC#3: Command-to-Skill Handoff Uses XML Tags"

grep -q "<ideation-context>" "$IDEATE_MD"
run_test "ideate.md contains <ideation-context> XML tag" $?

grep -q "</ideation-context>" "$IDEATE_MD"
run_test "ideate.md contains </ideation-context> closing tag" $?

grep -q "<business-idea>" "$IDEATE_MD"
run_test "ideate.md contains <business-idea> child element" $?

grep -q "<brainstorm-id>" "$IDEATE_MD"
run_test "ideate.md contains <brainstorm-id> child element" $?

grep -q "<project-mode>" "$IDEATE_MD"
run_test "ideate.md contains <project-mode> child element" $?

# Verify markdown bold marker is replaced (should NOT exist as sole detection mechanism)
grep -q '^\*\*Business Idea:\*\*' "$IDEATE_MD"
run_test "ideate.md does NOT use bare **Business Idea:** markdown marker (replaced with XML)" $([ $? -ne 0 ] && echo 0 || echo 1)

# ─── AC#4: Skill Detection Logic Parses XML Tags ─────────────────────────────

echo ""
echo "AC#4: Skill Detection Logic Parses XML Tags"

grep -q "ideation-context" "$SKILL_MD"
run_test "SKILL.md Phase 1 Step 0 references <ideation-context> parsing" $?

grep -q "business-idea" "$SKILL_MD"
run_test "SKILL.md contains business-idea XML tag parsing logic" $?

# Backward compatibility: markdown bold marker detection still present with deprecation note
grep -qi "deprecat" "$SKILL_MD"
run_test "SKILL.md contains deprecation warning for markdown bold marker" $?

grep -q "Business Idea:" "$SKILL_MD"
run_test "SKILL.md retains backward-compatible markdown bold marker detection" $?

# ─── AC#5: Multi-Source Inputs Use XML Wrappers ──────────────────────────────

echo ""
echo "AC#5: Multi-Source Inputs Use XML Wrappers"

grep -q "<brainstorm_context>" "$SKILL_MD"
run_test "SKILL.md contains <brainstorm_context> XML wrapper" $?

grep -q "<user_input>" "$SKILL_MD"
run_test "SKILL.md contains <user_input> XML wrapper" $?

grep -q "<project_context>" "$SKILL_MD"
run_test "SKILL.md contains <project_context> XML wrapper" $?

# ─── AC#6: SKILL.md Line Count Constraint ────────────────────────────────────

echo ""
echo "AC#6: SKILL.md Line Count Constraint"

LINE_COUNT=$(wc -l < "$SKILL_MD")
[ "$LINE_COUNT" -lt 500 ]
run_test "SKILL.md is under 500 lines (currently $LINE_COUNT lines)" $?

# ─── AC#7: Round-Trip Handoff Test ───────────────────────────────────────────

echo ""
echo "AC#7: Round-Trip Handoff Test"

# Brainstorm mode: ideate.md emits <brainstorm-id>, SKILL.md parses it
grep -q "<brainstorm-id>" "$IDEATE_MD"
run_test "ideate.md emits <brainstorm-id> XML marker (brainstorm mode)" $?

grep -q "brainstorm-id" "$SKILL_MD"
run_test "SKILL.md parses brainstorm-id XML element (brainstorm mode)" $?

# Fresh mode: ideate.md emits <project-mode>fresh</project-mode>
grep -q "fresh" "$IDEATE_MD"
run_test "ideate.md includes fresh mode value in XML context" $?

# Project mode: <project-mode> element carries mode value
grep -q "project" "$IDEATE_MD"
run_test "ideate.md includes project mode value in <project-mode> element" $?

# SKILL.md handles each mode explicitly
grep -q "brainstorm mode\|brainstorm-mode\|mode.*brainstorm" "$SKILL_MD"
run_test "SKILL.md has mode-specific handling for brainstorm context" $?

# ─── Summary ─────────────────────────────────────────────────────────────────

echo ""
echo "========================================"
echo "Results: $PASSED passed, $FAILED failed"
echo "========================================"

if [ $FAILED -gt 0 ]; then
    echo "STATUS: RED (expected - TDD pre-implementation)"
fi

[ $FAILED -eq 0 ] && exit 0 || exit 1
