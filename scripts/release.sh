#!/usr/bin/env bash
#
# DevForgeAI Release Automation Script
# Purpose: Orchestrate complete framework release workflow
# Usage: bash scripts/release.sh [--dry-run] [--yes] [--help]
#
# Phases:
#   0. Pre-flight validation (git, tests, authentication)
#   1. Interactive version selection
#   2. Operational files sync (.claude → src/claude, .devforgeai → src/devforgeai)
#   3. Version metadata update (version.json, CHANGELOG.md, git tag)
#   4. Integrity verification (SHA-256 checksums)
#   5. GitHub release creation
#   6. NPM package publication
#   7. Finalization and cleanup
#
# Rollback: Each phase supports rollback on failure

set -euo pipefail

# =============================================================================
# CONFIGURATION
# =============================================================================

# Script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load configuration
CONFIG_FILE="${PROJECT_ROOT}/.devforgeai/config/release-config.sh"
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
fi

# Default configuration (if config file missing)
DRY_RUN="${DRY_RUN:-false}"
AUTO_YES="${AUTO_YES:-false}"
CHECKSUM_ALGORITHM="${CHECKSUM_ALGORITHM:-sha256}"
NPM_REGISTRY="${NPM_REGISTRY:-https://registry.npmjs.org}"

# Exclude patterns for sync
CLAUDE_EXCLUDE_PATTERNS=("*.backup*" "__pycache__/" "*.pyc" ".DS_Store" "*.log")
DEVFORGEAI_EXCLUDE_PATTERNS=("backups/" "qa/reports/" "feedback/sessions/" "*.log" "*.backup*")

# File paths
VERSION_FILE="${PROJECT_ROOT}/src/version.json"
PACKAGE_JSON="${PROJECT_ROOT}/src/package.json"
CHECKSUMS_FILE="${PROJECT_ROOT}/src/checksums.txt"
SYNC_MANIFEST="${PROJECT_ROOT}/src/.sync-manifest.json"
CHANGELOG_FILE="${PROJECT_ROOT}/CHANGELOG.md"
RELEASE_LOG_DIR="${PROJECT_ROOT}/.devforgeai/releases"

# Phase tracking for rollback
PHASE_COMPLETED=()
GIT_TAG_CREATED=""
GIT_COMMIT_CREATED=""

# Colors
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
CYAN='\033[36m'
RESET='\033[0m'
NO_COLOR="${NO_COLOR:-}"

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

# Color output function - supports NO_COLOR environment variable
color() {
    local color_code="$1"
    shift
    if [[ -z "$NO_COLOR" ]] && [[ -t 1 ]]; then
        echo -e "${color_code}$*${RESET}"
    else
        echo "$*"
    fi
}

# Logging functions with consistent formatting
log_info() {
    color "$BLUE" "ℹ️  $*"
}

log_success() {
    color "$GREEN" "✓ $*"
}

log_error() {
    color "$RED" "❌ $*" >&2
}

log_warning() {
    color "$YELLOW" "⚠️  $*"
}

log_phase() {
    local phase_num="$1"
    local phase_name="$2"
    color "$CYAN" "[$phase_num/7] $phase_name..."
}

# Error handling with automatic rollback
error_exit() {
    local message="$1"
    local exit_code="${2:-1}"
    log_error "$message"
    rollback_on_failure
    exit "$exit_code"
}

# Phase completion tracking for rollback
mark_phase_complete() {
    local phase="$1"
    PHASE_COMPLETED+=("$phase")
}

# Command existence check with helpful error message
require_command() {
    local cmd="$1"
    local install_url="${2:-}"

    if ! command -v "$cmd" &> /dev/null; then
        local error_msg="$cmd not found."
        [[ -n "$install_url" ]] && error_msg+=" Install from: $install_url"
        error_exit "$error_msg"
    fi
}

# Validate file exists and is non-empty
require_file() {
    local file_path="$1"
    local error_msg="${2:-File not found: $file_path}"

    if [[ ! -f "$file_path" ]]; then
        error_exit "$error_msg"
    fi

    if [[ ! -s "$file_path" ]]; then
        error_exit "File is empty: $file_path"
    fi
}

# =============================================================================
# HELP AND VERSION
# =============================================================================

show_help() {
    cat <<EOF
DevForgeAI Release Automation Script

Usage: bash scripts/release.sh [OPTIONS]

Options:
  --dry-run        Simulate release without external changes
  --yes, -y        Skip interactive confirmations (CI mode)
  --help, -h       Show this help message
  --version, -v    Show script version

Phases:
  0. Pre-flight validation (git, tests, auth)
  1. Interactive version selection
  2. Operational files sync
  3. Version metadata update
  4. Checksum generation
  5. GitHub release creation
  6. NPM package publication
  7. Finalization

Requirements:
  - git >= 2.25
  - gh >= 2.0 (GitHub CLI, authenticated)
  - npm >= 8.0 (authenticated)
  - bash >= 4.0
  - sha256sum (or shasum on macOS)

EOF
}

show_version() {
    echo "DevForgeAI Release Script v1.0.0"
}

# =============================================================================
# PHASE 0: PRE-FLIGHT VALIDATION
# =============================================================================
# Validates environment is ready for release:
# - Git working tree is clean (no uncommitted changes)
# - All tests are passing
# - Required external tools are installed and authenticated

validate_git_working_tree() {
    log_info "Checking git working tree..."

    local status
    status=$(git status --porcelain)

    if [[ -n "$status" ]]; then
        log_error "Uncommitted changes detected:"
        echo "$status" | while IFS= read -r line; do
            echo "  $line"
        done
        error_exit "Commit or stash changes before releasing. Run: git status"
    fi

    log_success "Git working tree clean"
}

run_test_suite() {
    log_info "Running test suite..."

    if [[ -f "${PROJECT_ROOT}/package.json" ]]; then
        if npm test; then
            log_success "Tests passing"
        else
            error_exit "Tests failed. Fix test failures before releasing."
        fi
    else
        log_warning "No package.json found, skipping tests"
    fi
}

validate_cli_authentication() {
    local cli_name="$1"
    local auth_check_cmd="$2"
    local auth_fix_cmd="$3"

    if ! $auth_check_cmd &> /dev/null; then
        error_exit "$cli_name not authenticated. Run: $auth_fix_cmd"
    fi
    log_success "$cli_name authenticated"
}

validate_external_tools() {
    log_info "Validating external tools..."

    # Required command-line tools
    require_command "gh" "https://cli.github.com/"
    require_command "npm" "https://nodejs.org/"
    require_command "git"

    # Check authentication for external services
    validate_cli_authentication "gh CLI" "gh auth status" "gh auth login"
    validate_cli_authentication "npm" "npm whoami" "npm login"

    # Validate checksum utility availability (platform-dependent)
    if ! command -v sha256sum &> /dev/null && ! command -v shasum &> /dev/null; then
        error_exit "No SHA-256 utility found (sha256sum or shasum required)"
    fi
}

phase_preflight_validation() {
    log_phase 0 "Pre-flight validation"

    validate_git_working_tree
    run_test_suite
    validate_external_tools

    log_success "Pre-flight validation complete"
    mark_phase_complete "preflight"
}

# =============================================================================
# PHASE 1: VERSION SELECTION
# =============================================================================
# Interactive version selection workflow:
# - Display current version from version.json
# - Offer major/minor/patch bump or custom version
# - Validate semver format
# - Check version uniqueness against npm registry and git tags
# - Require user confirmation before proceeding

get_current_version() {
    if [[ -f "$VERSION_FILE" ]]; then
        jq -r '.version' "$VERSION_FILE"
    else
        echo "0.0.0"
    fi
}

increment_version() {
    local version="$1"
    local bump_type="$2"

    # Parse semver components
    local major minor patch
    IFS='.' read -r major minor patch <<< "$version"
    # Strip pre-release suffix (e.g., -beta.1)
    patch="${patch%%-*}"

    # Increment appropriate component based on bump type
    case "$bump_type" in
        major) echo "$((major + 1)).0.0" ;;
        minor) echo "${major}.$((minor + 1)).0" ;;
        patch) echo "${major}.${minor}.$((patch + 1))" ;;
        *)     echo "$version" ;;  # Invalid type, return unchanged
    esac
}

validate_semver() {
    local version="$1"
    if [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.]+)?$ ]]; then
        return 0
    else
        return 1
    fi
}

check_npm_version_available() {
    local version="$1"
    log_info "Checking npm registry for version $version..."

    if npm view "@devforgeai/framework@${version}" version &> /dev/null; then
        error_exit "Version $version already published to npm. Choose a different version."
    fi
}

check_git_tag_available() {
    local version="$1"
    log_info "Checking git tags for v${version}..."

    if git tag -l "v${version}" | grep -q "v${version}"; then
        error_exit "Git tag v${version} already exists. Delete tag or choose different version."
    fi
}

check_version_uniqueness() {
    local version="$1"

    check_npm_version_available "$version"
    check_git_tag_available "$version"

    log_success "Version $version is unique and available"
}

display_version_menu() {
    local current="$1"

    echo
    color "$CYAN" "=== DevForgeAI Release Workflow ==="
    echo "Current version: $current"
    echo
    echo "Select version bump type:"
    echo "  1) patch  ($current → $(increment_version "$current" "patch"))"
    echo "  2) minor  ($current → $(increment_version "$current" "minor"))"
    echo "  3) major  ($current → $(increment_version "$current" "major"))"
    echo "  4) custom (enter specific version)"
    echo
}

get_version_from_selection() {
    local current="$1"
    local selection="$2"

    case "$selection" in
        1) increment_version "$current" "patch" ;;
        2) increment_version "$current" "minor" ;;
        3) increment_version "$current" "major" ;;
        4)
            read -rp "Enter custom version (e.g., 2.0.0-beta.1): " custom_version
            if ! validate_semver "$custom_version"; then
                error_exit "Invalid semver format: $custom_version (expected: X.Y.Z or X.Y.Z-suffix)"
            fi
            echo "$custom_version"
            ;;
        *) error_exit "Invalid selection: $selection (expected: 1-4)" ;;
    esac
}

interactive_version_selection() {
    if [[ "$AUTO_YES" == "true" ]]; then
        # CI mode: automatically use patch bump
        SELECTED_VERSION=$(increment_version "$CURRENT_VERSION" "patch")
        log_info "Auto-selected version: $SELECTED_VERSION (CI mode)"
        return
    fi

    display_version_menu "$CURRENT_VERSION"
    read -rp "Enter selection [1-4]: " selection
    SELECTED_VERSION=$(get_version_from_selection "$CURRENT_VERSION" "$selection")
}

confirm_release() {
    if [[ "$AUTO_YES" == "true" ]]; then
        return 0
    fi

    echo
    log_warning "Release v${SELECTED_VERSION} will:"
    echo "  - Create git tag v${SELECTED_VERSION}"
    echo "  - Push to origin/main"
    echo "  - Create GitHub release"
    echo "  - Publish to npm registry"
    echo

    read -rp "Proceed? [y/N]: " confirmation

    if [[ ! "$confirmation" =~ ^[Yy]$ ]]; then
        log_info "Release cancelled by user"
        exit 0
    fi
}

phase_version_selection() {
    log_phase 1 "Version selection"

    CURRENT_VERSION=$(get_current_version)
    interactive_version_selection
    check_version_uniqueness "$SELECTED_VERSION"
    confirm_release

    log_success "Version selected: $SELECTED_VERSION"
    mark_phase_complete "version_selection"
}

# =============================================================================
# PHASE 2: OPERATIONAL FILES SYNC
# =============================================================================
# Sync operational directories to distribution source:
# - .claude/ → src/claude/ (framework skills, commands, agents)
# - .devforgeai/ → src/devforgeai/ (context files, templates, configs)
# - Apply exclusion patterns (backups, logs, temp files)
# - Validate sync completeness
# - Generate sync manifest for audit trail

build_rsync_exclude_args() {
    local -n patterns=$1  # nameref to array
    local -a rsync_opts=()

    for pattern in "${patterns[@]}"; do
        rsync_opts+=(--exclude="$pattern")
    done

    echo "${rsync_opts[@]}"
}

sync_with_rsync() {
    local source="$1"
    local dest="$2"
    shift 2
    local exclude_args=("$@")

    rsync -av --delete "${exclude_args[@]}" "$source/" "$dest/"
}

sync_with_cp() {
    local source="$1"
    local dest="$2"

    mkdir -p "$dest"
    cp -r "$source/"* "$dest/"
}

sync_directory() {
    local source="$1"
    local dest="$2"
    shift 2
    local exclude_patterns=("$@")

    log_info "Syncing $source → $dest"

    # Use rsync if available (faster and supports exclusions), otherwise fallback to cp
    if command -v rsync &> /dev/null; then
        local exclude_args
        exclude_args=($(build_rsync_exclude_args exclude_patterns))
        sync_with_rsync "$source" "$dest" "${exclude_args[@]}"
    else
        log_warning "rsync not found, using cp (exclusions not supported)"
        sync_with_cp "$source" "$dest"
    fi
}

count_files_in_directory() {
    local dir="$1"
    find "$dir" -type f 2>/dev/null | wc -l
}

validate_sync() {
    local source="$1"
    local dest="$2"

    local source_count dest_count
    source_count=$(count_files_in_directory "$source")
    dest_count=$(count_files_in_directory "$dest")

    # Destination must have at least 1 file (allow fewer than source due to exclusions)
    if [[ "$dest_count" -lt 1 ]]; then
        error_exit "Sync validation failed: destination directory is empty ($dest)"
    fi

    log_success "Sync validated: $dest_count files copied (source had $source_count files)"
}

generate_sync_manifest() {
    local file_count
    file_count=$(find "${PROJECT_ROOT}/src" -type f | wc -l)

    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    cat > "$SYNC_MANIFEST" <<EOF
{
  "sync_timestamp": "$timestamp",
  "file_count": $file_count,
  "excluded_patterns": [
    "*.backup*",
    "__pycache__/",
    "*.pyc",
    ".DS_Store",
    "backups/",
    "qa/reports/",
    "feedback/sessions/",
    "*.log"
  ],
  "source_hash": "$(find "${PROJECT_ROOT}/src" -type f -exec md5sum {} \\; | md5sum | awk '{print $1}')"
}
EOF

    log_success "Sync manifest created: $SYNC_MANIFEST"
}

phase_operational_files_sync() {
    log_phase 2 "Syncing operational files"

    # Sync .claude → src/claude
    sync_directory \
        "${PROJECT_ROOT}/.claude" \
        "${PROJECT_ROOT}/src/claude" \
        "${CLAUDE_EXCLUDE_PATTERNS[@]}"

    validate_sync "${PROJECT_ROOT}/.claude" "${PROJECT_ROOT}/src/claude"

    # Sync .devforgeai → src/devforgeai
    sync_directory \
        "${PROJECT_ROOT}/.devforgeai" \
        "${PROJECT_ROOT}/src/devforgeai" \
        "${DEVFORGEAI_EXCLUDE_PATTERNS[@]}"

    validate_sync "${PROJECT_ROOT}/.devforgeai" "${PROJECT_ROOT}/src/devforgeai"

    # Generate sync manifest
    generate_sync_manifest

    log_success "Operational files synced"
    mark_phase_complete "sync"
}

# =============================================================================
# PHASE 3: VERSION METADATA UPDATE
# =============================================================================
# Update version tracking and changelog:
# - Update src/version.json with new version and release date
# - Generate CHANGELOG.md from git commits (categorized by type)
# - Create git commit with version bump
# - Create annotated git tag

update_version_json() {
    local version="$1"
    local release_date
    release_date=$(date -u +"%Y-%m-%d")

    # Create or update version.json
    cat > "$VERSION_FILE" <<EOF
{
  "version": "$version",
  "release_date": "$release_date",
  "release_notes_path": "CHANGELOG.md#v${version}"
}
EOF

    log_success "Updated $VERSION_FILE"
}

get_commits_since_last_tag() {
    local last_tag
    last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

    if [[ -n "$last_tag" ]]; then
        git log --pretty=format:"%s" "${last_tag}..HEAD"
    else
        git log --pretty=format:"%s"
    fi
}

categorize_commits() {
    local commits="$1"
    local -n feat_ref=$2
    local -n fix_ref=$3
    local -n chore_ref=$4
    local -n docs_ref=$5

    while IFS= read -r commit; do
        [[ -z "$commit" ]] && continue

        case "$commit" in
            feat:*)  feat_ref+=("$commit") ;;
            fix:*)   fix_ref+=("$commit") ;;
            chore:*) chore_ref+=("$commit") ;;
            docs:*)  docs_ref+=("$commit") ;;
        esac
    done <<< "$commits"
}

build_changelog_section() {
    local version="$1"
    local release_date="$2"
    local -n feat=$3
    local -n fix=$4
    local -n chore=$5
    local -n docs=$6

    local section="## [v${version}] - ${release_date}"$'\n\n'

    # Add each category if it has commits
    if [[ ${#feat[@]} -gt 0 ]]; then
        section+="### Features"$'\n'
        for commit in "${feat[@]}"; do
            section+="- ${commit#feat: }"$'\n'
        done
        section+=$'\n'
    fi

    if [[ ${#fix[@]} -gt 0 ]]; then
        section+="### Bug Fixes"$'\n'
        for commit in "${fix[@]}"; do
            section+="- ${commit#fix: }"$'\n'
        done
        section+=$'\n'
    fi

    if [[ ${#chore[@]} -gt 0 ]]; then
        section+="### Chores"$'\n'
        for commit in "${chore[@]}"; do
            section+="- ${commit#chore: }"$'\n'
        done
        section+=$'\n'
    fi

    if [[ ${#docs[@]} -gt 0 ]]; then
        section+="### Documentation"$'\n'
        for commit in "${docs[@]}"; do
            section+="- ${commit#docs: }"$'\n'
        done
        section+=$'\n'
    fi

    echo "$section"
}

generate_changelog() {
    local version="$1"
    local release_date
    release_date=$(date -u +"%Y-%m-%d")

    # Get and categorize commits
    local commits
    commits=$(get_commits_since_last_tag)

    local feat=() fix=() chore=() docs=()
    categorize_commits "$commits" feat fix chore docs

    # Build changelog section
    local changelog_section
    changelog_section=$(build_changelog_section "$version" "$release_date" feat fix chore docs)

    # Prepend to CHANGELOG.md (create if doesn't exist)
    if [[ -f "$CHANGELOG_FILE" ]]; then
        local temp_file
        temp_file=$(mktemp)
        echo "$changelog_section" > "$temp_file"
        cat "$CHANGELOG_FILE" >> "$temp_file"
        mv "$temp_file" "$CHANGELOG_FILE"
    else
        echo "$changelog_section" > "$CHANGELOG_FILE"
    fi

    log_success "Updated $CHANGELOG_FILE with $(( ${#feat[@]} + ${#fix[@]} + ${#chore[@]} + ${#docs[@]} )) commits"
}

create_git_tag() {
    local version="$1"
    local tag="v${version}"

    # Create annotated tag
    local tag_message="Release v${version}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would create tag: $tag"
    else
        git tag -a "$tag" -m "$tag_message"
        GIT_TAG_CREATED="$tag"
        log_success "Created git tag: $tag"
    fi
}

create_release_commit() {
    local version="$1"
    local commit_message="chore(release): bump version to ${version}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would commit: $commit_message"
    else
        git add "$VERSION_FILE" "$CHANGELOG_FILE"
        git commit -m "$commit_message"
        GIT_COMMIT_CREATED=$(git rev-parse HEAD)
        log_success "Created release commit"
    fi
}

phase_version_metadata_update() {
    log_phase 3 "Updating version metadata"

    update_version_json "$SELECTED_VERSION"
    generate_changelog "$SELECTED_VERSION"
    create_release_commit "$SELECTED_VERSION"
    create_git_tag "$SELECTED_VERSION"

    log_success "Version metadata updated"
    mark_phase_complete "version_metadata"
}

# =============================================================================
# PHASE 4: CHECKSUM GENERATION
# =============================================================================
# Generate integrity verification checksums:
# - Create SHA-256 hashes for all files in src/
# - Sort alphabetically for deterministic output
# - Validate minimum entry count (framework has 100+ files)
# - Append checksum file hash to version.json

detect_checksum_command() {
    if command -v sha256sum &> /dev/null; then
        echo "sha256sum"
    elif command -v shasum &> /dev/null; then
        echo "shasum -a 256"
    else
        error_exit "No SHA-256 command found (sha256sum or shasum required)"
    fi
}

validate_checksum_count() {
    local file="$1"
    local min_count="${2:-50}"

    local line_count
    line_count=$(wc -l < "$file")

    if [[ "$line_count" -lt "$min_count" ]]; then
        error_exit "Checksum validation failed: only $line_count entries (minimum: $min_count)"
    fi

    echo "$line_count"
}

generate_checksums() {
    log_info "Generating SHA-256 checksums..."

    local checksum_cmd
    checksum_cmd=$(detect_checksum_command)

    local temp_file
    temp_file=$(mktemp)

    # Generate checksums in src/ directory
    cd "${PROJECT_ROOT}/src" || error_exit "Cannot access src/ directory"

    # Find all files, excluding specific paths and the checksums file itself
    find . -type f \
        -not -path "*/node_modules/*" \
        -not -path "*/.git/*" \
        -not -name "checksums.txt" \
        -exec $checksum_cmd {} \; | \
        sort -k2 > "$temp_file"

    cd "$PROJECT_ROOT" || error_exit "Cannot return to project root"

    # Move to final location
    mv "$temp_file" "$CHECKSUMS_FILE"

    # Validate minimum entry count
    local line_count
    line_count=$(validate_checksum_count "$CHECKSUMS_FILE" 50)

    log_success "Generated checksums for $line_count files"
}

append_checksum_hash_to_version() {
    local checksum_cmd
    checksum_cmd=$(detect_checksum_command)

    local checksum_hash
    checksum_hash=$($checksum_cmd "$CHECKSUMS_FILE" | awk '{print $1}')

    # Update version.json with checksum_file_sha256
    local temp_file
    temp_file=$(mktemp)

    jq --arg hash "$checksum_hash" '. + {checksum_file_sha256: $hash}' "$VERSION_FILE" > "$temp_file"
    mv "$temp_file" "$VERSION_FILE"

    log_success "Added checksum hash to version.json"
}

phase_checksum_generation() {
    log_phase 4 "Generating checksums"

    generate_checksums
    append_checksum_hash_to_version

    log_success "Checksums generated"
    mark_phase_complete "checksums"
}

# =============================================================================
# PHASE 5: GITHUB RELEASE CREATION
# =============================================================================
# Create GitHub release via gh CLI:
# - Detect pre-release versions (contains hyphen)
# - Create GitHub release with changelog notes
# - Attach checksums.txt file
# - Push git tag and commits to remote

is_prerelease() {
    local version="$1"
    if [[ "$version" =~ - ]]; then
        return 0
    else
        return 1
    fi
}

create_github_release() {
    local version="$1"
    local tag="v${version}"
    local title="DevForgeAI v${version}"

    log_info "Creating GitHub release..."

    local prerelease_flag=""
    if is_prerelease "$version"; then
        prerelease_flag="--prerelease"
        log_info "Marking as pre-release"
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would create GitHub release: $tag"
        echo "[DRY RUN] https://github.com/user/repo/releases/tag/$tag"
    else
        local release_url
        release_url=$(gh release create "$tag" \
            --title "$title" \
            --notes-file "$CHANGELOG_FILE" \
            $prerelease_flag \
            "$CHECKSUMS_FILE")

        log_success "GitHub release created: $release_url"
        echo "$release_url"
    fi
}

push_to_remote() {
    local tag="v${SELECTED_VERSION}"

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would push tag $tag to origin"
        log_info "[DRY RUN] Would push commits to origin/main"
    else
        git push origin "$tag"
        git push origin main
        log_success "Pushed to origin"
    fi
}

phase_github_release() {
    log_phase 5 "Creating GitHub release"

    create_github_release "$SELECTED_VERSION"
    push_to_remote

    log_success "GitHub release created"
    mark_phase_complete "github_release"
}

# =============================================================================
# PHASE 6: NPM PACKAGE PUBLICATION
# =============================================================================
# Publish package to npm registry:
# - Validate src/package.json exists (from STORY-067)
# - Update package.json version to match version.json
# - Publish with appropriate dist-tag (latest or beta)
# - Output npm package URL

validate_package_json() {
    if [[ ! -f "$PACKAGE_JSON" ]]; then
        error_exit "src/package.json not found. Run STORY-067 setup first."
    fi
    log_success "package.json validated"
}

update_package_version() {
    local version="$1"

    local temp_file
    temp_file=$(mktemp)

    jq --arg version "$version" '.version = $version' "$PACKAGE_JSON" > "$temp_file"
    mv "$temp_file" "$PACKAGE_JSON"

    log_success "Updated package.json version to $version"
}

publish_to_npm() {
    local version="$1"

    log_info "Publishing to npm..."

    cd "${PROJECT_ROOT}/src" || error_exit "Failed to cd to src/"

    local tag
    if is_prerelease "$version"; then
        tag="beta"
    else
        tag="latest"
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        npm publish --dry-run --tag "$tag"
        log_info "[DRY RUN] Would publish to npm with tag: $tag"
    else
        npm publish --tag "$tag"
        log_success "Published to npm with tag: $tag"
    fi

    cd "$PROJECT_ROOT" || error_exit "Failed to cd back"

    local npm_url="https://www.npmjs.com/package/@devforgeai/framework/v/${version}"
    log_success "NPM package: $npm_url"
    echo "$npm_url"
}

phase_npm_publication() {
    log_phase 6 "Publishing to npm"

    validate_package_json
    update_package_version "$SELECTED_VERSION"
    publish_to_npm "$SELECTED_VERSION"

    log_success "NPM package published"
    mark_phase_complete "npm_publish"
}

# =============================================================================
# PHASE 7: FINALIZATION
# =============================================================================
# Complete release workflow:
# - Create release log in .devforgeai/releases/
# - Display success summary with URLs
# - Mark all phases complete

create_release_log() {
    local version="$1"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H-%M-%S")

    mkdir -p "$RELEASE_LOG_DIR"

    local log_file="${RELEASE_LOG_DIR}/release-${version}-${timestamp}.log"

    cat > "$log_file" <<EOF
DevForgeAI Release Log
======================

Version: $version
Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Dry Run: $DRY_RUN

Phases Completed:
EOF

    for phase in "${PHASE_COMPLETED[@]}"; do
        echo "  ✓ $phase" >> "$log_file"
    done

    log_success "Release log saved: $log_file"
}

display_success_summary() {
    local version="$1"

    local file_count
    file_count=$(wc -l < "$CHECKSUMS_FILE" 2>/dev/null || echo "0")

    echo
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║           ✅ Release v${version} Complete                      ║"
    echo "╠═══════════════════════════════════════════════════════════╣"
    echo "║  Files synced:     $(printf '%-40s' "$(find src -type f | wc -l)")║"
    echo "║  Checksum entries: $(printf '%-40s' "$file_count")║"
    echo "╠───────────────────────────────────────────────────────────╣"
    echo "║  GitHub release:                                          ║"
    echo "║  https://github.com/user/repo/releases/tag/v${version}         ║"
    echo "║                                                           ║"
    echo "║  NPM package:                                             ║"
    echo "║  https://www.npmjs.com/package/@devforgeai/framework      ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo
}

phase_finalization() {
    log_phase 7 "Finalizing release"

    create_release_log "$SELECTED_VERSION"
    display_success_summary "$SELECTED_VERSION"

    log_success "Release complete!"
    mark_phase_complete "finalization"
}

# =============================================================================
# ROLLBACK ON FAILURE
# =============================================================================
# Automatic rollback on any phase failure:
# - Revert uncommitted changes (git reset --hard HEAD)
# - Delete created git tag (if not yet pushed)
# - Display rollback summary
# - Exit with error code 1

revert_uncommitted_changes() {
    if [[ -n "$(git status --porcelain)" ]]; then
        git reset --hard HEAD
        log_success "Reverted uncommitted changes"
        return 0
    fi
    return 1
}

delete_created_tag() {
    if [[ -n "$GIT_TAG_CREATED" ]]; then
        if git tag -l "$GIT_TAG_CREATED" | grep -q "$GIT_TAG_CREATED"; then
            git tag -d "$GIT_TAG_CREATED"
            log_success "Deleted local tag: $GIT_TAG_CREATED"
            return 0
        fi
    fi
    return 1
}

display_rollback_summary() {
    local reverted_changes=$1
    local deleted_tag=$2

    echo
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║           ❌ Release Failed                               ║"
    echo "╠═══════════════════════════════════════════════════════════╣"

    if [[ "$reverted_changes" == "1" ]]; then
        echo "║  Rollback:  ✓ Reverted uncommitted changes                ║"
    else
        echo "║  Rollback:  − No uncommitted changes to revert            ║"
    fi

    if [[ "$deleted_tag" == "1" ]]; then
        echo "║             ✓ Deleted local tag                           ║"
    else
        echo "║             − No local tag to delete                      ║"
    fi

    echo "║             ✗ GitHub release: Not created                 ║"
    echo "║             ✗ NPM publish: Not executed                   ║"
    echo "╠───────────────────────────────────────────────────────────╣"
    echo "║  Safe State: Local repository restored to pre-release     ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo
}

rollback_on_failure() {
    log_warning "Initiating rollback..."

    local reverted=0
    local deleted=0

    revert_uncommitted_changes && reverted=1
    delete_created_tag && deleted=1

    display_rollback_summary "$reverted" "$deleted"
}

# =============================================================================
# MAIN WORKFLOW
# =============================================================================

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --yes|-y)
                AUTO_YES=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            --version|-v)
                show_version
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

main() {
    parse_arguments "$@"

    # Change to project root
    cd "$PROJECT_ROOT" || error_exit "Failed to cd to project root"

    # Execute phases in order
    phase_preflight_validation
    phase_version_selection
    phase_operational_files_sync
    phase_version_metadata_update
    phase_checksum_generation
    phase_github_release
    phase_npm_publication
    phase_finalization

    exit 0
}

# Run main workflow
main "$@"
