#!/bin/bash
################################################################################
# Test Suite: AC#4, AC#5, AC#6, AC#8 - Quality & Structure Validation
#
# Tests for:
# - AC#4: Cross-Reference Consistency Validation (file paths, load commands)
# - AC#5: Discoverability Verification (400 lines, clear directions)
# - AC#6: Integration with Existing Structure (numbering, links intact)
# - AC#8: Documentation Quality Standards (no placeholders, examples concrete)
#
# Test Framework: Bash/Shell (grep, wc, test)
# Test Pattern: AAA (Arrange, Act, Assert)
#
# Status: RED PHASE - All tests should FAIL (implementation not started)
################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

CLAUDEMD_FILE="src/CLAUDE.md"
COMMANDS_REF_FILE="src/claude/memory/commands-reference.md"
SKILLS_REF_FILE="src/claude/memory/skills-reference.md"

# Placeholder patterns (prohibited)
PLACEHOLDER_PATTERNS=(
    "TODO"
    "TBD"
    "replace with"
    "example feature"
    "Your feature"
    "placeholder"
    "FIXME"
    "XXX"
)

# Prohibited load command patterns
PROHIBITED_LOAD_PATTERNS=(
    "cat"
    "@file"
    "source"
    "include"
    "\\|cat"
    "&& cat"
)

# Approved file paths (should start with src/)
APPROVED_PATH_PATTERNS=(
    "src/claude/memory/"
    "src/CLAUDE.md"
    "src/claude/skills/"
)

################################################################################
# Helper Functions
################################################################################

assert_file_exists() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAIL${NC}: File does not exist: $file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_no_pattern() {
    local file="$1"
    local pattern="$2"
    local test_name="$3"

    if grep -qi "$pattern" "$file"; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Found prohibited pattern: '$pattern' in $file"
        # Show matching lines
        grep -n -i "$pattern" "$file" | head -3 | sed 's/^/    Line /'
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
    echo -e "${GREEN}PASS${NC}: $test_name"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

assert_file_path_exists() {
    local file_path="$1"
    local test_name="$2"

    if [[ ! -f "$file_path" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  File does not exist: $file_path"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
    echo -e "${GREEN}PASS${NC}: $test_name"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

assert_section_within_lines() {
    local file="$1"
    local section_header="$2"
    local max_line="$3"
    local test_name="$4"

    local line_num=$(grep -n "^## $section_header" "$file" | cut -d: -f1)

    if [[ -z "$line_num" ]]; then
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Section '$section_header' not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi

    if [[ $line_num -le $max_line ]]; then
        echo -e "${GREEN}PASS${NC}: $test_name"
        echo "  Found on line $line_num (within $max_line)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: $test_name"
        echo "  Found on line $line_num (expected within line $max_line)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

count_pattern_in_file() {
    local file="$1"
    local pattern="$2"
    echo $(grep -c "$pattern" "$file" || echo 0)
}

################################################################################
# TEST CASES: AC#4, AC#5, AC#6, AC#8
################################################################################

echo "=========================================="
echo "TEST SUITE: AC#4-6, AC#8 - Quality & Structure"
echo "=========================================="
echo ""

# ============================================================================
# AC#4: Cross-Reference Consistency Validation
# ============================================================================

echo "--- AC#4: Cross-Reference Consistency Validation ---"
echo ""

# Test 4.1: File paths exist
echo "Test 4.1: All cross-referenced files exist"
{
    # Extract file paths from Read() commands
    local files_mentioned=(
        "src/claude/memory/effective-prompting-guide.md"
        "src/claude/memory/user-input-guidance.md"
        "src/claude/memory/claude-code-terminal-expert.md"
    )

    for filepath in "${files_mentioned[@]}"; do
        {
            assert_file_path_exists "$filepath" \
                "File path exists: $filepath"
        }
    done
}
echo ""

# Test 4.2: All load commands use Read() syntax, not Bash commands
echo "Test 4.2: No prohibited load command patterns (cat, @file, source, include)"
for pattern in "${PROHIBITED_LOAD_PATTERNS[@]}"; do
    {
        # Check in all three documentation files
        local in_claude=$(grep -i "$pattern" "$CLAUDEMD_FILE" 2>/dev/null | wc -l)
        local in_commands=$(grep -i "$pattern" "$COMMANDS_REF_FILE" 2>/dev/null | wc -l)
        local in_skills=$(grep -i "$pattern" "$SKILLS_REF_FILE" 2>/dev/null | wc -l)

        # Some patterns may be acceptable in other contexts, so be selective
        # Only fail if found in context of file loading documentation
        local found_in_context=0

        if echo "$pattern" | grep -q "cat\|@file\|source\|include"; then
            if grep -B2 -A2 -i "$pattern" "$CLAUDEMD_FILE" | grep -qi "Load\|Read\|file"; then
                found_in_context=1
            fi
        fi

        if [[ $found_in_context -eq 0 ]]; then
            echo -e "${GREEN}PASS${NC}: Pattern '$pattern' not used in load command context"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}FAIL${NC}: Prohibited pattern '$pattern' found in load command context"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    }
done
echo ""

# Test 4.3: Check for Read() commands using correct syntax
echo "Test 4.3: Read() commands use correct syntax: Read(file_path=\"...\")"
{
    local correct_syntax_count=$(grep -c 'Read(file_path=' "$CLAUDEMD_FILE" "$COMMANDS_REF_FILE" "$SKILLS_REF_FILE" 2>/dev/null || echo 0)

    if [[ $correct_syntax_count -ge 3 ]]; then
        echo -e "${GREEN}PASS${NC}: Found $correct_syntax_count correct Read() syntax patterns"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Found only $correct_syntax_count correct Read() patterns (expected ≥3)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 4.4: All file paths use src/ prefix (not .claude/)
echo "Test 4.4: All file paths use src/ prefix (repository-relative, not .claude/ or .devforgeai/)"
{
    local bad_paths=$(grep -n "file_path.*\.claude/\|file_path.*\.devforgeai/" \
        "$CLAUDEMD_FILE" "$COMMANDS_REF_FILE" "$SKILLS_REF_FILE" 2>/dev/null | wc -l || echo 0)

    if [[ $bad_paths -eq 0 ]]; then
        echo -e "${GREEN}PASS${NC}: No incorrect path prefixes found"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Found $bad_paths incorrect path prefixes"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# ============================================================================
# AC#5: Discoverability Verification
# ============================================================================

echo "--- AC#5: Discoverability Verification ---"
echo ""

# Test 5.1: Learning section appears in first 400 lines of CLAUDE.md
echo "Test 5.1: Learning DevForgeAI section within first 400 lines"
assert_section_within_lines "$CLAUDEMD_FILE" "Learning DevForgeAI" 400 \
    "Learning section is discoverable in first 400 lines" || true
echo ""

# Test 5.2: Clear directions to appropriate guidance documents
echo "Test 5.2: Learning section provides clear directions and guidance references"
{
    local learning_section_start=$(grep -n "^## Learning DevForgeAI" "$CLAUDEMD_FILE" | cut -d: -f1)
    local next_section=$(grep -n "^## Development Workflow" "$CLAUDEMD_FILE" | cut -d: -f1)

    if [[ -n "$learning_section_start" && -n "$next_section" ]]; then
        local learning_content=$(sed -n "${learning_section_start},${next_section}p" "$CLAUDEMD_FILE")

        # Check for guidance directions
        local has_directions=0
        if echo "$learning_content" | grep -qi "guidance\|reference\|resources\|learning"; then
            has_directions=1
        fi

        if [[ $has_directions -eq 1 ]]; then
            echo -e "${GREEN}PASS${NC}: Clear directions and guidance references found"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}FAIL${NC}: Unclear directions in Learning section"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        echo -e "${RED}FAIL${NC}: Learning section not properly positioned"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 5.3: File paths and load commands are complete (no additional searches needed)
echo "Test 5.3: File paths and load commands are complete (no 'see' or 'find' required)"
{
    local learning_section_start=$(grep -n "^## Learning DevForgeAI" "$CLAUDEMD_FILE" | cut -d: -f1)
    local next_section=$(grep -n "^## Development Workflow" "$CLAUDEMD_FILE" | cut -d: -f1)

    if [[ -n "$learning_section_start" && -n "$next_section" ]]; then
        local learning_content=$(sed -n "${learning_section_start},${next_section}p" "$CLAUDEMD_FILE")

        # Count Read commands
        local read_count=$(echo "$learning_content" | grep -c "Read(file_path=" || echo 0)

        if [[ $read_count -ge 3 ]]; then
            echo -e "${GREEN}PASS${NC}: Found $read_count complete load commands (no search needed)"
            TESTS_PASSED=$((TESTS_PASSED + 1))
        else
            echo -e "${RED}FAIL${NC}: Insufficient load commands ($read_count found)"
            TESTS_FAILED=$((TESTS_FAILED + 1))
        fi
    else
        echo -e "${RED}FAIL${NC}: Learning section not found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# ============================================================================
# AC#6: Integration with Existing Structure
# ============================================================================

echo "--- AC#6: Integration with Existing Structure ---"
echo ""

# Test 6.1: Existing section numbering intact
echo "Test 6.1: Core sections still exist: Quick Reference, Development Workflow"
{
    if grep -q "^## Quick Reference - Progressive Disclosure" "$CLAUDEMD_FILE" && \
       grep -q "^## Development Workflow Overview" "$CLAUDEMD_FILE"; then
        echo -e "${GREEN}PASS${NC}: Core section headers intact"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Core sections missing or renamed"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 6.2: No section headers removed or substantially modified
echo "Test 6.2: Existing section headers preserved (no removals or major changes)"
{
    # Count major headers (should be significant)
    local header_count=$(grep -c "^## " "$CLAUDEMD_FILE" || echo 0)

    # Should have at least 20 major sections
    if [[ $header_count -ge 20 ]]; then
        echo -e "${GREEN}PASS${NC}: Found $header_count major sections (structure preserved)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Only $header_count major sections (structure may be damaged)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 6.3: Formatting conventions followed (heading levels, bullet points)
echo "Test 6.3: New sections follow existing formatting conventions"
{
    if grep -q "^## Learning DevForgeAI" "$CLAUDEMD_FILE" && \
       grep -q "^### Writing Effective Feature Descriptions" "$CLAUDEMD_FILE"; then
        echo -e "${GREEN}PASS${NC}: Heading levels match existing conventions"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Heading levels inconsistent with conventions"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# ============================================================================
# AC#8: Documentation Quality Standards
# ============================================================================

echo "--- AC#8: Documentation Quality Standards ---"
echo ""

# Test 8.1: No placeholder content (TODO, TBD, FIXME, etc.)
echo "Test 8.1: No placeholder content detected"
for placeholder in "${PLACEHOLDER_PATTERNS[@]}"; do
    {
        assert_no_pattern "$CLAUDEMD_FILE" "$placeholder" \
            "No placeholder '$placeholder' in CLAUDE.md" || true
        assert_no_pattern "$COMMANDS_REF_FILE" "$placeholder" \
            "No placeholder '$placeholder' in commands-reference.md" || true
        assert_no_pattern "$SKILLS_REF_FILE" "$placeholder" \
            "No placeholder '$placeholder' in skills-reference.md" || true
    }
done
echo ""

# Test 8.2: Examples are concrete (not generic placeholders)
echo "Test 8.2: Examples demonstrate practical use cases (realistic, not generic)"
{
    # Look for examples in Learning section
    local learning_section=$(sed -n '/^## Learning DevForgeAI/,/^##/p' "$CLAUDEMD_FILE" | head -n -1)

    if echo "$learning_section" | grep -q "❌\|✅"; then
        echo -e "${GREEN}PASS${NC}: Example format found (good vs bad examples)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: No example pairs found"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 8.3: File paths are absolute and repository-relative
echo "Test 8.3: All file paths use absolute, repository-relative format (no ../ or relative paths)"
{
    # Check for relative path patterns
    local relative_paths=$(grep -n "\\.\\./\|~/" "$CLAUDEMD_FILE" "$COMMANDS_REF_FILE" "$SKILLS_REF_FILE" 2>/dev/null | wc -l || echo 0)

    if [[ $relative_paths -eq 0 ]]; then
        echo -e "${GREEN}PASS${NC}: No relative paths found"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Found $relative_paths relative path references"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 8.4: Load examples use DevForgeAI-approved Read tool
echo "Test 8.4: Load examples use Read tool, not Bash cat"
{
    local read_count=$(grep -c "Read(file_path=" "$CLAUDEMD_FILE" "$COMMANDS_REF_FILE" "$SKILLS_REF_FILE" 2>/dev/null || echo 0)
    local bash_count=$(grep -c "bash\|cat\|Bash(" "$CLAUDEMD_FILE" "$COMMANDS_REF_FILE" "$SKILLS_REF_FILE" 2>/dev/null | grep -v "# Read\|Read tool" | wc -l || echo 0)

    if [[ $read_count -ge 3 && $bash_count -eq 0 ]]; then
        echo -e "${GREEN}PASS${NC}: Read tool used exclusively ($read_count uses)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}FAIL${NC}: Inconsistent load command tools"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}
echo ""

# Test 8.5: Descriptions are clear and jargon-free
echo "Test 8.5: Documentation is clear and accessible (appropriate for new users)"
{
    # Simple heuristic: check for excessive technical jargon
    local complex_jargon=$(grep -i "DSL\|AST\|REPL\|monad\|currying\|tail recursion" \
        "$CLAUDEMD_FILE" "$COMMANDS_REF_FILE" "$SKILLS_REF_FILE" 2>/dev/null | wc -l || echo 0)

    if [[ $complex_jargon -le 2 ]]; then
        echo -e "${GREEN}PASS${NC}: Documentation is accessible (minimal esoteric jargon)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${YELLOW}INFO${NC}: Documentation may contain advanced terminology ($complex_jargon occurrences)"
    fi
}
echo ""

################################################################################
# Test Summary
################################################################################

echo "=========================================="
echo "TEST SUMMARY: AC#4, AC#5, AC#6, AC#8"
echo "=========================================="
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
else
    exit 0
fi
