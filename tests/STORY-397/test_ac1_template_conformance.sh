#!/bin/bash
# Test: AC#1 - All 17 Remaining Agents Conform to Canonical Template Structure
# Story: STORY-397
# Generated: 2026-02-13
# TDD Phase: RED (tests should FAIL before implementation)
#
# Validates that all 17 remaining agent files contain the 10 required
# sections from the canonical template v2.0.0, plus version field validation.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
AGENTS_DIR="${PROJECT_ROOT}/src/claude/agents"

# The 17 remaining agents targeted for Wave 3 migration
AGENTS=(
    "architect-reviewer"
    "documentation-writer"
    "framework-analyst"
    "git-validator"
    "git-worktree-manager"
    "ideation-result-interpreter"
    "internet-sleuth"
    "observation-extractor"
    "qa-result-interpreter"
    "dev-result-interpreter"
    "session-miner"
    "sprint-planner"
    "stakeholder-analyst"
    "story-requirements-analyst"
    "technical-debt-analyzer"
    "ui-spec-formatter"
    "agent-generator"
)

# The 10 required canonical template sections
REQUIRED_SECTIONS=(
    "## Purpose"
    "## When Invoked"
    "## Input/Output Specification"
    "## Constraints and Boundaries"
    "## Workflow"
    "## Success Criteria"
    "## Output Format"
    "## Examples"
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
echo "  AC#1: Template Conformance Tests (17 Agents x 10 Sections)"
echo "  Story: STORY-397 | Phase: RED"
echo "============================================================"
echo ""

# --- Test Group 1: All 17 agent files exist in src/ tree ---
echo "--- Test Group 1: Agent File Existence ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if test -f "$FILE"; then
        run_test "File exists: src/claude/agents/${agent}.md" 0
    else
        run_test "File exists: src/claude/agents/${agent}.md" 1
    fi
done
echo ""

# --- Test Group 2: YAML Frontmatter contains version: "2.0.0" ---
echo "--- Test Group 2: Version Field = 2.0.0 ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        # Check for version field set to 2.0.0 in YAML frontmatter
        # Frontmatter is between first two --- lines
        if grep -q '^version: ["'"'"']2\.0\.0["'"'"']' "$FILE" 2>/dev/null; then
            run_test "Version 2.0.0 in ${agent}.md" 0
        else
            run_test "Version 2.0.0 in ${agent}.md" 1
        fi
    else
        run_test "Version 2.0.0 in ${agent}.md (file missing)" 1
    fi
done
echo ""

# --- Test Group 3: Required Section Headers Present ---
echo "--- Test Group 3: 10 Required Canonical Sections ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        # Section 1: YAML Frontmatter with required fields
        # Check that frontmatter starts with --- and contains name: and description:
        HAS_FRONTMATTER=0
        if head -1 "$FILE" | grep -q '^---$'; then
            if grep -q '^name:' "$FILE" && grep -q '^description:' "$FILE"; then
                HAS_FRONTMATTER=0
            else
                HAS_FRONTMATTER=1
            fi
        else
            HAS_FRONTMATTER=1
        fi
        run_test "YAML Frontmatter (name+description) in ${agent}.md" $HAS_FRONTMATTER

        # Section 2: Title H1 matching name field
        AGENT_NAME_WORDS=$(echo "$agent" | sed 's/-/ /g')
        if grep -qi "^# " "$FILE" 2>/dev/null; then
            run_test "H1 Title present in ${agent}.md" 0
        else
            run_test "H1 Title present in ${agent}.md" 1
        fi

        # Sections 3-10: Required section headers
        for section in "${REQUIRED_SECTIONS[@]}"; do
            if grep -q "^${section}" "$FILE" 2>/dev/null; then
                run_test "Section '${section}' in ${agent}.md" 0
            else
                run_test "Section '${section}' in ${agent}.md" 1
            fi
        done
    else
        # File missing - fail all section checks
        run_test "YAML Frontmatter in ${agent}.md (file missing)" 1
        run_test "H1 Title in ${agent}.md (file missing)" 1
        for section in "${REQUIRED_SECTIONS[@]}"; do
            run_test "Section '${section}' in ${agent}.md (file missing)" 1
        done
    fi
done
echo ""

# --- Test Group 4: Frontmatter contains all required fields ---
echo "--- Test Group 4: Complete Frontmatter Fields ---"
FRONTMATTER_FIELDS=("name:" "description:" "tools:" "model:" "version:")
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        for field in "${FRONTMATTER_FIELDS[@]}"; do
            if grep -q "^${field}" "$FILE" 2>/dev/null; then
                run_test "Frontmatter field '${field}' in ${agent}.md" 0
            else
                run_test "Frontmatter field '${field}' in ${agent}.md" 1
            fi
        done
    else
        for field in "${FRONTMATTER_FIELDS[@]}"; do
            run_test "Frontmatter field '${field}' in ${agent}.md (file missing)" 1
        done
    fi
done
echo ""

# --- Test Group 5: Non-empty sections (minimum 2 lines of content) ---
echo "--- Test Group 5: Non-Empty Section Content ---"
for agent in "${AGENTS[@]}"; do
    FILE="${AGENTS_DIR}/${agent}.md"
    if [ -f "$FILE" ]; then
        # Check that ## Purpose has at least 2 lines of content after it
        PURPOSE_LINES=$(awk '/^## Purpose/{found=1; next} found && /^## /{exit} found && NF{count++} END{print count+0}' "$FILE")
        if [ "$PURPOSE_LINES" -ge 2 ] 2>/dev/null; then
            run_test "Purpose has 2+ content lines in ${agent}.md" 0
        else
            run_test "Purpose has 2+ content lines in ${agent}.md" 1
        fi

        # Check that ## Examples has at least 1 Task() pattern
        if grep -q 'Task(' "$FILE" 2>/dev/null; then
            run_test "Examples contains Task() pattern in ${agent}.md" 0
        else
            run_test "Examples contains Task() pattern in ${agent}.md" 1
        fi
    else
        run_test "Purpose has content in ${agent}.md (file missing)" 1
        run_test "Examples contains Task() in ${agent}.md (file missing)" 1
    fi
done
echo ""

# === Summary ===
echo "============================================================"
echo "  AC#1 Results: ${PASSED} passed, ${FAILED} failed (${TOTAL} total)"
echo "============================================================"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
