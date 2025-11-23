"""
Unit tests for STORY-059: User Input Guidance Validation & Testing Suite
Test Suite: AC#2 - Baseline Test Fixtures Created

Purpose: Validate that baseline test fixtures are created with correct naming,
content, quality issues, and natural language format.

Test Framework: pytest
Coverage: Fixture creation, naming convention, word counts, quality issues, content quality
"""

import os
import re
from pathlib import Path
from typing import List

import pytest


class TestBaselineFixturesCreation:
    """Tests for baseline fixtures (AC#2)"""

    @pytest.fixture
    def fixtures_base_path(self):
        """Base path for fixtures directory"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

    @pytest.fixture
    def expected_fixtures(self):
        """Expected baseline fixture configurations"""
        return [
            {"number": "01", "category": "crud-operations", "domain": "user management CRUD"},
            {"number": "02", "category": "authentication", "domain": "login/signup flow"},
            {"number": "03", "category": "api-integration", "domain": "third-party API calls"},
            {"number": "04", "category": "data-processing", "domain": "ETL or batch processing"},
            {"number": "05", "category": "ui-components", "domain": "dashboard or form UI"},
            {"number": "06", "category": "reporting", "domain": "analytics or reports generation"},
            {"number": "07", "category": "background-jobs", "domain": "scheduled tasks or workers"},
            {"number": "08", "category": "search-functionality", "domain": "search feature"},
            {"number": "09", "category": "file-uploads", "domain": "file handling"},
            {"number": "10", "category": "notifications", "domain": "notification system"},
        ]

    @pytest.fixture
    def quality_issues_patterns(self):
        """Common quality issues that should be detected in baseline fixtures"""
        return {
            "vague_requirements": ["fast", "good", "better", "optimized", "improved"],
            "missing_criteria": ["needs", "should", "must", "feature"],
            "ambiguous_ac": ["ac", "acceptance", "criteria"],
            "omitted_nfr": ["performance", "security", "scalability", "reliability"],
        }

    def test_should_create_10_baseline_fixtures_with_correct_naming(self, fixtures_base_path, expected_fixtures):
        """
        GIVEN baseline test fixtures are needed for validation
        WHEN 10 fixtures are created in fixtures/baseline/
        THEN each fixture file is named baseline-[NN]-[category].txt where NN is 01-10

        Evidence: All 10 fixtures exist with correct naming convention
        """
        # Arrange
        base_path = fixtures_base_path

        # Act
        existing_fixtures = []
        if base_path.exists():
            existing_fixtures = sorted([f.name for f in base_path.glob("baseline-*.txt")])

        # Assert
        expected_count = 10
        assert len(existing_fixtures) == expected_count, (
            f"Expected {expected_count} baseline fixtures, found {len(existing_fixtures)}: "
            f"{existing_fixtures}"
        )

        # Verify naming convention for each fixture
        naming_pattern = re.compile(r"^baseline-\d{2}-[a-z-]+\.txt$")
        for fixture in existing_fixtures:
            assert naming_pattern.match(fixture), (
                f"Fixture '{fixture}' does not match naming pattern "
                "'baseline-NN-category.txt'"
            )

    def test_should_match_expected_fixture_categories(self, fixtures_base_path, expected_fixtures):
        """
        GIVEN 10 baseline fixtures exist
        WHEN their categories are checked
        THEN the fixtures cover diverse domains (CRUD, Auth, API, Data, UI, Reporting, Jobs, Search, Files, Notifications)

        Evidence: All 10 fixture categories match expected domains
        """
        # Arrange
        base_path = fixtures_base_path
        expected_categories = {f["category"] for f in expected_fixtures}

        # Act
        existing_categories = set()
        if base_path.exists():
            for file in base_path.glob("baseline-*.txt"):
                # Extract category from filename: baseline-NN-[category].txt
                match = re.search(r"baseline-\d{2}-(.+)\.txt", file.name)
                if match:
                    existing_categories.add(match.group(1))

        # Assert
        assert existing_categories == expected_categories, (
            f"Found categories {existing_categories}, "
            f"expected {expected_categories}"
        )

    def test_should_have_word_count_between_50_and_200(self, fixtures_base_path):
        """
        GIVEN baseline fixtures are created
        WHEN word counts are measured
        THEN each fixture contains 50-200 words (realistic user input, not too brief or verbose)

        Evidence: All fixtures meet word count requirements
        """
        # Arrange
        base_path = fixtures_base_path
        min_words, max_words = 50, 200

        # Act
        word_count_results = {}
        if base_path.exists():
            for fixture_file in sorted(base_path.glob("baseline-*.txt")):
                content = fixture_file.read_text().strip()
                word_count = len(content.split())
                word_count_results[fixture_file.name] = word_count

        # Assert
        assert len(word_count_results) > 0, "No baseline fixtures found to validate word count"

        for fixture_name, word_count in word_count_results.items():
            assert (
                min_words <= word_count <= max_words
            ), f"{fixture_name}: {word_count} words (expected {min_words}-{max_words})"

    def test_should_exhibit_2_to_4_quality_issues_per_fixture(
        self, fixtures_base_path, quality_issues_patterns
    ):
        """
        GIVEN baseline fixtures represent typical user input
        WHEN quality issues are detected
        THEN each fixture exhibits 2-4 common quality issues (vague requirements, missing criteria, ambiguous AC, omitted NFRs)

        Evidence: Quality issues detected in baseline fixtures
        """
        # Arrange
        base_path = fixtures_base_path
        min_issues, max_issues = 2, 4

        # Act
        issue_detection_results = {}
        if base_path.exists():
            for fixture_file in sorted(base_path.glob("baseline-*.txt")):
                content = fixture_file.read_text().lower()
                detected_issues = set()

                # Check for vague requirements
                for term in quality_issues_patterns["vague_requirements"]:
                    if term in content:
                        detected_issues.add("vague_requirements")
                        break

                # Check for missing success criteria
                for phrase in ["needs to", "should", "must have", "feature"]:
                    if phrase in content:
                        detected_issues.add("missing_criteria")
                        break

                # Check for ambiguous acceptance criteria
                if "acceptance" in content or "criteria" in content:
                    detected_issues.add("ambiguous_ac")

                # Check for omitted NFRs
                for term in quality_issues_patterns["omitted_nfr"]:
                    if term not in content:
                        detected_issues.add("omitted_nfr")
                        break

                issue_detection_results[fixture_file.name] = len(detected_issues)

        # Assert
        assert len(issue_detection_results) > 0, "No baseline fixtures found to validate quality issues"

        for fixture_name, issue_count in issue_detection_results.items():
            assert (
                min_issues <= issue_count <= max_issues
            ), f"{fixture_name}: {issue_count} issues detected (expected {min_issues}-{max_issues})"

    def test_should_use_natural_language_format_not_technical_specs(self, fixtures_base_path):
        """
        GIVEN baseline fixtures are written in natural language
        WHEN content is analyzed
        THEN fixtures contain sentences (not bullets, not technical specs, not code)

        Evidence: Natural language format confirmed (sentences present, code/bullets absent)
        """
        # Arrange
        base_path = fixtures_base_path
        code_indicators = ["class ", "def ", "function", "interface", "void ", "public ", "return"]
        bullet_indicators = ["\n- ", "\n* ", "\n• "]

        # Act
        format_validation_results = {}
        if base_path.exists():
            for fixture_file in sorted(base_path.glob("baseline-*.txt")):
                content = fixture_file.read_text()

                has_sentences = bool(re.search(r"\. ", content))
                has_code = any(indicator in content for indicator in code_indicators)
                has_bullets = any(indicator in content for indicator in bullet_indicators)

                format_validation_results[fixture_file.name] = {
                    "has_sentences": has_sentences,
                    "has_code": has_code,
                    "has_bullets": has_bullets,
                    "is_valid_format": has_sentences and not has_code and not has_bullets,
                }

        # Assert
        assert len(format_validation_results) > 0, "No baseline fixtures found to validate format"

        for fixture_name, validation in format_validation_results.items():
            assert validation["is_valid_format"], (
                f"{fixture_name}: Invalid format - "
                f"has_sentences={validation['has_sentences']}, "
                f"has_code={validation['has_code']}, "
                f"has_bullets={validation['has_bullets']}"
            )

    @pytest.mark.parametrize(
        "fixture_number,expected_category",
        [
            ("01", "crud-operations"),
            ("02", "authentication"),
            ("03", "api-integration"),
            ("04", "data-processing"),
            ("05", "ui-components"),
            ("06", "reporting"),
            ("07", "background-jobs"),
            ("08", "search-functionality"),
            ("09", "file-uploads"),
            ("10", "notifications"),
        ],
    )
    def test_should_have_correct_fixture_file_for_each_category(
        self, fixtures_base_path, fixture_number, expected_category
    ):
        """
        GIVEN baseline fixtures are created
        WHEN each fixture is checked
        THEN the fixture file exists with correct naming (baseline-NN-category.txt)

        Evidence: All 10 expected fixture files exist with correct names
        Parameterized across all 10 fixtures
        """
        # Arrange
        base_path = fixtures_base_path
        expected_filename = f"baseline-{fixture_number}-{expected_category}.txt"
        expected_path = base_path / expected_filename

        # Act
        fixture_exists = expected_path.exists() if base_path.exists() else False

        # Assert
        assert fixture_exists, (
            f"Expected fixture '{expected_filename}' not found in {base_path}"
        )
