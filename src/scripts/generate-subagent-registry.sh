#!/bin/bash
#
# Subagent Registry Generator
# STORY-109: Auto-generates CLAUDE.md registry section from .claude/agents/*.md frontmatter
#
# Usage:
#   ./generate-subagent-registry.sh          # Update CLAUDE.md registry
#   ./generate-subagent-registry.sh --check  # Check if registry is up-to-date (exit 1 if stale)
#   ./generate-subagent-registry.sh --help   # Show usage
#   ./generate-subagent-registry.sh --generate-only --agents-dir <path>  # Output to stdout (for testing)
#
# Supports --source-only to export functions for testing
#

set -euo pipefail

# Script paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"
DEFAULT_AGENTS_DIR="$PROJECT_ROOT/.claude/agents"

# Marker comments
BEGIN_MARKER="<!-- BEGIN SUBAGENT REGISTRY -->"
END_MARKER="<!-- END SUBAGENT REGISTRY -->"

# ============================================================================
# Frontmatter Extraction Functions
# ============================================================================

# Extract a single field value from YAML frontmatter
# Usage: extract_field <file> <field_name>
extract_field() {
    local file="$1"
    local field="$2"

    # Check if file has valid frontmatter (starts with ---, handle Windows line endings)
    if ! head -1 "$file" 2>/dev/null | tr -d '\r' | grep -q '^---$'; then
        echo ""
        return 0
    fi

    # Extract ONLY the first frontmatter block (between first two --- markers)
    # Use awk to stop at exactly the second ---
    tr -d '\r' < "$file" 2>/dev/null | awk '
        /^---$/ { count++; if (count == 1) { next } if (count == 2) { exit } }
        count == 1 { print }
    ' | \
        grep -m1 "^${field}:" | \
        sed "s/^${field}: *//" | \
        sed 's/^"//' | sed 's/"$//'
}

# Extract array items from YAML frontmatter
# Usage: extract_array <file> <field_name>
extract_array() {
    local file="$1"
    local field="$2"

    # Check if file has valid frontmatter (handle Windows line endings)
    if ! head -1 "$file" 2>/dev/null | tr -d '\r' | grep -q '^---$'; then
        echo ""
        return 0
    fi

    # Extract ONLY the first frontmatter block (between first two --- markers)
    # Use awk to stop at exactly the second ---
    local frontmatter
    frontmatter=$(tr -d '\r' < "$file" 2>/dev/null | awk '
        /^---$/ { count++; if (count == 1) { next } if (count == 2) { exit } }
        count == 1 { print }
    ')

    # Check if field exists
    if ! echo "$frontmatter" | grep -q "^${field}:"; then
        echo ""
        return 0
    fi

    # Extract array items (lines starting with "  - ")
    # Stop at the next field (line starting with letter) or end
    echo "$frontmatter" | \
        sed -n "/^${field}:/,/^[a-z]/p" | \
        grep -E '^  - ' | \
        sed 's/^  - //' | \
        sed 's/^"//' | sed 's/"$//'
}

# ============================================================================
# Registry Generation Functions
# ============================================================================

# Generate the agent table rows
# Usage: generate_agent_table <agents_dir>
generate_agent_table() {
    local agents_dir="$1"
    local output=""

    # Get all agent files sorted alphabetically
    for agent_file in $(find "$agents_dir" -name "*.md" -type f 2>/dev/null | sort); do
        local name
        local description
        local tools

        name=$(extract_field "$agent_file" "name")
        description=$(extract_field "$agent_file" "description")
        tools=$(extract_field "$agent_file" "tools")

        # Skip files without valid name
        if [ -z "$name" ]; then
            echo "WARNING: Skipping $agent_file (no name field)" >&2
            continue
        fi

        # Truncate description if too long (max 80 chars for table)
        if [ ${#description} -gt 80 ]; then
            description="${description:0:77}..."
        fi

        # Clean up tools (handle both comma-separated and YAML list format)
        if [ -z "$tools" ]; then
            tools="(none)"
        fi

        output+="| $name | $description | $tools |"$'\n'
    done

    echo -n "$output"
}

# Generate the trigger mapping section
# Usage: generate_trigger_mapping <agents_dir>
generate_trigger_mapping() {
    local agents_dir="$1"
    local output=""
    declare -A trigger_agents  # Track triggers to detect duplicates

    # Get all agent files sorted alphabetically
    for agent_file in $(find "$agents_dir" -name "*.md" -type f 2>/dev/null | sort); do
        local name
        local triggers

        name=$(extract_field "$agent_file" "name")
        triggers=$(extract_array "$agent_file" "proactive_triggers")

        # Skip files without name or triggers
        if [ -z "$name" ] || [ -z "$triggers" ]; then
            continue
        fi

        # Process each trigger
        while IFS= read -r trigger; do
            if [ -n "$trigger" ]; then
                # Check for duplicate triggers
                if [ -n "${trigger_agents[$trigger]:-}" ]; then
                    echo "WARNING: Duplicate trigger '$trigger' found in $name (already in ${trigger_agents[$trigger]})" >&2
                else
                    trigger_agents["$trigger"]="$name"
                    output+="| $trigger | $name |"$'\n'
                fi
            fi
        done <<< "$triggers"
    done

    echo -n "$output"
}

# Generate the complete registry section
# Usage: generate_registry <agents_dir>
generate_registry() {
    local agents_dir="$1"

    local agent_table
    local trigger_mapping

    agent_table=$(generate_agent_table "$agents_dir")
    trigger_mapping=$(generate_trigger_mapping "$agents_dir")

    cat << EOF
$BEGIN_MARKER
## Subagent Registry

*Auto-generated from .claude/agents/*.md - DO NOT EDIT MANUALLY*

| Agent | Description | Tools |
|-------|-------------|-------|
$agent_table
### Proactive Trigger Mapping

| Trigger Pattern | Recommended Agent |
|-----------------|-------------------|
$trigger_mapping$END_MARKER
EOF
}

# ============================================================================
# CLAUDE.md Update Functions
# ============================================================================

# Check if CLAUDE.md has registry markers
has_markers() {
    grep -q "$BEGIN_MARKER" "$CLAUDE_MD" && grep -q "$END_MARKER" "$CLAUDE_MD"
}

# Extract current registry from CLAUDE.md
get_current_registry() {
    if has_markers; then
        sed -n "/$BEGIN_MARKER/,/$END_MARKER/p" "$CLAUDE_MD"
    else
        echo ""
    fi
}

# Update CLAUDE.md with new registry
update_claude_md() {
    local new_registry="$1"

    if ! has_markers; then
        echo "ERROR: CLAUDE.md does not have registry markers" >&2
        echo "Add these markers to CLAUDE.md:" >&2
        echo "  $BEGIN_MARKER" >&2
        echo "  $END_MARKER" >&2
        return 2
    fi

    # Create temp file
    local temp_file
    temp_file=$(mktemp)

    # Replace content between markers
    awk -v begin="$BEGIN_MARKER" -v end="$END_MARKER" -v new="$new_registry" '
        $0 ~ begin { print new; skip=1; next }
        $0 ~ end { skip=0; next }
        !skip { print }
    ' "$CLAUDE_MD" > "$temp_file"

    # Move temp file to CLAUDE.md
    mv "$temp_file" "$CLAUDE_MD"
}

# ============================================================================
# Main Entry Point
# ============================================================================

show_help() {
    cat << EOF
Subagent Registry Generator

Usage:
  $(basename "$0")                  Update CLAUDE.md registry
  $(basename "$0") --check          Check if registry is up-to-date (exit 1 if stale)
  $(basename "$0") --help           Show this help message
  $(basename "$0") --generate-only  Output registry to stdout (for testing)

Options:
  --agents-dir <path>  Use custom agents directory (default: .claude/agents)
  --source-only        Export functions only (for testing)

Exit Codes:
  0  Success (or up-to-date in check mode)
  1  Registry is stale (check mode only)
  2  Error (missing markers, file errors)
EOF
}

main() {
    local check_mode=false
    local generate_only=false
    local agents_dir="$DEFAULT_AGENTS_DIR"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --help)
                show_help
                exit 0
                ;;
            --check)
                check_mode=true
                shift
                ;;
            --generate-only)
                generate_only=true
                shift
                ;;
            --agents-dir)
                agents_dir="$2"
                shift 2
                ;;
            --source-only)
                # Just export functions, don't run main
                return 0
                ;;
            *)
                echo "Unknown option: $1" >&2
                show_help
                exit 2
                ;;
        esac
    done

    # Validate agents directory
    if [ ! -d "$agents_dir" ]; then
        echo "ERROR: Agents directory not found: $agents_dir" >&2
        exit 2
    fi

    # Generate registry
    local new_registry
    new_registry=$(generate_registry "$agents_dir")

    # Generate-only mode: just output and exit
    if [ "$generate_only" = true ]; then
        echo "$new_registry"
        exit 0
    fi

    # Check mode: compare and exit with appropriate code
    if [ "$check_mode" = true ]; then
        if ! has_markers; then
            echo "ERROR: CLAUDE.md does not have registry markers" >&2
            exit 2
        fi

        local current_registry
        current_registry=$(get_current_registry)

        if [ "$current_registry" = "$new_registry" ]; then
            echo "Registry is up-to-date"
            exit 0
        else
            echo "Registry is out of date - run: bash scripts/generate-subagent-registry.sh" >&2
            exit 1
        fi
    fi

    # Update mode: replace registry in CLAUDE.md
    update_claude_md "$new_registry"
    echo "Registry updated in CLAUDE.md"
}

# Only run main if not being sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]] || [[ "${1:-}" != "--source-only" ]]; then
    main "$@"
fi
