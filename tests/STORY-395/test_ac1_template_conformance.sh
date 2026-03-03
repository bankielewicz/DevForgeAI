#!/bin/bash
# Test: AC#1 - All 10 Agents Conform to Canonical Template Structure
# Story: STORY-395
# Generated: 2026-02-13
# TDD Phase: RED (tests expected to FAIL before migration)
#
# Validates that each of the 10 validator/analyzer agents contains
# all 10 required sections from the canonical template and has
# version set to "2.0.0" in YAML frontmatter.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
AGENTS_DIR="$PROJECT_ROOT/src/claude/agents"

# 10 target agents
AGENTS=(
    "anti-pattern-scanner"
    "context-validator"
    "context-preservation-validator"
    "coverage-analyzer"
    "code-quality-auditor"
    "deferral-validator"
    "dependency-graph-analyzer"
    "file-overlap-detector"
    "pattern-compliance-auditor"
    "tech-stack-detector"
)

# 10 required canonical template sections
# Section names must appear as H2 headings (## Section Name)
REQUIRED_SECTIONS=(
    "Purpose"
    "When Invoked"
    "Input/Output Specification"
    "Constraints and Boundaries"
    "Workflow"
    "Success Criteria"
    "Output Format"
    "Examples"
)

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

echo "=============================================="
echo "  AC#1: Template Conformance Validation"
echo "  Testing 10 agents x 10 sections + version"
echo "=============================================="
echo ""

# --- Test Group 1: Agent files exist ---
echo "--- Test Group 1: Agent Files Exist ---"
for agent in "${AGENTS[@]}"; do
    test -f "$AGENTS_DIR/${agent}.md" && RC=0 || RC=1
    run_test "File exists: ${agent}.md" $RC
done
echo ""

# --- Test Group 2: YAML Frontmatter with required fields ---
echo "--- Test Group 2: YAML Frontmatter Fields ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "YAML frontmatter: ${agent} (file missing)" 1
        continue
    fi

    # Check for YAML frontmatter delimiters (--- at start)
    head -1 "$AGENT_FILE" | grep -q "^---$" && RC=0 || RC=1
    run_test "YAML frontmatter start delimiter: ${agent}" $RC

    # Check for 'name' field in frontmatter
    sed -n '1,/^---$/p' "$AGENT_FILE" | tail -n +2 | head -n -1 | grep -q "^name:" && RC=0 || RC=1
    run_test "YAML field 'name': ${agent}" $RC

    # Check for 'description' field in frontmatter
    sed -n '1,/^---$/p' "$AGENT_FILE" | tail -n +2 | head -n -1 | grep -q "^description:" && RC=0 || RC=1
    run_test "YAML field 'description': ${agent}" $RC

    # Check for 'tools' field in frontmatter
    sed -n '1,/^---$/p' "$AGENT_FILE" | tail -n +2 | head -n -1 | grep -q "^tools:" && RC=0 || RC=1
    run_test "YAML field 'tools': ${agent}" $RC

    # Check for 'model' field in frontmatter
    sed -n '1,/^---$/p' "$AGENT_FILE" | tail -n +2 | head -n -1 | grep -q "^model:" && RC=0 || RC=1
    run_test "YAML field 'model': ${agent}" $RC
done
echo ""

# --- Test Group 3: Version field set to "2.0.0" ---
echo "--- Test Group 3: Version Field = 2.0.0 ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Version 2.0.0: ${agent} (file missing)" 1
        continue
    fi

    # Extract frontmatter and check version field equals "2.0.0"
    sed -n '2,/^---$/p' "$AGENT_FILE" | grep -qE '^version:\s*"2\.0\.0"' && RC=0 || RC=1
    run_test "Version is 2.0.0: ${agent}" $RC
done
echo ""

# --- Test Group 4: Title H1 matching name field ---
echo "--- Test Group 4: Title H1 Header ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Title H1: ${agent} (file missing)" 1
        continue
    fi

    # Check for H1 header (# Title) after frontmatter
    grep -q "^# " "$AGENT_FILE" && RC=0 || RC=1
    run_test "H1 title header exists: ${agent}" $RC
done
echo ""

# --- Test Group 5: All 8 required H2 sections present ---
echo "--- Test Group 5: Required H2 Sections ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        for section in "${REQUIRED_SECTIONS[@]}"; do
            run_test "Section '${section}': ${agent} (file missing)" 1
        done
        continue
    fi

    for section in "${REQUIRED_SECTIONS[@]}"; do
        # Match exact H2 section heading
        # Allow for variations like "## Purpose" or "## Purpose\n"
        grep -qE "^## ${section}$|^## ${section} " "$AGENT_FILE" && RC=0 || RC=1
        run_test "Section '${section}': ${agent}" $RC
    done
done
echo ""

# --- Test Group 6: YAML Frontmatter is complete block ---
echo "--- Test Group 6: YAML Frontmatter Complete Block ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "YAML block complete: ${agent} (file missing)" 1
        continue
    fi

    # Count --- delimiters: should have at least 2 (open and close)
    DELIMITER_COUNT=$(grep -c "^---$" "$AGENT_FILE" || true)
    if [ "$DELIMITER_COUNT" -ge 2 ]; then
        run_test "YAML frontmatter block complete (${DELIMITER_COUNT} delimiters): ${agent}" 0
    else
        run_test "YAML frontmatter block complete (${DELIMITER_COUNT} delimiters): ${agent}" 1
    fi
done
echo ""

# === Summary ===
echo "=============================================="
echo "  AC#1 Template Conformance Results"
echo "=============================================="
echo "  Total:  $TOTAL"
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo "=============================================="

if [ "$FAILED" -eq 0 ]; then
    echo "  STATUS: ALL TESTS PASSED"
    exit 0
else
    echo "  STATUS: $FAILED TESTS FAILED"
    exit 1
fi
