#!/bin/bash
#
# Session Catalog Functions for STORY-223
# Provides session file cataloging, dependency graph building, and session chain tracking
#
# Usage: source .claude/scripts/session_catalog.sh
#
# Functions:
#   catalog_session_files(directory)    - Map plans to stories to artifacts (AC#1)
#   build_dependency_graph(directory)   - Build file dependency graph (AC#2)
#   track_session_chains(directory)     - Track session continuity chains (AC#3)
#

# ============================================================================
# AC#1: Catalog Session Files
# Maps plan files → story references → associated artifacts
# ============================================================================
catalog_session_files() {
    local directory="${1:-.}"

    # Initialize JSON structure
    local plan_to_story_map="{}"
    local story_to_artifacts_map="{}"
    local story_to_plans_map="{}"
    local files_array="[]"

    # Find all plan files
    local plan_files=()
    while IFS= read -r -d '' file; do
        plan_files+=("$file")
    done < <(find "$directory/plans" -name "*.md" -type f -print0 2>/dev/null)

    # Process each plan file
    for plan_file in "${plan_files[@]}"; do
        local plan_id
        plan_id=$(basename "$plan_file" .md)

        # Extract story references from YAML frontmatter
        local story_refs=()
        while IFS= read -r line; do
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*(STORY-[0-9]+) ]]; then
                story_refs+=("${BASH_REMATCH[1]}")
            fi
        done < <(sed -n '/^related_stories:/,/^[^[:space:]-]/p' "$plan_file" 2>/dev/null)

        # Build plan_to_story_map entry
        if [[ ${#story_refs[@]} -gt 0 ]]; then
            local stories_json=""
            for story in "${story_refs[@]}"; do
                [[ -n "$stories_json" ]] && stories_json+=","
                stories_json+="\"$story\""
            done
            plan_to_story_map=$(echo "$plan_to_story_map" | jq -c --arg plan "$plan_id" --argjson stories "[$stories_json]" '. + {($plan): $stories}' 2>/dev/null || echo "$plan_to_story_map")

            # Build story_to_plans_map (reverse mapping)
            for story in "${story_refs[@]}"; do
                story_to_plans_map=$(echo "$story_to_plans_map" | jq -c --arg story "$story" --arg plan "$plan_id" 'if .[$story] then .[$story] += [$plan] else . + {($story): [$plan]} end' 2>/dev/null || echo "$story_to_plans_map")
            done
        fi

        # Add to files array
        files_array=$(echo "$files_array" | jq -c --arg path "$plan_file" '. + [{"path": $path, "type": "plan"}]' 2>/dev/null || echo "$files_array")
    done

    # Find artifacts and map to stories
    local artifact_dirs=()
    while IFS= read -r -d '' dir; do
        artifact_dirs+=("$dir")
    done < <(find "$directory/artifacts" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null)

    for artifact_dir in "${artifact_dirs[@]}"; do
        local story_id
        story_id=$(basename "$artifact_dir")

        # Find artifact files in this directory
        local artifact_files=()
        while IFS= read -r -d '' file; do
            local filename
            filename=$(basename "$file")
            artifact_files+=("$filename")

            # Add to files array
            files_array=$(echo "$files_array" | jq -c --arg path "$file" '. + [{"path": $path, "type": "artifact"}]' 2>/dev/null || echo "$files_array")
        done < <(find "$artifact_dir" -type f -print0 2>/dev/null)

        # Build story_to_artifacts_map
        if [[ ${#artifact_files[@]} -gt 0 ]]; then
            local artifacts_json=""
            for artifact in "${artifact_files[@]}"; do
                [[ -n "$artifacts_json" ]] && artifacts_json+=","
                artifacts_json+="\"$artifact\""
            done
            story_to_artifacts_map=$(echo "$story_to_artifacts_map" | jq -c --arg story "$story_id" --argjson artifacts "[$artifacts_json]" '. + {($story): $artifacts}' 2>/dev/null || echo "$story_to_artifacts_map")
        fi
    done

    # Find session files
    while IFS= read -r -d '' file; do
        files_array=$(echo "$files_array" | jq -c --arg path "$file" '. + [{"path": $path, "type": "session"}]' 2>/dev/null || echo "$files_array")
    done < <(find "$directory/sessions" -name "*.json" -type f -print0 2>/dev/null)

    # Output final JSON
    jq -n -c \
        --argjson plan_to_story "$plan_to_story_map" \
        --argjson story_to_artifacts "$story_to_artifacts_map" \
        --argjson story_to_plans "$story_to_plans_map" \
        --argjson files "$files_array" \
        '{
            "plan_to_story_map": $plan_to_story,
            "story_to_artifacts_map": $story_to_artifacts,
            "story_to_plans_map": $story_to_plans,
            "files": $files
        }'
}

# ============================================================================
# AC#2: Build Dependency Graph
# Analyzes file references and builds dependency graph
# ============================================================================
build_dependency_graph() {
    local directory="${1:-.}"

    local dependencies="[]"
    local nodes="{}"
    local circular_dependencies="[]"

    # Find all relevant files
    local all_files=()
    while IFS= read -r -d '' file; do
        all_files+=("$file")
    done < <(find "$directory" \( -name "*.md" -o -name "*.json" -o -name "*.sh" \) -type f -print0 2>/dev/null)

    # Build nodes map
    for file in "${all_files[@]}"; do
        local file_id
        file_id=$(basename "$file")
        local file_type="unknown"

        case "$file" in
            */plans/*) file_type="plan" ;;
            */sessions/*) file_type="session" ;;
            */artifacts/*) file_type="artifact" ;;
            */Stories/*) file_type="story" ;;
            *) file_type="other" ;;
        esac

        nodes=$(echo "$nodes" | jq -c --arg id "$file_id" --arg path "$file" --arg type "$file_type" '. + {($id): {"path": $path, "type": $type}}' 2>/dev/null || echo "$nodes")
    done

    # Analyze dependencies
    for file in "${all_files[@]}"; do
        local source_id
        source_id=$(basename "$file")

        # Check for references to other files
        for target_file in "${all_files[@]}"; do
            local target_id
            target_id=$(basename "$target_file")

            # Skip self-references
            [[ "$source_id" == "$target_id" ]] && continue

            # Check if source file references target
            if grep -q "$target_id" "$file" 2>/dev/null; then
                local dep_type="reference"

                # Classify dependency type
                if [[ "$file" == */plans/* && "$target_file" == */Stories/* ]]; then
                    dep_type="plan_to_story"
                elif [[ "$file" == */sessions/* && "$target_file" == */sessions/* ]]; then
                    dep_type="session_chain"
                fi

                dependencies=$(echo "$dependencies" | jq -c --arg source "$source_id" --arg target "$target_id" --arg type "$dep_type" '. + [{"source": $source, "target": $target, "type": $type}]' 2>/dev/null || echo "$dependencies")
            fi
        done
    done

    # Detect circular dependencies (simple 2-node cycles)
    local dep_pairs=()
    while IFS= read -r line; do
        dep_pairs+=("$line")
    done < <(echo "$dependencies" | jq -r '.[] | "\(.source)|\(.target)"' 2>/dev/null)

    for pair in "${dep_pairs[@]}"; do
        IFS='|' read -r source target <<< "$pair"
        # Check if reverse edge exists
        for check_pair in "${dep_pairs[@]}"; do
            IFS='|' read -r check_source check_target <<< "$check_pair"
            if [[ "$check_source" == "$target" && "$check_target" == "$source" ]]; then
                circular_dependencies=$(echo "$circular_dependencies" | jq -c --arg a "$source" --arg b "$target" 'if . | map(select(contains([$a, $b]))) | length == 0 then . + [[$a, $b]] else . end' 2>/dev/null || echo "$circular_dependencies")
            fi
        done
    done

    # Output final JSON
    jq -n -c \
        --argjson deps "$dependencies" \
        --argjson nodes "$nodes" \
        --argjson circular "$circular_dependencies" \
        '{
            "dependencies": $deps,
            "nodes": $nodes,
            "circular_dependencies": $circular
        }'
}

# ============================================================================
# AC#3: Track Session Chains
# Identifies parent-child relationships via parentUuid
# ============================================================================
track_session_chains() {
    local session_directory="${1:-.}"

    local session_chains="[]"
    local root_sessions="[]"
    local orphan_sessions="[]"

    # Find all session files
    local session_files=()
    while IFS= read -r -d '' file; do
        session_files+=("$file")
    done < <(find "$session_directory" -name "*.json" -type f -print0 2>/dev/null)

    # Build session map: uuid -> {file, parentUuid}
    declare -A session_map
    declare -A parent_map
    declare -A children_map

    for file in "${session_files[@]}"; do
        local uuid parent_uuid
        uuid=$(jq -r '.uuid // empty' "$file" 2>/dev/null)
        parent_uuid=$(jq -r '.parentUuid // empty' "$file" 2>/dev/null)

        [[ -z "$uuid" ]] && continue

        session_map["$uuid"]="$file"

        if [[ -n "$parent_uuid" ]]; then
            parent_map["$uuid"]="$parent_uuid"
            children_map["$parent_uuid"]+="$uuid "
        fi
    done

    # Identify root sessions (no parent) and orphans (parent not found)
    for uuid in "${!session_map[@]}"; do
        local parent="${parent_map[$uuid]:-}"

        if [[ -z "$parent" ]]; then
            # No parent = root session
            root_sessions=$(echo "$root_sessions" | jq -c --arg uuid "$uuid" '. + [$uuid]' 2>/dev/null || echo "$root_sessions")
        elif [[ -z "${session_map[$parent]:-}" ]]; then
            # Parent specified but not found = orphan
            orphan_sessions=$(echo "$orphan_sessions" | jq -c --arg uuid "$uuid" '. + [$uuid]' 2>/dev/null || echo "$orphan_sessions")
        fi
    done

    # Build session chains starting from each root
    build_chain() {
        local root_uuid="$1"
        local depth=0
        local nodes="[\"$root_uuid\"]"
        local current="$root_uuid"
        local queue=("$root_uuid")
        local visited=("$root_uuid")

        while [[ ${#queue[@]} -gt 0 ]]; do
            current="${queue[0]}"
            queue=("${queue[@]:1}")

            local children="${children_map[$current]:-}"
            for child in $children; do
                # Check if already visited (prevent cycles)
                local already_visited=false
                for v in "${visited[@]}"; do
                    [[ "$v" == "$child" ]] && already_visited=true && break
                done

                if [[ "$already_visited" == "false" ]]; then
                    visited+=("$child")
                    queue+=("$child")
                    nodes=$(echo "$nodes" | jq -c --arg uuid "$child" '. + [$uuid]' 2>/dev/null || echo "$nodes")
                    ((depth++))
                fi
            done
        done

        echo "{\"root\": \"$root_uuid\", \"nodes\": $nodes, \"depth\": $depth}"
    }

    # Build chains from each root
    while IFS= read -r root; do
        [[ -z "$root" ]] && continue
        local chain
        chain=$(build_chain "$root")
        session_chains=$(echo "$session_chains" | jq -c --argjson chain "$chain" '. + [$chain]' 2>/dev/null || echo "$session_chains")
    done < <(echo "$root_sessions" | jq -r '.[]' 2>/dev/null)

    # Output final JSON
    jq -n -c \
        --argjson chains "$session_chains" \
        --argjson roots "$root_sessions" \
        --argjson orphans "$orphan_sessions" \
        '{
            "session_chains": $chains,
            "root_sessions": $roots,
            "orphan_sessions": $orphans
        }'
}

# ============================================================================
# Export functions
# ============================================================================
export -f catalog_session_files
export -f build_dependency_graph
export -f track_session_chains
