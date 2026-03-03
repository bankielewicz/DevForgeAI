"""
STORY-175: Regression vs Pre-existing Classification for QA Validation.

This module classifies violations as REGRESSION or PRE_EXISTING based on
whether they occur in files changed by the current story.

- REGRESSION: Violations in changed files (blocking=true, blocks QA)
- PRE_EXISTING: Violations in unchanged files (blocking=false, warnings only)
"""

import logging
import subprocess
from typing import List, Dict, Any, Optional

# Configure module logger
logger = logging.getLogger(__name__)


# =============================================================================
# AC#1: Identify Files Changed by Current Story
# =============================================================================

def get_changed_files(project_root: Optional[str] = None) -> List[str]:
    """
    Get list of files changed in the current commit using git diff.

    Uses `git diff --name-only HEAD~1` to identify changed files.
    Falls back to `git diff --name-only origin/main...HEAD` for first commits.

    Args:
        project_root: Optional path to project root directory.
                      If None, uses current working directory.

    Returns:
        List of changed file paths (relative to project root).

    Raises:
        subprocess.CalledProcessError: If git command fails and no fallback works.
    """
    try:
        # Primary: Compare with previous commit
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1"],
            capture_output=True,
            text=True,
            cwd=project_root,
            check=True
        )
        return _parse_git_output(result.stdout)
    except subprocess.CalledProcessError:
        # Fallback: First commit scenario - compare with origin/main
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "origin/main...HEAD"],
                capture_output=True,
                text=True,
                cwd=project_root,
                check=True
            )
            return _parse_git_output(result.stdout)
        except subprocess.CalledProcessError:
            # If both fail, re-raise
            raise


def get_changed_files_safe() -> List[str]:
    """
    Error-tolerant version of get_changed_files.

    Returns empty list on any error (permission, timeout, no git, etc.).

    Returns:
        List of changed file paths, or empty list on error.
    """
    try:
        return get_changed_files()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            PermissionError, FileNotFoundError, OSError):
        return []


def is_git_repository() -> bool:
    """
    Check if current directory is inside a git repository.

    Returns:
        True if in a git repository, False otherwise.
    """
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def is_first_commit() -> bool:
    """
    Check if the current HEAD is the first commit (no parent).

    Returns:
        True if this is the first commit, False otherwise.
    """
    try:
        subprocess.run(
            ["git", "rev-parse", "HEAD~1"],
            capture_output=True,
            text=True,
            check=True
        )
        return False
    except subprocess.CalledProcessError:
        return True


def _parse_git_output(output: str) -> List[str]:
    """
    Parse git diff output into list of file paths.

    Strips whitespace and filters empty lines.

    Args:
        output: Raw stdout from git diff command.

    Returns:
        List of non-empty, stripped file paths.
    """
    lines = output.strip().split('\n')
    return [line.strip() for line in lines if line.strip()]


# =============================================================================
# AC#2: Classify Violations as REGRESSION or PRE_EXISTING
# =============================================================================

def classify_violation(violation: Dict[str, Any], changed_files: List[str]) -> str:
    """
    Classify a single violation as REGRESSION or PRE_EXISTING.

    A violation is REGRESSION if its file is in the changed files list.
    Path separators are normalized for cross-platform compatibility.

    Args:
        violation: Dict with 'file' key containing the file path.
        changed_files: List of files changed in current commit.

    Returns:
        "REGRESSION" if file is in changed_files, "PRE_EXISTING" otherwise.
    """
    violation_file = _normalize_path(violation.get("file", ""))
    normalized_changed = [_normalize_path(f) for f in changed_files]

    if violation_file in normalized_changed:
        return "REGRESSION"
    return "PRE_EXISTING"


def classify_violations(violations: List[Dict[str, Any]],
                        changed_files: List[str]) -> List[Dict[str, Any]]:
    """
    Classify a list of violations as REGRESSION or PRE_EXISTING.

    Adds 'classification' field to each violation dict.

    Args:
        violations: List of violation dicts, each with 'file' key.
        changed_files: List of files changed in current commit.

    Returns:
        List of violation dicts with 'classification' field added.
    """
    result = []
    for violation in violations:
        classified = violation.copy()
        classified["classification"] = classify_violation(violation, changed_files)
        result.append(classified)
    return result


def classify_violations_with_fallback(violations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Classify violations with full edge case handling.

    Handles:
    - No git repository: All violations are REGRESSION (blocking)
    - First commit: Uses origin/main comparison
    - Empty changed files: All violations are PRE_EXISTING

    Args:
        violations: List of violation dicts.

    Returns:
        List of classified violations with blocking status set.
    """
    if not is_git_repository():
        # No git repo: fallback to all REGRESSION
        logger.warning("Not in a git repository. Classifying all violations as REGRESSION.")
        result = []
        for violation in violations:
            classified = violation.copy()
            classified["classification"] = "REGRESSION"
            classified["blocking"] = True
            result.append(classified)
        return result

    # Normal path: get changed files and classify
    try:
        changed_files = get_changed_files()
    except subprocess.CalledProcessError:
        # If git diff fails completely, treat as no changes
        changed_files = []

    classified = classify_violations(violations, changed_files)
    return set_all_blocking_status(classified)


def _normalize_path(path: str) -> str:
    """
    Normalize path separators for cross-platform comparison.

    Converts backslashes to forward slashes.

    Args:
        path: File path to normalize.

    Returns:
        Normalized path with forward slashes.
    """
    return path.replace("\\", "/")


# =============================================================================
# AC#3: REGRESSION Violations Block QA
# =============================================================================

def set_blocking_status(violation: Dict[str, Any]) -> Dict[str, Any]:
    """
    Set blocking status based on classification.

    REGRESSION violations block QA (blocking=True).
    PRE_EXISTING violations are warnings only (blocking=False).

    Args:
        violation: Dict with 'classification' field.

    Returns:
        Violation dict with 'blocking' field added.
    """
    result = violation.copy()
    result["blocking"] = violation.get("classification") == "REGRESSION"
    return result


def set_all_blocking_status(violations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Set blocking status for all violations.

    Args:
        violations: List of classified violation dicts.

    Returns:
        List of violations with 'blocking' field added.
    """
    return [set_blocking_status(v) for v in violations]


def should_block_qa(violations: List[Dict[str, Any]]) -> bool:
    """
    Determine if QA should be blocked based on violations.

    QA is blocked if any violation has blocking=True.

    Args:
        violations: List of violations with 'blocking' field.

    Returns:
        True if any violation is blocking, False otherwise.
    """
    return any(v.get("blocking", False) for v in violations)


def _count_violations_by_field(violations: List[Dict[str, Any]],
                               field: str,
                               value: Any,
                               default: Any = None) -> int:
    """
    Count violations where a specific field matches a value.

    Generic helper to reduce duplication in counting functions.

    Args:
        violations: List of violation dicts.
        field: Field name to check.
        value: Value to match.
        default: Default if field is missing.

    Returns:
        Number of violations where field equals value.
    """
    return sum(1 for v in violations if v.get(field, default) == value)


def count_blocking(violations: List[Dict[str, Any]]) -> int:
    """
    Count violations with blocking=True.

    Args:
        violations: List of violations with 'blocking' field.

    Returns:
        Number of blocking violations.
    """
    return _count_violations_by_field(violations, "blocking", True, default=False)


def count_non_blocking(violations: List[Dict[str, Any]]) -> int:
    """
    Count violations with blocking=False.

    Args:
        violations: List of violations with 'blocking' field.

    Returns:
        Number of non-blocking violations.
    """
    return _count_violations_by_field(violations, "blocking", False, default=True)


# =============================================================================
# AC#4: Display Classification Breakdown
# =============================================================================

def format_breakdown(regression_count: int, pre_existing_count: int) -> str:
    """
    Format classification counts into display string.

    Args:
        regression_count: Number of REGRESSION violations.
        pre_existing_count: Number of PRE_EXISTING violations.

    Returns:
        String in format "Regressions: {count} | Pre-existing: {count}".
    """
    return f"Regressions: {regression_count} | Pre-existing: {pre_existing_count}"


def get_breakdown(violations: List[Dict[str, Any]]) -> str:
    """
    Calculate and format breakdown from violations list.

    Args:
        violations: List of classified violations.

    Returns:
        Formatted breakdown string.
    """
    regression_count = count_regressions(violations)
    pre_existing_count = count_pre_existing(violations)
    return format_breakdown(regression_count, pre_existing_count)


def count_regressions(violations: List[Dict[str, Any]]) -> int:
    """
    Count violations classified as REGRESSION.

    Args:
        violations: List of classified violations.

    Returns:
        Number of REGRESSION violations.
    """
    return _count_violations_by_field(violations, "classification", "REGRESSION")


def count_pre_existing(violations: List[Dict[str, Any]]) -> int:
    """
    Count violations classified as PRE_EXISTING.

    Args:
        violations: List of classified violations.

    Returns:
        Number of PRE_EXISTING violations.
    """
    return _count_violations_by_field(violations, "classification", "PRE_EXISTING")


def generate_classification_summary(violations: List[Dict[str, Any]]) -> str:
    """
    Generate classification summary for QA report.

    Args:
        violations: List of classified violations.

    Returns:
        Summary string with breakdown.
    """
    return get_breakdown(violations)


# =============================================================================
# Integration: Full Workflow
# =============================================================================

def run_classification_workflow(violations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Run complete classification workflow.

    1. Get changed files from git
    2. Classify each violation
    3. Set blocking status

    Args:
        violations: List of violation dicts.

    Returns:
        List of violations with classification and blocking status.
    """
    changed_files = get_changed_files()
    classified = classify_violations(violations, changed_files)
    return set_all_blocking_status(classified)


def generate_qa_report_section(violations: List[Dict[str, Any]]) -> str:
    """
    Generate QA report section with classification breakdown.

    Args:
        violations: List of classified violations.

    Returns:
        Report section string.
    """
    breakdown = get_breakdown(violations)
    blocking_count = count_blocking(violations)
    non_blocking_count = count_non_blocking(violations)

    lines = [
        "## Violation Classification",
        "",
        breakdown,
        "",
        f"Blocking: {blocking_count} | Warnings: {non_blocking_count}",
    ]

    return "\n".join(lines)


def _format_violation_line(violation: Dict[str, Any]) -> str:
    """
    Format a single violation as a report line.

    Args:
        violation: Violation dict with file, line, message fields.

    Returns:
        Formatted markdown line for report.
    """
    file_path = violation.get("file", "unknown")
    line_num = violation.get("line", "?")
    message = violation.get("message", "No message")
    return f"- `{file_path}:{line_num}` - {message}"


def _filter_violations_by_classification(violations: List[Dict[str, Any]],
                                         classification: str) -> List[Dict[str, Any]]:
    """
    Filter violations by classification value.

    Args:
        violations: List of classified violations.
        classification: Classification to filter by (REGRESSION or PRE_EXISTING).

    Returns:
        List of violations matching the classification.
    """
    return [v for v in violations if v.get("classification") == classification]


def generate_detailed_report(violations: List[Dict[str, Any]]) -> str:
    """
    Generate detailed report with all violation classifications.

    Args:
        violations: List of classified violations.

    Returns:
        Detailed report string.
    """
    lines = [
        "## Detailed Violation Report",
        "",
        get_breakdown(violations),
        "",
        "### Violations by Classification",
        "",
    ]

    # Group by classification
    regressions = _filter_violations_by_classification(violations, "REGRESSION")
    pre_existing = _filter_violations_by_classification(violations, "PRE_EXISTING")

    if regressions:
        lines.append("#### REGRESSION (Blocking)")
        lines.extend(_format_violation_line(v) for v in regressions)
        lines.append("")

    if pre_existing:
        lines.append("#### PRE_EXISTING (Warning Only)")
        lines.extend(_format_violation_line(v) for v in pre_existing)
        lines.append("")

    return "\n".join(lines)
