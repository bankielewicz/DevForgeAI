"""AC#6: STORY-431 AC#2 Trigger Phrases Folded."""
import os

import pytest

from conftest import SRC_NEW

SKILL_PATH = os.path.join(SRC_NEW, "SKILL.md")


class TestAC6TriggerPhrases:
    """AC#6: Trigger phrases integrated into SKILL.md."""

    @pytest.fixture(autouse=True)
    def load_skill(self):
        if os.path.isfile(SKILL_PATH):
            with open(SKILL_PATH) as f:
                self.content = f.read().lower()
        else:
            self.content = ""

    def test_should_contain_discovery_phrase(self):
        assert "discovery" in self.content

    def test_should_contain_elicitation_phrase(self):
        assert "elicitation" in self.content

    def test_should_contain_requirements_phrase(self):
        assert "requirements" in self.content

    def test_should_not_contain_architect_trigger_phrases(self):
        for phrase in ["complexity assessment", "feasibility analysis"]:
            assert phrase not in self.content, f"Architect trigger phrase '{phrase}' should be removed"
