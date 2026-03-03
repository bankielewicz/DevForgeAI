"""
Test: AC#4 - Anti-Pattern-Scanner Phase 5 Updated with Progressive Disclosure
Story: STORY-407
Generated: 2026-02-16

Validates that .claude/agents/anti-pattern-scanner.md Phase 5 section
includes progressive disclosure reference and lists all 11 smell types.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCANNER_PATH = os.path.join(
    PROJECT_ROOT, ".claude", "agents", "anti-pattern-scanner.md"
)

SMELL_NAMES = [
    "god object",
    "long method",
    "magic number",
    "data class",
    "long parameter list",
    "commented-out code",
    "orphaned import",
    "dead code",
    "placeholder code",
    "middle man",
    "message chain",
]


@pytest.fixture(scope="module")
def scanner_content():
    """Read anti-pattern-scanner.md content."""
    assert os.path.isfile(SCANNER_PATH), (
        f"anti-pattern-scanner.md not found at {SCANNER_PATH}"
    )
    with open(SCANNER_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def phase5_section(scanner_content):
    """Extract Phase 5 section from scanner content."""
    # Match Phase 5 heading to next same-level heading
    pattern = r"(?i)(#{2,3}\s+.*phase\s*5.*?code\s*smell.*?)(?=#{2,3}\s|\Z)"
    match = re.search(pattern, scanner_content, re.DOTALL)
    assert match, "Phase 5 (Code Smells) section not found in anti-pattern-scanner.md"
    return match.group(1)


class TestProgressiveDisclosure:
    """Tests for progressive disclosure reference in Phase 5."""

    def test_should_reference_code_smell_catalog(self, phase5_section):
        """Assert: Phase 5 references code-smell-catalog.md."""
        assert "code-smell-catalog.md" in phase5_section, (
            "Phase 5 should reference code-smell-catalog.md"
        )

    def test_should_have_load_instruction(self, phase5_section):
        """Assert: Phase 5 has progressive disclosure load instruction."""
        assert re.search(
            r"(?i)(load|read|see|refer).*code-smell-catalog", phase5_section
        ), "Phase 5 should have a load/reference instruction for the catalog"


class TestSmellTypeListing:
    """Tests for all 11 smell types listed in Phase 5."""

    @pytest.mark.parametrize("smell_name", SMELL_NAMES)
    def test_should_list_smell_type_in_phase5(self, phase5_section, smell_name):
        """Assert: Each smell type is listed in Phase 5."""
        assert smell_name.lower() in phase5_section.lower(), (
            f"Phase 5 should list '{smell_name}'"
        )

    def test_should_list_all_11_smell_types(self, phase5_section):
        """Assert: All 11 smell types are present."""
        found = sum(
            1 for name in SMELL_NAMES
            if name.lower() in phase5_section.lower()
        )
        assert found == 11, (
            f"Phase 5 should list all 11 smell types, found {found}"
        )
