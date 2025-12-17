"""
File Overlap Detector for STORY-094.

Detects file overlaps between parallel stories using spec-based
pre-flight and git-based post-flight analysis.

Functions:
    - extract_file_paths_from_spec: Parse technical_specification YAML
    - scan_active_stories: Find stories with status "In Development"
    - detect_overlaps: Cross-reference file paths
    - filter_dependency_overlaps: Exclude depends_on stories
    - run_git_diff: Execute git diff for post-flight
    - detect_spec_discrepancies: Compare git vs spec
    - generate_overlap_report: Create markdown report
    - generate_recommendations: Create actionable recommendations
    - analyze_overlaps: Main entry point
"""
import re
import yaml
import subprocess
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any

# Configure logging
logger = logging.getLogger(__name__)

# Pattern for valid story IDs
STORY_ID_PATTERN = re.compile(r'^STORY-\d{3,4}$')

# Constants
ACTIVE_STATUSES = ["In Development"]
DEFAULT_WARNING_THRESHOLD = 1
DEFAULT_BLOCKING_THRESHOLD = 10


def extract_file_paths_from_spec(content: str) -> Tuple[List[str], bool]:
    """
    Parse technical_specification YAML from story content and extract file_path values.

    Args:
        content: Full story file content

    Returns:
        Tuple of (file_paths list, spec_found boolean)
    """
    if not content or not isinstance(content, str):
        return [], False

    # Find technical_specification YAML block
    # Pattern: ```yaml ... technical_specification: ... ```
    yaml_block_pattern = r'```yaml\s*(technical_specification:[\s\S]*?)```'
    match = re.search(yaml_block_pattern, content)

    if not match:
        return [], False

    yaml_content = match.group(1)

    try:
        parsed = yaml.safe_load(yaml_content)
        if not parsed or 'technical_specification' not in parsed:
            # Try parsing without the key prefix
            if isinstance(parsed, dict) and 'format_version' in parsed:
                spec = parsed
            else:
                return [], False
        else:
            spec = parsed.get('technical_specification', {})

        # Check for nested technical_specification
        if 'technical_specification' in spec:
            spec = spec['technical_specification']

        components = spec.get('components', [])
        if not components:
            return [], True  # Spec found but empty components

        file_paths = []
        for component in components:
            if isinstance(component, dict) and 'file_path' in component:
                file_paths.append(component['file_path'])

        return file_paths, True

    except yaml.YAMLError as e:
        logger.warning(f"Failed to parse technical_specification YAML: {e}")
        return [], False


def _parse_yaml_frontmatter(content: str) -> Optional[Dict]:
    """
    Extract and parse YAML frontmatter from story content.

    Args:
        content: Full story file content

    Returns:
        Dict with parsed YAML, or None if parsing fails
    """
    if not content or not isinstance(content, str):
        return None

    content = content.strip()
    if not content.startswith('---'):
        return None

    # Find end of frontmatter
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return None

    frontmatter = content[3:end_match.start() + 3]

    try:
        return yaml.safe_load(frontmatter)
    except yaml.YAMLError:
        return None


def scan_active_stories(
    stories_dir: Path,
    exclude_ids: Optional[List[str]] = None
) -> Dict[str, List[str]]:
    """
    Scan all stories with status "In Development" and extract their file_paths.

    Args:
        stories_dir: Path to stories directory
        exclude_ids: Story IDs to exclude (e.g., target story)

    Returns:
        Dict mapping story_id to list of file_paths
    """
    exclude_ids = exclude_ids or []
    result = {}

    stories_path = Path(stories_dir)
    if not stories_path.exists():
        return result

    for story_file in stories_path.glob("*.story.md"):
        try:
            content = story_file.read_text(encoding='utf-8')

            # Parse frontmatter to get status and ID
            frontmatter = _parse_yaml_frontmatter(content)
            if not frontmatter:
                continue

            story_id = frontmatter.get('id', '')
            status = frontmatter.get('status', '')

            # Skip if not active or in exclude list
            if status not in ACTIVE_STATUSES:
                continue
            if story_id in exclude_ids:
                continue

            # Extract file paths from technical_specification
            file_paths, spec_found = extract_file_paths_from_spec(content)
            if file_paths:
                result[story_id] = file_paths

        except Exception as e:
            logger.warning(f"Error processing {story_file}: {e}")
            continue

    return result


def detect_overlaps(
    target_paths: List[str],
    active_stories: Dict[str, List[str]],
    target_story_id: str
) -> Dict[str, List[str]]:
    """
    Detect overlapping files between target and active stories.

    Args:
        target_paths: File paths from target story
        active_stories: Dict of story_id -> file_paths
        target_story_id: ID of story being developed

    Returns:
        Dict mapping overlapping_story_id to list of shared file_paths
    """
    overlaps = {}
    target_set = set(target_paths)

    for story_id, story_paths in active_stories.items():
        # Skip target story
        if story_id == target_story_id:
            continue

        # Find intersection
        story_path_set = set(story_paths)
        shared_paths = target_set & story_path_set

        if shared_paths:
            overlaps[story_id] = list(shared_paths)

    return overlaps


def filter_dependency_overlaps(
    overlaps: Dict[str, List[str]],
    depends_on: List[str]
) -> Dict[str, List[str]]:
    """
    Remove overlaps from stories in the depends_on chain.

    Args:
        overlaps: Dict of overlapping stories and files
        depends_on: List of story IDs this story depends on

    Returns:
        Filtered overlaps (non-dependent stories only)
    """
    if not depends_on:
        return overlaps

    depends_on_set = set(depends_on)
    return {
        story_id: paths
        for story_id, paths in overlaps.items()
        if story_id not in depends_on_set
    }


def run_git_diff(
    worktree_path: Optional[Path] = None,
    include_untracked: bool = False
) -> List[str]:
    """
    Execute git diff to find actually modified files.

    Args:
        worktree_path: Path to worktree (if parallel development)
        include_untracked: Include untracked files in result

    Returns:
        List of modified file paths
    """
    cwd = worktree_path if worktree_path else Path.cwd()

    try:
        # Get modified files (staged and unstaged)
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )

        modified_files = []
        if result.returncode == 0:
            modified_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]

        # Also get staged but not committed
        staged_result = subprocess.run(
            ["git", "diff", "--name-only", "--cached"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if staged_result.returncode == 0:
            staged_files = [f.strip() for f in staged_result.stdout.strip().split('\n') if f.strip()]
            modified_files.extend(staged_files)

        # Include untracked if requested
        if include_untracked:
            untracked_result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            if untracked_result.returncode == 0:
                untracked_files = [f.strip() for f in untracked_result.stdout.strip().split('\n') if f.strip()]
                modified_files.extend(untracked_files)

        # Remove duplicates while preserving order
        seen = set()
        unique_files = []
        for f in modified_files:
            if f not in seen:
                seen.add(f)
                unique_files.append(f)

        return unique_files

    except subprocess.TimeoutExpired:
        logger.warning("Git diff timed out")
        return []
    except FileNotFoundError:
        logger.warning("Git not available")
        return []
    except Exception as e:
        logger.warning(f"Git diff error: {e}")
        return []


def detect_spec_discrepancies(
    declared_paths: List[str],
    actual_paths: List[str]
) -> Dict[str, List[str]]:
    """
    Compare declared spec paths vs actual git changes.

    Args:
        declared_paths: file_path values from technical_specification
        actual_paths: Files modified according to git diff

    Returns:
        Dict with 'undeclared' and 'unused' lists
    """
    declared_set = set(declared_paths)
    actual_set = set(actual_paths)

    undeclared = list(actual_set - declared_set)
    unused = list(declared_set - actual_set)

    return {
        "undeclared": undeclared,
        "unused": unused
    }


def generate_recommendations(
    overlap_count: int,
    overlap_details: Dict[str, List[str]],
    blocking_threshold: int,
    is_circular: bool = False
) -> List[str]:
    """
    Generate actionable recommendations based on overlap severity.

    Args:
        overlap_count: Total overlapping file count
        overlap_details: Story-to-files mapping
        blocking_threshold: Threshold for blocking recommendation
        is_circular: Whether circular dependency detected

    Returns:
        List of recommendation strings
    """
    recommendations = []

    if is_circular:
        recommendations.append(
            "Circular dependency detected - recommend sequential development"
        )

    if overlap_count >= blocking_threshold:
        recommendations.append(
            f"High overlap ({overlap_count} files) - strongly recommend sequential development"
        )
    elif overlap_count >= 10:
        recommendations.append(
            "Consider sequential development due to significant file overlap"
        )

    # Add story-specific recommendations
    for story_id, files in overlap_details.items():
        if len(files) > 3:
            recommendations.append(
                f"Coordinate with {story_id} developer - {len(files)} shared files"
            )
        elif len(files) > 0:
            files_str = ", ".join(files[:2])
            if len(files) > 2:
                files_str += f" (+{len(files) - 2} more)"
            recommendations.append(
                f"Coordinate with {story_id} on {files_str}"
            )

    if not recommendations and overlap_count > 0:
        recommendations.append(
            "Review overlapping files before proceeding with parallel development"
        )

    return recommendations


def generate_overlap_report(
    story_id: str,
    analysis_type: str,
    overlaps: Dict[str, List[str]],
    discrepancies: Optional[Dict[str, List[str]]],
    recommendations: List[str],
    output_dir: Path
) -> Path:
    """
    Generate markdown overlap report.

    Args:
        story_id: Target story ID
        analysis_type: Type of analysis performed ("pre-flight" or "post-flight")
        overlaps: Overlap detection results
        discrepancies: Spec discrepancy results (post-flight only)
        recommendations: List of recommendations
        output_dir: Directory for report output

    Returns:
        Path to generated report file
    """
    timestamp = datetime.now(timezone.utc)
    timestamp_str = timestamp.strftime("%Y%m%d-%H%M%S")
    filename = f"overlap-{story_id}-{timestamp_str}.md"
    report_path = Path(output_dir) / filename

    # Calculate total overlap count
    overlap_count = sum(len(files) for files in overlaps.values())

    # Generate report content
    lines = [
        f"# File Overlap Report: {story_id}",
        "",
        f"**Generated:** {timestamp.isoformat()}Z",
        f"**Analysis Type:** {analysis_type}",
        f"**Total Overlapping Files:** {overlap_count}",
        "",
        "---",
        "",
    ]

    # Overlaps section
    lines.append("## Overlapping Files")
    lines.append("")

    if overlaps:
        for other_story, files in overlaps.items():
            lines.append(f"### {other_story}")
            lines.append("")
            for f in files:
                lines.append(f"- `{f}`")
            lines.append("")
    else:
        lines.append("No overlapping files detected.")
        lines.append("")

    # Discrepancies section (post-flight only)
    if discrepancies:
        lines.append("## Spec Discrepancies")
        lines.append("")

        if discrepancies.get("undeclared"):
            lines.append("### Undeclared Modifications")
            lines.append("*Files modified but not declared in technical_specification:*")
            lines.append("")
            for f in discrepancies["undeclared"]:
                lines.append(f"- `{f}`")
            lines.append("")

        if discrepancies.get("unused"):
            lines.append("### Unused Declarations")
            lines.append("*Files declared in technical_specification but not modified:*")
            lines.append("")
            for f in discrepancies["unused"]:
                lines.append(f"- `{f}`")
            lines.append("")

    # Recommendations section
    lines.append("## Recommendations")
    lines.append("")

    if recommendations:
        for rec in recommendations:
            lines.append(f"- {rec}")
    else:
        lines.append("No specific recommendations.")
    lines.append("")

    # Write report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding='utf-8')

    return report_path


def analyze_overlaps(
    story_id: str,
    mode: str = "pre-flight",
    story_content: Optional[str] = None,
    target_paths: Optional[List[str]] = None,
    declared_paths: Optional[List[str]] = None,
    actual_paths: Optional[List[str]] = None,
    active_stories: Optional[Dict[str, List[str]]] = None,
    fixtures_path: Optional[Path] = None,
    worktree_path: Optional[Path] = None,
    config: Optional[Dict[str, Any]] = None,
    output_dir: Optional[Path] = None,
    depends_on: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Main entry point for overlap analysis.

    Args:
        story_id: Story ID to analyze
        mode: Analysis mode ("pre-flight" or "post-flight")
        story_content: Story file content (if not loading from path)
        target_paths: Pre-extracted file paths from target story
        declared_paths: Declared file paths (for post-flight)
        actual_paths: Actual modified files (for post-flight)
        active_stories: Pre-loaded map of active story file paths
        fixtures_path: Path to stories directory
        worktree_path: Path to worktree (post-flight)
        config: Configuration dict (warning_threshold, blocking_threshold)
        output_dir: Directory for report generation
        depends_on: List of dependency story IDs

    Returns:
        JSON-serializable dict with analysis results
    """
    # Validate story_id
    if not story_id:
        return {
            "status": "ERROR",
            "story_id": story_id,
            "mode": mode,
            "error": "Invalid story_id",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }

    # Load config
    config = config or {}
    warning_threshold = config.get("warning_threshold", DEFAULT_WARNING_THRESHOLD)
    blocking_threshold = config.get("blocking_threshold", DEFAULT_BLOCKING_THRESHOLD)

    # Initialize result
    result = {
        "story_id": story_id,
        "mode": mode,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "warning_threshold": warning_threshold,
        "blocking_threshold": blocking_threshold
    }

    if mode == "pre-flight":
        # Pre-flight: Spec-based overlap detection
        spec_found = True
        paths = target_paths

        if paths is None and story_content:
            paths, spec_found = extract_file_paths_from_spec(story_content)
        elif paths is None:
            paths = []
            spec_found = False

        result["spec_found"] = spec_found
        result["declared_paths"] = paths
        result["declared_path_count"] = len(paths)

        if not spec_found:
            logger.warning(f"No technical_specification found for {story_id}")
            result["status"] = "PASS"
            result["overlaps"] = {}
            result["overlap_count"] = 0
            result["recommendations"] = []
            return result

        # Load active stories if not provided
        if active_stories is None and fixtures_path:
            active_stories = scan_active_stories(fixtures_path, exclude_ids=[story_id])
        elif active_stories is None:
            active_stories = {}

        # Detect overlaps
        overlaps = detect_overlaps(paths, active_stories, story_id)

        # Filter by dependencies
        depends_on = depends_on or []
        filtered_overlaps = filter_dependency_overlaps(overlaps, depends_on)

        # Calculate overlap count
        overlap_count = sum(len(files) for files in filtered_overlaps.values())

        result["overlaps"] = filtered_overlaps
        result["overlap_count"] = overlap_count

        # Generate recommendations
        recommendations = generate_recommendations(
            overlap_count=overlap_count,
            overlap_details=filtered_overlaps,
            blocking_threshold=blocking_threshold
        )
        result["recommendations"] = recommendations

        # Determine status
        if overlap_count == 0:
            result["status"] = "PASS"
        elif overlap_count >= blocking_threshold:
            result["status"] = "BLOCKED"
        elif overlap_count >= warning_threshold:
            result["status"] = "WARNING"
        else:
            result["status"] = "PASS"

        # Generate report if overlaps detected and output_dir provided
        if overlap_count > 0 and output_dir:
            report_path = generate_overlap_report(
                story_id=story_id,
                analysis_type="pre-flight",
                overlaps=filtered_overlaps,
                discrepancies=None,
                recommendations=recommendations,
                output_dir=output_dir
            )
            result["report_path"] = str(report_path)

    elif mode == "post-flight":
        # Post-flight: Git-based validation
        result["mode"] = "post-flight"

        # Get actual changed files if not provided
        if actual_paths is None:
            actual_paths = run_git_diff(worktree_path=worktree_path)

        # Use declared_paths if provided, otherwise empty
        declared_paths = declared_paths or []

        result["declared_paths"] = declared_paths
        result["actual_paths"] = actual_paths

        # Detect discrepancies
        discrepancies = detect_spec_discrepancies(declared_paths, actual_paths)
        result["discrepancies"] = discrepancies
        result["discrepancy_count"] = len(discrepancies["undeclared"]) + len(discrepancies["unused"])

        # Generate recommendations for discrepancies
        recommendations = []
        if discrepancies["undeclared"]:
            recommendations.append(
                f"Update technical_specification to include {len(discrepancies['undeclared'])} undeclared files"
            )
        if discrepancies["unused"]:
            recommendations.append(
                f"Review {len(discrepancies['unused'])} unused file declarations in technical_specification"
            )
        result["recommendations"] = recommendations

        # Determine status
        if discrepancies["undeclared"] or discrepancies["unused"]:
            result["status"] = "WARNING"
        else:
            result["status"] = "PASS"

        # Generate report if discrepancies found and output_dir provided
        if result["discrepancy_count"] > 0 and output_dir:
            report_path = generate_overlap_report(
                story_id=story_id,
                analysis_type="post-flight",
                overlaps={},
                discrepancies=discrepancies,
                recommendations=recommendations,
                output_dir=output_dir
            )
            result["report_path"] = str(report_path)

    else:
        result["status"] = "ERROR"
        result["error"] = f"Unknown mode: {mode}"

    return result
