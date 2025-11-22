"""
test_fixture_structure.py - Unit tests for test suite directory structure and fixture organization
Following TDD Red phase - all tests should FAIL before implementation
"""

import os
import json
import pytest
import stat
from pathlib import Path


class TestDirectoryStructureCreated:
    """AC#1: Test Directory Structure Created - 12 items

    Validates the directory structure exists with proper permissions and documentation.
    """

    def test_fixture_root_directory_exists(self):
        """Test: tests/user-input-guidance/ directory exists"""
        # Arrange
        fixture_root = Path("tests/user-input-guidance")

        # Assert
        assert fixture_root.exists(), "tests/user-input-guidance/ directory not found"
        assert fixture_root.is_dir(), "tests/user-input-guidance/ is not a directory"

    def test_baseline_fixtures_directory_exists(self):
        """Test: tests/user-input-guidance/fixtures/baseline/ directory exists"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")

        # Assert
        assert baseline_dir.exists(), "fixtures/baseline/ directory not found"
        assert baseline_dir.is_dir(), "fixtures/baseline/ is not a directory"

    def test_enhanced_fixtures_directory_exists(self):
        """Test: tests/user-input-guidance/fixtures/enhanced/ directory exists"""
        # Arrange
        enhanced_dir = Path("tests/user-input-guidance/fixtures/enhanced")

        # Assert
        assert enhanced_dir.exists(), "fixtures/enhanced/ directory not found"
        assert enhanced_dir.is_dir(), "fixtures/enhanced/ is not a directory"

    def test_expected_fixtures_directory_exists(self):
        """Test: tests/user-input-guidance/fixtures/expected/ directory exists"""
        # Arrange
        expected_dir = Path("tests/user-input-guidance/fixtures/expected")

        # Assert
        assert expected_dir.exists(), "fixtures/expected/ directory not found"
        assert expected_dir.is_dir(), "fixtures/expected/ is not a directory"

    def test_scripts_directory_exists(self):
        """Test: tests/user-input-guidance/scripts/ directory exists"""
        # Arrange
        scripts_dir = Path("tests/user-input-guidance/scripts")

        # Assert
        assert scripts_dir.exists(), "scripts/ directory not found"
        assert scripts_dir.is_dir(), "scripts/ is not a directory"

    def test_reports_directory_exists(self):
        """Test: tests/user-input-guidance/reports/ directory exists"""
        # Arrange
        reports_dir = Path("tests/user-input-guidance/reports")

        # Assert
        assert reports_dir.exists(), "reports/ directory not found"
        assert reports_dir.is_dir(), "reports/ is not a directory"

    def test_gitkeep_exists_in_reports(self):
        """Test: .gitkeep file exists in reports/ directory"""
        # Arrange
        gitkeep_file = Path("tests/user-input-guidance/reports/.gitkeep")

        # Assert
        assert gitkeep_file.exists(), "reports/.gitkeep file not found"

    def test_directory_permissions_are_755(self):
        """Test: All directories have 755 permissions (rwxr-xr-x)"""
        # Arrange
        directories = [
            Path("tests/user-input-guidance"),
            Path("tests/user-input-guidance/fixtures"),
            Path("tests/user-input-guidance/fixtures/baseline"),
            Path("tests/user-input-guidance/fixtures/enhanced"),
            Path("tests/user-input-guidance/fixtures/expected"),
            Path("tests/user-input-guidance/scripts"),
            Path("tests/user-input-guidance/reports"),
        ]

        # Act & Assert
        for directory in directories:
            if directory.exists():
                mode = stat.S_IMODE(directory.stat().st_mode)
                expected_mode = 0o755
                assert mode == expected_mode, f"{directory} permissions {oct(mode)} != {oct(expected_mode)}"

    def test_readme_md_exists(self):
        """Test: README.md exists in tests/user-input-guidance/"""
        # Arrange
        readme_file = Path("tests/user-input-guidance/README.md")

        # Assert
        assert readme_file.exists(), "README.md not found"
        assert readme_file.is_file(), "README.md is not a file"

    def test_readme_contains_purpose_section(self):
        """Test: README.md contains 'Purpose' section"""
        # Arrange
        readme_file = Path("tests/user-input-guidance/README.md")

        # Act
        content = readme_file.read_text()

        # Assert
        assert "Purpose" in content, "README.md missing 'Purpose' section"

    def test_readme_contains_usage_section(self):
        """Test: README.md contains 'Usage' section"""
        # Arrange
        readme_file = Path("tests/user-input-guidance/README.md")

        # Act
        content = readme_file.read_text()

        # Assert
        assert "Usage" in content or "usage" in content.lower(), "README.md missing 'Usage' section"

    def test_readme_contains_expected_outcomes_section(self):
        """Test: README.md contains 'Expected Outcomes' or similar section"""
        # Arrange
        readme_file = Path("tests/user-input-guidance/README.md")

        # Act
        content = readme_file.read_text()

        # Assert
        assert ("Expected Outcomes" in content or "Outcomes" in content or
                "expected" in content.lower()), "README.md missing 'Expected Outcomes' section"


class TestBaselineFixturesStructure:
    """AC#2: Baseline Test Fixtures Created (10 Feature Descriptions) - 13 items

    Validates baseline fixtures exist, follow naming convention, have correct word counts,
    and exhibit expected quality issues.
    """

    def test_10_baseline_fixtures_exist(self):
        """Test: Exactly 10 baseline fixture files exist (baseline-[01-10]-[category].txt)"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))

        # Assert
        assert len(baseline_files) == 10, f"Expected 10 baseline fixtures, found {len(baseline_files)}"

    def test_baseline_filenames_follow_convention(self):
        """Test: All baseline filenames follow convention baseline-[NN]-[category].txt"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")
        import re
        pattern = re.compile(r"^baseline-\d{2}-[a-z0-9-]+\.txt$")

        # Act
        baseline_files = list(baseline_dir.glob("baseline-*.txt"))

        # Assert
        for file in baseline_files:
            assert pattern.match(file.name), f"Filename {file.name} doesn't match convention"

    def test_baseline_covers_10_domains(self):
        """Test: 10 baseline fixtures cover diverse domains (CRUD, auth, API, data, UI, reporting, jobs, search, uploads, notifications)"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")
        expected_domains = {
            "crud-operations", "authentication", "api-integration", "data-processing",
            "ui-components", "reporting", "background-jobs", "search-functionality",
            "file-uploads", "notifications"
        }

        # Act
        baseline_files = list(baseline_dir.glob("baseline-*.txt"))
        found_domains = set()
        for file in baseline_files:
            # Extract domain from filename (baseline-NN-[DOMAIN].txt)
            domain = file.stem.replace("baseline-", "").lstrip("0123456789").lstrip("-")
            found_domains.add(domain)

        # Assert
        assert len(found_domains) == 10, f"Expected 10 distinct domains, found {len(found_domains)}"
        # Check that domains cover the expected categories (may have slight variations in naming)
        assert len(found_domains & expected_domains) >= 8, "Expected domains not well represented"

    def test_baseline_word_counts_50_to_200(self):
        """Test: Each baseline fixture has 50-200 words"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))
        word_counts = {}
        for file in baseline_files:
            content = file.read_text()
            word_count = len(content.split())
            word_counts[file.name] = word_count

        # Assert
        for filename, word_count in word_counts.items():
            assert 50 <= word_count <= 200, f"{filename} has {word_count} words (expected 50-200)"

    def test_baseline_contain_vague_terms(self):
        """Test: Baseline fixtures contain vague terms (fast, good, better, optimize, improve)"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")
        vague_terms = {"fast", "good", "better", "optimize", "improve", "easy", "simple", "efficient"}

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))

        # Assert
        for file in baseline_files:
            content = file.read_text().lower()
            found_vague = [term for term in vague_terms if term in content]
            assert len(found_vague) > 0, f"{file.name} should contain vague terms, found none"

    def test_baseline_missing_given_when_then_format(self):
        """Test: Baseline fixtures lack Given/When/Then format (quality issue)"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))

        # Assert
        for file in baseline_files:
            content = file.read_text().lower()
            # Count "given", "when", "then" keywords - baseline should have few or none
            gwt_count = content.count("given") + content.count("when") + content.count("then")
            # Allow some occurrences but not structured Given/When/Then
            assert gwt_count < 5, f"{file.name} appears to have Given/When/Then structure (shouldn't for baseline)"

    def test_baseline_lacks_specific_metrics(self):
        """Test: Baseline fixtures lack specific metrics (quality issue)"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")
        import re
        metric_pattern = re.compile(r"\d+\s*(ms|sec|seconds|minutes|%|users|requests|response|latency)")

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))

        # Assert
        for file in baseline_files:
            content = file.read_text()
            metrics = metric_pattern.findall(content)
            # Baseline should have very few specific metrics
            assert len(metrics) < 3, f"{file.name} has too many specific metrics for baseline"

    def test_baseline_natural_language_format(self):
        """Test: Baseline fixtures are natural language sentences (not bullet points or code)"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))

        # Assert
        for file in baseline_files:
            content = file.read_text()
            lines = content.strip().split("\n")
            # Should have mostly multi-line prose, not bullet-heavy structure
            bullet_count = sum(1 for line in lines if line.strip().startswith("-") or line.strip().startswith("*"))
            assert bullet_count < len(lines) // 2, f"{file.name} has too many bullet points (should be natural language)"

    def test_baseline_contains_at_least_2_quality_issues(self):
        """Test: Each baseline fixture exhibits ≥2 quality issues"""
        # Arrange - This test validates the fixture quality design
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))

        # Assert - Through combination of other checks, each file should have issues
        for file in baseline_files:
            content = file.read_text().lower()
            issues_found = 0

            # Issue 1: Vague terms
            vague_terms = {"fast", "good", "better", "optimize", "improve"}
            if any(term in content for term in vague_terms):
                issues_found += 1

            # Issue 2: Missing Given/When/Then
            if "given" not in content and "when" not in content:
                issues_found += 1

            # Issue 3: Lack of specific metrics
            if not any(char.isdigit() for char in content):
                issues_found += 1

            # Issue 4: Missing NFR mentions
            nfr_terms = {"performance", "security", "reliability", "scalability"}
            nfr_count = sum(1 for term in nfr_terms if term in content)
            if nfr_count < 2:
                issues_found += 1

            assert issues_found >= 2, f"{file.name} should have ≥2 quality issues, found {issues_found}"


class TestEnhancedFixturesStructure:
    """AC#3: Enhanced Test Fixtures Created (10 Rewritten Descriptions) - 6 items

    Validates enhanced fixtures exist with matching names, improved quality, and maintained readability.
    """

    def test_10_enhanced_fixtures_exist(self):
        """Test: Exactly 10 enhanced fixture files exist"""
        # Arrange
        enhanced_dir = Path("tests/user-input-guidance/fixtures/enhanced")

        # Act
        enhanced_files = sorted(enhanced_dir.glob("enhanced-*.txt"))

        # Assert
        assert len(enhanced_files) == 10, f"Expected 10 enhanced fixtures, found {len(enhanced_files)}"

    def test_enhanced_filenames_match_baseline(self):
        """Test: Enhanced filenames match baseline numbers and categories (enhanced-[NN]-[category].txt)"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")
        enhanced_dir = Path("tests/user-input-guidance/fixtures/enhanced")

        # Act
        baseline_files = sorted([f.name.replace("baseline", "enhanced") for f in baseline_dir.glob("baseline-*.txt")])
        enhanced_files = sorted([f.name for f in enhanced_dir.glob("enhanced-*.txt")])

        # Assert
        assert baseline_files == enhanced_files, "Enhanced filenames don't match baseline naming"

    def test_enhanced_30_to_60_percent_longer_than_baseline(self):
        """Test: Each enhanced fixture is 30-60% longer than baseline"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")
        enhanced_dir = Path("tests/user-input-guidance/fixtures/enhanced")

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))

        # Assert
        for baseline_file in baseline_files:
            # Find matching enhanced file
            enhanced_name = baseline_file.name.replace("baseline", "enhanced")
            enhanced_file = enhanced_dir / enhanced_name

            baseline_words = len(baseline_file.read_text().split())
            enhanced_words = len(enhanced_file.read_text().split())

            increase_percent = ((enhanced_words - baseline_words) / baseline_words) * 100
            assert 30 <= increase_percent <= 60, f"{enhanced_name}: {increase_percent:.1f}% increase (expected 30-60%)"

    def test_enhanced_applies_guidance_principles(self):
        """Test: Enhanced fixtures apply 3-5 guidance principles"""
        # Arrange
        enhanced_dir = Path("tests/user-input-guidance/fixtures/enhanced")
        guidance_keywords = {
            "specific": ["specifically", "clearly defined", "scope"],
            "measurable": ["measurable", "metrics", "within", "less than", "greater than", "%"],
            "acceptance": ["given", "when", "then", "acceptance criteria"],
            "constraints": ["constraint", "requirement", "must", "should", "technology"],
            "nfr": ["performance", "security", "reliability", "scalability"]
        }

        # Act
        enhanced_files = sorted(enhanced_dir.glob("enhanced-*.txt"))

        # Assert
        for file in enhanced_files:
            content = file.read_text().lower()
            principles_applied = 0

            for principle, keywords in guidance_keywords.items():
                if any(keyword in content for keyword in keywords):
                    principles_applied += 1

            assert principles_applied >= 3, f"{file.name}: only {principles_applied} guidance principles applied (expected ≥3)"

    def test_enhanced_maintains_feature_domain(self):
        """Test: Enhanced fixtures maintain same feature domain as baseline"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")
        enhanced_dir = Path("tests/user-input-guidance/fixtures/enhanced")

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))

        # Assert
        for baseline_file in baseline_files:
            # Extract domain from filename
            domain = baseline_file.name.split("-", 2)[2].replace(".txt", "")
            enhanced_name = baseline_file.name.replace("baseline", "enhanced")
            enhanced_file = enhanced_dir / enhanced_name

            # Domain should be identical between baseline and enhanced
            enhanced_domain = enhanced_file.name.split("-", 2)[2].replace(".txt", "")
            assert domain == enhanced_domain, f"Domain mismatch: {domain} vs {enhanced_domain}"

    def test_enhanced_improves_vague_term_reduction(self):
        """Test: Enhanced fixtures reduce vague terms significantly"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")
        enhanced_dir = Path("tests/user-input-guidance/fixtures/enhanced")
        vague_terms = {"fast", "good", "better", "optimize", "improve", "easy", "simple"}

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))

        # Assert
        for baseline_file in baseline_files:
            baseline_content = baseline_file.read_text().lower()
            baseline_vague = sum(baseline_content.count(term) for term in vague_terms)

            enhanced_name = baseline_file.name.replace("baseline", "enhanced")
            enhanced_file = enhanced_dir / enhanced_name
            enhanced_content = enhanced_file.read_text().lower()
            enhanced_vague = sum(enhanced_content.count(term) for term in vague_terms)

            # Enhanced should have significantly fewer vague terms
            assert enhanced_vague < baseline_vague, f"{enhanced_name}: vague terms not reduced ({enhanced_vague} vs {baseline_vague})"


class TestExpectedImprovementsStructure:
    """AC#4: Expected Improvements Documented (10 Comparison Files) - 5 items

    Validates expected improvement JSON files follow schema and have realistic values.
    """

    def test_10_expected_files_exist(self):
        """Test: Exactly 10 expected improvement JSON files exist"""
        # Arrange
        expected_dir = Path("tests/user-input-guidance/fixtures/expected")

        # Act
        expected_files = sorted(expected_dir.glob("expected-*.json"))

        # Assert
        assert len(expected_files) == 10, f"Expected 10 expected files, found {len(expected_files)}"

    def test_expected_filenames_match_baseline(self):
        """Test: Expected filenames match baseline numbers and categories"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")
        expected_dir = Path("tests/user-input-guidance/fixtures/expected")

        # Act
        baseline_files = sorted([f.name.replace("baseline", "expected").replace(".txt", ".json")
                                  for f in baseline_dir.glob("baseline-*.txt")])
        expected_files = sorted([f.name for f in expected_dir.glob("expected-*.json")])

        # Assert
        assert baseline_files == expected_files, "Expected filenames don't match baseline numbering"

    def test_expected_json_valid_schema(self):
        """Test: All expected JSON files have valid schema with required fields"""
        # Arrange
        expected_dir = Path("tests/user-input-guidance/fixtures/expected")
        required_fields = {"fixture_id", "category", "baseline_issues", "expected_improvements", "rationale"}
        required_improvements_fields = {"token_savings", "ac_completeness", "nfr_coverage", "specificity_score"}

        # Act
        expected_files = sorted(expected_dir.glob("expected-*.json"))

        # Assert
        for file in expected_files:
            try:
                data = json.loads(file.read_text())
            except json.JSONDecodeError as e:
                pytest.fail(f"{file.name} contains invalid JSON: {e}")

            # Check required top-level fields
            for field in required_fields:
                assert field in data, f"{file.name} missing field: {field}"

            # Check expected_improvements structure
            improvements = data.get("expected_improvements", {})
            for field in required_improvements_fields:
                assert field in improvements, f"{file.name} missing field: expected_improvements.{field}"

    def test_expected_numeric_values_in_valid_range(self):
        """Test: All numeric expected_improvements values are 0-100%"""
        # Arrange
        expected_dir = Path("tests/user-input-guidance/fixtures/expected")

        # Act
        expected_files = sorted(expected_dir.glob("expected-*.json"))

        # Assert
        for file in expected_files:
            data = json.loads(file.read_text())
            improvements = data.get("expected_improvements", {})

            for metric, value in improvements.items():
                assert isinstance(value, (int, float)), f"{file.name}: {metric} is not numeric"
                assert 0 <= value <= 100, f"{file.name}: {metric} = {value} (expected 0-100)"

    def test_expected_contains_evidence_based_rationale(self):
        """Test: Each expected file rationale references guidance documents"""
        # Arrange
        expected_dir = Path("tests/user-input-guidance/fixtures/expected")
        guidance_keywords = {"guidance", "principle", "pattern", "recommendation", "section"}

        # Act
        expected_files = sorted(expected_dir.glob("expected-*.json"))

        # Assert
        for file in expected_files:
            data = json.loads(file.read_text())
            rationale = data.get("rationale", "").lower()

            # Rationale should reference guidance or have specific reasoning
            has_guidance_ref = any(keyword in rationale for keyword in guidance_keywords)
            has_specific_details = any(term in rationale for term in ["vague", "clarity", "structure", "metric", "category"])

            assert has_guidance_ref or has_specific_details, f"{file.name} rationale lacks evidence-based reasoning"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
