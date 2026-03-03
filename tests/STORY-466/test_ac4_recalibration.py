"""
Test: AC#4 - Recalibration Support
Story: STORY-466
Phase: TDD Red (tests must FAIL until implementation is complete)

Verifies:
- assess-me.md supports a --recalibrate argument (documented in argument-hint)
- Command body describes the recalibrate flow
- Recalibrate flow overwrites the profile (user-profile.yaml referenced)
- Recalibrate flow preserves coaching session history (session log not overwritten)
- Business rule BR-002: only user-profile.yaml is modified during recalibration
"""

import os
import re

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

ASSESS_ME_PATH = os.path.join(
    PROJECT_ROOT, "src", "claude", "commands", "assess-me.md"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _parse_yaml_frontmatter(content: str) -> dict:
    """Extract key-value pairs from YAML frontmatter delimited by '---'."""
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
# --recalibrate argument tests
# ---------------------------------------------------------------------------


class TestRecalibrateArgument:
    """AC#4: assess-me.md must document the --recalibrate argument."""

    def test_assess_me_exists(self):
        """assess-me.md must exist before recalibration tests can run."""
        assert os.path.isfile(ASSESS_ME_PATH), (
            f"assess-me.md not found at: {ASSESS_ME_PATH}"
        )

    def test_argument_hint_mentions_recalibrate(self):
        """The 'argument-hint' frontmatter field must include '--recalibrate'."""
        content = _read_file(ASSESS_ME_PATH)
        frontmatter = _parse_yaml_frontmatter(content)
        argument_hint = frontmatter.get("argument-hint", "")
        assert "--recalibrate" in argument_hint, (
            f"assess-me.md 'argument-hint' frontmatter does not mention '--recalibrate'. "
            f"Found: '{argument_hint}'"
        )

    def test_command_body_handles_recalibrate_argument(self):
        """Command body must have a section or conditional handling --recalibrate."""
        content = _read_file(ASSESS_ME_PATH)
        assert re.search(r"--recalibrate", content), (
            "assess-me.md body does not handle '--recalibrate' argument"
        )

    def test_recalibrate_described_as_flow_or_mode(self):
        """Command must describe recalibrate as a distinct flow or mode."""
        content = _read_file(ASSESS_ME_PATH)
        # Accept 'recalibrate', 'recalibration', or 'recalibrating' in body
        assert re.search(r"recalibrat(e|ion|ing)", content, re.IGNORECASE), (
            "assess-me.md does not describe a recalibration flow"
        )


# ---------------------------------------------------------------------------
# Profile overwrite tests
# ---------------------------------------------------------------------------


class TestRecalibrateOverwritesProfile:
    """AC#4 + BR-002: Recalibration must overwrite user-profile.yaml."""

    def test_recalibrate_references_user_profile_yaml(self):
        """Recalibrate flow must reference 'user-profile.yaml' as the overwrite target."""
        content = _read_file(ASSESS_ME_PATH)
        assert "user-profile.yaml" in content, (
            "assess-me.md does not reference 'user-profile.yaml' "
            "as the recalibration overwrite target"
        )

    def test_recalibrate_mentions_overwrite_semantics(self):
        """Command must indicate the profile is overwritten/replaced during recalibration."""
        content = _read_file(ASSESS_ME_PATH)
        assert re.search(
            r"overwrit(e|es|ten)|replac(e|es|ing)\s+.*profile", content, re.IGNORECASE
        ), (
            "assess-me.md does not describe overwrite semantics for recalibration. "
            "Must state that the profile is overwritten."
        )


# ---------------------------------------------------------------------------
# Session history preservation tests
# ---------------------------------------------------------------------------


class TestRecalibratePreservesSessionHistory:
    """AC#4 + BR-002: Recalibration must preserve coaching session history."""

    def test_recalibrate_mentions_history_preservation(self):
        """Command must state that coaching session history is preserved during recalibration."""
        content = _read_file(ASSESS_ME_PATH)
        assert re.search(
            r"preserv(e|es|ing).{0,60}(history|session|log)",
            content,
            re.IGNORECASE | re.DOTALL,
        ), (
            "assess-me.md does not mention preserving coaching session history "
            "during --recalibrate flow. BR-002 requires this explicitly."
        )

    def test_recalibrate_does_not_overwrite_session_log(self):
        """Command must clarify that only user-profile.yaml is modified, not the session log."""
        content = _read_file(ASSESS_ME_PATH)
        # Must NOT state that session log / coaching history is overwritten/deleted
        # This checks for dangerous patterns near 'recalibrate'
        dangerous_patterns = [
            r"recalibrat\w+.{0,200}(delete|remove|overwrite|wipe).{0,80}(session|history|log)",
            r"(delete|remove|overwrite|wipe).{0,80}(session|history|log).{0,200}recalibrat",
        ]
        for pattern in dangerous_patterns:
            assert not re.search(pattern, content, re.IGNORECASE | re.DOTALL), (
                "assess-me.md appears to indicate session history is deleted during "
                "recalibration. BR-002 forbids this."
            )

    def test_command_only_modifies_profile_during_recalibration(self):
        """Recalibration section must indicate only the profile file is affected."""
        content = _read_file(ASSESS_ME_PATH)
        # The command should clarify scope: profile only
        assert re.search(
            r"(only|profile\s+only|profile\s+file\s+only|user.profile\.yaml\s+only)",
            content,
            re.IGNORECASE,
        ), (
            "assess-me.md does not clarify that only user-profile.yaml is modified "
            "during recalibration (BR-002 requirement)"
        )
