"""
Dependency Graph Analyzer for STORY-093.

Analyzes and validates story dependencies with transitive resolution,
cycle detection, and status validation.

Functions:
    - parse_yaml_frontmatter: Extract YAML from story content
    - validate_story_id: Check STORY-NNN pattern
    - normalize_depends_on: Filter valid/invalid IDs
    - build_dependency_graph: Build adjacency list from story files
    - detect_cycle: DFS cycle detection
    - resolve_transitive_dependencies: Get all transitive deps
    - validate_dependency_statuses: Check deps have valid status
    - generate_visualization: ASCII tree output
    - analyze_dependencies: Main entry point
"""
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional


# Pattern for valid story IDs: STORY-NNN or STORY-NNNN (3-4 digits)
STORY_ID_PATTERN = re.compile(r'^STORY-\d{3,4}$')

# Valid statuses for dependencies
VALID_STATUSES = [
    "Dev Complete",
    "QA Approved",
    "QA Approved ✅",
    "Released"
]

# Blocking statuses
BLOCKING_STATUSES = [
    "Backlog",
    "Ready for Dev",
    "In Development",
    "QA In Progress",
    "QA Failed"
]


def validate_story_id(story_id: str) -> bool:
    """
    Validate that a story ID matches the pattern ^STORY-\\d{3,4}$.

    Case-sensitive: 'story-123' is invalid, only 'STORY-123' is valid.

    Args:
        story_id: The story ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not story_id or not isinstance(story_id, str):
        return False
    # Case-sensitive - only uppercase STORY-NNN is valid
    return bool(STORY_ID_PATTERN.match(story_id.strip()))


def parse_yaml_frontmatter(content: str) -> Optional[dict]:
    """
    Extract and parse YAML frontmatter from story content.

    Args:
        content: The full story file content

    Returns:
        Dict with parsed YAML, or None if parsing fails
    """
    if not content or not isinstance(content, str):
        return None

    content = content.strip()
    if not content.startswith('---'):
        return None

    # Find the second --- delimiter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    yaml_content = parts[1].strip()
    if not yaml_content:
        return {}

    try:
        result = yaml.safe_load(yaml_content)
        if result is None:
            return {}
        if not isinstance(result, dict):
            return None
        return result
    except yaml.YAMLError:
        return None


def normalize_depends_on(ids: list) -> tuple[list, list]:
    """
    Normalize and validate dependency IDs.

    Strips whitespace and normalizes case:
    - IDs with any uppercase in prefix (STORY, Story) → normalize to uppercase
    - All-lowercase IDs (story-NNN) → invalid

    Args:
        ids: List of raw dependency IDs

    Returns:
        Tuple of (valid_ids, invalid_ids)
    """
    if not ids or not isinstance(ids, list):
        return ([], [])

    valid = []
    invalid = []

    for raw_id in ids:
        if not isinstance(raw_id, str):
            invalid.append(str(raw_id))
            continue

        # Normalize: strip whitespace
        stripped = raw_id.strip()

        # Try uppercase version for validation
        uppercased = stripped.upper()

        if validate_story_id(uppercased):
            # Check if ID has any uppercase letters in the prefix
            # "STORY-NNN" or "Story-NNN" → valid (has uppercase)
            # "story-NNN" → invalid (all lowercase prefix)
            prefix = stripped.split('-')[0] if '-' in stripped else stripped
            has_uppercase = any(c.isupper() for c in prefix)

            if has_uppercase:
                if uppercased not in valid:  # Avoid duplicates
                    valid.append(uppercased)
            else:
                # All lowercase prefix - treat as invalid
                invalid.append(raw_id)
        else:
            invalid.append(raw_id)

    return (valid, invalid)


def resolve_transitive_dependencies(story_id: str, graph: dict) -> list:
    """
    Resolve all transitive dependencies for a story.

    Args:
        story_id: The story to resolve dependencies for
        graph: Adjacency list {story_id: [dependency_ids]}

    Returns:
        List of all dependencies in topological order (deepest first)
    """
    if not graph or story_id not in graph:
        return []

    resolved = []
    seen = set()

    def dfs(node: str):
        if node in seen:
            return
        seen.add(node)

        for dep in graph.get(node, []):
            if dep not in seen:
                dfs(dep)
                if dep not in resolved:
                    resolved.append(dep)

    # Start DFS from each direct dependency
    for dep in graph.get(story_id, []):
        dfs(dep)
        if dep not in resolved:
            resolved.append(dep)

    return resolved


def detect_cycle(graph: dict, start: str) -> Optional[list]:
    """
    Detect circular dependencies using DFS.

    Args:
        graph: Adjacency list {story_id: [dependency_ids]}
        start: Story ID to start detection from

    Returns:
        Cycle path if found (list ending with repeated node), None otherwise
    """
    if not graph:
        return None

    # Check for self-dependency first
    if start in graph.get(start, []):
        return [start, start]

    visited = set()
    rec_stack = set()
    path = []

    def dfs(node: str) -> Optional[list]:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                cycle = dfs(neighbor)
                if cycle:
                    return cycle
            elif neighbor in rec_stack:
                # Found cycle - return path from cycle start to current + back to start
                cycle_start_idx = path.index(neighbor)
                return path[cycle_start_idx:] + [neighbor]

        path.pop()
        rec_stack.remove(node)
        return None

    return dfs(start)


def validate_dependency_statuses(deps: list, status_map: dict) -> list[dict]:
    """
    Validate that all dependencies have acceptable statuses.

    Args:
        deps: List of dependency story IDs
        status_map: Dict mapping story_id to status string

    Returns:
        List of failure dicts with keys: dependency, status, required, message
    """
    failures = []

    for dep_id in deps:
        status = status_map.get(dep_id, "Unknown")

        # Normalize status for comparison (remove emoji, trim)
        normalized_status = status.replace("✅", "").strip()
        valid_normalized = [s.replace("✅", "").strip() for s in VALID_STATUSES]

        if normalized_status not in valid_normalized:
            failure = {
                "dependency": dep_id,
                "status": status,
                "required": "Dev Complete or QA Approved",
                "message": f"Dependency {dep_id} status is '{status}'. Required: 'Dev Complete' or 'QA Approved'."
            }

            # Special message for QA Failed
            if "QA Failed" in status or "Failed" in status:
                failure["message"] = f"Dependency {dep_id} has failed QA."
                failure["suggestion"] = f"Run '/qa {dep_id} deep' to view failures."

            failures.append(failure)

    return failures


def generate_visualization(story_id: str, graph: dict, status_map: dict, depth: int = 0, visited: set = None) -> str:
    """
    Generate ASCII tree visualization of dependency chain.

    Args:
        story_id: Root story ID
        graph: Adjacency list {story_id: [dependency_ids]}
        status_map: Dict mapping story_id to status string
        depth: Current depth (for indentation)
        visited: Set of already visited nodes (prevents infinite recursion on cycles)

    Returns:
        ASCII tree string
    """
    if visited is None:
        visited = set()

    indent = "  " * depth
    connector = "└── " if depth > 0 else ""

    status = status_map.get(story_id, "")

    # Determine status icon
    if "Approved" in status or "Complete" in status or "Released" in status:
        status_icon = "✅"
    else:
        status_icon = "⏳"

    # Check for cycle
    if story_id in visited:
        if status:
            line = f"{indent}{connector}{story_id} 🔄 ({status}) [CIRCULAR]"
        else:
            line = f"{indent}{connector}{story_id} 🔄 [CIRCULAR]"
        return line

    visited.add(story_id)

    # Build current line
    if status:
        line = f"{indent}{connector}{story_id} {status_icon} ({status})"
    else:
        line = f"{indent}{connector}{story_id}"

    lines = [line]

    # Recurse for dependencies
    for dep in graph.get(story_id, []):
        dep_viz = generate_visualization(dep, graph, status_map, depth + 1, visited.copy())
        lines.append(dep_viz)

    return "\n".join(lines)


def build_dependency_graph(story_id: str, path: Path) -> tuple[dict, dict, list]:
    """
    Build dependency graph from story files.

    Args:
        story_id: Starting story ID
        path: Path to directory containing story files

    Returns:
        Tuple of (graph, status_map, missing_deps)
    """
    graph = {}
    status_map = {}
    missing_deps = []

    to_process = [story_id]
    processed = set()

    while to_process:
        current_id = to_process.pop(0)
        if current_id in processed:
            continue
        processed.add(current_id)

        # Find story file
        pattern = f"{current_id}*.story.md"
        story_files = list(path.glob(pattern))

        if not story_files:
            if current_id != story_id:  # Don't mark root as missing
                missing_deps.append(current_id)
            graph[current_id] = []
            continue

        # Read and parse
        content = story_files[0].read_text()
        frontmatter = parse_yaml_frontmatter(content)

        if frontmatter is None:
            graph[current_id] = []
            continue

        # Extract status
        status = frontmatter.get("status", "Unknown")
        status_map[current_id] = status

        # Extract dependencies
        raw_deps = frontmatter.get("depends_on", [])
        if raw_deps is None:
            raw_deps = []

        valid_deps, _ = normalize_depends_on(raw_deps)
        graph[current_id] = valid_deps

        # Queue dependencies for processing
        for dep in valid_deps:
            if dep not in processed:
                to_process.append(dep)

    return (graph, status_map, missing_deps)


def analyze_dependencies(
    story_id: str,
    fixtures_path: Optional[Path] = None,
    force: bool = False,
    log_dir: Optional[Path] = None,
    allow_missing: bool = False
) -> dict:
    """
    Main entry point for dependency analysis.

    Args:
        story_id: Story ID to analyze
        fixtures_path: Path to story files directory
        force: If True, bypass blocking (but log it)
        log_dir: Directory for bypass logs
        allow_missing: If True, don't fail on missing dependencies

    Returns:
        JSON-serializable dict with analysis results
    """
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Default path
    if fixtures_path is None:
        fixtures_path = Path("devforgeai/specs/Stories")

    # Build graph
    graph, status_map, missing_deps = build_dependency_graph(story_id, fixtures_path)

    # Get dependencies
    direct_deps = graph.get(story_id, [])
    transitive_deps = resolve_transitive_dependencies(story_id, graph)
    transitive_only = [d for d in transitive_deps if d not in direct_deps]

    # Detect cycles
    cycle_path = detect_cycle(graph, story_id)

    # Validate statuses
    status_failures = validate_dependency_statuses(transitive_deps, status_map)

    # Determine overall status
    blocking = False
    blocking_reason = None

    if cycle_path:
        status = "BLOCKED"
        blocking = True
        blocking_reason = "circular_dependency"
    elif missing_deps and not allow_missing:
        status = "BLOCKED"
        blocking = True
        blocking_reason = "missing_dependencies"
    elif status_failures:
        status = "BLOCKED"
        blocking = True
        blocking_reason = "invalid_dependency_status"
    else:
        status = "PASS"

    # Handle force bypass
    force_bypassed = False
    if force and blocking:
        blocking = False
        force_bypassed = True

        # Create log file
        if log_dir:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_filename = f"dependency-bypass-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.log"
            log_path = log_dir / log_filename
            log_content = f"""# Dependency Bypass Log
timestamp: {timestamp}
story: {story_id}
bypassed_failures:
{yaml.dump(status_failures, default_flow_style=False) if status_failures else '  none'}
"""
            log_path.write_text(log_content)

    # Generate visualization
    visualization = generate_visualization(story_id, graph, status_map)

    # Build response
    result = {
        "status": status,
        "story_id": story_id,
        "blocking": blocking,
        "blocking_reason": blocking_reason,
        "force_bypassed": force_bypassed,
        "dependencies": {
            "direct": direct_deps,
            "transitive": transitive_only,
            "total_count": len(transitive_deps)
        },
        "validation": {
            "all_exist": len(missing_deps) == 0,
            "missing": missing_deps,
            "all_valid_status": len(status_failures) == 0,
            "cycle_detected": cycle_path is not None,
            "cycle_path": cycle_path,
            "failures": status_failures
        },
        "chain_visualization": visualization,
        "timestamp": timestamp
    }

    return result
