#!/bin/bash
# Test: AC#3 - All 17 Skill SKILL.md Files Reviewed and Improved
# Story: STORY-397
# Generated: 2026-02-13
# TDD Phase: RED (tests should FAIL before implementation)
#
# Validates that all skill SKILL.md files conform to standardized sections
# (Purpose, Execution Phases, Validation Gates, Error Handling), apply
# Anthropic prompt patterns, and maintain backward compatibility.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILLS_DIR="${PROJECT_ROOT}/src/claude/skills"

# All skill directories expected to contain SKILL.md
SKILLS=(
    "devforgeai-ideation"
    "devforgeai-brainstorming"
    "devforgeai-architecture"
    "devforgeai-orchestration"
    "devforgeai-story-creation"
    "devforgeai-ui-generator"
    "devforgeai-development"
    "devforgeai-qa"
    "devforgeai-release"
    "devforgeai-documentation"
    "devforgeai-feedback"
    "devforgeai-rca"
    "devforgeai-subagent-creation"
    "devforgeai-mcp-cli-converter"
    "claude-code-terminal-expert"
    "devforgeai-github-actions"
    "skill-creator"
)

# Required standardized sections for skill files
SKILL_SECTIONS=(
    "## Purpose"
    "## Error Handling"
)

# === Helper Functions ===
run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

# === Test Suite ===
echo "============================================================"
echo "  AC#3: Skill SKILL.md Improvements (17 Skills)"
echo "  Story: STORY-397 | Phase: RED"
echo "============================================================"
echo ""

# --- Test Group 1: All 17 SKILL.md files exist ---
echo "--- Test Group 1: Skill File Existence ---"
SKILL_COUNT=0
for skill in "${SKILLS[@]}"; do
    FILE="${SKILLS_DIR}/${skill}/SKILL.md"
    if test -f "$FILE"; then
        run_test "SKILL.md exists: ${skill}" 0
        ((SKILL_COUNT++))
    else
        run_test "SKILL.md exists: ${skill}" 1
    fi
done
echo "  Found ${SKILL_COUNT}/17 skill files"
echo ""

# --- Test Group 2: Standardized section headers ---
echo "--- Test Group 2: Standardized Sections ---"
for skill in "${SKILLS[@]}"; do
    FILE="${SKILLS_DIR}/${skill}/SKILL.md"
    if [ -f "$FILE" ]; then
        for section in "${SKILL_SECTIONS[@]}"; do
            if grep -q "^${section}" "$FILE" 2>/dev/null; then
                run_test "Section '${section}' in ${skill}/SKILL.md" 0
            else
                run_test "Section '${section}' in ${skill}/SKILL.md" 1
            fi
        done

        # Check for execution phases or phase-related content
        if grep -qiE '(## (Execution )?Phase|## Workflow|Phase [0-9]|Phase 0[1-9])' "$FILE" 2>/dev/null; then
            run_test "Execution phases present in ${skill}/SKILL.md" 0
        else
            run_test "Execution phases present in ${skill}/SKILL.md" 1
        fi

        # Check for validation gates
        if grep -qiE '(## Validation|validation gate|quality gate|## Success Criteria)' "$FILE" 2>/dev/null; then
            run_test "Validation gates present in ${skill}/SKILL.md" 0
        else
            run_test "Validation gates present in ${skill}/SKILL.md" 1
        fi
    else
        for section in "${SKILL_SECTIONS[@]}"; do
            run_test "Section '${section}' in ${skill}/SKILL.md (file missing)" 1
        done
        run_test "Execution phases in ${skill}/SKILL.md (file missing)" 1
        run_test "Validation gates in ${skill}/SKILL.md (file missing)" 1
    fi
done
echo ""

# --- Test Group 3: Anthropic prompt patterns in skill phase instructions ---
echo "--- Test Group 3: Anthropic Patterns in Skills ---"
for skill in "${SKILLS[@]}"; do
    FILE="${SKILLS_DIR}/${skill}/SKILL.md"
    if [ -f "$FILE" ]; then
        # Check for chain-of-thought reasoning instructions in phases
        if grep -qiE '(\*?Reasoning:?\*?|reason about|think through|step.by.step|explicit.?reasoning)' "$FILE" 2>/dev/null; then
            run_test "CoT reasoning in phase instructions: ${skill}/SKILL.md" 0
        else
            run_test "CoT reasoning in phase instructions: ${skill}/SKILL.md" 1
        fi

        # Check for structured output specification for phase results
        if grep -qiE '(structured.?output|output.?format|result.?format|json.?schema|output.?structure)' "$FILE" 2>/dev/null; then
            run_test "Structured output for phases: ${skill}/SKILL.md" 0
        else
            run_test "Structured output for phases: ${skill}/SKILL.md" 1
        fi
    else
        run_test "CoT reasoning: ${skill}/SKILL.md (file missing)" 1
        run_test "Structured output: ${skill}/SKILL.md (file missing)" 1
    fi
done
echo ""

# --- Test Group 4: Backward compatibility - entry points unchanged ---
echo "--- Test Group 4: Backward Compatibility ---"
for skill in "${SKILLS[@]}"; do
    FILE="${SKILLS_DIR}/${skill}/SKILL.md"
    if [ -f "$FILE" ]; then
        # Check YAML frontmatter has name: field (entry point identifier)
        if grep -q '^name:' "$FILE" 2>/dev/null; then
            run_test "Frontmatter name: field preserved in ${skill}/SKILL.md" 0
        else
            run_test "Frontmatter name: field preserved in ${skill}/SKILL.md" 1
        fi

        # Check YAML frontmatter has description: field
        if grep -q '^description:' "$FILE" 2>/dev/null; then
            run_test "Frontmatter description: field in ${skill}/SKILL.md" 0
        else
            run_test "Frontmatter description: field in ${skill}/SKILL.md" 1
        fi
    else
        run_test "Frontmatter name: in ${skill}/SKILL.md (file missing)" 1
        run_test "Frontmatter description: in ${skill}/SKILL.md (file missing)" 1
    fi
done
echo ""

# --- Test Group 5: Content quality - no redundant/empty sections ---
echo "--- Test Group 5: Content Quality ---"
for skill in "${SKILLS[@]}"; do
    FILE="${SKILLS_DIR}/${skill}/SKILL.md"
    if [ -f "$FILE" ]; then
        # Check Purpose section has minimum 2 sentences (non-empty)
        PURPOSE_CONTENT=$(awk '/^## Purpose/{found=1; next} found && /^## [A-Z]/{exit} found && NF{count++} END{print count+0}' "$FILE")
        if [ "$PURPOSE_CONTENT" -ge 2 ] 2>/dev/null; then
            run_test "Purpose has 2+ content lines: ${skill}/SKILL.md" 0
        else
            run_test "Purpose has 2+ content lines: ${skill}/SKILL.md" 1
        fi

        # Check Error Handling section exists and has content
        ERROR_CONTENT=$(awk '/^## Error Handling/{found=1; next} found && /^## [A-Z]/{exit} found && NF{count++} END{print count+0}' "$FILE")
        if [ "$ERROR_CONTENT" -ge 1 ] 2>/dev/null; then
            run_test "Error Handling has content: ${skill}/SKILL.md" 0
        else
            run_test "Error Handling has content: ${skill}/SKILL.md" 1
        fi
    else
        run_test "Purpose content: ${skill}/SKILL.md (file missing)" 1
        run_test "Error Handling content: ${skill}/SKILL.md (file missing)" 1
    fi
done
echo ""

# === Summary ===
echo "============================================================"
echo "  AC#3 Results: ${PASSED} passed, ${FAILED} failed (${TOTAL} total)"
echo "============================================================"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
