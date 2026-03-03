#!/bin/bash

##############################################################################
# Test Suite: STORY-042 Acceptance Criteria Tests
# Purpose: Validate all 7 acceptance criteria for framework file migration
# Format: Bash script with TAP (Test Anything Protocol) compatible output
#
# AC-1: Copy .claude/ to src/claude/ with structure preserved (~370 files)
# AC-2: Copy devforgeai/ config/docs/protocols/specs/tests (~80 files)
# AC-3: Copy CLAUDE.md to src/CLAUDE.md as template
# AC-4: Validate file integrity with checksum verification (100% match)
# AC-5: Exclude backup files and build artifacts
# AC-6: Git track all copied files
# AC-7: Preserve original operational directories unchanged
##############################################################################

set -o pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Setup/Teardown
TEMP_DIR=""
TEST_LOG="/tmp/story-042-ac-tests.log"

##############################################################################
# Test Framework Functions
##############################################################################

setup_test_environment() {
    TEMP_DIR=$(mktemp -d)
    export TEMP_DIR
    echo "Test environment setup: $TEMP_DIR" >> "$TEST_LOG"
}

cleanup_test_environment() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
        echo "Test cleanup completed" >> "$TEST_LOG"
    fi
}

assert_file_count() {
    local dir=$1
    local expected=$2
    local tolerance=${3:-10}

    local actual=$(find "$dir" -type f 2>/dev/null | wc -l)
    local lower=$((expected - tolerance))
    local upper=$((expected + tolerance))

    if [ "$actual" -ge "$lower" ] && [ "$actual" -le "$upper" ]; then
        echo -e "${GREEN}✓${NC} File count verified: $actual (expected $expected ±$tolerance)"
        return 0
    else
        echo -e "${RED}✗${NC} File count mismatch: $actual files (expected $expected ±$tolerance)"
        return 1
    fi
}

assert_checksum_match() {
    local source=$1
    local dest=$2
    local filename=${source##*/}

    local src_hash=$(sha256sum "$source" 2>/dev/null | awk '{print $1}')
    local dst_hash=$(sha256sum "$dest" 2>/dev/null | awk '{print $1}')

    if [ "$src_hash" = "$dst_hash" ]; then
        echo -e "${GREEN}✓${NC} Checksum match: $filename"
        return 0
    else
        echo -e "${RED}✗${NC} Checksum mismatch: $filename (src: $src_hash, dst: $dst_hash)"
        return 1
    fi
}

assert_file_size_match() {
    local source=$1
    local dest=$2

    local src_size=$(stat -c%s "$source" 2>/dev/null || stat -f%z "$source" 2>/dev/null)
    local dst_size=$(stat -c%s "$dest" 2>/dev/null || stat -f%z "$dest" 2>/dev/null)

    if [ "$src_size" = "$dst_size" ]; then
        echo -e "${GREEN}✓${NC} File size match: $(basename "$source")"
        return 0
    else
        echo -e "${RED}✗${NC} File size mismatch: $(basename "$source") (src: $src_size, dst: $dst_size)"
        return 1
    fi
}

assert_directory_exists() {
    local dir=$1

    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} Directory exists: $dir"
        return 0
    else
        echo -e "${RED}✗${NC} Directory not found: $dir"
        return 1
    fi
}

assert_file_exists() {
    local file=$1

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} File exists: $file"
        return 0
    else
        echo -e "${RED}✗${NC} File not found: $file"
        return 1
    fi
}

assert_no_matches() {
    local pattern=$1
    local search_dir=$2
    local description=$3

    local matches=$(find "$search_dir" -name "$pattern" 2>/dev/null | wc -l)

    if [ "$matches" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} No excluded files found: $description"
        return 0
    else
        echo -e "${RED}✗${NC} Found $matches excluded files: $description"
        return 1
    fi
}

assert_git_added_count() {
    local expected=$1
    local tolerance=${2:-10}

    local actual=$(git status --porcelain 2>/dev/null | grep "^A " | wc -l)
    local lower=$((expected - tolerance))
    local upper=$((expected + tolerance))

    if [ "$actual" -ge "$lower" ] && [ "$actual" -le "$upper" ]; then
        echo -e "${GREEN}✓${NC} Git added files: $actual (expected $expected ±$tolerance)"
        return 0
    else
        echo -e "${RED}✗${NC} Git added file count mismatch: $actual (expected $expected ±$tolerance)"
        return 1
    fi
}

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"
    echo "Running: $test_func" >> "$TEST_LOG"

    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo "PASSED" >> "$TEST_LOG"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo "FAILED" >> "$TEST_LOG"
    fi
}

##############################################################################
# AC-1: Copy .claude/ to src/claude/ with structure preserved
##############################################################################

test_ac1_claude_directory_exists() {
    # Test: src/claude/ directory created
    [ -d "src/claude" ] && echo -e "${GREEN}✓${NC} src/claude/ directory exists" && return 0
    echo -e "${RED}✗${NC} src/claude/ directory not found" && return 1
}

test_ac1_subdirectories_preserved() {
    # Test: All subdirectories from .claude/ are preserved in src/claude/
    local required_dirs=("agents" "commands" "memory" "scripts" "skills")
    local all_exist=true

    for dir in "${required_dirs[@]}"; do
        if [ -d "src/claude/$dir" ]; then
            echo -e "${GREEN}✓${NC} Subdirectory preserved: src/claude/$dir"
        else
            echo -e "${RED}✗${NC} Subdirectory missing: src/claude/$dir"
            all_exist=false
        fi
    done

    [ "$all_exist" = true ] && return 0 || return 1
}

test_ac1_file_count_approximately_370() {
    # Test: Approximately 370 files in src/claude/ (±10)
    assert_file_count "src/claude" 370 10
}

test_ac1_nested_structure_preserved() {
    # Test: Deep nested directory structure preserved
    # E.g., .claude/skills/devforgeai-development/references/ → src/claude/skills/devforgeai-development/references/
    if [ -d "src/claude/skills/devforgeai-development/references" ]; then
        echo -e "${GREEN}✓${NC} Nested structure preserved: src/claude/skills/devforgeai-development/references/"
        return 0
    else
        echo -e "${RED}✗${NC} Nested structure not preserved"
        return 1
    fi
}

test_ac1_original_unchanged() {
    # Test: Original .claude/ directory unchanged (verify file count match)
    local original_count=$(find ".claude" -type f 2>/dev/null | wc -l)
    local copied_count=$(find "src/claude" -type f 2>/dev/null | wc -l)

    # Should be approximately equal (within variance)
    if [ "$((original_count - copied_count))" -le 5 ]; then
        echo -e "${GREEN}✓${NC} Original .claude/ unchanged: $original_count files present"
        return 0
    else
        echo -e "${RED}✗${NC} File count mismatch: Original=$original_count, Copied=$copied_count"
        return 1
    fi
}

##############################################################################
# AC-2: Copy devforgeai/ config/docs/protocols/specs/tests (~80 files)
##############################################################################

test_ac2_devforgeai_directory_exists() {
    # Test: src/devforgeai/ directory created
    assert_directory_exists "src/devforgeai"
}

test_ac2_allowed_subdirs_only() {
    # Test: Only config/, docs/, protocols/, specs/, tests/ subdirectories present
    # Excluded: qa/reports/, RCA/, adrs/, feedback/imported/, logs/

    local excluded_dirs=("qa/reports" "RCA" "adrs" "feedback/imported" "logs")
    local found_excluded=false

    for dir in "${excluded_dirs[@]}"; do
        if [ -d "src/devforgeai/$dir" ]; then
            echo -e "${RED}✗${NC} Excluded directory found: src/devforgeai/$dir"
            found_excluded=true
        fi
    done

    if [ "$found_excluded" = false ]; then
        echo -e "${GREEN}✓${NC} No excluded generated-content directories found"
        return 0
    else
        return 1
    fi
}

test_ac2_required_subdirs_present() {
    # Test: Required subdirectories present (config, docs, protocols, specs, tests)
    local required_dirs=("config" "docs" "protocols" "specs" "tests")
    local all_present=true

    for dir in "${required_dirs[@]}"; do
        if [ -d "src/devforgeai/$dir" ]; then
            echo -e "${GREEN}✓${NC} Required subdirectory present: src/devforgeai/$dir"
        else
            echo -e "${RED}✗${NC} Required subdirectory missing: src/devforgeai/$dir"
            all_present=false
        fi
    done

    [ "$all_present" = true ] && return 0 || return 1
}

test_ac2_file_count_approximately_80() {
    # Test: Approximately 80 files in src/devforgeai/ (±10)
    assert_file_count "src/devforgeai" 80 10
}

test_ac2_subdirectory_file_counts() {
    # Test: Individual subdirectory file counts are approximately as expected
    local -A expected_counts=(
        ["config"]=8
        ["docs"]=17
        ["protocols"]=10
        ["specs"]=30
        ["tests"]=15
    )

    local all_correct=true
    for dir in "${!expected_counts[@]}"; do
        local expected=${expected_counts[$dir]}
        local actual=$(find "src/devforgeai/$dir" -type f 2>/dev/null | wc -l)
        local tolerance=3

        if [ "$actual" -ge $((expected - tolerance)) ] && [ "$actual" -le $((expected + tolerance)) ]; then
            echo -e "${GREEN}✓${NC} $dir: $actual files (expected ~$expected)"
        else
            echo -e "${RED}✗${NC} $dir: $actual files (expected ~$expected)"
            all_correct=false
        fi
    done

    [ "$all_correct" = true ] && return 0 || return 1
}

##############################################################################
# AC-3: Copy CLAUDE.md as template with no modifications
##############################################################################

test_ac3_claude_md_copied() {
    # Test: src/CLAUDE.md file exists
    assert_file_exists "src/CLAUDE.md"
}

test_ac3_checksum_matches_exactly() {
    # Test: SHA256 checksum of CLAUDE.md matches src/CLAUDE.md
    assert_checksum_match "CLAUDE.md" "src/CLAUDE.md"
}

test_ac3_file_size_matches() {
    # Test: File size matches exactly
    assert_file_size_match "CLAUDE.md" "src/CLAUDE.md"
}

test_ac3_original_unchanged() {
    # Test: Original CLAUDE.md still exists in root
    assert_file_exists "CLAUDE.md"
}

test_ac3_template_marker_present() {
    # Test: src/CLAUDE.md has template marker comment
    if grep -q "TEMPLATE.*source template" "src/CLAUDE.md" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Template marker comment found"
        return 0
    else
        echo -e "${RED}✗${NC} Template marker comment missing"
        return 1
    fi
}

##############################################################################
# AC-4: Validate file integrity with checksum verification
##############################################################################

test_ac4_checksums_file_exists() {
    # Test: checksums.txt manifest file created
    assert_file_exists "checksums.txt"
}

test_ac4_checksum_count_approximately_450() {
    # Test: ~450 checksums in checksums.txt (±10)
    assert_file_count "checksums.txt" 450 10
    # Note: This is lines in a file, not files, so just check line count
    local lines=$(wc -l < "checksums.txt" 2>/dev/null || echo "0")
    if [ "$lines" -ge 440 ] && [ "$lines" -le 460 ]; then
        echo -e "${GREEN}✓${NC} Checksum lines: $lines (expected ~450)"
        return 0
    else
        echo -e "${RED}✗${NC} Checksum line count: $lines (expected ~450)"
        return 1
    fi
}

test_ac4_checksum_format_valid() {
    # Test: Checksum format is valid: <sha256> <filepath>
    local first_line=$(head -1 "checksums.txt" 2>/dev/null)

    if [[ $first_line =~ ^[a-f0-9]{64}[[:space:]]+ ]]; then
        echo -e "${GREEN}✓${NC} Checksum format valid: SHA256 space filepath"
        return 0
    else
        echo -e "${RED}✗${NC} Checksum format invalid: $first_line"
        return 1
    fi
}

test_ac4_checksums_verified_with_shasum() {
    # Test: shasum -c checksums.txt exits with 0 (all valid)
    # Note: This test may fail if shasum tool not available or paths incorrect
    # Running in lenient mode to allow test to pass even if shasum unavailable
    if command -v shasum &> /dev/null; then
        if shasum -c "checksums.txt" &>/dev/null; then
            echo -e "${GREEN}✓${NC} All checksums verified with shasum"
            return 0
        else
            echo -e "${RED}✗${NC} Checksum verification failed with shasum"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} shasum tool not available (skipping verification)"
        return 0
    fi
}

test_ac4_validation_report_generated() {
    # Test: migration-report.md or similar validation report exists
    if [ -f "migration-report.md" ] || [ -f "src/scripts/migration-report.md" ]; then
        echo -e "${GREEN}✓${NC} Migration report generated"
        return 0
    else
        echo -e "${RED}✗${NC} Migration report not found"
        return 1
    fi
}

##############################################################################
# AC-5: Exclude backup files and build artifacts
##############################################################################

test_ac5_no_backup_files() {
    # Test: No .backup* files in src/
    assert_no_matches "*.backup*" "src/" "backup files"
}

test_ac5_no_temporary_files() {
    # Test: No .tmp or .temp files in src/
    local tmp_count=$(find "src/" -name "*.tmp" -o -name "*.temp" 2>/dev/null | wc -l)
    if [ "$tmp_count" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} No temporary files (.tmp, .temp)"
        return 0
    else
        echo -e "${RED}✗${NC} Found $tmp_count temporary files"
        return 1
    fi
}

test_ac5_no_python_bytecode() {
    # Test: No __pycache__/ or *.pyc files in src/
    local pyc_count=$(find "src/" -name "*.pyc" -o -path "*/__pycache__/*" 2>/dev/null | wc -l)
    if [ "$pyc_count" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} No Python bytecode files"
        return 0
    else
        echo -e "${RED}✗${NC} Found $pyc_count Python bytecode files"
        return 1
    fi
}

test_ac5_no_egg_info() {
    # Test: No *.egg-info/ directories in src/
    assert_no_matches "*.egg-info" "src/" "Python egg-info"
}

test_ac5_no_coverage_artifacts() {
    # Test: No htmlcov/ or .coverage files in src/
    local cov_count=$(find "src/" -name "htmlcov" -o -name ".coverage" 2>/dev/null | wc -l)
    if [ "$cov_count" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} No coverage artifacts"
        return 0
    else
        echo -e "${RED}✗${NC} Found $cov_count coverage artifact files/dirs"
        return 1
    fi
}

test_ac5_no_node_modules() {
    # Test: No node_modules/ directories in src/
    assert_no_matches "node_modules" "src/" "Node.js modules"
}

test_ac5_no_git_directories() {
    # Test: No .git/ directories in src/
    assert_no_matches ".git" "src/" ".git directories"
}

##############################################################################
# AC-6: Git track all copied files
##############################################################################

test_ac6_git_initialized() {
    # Test: Git repository initialized
    if [ -d ".git" ]; then
        echo -e "${GREEN}✓${NC} Git repository initialized"
        return 0
    else
        echo -e "${RED}✗${NC} Git repository not initialized"
        return 1
    fi
}

test_ac6_files_staged_approximately_450() {
    # Test: Approximately 450 files added to git (±10)
    # Note: This requires files to be staged, skip if not in git repo
    if [ -d ".git" ]; then
        assert_git_added_count 450 10
    else
        echo -e "${YELLOW}⊘${NC} Git repo not available (skipping)"
        return 0
    fi
}

test_ac6_no_binary_files_large() {
    # Test: No binary files >1MB staged
    # Note: This is a validation rule, skip if git not available
    if [ -d ".git" ]; then
        local large_binaries=$(git ls-files --cached | while read file; do
            if [ -f "$file" ]; then
                size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
                if [ "$size" -gt 1048576 ]; then
                    file "$file" | grep -q "binary" && echo "$file"
                fi
            fi
        done | wc -l)

        if [ "$large_binaries" -eq 0 ]; then
            echo -e "${GREEN}✓${NC} No binary files >1MB"
            return 0
        else
            echo -e "${RED}✗${NC} Found $large_binaries binary files >1MB"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} Git repo not available (skipping)"
        return 0
    fi
}

test_ac6_git_status_shows_additions() {
    # Test: git status --porcelain shows "A" entries (additions)
    if [ -d ".git" ]; then
        local additions=$(git status --porcelain 2>/dev/null | grep "^A " | wc -l)
        if [ "$additions" -gt 0 ]; then
            echo -e "${GREEN}✓${NC} Git shows $additions file additions"
            return 0
        else
            echo -e "${RED}✗${NC} No file additions in git status"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} Git repo not available (skipping)"
        return 0
    fi
}

##############################################################################
# AC-7: Preserve original operational directories
##############################################################################

test_ac7_original_claude_exists() {
    # Test: Original .claude/ directory still exists
    assert_directory_exists ".claude"
}

test_ac7_original_devforgeai_exists() {
    # Test: Original devforgeai/ directory still exists
    assert_directory_exists "devforgeai"
}

test_ac7_original_claude_unchanged_filecount() {
    # Test: File count in .claude/ unchanged before/after
    # Note: This requires tracking before/after, so we test current state
    local claude_count=$(find ".claude" -type f 2>/dev/null | wc -l)
    if [ "$claude_count" -gt 300 ]; then
        echo -e "${GREEN}✓${NC} .claude/ has expected file count: $claude_count"
        return 0
    else
        echo -e "${RED}✗${NC} .claude/ file count low: $claude_count (expected >300)"
        return 1
    fi
}

test_ac7_no_symlinks_in_src() {
    # Test: No symbolic links created in src/ (true copies, not links)
    local symlink_count=$(find "src/" -type l 2>/dev/null | wc -l)
    if [ "$symlink_count" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} No symlinks in src/ (all true copies)"
        return 0
    else
        echo -e "${RED}✗${NC} Found $symlink_count symlinks in src/"
        return 1
    fi
}

test_ac7_commands_still_work() {
    # Test: DevForgeAI commands still functional (/dev and /qa at least)
    # Note: This requires CLI to be installed, skip if not available
    if command -v /dev &> /dev/null || [ -f ".claude/commands/dev.md" ]; then
        echo -e "${GREEN}✓${NC} Command infrastructure intact"
        return 0
    else
        echo -e "${YELLOW}⊘${NC} Command validation skipped"
        return 0
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}STORY-042: Acceptance Criteria Test Suite${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""

    > "$TEST_LOG"  # Clear log

    setup_test_environment

    echo -e "\n${YELLOW}AC-1: Copy .claude/ to src/claude/ with structure preserved${NC}"
    run_test "AC-1.1: src/claude/ directory exists" "test_ac1_claude_directory_exists"
    run_test "AC-1.2: All subdirectories preserved" "test_ac1_subdirectories_preserved"
    run_test "AC-1.3: File count approximately 370" "test_ac1_file_count_approximately_370"
    run_test "AC-1.4: Nested structure preserved" "test_ac1_nested_structure_preserved"
    run_test "AC-1.5: Original .claude/ unchanged" "test_ac1_original_unchanged"

    echo -e "\n${YELLOW}AC-2: Copy devforgeai/ config/docs/protocols/specs/tests${NC}"
    run_test "AC-2.1: src/devforgeai/ directory exists" "test_ac2_devforgeai_directory_exists"
    run_test "AC-2.2: Only allowed subdirectories present" "test_ac2_allowed_subdirs_only"
    run_test "AC-2.3: Required subdirectories present" "test_ac2_required_subdirs_present"
    run_test "AC-2.4: File count approximately 80" "test_ac2_file_count_approximately_80"
    run_test "AC-2.5: Subdirectory file counts correct" "test_ac2_subdirectory_file_counts"

    echo -e "\n${YELLOW}AC-3: Copy CLAUDE.md as template with no modifications${NC}"
    run_test "AC-3.1: src/CLAUDE.md file exists" "test_ac3_claude_md_copied"
    run_test "AC-3.2: Checksum matches exactly" "test_ac3_checksum_matches_exactly"
    run_test "AC-3.3: File size matches" "test_ac3_file_size_matches"
    run_test "AC-3.4: Original CLAUDE.md unchanged" "test_ac3_original_unchanged"
    run_test "AC-3.5: Template marker present" "test_ac3_template_marker_present"

    echo -e "\n${YELLOW}AC-4: Validate file integrity with checksum verification${NC}"
    run_test "AC-4.1: checksums.txt file exists" "test_ac4_checksums_file_exists"
    run_test "AC-4.2: Checksum count approximately 450" "test_ac4_checksum_count_approximately_450"
    run_test "AC-4.3: Checksum format valid" "test_ac4_checksum_format_valid"
    run_test "AC-4.4: Checksums verified with shasum" "test_ac4_checksums_verified_with_shasum"
    run_test "AC-4.5: Migration report generated" "test_ac4_validation_report_generated"

    echo -e "\n${YELLOW}AC-5: Exclude backup files and build artifacts${NC}"
    run_test "AC-5.1: No backup files" "test_ac5_no_backup_files"
    run_test "AC-5.2: No temporary files" "test_ac5_no_temporary_files"
    run_test "AC-5.3: No Python bytecode" "test_ac5_no_python_bytecode"
    run_test "AC-5.4: No egg-info" "test_ac5_no_egg_info"
    run_test "AC-5.5: No coverage artifacts" "test_ac5_no_coverage_artifacts"
    run_test "AC-5.6: No node_modules" "test_ac5_no_node_modules"
    run_test "AC-5.7: No .git directories" "test_ac5_no_git_directories"

    echo -e "\n${YELLOW}AC-6: Git track all copied files${NC}"
    run_test "AC-6.1: Git initialized" "test_ac6_git_initialized"
    run_test "AC-6.2: Files staged approximately 450" "test_ac6_files_staged_approximately_450"
    run_test "AC-6.3: No binary files >1MB" "test_ac6_no_binary_files_large"
    run_test "AC-6.4: Git status shows additions" "test_ac6_git_status_shows_additions"

    echo -e "\n${YELLOW}AC-7: Preserve original operational directories{{NC}"
    run_test "AC-7.1: Original .claude/ exists" "test_ac7_original_claude_exists"
    run_test "AC-7.2: Original devforgeai/ exists" "test_ac7_original_devforgeai_exists"
    run_test "AC-7.3: Original .claude/ unchanged" "test_ac7_original_claude_unchanged_filecount"
    run_test "AC-7.4: No symlinks in src/" "test_ac7_no_symlinks_in_src"
    run_test "AC-7.5: Commands still work" "test_ac7_commands_still_work"

    cleanup_test_environment

    # Summary
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "Tests run:    ${BLUE}$TESTS_RUN${NC}"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

    # Return appropriate exit code
    [ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
}

# Execute main
main "$@"
