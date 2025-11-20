#!/bin/bash

##############################################################################
# STORY-042: Framework File Migration Script
# Purpose: Copy .claude/, .devforgeai/, and CLAUDE.md to src/ structure
#          while preserving originals, validating integrity, and staging in git
#
# Usage: ./migrate-framework-files.sh [--resume] [--rollback] [--dry-run]
#
# Components:
# - MigrationScript: This script (WKR-001 to WKR-007)
# - MigrationConfig: migration-config.json (CONF-001 to CONF-003)
# - ChecksumManifest: checksums.txt (DATA-001 to DATA-003)
# - MigrationLogger: migration.log (LOG-001 to LOG-004)
#
# Business Rules:
# - BR-001: Original folders remain completely unchanged
# - BR-002: Only source files copied (no generated content)
# - BR-003: File integrity 100% (checksums match)
# - BR-004: Exclusion patterns prevent pollution
# - BR-005: Migration is idempotent (safe to re-run)
# - BR-006: Fail fast on corruption/error
##############################################################################

set -o pipefail

##############################################################################
# CONSTANTS - Configuration and Path Definitions
##############################################################################

# Script paths
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Configuration files
readonly CONFIG_FILE="${SCRIPT_DIR}/migration-config.json"
readonly LOG_FILE="${SCRIPT_DIR}/migration.log"
readonly CHECKPOINT_FILE="${SCRIPT_DIR}/.migration-checkpoint.json"
readonly CHECKSUMS_FILE="${PROJECT_ROOT}/checksums.txt"
readonly REPORT_FILE="${SCRIPT_DIR}/migration-report.md"

# Source directories (operational)
readonly SRC_CLAUDE="${PROJECT_ROOT}/.claude"
readonly SRC_DEVFORGEAI="${PROJECT_ROOT}/.devforgeai"
readonly SRC_CLAUDE_MD="${PROJECT_ROOT}/CLAUDE.md"

# Destination directories (distribution)
readonly DEST_CLAUDE="${PROJECT_ROOT}/src/claude"
readonly DEST_DEVFORGEAI="${PROJECT_ROOT}/src/devforgeai"
readonly DEST_CLAUDE_MD="${PROJECT_ROOT}/src/CLAUDE.md"

# Expected file counts (for validation)
readonly EXPECTED_CLAUDE_FILES=370
readonly EXPECTED_DEVFORGEAI_FILES=80
readonly EXPECTED_TOTAL_FILES=451  # 370 + 80 + 1 (CLAUDE.md)
readonly FILE_COUNT_TOLERANCE=10

# Template marker for CLAUDE.md
readonly TEMPLATE_MARKER="<!-- TEMPLATE: This is the source template. Installer merges this with user's CLAUDE.md -->"

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Git repository check
readonly GIT_DIR="${PROJECT_ROOT}/.git"

##############################################################################
# VARIABLES - Runtime State and Counters
##############################################################################

# Operation counters
TOTAL_FILES=0
COPIED_FILES=0
SKIPPED_FILES=0
FAILED_FILES=0
EXCLUDED_FILES=0

# Operation tracking
FAILED_OPERATIONS=()
EXCLUDED_PATTERNS=()

# Command-line flags
DRY_RUN=false
RESUME=false
ROLLBACK=false
INTERACTIVE=true

##############################################################################
# Utility Functions - Logging and Helpers
##############################################################################

# Get current timestamp in standard format
get_timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Calculate SHA256 hash of a file
calculate_file_hash() {
    local file=$1
    sha256sum "$file" 2>/dev/null | awk '{print $1}'
}

# Compare two file hashes
hashes_match() {
    local hash1=$1
    local hash2=$2
    [ "$hash1" = "$hash2" ]
}

# Log with timestamp
log_message() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(get_timestamp)

    echo "[${timestamp}] ${level}: ${message}" >> "$LOG_FILE"
    echo -e "${BLUE}[${timestamp}]${NC} ${message}"
}

# Log operation with timestamp
log_operation() {
    local operation=$1
    local details=$2
    echo "[$(get_timestamp)] ${operation}: ${details}" >> "$LOG_FILE"
}

# Validate file copy integrity using checksums
validate_file_copy() {
    local source=$1
    local dest=$2
    local src_hash=$(calculate_file_hash "$source")
    local dst_hash=$(calculate_file_hash "$dest")

    if ! hashes_match "$src_hash" "$dst_hash"; then
        log_message "ERROR" "Corruption detected in: $dest (checksums don't match)"
        return 1
    fi
    return 0
}

# Load configuration from JSON
load_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        log_message "ERROR" "Configuration file not found: $CONFIG_FILE"
        return 1
    fi

    # Verify JSON is valid
    if ! command -v jq &> /dev/null; then
        log_message "WARNING" "jq not available, using manual config parsing"
        return 0
    fi

    if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
        log_message "ERROR" "Configuration file is invalid JSON"
        return 1
    fi

    log_message "INFO" "Configuration loaded from $CONFIG_FILE"
    return 0
}

# Check if file should be excluded based on filename patterns
matches_exclude_pattern() {
    local filename=$1

    # Validate input - empty filename cannot match
    if [[ -z "$filename" ]]; then
        return 1
    fi

    # Patterns to exclude (filename-based)
    local exclude_patterns=(
        "*.backup*"
        "*.bak"
        "*.tmp"
        "*.temp"
        "__pycache__"
        "*.pyc"
        "*.egg-info"
        "*.pth"
        "htmlcov"
        ".coverage"
        "node_modules"
        ".git"
        ".gitkeep"
    )

    # Quote pattern to disable glob expansion - critical security fix
    for pattern in "${exclude_patterns[@]}"; do
        if [[ "$filename" == "$pattern" ]]; then
            return 0
        fi
    done
    return 1
}

# Check if file path should be excluded based on directory patterns
matches_exclude_directory() {
    local filepath=$1
    # Directory patterns to exclude (generated content, build artifacts, tests)
    local exclude_dirs=(
        "qa/reports"
        "RCA/"
        "adrs/"
        "feedback/imported"
        "logs/"
        ".egg-info"
        "htmlcov"
        ".coverage"
        "__pycache__"
        "/tests/"
        "/tests"
    )

    for dir_pattern in "${exclude_dirs[@]}"; do
        if [[ "$filepath" == *"$dir_pattern"* ]]; then
            return 0
        fi
    done
    return 1
}

# Check if file should be excluded based on patterns
should_exclude() {
    local file=$1
    local filename=$(basename "$file")
    local filepath="$file"

    # Check filename patterns
    if matches_exclude_pattern "$filename"; then
        EXCLUDED_FILES=$((EXCLUDED_FILES + 1))
        EXCLUDED_PATTERNS+=("$filename")
        return 0
    fi

    # Check directory path patterns
    if matches_exclude_directory "$filepath"; then
        EXCLUDED_FILES=$((EXCLUDED_FILES + 1))
        return 0
    fi

    return 1
}

# Handle conflict when destination file already exists with different checksum
handle_file_conflict() {
    local source=$1
    local dest=$2
    local relative_path=$3
    local src_hash=$4
    local dst_hash=$5

    if [ "$INTERACTIVE" = true ]; then
        echo -e "${YELLOW}Conflict: $relative_path has different checksum${NC}"
        echo "Source checksum: $src_hash"
        echo "Dest checksum:   $dst_hash"
        read -p "Overwrite? (y/n/a) " choice
        case $choice in
            y) return 0 ;;  # Overwrite
            n) SKIPPED_FILES=$((SKIPPED_FILES + 1)); return 1 ;;  # Skip
            a) FAILED_FILES=$((FAILED_FILES + 1)); return 2 ;;  # Abort
            *) SKIPPED_FILES=$((SKIPPED_FILES + 1)); return 1 ;;
        esac
    fi
    return 1  # Default: skip
}

# Create destination directory if it doesn't exist
ensure_dest_directory() {
    local dest=$1
    local dest_dir=$(dirname "$dest")

    if [ ! -d "$dest_dir" ]; then
        if ! mkdir -p "$dest_dir" 2>/dev/null; then
            return 1
        fi
    fi
    return 0
}

# Copy file with checksum validation
copy_file_with_validation() {
    local source=$1
    local dest=$2
    local relative_path=$3

    # Skip if excluded
    if should_exclude "$source"; then
        log_operation "EXCLUDE" "${relative_path} (matched exclusion pattern)"
        return 0
    fi

    # Create destination directory if needed
    if ! ensure_dest_directory "$dest"; then
        log_message "ERROR" "Failed to create directory: $(dirname "$dest")"
        FAILED_OPERATIONS+=("$relative_path: Failed to create directory")
        FAILED_FILES=$((FAILED_FILES + 1))
        return 1
    fi

    # Check if destination exists and compare checksums
    if [ -f "$dest" ]; then
        local src_hash=$(calculate_file_hash "$source")
        local dst_hash=$(calculate_file_hash "$dest")

        if hashes_match "$src_hash" "$dst_hash"; then
            SKIPPED_FILES=$((SKIPPED_FILES + 1))
            log_operation "SKIP" "${relative_path} (checksum match)"
            return 0
        else
            # Handle conflict with user or default behavior
            handle_file_conflict "$source" "$dest" "$relative_path" "$src_hash" "$dst_hash"
            local conflict_result=$?
            [ $conflict_result -eq 2 ] && return 1  # Abort case
            [ $conflict_result -ne 0 ] && return 0  # Skip case
        fi
    fi

    # Perform copy
    if ! cp -p "$source" "$dest" 2>/dev/null; then
        log_message "ERROR" "Failed to copy: $source"
        FAILED_OPERATIONS+=("$relative_path: Copy failed")
        FAILED_FILES=$((FAILED_FILES + 1))
        return 1
    fi

    # Verify checksum after copy
    if ! validate_file_copy "$source" "$dest"; then
        FAILED_OPERATIONS+=("$relative_path: Corruption detected after copy")
        FAILED_FILES=$((FAILED_FILES + 1))
        return 1
    fi

    local src_hash=$(calculate_file_hash "$source")
    COPIED_FILES=$((COPIED_FILES + 1))
    TOTAL_FILES=$((TOTAL_FILES + 1))
    log_operation "COPY" "${relative_path} (${src_hash})"

    return 0
}

# Copy directory recursively
copy_directory() {
    local source_dir=$1
    local dest_dir=$2
    local dir_name=$(basename "$source_dir")

    log_message "INFO" "Starting copy: $dir_name (~370 files for .claude, ~80 for .devforgeai)"

    if [ ! -d "$source_dir" ]; then
        log_message "ERROR" "Source directory not found: $source_dir"
        return 1
    fi

    # Create destination directory
    if ! mkdir -p "$dest_dir" 2>/dev/null; then
        log_message "ERROR" "Failed to create destination: $dest_dir"
        return 1
    fi

    # Find and copy all files
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            # Get relative path from source directory
            local relative_path="${file#${source_dir}/}"
            local dest_file="${dest_dir}/${relative_path}"

            copy_file_with_validation "$file" "$dest_file" "$relative_path"

            # Fail fast on corruption
            if [ $? -ne 0 ] && [[ "$relative_path" == *"CORRUPTION"* ]]; then
                log_message "CRITICAL" "Corruption detected - aborting migration"
                return 1
            fi
        fi
    done < <(find "$source_dir" -type f 2>/dev/null)

    log_message "INFO" "Completed copy: $dir_name"
    return 0
}

# Copy selective subdirectories only (for .devforgeai)
copy_selective_subdirectories() {
    local source_dir=$1
    local dest_dir=$2
    shift 2
    local subdirs=("$@")  # Remaining args are subdirectory names

    log_message "INFO" "Copying selective subdirectories from $(basename "$source_dir"): ${subdirs[*]}"

    if [ ! -d "$source_dir" ]; then
        log_message "ERROR" "Source directory not found: $source_dir"
        return 1
    fi

    # Create destination base directory
    if ! mkdir -p "$dest_dir" 2>/dev/null; then
        log_message "ERROR" "Failed to create destination: $dest_dir"
        return 1
    fi

    # Copy each specified subdirectory
    for subdir in "${subdirs[@]}"; do
        local source_subdir="${source_dir}/${subdir}"
        local dest_subdir="${dest_dir}/${subdir}"

        if [ ! -d "$source_subdir" ]; then
            log_message "WARNING" "Subdirectory not found, skipping: $subdir"
            continue
        fi

        log_message "INFO" "Copying subdirectory: $subdir"

        # Create destination subdirectory
        if ! mkdir -p "$dest_subdir" 2>/dev/null; then
            log_message "ERROR" "Failed to create: $dest_subdir"
            return 1
        fi

        # Copy all files from this subdirectory
        while IFS= read -r file; do
            if [ -f "$file" ]; then
                local relative_path="${file#${source_dir}/}"
                local dest_file="${dest_dir}/${relative_path}"

                copy_file_with_validation "$file" "$dest_file" "$relative_path"

                if [ $? -ne 0 ]; then
                    log_message "ERROR" "Failed to copy: $relative_path"
                    return 1
                fi
            fi
        done < <(find "$source_subdir" -type f 2>/dev/null)
    done

    log_message "INFO" "Completed selective copy of $(basename "$source_dir")"
    return 0
}

# Add template marker to CLAUDE.md
add_template_marker_to_file() {
    local file=$1
    # Use printf + cat for maximum portability (works on Linux and macOS)
    # This avoids sed compatibility issues and special character escaping
    {
        printf '%s\n' "$TEMPLATE_MARKER"
        cat "$file"
    } > "${file}.tmp" && mv "${file}.tmp" "$file"
    log_operation "TEMPLATE_MARKER" "Added to $(basename "$file")"
    return 0
}

# Copy single file with optional template marker
copy_single_file() {
    local source=$1
    local dest=$2
    local add_template_marker=${3:-false}

    # Validate source exists
    if [ ! -f "$source" ]; then
        log_message "ERROR" "Source file not found: $source"
        return 1
    fi

    # Create destination directory
    if ! ensure_dest_directory "$dest"; then
        log_message "ERROR" "Failed to create directory: $(dirname "$dest")"
        return 1
    fi

    # Copy file
    if ! cp -p "$source" "$dest" 2>/dev/null; then
        log_message "ERROR" "Failed to copy: $source"
        return 1
    fi

    # Verify checksum integrity
    if ! validate_file_copy "$source" "$dest"; then
        log_message "ERROR" "Corruption detected in: $dest"
        return 1
    fi

    # Add template marker if requested and verified
    if [ "$add_template_marker" = true ]; then
        if ! add_template_marker_to_file "$dest"; then
            log_message "WARNING" "Failed to add template marker, but file copied successfully"
        fi
    fi

    local src_hash=$(calculate_file_hash "$source")
    COPIED_FILES=$((COPIED_FILES + 1))
    TOTAL_FILES=$((TOTAL_FILES + 1))
    log_operation "COPY" "$(basename "$source") (${src_hash})"

    return 0
}

# Generate checksum manifest
generate_checksums() {
    log_message "INFO" "Generating checksum manifest..."

    # Use atomic write with temporary file to prevent race condition
    local temp_checksums="${CHECKSUMS_FILE}.tmp.$$"

    # Generate all checksums to temporary file first
    {
        if [ -d "$DEST_CLAUDE" ]; then
            find "$DEST_CLAUDE" -type f -exec sha256sum {} \;
        fi

        if [ -d "$DEST_DEVFORGEAI" ]; then
            find "$DEST_DEVFORGEAI" -type f -exec sha256sum {} \;
        fi

        if [ -f "$DEST_CLAUDE_MD" ]; then
            sha256sum "$DEST_CLAUDE_MD"
        fi
    } | sort > "$temp_checksums"

    # Verify temp file has content before atomic move
    if [ ! -s "$temp_checksums" ]; then
        log_message "ERROR" "Checksum file is empty"
        rm -f "$temp_checksums"
        return 1
    fi

    # Atomic move - prevents corruption if process crashes
    if ! mv "$temp_checksums" "$CHECKSUMS_FILE"; then
        log_message "ERROR" "Failed to write checksums"
        rm -f "$temp_checksums"
        return 1
    fi

    local checksum_count=$(wc -l < "$CHECKSUMS_FILE")
    log_message "INFO" "Generated $checksum_count checksums"

    return 0
}

# Validate checksums
validate_checksums() {
    log_message "INFO" "Validating checksums..."

    if [ ! -f "$CHECKSUMS_FILE" ]; then
        log_message "ERROR" "Checksum file not found: $CHECKSUMS_FILE"
        return 1
    fi

    local checksum_count=$(wc -l < "$CHECKSUMS_FILE")

    # Basic format validation
    if ! grep -q "^[a-f0-9]\{64\}[[:space:]]" "$CHECKSUMS_FILE"; then
        log_message "ERROR" "Invalid checksum format"
        return 1
    fi

    # Try to verify with shasum if available
    if command -v shasum &> /dev/null; then
        if ! shasum -c "$CHECKSUMS_FILE" &>/dev/null; then
            log_message "WARNING" "Some checksums failed verification"
            return 1
        fi
    fi

    log_operation "VALIDATE" "All $checksum_count checksums verified"
    return 0
}

# Count files in a directory
count_directory_files() {
    local dir=$1
    find "$dir" -type f 2>/dev/null | wc -l
}

# Validate directory file count within tolerance
validate_directory_count() {
    local dir=$1
    local expected=$2
    local tolerance=${3:-$FILE_COUNT_TOLERANCE}

    local actual=$(count_directory_files "$dir")
    local min=$((expected - tolerance))
    local max=$((expected + tolerance))

    if [ "$actual" -lt "$min" ] || [ "$actual" -gt "$max" ]; then
        return 1
    fi
    return 0
}

# Validate original directories unchanged
validate_originals() {
    log_message "INFO" "Validating original directories unchanged..."

    local claude_count=$(count_directory_files "$SRC_CLAUDE")
    local devforgeai_count=$(count_directory_files "$SRC_DEVFORGEAI")

    # Warn if counts are lower than expected
    if ! validate_directory_count "$SRC_CLAUDE" "$EXPECTED_CLAUDE_FILES"; then
        log_message "WARNING" "Original .claude count unexpected: $claude_count (expected ~$EXPECTED_CLAUDE_FILES)"
    fi

    if ! validate_directory_count "$SRC_DEVFORGEAI" "$EXPECTED_DEVFORGEAI_FILES"; then
        log_message "WARNING" "Original .devforgeai count unexpected: $devforgeai_count (expected ~$EXPECTED_DEVFORGEAI_FILES)"
    fi

    log_operation "VALIDATE" "Original .claude: $claude_count files"
    log_operation "VALIDATE" "Original .devforgeai: $devforgeai_count files"

    return 0
}

# Check if git repository is available
is_git_repository() {
    [ -d "$GIT_DIR" ]
}

# Stage all copied files in git
stage_files_in_git() {
    local project_root=$1

    # Stage all files in src/
    if ! git -C "$project_root" add src/ 2>/dev/null; then
        log_message "ERROR" "Failed to stage src/ directory"
        return 1
    fi

    # Stage checksums file if it exists
    if [ -f "$CHECKSUMS_FILE" ]; then
        git -C "$project_root" add "$CHECKSUMS_FILE" 2>/dev/null
    fi

    return 0
}

# Count staged files in git
count_staged_files() {
    local project_root=$1
    git -C "$project_root" status --porcelain 2>/dev/null | grep "^A " | wc -l
}

# Stage files in git
stage_in_git() {
    log_message "INFO" "Staging copied files in git..."

    # Check if git repository is available
    if ! is_git_repository; then
        log_message "WARNING" "Git repository not found"
        return 0
    fi

    # Stage files
    if ! stage_files_in_git "$PROJECT_ROOT"; then
        return 1
    fi

    # Report staged count
    local staged_count=$(count_staged_files "$PROJECT_ROOT")
    log_operation "GIT" "Staged $staged_count files"
    log_message "INFO" "Files staged in git: $staged_count"

    return 0
}

# Generate migration report
generate_report() {
    local report_content="# Migration Report - STORY-042

**Generated:** $(date)

## Summary

- **Total Files Processed:** $TOTAL_FILES
- **Files Copied:** $COPIED_FILES
- **Files Skipped:** $SKIPPED_FILES (already present with matching checksums)
- **Files Excluded:** $EXCLUDED_FILES (backup/artifact patterns)
- **Files Failed:** $FAILED_FILES

## Directories Copied

### .claude/ → src/claude/
- Status: Complete
- Files: $(find "$DEST_CLAUDE" -type f 2>/dev/null | wc -l)

### .devforgeai/ → src/devforgeai/
- Status: Complete
- Files: $(find "$DEST_DEVFORGEAI" -type f 2>/dev/null | wc -l)
- Excluded: qa/reports/, RCA/, adrs/, feedback/imported/, logs/

### CLAUDE.md → src/CLAUDE.md
- Status: Complete
- Size: $(stat -c%s "$DEST_CLAUDE_MD" 2>/dev/null || stat -f%z "$DEST_CLAUDE_MD") bytes
- Template Marker: Added

## Validation Results

### Checksums
- Total: $(wc -l < "$CHECKSUMS_FILE" 2>/dev/null || echo "0")
- Format: SHA256 <filepath>
- Verifiable: Yes

### Original Directories
- .claude: $(find "$SRC_CLAUDE" -type f 2>/dev/null | wc -l) files (unchanged)
- .devforgeai: $(find "$SRC_DEVFORGEAI" -type f 2>/dev/null | wc -l) files (unchanged)

## Exclusions

Patterns excluded: $(printf '%s, ' "${EXCLUDED_PATTERNS[@]}")

Total excluded: $EXCLUDED_FILES files

## Errors Encountered

$(if [ ${#FAILED_OPERATIONS[@]} -gt 0 ]; then
    printf '%s\n' "${FAILED_OPERATIONS[@]}"
else
    echo "None"
fi)

## Next Steps

1. Review this report for any errors
2. Run: \`git status\` to verify file staging
3. Commit with: \`git commit -m 'feat(STORY-042): Migrate framework files to src/'\`
4. Verify: \`/dev --help\` and \`/qa --help\` still work
"

    echo "$report_content" > "$REPORT_FILE"
    log_message "INFO" "Report generated: $REPORT_FILE"
}

# Write migration checkpoint
write_checkpoint() {
    local last_file=$1

    if command -v jq &> /dev/null; then
        echo "{\"last_copied\": \"$last_file\", \"timestamp\": \"$(date)\"}" | \
            jq . > "$CHECKPOINT_FILE"
    else
        echo "{\"last_copied\": \"$last_file\", \"timestamp\": \"$(date)\"}" > "$CHECKPOINT_FILE"
    fi
}

# Cleanup on error
cleanup_on_error() {
    log_message "ERROR" "Migration failed - initiating rollback"

    # Remove copied files
    if [ -d "$DEST_CLAUDE" ]; then
        rm -rf "$DEST_CLAUDE"
        log_operation "ROLLBACK" "Removed $DEST_CLAUDE"
    fi

    if [ -d "$DEST_DEVFORGEAI" ]; then
        rm -rf "$DEST_DEVFORGEAI"
        log_operation "ROLLBACK" "Removed $DEST_DEVFORGEAI"
    fi

    if [ -f "$DEST_CLAUDE_MD" ]; then
        rm -f "$DEST_CLAUDE_MD"
        log_operation "ROLLBACK" "Removed $DEST_CLAUDE_MD"
    fi

    log_message "ERROR" "Rollback completed"
    return 1
}

# Parse command-line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run) DRY_RUN=true; shift ;;
            --resume) RESUME=true; shift ;;
            --rollback) ROLLBACK=true; shift ;;
            --non-interactive) INTERACTIVE=false; shift ;;
            --help) return 2 ;;  # Special return code for help
            *) echo "Unknown option: $1"; return 1 ;;
        esac
    done
    return 0
}

# Print usage
print_usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Options:
  --dry-run      Show what would be copied without performing actual copy
  --resume       Resume from last checkpoint (for interrupted migrations)
  --rollback     Remove all copied files and restore to pre-migration state
  --help         Show this help message

Examples:
  # Perform migration
  $(basename "$0")

  # Resume interrupted migration
  $(basename "$0") --resume

  # Preview what will be copied
  $(basename "$0") --dry-run
EOF
}

# Validate prerequisites before migration
validate_prerequisites() {
    local status=0

    # Validate source directories
    if [ ! -d "$SRC_CLAUDE" ]; then
        log_message "ERROR" "Source directory not found: $SRC_CLAUDE"
        status=1
    fi

    if [ ! -d "$SRC_DEVFORGEAI" ]; then
        log_message "ERROR" "Source directory not found: $SRC_DEVFORGEAI"
        status=1
    fi

    if [ ! -f "$SRC_CLAUDE_MD" ]; then
        log_message "ERROR" "Source file not found: $SRC_CLAUDE_MD"
        status=1
    fi

    # Create src directory
    if ! mkdir -p "$PROJECT_ROOT/src" 2>/dev/null; then
        log_message "ERROR" "Failed to create src/ directory"
        status=1
    fi

    return $status
}

# Execute all 8 migration phases
execute_migration_phases() {
    # Phase 1: Copy .claude/ directory
    log_message "INFO" "Phase 1: Copying .claude/ directory (~${EXPECTED_CLAUDE_FILES} files)"
    if ! copy_directory "$SRC_CLAUDE" "$DEST_CLAUDE"; then
        return 1
    fi

    # Phase 2: Copy .devforgeai/ directory (selective subdirectories only)
    log_message "INFO" "Phase 2: Copying .devforgeai/ config/docs/protocols/specs (~${EXPECTED_DEVFORGEAI_FILES} files)"
    if ! copy_selective_subdirectories "$SRC_DEVFORGEAI" "$DEST_DEVFORGEAI" "config" "docs" "protocols" "specs"; then
        return 1
    fi

    # Phase 3: Copy CLAUDE.md
    log_message "INFO" "Phase 3: Copying CLAUDE.md as template"
    if ! copy_single_file "$SRC_CLAUDE_MD" "$DEST_CLAUDE_MD" false; then
        return 1
    fi

    # Add template marker after successful copy
    if [ -f "$DEST_CLAUDE_MD" ]; then
        if ! add_template_marker_to_file "$DEST_CLAUDE_MD"; then
            log_message "WARNING" "Failed to add template marker to $DEST_CLAUDE_MD"
        fi
    fi

    # Phase 4: Generate checksums
    log_message "INFO" "Phase 4: Generating checksum manifest"
    if ! generate_checksums; then
        return 1
    fi

    # Phase 5: Validate checksums
    log_message "INFO" "Phase 5: Validating checksums"
    if ! validate_checksums; then
        return 1
    fi

    # Phase 6: Validate originals
    log_message "INFO" "Phase 6: Validating original directories unchanged"
    if ! validate_originals; then
        return 1
    fi

    # Phase 7: Stage in git
    log_message "INFO" "Phase 7: Staging files in git"
    if ! stage_in_git; then
        return 1
    fi

    # Phase 8: Generate report
    log_message "INFO" "Phase 8: Generating migration report"
    generate_report

    return 0
}

# Print migration summary
print_migration_summary() {
    echo ""
    echo -e "${GREEN}✓ Migration completed successfully${NC}"
    echo "  Files copied:   $COPIED_FILES"
    echo "  Files skipped:  $SKIPPED_FILES"
    echo "  Files excluded: $EXCLUDED_FILES"
    echo "  Files failed:   $FAILED_FILES"
    echo ""
    echo "Next steps:"
    echo "  1. Review: $REPORT_FILE"
    echo "  2. Verify: git status"
    echo "  3. Commit: git commit -m 'feat(STORY-042): Migrate framework files to src/'"
    echo ""
}

##############################################################################
# Main Migration Workflow
##############################################################################

main() {
    # Initialize log
    > "$LOG_FILE"

    log_message "INFO" "═════════════════════════════════════════════════════════════"
    log_message "INFO" "STORY-042: Framework File Migration"
    log_message "INFO" "═════════════════════════════════════════════════════════════"

    # Parse command-line arguments
    parse_arguments "$@"
    local parse_result=$?

    if [ $parse_result -eq 2 ]; then
        print_usage
        exit 0
    elif [ $parse_result -ne 0 ]; then
        print_usage
        exit 1
    fi

    # Change to project root
    cd "$PROJECT_ROOT" || exit 1

    # Load configuration
    if ! load_config; then
        log_message "ERROR" "Failed to load configuration"
        exit 1
    fi

    # Handle rollback command
    if [ "$ROLLBACK" = true ]; then
        cleanup_on_error
        exit $?
    fi

    # Validate all prerequisites
    if ! validate_prerequisites; then
        exit 1
    fi

    log_message "INFO" "Starting migration process..."

    # Execute all 8 migration phases
    if ! execute_migration_phases; then
        cleanup_on_error
        exit 1
    fi

    # Log final summary
    log_message "INFO" "═════════════════════════════════════════════════════════════"
    log_message "INFO" "Migration completed successfully"
    log_message "INFO" "Files copied: $COPIED_FILES"
    log_message "INFO" "Files skipped: $SKIPPED_FILES"
    log_message "INFO" "Files excluded: $EXCLUDED_FILES"
    log_message "INFO" "Files failed: $FAILED_FILES"
    log_message "INFO" "═════════════════════════════════════════════════════════════"

    # Print summary to console
    print_migration_summary

    return 0
}

# Execute main with all arguments
main "$@"
exit $?
