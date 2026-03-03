"""Test AC#5: Safety Disclaimers.

Story: STORY-465
Validates that SKILL.md contains appropriate safety disclaimers and
does NOT use diagnostic language outside of disclaimer context.
"""
import re
import pytest
from pathlib import Path


class TestDisclaimerPresent:
    """Tests for safety disclaimer existence."""

    def test_should_contain_no_diagnosis_disclaimer(self, skill_file):
        """SKILL.md must explicitly state it does NOT diagnose mental health conditions."""
        content = skill_file.read_text(encoding="utf-8").lower()
        # Must contain a negation pattern about diagnosing
        has_never_diagnose = "never diagnose" in content or "never diagnoses" in content
        has_not_diagnose = "not diagnose" in content or "does not diagnose" in content
        has_no_diagnosis = "not a diagnosis" in content or "not a clinical" in content
        assert has_never_diagnose or has_not_diagnose or has_no_diagnosis, (
            "SKILL.md must contain an explicit disclaimer about NOT diagnosing "
            "mental health conditions (e.g., 'NEVER diagnoses', 'does not diagnose')."
        )

    def test_should_frame_as_self_reported(self, skill_file):
        """Content must frame assessment as self-reported preferences, not clinical."""
        content = skill_file.read_text(encoding="utf-8").lower()
        has_self_reported = "self-reported" in content or "self reported" in content
        has_preferences = "preferences" in content
        assert has_self_reported or has_preferences, (
            "SKILL.md must frame questions as 'self-reported' or 'preferences', "
            "not clinical assessments."
        )


class TestNoDiagnosticLanguage:
    """Tests that diagnostic language is used only in disclaimer/negation context."""

    DIAGNOSTIC_TERMS = ["diagnose", "diagnosis", "disorder"]

    def test_should_not_use_diagnostic_language_affirmatively(self, skill_file):
        """Diagnostic words must only appear in negation/disclaimer context.

        Words like 'diagnose', 'diagnosis', 'disorder' must only appear
        preceded by negation words (never, not, no, does not) or in
        explicit disclaimer sections.
        """
        content = skill_file.read_text(encoding="utf-8")
        lines = content.splitlines()

        violations = []
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            for term in self.DIAGNOSTIC_TERMS:
                if term in line_lower:
                    # Check if the line contains negation context
                    negation_patterns = [
                        "never", "not", "no ", "does not", "do not",
                        "will not", "cannot", "disclaimer", "important",
                        "warning", "note:"
                    ]
                    has_negation = any(neg in line_lower for neg in negation_patterns)
                    if not has_negation:
                        violations.append(
                            f"Line {line_num}: '{term}' used without "
                            f"negation context: {line.strip()[:80]}"
                        )

        assert len(violations) == 0, (
            f"Found {len(violations)} uses of diagnostic language without "
            f"negation/disclaimer context:\n" +
            "\n".join(violations)
        )
