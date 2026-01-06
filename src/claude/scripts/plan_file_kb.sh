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

# =============================================================================
# STORY-233: Search and Retrieve Decision Context Functions
# =============================================================================

# =============================================================================
# Function 5: search_by_story_id
# AC#1: Search decisions by story ID
# =============================================================================
search_by_story_id() {
    local index_dir="$1"
    local story_id="$2"

    local index_file="$index_dir/searchable_index.json"

    # Validate index exists
    if [[ ! -f "$index_file" ]]; then
        echo '{"error": "Index not found", "story_id": "'"$story_id"'", "decisions": [], "count": 0}'
        return 1
    fi

    # Validate story ID format
    if [[ ! "$story_id" =~ ^STORY-[0-9]+$ ]]; then
        echo '{"error": "Invalid story ID format", "story_id": "'"$story_id"'", "decisions": [], "count": 0}'
        return 1
    fi

    # Flatten JSON to single line for regex parsing
    local index_content
    index_content=$(cat "$index_file" | tr '\n' ' ' | tr -s ' ')

    # Check for story_index first (optimized path)
    local plan_files
    plan_files=$(echo "$index_content" | grep -oE "\"$story_id\": *\[[^\]]*\]" | sed 's/.*\[\([^]]*\)\]/\1/' | tr -d '"' | tr ',' '\n' | tr -d ' ' | grep -v '^$')

    if [[ -z "$plan_files" ]]; then
        # Fallback: search through plans section for matching story_id
        # Extract all plan file names
        local all_plans
        all_plans=$(echo "$index_content" | grep -oE '"[A-Za-z0-9_-]+\.md": *\{' | sed 's/": *{//' | tr -d '"')

        while IFS= read -r pfile; do
            [[ -z "$pfile" ]] && continue
            # Check if this plan has the target story_id
            if echo "$index_content" | grep -qE "\"$pfile\": *\{[^}]*\"story_id\": *\"$story_id\""; then
                plan_files+="$pfile"$'\n'
            fi
        done <<< "$all_plans"
    fi

    if [[ -z "$plan_files" ]]; then
        echo '{"story_id": "'"$story_id"'", "decisions": [], "count": 0}'
        return 0
    fi

    # Build decisions array
    local decisions="["
    local is_first=true
    local count=0

    while IFS= read -r plan_file; do
        [[ -z "$plan_file" ]] && continue

        # Extract plan data block (everything between this plan and next plan or end)
        local plan_data
        plan_data=$(echo "$index_content" | grep -oP "\"$plan_file\": *\{[^}]+\}" | head -1)

        if [[ -n "$plan_data" ]]; then
            # Extract fields
            local decision=$(echo "$plan_data" | grep -oE '"decision": *"[^"]*"' | sed 's/"decision": *"//' | sed 's/"$//')
            local status=$(echo "$plan_data" | grep -oE '"status": *"[^"]*"' | sed 's/"status": *"//' | sed 's/"$//')
            local created=$(echo "$plan_data" | grep -oE '"created": *"[^"]*"' | sed 's/"created": *"//' | sed 's/"$//')

            if [[ "$is_first" == "true" ]]; then
                is_first=false
            else
                decisions+=", "
            fi

            decisions+="{\"plan_file\": \"$plan_file\", \"decision\": \"$decision\", \"status\": \"$status\", \"created\": \"$created\"}"
            ((count++))
        fi
    done <<< "$plan_files"

    decisions+="]"

    printf '{"story_id": "%s", "decisions": %s, "count": %d}\n' "$story_id" "$decisions" "$count"
}

# =============================================================================
# Function 6: search_by_date_range
# AC#2: Search decisions by date range
# =============================================================================
search_by_date_range() {
    local index_dir="$1"
    local start_date="$2"
    local end_date="$3"

    local index_file="$index_dir/searchable_index.json"

    # Validate index exists
    if [[ ! -f "$index_file" ]]; then
        echo '{"error": "Index not found", "start_date": "'"$start_date"'", "end_date": "'"$end_date"'", "decisions": [], "count": 0}'
        return 1
    fi

    # Validate date format (YYYY-MM-DD)
    if [[ ! "$start_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo '{"error": "Invalid start date format", "start_date": "'"$start_date"'", "end_date": "'"$end_date"'", "decisions": [], "count": 0}'
        return 1
    fi

    if [[ ! "$end_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo '{"error": "Invalid end date format", "start_date": "'"$start_date"'", "end_date": "'"$end_date"'", "decisions": [], "count": 0}'
        return 1
    fi

    # Handle reversed dates
    if [[ "$start_date" > "$end_date" ]]; then
        echo '{"error": "Start date after end date", "start_date": "'"$start_date"'", "end_date": "'"$end_date"'", "decisions": [], "count": 0}'
        return 1
    fi

    # Flatten JSON to single line for regex parsing
    local index_content
    index_content=$(cat "$index_file" | tr '\n' ' ' | tr -s ' ')

    # Extract all plans with their dates
    local decisions="["
    local is_first=true
    local count=0

    # Get all plan entries
    local plan_files
    plan_files=$(echo "$index_content" | grep -oE '"[A-Za-z0-9_-]+\.md":' | tr -d '":')

    while IFS= read -r plan_file; do
        [[ -z "$plan_file" ]] && continue

        # Extract plan data
        local plan_data
        plan_data=$(echo "$index_content" | grep -oP "\"$plan_file\": *\{[^}]+\}" | head -1)

        if [[ -n "$plan_data" ]]; then
            local created=$(echo "$plan_data" | grep -oE '"created": *"[^"]*"' | sed 's/"created": *"//' | sed 's/"$//')

            # Check if date is in range (inclusive)
            # String comparison: dates in YYYY-MM-DD format can be compared lexicographically
            if [[ -n "$created" ]] && [[ ! "$created" < "$start_date" ]] && [[ ! "$created" > "$end_date" ]]; then
                local decision=$(echo "$plan_data" | grep -oE '"decision": *"[^"]*"' | sed 's/"decision": *"//' | sed 's/"$//')
                local story_id=$(echo "$plan_data" | grep -oE '"story_id": *"[^"]*"' | sed 's/"story_id": *"//' | sed 's/"$//')
                local status=$(echo "$plan_data" | grep -oE '"status": *"[^"]*"' | sed 's/"status": *"//' | sed 's/"$//')

                if [[ "$is_first" == "true" ]]; then
                    is_first=false
                else
                    decisions+=", "
                fi

                decisions+="{\"plan_file\": \"$plan_file\", \"story_id\": \"$story_id\", \"decision\": \"$decision\", \"status\": \"$status\", \"created\": \"$created\"}"
                ((count++))
            fi
        fi
    done <<< "$plan_files"

    decisions+="]"

    printf '{"start_date": "%s", "end_date": "%s", "decisions": %s, "count": %d}\n' "$start_date" "$end_date" "$decisions" "$count"
}

# =============================================================================
# Function 7: search_by_keywords
# AC#3: Search with relevance ranking
# =============================================================================
search_by_keywords() {
    local index_dir="$1"
    local keywords="$2"

    local index_file="$index_dir/searchable_index.json"

    # Validate index exists
    if [[ ! -f "$index_file" ]]; then
        echo '{"error": "Index not found", "keywords": "'"$keywords"'", "results": [], "count": 0}'
        return 1
    fi

    # Handle empty keywords
    if [[ -z "$keywords" ]]; then
        echo '{"keywords": "", "results": [], "count": 0}'
        return 0
    fi

    # Flatten JSON to single line for regex parsing
    local index_content
    index_content=$(cat "$index_file" | tr '\n' ' ' | tr -s ' ')

    # Convert keywords to lowercase for case-insensitive search
    local keywords_lower
    keywords_lower=$(echo "$keywords" | tr '[:upper:]' '[:lower:]')

    # Split keywords into array
    local -a keyword_array
    IFS=' ' read -ra keyword_array <<< "$keywords_lower"

    # Declare associative array for relevance scores
    declare -A relevance_scores
    declare -A plan_data_cache

    # Get all plan files
    local plan_files
    plan_files=$(echo "$index_content" | grep -oE '"[A-Za-z0-9_-]+\.md":' | tr -d '":')

    while IFS= read -r plan_file; do
        [[ -z "$plan_file" ]] && continue

        # Extract plan data
        local plan_data
        plan_data=$(echo "$index_content" | grep -oP "\"$plan_file\": *\{[^}]+\}" | head -1)

        if [[ -n "$plan_data" ]]; then
            plan_data_cache["$plan_file"]="$plan_data"

            # Get full text for searching (combine all text fields)
            local full_text
            full_text=$(echo "$plan_data" | grep -oE '"(decision|technical_approach|rationale|outcome|full_text)": *"[^"]*"' | sed 's/.*: *"//' | sed 's/"$//' | tr '\n' ' ')
            local full_text_lower
            full_text_lower=$(echo "$full_text" | tr '[:upper:]' '[:lower:]')

            # Calculate relevance score
            local score=0
            for keyword in "${keyword_array[@]}"; do
                # Count occurrences of keyword
                local matches
                matches=$(echo "$full_text_lower" | grep -o "$keyword" | wc -l)
                score=$((score + matches))
            done

            if [[ $score -gt 0 ]]; then
                relevance_scores["$plan_file"]=$score
            fi
        fi
    done <<< "$plan_files"

    # Sort by relevance score (descending)
    local sorted_plans
    sorted_plans=$(for plan in "${!relevance_scores[@]}"; do
        echo "${relevance_scores[$plan]} $plan"
    done | sort -rn | awk '{print $2}')

    # Build results array
    local results="["
    local is_first=true
    local count=0

    while IFS= read -r plan_file; do
        [[ -z "$plan_file" ]] && continue

        local plan_data="${plan_data_cache[$plan_file]}"
        local score="${relevance_scores[$plan_file]}"

        local decision=$(echo "$plan_data" | grep -oE '"decision": *"[^"]*"' | sed 's/"decision": *"//' | sed 's/"$//')
        local story_id=$(echo "$plan_data" | grep -oE '"story_id": *"[^"]*"' | sed 's/"story_id": *"//' | sed 's/"$//')

        if [[ "$is_first" == "true" ]]; then
            is_first=false
        else
            results+=", "
        fi

        results+="{\"plan_file\": \"$plan_file\", \"story_id\": \"$story_id\", \"decision\": \"$decision\", \"relevance_score\": $score}"
        ((count++))
    done <<< "$sorted_plans"

    results+="]"

    printf '{"keywords": "%s", "results": %s, "count": %d}\n' "$keywords" "$results" "$count"
}

# =============================================================================
# Function 8: retrieve_decision_context
# AC#4: Get full decision context
# =============================================================================
retrieve_decision_context() {
    local index_dir="$1"
    local plan_file="$2"

    local index_file="$index_dir/searchable_index.json"

    # Validate index exists
    if [[ ! -f "$index_file" ]]; then
        echo '{"error": "Index not found", "plan_file": "'"$plan_file"'"}'
        return 1
    fi

    # Security: Validate plan_file format to prevent path traversal
    if [[ ! "$plan_file" =~ ^[a-zA-Z0-9_.-]+\.md$ ]]; then
        echo '{"error": "Invalid filename format", "plan_file": "'"$plan_file"'"}'
        return 1
    fi

    # Flatten JSON to single line for regex parsing
    local index_content
    index_content=$(cat "$index_file" | tr '\n' ' ' | tr -s ' ')

    # Extract plan data
    local plan_data
    plan_data=$(echo "$index_content" | grep -oP "\"$plan_file\": *\{[^}]+\}" | head -1)

    if [[ -z "$plan_data" ]]; then
        echo '{"error": "Plan not found", "plan_file": "'"$plan_file"'"}'
        return 1
    fi

    # Extract all fields
    local story_id=$(echo "$plan_data" | grep -oE '"story_id": *"[^"]*"' | sed 's/"story_id": *"//' | sed 's/"$//')
    local status=$(echo "$plan_data" | grep -oE '"status": *"[^"]*"' | sed 's/"status": *"//' | sed 's/"$//')
    local created=$(echo "$plan_data" | grep -oE '"created": *"[^"]*"' | sed 's/"created": *"//' | sed 's/"$//')
    local decision=$(echo "$plan_data" | grep -oE '"decision": *"[^"]*"' | sed 's/"decision": *"//' | sed 's/"$//')
    local technical_approach=$(echo "$plan_data" | grep -oE '"technical_approach": *"[^"]*"' | sed 's/"technical_approach": *"//' | sed 's/"$//')
    local rationale=$(echo "$plan_data" | grep -oE '"rationale": *"[^"]*"' | sed 's/"rationale": *"//' | sed 's/"$//')
    local outcome=$(echo "$plan_data" | grep -oE '"outcome": *"[^"]*"' | sed 's/"outcome": *"//' | sed 's/"$//')

    # Ensure empty strings for missing fields
    story_id="${story_id:-}"
    status="${status:-}"
    created="${created:-}"
    decision="${decision:-}"
    technical_approach="${technical_approach:-}"
    rationale="${rationale:-}"
    outcome="${outcome:-}"

    printf '{"plan_file": "%s", "story_id": "%s", "status": "%s", "created": "%s", "decision": "%s", "rationale": "%s", "outcome": "%s", "technical_approach": "%s"}\n' \
        "$plan_file" "$story_id" "$status" "$created" "$decision" "$rationale" "$outcome" "$technical_approach"
}
