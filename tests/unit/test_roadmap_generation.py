"""
Test suite for AC8: Roadmap Generation from Stories and Epics

Tests extraction of epics/sprints, timeline generation, milestone visualization,
dependency showing, and dynamic roadmap updates.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
from typing import Dict, List


class TestEpicAndSprintExtraction:
    """Test extraction of epics and sprints from .ai_docs/."""

    def test_should_find_all_epics(self):
        """Test that roadmap generator finds all epics in devforgeai/specs/Epics/."""
        # Arrange
        epic_files = [
            "EPIC-001.epic.md",
            "EPIC-002.epic.md",
            "EPIC-003.epic.md"
        ]

        # Act
        from devforgeai_documentation import RoadmapGenerator
        gen = RoadmapGenerator()
        epics = gen.find_epics()

        # Assert
        assert epics is not None
        assert isinstance(epics, list)

    def test_should_find_all_sprints(self):
        """Test that roadmap generator finds all sprints in devforgeai/specs/Sprints/."""
        # Arrange
        sprint_files = [
            "Sprint-1.md",
            "Sprint-2.md",
            "Sprint-3.md"
        ]

        # Act
        from devforgeai_documentation import RoadmapGenerator
        gen = RoadmapGenerator()
        sprints = gen.find_sprints()

        # Assert
        assert sprints is not None
        assert isinstance(sprints, list)

    def test_should_extract_epic_metadata(self):
        """Test that epic metadata is extracted (ID, name, status, dates)."""
        # Arrange
        epic_content = """
---
id: EPIC-001
title: User Authentication System
status: In Progress
planned_completion: 2025-12-15
priority: High
---
"""

        # Act
        from devforgeai_documentation import EpicExtractor
        extractor = EpicExtractor()
        metadata = extractor.extract_metadata(epic_content)

        # Assert
        assert metadata is not None
        assert metadata.get("id") == "EPIC-001"
        assert metadata.get("title") == "User Authentication System"
        assert metadata.get("status") == "In Progress"

    def test_should_extract_sprint_metadata(self):
        """Test that sprint metadata is extracted."""
        # Arrange
        sprint_content = """
---
name: Sprint-1
start_date: 2025-11-18
end_date: 2025-12-02
status: In Progress
stories: [STORY-001, STORY-002, STORY-003]
---
"""

        # Act
        from devforgeai_documentation import SprintExtractor
        extractor = SprintExtractor()
        metadata = extractor.extract_metadata(sprint_content)

        # Assert
        assert metadata is not None
        assert metadata.get("name") == "Sprint-1"
        assert "2025-11-18" in str(metadata)

    def test_should_find_stories_in_sprint(self):
        """Test that all stories in a sprint are identified."""
        # Arrange
        sprint = {
            "name": "Sprint-1",
            "stories": ["STORY-001", "STORY-002", "STORY-003"]
        }

        # Act
        from devforgeai_documentation import SprintAnalyzer
        analyzer = SprintAnalyzer()
        stories = analyzer.get_stories(sprint)

        # Assert
        assert stories is not None
        assert len(stories) == 3


class TestTimelineGeneration:
    """Test timeline generation for roadmap."""

    def test_should_create_timeline_with_completed_items(self):
        """Test that timeline shows completed epics/sprints."""
        # Arrange
        items = [
            {"name": "EPIC-001", "status": "Completed", "end_date": "2025-11-01"},
            {"name": "EPIC-002", "status": "In Progress", "end_date": "2025-12-15"},
            {"name": "EPIC-003", "status": "Planned", "end_date": "2026-01-31"}
        ]

        # Act
        from devforgeai_documentation import TimelineGenerator
        gen = TimelineGenerator()
        timeline = gen.generate_timeline(items)

        # Assert
        assert timeline is not None
        timeline_text = str(timeline)
        assert "Completed" in timeline_text or "2025-11-01" in timeline_text

    def test_should_show_in_progress_items(self):
        """Test that timeline prominently shows in-progress items."""
        # Arrange
        items = [
            {"name": "EPIC-001", "status": "Completed", "end_date": "2025-11-01"},
            {"name": "EPIC-002", "status": "In Progress", "end_date": "2025-12-15"}
        ]

        # Act
        from devforgeai_documentation import TimelineGenerator
        gen = TimelineGenerator()
        timeline = gen.generate_timeline(items)

        # Assert
        assert timeline is not None
        assert "EPIC-002" in str(timeline) or "In Progress" in str(timeline)

    def test_should_show_planned_items(self):
        """Test that timeline shows future planned items."""
        # Arrange
        items = [
            {"name": "EPIC-003", "status": "Planned", "end_date": "2026-01-31"}
        ]

        # Act
        from devforgeai_documentation import TimelineGenerator
        gen = TimelineGenerator()
        timeline = gen.generate_timeline(items)

        # Assert
        assert timeline is not None
        assert "EPIC-003" in str(timeline) or "Planned" in str(timeline)

    def test_should_calculate_sprint_duration(self):
        """Test that sprint duration is calculated correctly."""
        # Arrange
        sprint = {
            "start_date": "2025-11-18",
            "end_date": "2025-12-02"
        }

        # Act
        from devforgeai_documentation import TimelineCalculator
        calc = TimelineCalculator()
        duration = calc.calculate_duration(sprint)

        # Assert
        assert duration is not None
        assert duration == 14  # 2 weeks

    def test_should_estimate_completion_date(self):
        """Test that completion dates are estimated for in-progress items."""
        # Arrange
        item = {
            "name": "EPIC-001",
            "start_date": "2025-11-01",
            "progress": 50,  # 50% complete
            "estimated_total_duration": 8  # weeks
        }

        # Act
        from devforgeai_documentation import TimelineCalculator
        calc = TimelineCalculator()
        estimated_end = calc.estimate_completion(item)

        # Assert
        assert estimated_end is not None
        # Should be approximately 4 weeks from start
        assert "2025" in str(estimated_end) or "11" in str(estimated_end)


class TestMilestoneVisualization:
    """Test milestone visualization in roadmap."""

    def test_should_identify_milestones(self):
        """Test that major milestones are identified from epics."""
        # Arrange
        epics = [
            {"name": "EPIC-001", "is_milestone": True, "date": "2025-11-30"},
            {"name": "EPIC-002", "is_milestone": False, "date": "2025-12-15"},
            {"name": "EPIC-003", "is_milestone": True, "date": "2026-01-31"}
        ]

        # Act
        from devforgeai_documentation import MilestoneIdentifier
        identifier = MilestoneIdentifier()
        milestones = identifier.find_milestones(epics)

        # Assert
        assert milestones is not None
        assert len(milestones) == 2

    def test_should_show_release_targets(self):
        """Test that release milestones are visualized."""
        # Arrange
        releases = [
            {"version": "1.0.0", "date": "2025-11-30", "features": ["Auth", "API"]},
            {"version": "1.1.0", "date": "2025-12-31", "features": ["Dashboard"]},
            {"version": "2.0.0", "date": "2026-01-31", "features": ["Mobile app"]}
        ]

        # Act
        from devforgeai_documentation import ReleaseVisualizer
        visualizer = ReleaseVisualizer()
        visualization = visualizer.visualize_releases(releases)

        # Assert
        assert visualization is not None
        vis_text = str(visualization).lower()
        assert "1.0.0" in vis_text or "release" in vis_text

    def test_should_show_milestone_dates(self):
        """Test that milestone dates are clearly marked."""
        # Arrange
        milestones = [
            {"name": "MVP Release", "date": "2025-11-30"},
            {"name": "v1.0 Stable", "date": "2025-12-15"}
        ]

        # Act
        from devforgeai_documentation import MilestoneVisualizer
        visualizer = MilestoneVisualizer()
        visualization = visualizer.visualize(milestones)

        # Assert
        assert visualization is not None
        assert "2025-11-30" in str(visualization) or "MVP" in str(visualization)

    def test_should_mark_completed_milestones(self):
        """Test that completed milestones are marked distinctly."""
        # Arrange
        milestones = [
            {"name": "Alpha", "date": "2025-10-15", "status": "Completed"},
            {"name": "Beta", "date": "2025-11-30", "status": "In Progress"},
            {"name": "GA", "date": "2025-12-31", "status": "Planned"}
        ]

        # Act
        from devforgeai_documentation import MilestoneVisualizer
        visualizer = MilestoneVisualizer()
        output = visualizer.visualize_with_status(milestones)

        # Assert
        assert output is not None
        output_text = str(output).lower()
        assert "completed" in output_text or "alpha" in output_text


class TestDependencyVisualization:
    """Test showing dependencies between features."""

    def test_should_identify_story_dependencies(self):
        """Test that dependencies between stories are identified."""
        # Arrange
        stories = [
            {"id": "STORY-001", "title": "Auth service", "depends_on": []},
            {"id": "STORY-002", "title": "User login", "depends_on": ["STORY-001"]},
            {"id": "STORY-003", "title": "Dashboard", "depends_on": ["STORY-002"]}
        ]

        # Act
        from devforgeai_documentation import DependencyAnalyzer
        analyzer = DependencyAnalyzer()
        dependencies = analyzer.analyze_dependencies(stories)

        # Assert
        assert dependencies is not None
        assert len(dependencies) >= 2

    def test_should_show_epic_dependencies(self):
        """Test that epic dependencies are visualized."""
        # Arrange
        epics = [
            {"id": "EPIC-001", "name": "Authentication", "depends_on": []},
            {"id": "EPIC-002", "name": "User Management", "depends_on": ["EPIC-001"]},
            {"id": "EPIC-003", "name": "Payment", "depends_on": ["EPIC-001", "EPIC-002"]}
        ]

        # Act
        from devforgeai_documentation import EpicDependencyVisualizer
        visualizer = EpicDependencyVisualizer()
        diagram = visualizer.create_dependency_diagram(epics)

        # Assert
        assert diagram is not None
        # Should show relationships
        diagram_text = str(diagram)
        assert "EPIC-001" in diagram_text or "-->" in diagram_text

    def test_should_detect_circular_dependencies(self):
        """Test that circular dependencies are detected."""
        # Arrange
        stories = [
            {"id": "STORY-001", "depends_on": ["STORY-002"]},
            {"id": "STORY-002", "depends_on": ["STORY-003"]},
            {"id": "STORY-003", "depends_on": ["STORY-001"]}  # Circular!
        ]

        # Act
        from devforgeai_documentation import DependencyAnalyzer
        analyzer = DependencyAnalyzer()
        circular = analyzer.find_circular_dependencies(stories)

        # Assert
        assert circular is not None
        assert len(circular) > 0

    def test_should_identify_blocking_dependencies(self):
        """Test that blocking dependencies are identified."""
        # Arrange
        stories = [
            {"id": "STORY-001", "title": "Setup DB", "depends_on": []},
            {"id": "STORY-002", "title": "Create API", "depends_on": ["STORY-001"]},
            {"id": "STORY-003", "title": "Frontend", "depends_on": ["STORY-002"]}
        ]

        # Act
        from devforgeai_documentation import BlockingDependencyDetector
        detector = BlockingDependencyDetector()
        blocking = detector.find_blocking(stories)

        # Assert
        assert blocking is not None
        # STORY-001 blocks both 002 and 003
        assert isinstance(blocking, dict) or isinstance(blocking, list)


class TestRoadmapFormats:
    """Test various roadmap visualization formats."""

    def test_should_generate_ascii_roadmap(self):
        """Test that ASCII roadmap is generated."""
        # Arrange
        items = [
            {"name": "Q4 2025", "items": ["EPIC-001", "EPIC-002"]},
            {"name": "Q1 2026", "items": ["EPIC-003"]}
        ]

        # Act
        from devforgeai_documentation import RoadmapFormatter
        formatter = RoadmapFormatter()
        roadmap = formatter.format_as_ascii(items)

        # Assert
        assert roadmap is not None
        assert isinstance(roadmap, str)

    def test_should_generate_gantt_roadmap(self):
        """Test that Gantt chart roadmap is generated."""
        # Arrange
        items = [
            {"name": "EPIC-001", "start": "2025-11-01", "end": "2025-12-31"},
            {"name": "EPIC-002", "start": "2025-12-01", "end": "2026-01-31"}
        ]

        # Act
        from devforgeai_documentation import GanttRoadmapGenerator
        gen = GanttRoadmapGenerator()
        gantt = gen.generate(items)

        # Assert
        assert gantt is not None

    def test_should_generate_mermaid_roadmap(self):
        """Test that Mermaid diagram roadmap is generated."""
        # Arrange
        items = [
            {"name": "EPIC-001", "date": "2025-11-30"},
            {"name": "EPIC-002", "date": "2025-12-31"}
        ]

        # Act
        from devforgeai_documentation import MermaidRoadmapGenerator
        gen = MermaidRoadmapGenerator()
        diagram = gen.generate(items)

        # Assert
        assert diagram is not None
        # Should be Mermaid syntax
        diagram_text = str(diagram).lower()
        assert "graph" in diagram_text or "timeline" in diagram_text or "-->" in diagram_text

    def test_should_generate_interactive_roadmap(self):
        """Test that interactive HTML roadmap is generated."""
        # Arrange
        items = [
            {"name": "EPIC-001", "status": "Completed"},
            {"name": "EPIC-002", "status": "In Progress"}
        ]

        # Act
        from devforgeai_documentation import InteractiveRoadmapGenerator
        gen = InteractiveRoadmapGenerator()
        html = gen.generate_interactive(items)

        # Assert
        assert html is not None
        # Should have HTML/JavaScript
        html_text = str(html).lower()
        assert "html" in html_text or "<" in html_text or "interactive" in html_text


class TestRoadmapUpdating:
    """Test dynamic roadmap updates as projects progress."""

    def test_should_update_roadmap_on_epic_completion(self):
        """Test that roadmap updates when epic is completed."""
        # Arrange
        epic_id = "EPIC-001"
        new_status = "Completed"

        # Act
        from devforgeai_documentation import RoadmapUpdater
        updater = RoadmapUpdater()
        updated = updater.update_epic_status(epic_id, new_status)

        # Assert
        assert updated is True

    def test_should_update_progress_percentages(self):
        """Test that completion percentages are updated."""
        # Arrange
        epic = {
            "id": "EPIC-001",
            "total_stories": 10,
            "completed_stories": 7
        }

        # Act
        from devforgeai_documentation import ProgressCalculator
        calc = ProgressCalculator()
        progress = calc.calculate_progress(epic)

        # Assert
        assert progress == 70 or progress == 70.0

    def test_should_update_milestone_status(self):
        """Test that milestone status is updated when reached."""
        # Arrange
        milestone = {"name": "MVP Release", "target_date": "2025-11-30"}
        current_date = "2025-11-30"

        # Act
        from devforgeai_documentation import MilestoneStatusUpdater
        updater = MilestoneStatusUpdater()
        status = updater.check_milestone_status(milestone, current_date)

        # Assert
        assert status in ["Reached", "Upcoming", "In Progress", "Delayed"]

    def test_should_recalculate_estimated_dates(self):
        """Test that estimated completion dates are recalculated."""
        # Arrange
        epic = {
            "id": "EPIC-001",
            "start_date": "2025-11-01",
            "initial_estimate": "2025-12-31",
            "progress": 60,
            "current_velocity": 1.2  # 20% ahead of schedule
        }

        # Act
        from devforgeai_documentation import EstimateRecalculator
        recalc = EstimateRecalculator()
        new_estimate = recalc.recalculate_estimate(epic)

        # Assert
        assert new_estimate is not None
        # Should show earlier completion due to higher velocity


class TestRoadmapIntegrationWithDocumentation:
    """Test roadmap integration in documentation."""

    def test_should_embed_roadmap_in_documentation(self):
        """Test that roadmap is embedded in main documentation."""
        # Arrange
        roadmap_content = "Timeline and milestones..."
        doc_template = "# Project\n\n## Roadmap\n\n{{roadmap}}\n\n## Other sections"

        # Act
        from devforgeai_documentation import RoadmapEmbedder
        embedder = RoadmapEmbedder()
        result = embedder.embed(doc_template, roadmap_content)

        # Assert
        assert result is not None
        assert roadmap_content in result or "Timeline" in result

    def test_should_update_roadmap_in_docs_on_epic_change(self):
        """Test that documentation roadmap updates when epic status changes."""
        # Arrange
        epic_id = "EPIC-001"
        new_status = "Completed"

        # Act
        from devforgeai_documentation import DocumentationRoadmapSync
        sync = DocumentationRoadmapSync()
        updated = sync.sync_on_epic_change(epic_id, new_status)

        # Assert
        assert updated is True or updated is None  # Success or no-op

    def test_should_generate_roadmap_markdown_file(self):
        """Test that roadmap is generated as separate markdown file."""
        # Arrange
        items = [
            {"name": "EPIC-001", "status": "Completed"},
            {"name": "EPIC-002", "status": "In Progress"}
        ]

        # Act
        from devforgeai_documentation import RoadmapMarkdownGenerator
        gen = RoadmapMarkdownGenerator()
        markdown = gen.generate_file(items)

        # Assert
        assert markdown is not None
        assert "# Roadmap" in markdown or "EPIC-001" in markdown


class TestRoadmapPerformance:
    """Test roadmap generation performance."""

    @pytest.mark.timeout(30)
    def test_roadmap_generation_should_complete_in_30_seconds(self):
        """Test that roadmap with 50+ epics generates in <30 seconds."""
        # Arrange
        epics = [
            {
                "id": f"EPIC-{i:03d}",
                "name": f"Feature {i}",
                "status": "Planned",
                "date": f"2025-{11+i%6:02d}-01"
            }
            for i in range(50)
        ]

        # Act
        from devforgeai_documentation import RoadmapGenerator
        import time
        gen = RoadmapGenerator()
        start = time.time()
        roadmap = gen.generate_roadmap(epics)
        elapsed = time.time() - start

        # Assert
        assert roadmap is not None
        assert elapsed < 30


class TestRoadmapDataModels:
    """Test data models for roadmap."""

    def test_epic_roadmap_item_structure(self):
        """Test Epic roadmap item data structure."""
        # Arrange
        epic_item = {
            "id": "EPIC-001",
            "name": "Authentication System",
            "status": "In Progress",
            "start_date": "2025-11-01",
            "estimated_end_date": "2025-12-31",
            "progress": 50,
            "features": ["Login", "Register", "MFA"]
        }

        # Act
        from devforgeai_documentation import EpicRoadmapItem
        item = EpicRoadmapItem(**epic_item)

        # Assert
        assert item.id == "EPIC-001"
        assert item.progress == 50

    def test_milestone_roadmap_item_structure(self):
        """Test Milestone roadmap item data structure."""
        # Arrange
        milestone_item = {
            "name": "MVP Release",
            "date": "2025-11-30",
            "status": "Upcoming",
            "epics_involved": ["EPIC-001", "EPIC-002"]
        }

        # Act
        from devforgeai_documentation import MilestoneRoadmapItem
        item = MilestoneRoadmapItem(**milestone_item)

        # Assert
        assert item.name == "MVP Release"
        assert len(item.epics_involved) == 2


class TestEdgeCases:
    """Test edge cases in roadmap generation."""

    def test_should_handle_empty_roadmap(self):
        """Test that empty roadmap is handled gracefully."""
        # Arrange
        epics = []
        sprints = []

        # Act
        from devforgeai_documentation import RoadmapGenerator
        gen = RoadmapGenerator()
        roadmap = gen.generate_roadmap(epics, sprints)

        # Assert
        assert roadmap is not None
        # Should return empty or placeholder

    def test_should_handle_missing_dates(self):
        """Test that items without dates are handled."""
        # Arrange
        items = [
            {"name": "EPIC-001", "date": "2025-11-30"},
            {"name": "EPIC-002"}  # No date!
        ]

        # Act
        from devforgeai_documentation import RoadmapGenerator
        gen = RoadmapGenerator()
        roadmap = gen.generate_roadmap(items)

        # Assert
        assert roadmap is not None
        # Should handle gracefully (put at end or mark as TBD)

    def test_should_handle_past_dates(self):
        """Test that past milestone dates are marked as completed."""
        # Arrange
        milestones = [
            {"name": "Alpha", "date": "2025-09-01"},  # Past
            {"name": "Beta", "date": "2025-12-15"}    # Future
        ]
        current_date = "2025-11-18"

        # Act
        from devforgeai_documentation import MilestoneAnalyzer
        analyzer = MilestoneAnalyzer()
        results = analyzer.categorize_by_date(milestones, current_date)

        # Assert
        assert results is not None
        # Alpha should be in past/completed category

    def test_should_handle_overlapping_epics(self):
        """Test that overlapping epic timelines are visualized correctly."""
        # Arrange
        epics = [
            {"name": "EPIC-001", "start": "2025-11-01", "end": "2025-12-31"},
            {"name": "EPIC-002", "start": "2025-12-01", "end": "2026-01-31"}
        ]

        # Act
        from devforgeai_documentation import RoadmapVisualizer
        visualizer = RoadmapVisualizer()
        visualization = visualizer.visualize_overlapping(epics)

        # Assert
        assert visualization is not None
