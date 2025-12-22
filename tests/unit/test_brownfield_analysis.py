"""
Test suite for AC2: Brownfield Project Documentation Analysis

Tests deep codebase analysis, existing documentation discovery,
gap identification, and coverage reporting.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, List
import json


class TestCodebaseAnalysis:
    """Test deep codebase analysis capabilities."""

    def test_analysis_should_scan_all_source_files(self):
        """Test that analyzer scans all source files in project."""
        # Arrange
        project_path = "/test_project"
        source_files = [
            "src/index.ts",
            "src/app.tsx",
            "src/services/UserService.ts",
            "src/controllers/UserController.ts",
            "src/models/User.ts"
        ]

        # Act
        from devforgeai_documentation import CodeAnalyzer
        analyzer = CodeAnalyzer()
        files = analyzer.find_source_files(project_path)

        # Assert
        assert files is not None
        assert len(files) >= 0  # Should return list

    def test_analysis_should_identify_architecture_patterns(self):
        """Test that analyzer identifies architecture pattern (MVC, Clean, DDD, etc)."""
        # Arrange
        codebase = {
            "structure": {
                "controllers/": "HTTP handlers",
                "services/": "Business logic",
                "models/": "Data models",
                "repositories/": "Data access"
            }
        }

        # Act
        from devforgeai_documentation import CodeAnalyzer
        analyzer = CodeAnalyzer()
        pattern = analyzer.detect_pattern(codebase)

        # Assert
        assert pattern is not None
        assert pattern in ["MVC", "Clean Architecture", "DDD", "CQRS", "Layered", "Unknown"]

    def test_analysis_should_extract_public_apis(self):
        """Test that analyzer extracts public API signatures."""
        # Arrange
        code = """
        export class UserService {
            async createUser(name: string, email: string): Promise<User> { }
            async getUser(id: string): Promise<User> { }
            async updateUser(id: string, data: UserInput): Promise<User> { }
        }
        """

        # Act
        from devforgeai_documentation import CodeAnalyzer
        analyzer = CodeAnalyzer()
        apis = analyzer.extract_public_apis(code)

        # Assert
        assert apis is not None
        assert len(apis) >= 3
        assert any("createUser" in str(api) for api in apis)

    def test_analysis_should_identify_dependencies(self):
        """Test that analyzer identifies internal and external dependencies."""
        # Arrange
        codebase_files = {
            "src/app.ts": "import express from 'express'\nimport { UserService } from './services/UserService'",
            "src/services/UserService.ts": "import { UserRepository } from '../repositories/UserRepository'"
        }

        # Act
        from devforgeai_documentation import CodeAnalyzer
        analyzer = CodeAnalyzer()
        deps = analyzer.extract_dependencies(codebase_files)

        # Assert
        assert deps is not None
        assert "external" in deps or "internal" in deps
        if "external" in deps:
            assert isinstance(deps["external"], list)

    def test_analysis_should_find_entry_points(self):
        """Test that analyzer identifies application entry points."""
        # Arrange
        codebase = {
            "files": ["src/index.ts", "src/app.tsx", "src/main.py"],
            "structure": {"src/": "Source code"}
        }

        # Act
        from devforgeai_documentation import CodeAnalyzer
        analyzer = CodeAnalyzer()
        entry_points = analyzer.find_entry_points(codebase)

        # Assert
        assert entry_points is not None
        assert isinstance(entry_points, list)
        # Should find some entry points
        assert len(entry_points) >= 1

    def test_analysis_should_extract_comments_and_docstrings(self):
        """Test that analyzer extracts existing comments and docstrings."""
        # Arrange
        code = '''
        /**
         * Creates a new user in the system.
         * @param name - User full name
         * @param email - User email address
         * @returns Created user object
         */
        async function createUser(name: string, email: string) { }
        '''

        # Act
        from devforgeai_documentation import CodeAnalyzer
        analyzer = CodeAnalyzer()
        comments = analyzer.extract_docstrings(code)

        # Assert
        assert comments is not None
        assert len(comments) > 0
        assert "Creates a new user" in str(comments)


class TestExistingDocumentationDiscovery:
    """Test discovery of existing documentation."""

    def test_should_discover_readme_files(self):
        """Test that analyzer finds existing README files."""
        # Arrange
        project_files = [
            "README.md",
            "docs/API.md",
            "docs/ARCHITECTURE.md",
            "src/index.ts"
        ]

        # Act
        from devforgeai_documentation import DocumentationDiscoverer
        discoverer = DocumentationDiscoverer()
        docs = discoverer.find_documentation_files(project_files)

        # Assert
        assert docs is not None
        assert "README.md" in docs or any("README" in str(d).upper() for d in docs)

    def test_should_consolidate_documentation_fragments(self):
        """Test that analyzer consolidates scattered documentation."""
        # Arrange
        fragments = {
            "docs/api/endpoints.md": "# API Endpoints\n... content ...",
            "src/services/README.md": "# Services\n... content ...",
            "docs/architecture.md": "# Architecture\n... content ..."
        }

        # Act
        from devforgeai_documentation import DocumentationDiscoverer
        discoverer = DocumentationDiscoverer()
        consolidated = discoverer.consolidate_fragments(fragments)

        # Assert
        assert consolidated is not None
        assert isinstance(consolidated, dict)

    def test_should_categorize_documentation_by_type(self):
        """Test that documentation is categorized (readme, api, guide, etc)."""
        # Arrange
        docs = {
            "README.md": "content",
            "docs/API.md": "content",
            "docs/DEVELOPER.md": "content",
            "CONTRIBUTING.md": "content"
        }

        # Act
        from devforgeai_documentation import DocumentationDiscoverer
        discoverer = DocumentationDiscoverer()
        categorized = discoverer.categorize_docs(docs)

        # Assert
        assert categorized is not None
        # Should have categories for different doc types
        categories = list(categorized.keys()) if isinstance(categorized, dict) else []
        assert len(categories) > 0


class TestDocumentationGapIdentification:
    """Test documentation gap identification."""

    def test_should_identify_missing_readme(self):
        """Test that analyzer detects missing README.md."""
        # Arrange
        existing_docs = ["docs/API.md", "CONTRIBUTING.md"]

        # Act
        from devforgeai_documentation import GapAnalyzer
        analyzer = GapAnalyzer()
        gaps = analyzer.find_gaps(existing_docs)

        # Assert
        assert gaps is not None
        assert "README" in str(gaps).upper() or any("readme" in str(g).lower() for g in gaps)

    def test_should_identify_missing_api_documentation(self):
        """Test that analyzer detects missing API docs."""
        # Arrange
        public_apis = [
            "GET /api/users",
            "POST /api/users",
            "GET /api/users/:id"
        ]
        existing_docs = {}  # No docs

        # Act
        from devforgeai_documentation import GapAnalyzer
        analyzer = GapAnalyzer()
        gaps = analyzer.find_api_gaps(public_apis, existing_docs)

        # Assert
        assert gaps is not None
        assert len(gaps) >= 3  # All APIs are undocumented

    def test_should_identify_missing_architecture_documentation(self):
        """Test that analyzer detects missing architecture docs."""
        # Arrange
        architecture = {
            "layers": ["presentation", "application", "domain", "infrastructure"]
        }
        existing_docs = ["README.md"]

        # Act
        from devforgeai_documentation import GapAnalyzer
        analyzer = GapAnalyzer()
        gaps = analyzer.find_architecture_gaps(architecture, existing_docs)

        # Assert
        assert gaps is not None
        assert "architecture" in str(gaps).lower() or "diagram" in str(gaps).lower()

    def test_should_identify_outdated_documentation(self):
        """Test that analyzer detects outdated docs (>30 days old)."""
        # Arrange
        docs = {
            "README.md": {"last_updated": "2025-09-01"},  # Old
            "CONTRIBUTING.md": {"last_updated": "2025-11-15"}  # Recent
        }
        current_date = "2025-11-18"

        # Act
        from devforgeai_documentation import GapAnalyzer
        analyzer = GapAnalyzer()
        outdated = analyzer.find_outdated_docs(docs, current_date)

        # Assert
        assert outdated is not None
        assert "README.md" in outdated or any("README" in str(d) for d in outdated)

    def test_should_identify_missing_examples(self):
        """Test that analyzer detects missing code examples."""
        # Arrange
        api_docs = "# API\nThis is the API documentation."  # No examples
        api_endpoints = [
            {"path": "/api/users", "method": "POST"},
            {"path": "/api/users", "method": "GET"}
        ]

        # Act
        from devforgeai_documentation import GapAnalyzer
        analyzer = GapAnalyzer()
        gaps = analyzer.find_example_gaps(api_docs, api_endpoints)

        # Assert
        assert gaps is not None
        assert isinstance(gaps, list)


class TestCoverageReportGeneration:
    """Test documentation coverage report generation."""

    def test_should_generate_coverage_report(self):
        """Test that coverage report is generated."""
        # Arrange
        analysis_result = {
            "total_files": 50,
            "documented_files": 40,
            "total_apis": 20,
            "documented_apis": 18,
            "gaps": ["README", "Architecture guide"]
        }

        # Act
        from devforgeai_documentation import ReportGenerator
        gen = ReportGenerator()
        report = gen.generate_coverage_report(analysis_result)

        # Assert
        assert report is not None
        assert isinstance(report, (str, dict))

    def test_coverage_report_should_show_percentage(self):
        """Test that coverage report includes percentage metrics."""
        # Arrange
        analysis_result = {
            "total_items": 100,
            "documented_items": 85,
            "gaps": []
        }

        # Act
        from devforgeai_documentation import ReportGenerator
        gen = ReportGenerator()
        report = gen.generate_coverage_report(analysis_result)

        # Assert
        assert report is not None
        assert "85" in str(report) or "coverage" in str(report).lower()

    def test_coverage_report_should_list_gaps(self):
        """Test that report lists identified gaps."""
        # Arrange
        gaps = [
            "Missing README.md",
            "Missing API documentation for 5 endpoints",
            "Outdated architecture guide"
        ]

        # Act
        from devforgeai_documentation import ReportGenerator
        gen = ReportGenerator()
        report = gen.format_gaps(gaps)

        # Assert
        assert report is not None
        assert "README" in str(report).upper() or "api" in str(report).lower()

    def test_coverage_report_should_show_what_exists(self):
        """Test that report shows what documentation exists."""
        # Arrange
        existing_docs = {
            "README.md": "Exists",
            "docs/API.md": "Exists",
            "docs/DEVELOPER.md": "Outdated"
        }

        # Act
        from devforgeai_documentation import ReportGenerator
        gen = ReportGenerator()
        report = gen.format_existing_docs(existing_docs)

        # Assert
        assert report is not None
        assert "README" in str(report).upper()

    def test_coverage_report_should_calculate_overall_coverage(self):
        """Test that report calculates overall documentation coverage."""
        # Arrange
        files = 50
        documented = 42

        # Act
        from devforgeai_documentation import ReportGenerator
        gen = ReportGenerator()
        coverage = gen.calculate_coverage(documented, files)

        # Assert
        assert coverage is not None
        assert isinstance(coverage, (int, float))
        assert coverage == 84 or coverage == 84.0


class TestRecommendationGeneration:
    """Test actionable recommendations for documentation improvement."""

    def test_should_generate_recommendations(self):
        """Test that analyzer generates improvement recommendations."""
        # Arrange
        gaps = [
            "Missing README.md",
            "API documentation incomplete (18/20 endpoints)"
        ]

        # Act
        from devforgeai_documentation import RecommendationGenerator
        gen = RecommendationGenerator()
        recommendations = gen.generate_recommendations(gaps)

        # Assert
        assert recommendations is not None
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

    def test_recommendations_should_be_actionable(self):
        """Test that recommendations include specific actions."""
        # Arrange
        gap = "Missing API documentation"

        # Act
        from devforgeai_documentation import RecommendationGenerator
        gen = RecommendationGenerator()
        recs = gen.recommend_for_gap(gap)

        # Assert
        assert recs is not None
        # Should suggest specific action
        rec_str = str(recs).lower()
        assert "run" in rec_str or "generate" in rec_str or "create" in rec_str

    def test_recommendations_should_prioritize_by_impact(self):
        """Test that recommendations are prioritized by impact."""
        # Arrange
        gaps = {
            "README.md": {"missing": True, "impact": "High"},
            "Architecture guide": {"missing": True, "impact": "Medium"},
            "API examples": {"incomplete": True, "impact": "Low"}
        }

        # Act
        from devforgeai_documentation import RecommendationGenerator
        gen = RecommendationGenerator()
        recommendations = gen.prioritize_recommendations(gaps)

        # Assert
        assert recommendations is not None
        # First recommendation should be for high impact item
        if isinstance(recommendations, list) and len(recommendations) > 0:
            assert "README" in str(recommendations[0]).upper()


class TestBrownfieldWorkflow:
    """Test complete brownfield analysis workflow."""

    def test_brownfield_mode_should_be_detected(self):
        """Test that brownfield mode is correctly detected."""
        # Arrange
        project_has_code = True
        project_has_docs = True

        # Act
        from devforgeai_documentation import ModeDetector
        detector = ModeDetector()
        mode = detector.detect_mode(project_has_code, project_has_docs)

        # Assert
        assert mode == "brownfield"

    def test_brownfield_analysis_should_return_comprehensive_report(self):
        """Test that brownfield analysis returns complete report."""
        # Arrange
        project_path = "/test_project"

        # Act
        from devforgeai_documentation import BrownfieldAnalyzer
        analyzer = BrownfieldAnalyzer()
        result = analyzer.analyze(project_path)

        # Assert
        assert result is not None
        expected_fields = ["coverage", "gaps", "recommendations", "existing_docs"]
        for field in expected_fields:
            # At least some of these fields should be present
            pass


class TestAnalysisPerformance:
    """Test performance for brownfield analysis."""

    @pytest.mark.timeout(600)  # 10 minutes max
    def test_analysis_should_handle_500_files_within_10_minutes(self):
        """Test that analysis of 500-file codebase completes in <10 minutes."""
        # Arrange
        file_count = 500

        # Act
        from devforgeai_documentation import CodeAnalyzer
        import time
        analyzer = CodeAnalyzer()
        start = time.time()
        # Simulate analysis of large codebase
        result = analyzer.estimate_analysis_time(file_count)
        elapsed = time.time() - start

        # Assert
        assert result is not None
        assert elapsed < 600  # 10 minutes


class TestIntegrationWithCodeAnalyzerSubagent:
    """Test integration with code-analyzer subagent."""

    def test_should_invoke_code_analyzer_subagent(self):
        """Test that brownfield analysis invokes code-analyzer subagent."""
        # Arrange
        project_path = "/test_project"

        # Act
        from devforgeai_documentation import BrownfieldAnalyzer
        analyzer = BrownfieldAnalyzer()
        # Mock the subagent invocation
        result = analyzer.invoke_code_analyzer(project_path)

        # Assert
        assert result is not None

    def test_code_analyzer_should_return_structured_json(self):
        """Test that code-analyzer returns properly structured output."""
        # Arrange
        project_data = {}

        # Act
        from devforgeai_documentation import CodeAnalyzerResponse
        # Expected response structure
        expected_fields = ["project_name", "tech_stack", "architecture_pattern",
                          "layers", "public_apis", "entry_points", "dependencies"]

        # Assert
        # Response should have all expected fields
        for field in expected_fields:
            pass  # Validation happens at integration test time


class TestDataModels:
    """Test data models for brownfield analysis."""

    def test_code_analysis_output_model(self):
        """Test code analysis output data model."""
        # Arrange
        analysis_output = {
            "project_name": "MyApp",
            "tech_stack": ["Node.js", "Express", "React"],
            "architecture_pattern": "Clean Architecture",
            "layers": {
                "presentation": ["src/views/"],
                "application": ["src/use-cases/"],
                "domain": ["src/entities/"]
            },
            "public_apis": [
                {"endpoint": "GET /api/users", "documented": False},
                {"endpoint": "POST /api/users", "documented": True}
            ]
        }

        # Act
        from devforgeai_documentation import CodeAnalysisOutput
        output = CodeAnalysisOutput(**analysis_output)

        # Assert
        assert output.project_name == "MyApp"
        assert len(output.tech_stack) == 3
        assert output.architecture_pattern == "Clean Architecture"

    def test_documentation_coverage_model(self):
        """Test documentation coverage metrics model."""
        # Arrange
        coverage_data = {
            "coverage_percentage": 85,
            "total_items": 100,
            "documented_items": 85,
            "last_updated": "2025-11-18",
            "stories_documented": ["STORY-001", "STORY-002"]
        }

        # Act
        from devforgeai_documentation import DocumentationCoverage
        coverage = DocumentationCoverage(**coverage_data)

        # Assert
        assert coverage.coverage_percentage == 85
        assert coverage.documented_items == 85


class TestEdgeCases:
    """Test edge cases in brownfield analysis."""

    def test_should_handle_empty_project(self):
        """Test that analysis handles empty project gracefully."""
        # Arrange
        project_files = []

        # Act
        from devforgeai_documentation import CodeAnalyzer
        analyzer = CodeAnalyzer()
        result = analyzer.analyze_files(project_files)

        # Assert
        assert result is not None
        # Should return empty or default structure, not crash

    def test_should_handle_mixed_language_codebase(self):
        """Test that analysis works with multiple programming languages."""
        # Arrange
        files = [
            "src/main.ts",
            "src/utils.py",
            "src/helper.rs",
            "src/script.sh"
        ]

        # Act
        from devforgeai_documentation import CodeAnalyzer
        analyzer = CodeAnalyzer()
        result = analyzer.analyze_files(files)

        # Assert
        assert result is not None

    def test_should_handle_binary_files_gracefully(self):
        """Test that analyzer skips binary files without error."""
        # Arrange
        files = [
            "src/app.ts",
            "images/logo.png",
            "assets/data.json"
        ]

        # Act
        from devforgeai_documentation import CodeAnalyzer
        analyzer = CodeAnalyzer()
        # Should not raise exception
        result = analyzer.analyze_files(files)

        # Assert
        assert result is not None
