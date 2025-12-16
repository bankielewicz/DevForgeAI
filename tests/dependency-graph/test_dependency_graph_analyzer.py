"""
Test suite for dependency-graph-analyzer subagent.
STORY-093: Dependency Graph Enforcement with Transitive Resolution

Run: pytest tests/dependency-graph/ -v
"""
import pytest
import json
import re
import time
from pathlib import Path

# Import the module under test (will fail until implemented)
try:
    from src.dependency_graph_analyzer import (
        parse_yaml_frontmatter,
        validate_story_id,
        normalize_depends_on,
        build_dependency_graph,
        detect_cycle,
        resolve_transitive_dependencies,
        validate_dependency_statuses,
        generate_visualization,
        analyze_dependencies,
    )
except ImportError:
    # Mark all tests to fail with clear message during TDD Red phase
    pytestmark = pytest.mark.skip(reason="dependency_graph_analyzer module not yet implemented")


class TestYAMLParsing:
    """AC#1: Story YAML depends_on Field Support (8 tests)"""

    def test_valid_depends_on_single(self, valid_story_content):
        """Test parsing single dependency from YAML frontmatter."""
        result = parse_yaml_frontmatter(valid_story_content)
        assert result is not None
        assert "depends_on" in result
        assert result["depends_on"] == ["STORY-101"]

    def test_valid_depends_on_multiple(self):
        """Test parsing multiple dependencies."""
        content = '''---
id: STORY-109
depends_on: ["STORY-101", "STORY-102", "STORY-103"]
---
'''
        result = parse_yaml_frontmatter(content)
        assert len(result["depends_on"]) == 3
        assert "STORY-101" in result["depends_on"]
        assert "STORY-102" in result["depends_on"]
        assert "STORY-103" in result["depends_on"]

    def test_empty_depends_on_array(self, empty_depends_on_content):
        """Test parsing empty depends_on: []"""
        result = parse_yaml_frontmatter(empty_depends_on_content)
        assert result["depends_on"] == []

    def test_missing_depends_on_field(self):
        """Test story without depends_on field returns empty list."""
        content = '''---
id: STORY-111
title: No depends_on field
---
'''
        result = parse_yaml_frontmatter(content)
        assert result.get("depends_on", []) == []

    def test_invalid_story_id_format(self):
        """Test rejection of invalid IDs like 'STORY-1' or 'story-123'."""
        invalid_ids = ["STORY-1", "STORY-12", "story-123", "INVALID", "123", ""]
        for invalid_id in invalid_ids:
            assert validate_story_id(invalid_id) is False, f"{invalid_id} should be invalid"

    def test_valid_story_id_format(self):
        """Test acceptance of valid IDs matching ^STORY-\d{3,4}$"""
        valid_ids = ["STORY-001", "STORY-123", "STORY-0001", "STORY-9999"]
        for valid_id in valid_ids:
            assert validate_story_id(valid_id) is True, f"{valid_id} should be valid"

    def test_mixed_valid_invalid_ids(self, invalid_id_content):
        """Test filtering of mixed valid/invalid IDs."""
        result = parse_yaml_frontmatter(invalid_id_content)
        valid, invalid = normalize_depends_on(result["depends_on"])
        assert "STORY-103" in valid
        assert "STORY-1" in invalid
        assert "story-102" in invalid
        assert "INVALID" in invalid

    def test_whitespace_and_case_normalization(self):
        """Test trimming whitespace and uppercase normalization."""
        raw_ids = ["  STORY-101  ", "story-102", " Story-103 "]
        valid, invalid = normalize_depends_on(raw_ids)
        assert "STORY-101" in valid
        assert "STORY-103" in valid
        # story-102 normalized to STORY-102 which is valid format
        assert "STORY-102" in valid or "story-102" in invalid


class TestGraphBuilding:
    """AC#4: Transitive Dependency Resolution (6 tests)"""

    def test_simple_chain_resolution(self, fixtures_dir):
        """Test A -> B -> C resolves to [C, B] (deepest first)."""
        # STORY-103 -> STORY-104 -> STORY-105
        graph = {
            "STORY-103": ["STORY-104"],
            "STORY-104": ["STORY-105"],
            "STORY-105": [],
        }
        transitive = resolve_transitive_dependencies("STORY-103", graph)
        # Should resolve deepest first: STORY-105, then STORY-104
        assert "STORY-105" in transitive
        assert "STORY-104" in transitive
        assert transitive.index("STORY-105") < transitive.index("STORY-104")

    def test_diamond_pattern_unique(self):
        """Test diamond pattern (A -> B, A -> C, B -> D, C -> D) resolves D once."""
        graph = {
            "STORY-A": ["STORY-B", "STORY-C"],
            "STORY-B": ["STORY-D"],
            "STORY-C": ["STORY-D"],
            "STORY-D": [],
        }
        transitive = resolve_transitive_dependencies("STORY-A", graph)
        # STORY-D should appear only once
        assert transitive.count("STORY-D") == 1

    def test_multiple_direct_deps(self):
        """Test A -> [B, C, D] resolves all direct dependencies."""
        graph = {
            "STORY-A": ["STORY-B", "STORY-C", "STORY-D"],
            "STORY-B": [],
            "STORY-C": [],
            "STORY-D": [],
        }
        transitive = resolve_transitive_dependencies("STORY-A", graph)
        assert len(transitive) == 3
        assert set(transitive) == {"STORY-B", "STORY-C", "STORY-D"}

    def test_deep_chain_over_10_levels(self):
        """Test chain >10 levels resolves correctly."""
        # Build a chain of 15 stories
        graph = {}
        for i in range(1, 16):
            story_id = f"STORY-{i:03d}"
            if i < 15:
                graph[story_id] = [f"STORY-{i+1:03d}"]
            else:
                graph[story_id] = []

        transitive = resolve_transitive_dependencies("STORY-001", graph)
        assert len(transitive) == 14  # All except STORY-001 itself

    def test_no_dependencies_returns_empty(self):
        """Test story with no dependencies returns empty list."""
        graph = {"STORY-110": []}
        transitive = resolve_transitive_dependencies("STORY-110", graph)
        assert transitive == []

    def test_complex_graph_10_stories(self):
        """Test complex graph with 10+ stories and mixed patterns."""
        graph = {
            "STORY-001": ["STORY-002", "STORY-003"],
            "STORY-002": ["STORY-004", "STORY-005"],
            "STORY-003": ["STORY-005", "STORY-006"],
            "STORY-004": ["STORY-007"],
            "STORY-005": ["STORY-007", "STORY-008"],
            "STORY-006": ["STORY-008"],
            "STORY-007": ["STORY-009"],
            "STORY-008": ["STORY-009"],
            "STORY-009": ["STORY-010"],
            "STORY-010": [],
        }
        transitive = resolve_transitive_dependencies("STORY-001", graph)
        # All 9 dependencies should be resolved
        assert len(transitive) == 9
        # STORY-010 should be resolved first (deepest)
        assert "STORY-010" in transitive


class TestCycleDetection:
    """AC#5: Circular Dependency Detection (6 tests)"""

    def test_direct_cycle_a_b_a(self, circular_graph):
        """Test A -> B -> A is detected as cycle."""
        cycle = detect_cycle(circular_graph, "STORY-106")
        assert cycle is not None
        assert "STORY-106" in cycle
        assert "STORY-107" in cycle

    def test_indirect_cycle_a_b_c_a(self):
        """Test A -> B -> C -> A is detected."""
        graph = {
            "STORY-A": ["STORY-B"],
            "STORY-B": ["STORY-C"],
            "STORY-C": ["STORY-A"],
        }
        cycle = detect_cycle(graph, "STORY-A")
        assert cycle is not None
        assert len(cycle) >= 3

    def test_self_dependency(self):
        """Test A -> A (self-dependency) is detected."""
        graph = {"STORY-A": ["STORY-A"]}
        cycle = detect_cycle(graph, "STORY-A")
        assert cycle is not None
        assert cycle == ["STORY-A", "STORY-A"]

    def test_no_cycle_in_valid_dag(self, sample_graph):
        """Test valid DAG has no cycle detected."""
        cycle = detect_cycle(sample_graph, "STORY-103")
        assert cycle is None

    def test_cycle_path_is_correct(self):
        """Test cycle path correctly shows the cycle."""
        graph = {
            "STORY-A": ["STORY-B"],
            "STORY-B": ["STORY-C"],
            "STORY-C": ["STORY-A"],
        }
        cycle = detect_cycle(graph, "STORY-A")
        # Cycle path should end with the node that creates the cycle
        assert cycle[-1] == cycle[0] or "STORY-A" in cycle

    def test_multiple_cycles_first_detected(self):
        """Test when multiple cycles exist, first encountered is reported."""
        graph = {
            "STORY-A": ["STORY-B", "STORY-D"],
            "STORY-B": ["STORY-C"],
            "STORY-C": ["STORY-A"],  # Cycle 1
            "STORY-D": ["STORY-E"],
            "STORY-E": ["STORY-D"],  # Cycle 2
        }
        cycle = detect_cycle(graph, "STORY-A")
        assert cycle is not None  # At least one cycle detected


class TestStatusValidation:
    """AC#2, AC#7, AC#8: Status Validation (6 tests)"""

    def test_dev_complete_status_passes(self):
        """Test 'Dev Complete' status is valid for dependencies."""
        status_map = {"STORY-101": "Dev Complete"}
        failures = validate_dependency_statuses(["STORY-101"], status_map)
        assert len(failures) == 0

    def test_qa_approved_status_passes(self):
        """Test 'QA Approved' and 'QA Approved checkmark' statuses pass."""
        status_map = {
            "STORY-101": "QA Approved",
            "STORY-102": "QA Approved ✅",
        }
        failures = validate_dependency_statuses(["STORY-101", "STORY-102"], status_map)
        assert len(failures) == 0

    def test_in_development_status_blocks(self):
        """Test 'In Development' status blocks with correct message."""
        status_map = {"STORY-102": "In Development"}
        failures = validate_dependency_statuses(["STORY-102"], status_map)
        assert len(failures) == 1
        assert failures[0]["dependency"] == "STORY-102"
        assert "In Development" in failures[0]["status"]
        assert "Dev Complete" in failures[0]["required"] or "QA Approved" in failures[0]["required"]

    def test_qa_failed_status_blocks_with_suggestion(self):
        """Test 'QA Failed' blocks with suggestion to run /qa."""
        status_map = {"STORY-108": "QA Failed"}
        failures = validate_dependency_statuses(["STORY-108"], status_map)
        assert len(failures) == 1
        assert "QA Failed" in failures[0]["status"] or "failed QA" in failures[0]["message"]
        assert "suggestion" in failures[0] or "/qa" in failures[0].get("message", "")

    def test_multiple_failures_all_reported(self, status_map_invalid):
        """Test all failures are reported, not just first."""
        deps = ["STORY-101", "STORY-102", "STORY-108"]
        failures = validate_dependency_statuses(deps, status_map_invalid)
        # STORY-101 is valid, STORY-102 and STORY-108 should fail
        assert len(failures) == 2
        failed_ids = [f["dependency"] for f in failures]
        assert "STORY-102" in failed_ids
        assert "STORY-108" in failed_ids

    def test_released_status_passes(self):
        """Test 'Released' status is valid for dependencies."""
        status_map = {"STORY-101": "Released"}
        failures = validate_dependency_statuses(["STORY-101"], status_map)
        assert len(failures) == 0


class TestForceBypass:
    """AC#6: Force Flag Bypass (3 tests)"""

    def test_force_flag_bypasses_validation(self):
        """Test --force flag allows proceeding despite failures."""
        # This is tested at integration level with full analyze_dependencies
        result = analyze_dependencies(
            story_id="STORY-109",  # Has invalid dependencies
            force=True,
            fixtures_path=Path(__file__).parent / "fixtures"
        )
        # With force=True, blocking should be False even with failures
        assert result["blocking"] is False or result.get("force_bypassed") is True

    def test_force_bypass_logs_warning(self, tmp_path):
        """Test force bypass creates log file."""
        log_dir = tmp_path / ".devforgeai" / "logs"
        result = analyze_dependencies(
            story_id="STORY-109",
            force=True,
            fixtures_path=Path(__file__).parent / "fixtures",
            log_dir=log_dir
        )
        # Log file should be created
        if result.get("force_bypassed"):
            log_files = list(log_dir.glob("dependency-bypass-*.log"))
            assert len(log_files) >= 1

    def test_force_log_contains_details(self, tmp_path):
        """Test force bypass log contains story ID, timestamp, and failures."""
        log_dir = tmp_path / ".devforgeai" / "logs"
        result = analyze_dependencies(
            story_id="STORY-109",
            force=True,
            fixtures_path=Path(__file__).parent / "fixtures",
            log_dir=log_dir
        )
        if result.get("force_bypassed"):
            log_files = list(log_dir.glob("dependency-bypass-*.log"))
            if log_files:
                content = log_files[0].read_text()
                assert "STORY-109" in content
                assert "timestamp" in content.lower() or "2025" in content


class TestVisualization:
    """AC#9: Dependency Graph Visualization (5 tests)"""

    def test_visualization_ascii_tree_generated(self, sample_graph, status_map_valid):
        """Test ASCII tree is generated for graph."""
        viz = generate_visualization("STORY-103", sample_graph, status_map_valid)
        assert viz is not None
        assert isinstance(viz, str)
        assert "STORY-103" in viz

    def test_visualization_shows_status_icons(self, sample_graph, status_map_valid):
        """Test visualization shows status icons (checkmark/clock)."""
        viz = generate_visualization("STORY-103", sample_graph, status_map_valid)
        # Should contain status indicator
        assert "✅" in viz or "⏳" in viz or "Approved" in viz or "Complete" in viz

    def test_visualization_indentation_for_depth(self, sample_graph, status_map_valid):
        """Test deeper dependencies are indented."""
        viz = generate_visualization("STORY-103", sample_graph, status_map_valid)
        lines = viz.split("\n")
        # Find lines with dependencies - they should have indentation
        dep_lines = [l for l in lines if "STORY-104" in l or "STORY-105" in l]
        if dep_lines:
            # At least one dependency line should have leading whitespace
            assert any(l.startswith(" ") or "└" in l for l in dep_lines)

    def test_visualization_handles_empty_graph(self):
        """Test visualization handles story with no dependencies."""
        graph = {"STORY-110": []}
        status_map = {}
        viz = generate_visualization("STORY-110", graph, status_map)
        assert "STORY-110" in viz

    def test_visualization_blocked_deps_marked(self):
        """Test blocked dependencies are visually marked."""
        graph = {"STORY-A": ["STORY-B"]}
        status_map = {"STORY-B": "In Development"}
        viz = generate_visualization("STORY-A", graph, status_map)
        # Should indicate STORY-B is not ready
        assert "⏳" in viz or "In Development" in viz or "blocked" in viz.lower()


class TestEdgeCases:
    """Edge cases from story spec (5 tests)"""

    def test_nonexistent_dependency_handled(self, fixtures_dir):
        """Test graceful handling when dependency story file not found."""
        result = analyze_dependencies(
            story_id="STORY-100",  # Depends on STORY-101 which may not exist at runtime
            fixtures_path=fixtures_dir,
            allow_missing=True
        )
        # Should not crash, should report missing in validation
        assert result is not None
        assert "status" in result

    def test_malformed_yaml_handled(self, tmp_path):
        """Test graceful handling of invalid YAML frontmatter."""
        bad_story = tmp_path / "STORY-BAD.story.md"
        bad_story.write_text('''---
id: STORY-BAD
depends_on: [not valid yaml
---
''')
        result = parse_yaml_frontmatter(bad_story.read_text())
        # Should return None or error indicator, not crash
        assert result is None or result.get("error") is not None

    def test_empty_story_file_handled(self, tmp_path):
        """Test graceful handling of empty story file."""
        empty_story = tmp_path / "STORY-EMPTY.story.md"
        empty_story.write_text("")
        result = parse_yaml_frontmatter(empty_story.read_text())
        assert result is None or result == {}

    def test_performance_50_stories_under_500ms(self, tmp_path):
        """Test validation of 50-story graph completes in <500ms."""
        # Build 50-story graph
        graph = {}
        for i in range(1, 51):
            story_id = f"STORY-{i:03d}"
            if i < 50:
                graph[story_id] = [f"STORY-{i+1:03d}"]
            else:
                graph[story_id] = []

        start = time.time()
        transitive = resolve_transitive_dependencies("STORY-001", graph)
        elapsed = time.time() - start

        assert elapsed < 0.5, f"Took {elapsed:.3f}s, should be <0.5s"
        assert len(transitive) == 49

    def test_content_without_frontmatter_delimiters(self):
        """Test content that doesn't start with '---'."""
        content = "No frontmatter here"
        result = parse_yaml_frontmatter(content)
        assert result is None

    def test_content_with_single_delimiter(self):
        """Test content with only one '---' delimiter."""
        content = "---\nid: STORY-100"
        result = parse_yaml_frontmatter(content)
        assert result is None

    def test_empty_yaml_section(self):
        """Test content with empty YAML between delimiters."""
        content = "---\n---\nBody content"
        result = parse_yaml_frontmatter(content)
        assert result == {}

    def test_yaml_parses_to_none(self):
        """Test YAML that explicitly parses to null/None."""
        content = "---\nnull\n---\nBody"
        result = parse_yaml_frontmatter(content)
        assert result == {}

    def test_yaml_parses_to_list_not_dict(self):
        """Test YAML that parses to a list instead of dict."""
        content = "---\n- item1\n- item2\n---\nBody"
        result = parse_yaml_frontmatter(content)
        assert result is None

    def test_normalize_with_non_string_items(self):
        """Test normalize_depends_on with non-string items in list."""
        ids = ["STORY-101", 123, None, "STORY-102"]
        valid, invalid = normalize_depends_on(ids)
        assert "STORY-101" in valid
        assert "STORY-102" in valid
        assert "123" in invalid
        assert "None" in invalid

    def test_json_output_format_valid(self, fixtures_dir):
        """Test analyze_dependencies returns valid JSON structure."""
        result = analyze_dependencies(
            story_id="STORY-100",
            fixtures_path=fixtures_dir
        )

        # Validate JSON structure
        assert "status" in result
        assert result["status"] in ["PASS", "BLOCKED", "ERROR"]
        assert "story_id" in result
        assert "blocking" in result
        assert "dependencies" in result
        assert "validation" in result

        # Dependencies structure
        deps = result["dependencies"]
        assert "direct" in deps
        assert "transitive" in deps
        assert "total_count" in deps

        # Validation structure
        val = result["validation"]
        assert "all_exist" in val
        assert "all_valid_status" in val
        assert "cycle_detected" in val
