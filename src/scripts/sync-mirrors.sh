#!/bin/bash
# sync-mirrors.sh - Sync source of truth to operational directories
# STORY-313: Consolidate Triple Mirror Pattern to Single Source of Truth
#
# This script copies files from src/ (source of truth) to operational directories:
# - src/.claude/ -> .claude/
# - src/devforgeai/ -> devforgeai/
#
# Usage: bash scripts/sync-mirrors.sh [--dry-run]

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Source directories (source of truth)
SRC_CLAUDE="$PROJECT_ROOT/src/claude"
SRC_DEVFORGEAI="$PROJECT_ROOT/src/devforgeai"

# Target directories (operational)
TARGET_CLAUDE="$PROJECT_ROOT/.claude"
TARGET_DEVFORGEAI="$PROJECT_ROOT/devforgeai"

# Options
DRY_RUN=false
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--dry-run] [--verbose]"
            exit 1
            ;;
    esac
done

# Logging functions
log_info() {
    echo "[INFO] $1"
}

log_success() {
    echo "[success] $1"
}

log_error() {
    echo "[ERROR] $1" >&2
}

# Check if source directories exist
check_sources() {
    local errors=0

    if [ ! -d "$SRC_CLAUDE" ]; then
        log_error "Source directory not found: src/claude"
        ((errors++))
    fi

    if [ ! -d "$SRC_DEVFORGEAI" ]; then
        log_error "Source directory not found: src/devforgeai"
        ((errors++))
    fi

    if [ $errors -gt 0 ]; then
        log_error "Cannot proceed - source directories missing"
        exit 1
    fi
}

# Sync a single directory using rsync with archive mode (-a preserves permissions)
sync_directory() {
    local src="$1"
    local target="$2"
    local name="$3"

    log_info "Syncing $name..."
    log_info "  From: $src"
    log_info "  To:   $target"

    if [ "$DRY_RUN" = true ]; then
        log_info "  [DRY RUN] Would sync with: rsync -a --delete"
        if [ "$VERBOSE" = true ]; then
            rsync -a --delete --dry-run --itemize-changes "$src/" "$target/"
        fi
    else
        # Use rsync -a to preserve permissions and timestamps
        # --delete removes files in target that don't exist in source
        if [ "$VERBOSE" = true ]; then
            rsync -a --delete --itemize-changes "$src/" "$target/"
        else
            rsync -a --delete "$src/" "$target/"
        fi
        log_success "$name synced successfully"
    fi
}

# Count files for reporting
count_files() {
    local dir="$1"
    find "$dir" -type f 2>/dev/null | wc -l | tr -d ' '
}

# Main execution
main() {
    echo "=============================================="
    echo "DevForgeAI Mirror Sync"
    echo "=============================================="
    echo ""

    if [ "$DRY_RUN" = true ]; then
        log_info "Running in DRY RUN mode - no changes will be made"
        echo ""
    fi

    # Verify sources exist
    check_sources

    # Sync src/claude -> .claude
    sync_directory "$SRC_CLAUDE" "$TARGET_CLAUDE" "src/claude -> .claude"

    echo ""

    # Sync src/devforgeai -> devforgeai
    sync_directory "$SRC_DEVFORGEAI" "$TARGET_DEVFORGEAI" "src/devforgeai -> devforgeai"

    echo ""
    echo "=============================================="

    if [ "$DRY_RUN" = true ]; then
        log_info "Dry run complete - no files were copied"
    else
        # Report summary
        local claude_count=$(count_files "$TARGET_CLAUDE")
        local devforgeai_count=$(count_files "$TARGET_DEVFORGEAI")

        log_success "Sync complete!"
        log_info "  .claude files: $claude_count"
        log_info "  devforgeai files: $devforgeai_count"
    fi

    echo "=============================================="
}

# Run main
main
