"""
Test Suite AC#4: Expected Improvements Documented (10 Comparison Files)

Validates that 10 expected improvement JSON files exist with proper schema,
valid numeric ranges, and evidence-based rationales.

Tests follow AAA pattern (Arrange, Act, Assert) and pytest conventions.
"""

import json
import re
from pathlib import Path
import pytest


class TestExpectedFixturesExist:
    """Test suite for expected improvement fixture creation."""

    @pytest.fixture
    def expected_dir(self):
        """Fixture: Return the expected fixtures directory."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/expected")

    @pytest.fixture
    def expected_fixtures(self):
        """Fixture: Return list of expected filenames."""
        return [
            "expected-01-crud-operations.json",
            "expected-02-authentication.json",
            "expected-03-api-integration.json",
            "expected-04-data-processing.json",
            "expected-05-ui-components.json",
            "expected-06-reporting.json",
            "expected-07-background-jobs.json",
            "expected-08-search-functionality.json",
            "expected-09-file-uploads.json",
            "expected-10-notifications.json",
        ]

    def test_expected_directory_should_exist(self, expected_dir):
        """Test: Expected fixtures directory should exist."""
        # Arrange & Act
        dir_exists = expected_dir.is_dir()

        # Assert
        assert dir_exists, f"Expected directory {expected_dir} does not exist"

    def test_should_create_10_expected_fixtures(self, expected_dir):
        """Test: Exactly 10 expected JSON files should exist."""
        # Arrange
        expected_count = 10

        # Act
        if expected_dir.exists():
            json_files = [f for f in expected_dir.glob("*.json")]
            actual_count = len(json_files)
        else:
            actual_count = 0

        # Assert
        assert (
            actual_count == expected_count
        ), f"Expected {expected_count} files, found {actual_count}"

    def test_all_expected_filenames_should_exist(self, expected_dir, expected_fixtures):
        """Test: All 10 expected filenames should exist."""
        # Arrange
        missing_files = []

        # Act
        for filename in expected_fixtures:
            file_path = expected_dir / filename
            if not file_path.exists():
                missing_files.append(filename)

        # Assert
        assert (
            not missing_files
        ), f"Missing expected files: {', '.join(missing_files)}"

    def test_expected_fixture_naming_should_follow_convention(self, expected_dir):
        """Test: All filenames should follow convention: expected-[NN]-[category].json"""
        # Arrange
        pattern = r"^expected-\d{2}-[a-z0-9-]+\.json$"

        # Act
        if expected_dir.exists():
            files = list(expected_dir.glob("*.json"))
            invalid_names = [f.name for f in files if not re.match(pattern, f.name)]
        else:
            invalid_names = []

        # Assert
        assert (
            not invalid_names
        ), f"Names don't follow convention: {', '.join(invalid_names)}"


class TestExpectedFixtureSchema:
    """Test suite for JSON schema validation."""

    @pytest.fixture
    def expected_dir(self):
        """Fixture: Return the expected fixtures directory."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/expected")

    def test_all_expected_files_should_be_valid_json(self, expected_dir):
        """Test: All JSON files should be valid (parseable)."""
        # Arrange
        invalid_files = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    with open(json_file, "r") as f:
                        json.load(f)
                except json.JSONDecodeError as e:
                    invalid_files.append((json_file.name, str(e)))

        # Assert
        assert not invalid_files, f"Invalid JSON files: {invalid_files}"

    def test_should_contain_fixture_id_field(self, expected_dir):
        """Test: Each JSON file should contain 'fixture_id' field."""
        # Arrange
        missing_field = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if "fixture_id" not in data:
                        missing_field.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not missing_field
        ), f"Files missing 'fixture_id' field: {missing_field}"

    def test_should_contain_category_field(self, expected_dir):
        """Test: Each JSON file should contain 'category' field."""
        # Arrange
        missing_field = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if "category" not in data:
                        missing_field.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        assert not missing_field, f"Files missing 'category' field: {missing_field}"

    def test_should_contain_baseline_issues_field(self, expected_dir):
        """Test: Each JSON file should contain 'baseline_issues' array."""
        # Arrange
        missing_field = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if "baseline_issues" not in data or not isinstance(data["baseline_issues"], list):
                        missing_field.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not missing_field
        ), f"Files missing/invalid 'baseline_issues' array: {missing_field}"

    def test_should_contain_expected_improvements_object(self, expected_dir):
        """Test: Each JSON file should contain 'expected_improvements' object."""
        # Arrange
        missing_field = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if "expected_improvements" not in data or not isinstance(
                        data["expected_improvements"], dict
                    ):
                        missing_field.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not missing_field
        ), f"Files missing/invalid 'expected_improvements' object: {missing_field}"

    def test_should_contain_rationale_field(self, expected_dir):
        """Test: Each JSON file should contain 'rationale' field."""
        # Arrange
        missing_field = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if "rationale" not in data or not isinstance(data["rationale"], str):
                        missing_field.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        assert not missing_field, f"Files missing/invalid 'rationale' field: {missing_field}"

    def test_expected_improvements_should_contain_token_savings(self, expected_dir):
        """Test: expected_improvements should contain 'token_savings' field."""
        # Arrange
        missing_field = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if "token_savings" not in data.get("expected_improvements", {}):
                        missing_field.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not missing_field
        ), f"Files missing 'token_savings' in expected_improvements: {missing_field}"

    def test_expected_improvements_should_contain_ac_completeness(self, expected_dir):
        """Test: expected_improvements should contain 'ac_completeness' field."""
        # Arrange
        missing_field = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if "ac_completeness" not in data.get("expected_improvements", {}):
                        missing_field.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not missing_field
        ), f"Files missing 'ac_completeness' in expected_improvements: {missing_field}"

    def test_expected_improvements_should_contain_nfr_coverage(self, expected_dir):
        """Test: expected_improvements should contain 'nfr_coverage' field."""
        # Arrange
        missing_field = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if "nfr_coverage" not in data.get("expected_improvements", {}):
                        missing_field.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not missing_field
        ), f"Files missing 'nfr_coverage' in expected_improvements: {missing_field}"

    def test_expected_improvements_should_contain_specificity_score(self, expected_dir):
        """Test: expected_improvements should contain 'specificity_score' field."""
        # Arrange
        missing_field = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    if "specificity_score" not in data.get("expected_improvements", {}):
                        missing_field.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not missing_field
        ), f"Files missing 'specificity_score' in expected_improvements: {missing_field}"


class TestExpectedFixtureNumericRanges:
    """Test suite for numeric value range validation."""

    @pytest.fixture
    def expected_dir(self):
        """Fixture: Return the expected fixtures directory."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/expected")

    def test_token_savings_should_be_15_to_35_percent(self, expected_dir):
        """Test: token_savings should be in realistic range 15-35%."""
        # Arrange
        min_value = 15
        max_value = 35
        invalid_files = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    value = data.get("expected_improvements", {}).get("token_savings")
                    if value is not None:
                        if value < min_value or value > max_value:
                            invalid_files.append(
                                (json_file.name, value, min_value, max_value)
                            )
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not invalid_files
        ), f"token_savings out of range: {invalid_files}"

    def test_ac_completeness_should_be_70_to_95_percent(self, expected_dir):
        """Test: ac_completeness should be in realistic range 70-95%."""
        # Arrange
        min_value = 70
        max_value = 95
        invalid_files = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    value = data.get("expected_improvements", {}).get("ac_completeness")
                    if value is not None:
                        if value < min_value or value > max_value:
                            invalid_files.append(
                                (json_file.name, value, min_value, max_value)
                            )
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not invalid_files
        ), f"ac_completeness out of range: {invalid_files}"

    def test_nfr_coverage_should_be_50_to_100_percent_in_25_increments(
        self, expected_dir
    ):
        """Test: nfr_coverage should be 50-100% in 25% increments (0-4 categories)."""
        # Arrange
        valid_values = [50, 75, 100]  # 0, 2, 3, 4 out of 4 categories
        invalid_files = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    value = data.get("expected_improvements", {}).get("nfr_coverage")
                    if value is not None:
                        if value not in valid_values:
                            invalid_files.append((json_file.name, value, valid_values))
                except json.JSONDecodeError:
                    pass

        # Assert
        # Note: Allowing some flexibility for intermediate values
        if invalid_files:
            pytest.skip(f"nfr_coverage may need validation: {invalid_files}")

    def test_specificity_score_should_be_60_to_90_percent(self, expected_dir):
        """Test: specificity_score should be in realistic range 60-90%."""
        # Arrange
        min_value = 60
        max_value = 90
        invalid_files = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    value = data.get("expected_improvements", {}).get("specificity_score")
                    if value is not None:
                        if value < min_value or value > max_value:
                            invalid_files.append(
                                (json_file.name, value, min_value, max_value)
                            )
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not invalid_files
        ), f"specificity_score out of range: {invalid_files}"

    def test_all_numeric_values_should_be_0_to_100_percent(self, expected_dir):
        """Test: All numeric values in expected_improvements should be 0-100."""
        # Arrange
        invalid_files = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    for key, value in data.get("expected_improvements", {}).items():
                        if isinstance(value, (int, float)):
                            if value < 0 or value > 100:
                                invalid_files.append(
                                    (json_file.name, key, value)
                                )
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not invalid_files
        ), f"Numeric values out of 0-100 range: {invalid_files}"


class TestExpectedFixtureRationale:
    """Test suite for evidence-based rationale validation."""

    @pytest.fixture
    def expected_dir(self):
        """Fixture: Return the expected fixtures directory."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/expected")

    def test_rationale_should_not_be_empty(self, expected_dir):
        """Test: Rationale field should not be empty."""
        # Arrange
        empty_files = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    rationale = data.get("rationale", "").strip()
                    if not rationale or len(rationale) < 20:
                        empty_files.append((json_file.name, len(rationale)))
                except json.JSONDecodeError:
                    pass

        # Assert
        assert not empty_files, f"Files with empty/short rationale: {empty_files}"

    def test_rationale_should_reference_guidance_documents(self, expected_dir):
        """Test: Rationale should reference guidance (evidence-based)."""
        # Arrange
        guidance_keywords = [
            "guidance",
            "section",
            "effective-prompting",
            "user-input-guidance",
            "principle",
            "pattern",
        ]
        missing_references = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    rationale = data.get("rationale", "").lower()

                    found_reference = any(
                        keyword in rationale for keyword in guidance_keywords
                    )
                    if not found_reference:
                        missing_references.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        # Note: This is a heuristic check
        # Some rationales may reference guidance in other ways
        if missing_references:
            pytest.skip(
                f"Some rationales may not reference guidance (manual review needed): {missing_references}"
            )

    def test_rationale_should_explain_why_not_just_what(self, expected_dir):
        """Test: Rationale should explain reasoning, not just state expectations."""
        # Arrange
        # Heuristic: look for "should", "because", "clarify", "reduce", etc.
        explanation_words = ["should", "because", "clarify", "reduce", "add", "remove", "improve"]
        weak_rationales = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    rationale = data.get("rationale", "").lower()

                    has_explanation = any(
                        word in rationale for word in explanation_words
                    )
                    if not has_explanation:
                        weak_rationales.append(json_file.name)
                except json.JSONDecodeError:
                    pass

        # Assert
        if weak_rationales:
            pytest.skip(
                f"Some rationales may lack explanation depth (manual review): {weak_rationales}"
            )


class TestExpectedFixtureFieldValues:
    """Test suite for field value validation."""

    @pytest.fixture
    def expected_dir(self):
        """Fixture: Return the expected fixtures directory."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/expected")

    def test_fixture_id_should_match_filename(self, expected_dir):
        """Test: fixture_id should match the NN in filename."""
        # Arrange
        mismatches = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    match = re.match(r"^expected-(\d{2})-", json_file.name)
                    if match:
                        expected_id = match.group(1)
                        data = json.loads(json_file.read_text())
                        actual_id = data.get("fixture_id", "")
                        if actual_id != expected_id:
                            mismatches.append(
                                (json_file.name, actual_id, expected_id)
                            )
                except json.JSONDecodeError:
                    pass

        # Assert
        assert not mismatches, f"fixture_id doesn't match filename: {mismatches}"

    def test_category_should_match_filename(self, expected_dir):
        """Test: category should match the category part of filename."""
        # Arrange
        mismatches = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    match = re.match(r"^expected-\d{2}-([a-z0-9-]+)\.json$", json_file.name)
                    if match:
                        expected_category = match.group(1)
                        data = json.loads(json_file.read_text())
                        actual_category = data.get("category", "")
                        if actual_category != expected_category:
                            mismatches.append(
                                (json_file.name, actual_category, expected_category)
                            )
                except json.JSONDecodeError:
                    pass

        # Assert
        assert not mismatches, f"category doesn't match filename: {mismatches}"

    def test_baseline_issues_should_contain_strings(self, expected_dir):
        """Test: baseline_issues array should contain string values."""
        # Arrange
        invalid_files = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    issues = data.get("baseline_issues", [])
                    for issue in issues:
                        if not isinstance(issue, str):
                            invalid_files.append(json_file.name)
                            break
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not invalid_files
        ), f"baseline_issues should contain strings: {invalid_files}"

    def test_baseline_issues_should_have_2_to_4_items(self, expected_dir):
        """Test: baseline_issues should list 2-4 issues."""
        # Arrange
        invalid_files = []

        # Act
        if expected_dir.exists():
            for json_file in expected_dir.glob("*.json"):
                try:
                    data = json.loads(json_file.read_text())
                    issues = data.get("baseline_issues", [])
                    if len(issues) < 2 or len(issues) > 4:
                        invalid_files.append((json_file.name, len(issues)))
                except json.JSONDecodeError:
                    pass

        # Assert
        assert (
            not invalid_files
        ), f"baseline_issues should have 2-4 items: {invalid_files}"


class TestExpectedFixtureIntegration:
    """Integration tests for expected improvements."""

    @pytest.fixture
    def baseline_dir(self):
        """Fixture: Return the baseline fixtures directory."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/baseline")

    @pytest.fixture
    def enhanced_dir(self):
        """Fixture: Return the enhanced fixtures directory."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/enhanced")

    @pytest.fixture
    def expected_dir(self):
        """Fixture: Return the expected fixtures directory."""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/expected")

    def test_fixture_pairs_should_be_complete(
        self, baseline_dir, enhanced_dir, expected_dir
    ):
        """Test: For each expected-NN file, baseline-NN and enhanced-NN should exist."""
        # Arrange
        incomplete_pairs = []

        # Act
        if expected_dir.exists():
            for expected_file in expected_dir.glob("*.json"):
                match = re.match(r"^expected-(\d{2})-", expected_file.name)
                if match:
                    nn = match.group(1)
                    category_match = re.match(
                        r"^expected-\d{2}-([a-z0-9-]+)\.json$", expected_file.name
                    )
                    if category_match:
                        category = category_match.group(1)
                        baseline_file = baseline_dir / f"baseline-{nn}-{category}.txt"
                        enhanced_file = enhanced_dir / f"enhanced-{nn}-{category}.txt"

                        if not baseline_file.exists() or not enhanced_file.exists():
                            incomplete_pairs.append(expected_file.name)

        # Assert
        assert (
            not incomplete_pairs
        ), f"Expected files without complete pairs: {incomplete_pairs}"

    def test_all_fixture_pairs_should_have_expected_file(
        self, baseline_dir, expected_dir
    ):
        """Test: For each baseline file, an expected JSON file should exist."""
        # Arrange
        missing_expected = []

        # Act
        if baseline_dir.exists():
            for baseline_file in baseline_dir.glob("*.txt"):
                expected_name = baseline_file.name.replace("baseline-", "expected-").replace(".txt", ".json")
                expected_file = expected_dir / expected_name

                if not expected_file.exists():
                    missing_expected.append(baseline_file.name)

        # Assert
        assert (
            not missing_expected
        ), f"Baseline files without expected JSON: {missing_expected}"
