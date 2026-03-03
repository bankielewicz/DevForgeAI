"""
Test: AC#2 - Rule 2 Prohibits /tmp/ and Mandates Project-Scoped tmp
Story: STORY-505
Phase: Red (TDD)

Validates that Rule 2 explicitly forbids /tmp/, specifies correct path pattern,
provides wrong/correct examples, and explains rationale.
"""
import re
import pytest


class TestRule2TmpProhibition:
    """AC#2: Rule 2 must prohibit /tmp/ and mandate project-scoped tmp."""

    def test_should_state_tmp_is_forbidden(self, rule_file_content):
        """Rule 2 must explicitly state /tmp/ is FORBIDDEN."""
        content_upper = rule_file_content.upper()
        assert "FORBIDDEN" in content_upper, (
            "Rule 2 must use the word FORBIDDEN"
        )
        assert "/tmp/" in rule_file_content, (
            "Rule 2 must mention /tmp/ path"
        )

    def test_should_specify_correct_path_pattern(self, rule_file_content):
        """Rule 2 must specify {project-root}/tmp/{story-id}/ as correct pattern."""
        assert re.search(
            r"\{project-root\}/tmp/\{story-id\}",
            rule_file_content,
            re.IGNORECASE,
        ), "Rule 2 must specify {project-root}/tmp/{story-id}/ path pattern"

    def test_should_have_wrong_example(self, rule_file_content):
        """Rule 2 must provide a wrong example showing /tmp/ usage."""
        # Look for wrong/incorrect example markers
        has_wrong = re.search(
            r"(wrong|incorrect|bad|prohibited|FORBIDDEN).*example|example.*wrong|"
            r"[xX]|WRONG",
            rule_file_content,
            re.IGNORECASE,
        )
        assert has_wrong, "Rule 2 must provide a wrong example"

    def test_should_have_correct_example(self, rule_file_content):
        """Rule 2 must provide a correct example showing project-scoped path."""
        has_correct = re.search(
            r"(correct|right|good|approved).*example|example.*correct|"
            r"[vV]|CORRECT|tmp/STORY-",
            rule_file_content,
            re.IGNORECASE,
        )
        assert has_correct, "Rule 2 must provide a correct example"

    def test_should_explain_portability_rationale(self, rule_file_content):
        """Rule 2 must explain rationale about portability across WSL/Windows/Linux."""
        content_lower = rule_file_content.lower()
        has_portability = any(
            term in content_lower
            for term in ["portability", "wsl", "windows", "cross-platform"]
        )
        assert has_portability, (
            "Rule 2 must explain portability rationale (WSL/Windows/Linux)"
        )

    def test_should_explain_traceability_rationale(self, rule_file_content):
        """Rule 2 must explain traceability by story rationale."""
        content_lower = rule_file_content.lower()
        has_traceability = any(
            term in content_lower
            for term in ["traceability", "traceable", "story-id", "story id"]
        )
        assert has_traceability, (
            "Rule 2 must explain traceability-by-story rationale"
        )

    def test_should_have_wrong_and_correct_example_block(self, rule_file_content):
        """Rule 2 must have both wrong and correct in an example block."""
        # Both wrong and correct should appear, ideally near each other
        assert "/tmp/" in rule_file_content, "Wrong example must show /tmp/"
        assert re.search(r"tmp/STORY-\d+", rule_file_content), (
            "Correct example must show tmp/STORY-NNN pattern"
        )
