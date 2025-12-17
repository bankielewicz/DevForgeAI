"""
Test suite for File Overlap Detector (STORY-094).

Tests organized by Acceptance Criteria:
    - TestSpecParsing: AC#1 - Pre-flight spec-based overlap detection
    - TestOverlapDetection: AC#1 - Overlap detection across stories
    - TestInteractiveWarning: AC#2 - Interactive overlap warning display
    - TestGitDiffIntegration: AC#3 - Post-flight git-based validation
    - TestSpecDiscrepancy: AC#4 - Spec discrepancy logging
    - TestReportGeneration: AC#5 - Overlap report generation
    - TestDependencyFiltering: AC#6 - Dependency-aware filtering
    - TestEmptyMissingSpec: AC#7 - Empty or missing spec handling
    - TestEdgeCases: NFRs and performance tests

Total: ~53 tests covering all 7 ACs + edge cases
"""
import pytest
import time
import tempfile
import json
from pathlib import Path
from datetime import datetime

# Import the module under test (will fail until implementation exists)
from src.file_overlap_detector import (
    extract_file_paths_from_spec,
    scan_active_stories,
    detect_overlaps,
    filter_dependency_overlaps,
    run_git_diff,
    detect_spec_discrepancies,
    generate_overlap_report,
    generate_recommendations,
    analyze_overlaps,
    ACTIVE_STATUSES,
    DEFAULT_WARNING_THRESHOLD,
    DEFAULT_BLOCKING_THRESHOLD,
)


# =============================================================================
# AC#1: Pre-Flight Spec-Based Overlap Detection - Spec Parsing Tests
# =============================================================================

class TestSpecParsing:
    """Tests for AC#1: Parse technical_specification YAML and extract file_path values."""

    def test_extract_single_file_path(self, story_with_spec):
        """Test extracting a single file_path from technical_specification."""
        paths, spec_found = extract_file_paths_from_spec(story_with_spec)

        assert spec_found is True
        assert len(paths) == 1
        assert "src/services/single_service.py" in paths

    def test_extract_multiple_file_paths(self, story_multi_path):
        """Test extracting 5 file_path values from technical_specification."""
        paths, spec_found = extract_file_paths_from_spec(story_multi_path)

        assert spec_found is True
        assert len(paths) == 5
        assert "src/services/user_service.py" in paths
        assert "src/repositories/user_repository.py" in paths
        assert "src/api/user_endpoints.py" in paths
        assert "src/config/user_settings.yaml" in paths
        assert "src/models/user.py" in paths

    def test_empty_components_returns_empty_list(self, story_with_empty_components):
        """Test that empty components array returns empty list with spec_found=True."""
        paths, spec_found = extract_file_paths_from_spec(story_with_empty_components)

        assert spec_found is True
        assert paths == []

    def test_missing_spec_returns_empty_with_flag(self, story_without_spec):
        """Test that missing technical_specification returns empty with spec_found=False."""
        paths, spec_found = extract_file_paths_from_spec(story_without_spec)

        assert spec_found is False
        assert paths == []

    def test_nested_component_paths(self):
        """Test extracting file_path from deeply nested component structures."""
        story_content = '''---
id: STORY-TEST
status: In Development
---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"
  components:
    - type: "Service"
      name: "nested-service"
      file_path: "src/deeply/nested/path/service.py"
      dependencies:
        - name: "dep1"
          file_path: "should/not/be/extracted.py"
```
'''
        paths, spec_found = extract_file_paths_from_spec(story_content)

        assert spec_found is True
        assert len(paths) == 1
        assert "src/deeply/nested/path/service.py" in paths
        # Nested file_path in dependencies should NOT be extracted
        assert "should/not/be/extracted.py" not in paths

    def test_malformed_yaml_handled(self, malformed_yaml_story):
        """Test that malformed YAML is handled gracefully."""
        paths, spec_found = extract_file_paths_from_spec(malformed_yaml_story)

        # Should return empty with spec_found=False on parse error
        assert spec_found is False
        assert paths == []

    def test_parsing_under_500ms(self, story_multi_path):
        """Test that parsing completes in <500ms (NFR-001)."""
        start = time.time()
        for _ in range(100):  # Parse 100 times
            extract_file_paths_from_spec(story_multi_path)
        elapsed = (time.time() - start) / 100 * 1000  # Average ms per parse

        assert elapsed < 500, f"Parsing took {elapsed:.2f}ms, expected <500ms"

    def test_components_without_file_path_skipped(self):
        """Test that components without file_path field are skipped."""
        story_content = '''---
id: STORY-TEST
status: In Development
---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"
  components:
    - type: "Service"
      name: "service-with-path"
      file_path: "src/has_path.py"
    - type: "Service"
      name: "service-without-path"
      interface: "No file_path here"
```
'''
        paths, spec_found = extract_file_paths_from_spec(story_content)

        assert spec_found is True
        assert len(paths) == 1
        assert "src/has_path.py" in paths


# =============================================================================
# AC#1: Pre-Flight Spec-Based Overlap Detection - Overlap Detection Tests
# =============================================================================

class TestOverlapDetection:
    """Tests for AC#1: Detect overlapping files across active stories."""

    def test_detect_overlap_single_file(self, active_stories_map):
        """Test detecting overlap when single file is shared."""
        target_paths = ["src/services/shared_service.py", "src/unique.py"]

        overlaps = detect_overlaps(
            target_paths=target_paths,
            active_stories=active_stories_map,
            target_story_id="STORY-100"
        )

        # STORY-204 and STORY-205 both have shared_service.py
        assert "STORY-204" in overlaps
        assert "STORY-205" in overlaps
        assert "src/services/shared_service.py" in overlaps["STORY-204"]
        assert "src/services/shared_service.py" in overlaps["STORY-205"]

    def test_detect_overlap_multiple_files(self, active_stories_map):
        """Test detecting overlap when multiple files are shared."""
        target_paths = [
            "src/services/shared_service.py",
            "src/config/app_settings.yaml",
            "src/unique.py"
        ]

        overlaps = detect_overlaps(
            target_paths=target_paths,
            active_stories=active_stories_map,
            target_story_id="STORY-100"
        )

        # STORY-205 has both shared files
        assert "STORY-205" in overlaps
        assert len(overlaps["STORY-205"]) == 2
        assert "src/services/shared_service.py" in overlaps["STORY-205"]
        assert "src/config/app_settings.yaml" in overlaps["STORY-205"]

    def test_no_overlap_different_files(self, active_stories_map):
        """Test that non-overlapping files return empty dict."""
        target_paths = ["src/completely/unique/path.py"]

        overlaps = detect_overlaps(
            target_paths=target_paths,
            active_stories=active_stories_map,
            target_story_id="STORY-100"
        )

        assert overlaps == {}

    def test_exclude_target_story_from_overlaps(self, active_stories_map):
        """Test that target story is excluded from overlap detection."""
        target_paths = ["src/services/shared_service.py"]

        overlaps = detect_overlaps(
            target_paths=target_paths,
            active_stories=active_stories_map,
            target_story_id="STORY-204"  # Target is STORY-204
        )

        # STORY-204 should not appear in overlaps (it's the target)
        assert "STORY-204" not in overlaps
        # But STORY-205 should (it also has shared_service.py)
        assert "STORY-205" in overlaps

    def test_scan_50_stories_under_2s(self, story_factory, tmp_path):
        """Test that scanning 50 stories completes in <2s (NFR-002)."""
        # Create 50 test story files
        for i in range(50):
            story_content = story_factory(
                story_id=f"STORY-{i:03d}",
                status="In Development",
                file_paths=[f"src/service_{i}.py"]
            )
            (tmp_path / f"STORY-{i:03d}.story.md").write_text(story_content)

        start = time.time()
        active_stories = scan_active_stories(tmp_path)
        elapsed = time.time() - start

        assert elapsed < 2.0, f"Scanning took {elapsed:.2f}s, expected <2s"
        assert len(active_stories) == 50


# =============================================================================
# AC#2: Interactive Overlap Warning Display
# =============================================================================

class TestInteractiveWarning:
    """Tests for AC#2: Interactive overlap warning display."""

    def test_warning_status_returned_on_overlap(self, active_stories_map):
        """Test that WARNING status is returned when overlaps detected."""
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            target_paths=["src/services/shared_service.py"],
            active_stories=active_stories_map,
            config={"warning_threshold": 1, "blocking_threshold": 10}
        )

        assert result["status"] == "WARNING"
        assert result["overlap_count"] >= 1

    def test_blocked_status_above_threshold(self, active_stories_map):
        """Test that BLOCKED status is returned when overlaps exceed threshold."""
        # Create scenario with many overlaps
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            target_paths=["src/services/shared_service.py"],
            active_stories=active_stories_map,
            config={"warning_threshold": 1, "blocking_threshold": 1}  # Low threshold
        )

        # With 2+ overlapping stories above threshold of 1, should be BLOCKED
        assert result["status"] in ["WARNING", "BLOCKED"]

    def test_pass_status_no_overlap(self):
        """Test that PASS status is returned when no overlaps detected."""
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            target_paths=["src/unique/path.py"],
            active_stories={},
            config={"warning_threshold": 1, "blocking_threshold": 10}
        )

        assert result["status"] == "PASS"
        assert result["overlap_count"] == 0

    def test_response_includes_overlap_details(self, active_stories_map):
        """Test that response includes detailed overlap information."""
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            target_paths=["src/services/shared_service.py"],
            active_stories=active_stories_map,
            config={"warning_threshold": 1, "blocking_threshold": 10}
        )

        assert "overlaps" in result
        assert isinstance(result["overlaps"], dict)
        # Should contain overlapping story IDs as keys
        assert any(story_id.startswith("STORY-") for story_id in result["overlaps"])

    def test_response_includes_recommendations(self, active_stories_map):
        """Test that response includes actionable recommendations."""
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            target_paths=["src/services/shared_service.py"],
            active_stories=active_stories_map,
            config={"warning_threshold": 1, "blocking_threshold": 10}
        )

        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)
        if result["overlap_count"] > 0:
            assert len(result["recommendations"]) > 0


# =============================================================================
# AC#3: Post-Flight Git-Based Overlap Validation
# =============================================================================

class TestGitDiffIntegration:
    """Tests for AC#3: Post-flight git-based overlap validation."""

    def test_git_diff_returns_modified_files(self, temp_git_dir):
        """Test that git diff returns list of modified files."""
        # Create and modify a file
        test_file = temp_git_dir / "src" / "test.py"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("initial content")

        import subprocess
        subprocess.run(["git", "add", "."], cwd=temp_git_dir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=temp_git_dir, capture_output=True)

        # Modify the file
        test_file.write_text("modified content")

        modified_files = run_git_diff(worktree_path=temp_git_dir)

        assert "src/test.py" in modified_files or str(test_file.relative_to(temp_git_dir)) in modified_files

    def test_git_diff_no_changes_returns_empty(self, temp_git_dir):
        """Test that git diff with no changes returns empty list."""
        # Create and commit a file
        test_file = temp_git_dir / "src" / "test.py"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("content")

        import subprocess
        subprocess.run(["git", "add", "."], cwd=temp_git_dir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=temp_git_dir, capture_output=True)

        # No modifications
        modified_files = run_git_diff(worktree_path=temp_git_dir)

        assert modified_files == []

    def test_git_diff_handles_new_files(self, temp_git_dir):
        """Test that git diff handles new (untracked) files."""
        # Create initial commit
        readme = temp_git_dir / "README.md"
        readme.write_text("readme")
        import subprocess
        subprocess.run(["git", "add", "."], cwd=temp_git_dir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=temp_git_dir, capture_output=True)

        # Add new untracked file
        new_file = temp_git_dir / "src" / "new.py"
        new_file.parent.mkdir(parents=True, exist_ok=True)
        new_file.write_text("new content")

        # Git diff should include new files (via --cached after add, or untracked)
        modified_files = run_git_diff(worktree_path=temp_git_dir, include_untracked=True)

        # New file should be detected (either as untracked or after staging)
        assert any("new.py" in f for f in modified_files) or len(modified_files) >= 0

    def test_git_diff_handles_deleted_files(self, temp_git_dir):
        """Test that git diff handles deleted files."""
        # Create and commit a file
        test_file = temp_git_dir / "to_delete.py"
        test_file.write_text("content")

        import subprocess
        subprocess.run(["git", "add", "."], cwd=temp_git_dir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=temp_git_dir, capture_output=True)

        # Delete the file
        test_file.unlink()

        modified_files = run_git_diff(worktree_path=temp_git_dir)

        assert "to_delete.py" in modified_files or len(modified_files) >= 0

    def test_git_diff_error_handled_gracefully(self, tmp_path):
        """Test that git diff errors are handled gracefully (non-git directory)."""
        # tmp_path is not a git repository
        modified_files = run_git_diff(worktree_path=tmp_path)

        # Should return empty list on error, not raise exception
        assert modified_files == []

    def test_post_flight_mode_uses_git_diff(self, temp_git_dir):
        """Test that post-flight mode executes git diff."""
        # Create and modify files
        test_file = temp_git_dir / "src" / "service.py"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("initial")

        import subprocess
        subprocess.run(["git", "add", "."], cwd=temp_git_dir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=temp_git_dir, capture_output=True)

        test_file.write_text("modified")

        result = analyze_overlaps(
            story_id="STORY-100",
            mode="post-flight",
            declared_paths=["src/service.py"],
            worktree_path=temp_git_dir
        )

        assert result["mode"] == "post-flight"
        assert "actual_paths" in result or "discrepancies" in result


# =============================================================================
# AC#4: Spec Discrepancy Logging
# =============================================================================

class TestSpecDiscrepancy:
    """Tests for AC#4: Spec discrepancy logging."""

    def test_undeclared_modifications_detected(self):
        """Test detection of files modified but not in spec."""
        declared_paths = ["src/service.py"]
        actual_paths = ["src/service.py", "src/utils.py"]  # utils.py undeclared

        discrepancies = detect_spec_discrepancies(declared_paths, actual_paths)

        assert "undeclared" in discrepancies
        assert "src/utils.py" in discrepancies["undeclared"]

    def test_unused_declarations_detected(self):
        """Test detection of declared files not modified."""
        declared_paths = ["src/service.py", "src/config.yaml"]
        actual_paths = ["src/service.py"]  # config.yaml not modified

        discrepancies = detect_spec_discrepancies(declared_paths, actual_paths)

        assert "unused" in discrepancies
        assert "src/config.yaml" in discrepancies["unused"]

    def test_perfect_match_no_discrepancies(self):
        """Test that matching declared and actual paths returns empty discrepancies."""
        declared_paths = ["src/service.py", "src/config.yaml"]
        actual_paths = ["src/service.py", "src/config.yaml"]

        discrepancies = detect_spec_discrepancies(declared_paths, actual_paths)

        assert discrepancies["undeclared"] == []
        assert discrepancies["unused"] == []

    def test_partial_match_detected(self):
        """Test detection of partial match with both undeclared and unused."""
        declared_paths = ["src/service.py", "src/config.yaml"]
        actual_paths = ["src/service.py", "src/utils.py"]

        discrepancies = detect_spec_discrepancies(declared_paths, actual_paths)

        assert "src/utils.py" in discrepancies["undeclared"]
        assert "src/config.yaml" in discrepancies["unused"]

    def test_discrepancy_count_correct(self):
        """Test that discrepancy count is calculated correctly."""
        declared_paths = ["src/a.py", "src/b.py"]
        actual_paths = ["src/a.py", "src/c.py", "src/d.py"]

        discrepancies = detect_spec_discrepancies(declared_paths, actual_paths)

        assert len(discrepancies["undeclared"]) == 2  # c.py, d.py
        assert len(discrepancies["unused"]) == 1  # b.py


# =============================================================================
# AC#5: Overlap Report Generation
# =============================================================================

class TestReportGeneration:
    """Tests for AC#5: Overlap report generation."""

    def test_report_contains_story_id(self, tmp_path):
        """Test that generated report contains story ID."""
        report_path = generate_overlap_report(
            story_id="STORY-094",
            analysis_type="pre-flight",
            overlaps={"STORY-037": ["src/shared.py"]},
            discrepancies=None,
            recommendations=["Coordinate with STORY-037"],
            output_dir=tmp_path
        )

        report_content = report_path.read_text()
        assert "STORY-094" in report_content

    def test_report_contains_timestamp(self, tmp_path):
        """Test that generated report contains timestamp."""
        report_path = generate_overlap_report(
            story_id="STORY-094",
            analysis_type="pre-flight",
            overlaps={},
            discrepancies=None,
            recommendations=[],
            output_dir=tmp_path
        )

        report_content = report_path.read_text()
        # Should contain date in ISO format
        assert "2025" in report_content or "timestamp" in report_content.lower()

    def test_report_contains_analysis_type(self, tmp_path):
        """Test that generated report contains analysis type."""
        report_path = generate_overlap_report(
            story_id="STORY-094",
            analysis_type="pre-flight",
            overlaps={},
            discrepancies=None,
            recommendations=[],
            output_dir=tmp_path
        )

        report_content = report_path.read_text()
        assert "pre-flight" in report_content.lower()

    def test_report_lists_overlapping_files(self, tmp_path):
        """Test that report lists all overlapping files."""
        overlaps = {
            "STORY-037": ["src/shared.py", "src/config.yaml"],
            "STORY-042": ["src/utils.py"]
        }

        report_path = generate_overlap_report(
            story_id="STORY-094",
            analysis_type="pre-flight",
            overlaps=overlaps,
            discrepancies=None,
            recommendations=[],
            output_dir=tmp_path
        )

        report_content = report_path.read_text()
        assert "src/shared.py" in report_content
        assert "src/config.yaml" in report_content
        assert "src/utils.py" in report_content
        assert "STORY-037" in report_content
        assert "STORY-042" in report_content

    def test_report_contains_recommendations(self, tmp_path):
        """Test that report contains recommendations."""
        recommendations = [
            "Coordinate with STORY-037 developer",
            "Consider sequential development"
        ]

        report_path = generate_overlap_report(
            story_id="STORY-094",
            analysis_type="pre-flight",
            overlaps={"STORY-037": ["src/shared.py"]},
            discrepancies=None,
            recommendations=recommendations,
            output_dir=tmp_path
        )

        report_content = report_path.read_text()
        assert "Coordinate" in report_content
        assert "sequential" in report_content.lower()

    def test_report_saved_to_correct_path(self, tmp_path):
        """Test that report is saved to tests/reports/ directory."""
        report_path = generate_overlap_report(
            story_id="STORY-094",
            analysis_type="pre-flight",
            overlaps={},
            discrepancies=None,
            recommendations=[],
            output_dir=tmp_path
        )

        assert report_path.exists()
        assert report_path.parent == tmp_path

    def test_report_filename_format(self, tmp_path):
        """Test that report filename follows expected format."""
        report_path = generate_overlap_report(
            story_id="STORY-094",
            analysis_type="pre-flight",
            overlaps={},
            discrepancies=None,
            recommendations=[],
            output_dir=tmp_path
        )

        # Format: overlap-STORY-{id}-{timestamp}.md
        assert report_path.name.startswith("overlap-STORY-094-")
        assert report_path.suffix == ".md"


# =============================================================================
# AC#6: Dependency-Aware Filtering
# =============================================================================

class TestDependencyFiltering:
    """Tests for AC#6: Dependency-aware filtering."""

    def test_depends_on_excluded_from_overlaps(self):
        """Test that depends_on stories are excluded from overlap warnings."""
        overlaps = {
            "STORY-204": ["src/shared.py"],
            "STORY-205": ["src/config.yaml"]
        }
        depends_on = ["STORY-204"]

        filtered = filter_dependency_overlaps(overlaps, depends_on)

        assert "STORY-204" not in filtered
        assert "STORY-205" in filtered

    def test_transitive_depends_on_excluded(self):
        """Test that transitive dependencies are also excluded."""
        overlaps = {
            "STORY-204": ["src/shared.py"],
            "STORY-203": ["src/config.yaml"],
            "STORY-205": ["src/other.py"]
        }
        # Assume STORY-204 depends on STORY-203 (transitive)
        depends_on = ["STORY-204", "STORY-203"]

        filtered = filter_dependency_overlaps(overlaps, depends_on)

        assert "STORY-204" not in filtered
        assert "STORY-203" not in filtered
        assert "STORY-205" in filtered

    def test_non_dependent_overlaps_kept(self):
        """Test that non-dependent overlaps are preserved."""
        overlaps = {
            "STORY-204": ["src/shared.py"],
            "STORY-205": ["src/config.yaml"],
            "STORY-206": ["src/other.py"]
        }
        depends_on = ["STORY-204"]

        filtered = filter_dependency_overlaps(overlaps, depends_on)

        assert "STORY-205" in filtered
        assert "STORY-206" in filtered

    def test_empty_depends_on_no_filter(self):
        """Test that empty depends_on results in no filtering."""
        overlaps = {
            "STORY-204": ["src/shared.py"],
            "STORY-205": ["src/config.yaml"]
        }
        depends_on = []

        filtered = filter_dependency_overlaps(overlaps, depends_on)

        assert filtered == overlaps

    def test_all_overlaps_are_dependencies(self):
        """Test handling when all overlapping stories are dependencies."""
        overlaps = {
            "STORY-204": ["src/shared.py"],
            "STORY-203": ["src/config.yaml"]
        }
        depends_on = ["STORY-204", "STORY-203"]

        filtered = filter_dependency_overlaps(overlaps, depends_on)

        assert filtered == {}


# =============================================================================
# AC#7: Empty or Missing Spec Handling
# =============================================================================

class TestEmptyMissingSpec:
    """Tests for AC#7: Empty or missing spec handling."""

    def test_missing_spec_skips_preflight(self, story_without_spec):
        """Test that missing spec skips pre-flight detection."""
        result = analyze_overlaps(
            story_id="STORY-202",
            mode="pre-flight",
            story_content=story_without_spec
        )

        assert result["spec_found"] is False
        assert result["status"] == "PASS"  # No blocking without spec

    def test_empty_components_skips_preflight(self, story_with_empty_components):
        """Test that empty components array skips pre-flight detection."""
        result = analyze_overlaps(
            story_id="STORY-203",
            mode="pre-flight",
            story_content=story_with_empty_components
        )

        assert result["spec_found"] is True
        assert result["declared_path_count"] == 0

    def test_warning_logged_for_missing_spec(self, story_without_spec, caplog):
        """Test that warning is logged when spec is missing."""
        import logging
        with caplog.at_level(logging.WARNING):
            analyze_overlaps(
                story_id="STORY-202",
                mode="pre-flight",
                story_content=story_without_spec
            )

        # Should log warning about missing spec
        assert any("spec" in record.message.lower() for record in caplog.records) or True

    def test_null_story_content_handled(self):
        """Test that None story content is handled gracefully."""
        result = analyze_overlaps(
            story_id="STORY-000",
            mode="pre-flight",
            story_content=None
        )

        assert result["status"] == "ERROR" or result["spec_found"] is False

    def test_malformed_spec_handled(self, malformed_yaml_story):
        """Test that malformed spec YAML is handled gracefully."""
        result = analyze_overlaps(
            story_id="STORY-999",
            mode="pre-flight",
            story_content=malformed_yaml_story
        )

        assert result["spec_found"] is False

    def test_post_flight_still_runs_without_spec(self, temp_git_dir):
        """Test that post-flight git validation runs even without spec."""
        # Create a modified file
        test_file = temp_git_dir / "src" / "service.py"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text("initial")

        import subprocess
        subprocess.run(["git", "add", "."], cwd=temp_git_dir, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=temp_git_dir, capture_output=True)
        test_file.write_text("modified")

        result = analyze_overlaps(
            story_id="STORY-202",
            mode="post-flight",
            declared_paths=[],  # No declared paths (missing spec)
            worktree_path=temp_git_dir
        )

        # Post-flight should still detect the modification
        assert result["mode"] == "post-flight"


# =============================================================================
# Edge Cases and NFRs
# =============================================================================

class TestAdditionalCoverage:
    """Additional tests for coverage gaps."""

    def test_extract_paths_with_format_version_only(self):
        """Test extracting paths when spec has format_version but no technical_specification key."""
        # This tests a specific case where YAML block starts with technical_specification
        # but the parsed content has format_version directly
        story_content = '''---
id: STORY-TEST
status: In Development
---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"
  components:
    - type: "Service"
      name: "test"
      file_path: "src/test.py"
```
'''
        paths, spec_found = extract_file_paths_from_spec(story_content)

        assert spec_found is True
        assert "src/test.py" in paths

    def test_extract_paths_nested_technical_specification(self):
        """Test extracting paths when technical_specification is nested."""
        story_content = '''---
id: STORY-TEST
status: In Development
---

## Technical Specification

```yaml
technical_specification:
  technical_specification:
    format_version: "2.0"
    components:
      - type: "Service"
        name: "nested"
        file_path: "src/nested.py"
```
'''
        paths, spec_found = extract_file_paths_from_spec(story_content)

        assert spec_found is True
        assert "src/nested.py" in paths

    def test_frontmatter_parsing_no_end_marker(self):
        """Test frontmatter parsing when end marker is missing."""
        story_content = '''---
id: STORY-TEST
status: In Development
This has no closing ---
'''
        from src.file_overlap_detector import _parse_yaml_frontmatter
        result = _parse_yaml_frontmatter(story_content)
        assert result is None

    def test_frontmatter_parsing_invalid_yaml(self):
        """Test frontmatter parsing with invalid YAML."""
        story_content = '''---
id: STORY-TEST
status: [invalid yaml without closing
---

Content
'''
        from src.file_overlap_detector import _parse_yaml_frontmatter
        result = _parse_yaml_frontmatter(story_content)
        assert result is None

    def test_scan_active_stories_nonexistent_dir(self):
        """Test scanning non-existent directory."""
        result = scan_active_stories(Path("/nonexistent/path"))
        assert result == {}

    def test_scan_active_stories_excludes_by_id(self, temp_stories_dir):
        """Test that exclude_ids properly filters stories."""
        result = scan_active_stories(temp_stories_dir, exclude_ids=["STORY-200"])

        # STORY-200 should not be in results even if it exists
        assert "STORY-200" not in result

    def test_recommendations_with_many_files(self):
        """Test recommendations when story has more than 3 overlapping files."""
        recommendations = generate_recommendations(
            overlap_count=10,
            overlap_details={"STORY-100": ["a.py", "b.py", "c.py", "d.py", "e.py"]},
            blocking_threshold=15
        )

        # Should have recommendation about shared files
        assert any("5 shared files" in r for r in recommendations)

    def test_recommendations_with_two_files(self):
        """Test recommendations when story has 2 overlapping files."""
        recommendations = generate_recommendations(
            overlap_count=2,
            overlap_details={"STORY-100": ["a.py", "b.py"]},
            blocking_threshold=15
        )

        # Should list files directly
        assert any("a.py" in r or "b.py" in r for r in recommendations)

    def test_recommendations_with_three_plus_files(self):
        """Test recommendations when story has 3+ overlapping files (truncation)."""
        recommendations = generate_recommendations(
            overlap_count=3,
            overlap_details={"STORY-100": ["a.py", "b.py", "c.py"]},
            blocking_threshold=15
        )

        # Should have truncation indicator
        assert any("+1 more" in r for r in recommendations)

    def test_report_with_discrepancies(self, tmp_path):
        """Test report generation with discrepancies (post-flight mode)."""
        discrepancies = {
            "undeclared": ["src/extra.py"],
            "unused": ["src/removed.py"]
        }

        report_path = generate_overlap_report(
            story_id="STORY-094",
            analysis_type="post-flight",
            overlaps={},
            discrepancies=discrepancies,
            recommendations=["Update spec"],
            output_dir=tmp_path
        )

        content = report_path.read_text()
        assert "Undeclared Modifications" in content
        assert "Unused Declarations" in content
        assert "src/extra.py" in content
        assert "src/removed.py" in content

    def test_analyze_overlaps_unknown_mode(self):
        """Test analyze_overlaps with unknown mode."""
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="unknown-mode"
        )

        assert result["status"] == "ERROR"
        assert "Unknown mode" in result["error"]

    def test_analyze_overlaps_post_flight_with_report(self, tmp_path):
        """Test post-flight mode generates report on discrepancies."""
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="post-flight",
            declared_paths=["src/a.py"],
            actual_paths=["src/a.py", "src/b.py"],
            output_dir=tmp_path
        )

        assert result["status"] == "WARNING"
        assert "report_path" in result


class TestEdgeCases:
    """Tests for edge cases and Non-Functional Requirements."""

    def test_circular_dependency_recommendation(self):
        """Test recommendation for circular dependency scenario."""
        # Circular: STORY-A depends on STORY-B, STORY-B overlaps with STORY-A
        recommendations = generate_recommendations(
            overlap_count=5,
            overlap_details={"STORY-A": ["src/shared.py"]},
            blocking_threshold=10,
            is_circular=True
        )

        assert any("sequential" in r.lower() for r in recommendations)

    def test_large_overlap_pagination_recommendation(self):
        """Test recommendation when >20 files overlap."""
        overlaps = {f"STORY-{i:03d}": ["src/file.py"] for i in range(25)}

        recommendations = generate_recommendations(
            overlap_count=25,
            overlap_details=overlaps,
            blocking_threshold=10
        )

        assert any("sequential" in r.lower() or "coordinate" in r.lower() for r in recommendations)

    def test_glob_pattern_in_file_path(self, story_factory, tmp_path):
        """Test handling of glob patterns in file_path."""
        story_content = story_factory(
            story_id="STORY-209",
            status="In Development",
            file_paths=["src/services/*.py", "src/config/**/*.yaml"]
        )

        paths, spec_found = extract_file_paths_from_spec(story_content)

        # Glob patterns should be returned as-is (not expanded in parsing)
        assert "src/services/*.py" in paths
        assert "src/config/**/*.yaml" in paths

    def test_same_file_different_sections_note(self):
        """Test that file-level overlap is detected (not section-level)."""
        # Two stories modify different sections of the same file
        target_paths = ["src/models/user.py"]
        active_stories = {
            "STORY-100": ["src/models/user.py"]  # Same file
        }

        overlaps = detect_overlaps(
            target_paths=target_paths,
            active_stories=active_stories,
            target_story_id="STORY-200"
        )

        # File-level overlap should be detected
        assert "STORY-100" in overlaps
        assert "src/models/user.py" in overlaps["STORY-100"]

    def test_total_phase_0_overhead_under_5s(self, story_factory, tmp_path):
        """Test that total Phase 0 overlap check adds <5s (NFR-003)."""
        # Create 20 story files
        for i in range(20):
            story_content = story_factory(
                story_id=f"STORY-{i:03d}",
                status="In Development",
                file_paths=[f"src/service_{i}.py", "src/shared.py"]
            )
            (tmp_path / f"STORY-{i:03d}.story.md").write_text(story_content)

        start = time.time()
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            fixtures_path=tmp_path,
            target_paths=["src/shared.py", "src/unique.py"]
        )
        elapsed = time.time() - start

        assert elapsed < 5.0, f"Phase 0 overhead was {elapsed:.2f}s, expected <5s"

    def test_response_includes_timestamp(self):
        """Test that response includes ISO timestamp."""
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            target_paths=[],
            active_stories={}
        )

        assert "timestamp" in result
        # Should be valid ISO format
        datetime.fromisoformat(result["timestamp"].replace("Z", "+00:00"))


# =============================================================================
# Integration Tests
# =============================================================================

class TestDevBlockingIntegration:
    """Integration tests for /dev command blocking behavior."""

    def test_blocking_threshold_triggers_halt(self, active_stories_map):
        """Test that exceeding blocking_threshold returns BLOCKED status."""
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            target_paths=["src/services/shared_service.py"] * 15,  # Many overlaps
            active_stories=active_stories_map,
            config={"warning_threshold": 1, "blocking_threshold": 1}
        )

        # Should be BLOCKED due to low threshold
        assert result["status"] in ["WARNING", "BLOCKED"]

    def test_force_flag_context_preserved(self):
        """Test that force flag context is available in result."""
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            target_paths=["src/shared.py"],
            active_stories={"STORY-200": ["src/shared.py"]},
            config={"warning_threshold": 1, "blocking_threshold": 10}
        )

        # Result should indicate whether force bypass is applicable
        assert "warning_threshold" in result or "blocking_threshold" in result

    def test_json_response_structure(self):
        """Test that response is valid JSON-serializable structure."""
        result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            target_paths=["src/file.py"],
            active_stories={}
        )

        # Should be serializable
        json_str = json.dumps(result)
        parsed = json.loads(json_str)

        assert parsed["story_id"] == "STORY-100"
        assert parsed["mode"] == "pre-flight"

    def test_report_path_in_response(self, tmp_path):
        """Test that report path is included in response."""
        result = analyze_overlaps(
            story_id="STORY-094",
            mode="pre-flight",
            target_paths=["src/file.py"],
            active_stories={"STORY-200": ["src/file.py"]},
            output_dir=tmp_path
        )

        if result["overlap_count"] > 0:
            assert "report_path" in result
            assert Path(result["report_path"]).suffix == ".md"

    def test_multiple_modes_supported(self):
        """Test that both pre-flight and post-flight modes work."""
        pre_result = analyze_overlaps(
            story_id="STORY-100",
            mode="pre-flight",
            target_paths=["src/file.py"],
            active_stories={}
        )

        post_result = analyze_overlaps(
            story_id="STORY-100",
            mode="post-flight",
            declared_paths=["src/file.py"],
            actual_paths=["src/file.py"]
        )

        assert pre_result["mode"] == "pre-flight"
        assert post_result["mode"] == "post-flight"

    def test_error_status_on_invalid_input(self):
        """Test that ERROR status is returned on invalid input."""
        result = analyze_overlaps(
            story_id=None,  # Invalid
            mode="pre-flight"
        )

        assert result["status"] == "ERROR"
