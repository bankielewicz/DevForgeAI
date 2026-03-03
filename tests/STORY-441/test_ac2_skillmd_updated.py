"""AC#2: SKILL.md Name and Description Updated."""
import os
import re

import pytest

from conftest import SRC_NEW

SKILL_PATH = os.path.join(SRC_NEW, "SKILL.md")


class TestAC2SkillmdUpdated:
    """AC#2: SKILL.md reflects new name and PM-focused scope."""

    @pytest.fixture(autouse=True)
    def load_skill(self):
        if os.path.isfile(SKILL_PATH):
            with open(SKILL_PATH) as f:
                self.content = f.read()
        else:
            self.content = ""

    def test_should_have_name_discovering_requirements_in_frontmatter(self):
        assert re.search(r"^name:\s*discovering-requirements\s*$", self.content, re.MULTILINE), \
            "SKILL.md frontmatter must have name: discovering-requirements"

    def test_should_not_have_old_name_in_frontmatter(self):
        assert "devforgeai-ideation" not in self.content, "SKILL.md must not contain devforgeai-ideation"

    def test_should_not_reference_architect_phases_in_description(self):
        for phrase in ["complexity assessment", "epic decomposition", "feasibility analysis"]:
            assert phrase.lower() not in self.content.lower(), \
                f"SKILL.md should not reference removed phase: {phrase}"
