"""
Branching Analysis Module for STORY-228

Provides functionality for:
- AC#1: Branching Point Detection
- AC#2: Decision Tree Building
- AC#3: Branch Probability Validation

Part of EPIC-034: Session Data Mining for Framework Intelligence
"""

from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict


# ============================================================================
# AC#1: Branching Point Detection Functions
# ============================================================================

def group_by_session(session_entries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group session entries by session_id and sort by timestamp.

    Args:
        session_entries: List of session entry dictionaries

    Returns:
        Dictionary mapping session_id to list of entries, sorted by timestamp
    """
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for entry in session_entries:
        # Handle missing session_id - use 'unknown' as fallback
        session_id = entry.get("session_id", "unknown")
        grouped[session_id].append(entry)

    # Sort each session's entries by timestamp
    for session_id in grouped:
        grouped[session_id].sort(key=lambda e: e.get("timestamp", ""))

    return dict(grouped)


def extract_transitions(session_entries: List[Dict[str, Any]]) -> List[Tuple[str, str]]:
    """
    Extract command transitions (A -> B) from session entries.

    Args:
        session_entries: List of session entry dictionaries

    Returns:
        List of (source_command, target_command) tuples
    """
    transitions: List[Tuple[str, str]] = []

    # Group by session first
    grouped = group_by_session(session_entries)

    # Extract transitions from each session
    for session_id, entries in grouped.items():
        for i in range(len(entries) - 1):
            source_cmd = entries[i].get("command", "")
            target_cmd = entries[i + 1].get("command", "")
            if source_cmd and target_cmd:
                transitions.append((source_cmd, target_cmd))

    return transitions


def count_downstream(session_entries: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """
    Count downstream commands for each source command.

    Args:
        session_entries: List of session entry dictionaries

    Returns:
        Dictionary mapping source_command to {target_command: count}
    """
    downstream_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    transitions = extract_transitions(session_entries)

    for source_cmd, target_cmd in transitions:
        downstream_counts[source_cmd][target_cmd] += 1

    # Convert to regular dicts
    return {cmd: dict(targets) for cmd, targets in downstream_counts.items()}


def detect_branching_points(
    session_entries: List[Dict[str, Any]],
    min_paths: int = 2
) -> Dict[str, Dict[str, Any]]:
    """
    Identify commands that trigger multiple downstream choices.

    Args:
        session_entries: List of session entry dictionaries
        min_paths: Minimum number of different downstream paths to be a branching point

    Returns:
        Dictionary of branching points with downstream commands and frequencies
    """
    if not session_entries:
        return {}

    downstream_counts = count_downstream(session_entries)
    branching_points: Dict[str, Dict[str, Any]] = {}

    for command, downstream in downstream_counts.items():
        # Check if this command has enough different downstream paths
        if len(downstream) >= min_paths:
            branching_points[command] = {
                "downstream": {
                    target: {"frequency": count}
                    for target, count in downstream.items()
                }
            }

    return branching_points


# ============================================================================
# AC#2: Decision Tree Building Functions
# ============================================================================

def calculate_probabilities(branching_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert frequencies to probabilities for each branching point.

    Args:
        branching_input: Branching points with frequency data

    Returns:
        Decision tree with calculated probabilities
    """
    result: Dict[str, Any] = {}

    for command, data in branching_input.items():
        downstream = data.get("downstream", {})

        # Calculate total frequency
        total_freq = sum(
            d.get("frequency", 0)
            for d in downstream.values()
        )

        # Build branches with probabilities
        branches = []
        for target_cmd, target_data in downstream.items():
            freq = target_data.get("frequency", 0)

            # Calculate probability
            if total_freq > 0:
                raw_prob = freq / total_freq
                # Round to 2 decimals, but preserve very small probabilities
                # (don't round to 0 unless actually 0)
                if raw_prob > 0 and raw_prob < 0.005:
                    probability = 0.01  # Minimum non-zero probability
                else:
                    probability = round(raw_prob, 2)
            else:
                # Equal distribution for all-zero case
                probability = round(1.0 / len(downstream), 2) if downstream else 0.0

            branches.append({
                "command": target_cmd,
                "frequency": freq,
                "probability": probability
            })

        # Sort branches by probability (highest first)
        branches.sort(key=lambda b: b["probability"], reverse=True)

        # Ensure probabilities sum to 1.0 by adjusting the highest one (not the last)
        if branches:
            current_sum = sum(b["probability"] for b in branches)
            if abs(current_sum - 1.0) > 0.001 and total_freq > 0:
                # Adjust the first (highest) branch to make sum exactly 1.0
                # This prevents wiping out small probabilities
                adjustment = round(1.0 - current_sum, 2)
                branches[0]["probability"] = round(
                    branches[0]["probability"] + adjustment, 2
                )

        result[command] = {
            "branches": branches,
            "total_frequency": total_freq
        }

    return result


def build_decision_tree(
    branching_points: Dict[str, Any],
    track_depth: bool = False
) -> Dict[str, Any]:
    """
    Build a decision tree from branching points.

    Args:
        branching_points: Dictionary of branching points with downstream data
        track_depth: Whether to include depth information

    Returns:
        Decision tree with probabilities and branch information
    """
    if not branching_points:
        return {}

    # Calculate probabilities for all branching points
    tree = calculate_probabilities(branching_points)

    # Add depth tracking if requested
    if track_depth:
        for command in tree:
            tree[command]["depth"] = 0  # Simple depth for now

    return tree


def format_decision_tree(branching_points: Dict[str, Any]) -> str:
    """
    Format decision tree as human-readable string.

    Format: "command A -> command B (70%) or command C (30%)"

    Args:
        branching_points: Dictionary of branching points

    Returns:
        Formatted string representation
    """
    tree = build_decision_tree(branching_points)

    lines = []
    for command, node in tree.items():
        branches = node.get("branches", [])

        if not branches:
            continue

        # Format each branch as "target (XX%)"
        branch_strs = []
        for branch in branches:
            target = branch["command"]
            prob_pct = int(round(branch["probability"] * 100))
            branch_strs.append(f"{target} ({prob_pct}%)")

        # Join with " or " for multiple branches
        if len(branch_strs) > 1:
            branches_formatted = " or ".join(branch_strs)
        else:
            branches_formatted = branch_strs[0] if branch_strs else ""

        lines.append(f"{command} -> {branches_formatted}")

    return "\n".join(lines)


# ============================================================================
# AC#3: Branch Probability Validation Functions
# ============================================================================

def validate_probability_sum(decision_tree: Dict[str, Any]) -> bool:
    """
    Validate that all branch probabilities sum to 100% (1.0).

    Args:
        decision_tree: Decision tree with probability data

    Returns:
        True if all nodes sum to 100%, False otherwise
    """
    if not decision_tree:
        return True  # Empty tree is vacuously valid

    for command, node in decision_tree.items():
        branches = node.get("branches", [])

        if not branches:
            continue  # Empty branches is acceptable

        # Sum probabilities
        prob_sum = sum(b.get("probability", 0) for b in branches)

        # Check if sum is approximately 1.0 (allowing for rounding)
        if abs(prob_sum - 1.0) > 0.01:
            return False

    return True


def validate_all_probability_sums(
    decision_tree: Dict[str, Any]
) -> Dict[str, Dict[str, Any]]:
    """
    Validate probability sums for each decision point and return detailed report.

    Args:
        decision_tree: Decision tree with probability data

    Returns:
        Dictionary mapping each command to validation result with 'valid' and 'sum'
    """
    report: Dict[str, Dict[str, Any]] = {}

    for command, node in decision_tree.items():
        branches = node.get("branches", [])

        # Calculate sum
        prob_sum = sum(b.get("probability", 0) for b in branches)

        # Determine validity (within 1% of 1.0)
        is_valid = abs(prob_sum - 1.0) < 0.01 if branches else True

        report[command] = {
            "valid": is_valid,
            "sum": round(prob_sum, 2)
        }

    return report
