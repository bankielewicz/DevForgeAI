"""
Test: AC#1 - ASCII Progress Bar Rendering
Story: STORY-470 (Terminal-Compatible Gamification)
Generated: 2026-03-04

Verifies celebration-engine.md has ASCII progress bar patterns
using ASCII-safe characters only.
"""

import pytest
from pathlib import Path

# Project root resolved from test file location
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CELEBRATION_ENGINE = PROJECT_ROOT / "src" / "claude" / "skills" / "coaching-entrepreneur" / "references" / "celebration-engine.md"


class TestCelebrationEngineFileExists:
    """Verify the celebration engine reference file exists."""

    def test_celebration_engine_file_exists(self):
        """Arrange: Path to celebration-engine.md in src/ tree.
        Act: Check file existence.
        Assert: File exists on disk."""
        assert CELEBRATION_ENGINE.exists(), (
            f"celebration-engine.md not found at {CELEBRATION_ENGINE}"
        )


class TestAsciiProgressBarSection:
    """Verify ASCII progress bar patterns section exists and has correct content."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        """Load celebration engine content for all tests in this class."""
        self.content = CELEBRATION_ENGINE.read_text(encoding="utf-8")

    def test_ascii_progress_patterns_section_exists(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for ascii-progress-patterns section header.
        Assert: Section header found in document."""
        assert "ascii-progress-patterns" in self.content.lower() or "ASCII Progress" in self.content, (
            "Missing 'ascii-progress-patterns' section in celebration-engine.md"
        )

    def test_progress_bar_uses_block_characters(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for block fill character used in progress bars.
        Assert: Contains block characters for progress rendering."""
        # Must contain the filled block character used in progress bars
        assert "\u2588" in self.content or "█" in self.content, (
            "Missing filled block character (█) for progress bar rendering"
        )

    def test_progress_bar_uses_empty_block_characters(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for empty/light block character.
        Assert: Contains light shade character for unfilled portion."""
        assert "\u2591" in self.content or "░" in self.content, (
            "Missing light shade character (░) for empty progress bar portion"
        )

    def test_progress_bar_shows_percentage(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for percentage display pattern.
        Assert: Contains percentage indicator in progress bar example."""
        assert "%" in self.content, (
            "Missing percentage indicator in progress bar pattern"
        )

    def test_progress_bar_example_present(self):
        """Arrange: Celebration engine content loaded.
        Act: Search for a complete progress bar example line.
        Assert: Contains example combining block chars and percentage."""
        lines = self.content.split("\n")
        has_example = any(
            ("█" in line or "\u2588" in line) and "%" in line
            for line in lines
        )
        assert has_example, (
            "Missing complete progress bar example (e.g., '████████░░░░ 60% Complete')"
        )


class TestAsciiSafeCharacters:
    """BR-001: All visual elements must use ASCII-safe characters only."""

    @pytest.fixture(autouse=True)
    def load_content(self):
        self.content = CELEBRATION_ENGINE.read_text(encoding="utf-8")

    def test_no_gui_specific_markup(self):
        """Arrange: Celebration engine content loaded.
        Act: Check for HTML/GUI-specific tags.
        Assert: No GUI markup present (NFR-001)."""
        gui_markers = ["<div", "<span", "<canvas", "<svg", "<img"]
        for marker in gui_markers:
            assert marker not in self.content.lower(), (
                f"GUI-specific markup '{marker}' found - must be ASCII terminal only"
            )

    def test_progress_patterns_no_emoji(self):
        """Arrange: Celebration engine content loaded.
        Act: Check progress bar section for emoji characters.
        Assert: No emoji in progress bar patterns (ASCII-safe only)."""
        # Extract lines around progress patterns
        lines = self.content.split("\n")
        progress_lines = [
            line for line in lines
            if "█" in line or "░" in line or "progress" in line.lower()
        ]
        for line in progress_lines:
            for char in line:
                # Allow standard ASCII, extended Latin, and block drawing chars
                code_point = ord(char)
                if code_point > 0x2600 and code_point < 0x27BF:
                    pytest.fail(
                        f"Emoji character U+{code_point:04X} found in progress pattern line: {line[:60]}"
                    )
