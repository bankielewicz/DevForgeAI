"""
Test: AC#3 - /assess-me Command
Story: STORY-466
Phase: TDD Red (tests must FAIL until implementation is complete)

Verifies:
- assess-me.md exists at src/claude/commands/assess-me.md
- File has valid YAML frontmatter with 'description' and 'argument-hint' fields
- File is under 500 lines (NFR-001)
- File contains a Skill() invocation of the assessing-entrepreneur skill
"""

import os
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

ASSESS_ME_PATH = os.path.join(
    PROJECT_ROOT, "src", "claude", "commands", "assess-me.md"
)

MAX_LINE_COUNT = 500


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _parse_yaml_frontmatter(content: str) -> dict:
    """
    Extract key-value pairs from YAML frontmatter delimited by '---'.
    Returns an empty dict if no valid frontmatter found.
    """
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    frontmatter_text = match.group(1)
    result = {}
    for line in frontmatter_text.splitlines():
        kv = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if kv:
            result[kv.group(1)] = kv.group(2).strip()
    return result


# ---------------------------------------------------------------------------
# File existence tests
# ---------------------------------------------------------------------------


class TestAssessMeCommandExists:
    """AC#3: assess-me.md must exist at the expected src/ path."""

    def test_assess_me_md_file_exists(self):
        """assess-me.md must be present at src/claude/commands/assess-me.md."""
        assert os.path.isfile(ASSESS_ME_PATH), (
            f"assess-me.md not found at expected path: {ASSESS_ME_PATH}\n"
            "This file must be created as part of STORY-466 implementation."
        )


# ---------------------------------------------------------------------------
# YAML frontmatter tests
# ---------------------------------------------------------------------------


class TestAssessMeFrontmatter:
    """AC#3: assess-me.md must have valid YAML frontmatter with required fields."""

    def test_assess_me_has_yaml_frontmatter(self):
        """assess-me.md must start with a '---' frontmatter block."""
        content = _read_file(ASSESS_ME_PATH)
        assert content.startswith("---"), (
            "assess-me.md does not start with YAML frontmatter ('---')"
        )
        assert re.match(r"^---\s*\n.*?\n---", content, re.DOTALL), (
            "assess-me.md has no valid closing '---' for YAML frontmatter"
        )

    def test_assess_me_frontmatter_has_description(self):
        """Frontmatter must include a non-empty 'description' field."""
        content = _read_file(ASSESS_ME_PATH)
        frontmatter = _parse_yaml_frontmatter(content)
        assert "description" in frontmatter, (
            "assess-me.md frontmatter missing required 'description' field"
        )
        assert frontmatter["description"], (
            "assess-me.md frontmatter 'description' field must not be empty"
        )

    def test_assess_me_frontmatter_has_argument_hint(self):
        """Frontmatter must include a non-empty 'argument-hint' field."""
        content = _read_file(ASSESS_ME_PATH)
        frontmatter = _parse_yaml_frontmatter(content)
        assert "argument-hint" in frontmatter, (
            "assess-me.md frontmatter missing required 'argument-hint' field"
        )
        assert frontmatter["argument-hint"], (
            "assess-me.md frontmatter 'argument-hint' field must not be empty"
        )

    def test_assess_me_description_is_meaningful(self):
        """'description' must describe the assessment purpose (not a placeholder)."""
        content = _read_file(ASSESS_ME_PATH)
        frontmatter = _parse_yaml_frontmatter(content)
        description = frontmatter.get("description", "")
        # Must have at least 10 chars to be a real description
        assert len(description) >= 10, (
            f"assess-me.md description is too short to be meaningful: '{description}'"
        )


# ---------------------------------------------------------------------------
# Line count tests
# ---------------------------------------------------------------------------


class TestAssessMeLineCount:
    """AC#3 + NFR-001: assess-me.md must be under 500 lines."""

    def test_assess_me_under_500_lines(self):
        """assess-me.md file must be fewer than 500 lines (NFR-001)."""
        content = _read_file(ASSESS_ME_PATH)
        line_count = len(content.splitlines())
        assert line_count < MAX_LINE_COUNT, (
            f"assess-me.md exceeds 500-line limit: {line_count} lines. "
            f"Keep commands lean per source-tree.md conventions."
        )


# ---------------------------------------------------------------------------
# Skill invocation tests
# ---------------------------------------------------------------------------


class TestAssessMeSkillInvocation:
    """AC#3: assess-me.md must invoke the assessing-entrepreneur skill via Skill()."""

    def test_assess_me_invokes_assessing_entrepreneur_skill(self):
        """assess-me.md must contain a Skill() invocation referencing assessing-entrepreneur."""
        content = _read_file(ASSESS_ME_PATH)
        assert re.search(
            r'Skill\s*\(\s*["\']?assessing-entrepreneur["\']?', content
        ), (
            "assess-me.md does not contain Skill() invocation of 'assessing-entrepreneur'"
        )

    def test_assess_me_references_assessing_entrepreneur_skill_name(self):
        """assess-me.md body must mention 'assessing-entrepreneur' skill."""
        content = _read_file(ASSESS_ME_PATH)
        assert "assessing-entrepreneur" in content, (
            "assess-me.md does not reference the 'assessing-entrepreneur' skill"
        )
