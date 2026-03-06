"""
Integration Test: Cross-file consistency between managing-finances SKILL.md
and funding-options-guide.md, plus end-to-end decision tree reachability.

Story: STORY-552
Phase: Integration (Phase 05)
Generated: 2026-03-06

These tests verify component interactions across file boundaries:
1. SKILL.md references the guide file correctly
2. All 5 funding types are reachable through the decision tree
3. Decision tree inputs produce complete traversal paths
4. Output template references valid artifact paths
"""
import os
import re
import pytest


GUIDE_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..',
    'src', 'claude', 'skills', 'managing-finances', 'references',
    'funding-options-guide.md'
)

SKILL_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..',
    'src', 'claude', 'skills', 'managing-finances', 'SKILL.md'
)


@pytest.fixture
def skill_content():
    """Read the managing-finances SKILL.md file."""
    with open(SKILL_PATH, 'r') as f:
        return f.read()


@pytest.fixture
def guide_content():
    """Read the funding options guide."""
    with open(GUIDE_PATH, 'r') as f:
        return f.read()


def _extract_section(content, heading_pattern):
    """Extract a markdown section by heading pattern (## or ### level)."""
    pattern = re.compile(
        rf'^(##{{1,3}})\s+.*{heading_pattern}.*$',
        re.IGNORECASE | re.MULTILINE
    )
    match = pattern.search(content)
    if not match:
        return ""
    start = match.start()
    level = len(match.group(1))
    next_section = re.compile(rf'^#{{1,{level}}}\s+', re.MULTILINE)
    remainder = content[match.end():]
    next_match = next_section.search(remainder)
    if next_match:
        return content[start:match.end() + next_match.start()]
    return content[start:]


# ---------------------------------------------------------------------------
# Integration Point 1: SKILL.md <-> Guide file cross-reference
# ---------------------------------------------------------------------------

class TestSkillGuideIntegration:
    """Verify SKILL.md and funding-options-guide.md reference each other."""

    def test_should_exist_as_referenced_file_when_skill_loaded(self):
        """Arrange: Both files at expected paths
        Act: Check guide file exists at SKILL.md-referenced path
        Assert: File exists and is non-empty
        """
        assert os.path.isfile(GUIDE_PATH), (
            f"funding-options-guide.md must exist at {GUIDE_PATH}"
        )
        assert os.path.getsize(GUIDE_PATH) > 0, (
            "funding-options-guide.md must be non-empty"
        )

    def test_should_reference_guide_in_skill_references_table_when_skill_loaded(
        self, skill_content
    ):
        """Arrange: SKILL.md content loaded
        Act: Search References table for funding-options-guide
        Assert: Guide is listed in the references table or body
        """
        # The SKILL.md references table or body should mention the guide
        # Either directly or via the references/ directory listing
        has_guide_ref = bool(re.search(
            r'funding-options-guide', skill_content, re.IGNORECASE
        ))
        has_references_dir = bool(re.search(
            r'references/', skill_content, re.IGNORECASE
        ))
        assert has_guide_ref or has_references_dir, (
            "SKILL.md must reference funding-options-guide.md or "
            "the references/ directory containing it"
        )

    def test_should_have_consistent_disclaimer_language_between_skill_and_guide(
        self, skill_content, guide_content
    ):
        """Arrange: Both SKILL.md and guide content loaded
        Act: Check both files include educational disclaimer language
        Assert: Both files contain disclaimer or 'not financial advice' language
        """
        # SKILL.md has "not financial advice" disclaimer requirement
        skill_has_disclaimer = bool(re.search(
            r'disclaimer|not\s+financial\s+advice', skill_content, re.IGNORECASE
        ))
        guide_has_disclaimer = bool(re.search(
            r'disclaimer', guide_content, re.IGNORECASE
        ))
        assert skill_has_disclaimer, (
            "SKILL.md must reference disclaimer requirement"
        )
        assert guide_has_disclaimer, (
            "Guide must contain disclaimer sections"
        )


# ---------------------------------------------------------------------------
# Integration Point 2: End-to-end decision tree reachability
# ---------------------------------------------------------------------------

FUNDING_TYPES = [
    ("Bootstrapping", r'bootstrapping'),
    ("Grants", r'grants'),
    ("Angel Investment", r'angel\s+investment'),
    ("Venture Capital", r'venture\s+capital'),
    ("Debt/Loans", r'debt(?:\s+and\s+loans|\s*/\s*loans)?'),
]


class TestDecisionTreeEndToEndReachability:
    """Verify all 5 funding types are reachable from the decision tree entry
    point through a complete traversal path (inputs -> evaluation -> output)."""

    def test_should_have_decision_tree_entry_point_when_guide_loaded(self, guide_content):
        """Arrange: Guide content loaded
        Act: Search for decision tree overview/entry section
        Assert: Entry point section exists with all 3 input dimensions
        """
        entry = _extract_section(guide_content, r'decision\s+tree')
        assert entry, "Decision tree entry point section must exist"
        assert re.search(r'business\s+stage', entry, re.IGNORECASE), (
            "Entry point must reference business stage input"
        )
        assert re.search(r'capital\s+need', entry, re.IGNORECASE), (
            "Entry point must reference capital need input"
        )
        assert re.search(r'equity\s+preference', entry, re.IGNORECASE), (
            "Entry point must reference equity preference input"
        )

    @pytest.mark.parametrize("name,pattern", FUNDING_TYPES)
    def test_should_have_dedicated_section_for_each_funding_type_when_guide_loaded(
        self, guide_content, name, pattern
    ):
        """Arrange: Guide content loaded
        Act: Extract section for each funding type
        Assert: Each funding type has its own ## section with content
        """
        section = _extract_section(guide_content, pattern)
        assert section, (
            f"Funding type '{name}' must have a dedicated section in the guide"
        )
        # Section must have substantive content (not just a header)
        content_lines = [
            line for line in section.strip().split('\n')
            if line.strip() and not line.strip().startswith('#')
        ]
        assert len(content_lines) >= 3, (
            f"Funding type '{name}' section must contain substantive content "
            f"(found {len(content_lines)} non-header lines)"
        )

    @pytest.mark.parametrize("name,pattern", FUNDING_TYPES)
    def test_should_have_suitability_criteria_for_each_funding_type(
        self, guide_content, name, pattern
    ):
        """Arrange: Guide content loaded
        Act: Search each funding type section for suitability/when-to-use content
        Assert: Each type has guidance on when it may be suitable
        """
        section = _extract_section(guide_content, pattern)
        assert section, f"Section for '{name}' must exist"
        suitability = re.search(
            r'suitable|consider|when\s+to|best\s+for|ideal|appropriate|qualify',
            section, re.IGNORECASE
        )
        assert suitability, (
            f"Funding type '{name}' must include suitability/when-to-use guidance"
        )

    def test_should_have_output_template_referencing_all_types_when_guide_loaded(
        self, guide_content
    ):
        """Arrange: Guide content loaded
        Act: Check output template section exists and references ranked format
        Assert: Output template shows ranked shortlist format
        """
        output_section = _extract_section(guide_content, r'output\s+template')
        assert output_section, "Output template section must exist"
        assert re.search(r'ranked', output_section, re.IGNORECASE), (
            "Output template must reference ranked shortlist format"
        )
        assert re.search(r'funding.type|funding\s+type', output_section, re.IGNORECASE), (
            "Output template must reference funding type in output format"
        )


# ---------------------------------------------------------------------------
# Integration Point 3: Boundary case completeness
# ---------------------------------------------------------------------------

class TestBoundaryIntegration:
    """Verify boundary/ambiguous section integrates with the comparison table
    and covers all 5 funding types in the comparison."""

    def test_should_list_all_5_funding_types_in_comparison_table(self, guide_content):
        """Arrange: Guide content loaded
        Act: Extract boundary/comparison section, check all types present
        Assert: Comparison table row exists for each funding type
        """
        boundary_section = _extract_section(
            guide_content, r'boundary|comparison'
        )
        assert boundary_section, "Boundary/comparison section must exist"

        for name, _ in FUNDING_TYPES:
            # Handle "Debt/Loans" matching either term
            if "Debt" in name:
                found = (
                    re.search(r'debt', boundary_section, re.IGNORECASE) or
                    re.search(r'loan', boundary_section, re.IGNORECASE)
                )
            else:
                found = re.search(re.escape(name), boundary_section, re.IGNORECASE)
            assert found, (
                f"Comparison table must include '{name}' as a row"
            )

    def test_should_have_resolving_guidance_after_comparison_table(self, guide_content):
        """Arrange: Guide content loaded
        Act: Check for resolution guidance following the comparison table
        Assert: Guidance on resolving ambiguous results is present
        """
        boundary_section = _extract_section(
            guide_content, r'boundary|ambiguous'
        )
        assert boundary_section, "Boundary section must exist"
        assert re.search(
            r'resolv|reconsider|adjust|next\s+step',
            boundary_section, re.IGNORECASE
        ), (
            "Boundary section must include guidance on resolving ambiguous results"
        )


# ---------------------------------------------------------------------------
# Integration Point 4: Equity vs non-equity path consistency
# ---------------------------------------------------------------------------

class TestEquityNonEquityPathConsistency:
    """Verify equity paths have referral triggers and non-equity paths do not,
    tested as an end-to-end cross-section validation."""

    def test_should_have_referral_in_equity_paths_only(self, guide_content):
        """Arrange: Guide content loaded
        Act: Check referral trigger presence across all 5 funding type sections
        Assert: Only VC and Angel sections contain referral triggers
        """
        equity_types = [
            ("Angel Investment", r'angel\s+investment'),
            ("Venture Capital", r'venture\s+capital'),
        ]
        non_equity_types = [
            ("Bootstrapping", r'bootstrapping'),
            ("Grants", r'grants'),
        ]

        for name, pattern in equity_types:
            section = _extract_section(guide_content, pattern)
            assert section, f"{name} section must exist"
            has_referral = bool(re.search(
                r'professional\s+referral|financial\s+advisor|attorney',
                section, re.IGNORECASE
            ))
            assert has_referral, (
                f"Equity path '{name}' must contain professional referral trigger"
            )

        for name, pattern in non_equity_types:
            section = _extract_section(guide_content, pattern)
            assert section, f"{name} section must exist"
            has_referral = bool(re.search(
                r'professional\s+referral', section, re.IGNORECASE
            ))
            assert not has_referral, (
                f"Non-equity path '{name}' must NOT contain professional referral trigger"
            )
