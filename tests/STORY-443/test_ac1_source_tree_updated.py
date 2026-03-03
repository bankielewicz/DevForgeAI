"""AC#1: source-tree.md Updated with New Skill Names.

Tests that devforgeai/specs/context/source-tree.md:
  (a) Lists discovering-requirements/ instead of devforgeai-ideation/
  (b) Lists brainstorming/ instead of devforgeai-brainstorming/
  (c) Lists designing-systems/ (no old devforgeai-architecture pattern)
  (d) Lists implementing-stories/ (already done; verify stable)
  (e) No old skill name directory references remain
  (f) Naming convention section references gerund pattern per ADR-017

All tests MUST FAIL before implementation (TDD Red phase).
Story: STORY-443
"""
import os

from conftest import (
    SOURCE_TREE_MD,
    ARCH_CONSTRAINTS_MD,
    CODING_STANDARDS_MD,
    PROJECT_ROOT,
)


def _read_source_tree() -> str:
    with open(SOURCE_TREE_MD, encoding="utf-8") as f:
        return f.read()


class TestAC1SourceTreeNewDirectoryNames:
    """Verify new skill directory names appear in source-tree.md."""

    def test_should_list_discovering_requirements_directory_when_updated(self):
        content = _read_source_tree()
        assert "discovering-requirements/" in content, (
            "source-tree.md must list discovering-requirements/ skill directory"
        )

    def test_should_list_brainstorming_directory_when_updated(self):
        content = _read_source_tree()
        assert "brainstorming/" in content, (
            "source-tree.md must list brainstorming/ skill directory"
        )

    def test_should_list_designing_systems_directory_when_updated(self):
        content = _read_source_tree()
        assert "designing-systems/" in content, (
            "source-tree.md must list designing-systems/ skill directory"
        )

    def test_should_list_implementing_stories_directory_when_updated(self):
        content = _read_source_tree()
        assert "implementing-stories/" in content, (
            "source-tree.md must list implementing-stories/ skill directory"
        )


class TestAC1SourceTreeOldNamesAbsent:
    """Verify stale old skill directory names are absent from source-tree.md."""

    def test_should_not_list_devforgeai_ideation_directory_when_updated(self):
        content = _read_source_tree()
        # Allow the word to appear in historical/comment context, but NOT
        # as an active directory path reference (e.g., "devforgeai-ideation/")
        assert "devforgeai-ideation/" not in content, (
            "source-tree.md must not reference devforgeai-ideation/ directory path"
        )

    def test_should_not_list_devforgeai_brainstorming_directory_when_updated(self):
        content = _read_source_tree()
        assert "devforgeai-brainstorming/" not in content, (
            "source-tree.md must not reference devforgeai-brainstorming/ directory path"
        )

    def test_should_not_reference_devforgeai_ideation_anywhere_in_directory_listing(self):
        """The directory tree section must not contain devforgeai-ideation."""
        content = _read_source_tree()
        # Check the directory tree section specifically
        tree_start = content.find("```")
        tree_end = content.find("```", tree_start + 3) if tree_start != -1 else -1
        if tree_start != -1 and tree_end != -1:
            tree_section = content[tree_start:tree_end]
            assert "devforgeai-ideation" not in tree_section, (
                "Directory tree section must not contain devforgeai-ideation"
            )

    def test_should_not_reference_devforgeai_brainstorming_anywhere_in_directory_listing(self):
        """The directory tree section must not contain devforgeai-brainstorming."""
        content = _read_source_tree()
        tree_start = content.find("```")
        tree_end = content.find("```", tree_start + 3) if tree_start != -1 else -1
        if tree_start != -1 and tree_end != -1:
            tree_section = content[tree_start:tree_end]
            assert "devforgeai-brainstorming" not in tree_section, (
                "Directory tree section must not contain devforgeai-brainstorming"
            )


class TestAC1SourceTreeNamingConvention:
    """Verify naming convention section references ADR-017 gerund pattern."""

    def test_should_reference_adr_017_in_naming_convention_when_updated(self):
        content = _read_source_tree()
        assert "ADR-017" in content, (
            "source-tree.md naming convention section must reference ADR-017"
        )

    def test_should_document_gerund_naming_pattern_when_updated(self):
        """The naming convention must describe gerund form, not devforgeai-[phase]."""
        content = _read_source_tree()
        # The current convention should call out gerund form
        assert "gerund" in content.lower(), (
            "source-tree.md must document gerund naming convention per ADR-017"
        )

    def test_should_not_show_devforgeai_phase_as_current_convention_when_updated(self):
        """The Naming Convention section must not present devforgeai-[phase] as current standard.

        The old text 'Naming Convention: devforgeai-[phase]' must be replaced with
        gerund convention. Historical mentions in examples/deprecated sections are OK,
        but the authoritative rule must not state devforgeai-[phase] as current.
        """
        content = _read_source_tree()
        # Look for the Skills naming convention rule block
        if "**Naming Convention**:" in content or "**Pattern**:" in content:
            # Find the Skills naming convention section
            skills_naming_start = content.find("### Skills")
            if skills_naming_start != -1:
                # Extract the Skills naming section (up to next ###)
                next_section = content.find("###", skills_naming_start + 5)
                skills_section = content[skills_naming_start:next_section] if next_section != -1 else content[skills_naming_start:]
                # The authoritative pattern line must NOT say devforgeai-[phase]
                assert "devforgeai-[phase]" not in skills_section or "legacy" in skills_section.lower() or "deprecated" in skills_section.lower(), (
                    "Skills naming convention section must not present devforgeai-[phase] as current convention"
                )

    def test_should_show_gerund_examples_in_naming_convention_when_updated(self):
        """Naming convention examples must use new gerund names."""
        content = _read_source_tree()
        # At least one gerund skill name must appear as a positive example
        gerund_skills = ["implementing-stories", "designing-systems", "discovering-requirements"]
        found_any = any(skill in content for skill in gerund_skills)
        assert found_any, (
            f"source-tree.md naming convention must show gerund examples: {gerund_skills}"
        )
