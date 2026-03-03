#!/usr/bin/env python3
"""
Test: AC#1 - Progressive Task Disclosure Section Presence
Story: STORY-530
Generated: 2026-03-03

Validates that all 12 phase files contain a "## Progressive Task Disclosure"
section with required subsections: purpose statement, registry read instruction,
phase filtering logic, and TaskCreate instructions.
"""

import os
import pytest

# Base path for phase files under src/ tree
PHASES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "src", "claude", "skills", "implementing-stories", "phases"
)
PHASES_DIR = os.path.normpath(PHASES_DIR)

PHASE_FILES = [
    "phase-01-preflight.md",
    "phase-02-test-first.md",
    "phase-03-implementation.md",
    "phase-04-refactoring.md",
    "phase-04.5-ac-verification.md",
    "phase-05-integration.md",
    "phase-05.5-ac-verification.md",
    "phase-06-deferral.md",
    "phase-07-dod-update.md",
    "phase-08-git-workflow.md",
    "phase-09-feedback.md",
    "phase-10-result.md",
]


class TestSectionPresence:
    """AC#1: All 12 phase files contain Progressive Task Disclosure section."""

    @pytest.fixture(params=PHASE_FILES)
    def phase_content(self, request):
        """Load phase file content for parameterized tests."""
        filepath = os.path.join(PHASES_DIR, request.param)
        assert os.path.exists(filepath), f"Phase file not found: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            return {"name": request.param, "content": f.read()}

    def test_should_contain_progressive_task_disclosure_heading_when_phase_file_read(
        self, phase_content
    ):
        """Arrange: Phase file loaded. Act: Search for heading. Assert: Heading exists."""
        content = phase_content["content"]
        name = phase_content["name"]
        assert "## Progressive Task Disclosure" in content, (
            f"{name} missing '## Progressive Task Disclosure' section"
        )

    def test_should_contain_purpose_statement_when_section_present(
        self, phase_content
    ):
        """Arrange: Phase file loaded. Act: Search for purpose. Assert: Purpose exists."""
        content = phase_content["content"]
        name = phase_content["name"]
        # Section must exist first
        assert "## Progressive Task Disclosure" in content, (
            f"{name} missing section entirely"
        )
        # Extract section content (from heading to next ## heading)
        section = _extract_section(content, "## Progressive Task Disclosure")
        assert section is not None, f"{name} could not extract section"
        # Purpose statement should mention "purpose" or describe intent
        assert "purpose" in section.lower() or "intent" in section.lower(), (
            f"{name} Progressive Task Disclosure section missing purpose statement"
        )

    def test_should_contain_registry_read_instruction_when_section_present(
        self, phase_content
    ):
        """Arrange: Phase file loaded. Act: Search for registry ref. Assert: Registry referenced."""
        content = phase_content["content"]
        name = phase_content["name"]
        section = _extract_section(content, "## Progressive Task Disclosure")
        assert section is not None, f"{name} could not extract section"
        assert "phase-steps-registry.json" in section, (
            f"{name} section missing reference to phase-steps-registry.json"
        )

    def test_should_contain_phase_filtering_logic_when_section_present(
        self, phase_content
    ):
        """Arrange: Phase file loaded. Act: Search for filter logic. Assert: Filtering present."""
        content = phase_content["content"]
        name = phase_content["name"]
        section = _extract_section(content, "## Progressive Task Disclosure")
        assert section is not None, f"{name} could not extract section"
        # Should reference filtering for current phase
        has_filter = (
            "filter" in section.lower()
            or "current phase" in section.lower()
            or "phase_id" in section.lower()
        )
        assert has_filter, (
            f"{name} section missing phase filtering logic"
        )

    def test_should_contain_taskcreate_instruction_when_section_present(
        self, phase_content
    ):
        """Arrange: Phase file loaded. Act: Search for TaskCreate. Assert: TaskCreate present."""
        content = phase_content["content"]
        name = phase_content["name"]
        section = _extract_section(content, "## Progressive Task Disclosure")
        assert section is not None, f"{name} could not extract section"
        assert "TaskCreate" in section, (
            f"{name} section missing TaskCreate instruction"
        )


def _extract_section(content: str, heading: str) -> str | None:
    """Extract content from a heading to the next same-level heading."""
    lines = content.split("\n")
    in_section = False
    section_lines = []
    heading_level = heading.count("#")

    for line in lines:
        if line.strip().startswith(heading):
            in_section = True
            continue
        if in_section:
            # Stop at next heading of same or higher level
            stripped = line.lstrip()
            if stripped.startswith("#"):
                hashes = len(stripped) - len(stripped.lstrip("#"))
                if hashes <= heading_level:
                    break
            section_lines.append(line)

    return "\n".join(section_lines) if section_lines else None
