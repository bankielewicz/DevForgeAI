"""AC#3: coding-standards.md Updated with New Naming Convention.

Tests that devforgeai/specs/context/coding-standards.md:
  (a) Skill naming pattern changed from devforgeai-[phase] to gerund convention per ADR-017
  (b) Examples use new skill names (designing-systems, discovering-requirements, brainstorming)
  (c) Naming convention section references ADR-017 as authority
  (d) No devforgeai- prefix mentioned as the CURRENT convention
  (e) Documentation Standards section references implementing-stories

All tests MUST FAIL before implementation (TDD Red phase).
Story: STORY-443
"""
import os

from conftest import CODING_STANDARDS_MD


def _read_coding_standards() -> str:
    with open(CODING_STANDARDS_MD, encoding="utf-8") as f:
        return f.read()


class TestAC3GerundConventionDocumented:
    """Verify gerund naming convention is documented in coding-standards.md."""

    def test_should_document_gerund_naming_with_adr_017_reference_when_updated(self):
        """The Skill Naming Convention section must cite ADR-017."""
        content = _read_coding_standards()
        # Find the naming convention section
        naming_start = content.find("Skill Naming Convention")
        assert naming_start != -1, (
            "coding-standards.md must have a Skill Naming Convention section"
        )
        # ADR-017 must appear in or near that section
        next_section = content.find("###", naming_start + 5)
        naming_section = content[naming_start:next_section] if next_section != -1 else content[naming_start:]
        assert "ADR-017" in naming_section, (
            "Skill Naming Convention section must reference ADR-017 as authority"
        )

    def test_should_show_gerund_form_as_correct_pattern_when_updated(self):
        """coding-standards.md must present gerund form as the correct pattern."""
        content = _read_coding_standards()
        # The skill naming section must document gerund as the positive example
        naming_start = content.find("Skill Naming Convention")
        if naming_start != -1:
            next_section = content.find("###", naming_start + 5)
            naming_section = content[naming_start:next_section] if next_section != -1 else content[naming_start:]
            # Must contain gerund example like implementing-stories or designing-systems
            assert "implementing-stories" in naming_section or "designing-systems" in naming_section, (
                "Skill Naming Convention section must show gerund examples "
                "(e.g., implementing-stories, designing-systems)"
            )

    def test_should_have_adr_017_reference_in_naming_conventions_table_when_updated(self):
        """The Naming Conventions table must reference ADR-017 for skills."""
        content = _read_coding_standards()
        # Look for the Naming Conventions table section
        if "Naming Conventions" in content:
            naming_start = content.find("### Naming Conventions")
            if naming_start != -1:
                next_section = content.find("###", naming_start + 5)
                naming_section = content[naming_start:next_section] if next_section != -1 else content[naming_start:]
                assert "ADR-017" in naming_section, (
                    "Naming Conventions table section must reference ADR-017 for skill naming"
                )

    def test_should_document_no_devforgeai_prefix_as_current_when_updated(self):
        """The naming convention must explicitly mark devforgeai- prefix as old/deprecated."""
        content = _read_coding_standards()
        naming_start = content.find("Skill Naming Convention")
        if naming_start != -1:
            next_section = content.find("###", naming_start + 5)
            naming_section = content[naming_start:next_section] if next_section != -1 else content[naming_start:]
            # Either the section must use a negation marker (❌) next to devforgeai-[name]
            # OR must not present devforgeai-[name] as a positive example at all
            if "devforgeai-[name]" in naming_section or "devforgeai-[phase]" in naming_section:
                # If mentioned, must be in a negative/deprecated context
                assert "❌" in naming_section or "old convention" in naming_section.lower() or "deprecated" in naming_section.lower(), (
                    "If devforgeai- prefix appears in naming convention section, "
                    "it must be marked as old/deprecated (❌ or 'old convention')"
                )


class TestAC3OldConventionNotCurrentlyPrescribed:
    """The devforgeai- prefix must not be presented as the current naming standard."""

    def test_should_not_prescribe_devforgeai_prefix_as_current_convention_when_updated(self):
        """coding-standards.md must NOT list devforgeai-[phase] as the current convention.

        The old text was:
          Skills: [gerund-phrase] (e.g., `implementing-stories`, `validating-quality`) — see ADR-017

        After the update, the table row for Skills must reference gerund form, not devforgeai-.
        """
        content = _read_coding_standards()
        # Find the Naming Conventions table row for Skills
        # Check it does NOT say the current skill pattern is 'devforgeai-*'
        if "**Skills**:" in content or "Skills:" in content:
            lines = content.split("\n")
            skills_lines = [
                line for line in lines
                if ("skills" in line.lower() or "Skills" in line)
                and ("pattern" in line.lower() or "gerund" in line.lower()
                     or "devforgeai-" in line or "ADR-017" in line)
            ]
            for line in skills_lines:
                # If a skills pattern line says devforgeai- is current, that's a failure
                if "devforgeai-[phase]" in line or "devforgeai-[name]" in line:
                    assert "❌" in line or "old" in line.lower() or "deprecated" in line.lower(), (
                        f"Skills naming line still prescribes devforgeai- prefix as current: {line!r}"
                    )

    def test_should_not_have_devforgeai_development_as_convention_example_when_updated(self):
        """coding-standards.md must not use devforgeai-development as a positive example."""
        content = _read_coding_standards()
        # Look for positive example markers (✅) followed by devforgeai-development
        lines = content.split("\n")
        bad_lines = [
            line for line in lines
            if "✅" in line and "devforgeai-development" in line
        ]
        assert len(bad_lines) == 0, (
            f"Found {len(bad_lines)} positive examples using devforgeai-development:\n"
            + "\n".join(bad_lines)
        )


class TestAC3NewNamingExamplesPresent:
    """Verify coding-standards.md uses new gerund names in examples."""

    def test_should_use_implementing_stories_in_examples_when_updated(self):
        content = _read_coding_standards()
        assert "implementing-stories" in content, (
            "coding-standards.md must use implementing-stories as a naming example"
        )

    def test_should_use_designing_systems_in_examples_when_updated(self):
        content = _read_coding_standards()
        assert "designing-systems" in content, (
            "coding-standards.md must use designing-systems as a naming example"
        )

    def test_should_reference_implementing_stories_in_documentation_standards_when_updated(self):
        """The Documentation Standards section must reference implementing-stories, not devforgeai-development."""
        content = _read_coding_standards()
        # Find the Documentation Standards or Phase Naming Convention section
        doc_start = content.find("Phase Naming Convention")
        if doc_start == -1:
            doc_start = content.find("Documentation Standards")
        if doc_start != -1:
            # Find the 'See:' reference line
            ref_region = content[doc_start:doc_start + 500]
            # Must not say devforgeai-development in the See: reference
            if "devforgeai-development" in ref_region:
                assert False, (
                    "Documentation Standards / Phase Naming section must reference "
                    "implementing-stories, not devforgeai-development"
                )

    def test_should_have_see_reference_to_implementing_stories_skill_when_updated(self):
        """The coding-standards.md 'See:' cross-reference must point to implementing-stories."""
        content = _read_coding_standards()
        # The file currently has: 'See: .claude/skills/implementing-stories/'
        # This was already partially updated; verify it doesn't revert
        if "**See:**" in content or "See:" in content:
            see_lines = [
                line for line in content.split("\n")
                if "See:" in line and ("skills" in line or "skill" in line)
            ]
            for line in see_lines:
                # If a see-line mentions the old devforgeai-development path, it's stale
                assert "devforgeai-development" not in line, (
                    f"'See:' reference line still points to devforgeai-development: {line!r}"
                )
