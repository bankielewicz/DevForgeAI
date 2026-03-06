"""
Test: AC#2 - Subagent Is Under 500 Lines and Does Not Invoke Skills or Commands
Story: STORY-551
Generated: 2026-03-05

Verifies the financial-modeler.md subagent exists, is under 500 lines,
includes "Not financial advice" disclaimer, and contains no Skill() or
slash-command execution directives.
"""

import re


class TestSubagentFileExists:
    """Verify subagent file exists at expected path."""

    def test_should_exist_at_src_claude_agents(self, subagent_file):
        """Subagent file must exist at src/claude/agents/financial-modeler.md."""
        assert subagent_file.exists(), (
            f"Subagent file not found at {subagent_file}. "
            "AC#2 requires financial-modeler.md in src/claude/agents/"
        )


class TestSubagentLineCount:
    """Verify subagent file is under 500 lines."""

    def test_should_have_fewer_than_500_lines(self, subagent_lines):
        """Subagent file must be under 500 lines per tech-stack.md."""
        line_count = len(subagent_lines)
        assert line_count < 500, (
            f"Subagent file has {line_count} lines (limit: 500). "
            "Subagent maximum is 500 lines per tech-stack.md."
        )

    def test_should_have_at_least_10_lines(self, subagent_lines):
        """Subagent file must have meaningful content."""
        assert len(subagent_lines) >= 10, (
            "Subagent file has fewer than 10 lines. "
            "A valid subagent needs YAML frontmatter and system prompt."
        )


class TestDisclaimerPresent:
    """Verify 'Not financial advice' disclaimer is present."""

    def test_should_contain_not_financial_advice_disclaimer(self, subagent_content):
        """Subagent must include 'Not financial advice' disclaimer (BR-001)."""
        assert re.search(r'(?i)not\s+financial\s+advice', subagent_content), (
            "Subagent file missing 'Not financial advice' disclaimer. "
            "BR-001: All financial model outputs must include disclaimer."
        )

    def test_should_mention_consult_professional(self, subagent_content):
        """Disclaimer should reference consulting a professional."""
        assert re.search(
            r'(?i)(consult|seek|contact).*(?:financial|qualified).*professional',
            subagent_content
        ), (
            "Disclaimer should recommend consulting a qualified financial professional."
        )


class TestNoSkillInvocations:
    """Verify subagent contains no Skill() calls (BR-003)."""

    def test_should_not_contain_skill_calls(self, subagent_content):
        """Subagent must not invoke skills via Skill() pattern."""
        skill_patterns = [
            r'Skill\s*\(',
            r'Skill\s*\(\s*command\s*=',
        ]
        for pattern in skill_patterns:
            match = re.search(pattern, subagent_content)
            assert not match, (
                f"Subagent contains Skill() invocation: '{match.group()}'. "
                "BR-003: Subagent must not invoke skills."
            )

    def test_should_not_contain_slash_command_directives(self, subagent_content):
        """Subagent must not contain slash-command execution directives."""
        # Match patterns like "run /command" or "invoke /command" or "execute /command"
        slash_patterns = [
            r'(?i)(?:run|invoke|execute|call)\s+/\w+',
        ]
        for pattern in slash_patterns:
            match = re.search(pattern, subagent_content)
            assert not match, (
                f"Subagent contains slash-command directive: '{match.group()}'. "
                "BR-003: Subagent must not execute commands."
            )


class TestSubagentYAMLFrontmatter:
    """Verify subagent has proper YAML frontmatter."""

    def test_should_start_with_yaml_frontmatter(self, subagent_content):
        """Subagent must have YAML frontmatter per tech-stack.md."""
        assert subagent_content.startswith("---"), (
            "Subagent file must start with YAML frontmatter (---)."
        )

    def test_should_have_name_in_frontmatter(self, subagent_content):
        """Frontmatter must include name field."""
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', subagent_content, re.DOTALL)
        assert frontmatter_match, "Could not parse YAML frontmatter."
        frontmatter = frontmatter_match.group(1)
        assert "name:" in frontmatter.lower(), (
            "YAML frontmatter missing 'name' field."
        )

    def test_should_have_description_in_frontmatter(self, subagent_content):
        """Frontmatter must include description field."""
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', subagent_content, re.DOTALL)
        assert frontmatter_match, "Could not parse YAML frontmatter."
        frontmatter = frontmatter_match.group(1)
        assert "description:" in frontmatter.lower(), (
            "YAML frontmatter missing 'description' field."
        )


class TestEdgeCaseEC004DirectInvocation:
    """EC-004: Subagent invoked directly warns about missing context."""

    def test_should_document_direct_invocation_warning(self, subagent_content):
        """Subagent must warn when invoked outside managing-finances skill."""
        assert re.search(
            r'(?i)(direct\s+invocation|invoked\s+directly|outside.*skill|isolation)',
            subagent_content
        ), (
            "EC-004: Subagent must document behavior when invoked directly "
            "(outside managing-finances skill)."
        )
