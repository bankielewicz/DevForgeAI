"""
STORY-274: Verification Report Generator

Functions for generating AC compliance verification reports.
Reports are written to devforgeai/qa/verification/{STORY-ID}-ac-verification.json
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

from devforgeai.qa.verification.models import ACResult, Issue, VerificationReport


def get_report_path(story_id: str) -> str:
    """
    Get the file path for a verification report.

    Args:
        story_id: Story identifier (e.g., "STORY-274")

    Returns:
        Path to the verification report file:
        devforgeai/qa/verification/{story_id}-ac-verification.json
    """
    return f"devforgeai/qa/verification/{story_id}-ac-verification.json"


def calculate_overall_result(ac_results: List[ACResult]) -> str:
    """
    Calculate overall verification result from AC results.

    Business Rule BR-001: Overall PASS requires ALL ACs to PASS.
    If any AC fails, overall result is FAIL.

    Args:
        ac_results: List of ACResult objects

    Returns:
        "PASS" if all ACs pass, "FAIL" otherwise
    """
    if not ac_results:
        # No ACs to verify means can't determine PASS
        return "FAIL"

    for ac in ac_results:
        if hasattr(ac, 'result'):
            if ac.result == "FAIL":
                return "FAIL"
        elif isinstance(ac, dict) and ac.get('result') == "FAIL":
            return "FAIL"

    return "PASS"


def generate_verification_report(
    story_id: str,
    verification_results: Dict[str, Any],
    phase: str = "4.5",
    start_time: datetime = None,
) -> Dict[str, Any]:
    """
    Generate a verification report and write it to file.

    Args:
        story_id: Story identifier (e.g., "STORY-274")
        verification_results: Dict containing:
            - acceptance_criteria: List of AC results
            - files_inspected: List of file paths inspected
        phase: Verification phase ("4.5" or "5.5")
        start_time: When verification started (for duration calculation)

    Returns:
        Report dictionary containing all verification data

    Raises:
        PermissionError: If directory cannot be created
        OSError: If file cannot be written
    """
    # Calculate timing
    end_time = datetime.now(timezone.utc)
    if start_time is None:
        start_time = end_time
    duration_seconds = int((end_time - start_time).total_seconds())

    # Extract data from verification_results
    ac_results_data = verification_results.get("acceptance_criteria", [])
    files_inspected = verification_results.get("files_inspected", [])

    # Convert AC results to ACResult objects if they are dicts
    ac_results = []
    for ac_data in ac_results_data:
        if isinstance(ac_data, ACResult):
            ac_results.append(ac_data)
        elif isinstance(ac_data, dict):
            # Convert issues to Issue objects if they are dicts
            issues_data = ac_data.get("issues", [])
            issues = []
            for issue_data in issues_data:
                if isinstance(issue_data, Issue):
                    issues.append(issue_data)
                elif isinstance(issue_data, dict):
                    issues.append(Issue(
                        file_path=issue_data.get("file_path", ""),
                        line_number=issue_data.get("line_number", 1),
                        description=issue_data.get("description", ""),
                    ))

            ac_results.append(ACResult(
                ac_id=ac_data.get("ac_id", ""),
                result=ac_data.get("result", "FAIL"),
                evidence=ac_data.get("evidence", {}),
                issues=issues,
            ))

    # Calculate overall result (BR-001)
    overall_result = calculate_overall_result(ac_results)

    # Calculate total issues
    total_issues = sum(
        len(ac.issues) if hasattr(ac, 'issues') else 0
        for ac in ac_results
    )

    # Create report
    report = VerificationReport(
        story_id=story_id,
        verification_timestamp=end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        verification_duration_seconds=duration_seconds,
        phase=phase,
        overall_result=overall_result,
        acceptance_criteria=ac_results,
        files_inspected=files_inspected,
        total_issues=total_issues,
    )

    # Get report path
    report_path = get_report_path(story_id)

    # Create directory if it doesn't exist
    report_dir = os.path.dirname(report_path)
    if report_dir:
        os.makedirs(report_dir, exist_ok=True)

    # Write report to file
    report_dict = report.to_dict()
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_dict, f, indent=2, ensure_ascii=False)

    return report_dict
