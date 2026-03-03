"""
Audit module for verifying explicit Skill(command="...") invocation patterns
in DevForgeAI command files.

This module provides functions and data classes to audit command files for
compliant Skill() invocation syntax, detect non-compliant summary language,
and generate structured audit reports.

STORY-356: Audit Other Commands for Similar Skill Invocation Pattern
"""
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path("/mnt/c/Projects/DevForgeAI2")
SRC_COMMANDS_DIR = PROJECT_ROOT / "src" / "claude" / "commands"

# BR-001: Compliance regex - must match Skill(command="<skill-name>"
SKILL_INVOCATION_REGEX = re.compile(r'Skill\(command="[a-z0-9-]+"')


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------
@dataclass
class AuditResult:
    """Result of auditing a single command file for Skill() invocation compliance."""

    command_name: str
    skill_name: str
    file_found: bool
    line_number: Optional[int]
    compliant: bool
    status: str
    remediation_needed: bool
    matched_text: Optional[str]
    invocation_count: int

    def to_dict(self) -> dict:
        """Serialize the audit result to a dictionary."""
        return {
            "command_name": self.command_name,
            "skill_name": self.skill_name,
            "file_found": self.file_found,
            "line_number": self.line_number,
            "compliant": self.compliant,
            "status": self.status,
            "remediation_needed": self.remediation_needed,
            "matched_text": self.matched_text,
            "invocation_count": self.invocation_count,
        }


@dataclass
class AuditReport:
    """Summary report of all audit findings."""

    findings: List[AuditResult] = field(default_factory=list)
    total_audited: int = 0
    compliant_count: int = 0
    non_compliant_count: int = 0
    not_found_count: int = 0

    def to_dict(self) -> dict:
        """Serialize the audit report to a dictionary with findings and summary."""
        return {
            "findings": [f.to_dict() for f in self.findings],
            "summary": {
                "total_audited": self.total_audited,
                "compliant_count": self.compliant_count,
                "non_compliant_count": self.non_compliant_count,
                "not_found_count": self.not_found_count,
            },
        }


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------
def _find_compliant_invocations(
    content: str,
    skill_name: Optional[str] = None,
) -> List[tuple]:
    """
    Find Skill(command="...") invocations excluding those in WRONG example sections.

    Args:
        content: File content to search.
        skill_name: If provided, only match invocations for this specific skill.
            If None, matches any Skill(command="...") pattern.

    Returns list of (line_number, matched_text) tuples with 1-indexed line numbers.
    """
    # Use skill-specific regex if skill_name provided, otherwise generic BR-001 regex
    if skill_name:
        pattern = re.compile(rf'Skill\(command="{re.escape(skill_name)}"')
    else:
        pattern = SKILL_INVOCATION_REGEX

    lines = content.splitlines()
    matches = []
    for line_idx, line in enumerate(lines):
        match = pattern.search(line)
        if match:
            # Check preceding 5 lines for WRONG markers
            start = max(0, line_idx - 5)
            preceding_context = "\n".join(lines[start:line_idx])
            if re.search(r"\bWRONG\b", preceding_context, re.IGNORECASE):
                continue  # Skip - inside a WRONG example section
            matches.append((line_idx + 1, match.group()))
    return matches


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def audit_command(
    command_name: str,
    skill_name: str,
    content_override: Optional[str] = None,
) -> AuditResult:
    """
    Audit a single command file for explicit Skill(command="...") invocation.

    Args:
        command_name: The command name (e.g., "ideate", "create-epic").
        skill_name: The expected skill invocation name (e.g., "devforgeai-ideation").
        content_override: If provided, audit this content instead of reading from disk.

    Returns:
        AuditResult with compliance details.
    """
    # Determine content source
    if content_override is not None:
        content = content_override
        file_found = True
    else:
        file_path = SRC_COMMANDS_DIR / f"{command_name}.md"
        if not file_path.exists():
            return AuditResult(
                command_name=command_name,
                skill_name=skill_name,
                file_found=False,
                line_number=None,
                compliant=False,
                status="NOT FOUND",
                remediation_needed=True,
                matched_text=None,
                invocation_count=0,
            )
        content = file_path.read_text(encoding="utf-8")
        file_found = True

    # Find compliant invocations for the specific skill (excluding WRONG example sections)
    compliant_matches = _find_compliant_invocations(content, skill_name=skill_name)

    if compliant_matches:
        first_line, first_text = compliant_matches[0]
        return AuditResult(
            command_name=command_name,
            skill_name=skill_name,
            file_found=file_found,
            line_number=first_line,
            compliant=True,
            status="COMPLIANT",
            remediation_needed=False,
            matched_text=first_text,
            invocation_count=len(compliant_matches),
        )

    # No compliant invocations found
    return AuditResult(
        command_name=command_name,
        skill_name=skill_name,
        file_found=file_found,
        line_number=None,
        compliant=False,
        status="NON-COMPLIANT",
        remediation_needed=True,
        matched_text=None,
        invocation_count=0,
    )


def generate_audit_report(
    command_skill_map: Dict[str, str],
    content_overrides: Optional[Dict[str, str]] = None,
) -> AuditReport:
    """
    Generate an audit report for multiple commands.

    Args:
        command_skill_map: Mapping of command name to expected skill name.
        content_overrides: Optional mapping of command name to content string
            to use instead of reading from disk.

    Returns:
        AuditReport with findings and summary counts.
    """
    if content_overrides is None:
        content_overrides = {}

    findings: List[AuditResult] = []
    for command_name, skill_name in command_skill_map.items():
        override = content_overrides.get(command_name)
        result = audit_command(command_name, skill_name, content_override=override)
        findings.append(result)

    # Compute summary counts
    compliant_count = sum(1 for f in findings if f.status == "COMPLIANT")
    non_compliant_count = sum(1 for f in findings if f.status == "NON-COMPLIANT")
    not_found_count = sum(1 for f in findings if f.status == "NOT FOUND")

    return AuditReport(
        findings=findings,
        total_audited=len(findings),
        compliant_count=compliant_count,
        non_compliant_count=non_compliant_count,
        not_found_count=not_found_count,
    )
