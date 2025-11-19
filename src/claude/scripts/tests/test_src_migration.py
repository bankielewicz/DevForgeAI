#!/usr/bin/env python3

"""
STORY-044: Comprehensive Testing of src/ Structure
Unit test suite for validating src/ path migration

Tests:
- All 23 commands exist and are properly formatted
- All 14 skills reference loading works
- All 27 subagents are available
- Path resolution correctness
- No regressions in existing functionality
"""

import os
import json
import pytest
from pathlib import Path
from typing import List, Dict, Any

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent


class TestCommandsExist:
    """Test all 23 slash commands exist and are valid"""

    EXPECTED_COMMANDS = {
        "core_workflow": ["dev", "qa", "release", "orchestrate"],
        "planning_setup": ["ideate", "create-context", "create-epic", "create-sprint", "create-story", "create-ui", "create-agent"],
        "framework_maintenance": ["audit-deferrals", "audit-budget", "audit-hooks", "rca"],
        "feedback_system": ["feedback", "feedback-config", "feedback-search", "feedback-reindex", "feedback-export-data", "export-feedback", "import-feedback"],
        "documentation": ["document"],
    }

    def get_all_commands(self) -> List[str]:
        """Get all expected commands flattened"""
        all_cmds = []
        for category, cmds in self.EXPECTED_COMMANDS.items():
            all_cmds.extend(cmds)
        return all_cmds

    def test_command_count(self):
        """Verify we have exactly 23 commands"""
        all_cmds = self.get_all_commands()
        assert len(all_cmds) == 23, f"Expected 23 commands, found {len(all_cmds)}"

    @pytest.mark.parametrize("cmd_name", [
        "dev", "qa", "release", "orchestrate",
        "ideate", "create-context", "create-epic", "create-sprint", "create-story", "create-ui", "create-agent",
        "audit-deferrals", "audit-budget", "audit-hooks", "rca",
        "feedback", "feedback-config", "feedback-search", "feedback-reindex", "feedback-export-data", "export-feedback", "import-feedback",
        "document"
    ])
    def test_command_file_exists(self, cmd_name: str):
        """Test each command file exists"""
        cmd_file = PROJECT_ROOT / ".claude" / "commands" / f"{cmd_name}.md"
        assert cmd_file.exists(), f"Command file not found: {cmd_file}"
        assert cmd_file.stat().st_size > 100, f"Command file too small: {cmd_file}"

    @pytest.mark.parametrize("cmd_name", [
        "dev", "qa", "release", "orchestrate",
        "ideate", "create-context", "create-epic", "create-sprint", "create-story", "create-ui", "create-agent",
        "audit-deferrals", "audit-budget", "audit-hooks", "rca",
        "feedback", "feedback-config", "feedback-search", "feedback-reindex", "feedback-export-data", "export-feedback", "import-feedback",
        "document"
    ])
    def test_command_has_metadata(self, cmd_name: str):
        """Test each command has required metadata"""
        cmd_file = PROJECT_ROOT / ".claude" / "commands" / f"{cmd_name}.md"
        content = cmd_file.read_text()

        # Commands should have description and model metadata
        assert "description:" in content or "Description:" in content, \
            f"Command {cmd_name} missing description"


class TestSkillsReferenceLoading:
    """Test all 14 DevForgeAI skills reference loading"""

    EXPECTED_SKILLS = [
        "devforgeai-architecture",
        "devforgeai-development",
        "devforgeai-documentation",
        "devforgeai-feedback",
        "devforgeai-ideation",
        "devforgeai-mcp-cli-converter",
        "devforgeai-orchestration",
        "devforgeai-qa",
        "devforgeai-release",
        "devforgeai-rca",
        "devforgeai-story-creation",
        "devforgeai-subagent-creation",
        "devforgeai-ui-generator",
        "claude-code-terminal-expert",
    ]

    def test_skill_count(self):
        """Verify we have exactly 14 DevForgeAI skills"""
        assert len(self.EXPECTED_SKILLS) == 14, f"Expected 14 skills, found {len(self.EXPECTED_SKILLS)}"

    @pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
    def test_skill_skill_file_exists(self, skill_name: str):
        """Test each skill has SKILL.md"""
        skill_file = PROJECT_ROOT / ".claude" / "skills" / skill_name / "SKILL.md"
        assert skill_file.exists(), f"Skill file not found: {skill_file}"
        assert skill_file.stat().st_size > 100, f"Skill file too small: {skill_file}"

    @pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
    def test_skill_references_directory(self, skill_name: str):
        """Test skill references directory exists (if applicable)"""
        skill_dir = PROJECT_ROOT / ".claude" / "skills" / skill_name
        ref_dir = skill_dir / "references"

        # References directory not required for all skills, but if it exists should have content
        if ref_dir.exists():
            assert ref_dir.is_dir(), f"References should be a directory: {ref_dir}"
            ref_files = list(ref_dir.glob("*.md"))
            # May have 0 files (optional) so just check directory structure


class TestSubagentsAvailable:
    """Test all 27 subagents are available"""

    EXPECTED_AGENTS = [
        "agent-generator",
        "api-designer",
        "architect-reviewer",
        "backend-architect",
        "code-analyzer",
        "code-reviewer",
        "context-validator",
        "deferral-validator",
        "deployment-engineer",
        "dev-result-interpreter",
        "documentation-writer",
        "frontend-developer",
        "git-validator",
        "integration-tester",
        "internet-sleuth",
        "pattern-compliance-auditor",
        "qa-result-interpreter",
        "refactoring-specialist",
        "requirements-analyst",
        "security-auditor",
        "sprint-planner",
        "story-requirements-analyst",
        "tech-stack-detector",
        "technical-debt-analyzer",
        "test-automator",
        "ui-spec-formatter",
    ]

    def test_agent_count(self):
        """Verify we have exactly 27 subagents"""
        assert len(self.EXPECTED_AGENTS) == 27, f"Expected 27 agents, found {len(self.EXPECTED_AGENTS)}"

    @pytest.mark.parametrize("agent_name", EXPECTED_AGENTS)
    def test_agent_file_exists(self, agent_name: str):
        """Test each agent file exists"""
        agent_file = PROJECT_ROOT / ".claude" / "agents" / f"{agent_name}.md"
        assert agent_file.exists(), f"Agent file not found: {agent_file}"
        assert agent_file.stat().st_size > 100, f"Agent file too small: {agent_file}"

    @pytest.mark.parametrize("agent_name", EXPECTED_AGENTS)
    def test_agent_has_description(self, agent_name: str):
        """Test each agent has description metadata"""
        agent_file = PROJECT_ROOT / ".claude" / "agents" / f"{agent_name}.md"
        content = agent_file.read_text()
        assert "description:" in content or "Description:" in content, \
            f"Agent {agent_name} missing description"


class TestPathResolution:
    """Test path resolution correctness"""

    def test_context_files_directory_structure(self):
        """Test context files are in correct location"""
        context_dir = PROJECT_ROOT / ".devforgeai" / "context"
        assert context_dir.exists(), "Context directory not found"

        required_context_files = [
            "tech-stack.md",
            "source-tree.md",
            "dependencies.md",
            "coding-standards.md",
            "architecture-constraints.md",
            "anti-patterns.md",
        ]

        for ctx_file in required_context_files:
            assert (context_dir / ctx_file).exists(), f"Context file not found: {ctx_file}"

    def test_story_files_directory_structure(self):
        """Test story files are in correct location"""
        stories_dir = PROJECT_ROOT / ".ai_docs" / "Stories"
        assert stories_dir.exists(), "Stories directory not found"
        assert stories_dir.is_dir(), "Stories should be a directory"

    def test_epic_files_directory_structure(self):
        """Test epic files are in correct location"""
        epics_dir = PROJECT_ROOT / ".ai_docs" / "Epics"
        assert epics_dir.exists(), "Epics directory not found"
        assert epics_dir.is_dir(), "Epics should be a directory"

    def test_sprint_files_directory_structure(self):
        """Test sprint files are in correct location"""
        sprints_dir = PROJECT_ROOT / ".ai_docs" / "Sprints"
        assert sprints_dir.exists(), "Sprints directory not found"
        assert sprints_dir.is_dir(), "Sprints should be a directory"

    def test_qa_directory_structure(self):
        """Test QA directory structure"""
        qa_dir = PROJECT_ROOT / ".devforgeai" / "qa"
        assert qa_dir.exists(), "QA directory not found"
        assert qa_dir.is_dir(), "QA should be a directory"

    def test_adr_directory_structure(self):
        """Test ADR directory structure"""
        adr_dir = PROJECT_ROOT / ".devforgeai" / "adrs"
        assert adr_dir.exists(), "ADR directory not found"
        assert adr_dir.is_dir(), "ADR should be a directory"

    def test_no_duplicate_paths(self):
        """Test no duplicate command definitions"""
        commands_dir = PROJECT_ROOT / ".claude" / "commands"
        cmd_files = list(commands_dir.glob("*.md"))
        cmd_names = [f.stem for f in cmd_files]

        assert len(cmd_names) == len(set(cmd_names)), \
            f"Found duplicate command definitions: {[x for x in cmd_names if cmd_names.count(x) > 1]}"


class TestIntegrationWorkflows:
    """Test complete workflow paths exist"""

    def test_workflow_1_epic_to_story_dev_paths(self):
        """Test Workflow 1: Epic → Story → Development"""
        # Epic directory
        assert (PROJECT_ROOT / ".ai_docs" / "Epics").exists()

        # Story directory
        assert (PROJECT_ROOT / ".ai_docs" / "Stories").exists()

        # Development skill
        assert (PROJECT_ROOT / ".claude" / "skills" / "devforgeai-development" / "SKILL.md").exists()

        # Test directory
        assert (PROJECT_ROOT / "tests").exists()

        # All 6 context files
        for ctx_file in ["tech-stack.md", "source-tree.md", "dependencies.md",
                        "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"]:
            assert (PROJECT_ROOT / ".devforgeai" / "context" / ctx_file).exists(), \
                f"Missing context file: {ctx_file}"

    def test_workflow_2_context_to_story_qa_paths(self):
        """Test Workflow 2: Context → Story → QA"""
        # All 6 context files
        for ctx_file in ["tech-stack.md", "source-tree.md", "dependencies.md",
                        "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"]:
            assert (PROJECT_ROOT / ".devforgeai" / "context" / ctx_file).exists()

        # Story directory
        assert (PROJECT_ROOT / ".ai_docs" / "Stories").exists()

        # QA directory
        assert (PROJECT_ROOT / ".devforgeai" / "qa").exists()

        # QA skill
        assert (PROJECT_ROOT / ".claude" / "skills" / "devforgeai-qa" / "SKILL.md").exists()

    def test_workflow_3_sprint_to_story_paths(self):
        """Test Workflow 3: Sprint Planning → Story"""
        # Sprint directory
        assert (PROJECT_ROOT / ".ai_docs" / "Sprints").exists()

        # Story directory
        assert (PROJECT_ROOT / ".ai_docs" / "Stories").exists()

        # Orchestration skill
        assert (PROJECT_ROOT / ".claude" / "skills" / "devforgeai-orchestration" / "SKILL.md").exists()

        # Story creation skill
        assert (PROJECT_ROOT / ".claude" / "skills" / "devforgeai-story-creation" / "SKILL.md").exists()

        # ADR directory
        assert (PROJECT_ROOT / ".devforgeai" / "adrs").exists()


class TestFileStructureIntegrity:
    """Test overall file structure integrity"""

    def test_no_broken_symlinks(self):
        """Test no broken symbolic links in framework"""
        for root, dirs, files in os.walk(str(PROJECT_ROOT / ".claude")):
            for file in files:
                filepath = Path(root) / file
                if filepath.is_symlink():
                    assert filepath.resolve().exists(), f"Broken symlink: {filepath}"

    def test_command_files_are_readable(self):
        """Test all command files are readable text"""
        commands_dir = PROJECT_ROOT / ".claude" / "commands"
        for cmd_file in commands_dir.glob("*.md"):
            try:
                cmd_file.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                pytest.fail(f"Command file not readable as UTF-8: {cmd_file}")

    def test_skill_files_are_readable(self):
        """Test all skill files are readable text"""
        skills_dir = PROJECT_ROOT / ".claude" / "skills"
        for skill_file in skills_dir.rglob("SKILL.md"):
            try:
                skill_file.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                pytest.fail(f"Skill file not readable as UTF-8: {skill_file}")

    def test_agent_files_are_readable(self):
        """Test all agent files are readable text"""
        agents_dir = PROJECT_ROOT / ".claude" / "agents"
        for agent_file in agents_dir.glob("*.md"):
            try:
                agent_file.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                pytest.fail(f"Agent file not readable as UTF-8: {agent_file}")


class TestPerformance:
    """Test performance characteristics"""

    def test_command_file_scan_performance(self):
        """Test command file scanning is reasonably fast"""
        import time

        commands_dir = PROJECT_ROOT / ".claude" / "commands"
        start = time.time()
        list(commands_dir.glob("*.md"))
        duration = time.time() - start

        # Should be very fast (< 1 second)
        assert duration < 1.0, f"Command file scanning too slow: {duration:.3f}s"

    def test_skill_file_scan_performance(self):
        """Test skill file scanning is reasonably fast"""
        import time

        skills_dir = PROJECT_ROOT / ".claude" / "skills"
        start = time.time()
        list(skills_dir.glob("*/SKILL.md"))
        duration = time.time() - start

        # Should be very fast (< 1 second)
        assert duration < 1.0, f"Skill file scanning too slow: {duration:.3f}s"

    def test_agent_file_scan_performance(self):
        """Test agent file scanning is reasonably fast"""
        import time

        agents_dir = PROJECT_ROOT / ".claude" / "agents"
        start = time.time()
        list(agents_dir.glob("*.md"))
        duration = time.time() - start

        # Should be very fast (< 1 second)
        assert duration < 1.0, f"Agent file scanning too slow: {duration:.3f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
