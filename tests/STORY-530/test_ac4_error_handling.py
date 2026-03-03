#!/usr/bin/env python3
"""
Test: AC#4 - Error Handling Instructions
Story: STORY-530
Generated: 2026-03-03

Validates error handling instructions in Progressive Task Disclosure sections:
- Missing registry -> HALT referencing STORY-525
- Malformed JSON -> HALT
- Invalid entries -> skip with warning
"""

import os
import pytest

PHASES_DIR = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), "..", "..",
        "src", "claude", "skills", "implementing-stories", "phases"
    )
)

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


def _extract_section(content: str, heading: str) -> str | None:
    """Extract content from heading to next same-level heading."""
    lines = content.split("\n")
    in_section = False
    section_lines = []
    heading_level = heading.count("#")

    for line in lines:
        if line.strip().startswith(heading):
            in_section = True
            continue
        if in_section:
            stripped = line.lstrip()
            if stripped.startswith("#"):
                hashes = len(stripped) - len(stripped.lstrip("#"))
                if hashes <= heading_level:
                    break
            section_lines.append(line)

    return "\n".join(section_lines) if section_lines else None


class TestMissingRegistryHalt:
    """AC#4: Missing registry triggers HALT referencing STORY-525."""

    @pytest.fixture(params=PHASE_FILES)
    def phase_section(self, request):
        filepath = os.path.join(PHASES_DIR, request.param)
        assert os.path.exists(filepath), f"Phase file not found: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        section = _extract_section(content, "## Progressive Task Disclosure")
        return {"name": request.param, "section": section}

    def test_should_halt_when_registry_missing(self, phase_section):
        """Arrange: Section loaded. Act: Check for HALT. Assert: HALT present for missing registry."""
        section = phase_section["section"]
        name = phase_section["name"]
        assert section is not None, f"{name} missing Progressive Task Disclosure section"
        assert "HALT" in section, (
            f"{name} missing HALT instruction for missing registry"
        )

    def test_should_reference_story_525_when_registry_missing(self, phase_section):
        """Arrange: Section loaded. Act: Check STORY-525 ref. Assert: STORY-525 referenced."""
        section = phase_section["section"]
        name = phase_section["name"]
        assert section is not None, f"{name} missing Progressive Task Disclosure section"
        assert "STORY-525" in section, (
            f"{name} missing STORY-525 reference for missing registry HALT"
        )


class TestMalformedJsonHalt:
    """AC#4: Malformed JSON triggers HALT."""

    @pytest.fixture(params=PHASE_FILES)
    def phase_section(self, request):
        filepath = os.path.join(PHASES_DIR, request.param)
        assert os.path.exists(filepath), f"Phase file not found: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        section = _extract_section(content, "## Progressive Task Disclosure")
        return {"name": request.param, "section": section}

    def test_should_halt_when_json_malformed(self, phase_section):
        """Arrange: Section loaded. Act: Check malformed JSON handling. Assert: HALT present."""
        section = phase_section["section"]
        name = phase_section["name"]
        assert section is not None, f"{name} missing Progressive Task Disclosure section"
        has_malformed_handling = (
            "malformed" in section.lower()
            or "invalid json" in section.lower()
            or "parse error" in section.lower()
            or "json error" in section.lower()
        )
        assert has_malformed_handling, (
            f"{name} missing malformed JSON HALT instruction"
        )


class TestInvalidEntriesSkip:
    """AC#4: Invalid entries are skipped with warning."""

    @pytest.fixture(params=PHASE_FILES)
    def phase_section(self, request):
        filepath = os.path.join(PHASES_DIR, request.param)
        assert os.path.exists(filepath), f"Phase file not found: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        section = _extract_section(content, "## Progressive Task Disclosure")
        return {"name": request.param, "section": section}

    def test_should_skip_invalid_entries_with_warning(self, phase_section):
        """Arrange: Section loaded. Act: Check skip logic. Assert: Skip with warning present."""
        section = phase_section["section"]
        name = phase_section["name"]
        assert section is not None, f"{name} missing Progressive Task Disclosure section"
        has_skip = "skip" in section.lower()
        has_warning = "warning" in section.lower() or "warn" in section.lower()
        assert has_skip and has_warning, (
            f"{name} missing 'skip with warning' instruction for invalid entries"
        )
