#!/bin/bash
# Plan File Knowledge Base Functions
# STORY-222: Extract Plan File Knowledge Base for Decision Archive
#
# Provides 4 functions for plan file parsing and decision archive building:
# - extract_yaml_frontmatter: Parse YAML frontmatter from plan files
# - extract_story_ids: Extract STORY-NNN patterns with context
# - build_decision_archive: Build bidirectional story<->plan mapping
# - query_archive: Query archive for related plan files

set -euo pipefail

# =============================================================================
# Helper Functions
# =============================================================================

# Validate that a file exists before processing
# Usage: validate_file_exists "$file_path"
# Returns: 0 if exists, 1 if not (also outputs JSON error)
validate_file_exists() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo '{"error": "File not found"}'
        return 1
    fi
    return 0
}

# Escape special characters for JSON output
# Usage: json_escape "$string"
# Handles: backslash, quotes, newlines, carriage returns, tabs
json_escape() {
    local str="$1"
    str="${str//\\/\\\\}"
    str="${str//\"/\\\"}"
    str="${str//$'\n'/\\n}"
    str="${str//$'\r'/\\r}"
    str="${str//$'\t'/\\t}"
    echo "$str"
}

# Build a JSON array from newline-separated lines
# Usage: json_array_from_lines < input_lines
# Example: echo -e "STORY-001\nSTORY-002" | json_array_from_lines
json_array_from_lines() {
    awk 'BEGIN{printf "["} NR>1{printf ", "} {printf "\"%s\"", $0} END{printf "]"}'
}

# Parse a specific YAML field from content
# Usage: parse_yaml_field "$yaml_content" "status"
# Returns: field value without quotes
parse_yaml_field() {
    local content="$1"
    local field_name="$2"
    echo "$content" | grep -E "^${field_name}:" | sed "s/^${field_name}:[[:space:]]*//" | tr -d '"' | tr -d "'" || echo ""
}

# =============================================================================
# Function 1: extract_yaml_frontmatter
# AC#1: Parse YAML frontmatter from plan files
# SM-010: Parse YAML frontmatter from plan files (Critical)
# =============================================================================
extract_yaml_frontmatter() {
    local plan_file="$1"

    validate_file_exists "$plan_file" || return 1

    # Check if file starts with ---
    local first_line
    first_line=$(head -n1 "$plan_file" 2>/dev/null || echo "")

    if [[ "$first_line" != "---" ]]; then
        # No YAML frontmatter - return empty/default
        echo '{"status": "", "created": "", "author": "", "related_stories": []}'
        return 0
    fi

    # Extract content between first and second ---
    local yaml_content
    yaml_content=$(awk 'BEGIN{found=0} /^---$/{found++; if(found==2) exit; next} found==1{print}' "$plan_file" 2>/dev/null || echo "")

    if [[ -z "$yaml_content" ]]; then
        echo '{"status": "", "created": "", "author": "", "related_stories": []}'
        return 0
    fi

    # Parse individual fields from YAML using helper
    local status
    status=$(parse_yaml_field "$yaml_content" "status")

    local created
    created=$(parse_yaml_field "$yaml_content" "created")

    local author
    author=$(parse_yaml_field "$yaml_content" "author")

    # Extract related_stories array
    local related_stories
    related_stories=$(parse_related_stories "$yaml_content")

    # Output JSON
    printf '{"status": "%s", "created": "%s", "author": "%s", "related_stories": %s}\n' \
        "$status" "$created" "$author" "$related_stories"
}

# Helper to parse related_stories field (handles inline and multiline formats)
parse_related_stories() {
    local yaml_content="$1"
    local related_stories_field
    related_stories_field=$(echo "$yaml_content" | grep -E "^related_stories:" || echo "")

    if [[ -z "$related_stories_field" ]]; then
        echo "[]"
        return 0
    fi

    # Try to extract STORY-XXX patterns from the field
    local stories_array
    stories_array=$(echo "$yaml_content" | grep -E "^related_stories:" | \
        sed 's/^related_stories:[[:space:]]*//' | \
        grep -oE 'STORY-[0-9]+' | \
        json_array_from_lines)

    # If no patterns found, return empty array
    if [[ -z "$stories_array" || "$stories_array" == "[]" ]]; then
        echo "[]"
    else
        echo "$stories_array"
    fi
}

# =============================================================================
# Function 2: extract_story_ids
# AC#2: Extract STORY-NNN patterns with surrounding context
# SM-011: Extract STORY-NNN patterns with regex (High)
# =============================================================================
extract_story_ids() {
    local plan_file="$1"

    validate_file_exists "$plan_file" || return 1

    # Extract all STORY-NNN patterns (3+ digits)
    local story_ids
    story_ids=$(grep -oE 'STORY-[0-9]{3,}' "$plan_file" 2>/dev/null | sort -u || echo "")

    if [[ -z "$story_ids" ]]; then
        echo '{"story_ids": [], "contexts": {}}'
        return 0
    fi

    # Build JSON array of story IDs using helper
    local ids_json
    ids_json=$(echo "$story_ids" | json_array_from_lines)

    # Build contexts object with surrounding text for each story ID
    local contexts_json="{"
    local is_first_id_entry=true

    while IFS= read -r story_id; do
        if [[ -z "$story_id" ]]; then continue; fi

        # Get line with context (extract the line containing the story ID)
        local context
        context=$(grep -m1 "$story_id" "$plan_file" 2>/dev/null | head -c 200 | tr '\n' ' ' | tr '"' "'" || echo "")

        if [[ "$is_first_id_entry" == "true" ]]; then
            is_first_id_entry=false
        else
            contexts_json+=", "
        fi
        contexts_json+="\"$story_id\": \"$context\""
    done <<< "$story_ids"

    contexts_json+="}"

    printf '{"story_ids": %s, "contexts": %s}\n' "$ids_json" "$contexts_json"
}

# =============================================================================
# Function 3: build_decision_archive
# AC#3: Build bidirectional story<->decision mapping
# SM-012: Build story→decision bidirectional mapping (High)
# NFR-010: Index 350+ plan files within 10 seconds
# =============================================================================
# Process a single plan file and update mappings
process_plan_file() {
    local plan_file="$1"
    local -n story_to_plans_ref=$2
    local -n plan_to_stories_ref=$3
    local -n plan_metadata_ref=$4

    local plan_name
    plan_name=$(basename "$plan_file")

    # Extract frontmatter
    local frontmatter
    frontmatter=$(extract_yaml_frontmatter "$plan_file")
    plan_metadata_ref["$plan_name"]="$frontmatter"

    # Extract story IDs
    local story_ids
    story_ids=$(grep -oE 'STORY-[0-9]+' "$plan_file" 2>/dev/null | sort -u || echo "")

    # Build plan_to_stories mapping using helper
    if [[ -n "$story_ids" ]]; then
        local stories_array
        stories_array=$(echo "$story_ids" | json_array_from_lines)
        plan_to_stories_ref["$plan_name"]="$stories_array"

        # Build story_to_plans mapping (bidirectional)
        while IFS= read -r story_id; do
            if [[ -n "$story_id" ]]; then
                if [[ -n "${story_to_plans_ref[$story_id]:-}" ]]; then
                    story_to_plans_ref["$story_id"]+=", \"$plan_name\""
                else
                    story_to_plans_ref["$story_id"]="\"$plan_name\""
                fi
            fi
        done <<< "$story_ids"
    else
        plan_to_stories_ref["$plan_name"]="[]"
    fi
}

# Build JSON object from associative array
build_json_object_from_array() {
    local -n array_ref=$1
    local json_str="{"
    local is_first=true

    for key in "${!array_ref[@]}"; do
        if [[ "$is_first" == "true" ]]; then
            is_first=false
        else
            json_str+=", "
        fi
        json_str+="\"$key\": ${array_ref[$key]}"
    done
    json_str+="}"
    echo "$json_str"
}

# Build JSON array of plan names from story_to_plans mapping
build_story_to_plans_json() {
    local -n array_ref=$1
    local json_str="{"
    local is_first=true

    for story_id in "${!array_ref[@]}"; do
        if [[ "$is_first" == "true" ]]; then
            is_first=false
        else
            json_str+=", "
        fi
        json_str+="\"$story_id\": [${array_ref[$story_id]}]"
    done
    json_str+="}"
    echo "$json_str"
}

build_decision_archive() {
    local plans_dir="$1"
    local archive_dir="$2"

    if [[ ! -d "$plans_dir" ]]; then
        echo '{"error": "Plans directory not found"}'
        return 1
    fi

    # Create archive directory if it doesn't exist
    mkdir -p "$archive_dir"

    # Initialize data structures
    declare -A story_to_plans
    declare -A plan_to_stories
    declare -A plan_metadata

    # Process all plan files
    local plan_count=0
    while IFS= read -r -d '' plan_file; do
        process_plan_file "$plan_file" story_to_plans plan_to_stories plan_metadata
        ((plan_count++))
    done < <(find "$plans_dir" -name "*.md" -type f -print0 2>/dev/null)

    # Build final JSON using helpers
    local story_to_plans_json
    story_to_plans_json=$(build_story_to_plans_json story_to_plans)

    local plan_to_stories_json
    plan_to_stories_json=$(build_json_object_from_array plan_to_stories)

    local plan_metadata_json
    plan_metadata_json=$(build_json_object_from_array plan_metadata)

    local archive_json
    archive_json="{\"story_to_plans\": $story_to_plans_json, \"plan_to_stories\": $plan_to_stories_json, \"metadata\": $plan_metadata_json}"

    # Write archive to file
    echo "$archive_json" > "$archive_dir/decision_archive.json"

    # Return summary
    printf '{"status": "success", "plan_count": %d, "archive_path": "%s/decision_archive.json"}\n' \
        "$plan_count" "$archive_dir"
}

# =============================================================================
# Function 4: query_archive
# AC#4: Query archive for related plan files
# =============================================================================
# Extract plans for a story from archive content
extract_plans_from_archive() {
    local archive_content="$1"
    local story_id="$2"

    # Try to extract story_to_plans entry
    local plans_array
    plans_array=$(echo "$archive_content" | grep -oE "\"$story_id\": *\[[^]]*\]" | \
        sed 's/.*\[\([^]]*\)\].*/[\1]/' | head -1 || echo "[]")

    # If not found, try alternate pattern
    if [[ -z "$plans_array" || "$plans_array" == "[]" ]]; then
        local story_entry
        story_entry=$(echo "$archive_content" | grep -o "\"$story_id\": \[[^]]*\]" || echo "")
        if [[ -n "$story_entry" ]]; then
            plans_array=$(echo "$story_entry" | sed 's/.*\[\(.*\)\]/[\1]/')
        fi
    fi

    echo "$plans_array"
}

query_archive() {
    local archive_dir="$1"
    local story_id="$2"

    local archive_file="$archive_dir/decision_archive.json"

    if [[ ! -f "$archive_file" ]]; then
        echo '{"error": "Archive not found", "story_id": "'"$story_id"'", "plans": []}'
        return 1
    fi

    # Read archive
    local archive_content
    archive_content=$(cat "$archive_file")

    # Extract plans using helper
    local plans_array
    plans_array=$(extract_plans_from_archive "$archive_content" "$story_id")

    if [[ -z "$plans_array" || "$plans_array" == "[]" ]]; then
        echo '{"story_id": "'"$story_id"'", "plans": [], "count": 0}'
        return 0
    fi

    # Count plans
    local count
    count=$(echo "$plans_array" | grep -oE '"[^"]*\.md"' | wc -l || echo "0")

    # Build result with plan details
    local result='{"story_id": "'"$story_id"'", "plans": '"$plans_array"', "count": '"$count"'}'

    echo "$result"
}

# =============================================================================
# Helper: Get archive statistics
# =============================================================================
get_archive_stats() {
    local archive_dir="$1"
    local archive_file="$archive_dir/decision_archive.json"

    if [[ ! -f "$archive_file" ]]; then
        echo '{"error": "Archive not found"}'
        return 1
    fi

    local story_count
    story_count=$(grep -oE '"STORY-[0-9]+":' "$archive_file" | sort -u | wc -l || echo "0")

    local plan_count
    plan_count=$(grep -oE '"[^"]+\.md":' "$archive_file" | sort -u | wc -l || echo "0")

    printf '{"story_count": %d, "plan_count": %d}\n' "$story_count" "$plan_count"
}
