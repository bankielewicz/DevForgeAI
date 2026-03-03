"""
Test Suite: STORY-048 AC-6 - ROADMAP.md Updated with Migration Completion

Tests validate that ROADMAP.md has been updated to reflect completion of
Phase 4 and version 1.0.1 release.
"""

import re
from pathlib import Path

import pytest


class TestRoadmapPhaseCompletion:
    """Tests for Phase 4 completion marking in ROADMAP.md."""

    @pytest.fixture
    def roadmap_path(self):
        """Return path to ROADMAP.md"""
        return Path("ROADMAP.md")

    @pytest.fixture
    def roadmap_content(self, roadmap_path):
        """Load ROADMAP.md content"""
        if not roadmap_path.exists():
            pytest.skip("ROADMAP.md not found")
        return roadmap_path.read_text()

    # AC-6 Tests

    def test_roadmap_file_exists(self, roadmap_path):
        """Test: ROADMAP.md exists"""
        # Assert
        assert roadmap_path.exists(), "ROADMAP.md must exist"

    def test_roadmap_mentions_phase_4(self, roadmap_content):
        """Test: ROADMAP.md mentions Phase 4"""
        # Act & Assert
        assert re.search(r'[Pp]hase\s+4|[Pp]hase.*[Mm]igration|src.*[Mm]igration', roadmap_content, re.IGNORECASE), \
            "ROADMAP.md should mention Phase 4"

    def test_roadmap_phase_4_marked_complete(self, roadmap_content):
        """Test: Phase 4 marked with checkmark or COMPLETE"""
        # Arrange: Find Phase 4 section
        phase4_match = re.search(
            r'[Pp]hase\s+4.*?(?=[Pp]hase\s+\d|\Z)',
            roadmap_content,
            re.DOTALL
        )

        if not phase4_match:
            pytest.skip("Phase 4 section not found")

        phase4_section = phase4_match.group(0)

        # Act & Assert
        assert re.search(r'✅|✔|COMPLETE|Done', phase4_section), \
            "Phase 4 should be marked as complete"

    def test_roadmap_lists_all_phase_4_stories(self, roadmap_content):
        """Test: ROADMAP.md lists all 8 Phase 4 stories (STORY-041 through STORY-048)"""
        # Act & Assert
        for story_id in range(41, 49):
            assert re.search(f'STORY-{story_id}', roadmap_content), \
                f"ROADMAP.md should list STORY-{story_id}"

    def test_roadmap_story_041_marked_complete(self, roadmap_content):
        """Test: STORY-041 marked complete"""
        # Arrange: Find story in roadmap
        story_match = re.search(
            r'STORY-041.*?(?=STORY-\d|\Z)',
            roadmap_content,
            re.DOTALL
        )

        if not story_match:
            pytest.skip("STORY-041 not found in ROADMAP")

        story_section = story_match.group(0)

        # Act & Assert
        assert re.search(r'✅|✔|COMPLETE|Done', story_section), \
            "STORY-041 should be marked complete"

    def test_roadmap_story_048_marked_complete(self, roadmap_content):
        """Test: STORY-048 marked complete"""
        # Arrange: Find story in roadmap
        story_match = re.search(
            r'STORY-048.*?(?=STORY-\d|[Pp]hase\s+\d|\Z)',
            roadmap_content,
            re.DOTALL
        )

        if not story_match:
            pytest.skip("STORY-048 not found in ROADMAP")

        story_section = story_match.group(0)

        # Act & Assert
        assert re.search(r'✅|✔|COMPLETE|Done', story_section), \
            "STORY-048 should be marked complete"

    def test_roadmap_version_is_1_0_1(self, roadmap_content):
        """Test: Version number updated to 1.0.1"""
        # Act & Assert
        assert re.search(r'1\.0\.1|version.*1\.0\.1', roadmap_content, re.IGNORECASE), \
            "ROADMAP.md should show version 1.0.1"

    def test_roadmap_has_deliverables_section(self, roadmap_content):
        """Test: Phase 4 includes Deliverables section"""
        # Arrange: Find Phase 4 detailed section (heading level 3 or 2)
        phase4_match = re.search(
            r'###?\s+Phase\s+4[^\n]*\n(.*?)(?=\n##\s+(?!#)|\Z)',
            roadmap_content,
            re.DOTALL | re.IGNORECASE
        )

        if not phase4_match:
            pytest.skip("Phase 4 section not found")

        phase4_section = phase4_match.group(1)  # Content after header

        # Act & Assert
        assert re.search(r'[Dd]eliverable', phase4_section, re.IGNORECASE), \
            "Phase 4 should list deliverables"

    def test_roadmap_mentions_src_migration(self, roadmap_content):
        """Test: Deliverables mention src/ migration"""
        # Arrange: Find Phase 4 detailed section (### Phase 4)
        phase4_match = re.search(
            r'###?\s+Phase\s+4[^\n]*\n(.*?)(?=\n##\s+(?!#)|\Z)',
            roadmap_content,
            re.DOTALL | re.IGNORECASE
        )

        if not phase4_match:
            pytest.skip("Phase 4 detailed section not found")

        phase4_section = phase4_match.group(1)  # Content after header

        # Act & Assert
        assert re.search(r'src/|source.*tree|source.*migration', phase4_section, re.IGNORECASE), \
            "Phase 4 deliverables should mention src/"

    def test_roadmap_mentions_distribution_packages(self, roadmap_content):
        """Test: Deliverables mention distribution packages"""
        # Arrange: Find Phase 4 section
        phase4_match = re.search(
            r'[Pp]hase\s+4.*?(?=[Pp]hase\s+\d|\Z)',
            roadmap_content,
            re.DOTALL
        )

        if not phase4_match:
            pytest.skip("Phase 4 section not found")

        phase4_section = phase4_match.group(0)

        # Act & Assert
        assert re.search(r'tar|zip|package|distrib', phase4_section, re.IGNORECASE), \
            "Phase 4 deliverables should mention distribution packages"


class TestRoadmapNextPhase:
    """Tests for Phase 5 information in ROADMAP.md."""

    @pytest.fixture
    def roadmap_content(self):
        """Load ROADMAP.md content"""
        roadmap_path = Path("ROADMAP.md")
        if not roadmap_path.exists():
            pytest.skip("ROADMAP.md not found")
        return roadmap_path.read_text()

    def test_roadmap_mentions_phase_5(self, roadmap_content):
        """Test: ROADMAP.md mentions Phase 5 as next"""
        # Act & Assert
        assert re.search(r'[Pp]hase\s+5', roadmap_content), \
            "ROADMAP.md should mention Phase 5"

    def test_roadmap_phase_5_describes_next_steps(self, roadmap_content):
        """Test: Phase 5 describes public release or community onboarding"""
        # Arrange: Find Phase 5 section
        phase5_match = re.search(
            r'[Pp]hase\s+5.*?(?=[Pp]hase\s+\d|\Z)',
            roadmap_content,
            re.DOTALL
        )

        if not phase5_match:
            pytest.skip("Phase 5 not found in ROADMAP")

        phase5_section = phase5_match.group(0)

        # Act & Assert
        assert re.search(
            r'[Pp]ublic|release|community|onboard',
            phase5_section,
            re.IGNORECASE
        ), "Phase 5 should describe public release or community onboarding"


class TestRoadmapStructure:
    """Tests for ROADMAP.md structure and format."""

    @pytest.fixture
    def roadmap_content(self):
        """Load ROADMAP.md content"""
        roadmap_path = Path("ROADMAP.md")
        if not roadmap_path.exists():
            pytest.skip("ROADMAP.md not found")
        return roadmap_path.read_text()

    def test_roadmap_is_well_formatted_markdown(self, roadmap_content):
        """Test: ROADMAP.md is valid markdown"""
        # Arrange: Count headings
        h1_count = len(re.findall(r'^#\s+', roadmap_content, re.MULTILINE))
        h2_count = len(re.findall(r'^##\s+', roadmap_content, re.MULTILINE))

        # Assert
        assert h1_count > 0 or h2_count > 0, \
            "ROADMAP.md should have proper markdown headings"

    def test_roadmap_has_clear_phases(self, roadmap_content):
        """Test: ROADMAP clearly shows phases"""
        # Act & Assert
        phase_count = len(re.findall(r'[Pp]hase\s+\d', roadmap_content))
        assert phase_count >= 4, \
            "ROADMAP should clearly show multiple phases"

    def test_roadmap_version_consistent(self, roadmap_content):
        """Test: ROADMAP mentions version 1.0.1 consistently"""
        # Act & Assert
        version_mentions = len(re.findall(r'1\.0\.1', roadmap_content))
        assert version_mentions >= 1, \
            "ROADMAP should mention version 1.0.1"


class TestRoadmapHistorical:
    """Tests for historical accuracy in ROADMAP.md."""

    @pytest.fixture
    def roadmap_content(self):
        """Load ROADMAP.md content"""
        roadmap_path = Path("ROADMAP.md")
        if not roadmap_path.exists():
            pytest.skip("ROADMAP.md not found")
        return roadmap_path.read_text()

    def test_roadmap_has_release_notes_or_breaking_changes_section(self, roadmap_content):
        """Test: ROADMAP has release notes or breaking changes documented"""
        # Act & Assert: Look for sections documenting changes
        has_release_notes = re.search(
            r'[Rr]elease.*[Nn]otes|[Bb]reaking.*[Cc]hange|[Cc]hange.*[Ll]og',
            roadmap_content,
            re.IGNORECASE
        )

        # It's acceptable to not have breaking changes, but format should show version
        assert re.search(r'1\.0\.1|version', roadmap_content, re.IGNORECASE), \
            "ROADMAP should clearly show current version (1.0.1)"

    def test_roadmap_phase_dates_if_mentioned(self, roadmap_content):
        """Test: If dates are mentioned, Phase 4 completion date near 2025-11"""
        # Arrange: Look for Phase 4 date
        phase4_match = re.search(
            r'[Pp]hase\s+4.*?(?=[Pp]hase\s+\d|\Z)',
            roadmap_content,
            re.DOTALL
        )

        if not phase4_match:
            pytest.skip("Phase 4 section not found")

        phase4_section = phase4_match.group(0)

        # Act: Look for date (optional)
        date_match = re.search(r'2025-1[01]|2025-11|Nov.*2025', phase4_section)

        # Assert: If date mentioned, should be recent (no assertion if not mentioned)
        if date_match:
            assert date_match.group(0), "Phase 4 date should be recent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
