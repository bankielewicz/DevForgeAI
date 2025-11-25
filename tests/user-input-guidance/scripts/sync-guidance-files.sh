#!/bin/bash

################################################################################
# Sync Guidance Files Script
#
# This script synchronizes user input guidance files from the source distribution
# (src/) to operational locations with conflict detection, atomic backups, and
# validation.
#
# Usage:
#   ./sync-guidance-files.sh [--dry-run] [--force] [--help]
#
# Flags:
#   --dry-run   : Simulate sync operations without modifying files
#   --force     : Bypass conflict detection and overwrite operational files
#   --help      : Display this help message
#
# Exit Codes:
#   0 - Success (all files synced)
#   1 - Missing source file
#   2 - Permission denied / disk space exhausted
#   3 - Rollback triggered (copy failure)
#   4 - Validation failed (hash mismatch)
#   5 - Manual merge needed (conflict detected)
#   6 - Lock file exists (concurrent execution)
#
# File Mappings:
#   src/CLAUDE.md → CLAUDE.md
#   src/.claude/memory/commands-reference.md → .claude/memory/commands-reference.md
#   src/.claude/memory/skills-reference.md → .claude/memory/skills-reference.md
################################################################################

set -e
set -o pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration (allow environment variable overrides for testing)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${REPO_ROOT:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
SOURCE_DIR="${SOURCE_DIR:-$REPO_ROOT/src}"
OPERATIONAL_DIR="${OPERATIONAL_DIR:-$REPO_ROOT}"
SYNC_STATE_FILE="${SYNC_STATE_FILE:-$SCRIPT_DIR/../sync-state.json}"
LOCK_FILE="${LOCK_FILE:-$SCRIPT_DIR/../.sync.lock}"
LOCK_TIMEOUT_SECONDS=600  # 10 minutes
REPORT_DIR="${REPORT_DIR:-$REPO_ROOT/.devforgeai/qa/reports}"
CUMULATIVE_LOG="${CUMULATIVE_LOG:-$REPORT_DIR/guidance-sync-cumulative.log}"

# Command line flags
DRY_RUN=false
FORCE_SYNC=false

# File mappings (source → operational)
declare -A FILE_MAPPINGS=(
    ["$SOURCE_DIR/CLAUDE.md"]="$OPERATIONAL_DIR/CLAUDE.md"
    ["$SOURCE_DIR/claude/memory/commands-reference.md"]="$OPERATIONAL_DIR/.claude/memory/commands-reference.md"
    ["$SOURCE_DIR/claude/memory/skills-reference.md"]="$OPERATIONAL_DIR/.claude/memory/skills-reference.md"
)

# Backup tracking (for rollback)
declare -a BACKUP_FILES=()
declare -a SYNCED_FILES=()

################################################################################
# Utility Functions
################################################################################

log_info() {
    echo -e "${GREEN}✓${NC} $1" >&2
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1" >&2
}

log_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

show_help() {
    head -40 "$0" | tail -36
}

################################################################################
# Lock File Management
################################################################################

acquire_lock() {
    if [[ -f "$LOCK_FILE" ]]; then
        local lock_pid
        lock_pid=$(cat "$LOCK_FILE")
        local lock_age

        if [[ "$(uname)" == "Linux" ]]; then
            lock_age=$(($(date +%s) - $(stat -c %Y "$LOCK_FILE" 2>/dev/null || echo 0)))
        else
            lock_age=$(($(date +%s) - $(stat -f %m "$LOCK_FILE" 2>/dev/null || echo 0)))
        fi

        # Check if lock is stale (>10 minutes)
        if [[ $lock_age -gt $LOCK_TIMEOUT_SECONDS ]]; then
            log_warning "Stale lock file detected (age: ${lock_age}s > ${LOCK_TIMEOUT_SECONDS}s), removing"
            rm -f "$LOCK_FILE"
        else
            log_error "Another sync process is running (PID: $lock_pid, age: ${lock_age}s)"
            exit 6
        fi
    fi

    echo "$$" > "$LOCK_FILE"
    log_info "Lock acquired (PID: $$)"
}

release_lock() {
    if [[ -f "$LOCK_FILE" ]]; then
        rm -f "$LOCK_FILE"
        log_info "Lock released"
    fi
}

################################################################################
# Validation Functions
################################################################################

validate_path() {
    local path="$1"

    # Check if path is regular file (not symlink)
    if [[ -L "$path" ]]; then
        log_error "Symlinks not allowed: $path"
        return 1
    fi

    # Check path length (4096 char limit)
    if [[ ${#path} -gt 4096 ]]; then
        log_error "Path exceeds 4096 characters: $path"
        return 1
    fi

    # Check if regular file
    if [[ ! -f "$path" ]]; then
        log_error "Not a regular file: $path"
        return 1
    fi

    return 0
}

validate_hash() {
    local hash="$1"
    local hash_regex="^[a-f0-9]{32}$"

    if [[ ! "$hash" =~ $hash_regex ]]; then
        log_error "Invalid MD5 hash format: $hash"
        return 1
    fi

    return 0
}

calculate_hash() {
    local file="$1"
    local hash

    hash=$(md5sum "$file" 2>/dev/null | awk '{print $1}')

    if ! validate_hash "$hash"; then
        return 1
    fi

    echo "$hash"
}

check_disk_space() {
    local target_dir="$1"
    local required_kb="${2:-100}"  # Default 100KB

    # Find first existing parent directory
    local check_dir="$target_dir"
    while [[ ! -d "$check_dir" ]] && [[ "$check_dir" != "/" ]]; do
        check_dir=$(dirname "$check_dir")
    done

    local available_kb
    available_kb=$(df "$check_dir" 2>/dev/null | tail -1 | awk '{print $4}')

    # Handle empty or non-numeric value
    if [[ -z "$available_kb" ]] || ! [[ "$available_kb" =~ ^[0-9]+$ ]]; then
        log_warning "Unable to determine disk space, proceeding anyway"
        return 0
    fi

    if [[ $available_kb -lt $required_kb ]]; then
        log_error "Insufficient disk space: ${available_kb}KB available, ${required_kb}KB required"
        return 2
    fi

    return 0
}

################################################################################
# Source File Discovery
################################################################################

discover_source_files() {
    log_info "Discovering source files..."

    local missing_files=()

    for source_file in "${!FILE_MAPPINGS[@]}"; do
        if [[ ! -f "$source_file" ]]; then
            missing_files+=("$source_file")
        else
            if ! validate_path "$source_file"; then
                exit 1
            fi
        fi
    done

    if [[ ${#missing_files[@]} -gt 0 ]]; then
        log_error "Missing source files:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        exit 1
    fi

    log_info "All 3 source files discovered and validated"
}

################################################################################
# Sync State Management
################################################################################

load_sync_state() {
    if [[ ! -f "$SYNC_STATE_FILE" ]]; then
        echo "{}"
        return
    fi

    cat "$SYNC_STATE_FILE"
}

save_sync_state() {
    local timestamp="$1"
    local source_hashes="$2"
    local operational_hashes="$3"

    mkdir -p "$(dirname "$SYNC_STATE_FILE")"

    cat > "$SYNC_STATE_FILE" << EOF
{
  "last_sync_timestamp": "$timestamp",
  "source_hashes": $source_hashes,
  "operational_hashes": $operational_hashes
}
EOF

    log_info "Sync state saved to: $SYNC_STATE_FILE"
}

get_last_sync_hash() {
    local file_key="$1"
    local sync_state

    sync_state=$(load_sync_state)

    if command -v jq &> /dev/null; then
        echo "$sync_state" | jq -r ".operational_hashes[\"$file_key\"] // \"\"" 2>/dev/null || echo ""
    else
        echo ""
    fi
}

################################################################################
# Conflict Detection
################################################################################

detect_conflicts() {
    log_info "Checking for conflicts..."

    local conflicts_found=false

    for source_file in "${!FILE_MAPPINGS[@]}"; do
        local operational_file="${FILE_MAPPINGS[$source_file]}"
        local file_key
        file_key=$(basename "$source_file")

        # Skip if operational file doesn't exist (first-time sync)
        if [[ ! -f "$operational_file" ]]; then
            continue
        fi

        # Calculate hashes
        local source_hash
        source_hash=$(calculate_hash "$source_file")
        local operational_hash
        operational_hash=$(calculate_hash "$operational_file")
        local last_sync_hash
        last_sync_hash=$(get_last_sync_hash "$file_key")

        # Conflict detection: operational ≠ source AND operational ≠ last_sync
        if [[ "$source_hash" != "$operational_hash" ]]; then
            if [[ -n "$last_sync_hash" && "$operational_hash" != "$last_sync_hash" ]]; then
                log_warning "Conflict detected: $file_key"
                echo "  Source hash:      $source_hash"
                echo "  Operational hash: $operational_hash"
                echo "  Last sync hash:   $last_sync_hash"
                conflicts_found=true
            fi
        fi
    done

    if [[ "$conflicts_found" == true ]]; then
        if [[ "$FORCE_SYNC" == true ]]; then
            log_warning "Conflicts detected but --force flag set, proceeding with sync"
        else
            log_error "Conflicts detected. Manual merge required or use --force to overwrite"
            exit 5
        fi
    else
        log_info "No conflicts detected"
    fi
}

################################################################################
# Backup Management
################################################################################

create_backup() {
    local operational_file="$1"
    local timestamp
    timestamp=$(date +"%Y%m%d-%H%M%S")
    local backup_file="${operational_file}.backup-${timestamp}"

    if [[ -f "$operational_file" ]]; then
        if ! cp "$operational_file" "$backup_file"; then
            log_error "Failed to create backup: $backup_file"
            return 3
        fi

        chmod 600 "$backup_file"
        BACKUP_FILES+=("$backup_file")

        if [[ "$DRY_RUN" == true ]]; then
            log_info "Would create backup: $backup_file"
        else
            log_info "Backup created: $backup_file"
        fi
    fi

    return 0
}

cleanup_backups() {
    log_info "Cleaning up backups after successful validation..."

    if [[ ${#BACKUP_FILES[@]} -eq 0 ]]; then
        log_info "No backups to clean up (BACKUP_FILES array is empty)"
        return
    fi

    for backup_file in "${BACKUP_FILES[@]}"; do
        if [[ -f "$backup_file" ]]; then
            rm -f "$backup_file"
            log_info "Removed backup: $backup_file"
        else
            log_warning "Backup file not found: $backup_file"
        fi
    done
}

rollback_changes() {
    log_error "Rolling back changes..."

    for i in "${!BACKUP_FILES[@]}"; do
        local backup_file="${BACKUP_FILES[$i]}"
        local operational_file="${SYNCED_FILES[$i]}"

        if [[ -f "$backup_file" ]]; then
            mv "$backup_file" "$operational_file"
            log_info "Restored: $operational_file"
        fi
    done

    log_info "Rollback complete"
}

################################################################################
# Atomic File Copy
################################################################################

atomic_copy() {
    local source_file="$1"
    local operational_file="$2"

    # Check disk space
    if ! check_disk_space "$(dirname "$operational_file")" 100; then
        return 2
    fi

    # Create parent directory if needed
    mkdir -p "$(dirname "$operational_file")"

    # Atomic copy: temp file + mv
    local temp_file="${operational_file}.tmp.$$"

    if ! cp "$source_file" "$temp_file"; then
        log_error "Copy failed: $source_file → $temp_file"
        rm -f "$temp_file"
        return 3
    fi

    if ! mv "$temp_file" "$operational_file"; then
        log_error "Move failed: $temp_file → $operational_file"
        rm -f "$temp_file"
        return 3
    fi

    SYNCED_FILES+=("$operational_file")

    return 0
}

################################################################################
# Post-Sync Validation
################################################################################

validate_sync() {
    log_info "Validating sync integrity..."

    local validation_failed=false

    for source_file in "${!FILE_MAPPINGS[@]}"; do
        local operational_file="${FILE_MAPPINGS[$source_file]}"
        local file_key
        file_key=$(basename "$source_file")

        local source_hash
        source_hash=$(calculate_hash "$source_file")
        local operational_hash
        operational_hash=$(calculate_hash "$operational_file")

        if [[ "$source_hash" != "$operational_hash" ]]; then
            log_error "Validation failed: $file_key"
            echo "  Expected: $source_hash"
            echo "  Got:      $operational_hash"
            validation_failed=true

            # Mark corrupted file
            if [[ -f "$operational_file" ]]; then
                mv "$operational_file" "${operational_file}.CORRUPT"
                log_warning "Corrupted file moved to: ${operational_file}.CORRUPT"
            fi
        else
            log_info "Validated: $file_key (hash: $source_hash)"
        fi
    done

    if [[ "$validation_failed" == true ]]; then
        rollback_changes
        exit 4
    fi

    log_info "All files validated successfully"
}

################################################################################
# Sync Execution
################################################################################

sync_files() {
    log_info "Starting file synchronization..."

    FILES_SYNCED_COUNT=0
    FILES_SKIPPED_COUNT=0

    for source_file in "${!FILE_MAPPINGS[@]}"; do
        local operational_file="${FILE_MAPPINGS[$source_file]}"
        local file_key
        file_key=$(basename "$source_file")

        # Check if sync needed (hash comparison)
        local source_hash
        source_hash=$(calculate_hash "$source_file")

        if [[ -f "$operational_file" ]]; then
            local operational_hash
            operational_hash=$(calculate_hash "$operational_file")

            if [[ "$source_hash" == "$operational_hash" ]]; then
                log_info "Skipped (already in sync): $file_key"
                ((++FILES_SKIPPED_COUNT)) || true
                continue
            fi
        fi

        if [[ "$DRY_RUN" == true ]]; then
            log_info "Would sync: $file_key"
            ((++FILES_SYNCED_COUNT)) || true
            continue
        fi

        # Create backup before sync
        if ! create_backup "$operational_file"; then
            rollback_changes
            exit 3
        fi

        # Atomic copy
        if ! atomic_copy "$source_file" "$operational_file"; then
            rollback_changes
            exit 3
        fi

        log_info "Synced: $file_key"
        ((++FILES_SYNCED_COUNT)) || true
    done

    log_info "Sync complete: $FILES_SYNCED_COUNT synced, $FILES_SKIPPED_COUNT skipped"
}

################################################################################
# Report Generation
################################################################################

generate_sync_report() {
    local exit_code="$1"
    local files_synced="$2"
    local files_skipped="$3"
    local timestamp
    timestamp=$(date +"%Y%m%d-%H%M%S")
    local report_file="$REPORT_DIR/guidance-sync-${timestamp}.md"

    mkdir -p "$REPORT_DIR"

    # Generate report
    cat > "$report_file" << EOF
# Guidance Files Sync Report

**Generated**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Exit Code**: $exit_code
**Files Synced**: $files_synced
**Files Skipped**: $files_skipped
**Dry Run**: $DRY_RUN
**Force Mode**: $FORCE_SYNC

## File Mappings

EOF

    for source_file in "${!FILE_MAPPINGS[@]}"; do
        local operational_file="${FILE_MAPPINGS[$source_file]}"
        local file_key
        file_key=$(basename "$source_file")

        local source_hash=""
        local operational_hash=""

        if [[ -f "$source_file" ]]; then
            source_hash=$(calculate_hash "$source_file")
        fi

        if [[ -f "$operational_file" ]]; then
            operational_hash=$(calculate_hash "$operational_file")
        fi

        cat >> "$report_file" << EOF
### $file_key

- **Source**: \`$source_file\`
- **Operational**: \`$operational_file\`
- **Source Hash**: \`$source_hash\`
- **Operational Hash**: \`$operational_hash\`
- **Status**: $(if [[ "$source_hash" == "$operational_hash" ]]; then echo "✓ In sync"; else echo "⚠ Out of sync"; fi)

EOF
    done

    # Append summary
    cat >> "$report_file" << EOF

## Summary

- Total source files: 3
- Files synchronized: $files_synced
- Files skipped: $files_skipped
- Backups created: ${#BACKUP_FILES[@]}
- Exit code: $exit_code

## Exit Code Reference

- 0: Success
- 1: Missing source file
- 2: Permission denied / disk space exhausted
- 3: Rollback triggered (copy failure)
- 4: Validation failed (hash mismatch)
- 5: Manual merge needed (conflict detected)
- 6: Lock file exists (concurrent execution)
EOF

    log_info "Report generated: $report_file"

    # Append to cumulative log
    local status_message
    case $exit_code in
        0) status_message="Successful sync" ;;
        1) status_message="Missing source file" ;;
        2) status_message="Permission/disk space error" ;;
        3) status_message="Rollback triggered" ;;
        4) status_message="Validation failed" ;;
        5) status_message="Manual merge needed" ;;
        6) status_message="Lock file exists" ;;
        *) status_message="Unknown error" ;;
    esac

    echo "$(date +"%Y-%m-%d %H:%M:%S") | $exit_code | $files_synced | $files_skipped | $status_message" >> "$CUMULATIVE_LOG"
    log_info "Cumulative log updated: $CUMULATIVE_LOG"
}

################################################################################
# Main Execution
################################################################################

main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --force)
                FORCE_SYNC=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done

    # Show mode
    if [[ "$DRY_RUN" == true ]]; then
        log_warning "DRY-RUN MODE: No files will be modified"
    fi

    if [[ "$FORCE_SYNC" == true ]]; then
        log_warning "FORCE MODE: Conflicts will be overwritten"
    fi

    # Acquire lock
    acquire_lock

    # Ensure lock is released on exit
    trap 'release_lock' EXIT

    # Step 1: Discover source files
    discover_source_files

    # Step 2: Detect conflicts
    detect_conflicts

    # Step 3: Sync files
    sync_files
    local files_synced="$FILES_SYNCED_COUNT"
    local files_skipped="$FILES_SKIPPED_COUNT"

    # Step 4: Post-sync validation
    if [[ "$DRY_RUN" == false ]]; then
        validate_sync

        # Step 5: Save sync state
        local timestamp
        timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

        # Build hash objects
        local source_hashes_json="{"
        local operational_hashes_json="{"
        local first=true

        for source_file in "${!FILE_MAPPINGS[@]}"; do
            local operational_file="${FILE_MAPPINGS[$source_file]}"
            local file_key
            file_key=$(basename "$source_file")

            local source_hash
            source_hash=$(calculate_hash "$source_file")
            local operational_hash
            operational_hash=$(calculate_hash "$operational_file")

            if [[ "$first" == false ]]; then
                source_hashes_json+=","
                operational_hashes_json+=","
            fi

            source_hashes_json+="\"$file_key\": \"$source_hash\""
            operational_hashes_json+="\"$file_key\": \"$operational_hash\""
            first=false
        done

        source_hashes_json+="}"
        operational_hashes_json+="}"

        save_sync_state "$timestamp" "$source_hashes_json" "$operational_hashes_json"

        # Step 6: Cleanup backups
        cleanup_backups
    fi

    # Step 7: Generate report
    generate_sync_report 0 "$files_synced" "$files_skipped"

    log_info "Sync completed successfully"
    exit 0
}

# Execute main
main "$@"
