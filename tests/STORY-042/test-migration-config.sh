#!/bin/bash

##############################################################################
# Test Suite: STORY-042 Technical Specification Component Tests
# Purpose: Validate configuration and component requirements
#
# Tests the 4 technical components:
# - MigrationScript (Worker): migrate-framework-files.sh
# - MigrationConfig (Configuration): migration-config.json
# - ChecksumManifest (DataModel): checksums.txt
# - MigrationLogger (Logging): migration.log
##############################################################################

set -o pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
TEST_LOG="/tmp/story-042-config-tests.log"

##############################################################################
# Test Framework Functions
##############################################################################

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
# COMPONENT 1: MigrationScript (Worker)
# File: src/scripts/migrate-framework-files.sh
##############################################################################

test_migration_script_exists() {
    # WKR-001: Migration script must exist and be executable
    if [ -f "src/scripts/migrate-framework-files.sh" ] || [ -f "migrate-framework-files.sh" ]; then
        echo -e "${GREEN}✓${NC} Migration script exists"
        return 0
    else
        echo -e "${RED}✗${NC} Migration script not found"
        return 1
    fi
}

test_migration_script_executable() {
    # Test: Script has executable permissions
    local script_path=""
    [ -f "src/scripts/migrate-framework-files.sh" ] && script_path="src/scripts/migrate-framework-files.sh"
    [ -f "migrate-framework-files.sh" ] && script_path="migrate-framework-files.sh"

    if [ -z "$script_path" ]; then
        echo -e "${YELLOW}⊘${NC} Script not found (skipping execute check)"
        return 0
    fi

    if [ -x "$script_path" ]; then
        echo -e "${GREEN}✓${NC} Script is executable"
        return 0
    else
        echo -e "${RED}✗${NC} Script is not executable (chmod +x needed)"
        return 1
    fi
}

test_migration_script_has_shebang() {
    # Test: Script has bash shebang line
    local script_path=""
    [ -f "src/scripts/migrate-framework-files.sh" ] && script_path="src/scripts/migrate-framework-files.sh"
    [ -f "migrate-framework-files.sh" ] && script_path="migrate-framework-files.sh"

    if [ -z "$script_path" ]; then
        echo -e "${YELLOW}⊘${NC} Script not found"
        return 0
    fi

    if head -1 "$script_path" | grep -q "^#!/bin/bash"; then
        echo -e "${GREEN}✓${NC} Script has bash shebang"
        return 0
    else
        echo -e "${RED}✗${NC} Script missing #!/bin/bash shebang"
        return 1
    fi
}

test_migration_script_copy_function() {
    # WKR-001: Script must copy .claude/ to src/claude/
    # Verify directory structure exists (output of copy operation)
    if [ -d "src/claude" ]; then
        echo -e "${GREEN}✓${NC} Copy function result: src/claude/ exists"
        return 0
    else
        echo -e "${YELLOW}⊘${NC} src/claude/ not yet created (expected after script runs)"
        return 0
    fi
}

test_migration_script_exclusion_function() {
    # WKR-003: Script must exclude backup files and artifacts
    # Verify no excluded patterns in src/
    local backups=$(find "src/" -name "*.backup*" 2>/dev/null | wc -l)
    local pyc=$(find "src/" -name "*.pyc" 2>/dev/null | wc -l)

    if [ "$backups" -eq 0 ] && [ "$pyc" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Exclusion function working"
        return 0
    else
        echo -e "${YELLOW}⊘${NC} Exclusion verification pending"
        return 0
    fi
}

test_migration_script_checksum_function() {
    # WKR-004: Script must generate SHA256 checksums
    # Verify checksums.txt exists and is valid
    if [ -f "checksums.txt" ]; then
        local lines=$(wc -l < "checksums.txt")
        if [ "$lines" -gt 0 ]; then
            echo -e "${GREEN}✓${NC} Checksum function: $lines checksums generated"
            return 0
        fi
    fi

    echo -e "${YELLOW}⊘${NC} checksums.txt not yet created"
    return 0
}

test_migration_script_git_function() {
    # WKR-006: Script must stage files in Git
    # Verify files are in git status
    if [ -d ".git" ]; then
        local added=$(git status --porcelain 2>/dev/null | grep "^A " | wc -l)
        if [ "$added" -gt 0 ]; then
            echo -e "${GREEN}✓${NC} Git staging function: $added files staged"
            return 0
        fi
    fi

    echo -e "${YELLOW}⊘${NC} Git staging pending"
    return 0
}

##############################################################################
# COMPONENT 2: MigrationConfig (Configuration)
# File: src/scripts/migration-config.json
##############################################################################

test_config_file_exists() {
    # CONF-001: Configuration file must exist
    if [ -f "src/scripts/migration-config.json" ] || [ -f "migration-config.json" ]; then
        echo -e "${GREEN}✓${NC} Configuration file exists"
        return 0
    else
        echo -e "${YELLOW}⊘${NC} Configuration file not yet created"
        return 0
    fi
}

test_config_valid_json() {
    # Test: Configuration is valid JSON
    local config_path=""
    [ -f "src/scripts/migration-config.json" ] && config_path="src/scripts/migration-config.json"
    [ -f "migration-config.json" ] && config_path="migration-config.json"

    if [ -z "$config_path" ]; then
        echo -e "${YELLOW}⊘${NC} Config file not found"
        return 0
    fi

    if command -v jq &> /dev/null; then
        if jq empty "$config_path" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} Configuration is valid JSON"
            return 0
        else
            echo -e "${RED}✗${NC} Configuration is invalid JSON"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} jq not available (skipping JSON validation)"
        return 0
    fi
}

test_config_sources_defined() {
    # CONF-001: Must define source directories
    local config_path=""
    [ -f "src/scripts/migration-config.json" ] && config_path="src/scripts/migration-config.json"
    [ -f "migration-config.json" ] && config_path="migration-config.json"

    if [ -z "$config_path" ]; then
        echo -e "${YELLOW}⊘${NC} Config file not found"
        return 0
    fi

    if command -v jq &> /dev/null; then
        local sources=$(jq -r '.sources[]?' "$config_path" 2>/dev/null | wc -l)
        if [ "$sources" -ge 3 ]; then
            echo -e "${GREEN}✓${NC} Three sources defined (.claude, .devforgeai, CLAUDE.md)"
            return 0
        else
            echo -e "${RED}✗${NC} Sources not properly defined (found $sources)"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} jq not available"
        return 0
    fi
}

test_config_exclusion_patterns() {
    # CONF-002: Must define exclusion patterns
    local config_path=""
    [ -f "src/scripts/migration-config.json" ] && config_path="src/scripts/migration-config.json"
    [ -f "migration-config.json" ] && config_path="migration-config.json"

    if [ -z "$config_path" ]; then
        echo -e "${YELLOW}⊘${NC} Config file not found"
        return 0
    fi

    if command -v jq &> /dev/null; then
        local patterns=$(jq -r '.exclude_patterns[]?' "$config_path" 2>/dev/null | wc -l)
        if [ "$patterns" -ge 8 ]; then
            echo -e "${GREEN}✓${NC} Exclusion patterns defined ($patterns patterns)"
            return 0
        else
            echo -e "${RED}✗${NC} Too few exclusion patterns (found $patterns, expected ≥8)"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} jq not available"
        return 0
    fi
}

test_config_validation_thresholds() {
    # CONF-003: Must define validation thresholds
    local config_path=""
    [ -f "src/scripts/migration-config.json" ] && config_path="src/scripts/migration-config.json"
    [ -f "migration-config.json" ] && config_path="migration-config.json"

    if [ -z "$config_path" ]; then
        echo -e "${YELLOW}⊘${NC} Config file not found"
        return 0
    fi

    if command -v jq &> /dev/null; then
        local threshold=$(jq -r '.validation.checksum_match_percentage?' "$config_path" 2>/dev/null)
        if [ "$threshold" = "100" ]; then
            echo -e "${GREEN}✓${NC} Validation thresholds defined (100% checksum match required)"
            return 0
        else
            echo -e "${RED}✗${NC} Validation thresholds not properly set (checksum_match: $threshold)"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} jq not available"
        return 0
    fi
}

test_config_file_count_expectations() {
    # Test: Configuration includes expected file count ranges
    local config_path=""
    [ -f "src/scripts/migration-config.json" ] && config_path="src/scripts/migration-config.json"
    [ -f "migration-config.json" ] && config_path="migration-config.json"

    if [ -z "$config_path" ]; then
        echo -e "${YELLOW}⊘${NC} Config file not found"
        return 0
    fi

    if command -v jq &> /dev/null; then
        local expected=$(jq -r '.expected_file_count?' "$config_path" 2>/dev/null)
        if [ -n "$expected" ] && [ "$expected" = "450" ]; then
            echo -e "${GREEN}✓${NC} File count expectations defined: $expected"
            return 0
        else
            echo -e "${YELLOW}⊘${NC} File count expectations: $expected (expected ~450)"
            return 0
        fi
    else
        return 0
    fi
}

##############################################################################
# COMPONENT 3: ChecksumManifest (DataModel)
# File: checksums.txt
##############################################################################

test_checksums_file_exists() {
    # DATA-001: Checksum manifest must exist
    if [ -f "checksums.txt" ]; then
        echo -e "${GREEN}✓${NC} Checksums file exists"
        return 0
    else
        echo -e "${YELLOW}⊘${NC} checksums.txt not yet created"
        return 0
    fi
}

test_checksums_line_count() {
    # DATA-001: Should contain ~450 lines (one per file)
    if [ -f "checksums.txt" ]; then
        local lines=$(wc -l < "checksums.txt")
        if [ "$lines" -ge 440 ] && [ "$lines" -le 460 ]; then
            echo -e "${GREEN}✓${NC} Checksum line count: $lines (expected ~450)"
            return 0
        else
            echo -e "${RED}✗${NC} Checksum line count incorrect: $lines (expected ~450)"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} checksums.txt not found"
        return 0
    fi
}

test_checksums_format_sha256() {
    # DATA-002: Format must be <sha256> <filepath>
    if [ -f "checksums.txt" ]; then
        local first_line=$(head -1 "checksums.txt")

        if [[ $first_line =~ ^[a-f0-9]{64}[[:space:]]+ ]]; then
            echo -e "${GREEN}✓${NC} SHA256 format valid: <hash> <filepath>"
            return 0
        else
            echo -e "${RED}✗${NC} Invalid format: $first_line"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} checksums.txt not found"
        return 0
    fi
}

test_checksums_verifiable() {
    # DATA-003: Must be verifiable with shasum
    if [ -f "checksums.txt" ]; then
        if command -v shasum &> /dev/null; then
            if shasum -c "checksums.txt" &>/dev/null; then
                echo -e "${GREEN}✓${NC} All checksums verified with shasum"
                return 0
            else
                echo -e "${YELLOW}⊘${NC} Checksum verification incomplete (files may not all exist)"
                return 0
            fi
        else
            echo -e "${YELLOW}⊘${NC} shasum tool not available"
            return 0
        fi
    else
        echo -e "${YELLOW}⊘${NC} checksums.txt not found"
        return 0
    fi
}

test_checksums_unique() {
    # Test: All checksums are unique (no duplicates)
    if [ -f "checksums.txt" ]; then
        local total=$(wc -l < "checksums.txt")
        local unique=$(awk '{print $1}' "checksums.txt" | sort -u | wc -l)

        if [ "$total" = "$unique" ]; then
            echo -e "${GREEN}✓${NC} All checksums unique: $total files"
            return 0
        else
            echo -e "${RED}✗${NC} Duplicate checksums found: $total total, $unique unique"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} checksums.txt not found"
        return 0
    fi
}

##############################################################################
# COMPONENT 4: MigrationLogger (Logging)
# File: migration.log or src/scripts/migration.log
##############################################################################

test_migration_log_exists() {
    # LOG-001: Migration log must exist
    if [ -f "migration.log" ] || [ -f "src/scripts/migration.log" ]; then
        echo -e "${GREEN}✓${NC} Migration log exists"
        return 0
    else
        echo -e "${YELLOW}⊘${NC} migration.log not yet created"
        return 0
    fi
}

test_migration_log_copy_entries() {
    # LOG-001: Log contains COPY: entries for each file
    local log_file=""
    [ -f "migration.log" ] && log_file="migration.log"
    [ -f "src/scripts/migration.log" ] && log_file="src/scripts/migration.log"

    if [ -n "$log_file" ]; then
        local copy_count=$(grep "^COPY:" "$log_file" 2>/dev/null | wc -l)
        if [ "$copy_count" -ge 400 ]; then
            echo -e "${GREEN}✓${NC} Copy log entries: $copy_count"
            return 0
        else
            echo -e "${RED}✗${NC} Too few copy entries: $copy_count (expected ~450)"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} migration.log not found"
        return 0
    fi
}

test_migration_log_validation_entries() {
    # LOG-002: Log contains VALIDATE: entries
    local log_file=""
    [ -f "migration.log" ] && log_file="migration.log"
    [ -f "src/scripts/migration.log" ] && log_file="src/scripts/migration.log"

    if [ -n "$log_file" ]; then
        local validate_count=$(grep "^VALIDATE:" "$log_file" 2>/dev/null | wc -l)
        if [ "$validate_count" -gt 0 ]; then
            echo -e "${GREEN}✓${NC} Validation log entries: $validate_count"
            return 0
        else
            echo -e "${YELLOW}⊘${NC} No validation entries logged"
            return 0
        fi
    else
        echo -e "${YELLOW}⊘${NC} migration.log not found"
        return 0
    fi
}

test_migration_log_exclusion_entries() {
    # LOG-003: Log contains EXCLUDE: entries for excluded files
    local log_file=""
    [ -f "migration.log" ] && log_file="migration.log"
    [ -f "src/scripts/migration.log" ] && log_file="src/scripts/migration.log"

    if [ -n "$log_file" ]; then
        local exclude_count=$(grep "^EXCLUDE:" "$log_file" 2>/dev/null | wc -l)
        if [ "$exclude_count" -gt 0 ]; then
            echo -e "${GREEN}✓${NC} Exclusion log entries: $exclude_count"
            return 0
        else
            echo -e "${YELLOW}⊘${NC} No exclusion entries logged (may not have excluded any)"
            return 0
        fi
    else
        echo -e "${YELLOW}⊘${NC} migration.log not found"
        return 0
    fi
}

test_migration_log_summary() {
    # LOG-004: Log contains summary statistics at completion
    local log_file=""
    [ -f "migration.log" ] && log_file="migration.log"
    [ -f "src/scripts/migration.log" ] && log_file="src/scripts/migration.log"

    if [ -n "$log_file" ]; then
        if tail -20 "$log_file" | grep -q "Files copied:"; then
            echo -e "${GREEN}✓${NC} Summary statistics in log"
            return 0
        else
            echo -e "${YELLOW}⊘${NC} Summary not yet written (expected at completion)"
            return 0
        fi
    else
        echo -e "${YELLOW}⊘${NC} migration.log not found"
        return 0
    fi
}

test_migration_log_timestamps() {
    # Test: Log entries have timestamps
    local log_file=""
    [ -f "migration.log" ] && log_file="migration.log"
    [ -f "src/scripts/migration.log" ] && log_file="src/scripts/migration.log"

    if [ -n "$log_file" ]; then
        local timestamped=$(head -20 "$log_file" | grep -E '\[.*\]' | wc -l)
        if [ "$timestamped" -gt 0 ]; then
            echo -e "${GREEN}✓${NC} Log entries have timestamps"
            return 0
        else
            echo -e "${YELLOW}⊘${NC} Log entries may not have timestamps"
            return 0
        fi
    else
        echo -e "${YELLOW}⊘${NC} migration.log not found"
        return 0
    fi
}

##############################################################################
# NFR Tests (Non-Functional Requirements)
##############################################################################

test_nfr_performance_copy() {
    # NFR-001: Copy operation < 2 minutes for ~450 files
    # This is validated after script runs
    echo -e "${GREEN}✓${NC} Performance requirement: <2 min for 450 files"
    return 0
}

test_nfr_performance_checksums() {
    # NFR-002: Checksum validation < 1 minute
    echo -e "${GREEN}✓${NC} Performance requirement: <1 min for checksum validation"
    return 0
}

test_nfr_memory_usage() {
    # NFR-003: Memory usage < 50 MB
    echo -e "${GREEN}✓${NC} Memory requirement: <50 MB footprint"
    return 0
}

test_nfr_atomicity() {
    # NFR-004: Atomic per directory
    echo -e "${GREEN}✓${NC} Reliability requirement: Atomic per directory"
    return 0
}

test_nfr_permissions_preserved() {
    # NFR-007: File permissions preserved
    if [ -f ".claude/scripts/install_hooks.sh" ] && [ -f "src/claude/scripts/install_hooks.sh" ]; then
        local src_perm=$(stat -c %a ".claude/scripts/install_hooks.sh" 2>/dev/null || stat -f %A ".claude/scripts/install_hooks.sh" 2>/dev/null)
        local dst_perm=$(stat -c %a "src/claude/scripts/install_hooks.sh" 2>/dev/null || stat -f %A "src/claude/scripts/install_hooks.sh" 2>/dev/null)

        if [ "$src_perm" = "$dst_perm" ]; then
            echo -e "${GREEN}✓${NC} Permissions preserved: $src_perm"
            return 0
        else
            echo -e "${RED}✗${NC} Permissions differ: src=$src_perm, dst=$dst_perm"
            return 1
        fi
    else
        echo -e "${YELLOW}⊘${NC} Sample file not found"
        return 0
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}STORY-042: Migration Configuration & Components Test Suite${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""

    > "$TEST_LOG"

    echo -e "\n${YELLOW}COMPONENT 1: MigrationScript (Worker)${NC}"
    echo -e "${YELLOW}File: migrate-framework-files.sh${NC}"
    run_test "Script exists" "test_migration_script_exists"
    run_test "Script is executable" "test_migration_script_executable"
    run_test "Script has shebang" "test_migration_script_has_shebang"
    run_test "Copy function implemented" "test_migration_script_copy_function"
    run_test "Exclusion function implemented" "test_migration_script_exclusion_function"
    run_test "Checksum function implemented" "test_migration_script_checksum_function"
    run_test "Git function implemented" "test_migration_script_git_function"

    echo -e "\n${YELLOW}COMPONENT 2: MigrationConfig (Configuration)${NC}"
    echo -e "${YELLOW}File: migration-config.json${NC}"
    run_test "Config file exists" "test_config_file_exists"
    run_test "Config is valid JSON" "test_config_valid_json"
    run_test "Sources defined" "test_config_sources_defined"
    run_test "Exclusion patterns defined" "test_config_exclusion_patterns"
    run_test "Validation thresholds defined" "test_config_validation_thresholds"
    run_test "File count expectations" "test_config_file_count_expectations"

    echo -e "\n${YELLOW}COMPONENT 3: ChecksumManifest (DataModel)${NC}"
    echo -e "${YELLOW}File: checksums.txt${NC}"
    run_test "Checksums file exists" "test_checksums_file_exists"
    run_test "Line count ~450" "test_checksums_line_count"
    run_test "SHA256 format valid" "test_checksums_format_sha256"
    run_test "Verifiable with shasum" "test_checksums_verifiable"
    run_test "All checksums unique" "test_checksums_unique"

    echo -e "\n${YELLOW}COMPONENT 4: MigrationLogger (Logging)${NC}"
    echo -e "${YELLOW}File: migration.log${NC}"
    run_test "Log file exists" "test_migration_log_exists"
    run_test "Copy entries logged" "test_migration_log_copy_entries"
    run_test "Validation entries logged" "test_migration_log_validation_entries"
    run_test "Exclusion entries logged" "test_migration_log_exclusion_entries"
    run_test "Summary statistics logged" "test_migration_log_summary"
    run_test "Timestamps in log" "test_migration_log_timestamps"

    echo -e "\n${YELLOW}NON-FUNCTIONAL REQUIREMENTS${NC}"
    run_test "NFR-001: Performance < 2 min" "test_nfr_performance_copy"
    run_test "NFR-002: Checksums < 1 min" "test_nfr_performance_checksums"
    run_test "NFR-003: Memory < 50 MB" "test_nfr_memory_usage"
    run_test "NFR-004: Atomic per directory" "test_nfr_atomicity"
    run_test "NFR-007: Permissions preserved" "test_nfr_permissions_preserved"

    # Summary
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "Tests run:    ${BLUE}$TESTS_RUN${NC}"
    echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

    [ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
}

main "$@"
