"""
STORY-274: Data Models for AC Verification Reports

Data models:
- Issue: Issue with file path, line number, and description
- ACResult: Single AC verification result with pass/fail and evidence
- VerificationReport: Complete verification report with all AC results
"""

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Issue:
    """
    Issue detected during verification.

    Attributes:
        file_path: Path to the file containing the issue
        line_number: Line number where issue was found (must be >= 1)
        description: Description of the issue
    """
    file_path: str
    line_number: int
    description: str

    def __post_init__(self):
        """Validate Issue fields."""
        # Validate line_number is positive
        if not isinstance(self.line_number, int):
            raise TypeError(f"line_number must be int, got {type(self.line_number).__name__}")
        if self.line_number < 1:
            raise ValueError(f"line_number must be >= 1, got {self.line_number}")

        # Validate file_path is string
        if not isinstance(self.file_path, str):
            raise TypeError(f"file_path must be str, got {type(self.file_path).__name__}")

        # Validate description is string
        if not isinstance(self.description, str):
            raise TypeError(f"description must be str, got {type(self.description).__name__}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert Issue to dictionary for JSON serialization."""
        return {
            "file_path": self.file_path,
            "line_number": self.line_number,
            "description": self.description,
        }


@dataclass
class ACResult:
    """
    Single AC verification result.

    Attributes:
        ac_id: AC identifier (e.g., "AC#1")
        result: Pass/fail status (must be "PASS" or "FAIL")
        evidence: Supporting evidence for the determination
        issues: List of issues found for this AC
    """
    ac_id: str
    result: str
    evidence: Dict[str, Any]
    issues: List[Issue] = field(default_factory=list)

    def __post_init__(self):
        """Validate ACResult fields."""
        # Validate ac_id is non-empty string
        if not isinstance(self.ac_id, str) or len(self.ac_id) == 0:
            raise ValueError("ac_id must be non-empty string")

        # Validate result is PASS or FAIL
        if self.result not in ("PASS", "FAIL"):
            raise ValueError(f"result must be 'PASS' or 'FAIL', got '{self.result}'")

        # Validate evidence is dict
        if not isinstance(self.evidence, dict):
            raise TypeError(f"evidence must be dict, got {type(self.evidence).__name__}")

        # Validate issues is list
        if not isinstance(self.issues, list):
            raise TypeError(f"issues must be list, got {type(self.issues).__name__}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert ACResult to dictionary for JSON serialization."""
        return {
            "ac_id": self.ac_id,
            "result": self.result,
            "evidence": self.evidence,
            "issues": [issue.to_dict() if hasattr(issue, 'to_dict') else issue for issue in self.issues],
        }


@dataclass
class VerificationReport:
    """
    Complete AC verification report.

    Attributes:
        story_id: Story identifier (must match STORY-NNN pattern)
        verification_timestamp: When verification ran (ISO 8601 format)
        verification_duration_seconds: How long verification took (>= 0)
        phase: Which phase triggered verification ("4.5" or "5.5")
        overall_result: Overall verification result ("PASS" or "FAIL")
        acceptance_criteria: Per-AC results
        files_inspected: All files inspected during verification
        total_issues: Total number of issues found
    """
    story_id: str
    verification_timestamp: str
    verification_duration_seconds: int
    phase: str
    overall_result: str
    acceptance_criteria: List[ACResult]
    files_inspected: List[str]
    total_issues: int

    # Pattern for story ID validation
    STORY_ID_PATTERN = re.compile(r'^STORY-\d+$')

    # Valid phases
    VALID_PHASES = ("4.5", "5.5")

    # Valid results
    VALID_RESULTS = ("PASS", "FAIL")

    def __post_init__(self):
        """Validate VerificationReport fields."""
        # Validate story_id matches pattern
        if not isinstance(self.story_id, str) or not self.STORY_ID_PATTERN.match(self.story_id):
            raise ValueError(f"story_id must match STORY-NNN pattern, got '{self.story_id}'")

        # Validate verification_timestamp is string (ISO 8601 validation is loose)
        if not isinstance(self.verification_timestamp, str):
            raise TypeError(f"verification_timestamp must be str, got {type(self.verification_timestamp).__name__}")

        # Validate verification_duration_seconds is non-negative int
        if not isinstance(self.verification_duration_seconds, int):
            raise TypeError(f"verification_duration_seconds must be int, got {type(self.verification_duration_seconds).__name__}")
        if self.verification_duration_seconds < 0:
            raise ValueError(f"verification_duration_seconds must be >= 0, got {self.verification_duration_seconds}")

        # Validate phase
        if self.phase not in self.VALID_PHASES:
            raise ValueError(f"phase must be one of {self.VALID_PHASES}, got '{self.phase}'")

        # Validate overall_result
        if self.overall_result not in self.VALID_RESULTS:
            raise ValueError(f"overall_result must be one of {self.VALID_RESULTS}, got '{self.overall_result}'")

        # Validate acceptance_criteria is list
        if not isinstance(self.acceptance_criteria, list):
            raise TypeError(f"acceptance_criteria must be list, got {type(self.acceptance_criteria).__name__}")

        # Validate files_inspected is list of strings
        if not isinstance(self.files_inspected, list):
            raise TypeError(f"files_inspected must be list, got {type(self.files_inspected).__name__}")

        # Validate total_issues is non-negative
        if not isinstance(self.total_issues, int):
            raise TypeError(f"total_issues must be int, got {type(self.total_issues).__name__}")
        if self.total_issues < 0:
            raise ValueError(f"total_issues must be >= 0, got {self.total_issues}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert VerificationReport to dictionary for JSON serialization."""
        return {
            "story_id": self.story_id,
            "verification_timestamp": self.verification_timestamp,
            "verification_duration_seconds": self.verification_duration_seconds,
            "phase": self.phase,
            "overall_result": self.overall_result,
            "acceptance_criteria": [
                ac.to_dict() if hasattr(ac, 'to_dict') else ac
                for ac in self.acceptance_criteria
            ],
            "files_inspected": self.files_inspected,
            "total_issues": self.total_issues,
        }
