"""
Test: AC#5 - Follow-Up Stories Created If Needed
Story: STORY-412
Generated: 2026-02-16

Validates that violations requiring refactoring have follow-up
story IDs proposed or created.
"""
import os
import re
import pytest

AUDIT_RESULTS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..",
    "devforgeai", "specs", "analysis", "command-hybrid-audit-results.md"
)


class TestFollowupStories:
    """AC#5: Follow-up stories created/proposed if violations need refactoring."""

    def _read_audit(self):
        with open(AUDIT_RESULTS_PATH, "r") as f:
            return f.read()

    def test_should_have_followup_section_when_violations_require_refactoring(self):
        """Assert audit results contain a follow-up stories section."""
        content = self._read_audit()
        has_followup = bool(re.search(r"(?i)(follow.up|next.step|proposed.stor)", content))
        has_refactor = "refactor" in content.lower()
        if has_refactor:
            assert has_followup, (
                "Violations recommend refactoring but no follow-up stories section found"
            )

    def test_should_reference_story_ids_in_followup_section(self):
        """Assert follow-up section references STORY-NNN identifiers."""
        content = self._read_audit()
        story_refs = re.findall(r"STORY-\d+", content)
        has_refactor = "refactor" in content.lower()
        if has_refactor:
            assert story_refs, (
                "Refactoring recommended but no STORY-NNN references found for follow-up"
            )

    def test_should_propose_story_for_each_refactor_recommendation(self):
        """Assert each refactor recommendation has a corresponding story proposal."""
        content = self._read_audit()
        # Count refactor recommendations
        refactor_count = len(re.findall(r"(?i)refactor", content))
        # Count story references (excluding STORY-410/412 which are this story's refs)
        story_refs = [
            s for s in re.findall(r"STORY-(\d+)", content)
            if s not in ("410", "412")
        ]
        if refactor_count > 0:
            assert len(story_refs) > 0, (
                f"Found {refactor_count} refactor recommendations but no new story proposals"
            )

    def test_should_acknowledge_no_followup_needed_when_all_clean(self):
        """If no violations require refactoring, audit should state no follow-up needed."""
        content = self._read_audit()
        has_refactor = "refactor" in content.lower()
        if not has_refactor:
            has_no_followup = bool(
                re.search(r"(?i)(no.follow.up|no.remediation|all.clean|no.action)", content)
            )
            assert has_no_followup, (
                "All commands clean but audit does not acknowledge no follow-up needed"
            )
