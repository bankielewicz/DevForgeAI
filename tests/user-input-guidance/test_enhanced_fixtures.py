"""
Unit tests for STORY-059: User Input Guidance Validation & Testing Suite
Test Suite: AC#3 - Enhanced Test Fixtures Created

Purpose: Validate that enhanced test fixtures are created with proper guidance
application, readability, length increase, and feature preservation.

Test Framework: pytest
Coverage: Enhanced fixture creation, guidance application, readability, length increase, domain preservation
"""

import re
from pathlib import Path

import pytest

try:
    import textstat
except ImportError:
    textstat = None


class TestEnhancedFixturesCreation:
    """Tests for enhanced fixtures (AC#3)"""

    @pytest.fixture
    def enhanced_fixtures_path(self):
        """Base path for enhanced fixtures directory"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

    @pytest.fixture
    def baseline_fixtures_path(self):
        """Base path for baseline fixtures directory"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

    @pytest.fixture
    def guidance_principles(self):
        """Guidance principles that should be applied in enhanced fixtures"""
        return {
            "specific_scope": ["clearly", "defined", "scope", "boundary", "specific"],
            "measurable_criteria": ["<", ">", "%", "ms", "seconds", "users", "uptime"],
            "clear_ac": ["given", "when", "then", "testable"],
            "explicit_constraints": ["constraint", "requirement", "technology", "integration"],
            "nfr": ["performance", "security", "reliability", "scalability"],
        }

    def test_should_create_10_enhanced_fixtures_matching_baselines(
        self, enhanced_fixtures_path, baseline_fixtures_path
    ):
        """
        GIVEN baseline fixtures exist
        WHEN enhanced fixtures are created
        THEN 10 enhanced fixtures exist with matching filenames (enhanced-[NN]-[category].txt)

        Evidence: All 10 enhanced fixtures created with correct naming
        """
        # Arrange
        enhanced_path = enhanced_fixtures_path
        baseline_path = baseline_fixtures_path

        # Act
        enhanced_fixtures = []
        if enhanced_path.exists():
            enhanced_fixtures = sorted([f.name for f in enhanced_path.glob("enhanced-*.txt")])

        baseline_fixtures = []
        if baseline_path.exists():
            baseline_fixtures = sorted([f.name for f in baseline_path.glob("baseline-*.txt")])

        # Assert
        expected_count = 10
        assert len(enhanced_fixtures) == expected_count, (
            f"Expected {expected_count} enhanced fixtures, found {len(enhanced_fixtures)}"
        )

        # Verify naming pattern
        naming_pattern = re.compile(r"^enhanced-\d{2}-[a-z-]+\.txt$")
        for fixture in enhanced_fixtures:
            assert naming_pattern.match(fixture), (
                f"Enhanced fixture '{fixture}' does not match pattern 'enhanced-NN-category.txt'"
            )

    def test_should_apply_3_to_5_guidance_principles_per_fixture(
        self, enhanced_fixtures_path, guidance_principles
    ):
        """
        GIVEN enhanced fixtures apply guidance recommendations
        WHEN guidance principles are counted
        THEN each fixture applies 3-5 guidance principles (specific scope, measurable criteria, clear AC, constraints, NFRs)

        Evidence: Guidance principles applied to enhanced fixtures
        """
        # Arrange
        enhanced_path = enhanced_fixtures_path
        min_principles, max_principles = 3, 5

        # Act
        principle_counts = {}
        if enhanced_path.exists():
            for fixture_file in sorted(enhanced_path.glob("enhanced-*.txt")):
                content = fixture_file.read_text().lower()
                detected_principles = set()

                # Check for specific scope principle
                for term in guidance_principles["specific_scope"]:
                    if term in content:
                        detected_principles.add("specific_scope")
                        break

                # Check for measurable criteria principle
                for term in guidance_principles["measurable_criteria"]:
                    if term in content:
                        detected_principles.add("measurable_criteria")
                        break

                # Check for clear AC principle
                if any(term in content for term in guidance_principles["clear_ac"]):
                    detected_principles.add("clear_ac")

                # Check for explicit constraints principle
                if any(term in content for term in guidance_principles["explicit_constraints"]):
                    detected_principles.add("explicit_constraints")

                # Check for NFR principle
                if any(term in content for term in guidance_principles["nfr"]):
                    detected_principles.add("nfr")

                principle_counts[fixture_file.name] = len(detected_principles)

        # Assert
        assert len(principle_counts) > 0, "No enhanced fixtures found to validate guidance principles"

        for fixture_name, principle_count in principle_counts.items():
            assert (
                min_principles <= principle_count <= max_principles
            ), f"{fixture_name}: {principle_count} principles detected (expected {min_principles}-{max_principles})"

    def test_should_demonstrate_30_to_60_percent_length_increase(
        self, enhanced_fixtures_path, baseline_fixtures_path
    ):
        """
        GIVEN enhanced fixtures are rewritten versions of baselines
        WHEN length is compared
        THEN enhanced fixtures are 30-60% longer than corresponding baselines

        Evidence: Length increase measured and validated
        """
        # Arrange
        enhanced_path = enhanced_fixtures_path
        baseline_path = baseline_fixtures_path
        min_increase_pct, max_increase_pct = 30, 60

        # Act
        length_comparisons = {}
        if enhanced_path.exists() and baseline_path.exists():
            for enhanced_file in sorted(enhanced_path.glob("enhanced-*.txt")):
                # Extract fixture number and category
                match = re.search(r"enhanced-(\d{2})-(.+)\.txt", enhanced_file.name)
                if not match:
                    continue

                baseline_filename = f"baseline-{match.group(1)}-{match.group(2)}.txt"
                baseline_file = baseline_path / baseline_filename

                if baseline_file.exists():
                    enhanced_words = len(enhanced_file.read_text().split())
                    baseline_words = len(baseline_file.read_text().split())

                    if baseline_words > 0:
                        increase_pct = ((enhanced_words - baseline_words) / baseline_words) * 100
                        length_comparisons[enhanced_file.name] = {
                            "baseline_words": baseline_words,
                            "enhanced_words": enhanced_words,
                            "increase_pct": increase_pct,
                        }

        # Assert
        assert len(length_comparisons) > 0, "No baseline/enhanced pairs found to validate length increase"

        for fixture_name, comparison in length_comparisons.items():
            increase = comparison["increase_pct"]
            assert (
                min_increase_pct <= increase <= max_increase_pct
            ), (
                f"{fixture_name}: {increase:.1f}% increase "
                f"(expected {min_increase_pct}-{max_increase_pct}%)"
            )

    def test_should_maintain_readability_flesch_score_greater_than_60(
        self, enhanced_fixtures_path
    ):
        """
        GIVEN enhanced fixtures contain additional detail and specificity
        WHEN readability is measured
        THEN Flesch Reading Ease score is ≥60 (readable by professionals)

        Evidence: Readability scores validated via textstat library
        """
        if textstat is None:
            pytest.skip("textstat library not installed - cannot measure readability")

        # Arrange
        enhanced_path = enhanced_fixtures_path
        min_fre_score = 60

        # Act
        readability_results = {}
        if enhanced_path.exists():
            for fixture_file in sorted(enhanced_path.glob("enhanced-*.txt")):
                content = fixture_file.read_text()
                fre_score = textstat.flesch_reading_ease(content)
                readability_results[fixture_file.name] = fre_score

        # Assert
        assert len(readability_results) > 0, "No enhanced fixtures found to validate readability"

        for fixture_name, fre_score in readability_results.items():
            assert (
                fre_score >= min_fre_score
            ), f"{fixture_name}: FRE {fre_score:.1f} (expected ≥{min_fre_score})"

    def test_should_preserve_original_feature_intent_same_domain(
        self, enhanced_fixtures_path, baseline_fixtures_path
    ):
        """
        GIVEN enhanced fixtures are rewrites of baseline fixtures
        WHEN domain and intent are compared
        THEN enhanced fixtures preserve the original feature intent (same domain, same core functionality)

        Evidence: Domain keywords match between baseline and enhanced versions
        """
        # Arrange
        enhanced_path = enhanced_fixtures_path
        baseline_path = baseline_fixtures_path

        # Domain-specific keywords to verify preservation
        domain_keywords = {
            "crud": ["user", "create", "read", "update", "delete"],
            "auth": ["login", "signup", "authenticate", "authorization"],
            "api": ["api", "endpoint", "request", "response", "integration"],
            "data": ["data", "process", "etl", "batch"],
            "ui": ["ui", "component", "dashboard", "form"],
            "report": ["report", "analytics", "generate"],
            "job": ["job", "background", "worker", "scheduled"],
            "search": ["search", "query", "filter"],
            "file": ["file", "upload", "download"],
            "notify": ["notification", "alert", "message"],
        }

        # Act
        domain_preservation_results = {}
        if enhanced_path.exists() and baseline_path.exists():
            for enhanced_file in sorted(enhanced_path.glob("enhanced-*.txt")):
                match = re.search(r"enhanced-(\d{2})-(.+)\.txt", enhanced_file.name)
                if not match:
                    continue

                baseline_filename = f"baseline-{match.group(1)}-{match.group(2)}.txt"
                baseline_file = baseline_path / baseline_filename

                if baseline_file.exists():
                    enhanced_content = enhanced_file.read_text().lower()
                    baseline_content = baseline_file.read_text().lower()

                    # Extract domain from filename
                    category = match.group(2)
                    domain_key = category.split("-")[0]

                    # Check if baseline has domain keywords
                    baseline_keywords = domain_keywords.get(domain_key, [])
                    baseline_matches = sum(
                        1 for kw in baseline_keywords if kw in baseline_content
                    )
                    enhanced_matches = sum(
                        1 for kw in baseline_keywords if kw in enhanced_content
                    )

                    domain_preservation_results[enhanced_file.name] = {
                        "baseline_keyword_matches": baseline_matches,
                        "enhanced_keyword_matches": enhanced_matches,
                        "preserved": enhanced_matches >= baseline_matches,
                    }

        # Assert
        assert len(domain_preservation_results) > 0, "No baseline/enhanced pairs found to validate domain preservation"

        for fixture_name, result in domain_preservation_results.items():
            assert result["preserved"], (
                f"{fixture_name}: Domain keywords not preserved - "
                f"baseline {result['baseline_keyword_matches']}, enhanced {result['enhanced_keyword_matches']}"
            )

    def test_should_use_concrete_terminology_not_generic_terms(self, enhanced_fixtures_path):
        """
        GIVEN enhanced fixtures should use concrete terminology
        WHEN generic terms are checked
        THEN enhanced fixtures use specific terms (e.g., "customers" not "users", "transaction records" not "data")

        Evidence: Generic term reduction validated
        """
        # Arrange
        enhanced_path = enhanced_fixtures_path

        # Generic vs concrete term patterns
        generic_terms = {
            "users": ["customer", "client", "admin", "stakeholder"],
            "data": ["record", "transaction", "entity", "profile"],
            "system": ["application", "service", "platform", "module"],
            "feature": ["function", "capability", "operation", "action"],
        }

        # Act
        concreteness_results = {}
        if enhanced_path.exists():
            for fixture_file in sorted(enhanced_path.glob("enhanced-*.txt")):
                content = fixture_file.read_text().lower()

                has_concrete_terms = False
                for generic, concrete_list in generic_terms.items():
                    if generic in content:
                        # Check if concrete alternatives are also present
                        if any(concrete in content for concrete in concrete_list):
                            has_concrete_terms = True
                            break

                concreteness_results[fixture_file.name] = has_concrete_terms

        # Assert
        assert len(concreteness_results) > 0, "No enhanced fixtures found to validate terminology"

        for fixture_name, has_concrete in concreteness_results.items():
            assert has_concrete, (
                f"{fixture_name}: Does not use concrete terminology "
                "(should replace 'users' with 'customers/admins', 'data' with 'records/profiles', etc.)"
            )
