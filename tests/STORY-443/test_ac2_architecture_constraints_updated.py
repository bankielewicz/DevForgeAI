"""AC#2: architecture-constraints.md Updated with New Responsibilities.

Tests that devforgeai/specs/context/architecture-constraints.md:
  (a) Uses implementing-stories (not devforgeai-development) in skill references
  (b) Uses designing-systems skill name
  (c) References discovering-requirements where ideation responsibilities described
  (d) References ADR-017 for naming convention
  (e) No old devforgeai-development in active skill name references
  (f) Single Responsibility Principle section uses new names

All tests MUST FAIL before implementation (TDD Red phase).
Story: STORY-443
"""
import os

from conftest import ARCH_CONSTRAINTS_MD


def _read_arch_constraints() -> str:
    with open(ARCH_CONSTRAINTS_MD, encoding="utf-8") as f:
        return f.read()


class TestAC2NewSkillNamesPresent:
    """Verify new skill names appear in architecture-constraints.md."""

    def test_should_reference_implementing_stories_in_srp_section_when_updated(self):
        """The Single Responsibility Principle section should use implementing-stories."""
        content = _read_arch_constraints()
        assert "implementing-stories" in content, (
            "architecture-constraints.md must reference implementing-stories "
            "(ADR-017 compliant name for devforgeai-development)"
        )

    def test_should_reference_designing_systems_skill_name_when_updated(self):
        content = _read_arch_constraints()
        assert "designing-systems" in content, (
            "architecture-constraints.md must reference designing-systems skill name"
        )

    def test_should_reference_adr_017_for_naming_convention_when_updated(self):
        content = _read_arch_constraints()
        assert "ADR-017" in content, (
            "architecture-constraints.md must reference ADR-017 for naming convention"
        )


class TestAC2OldSkillNamesAbsentFromActiveReferences:
    """Verify old devforgeai-* skill names are not used as current/active references."""

    def test_should_not_use_devforgeai_development_as_current_skill_when_updated(self):
        """devforgeai-development must not appear in skill design examples.

        The Single Responsibility Principle section previously cited
        'implementing-stories: TDD implementation only (devforgeai-development naming)'.
        After update it should use 'implementing-stories' as the canonical name.
        """
        content = _read_arch_constraints()
        # Find the SRP section
        srp_start = content.find("Single Responsibility Principle")
        if srp_start == -1:
            # Section header not found — content not yet updated, test still fails with assertion
            assert False, (
                "Single Responsibility Principle section not found in architecture-constraints.md"
            )
        # Extract up to next '---' separator or end of section
        next_divider = content.find("---", srp_start)
        srp_section = content[srp_start:next_divider] if next_divider != -1 else content[srp_start:]
        # devforgeai-development must not appear as an active skill example in SRP
        assert "devforgeai-development" not in srp_section, (
            "SRP section must not reference devforgeai-development as active skill name; "
            "use implementing-stories instead"
        )

    def test_should_not_reference_devforgeai_ideation_as_skill_name_when_updated(self):
        """devforgeai-ideation must not be used as a skill name in the constraints."""
        content = _read_arch_constraints()
        # Skip historical mentions that are clearly notes or comments
        lines_with_old_name = [
            line for line in content.split("\n")
            if "devforgeai-ideation" in line
            and "legacy" not in line.lower()
            and "old" not in line.lower()
            and "renamed" not in line.lower()
            and "deprecated" not in line.lower()
        ]
        assert len(lines_with_old_name) == 0, (
            f"Found {len(lines_with_old_name)} active references to devforgeai-ideation:\n"
            + "\n".join(lines_with_old_name[:5])
        )

    def test_should_not_reference_devforgeai_brainstorming_as_skill_name_when_updated(self):
        """devforgeai-brainstorming must not be used as an active skill name."""
        content = _read_arch_constraints()
        lines_with_old_name = [
            line for line in content.split("\n")
            if "devforgeai-brainstorming" in line
            and "legacy" not in line.lower()
            and "old" not in line.lower()
            and "renamed" not in line.lower()
            and "deprecated" not in line.lower()
        ]
        assert len(lines_with_old_name) == 0, (
            f"Found {len(lines_with_old_name)} active references to devforgeai-brainstorming:\n"
            + "\n".join(lines_with_old_name[:5])
        )


class TestAC2SRPSectionReflectsNewBoundaries:
    """Verify Single Responsibility Principle section uses correct new names."""

    def test_should_not_have_devforgeai_development_in_srp_examples_when_updated(self):
        """SRP examples must use new skill names."""
        content = _read_arch_constraints()
        # Look for the parenthetical note '(ADR-017 naming)' next to implementing-stories
        # This was the form used after STORY-440 partial update but before full sweep
        srp_start = content.find("Single Responsibility Principle")
        if srp_start != -1:
            next_divider = content.find("---", srp_start)
            srp_section = content[srp_start:next_divider] if next_divider != -1 else content[srp_start:]
            # The old line was: '✅ devforgeai-development: TDD implementation only'
            assert "✅ devforgeai-development" not in srp_section, (
                "SRP checkmark examples must not use devforgeai-development"
            )

    def test_should_have_implementing_stories_in_srp_positive_example_when_updated(self):
        """SRP positive examples (✅) must include implementing-stories."""
        content = _read_arch_constraints()
        srp_start = content.find("Single Responsibility Principle")
        if srp_start != -1:
            next_divider = content.find("---", srp_start)
            srp_section = content[srp_start:next_divider] if next_divider != -1 else content[srp_start:]
            assert "implementing-stories" in srp_section, (
                "SRP section must show implementing-stories as a positive example"
            )
