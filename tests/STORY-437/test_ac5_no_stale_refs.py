"""
Test: AC#5 - No Stale References to Removed Content
Story: STORY-437
TDD Phase: RED - All tests should FAIL before implementation.

Grep sweep across orchestration skill directory verifying no stale
references to Phase 4A, Epic Creation Mode, or create-epic context
markers remain. Acceptable: "Epic -> Sprint -> Story" hierarchy mentions.
"""
import os
import re
import pytest


class TestNoPhase4AReferences:
    """Grep sweep: no 'Phase 4A' references remain."""

    def test_should_find_zero_phase_4a_refs_when_sweeping_all_files(self, all_orchestration_files):
        """No file in orchestration directory should reference Phase 4A."""
        violations = []
        for fpath, content in all_orchestration_files.items():
            if "Phase 4A" in content:
                violations.append(os.path.basename(fpath))
        assert violations == [], (
            f"Stale 'Phase 4A' references found in: {violations}"
        )


class TestNoEpicCreationModeReferences:
    """Grep sweep: no 'Epic Creation Mode' references remain."""

    def test_should_find_zero_epic_creation_mode_refs_when_sweeping(self, all_orchestration_files):
        """No file should reference 'Epic Creation Mode'."""
        violations = []
        for fpath, content in all_orchestration_files.items():
            if "Epic Creation Mode" in content:
                violations.append(os.path.basename(fpath))
        assert violations == [], (
            f"Stale 'Epic Creation Mode' references found in: {violations}"
        )


class TestNoCreateEpicContextMarkers:
    """Grep sweep: no 'create-epic' context marker references remain."""

    def test_should_find_zero_create_epic_markers_when_sweeping(self, all_orchestration_files):
        """No file should contain 'create-epic' context marker."""
        violations = []
        for fpath, content in all_orchestration_files.items():
            if "create-epic" in content:
                violations.append(os.path.basename(fpath))
        assert violations == [], (
            f"Stale 'create-epic' references found in: {violations}"
        )


class TestAcceptableEpicReferencesOnly:
    """Only acceptable 'Epic' refs remain (hierarchy mentions)."""

    def test_should_only_have_hierarchy_epic_refs_when_sweeping_skill_md(self, skill_md_content):
        """Any remaining 'Epic' mentions must be hierarchy references only."""
        # Find all lines containing "Epic" (case-sensitive)
        lines_with_epic = [
            line.strip()
            for line in skill_md_content.split("\n")
            if "Epic" in line
        ]

        # Filter out acceptable hierarchy patterns
        unacceptable = []
        acceptable_patterns = [
            r"Epic\s*->\s*Sprint",       # "Epic -> Sprint -> Story"
            r"Epic\s*→\s*Sprint",        # "Epic → Sprint → Story" (unicode arrow)
            r"Epic\s*>\s*Sprint",        # "Epic > Sprint"
            r"epic.*hierarchy",           # hierarchy mentions
            r"within\s+epics",           # "within epics"
            r"Epics\)",                  # "(Epics)" in description
            r"initiatives\s*\(Epics\)",  # "initiatives (Epics)"
            r"from.*Epics.*through",     # "from Epics through Stories"
        ]

        for line in lines_with_epic:
            is_acceptable = any(
                re.search(pat, line, re.IGNORECASE)
                for pat in acceptable_patterns
            )
            if not is_acceptable:
                unacceptable.append(line)

        assert unacceptable == [], (
            f"Non-hierarchy 'Epic' references found:\n" +
            "\n".join(f"  - {line}" for line in unacceptable)
        )

    def test_should_not_mention_starting_new_epic_when_skill_read(self, skill_md_content):
        """'Starting a new epic' must not appear anywhere."""
        assert "Starting a new epic" not in skill_md_content, (
            "Stale 'Starting a new epic' reference found"
        )
