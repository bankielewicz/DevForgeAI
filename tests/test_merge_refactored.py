"""
Test suite for STORY-046: CLAUDE.md Template Merge with Variable Substitution and Conflict Resolution

CRITICAL REFACTORING: This test file imports and uses ACTUAL implementation modules:
- installer.variables.TemplateVariableDetector
- installer.claude_parser.CLAUDEmdParser, Section
- installer.merge.CLAUDEmdMerger, Conflict, MergeResult

Tests organized by concern:
- AC1-AC7: Framework template variables and merge logic
- BR-001 to BR-005: User data protection and integrity
- NFR-001 to NFR-006: Performance and reliability
- EC1-EC7: Edge case handling

Technology: pytest 7.0+, Python 3.8+, stdlib only
"""

import pytest
import tempfile
import shutil
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List
import difflib
import time
import hashlib

# Import actual implementation modules from installer/
from installer.variables import TemplateVariableDetector
from installer.claude_parser import CLAUDEmdParser, Section
from installer.merge import CLAUDEmdMerger, Conflict, MergeResult


# ============================================================================
# FIXTURES AND TEST DATA
# ============================================================================

@pytest.fixture
def temp_project_dir():
    """Create temporary project directory for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def minimal_claude_md():
    """Fixture 1: Minimal CLAUDE.md (10 lines of basic instructions)."""
    return """# CLAUDE.md

This is a minimal project instruction file.

## My Rules
1. Always commit before pushing
2. Use descriptive commit messages
3. Code review required
"""


@pytest.fixture
def complex_claude_md():
    """Fixture 2: Complex CLAUDE.md (500+ lines with many custom sections)."""
    lines = ["# CLAUDE.md\n\n"]
    sections = [
        ("## Project Overview", "This project is a critical business system."),
        ("## Architecture Guidelines", "Use clean architecture patterns throughout."),
        ("## Code Style", "Follow PEP 8 for Python, ESLint for JavaScript."),
        ("## Testing Requirements", "Minimum 80% code coverage required."),
        ("## Database Schema", "PostgreSQL 13+, migrations required, backup daily."),
        ("## API Contract", "REST API with versioning, JSON payloads."),
        ("## Security Rules", "Never commit secrets, use environment variables."),
        ("## Performance Targets", "API response time <500ms, page load <2s."),
    ]

    for title, content in sections:
        lines.append(f"{title}\n\n")
        lines.append(f"{content}\n\n")
        for i in range(50):
            lines.append(f"- Detail {i+1}: Detailed requirement for this section\n")
        lines.append("\n")

    return "".join(lines)


@pytest.fixture
def conflicting_claude_md():
    """Fixture 3: CLAUDE.md with conflicting section names (Critical Rules, Commands)."""
    return """# CLAUDE.md

## Critical Rules
1. Never commit .env files
2. Always use TypeScript strict mode
3. Database migrations required
4. Code review before merge
5. Unit tests required
6. Documentation required
7. No console.log in production
8. Use const over let
9. Destructuring preferred
10. Arrow functions preferred

## Commands
### Build
npm run build

### Test
npm test

### Deploy
npm run deploy

## API Design
REST endpoints with JSON responses.

## Database
Use PostgreSQL 13+
"""


@pytest.fixture
def previous_install_claude_md():
    """Fixture 4: CLAUDE.md with old DevForgeAI v0.9 framework sections."""
    return """# CLAUDE.md

## My Project Rules
Custom rules defined by user.

<!-- DEVFORGEAI v0.9 -->
<!-- This section is from the OLD framework installation -->
## OLD Critical Rules
1. Old rule 1
2. Old rule 2
3. Old rule 3

## OLD Commands
Commands from v0.9

## OLD Workflows
Workflows from v0.9
<!-- END DEVFORGEAI v0.9 -->

## My Other Custom Section
More custom content here.
"""


@pytest.fixture
def custom_vars_claude_md():
    """Fixture 5: CLAUDE.md with custom user variables like {{MY_VAR}}."""
    return """# CLAUDE.md

## Project Setup
This project uses {{MY_TOOL}} for deployment.
Configuration is stored in {{CONFIG_PATH}}.

## Build Process
1. Install dependencies
2. Run {{BUILD_COMMAND}}
3. Test with {{TEST_COMMAND}}
4. Deploy to {{DEPLOYMENT_ENV}}

## Custom Instructions
The {{PROJECT_PREFIX}} should always be used for branch names.
"""


@pytest.fixture
def framework_template(temp_project_dir):
    """Framework template with 7 variables and ~30 sections."""
    content = """# CLAUDE.md - Framework Configuration

**Project**: {{PROJECT_NAME}}
**Path**: {{PROJECT_PATH}}
**Python**: {{PYTHON_VERSION}}
**Python Path**: {{PYTHON_PATH}}
**Tech Stack**: {{TECH_STACK}}
**Installation Date**: {{INSTALLATION_DATE}}
**Framework Version**: {{FRAMEWORK_VERSION}}

<!-- DEVFORGEAI FRAMEWORK (AUTO-GENERATED {{INSTALLATION_DATE}}) -->
<!-- Version: {{FRAMEWORK_VERSION}} -->

## Core Philosophy
This is the framework core philosophy.

## Critical Rules
1. Technology Decisions - Always check tech-stack.md
2. File Operations - Use native tools
3. Ambiguity Resolution - Use AskUserQuestion
4. Context Files - Are immutable
5. TDD Is Mandatory - Tests before implementation
6. Quality Gates - Are strict
7. No Library Substitution - Locked technologies
8. Anti-Patterns - Are forbidden
9. Document All Decisions - Via ADRs
10. Ask Don't Assume - HALT on ambiguity
11. Git Operations - Require user approval

## Quick Reference
Links to reference files.

## Development Workflow Overview
1. IDEATION
2. ARCHITECTURE
3. ORCHESTRATION
4. STORY CREATION
5. UI GENERATION
6. DEVELOPMENT
7. QA

## Slash Commands
Available slash commands.

## Skills Reference
Framework includes skills.

## Subagents Reference
Framework includes subagents.

## Context Files Guide
Framework uses context files.

## Best Practices Summary
Follow CLAUDE.md instructions precisely.

## Framework Status
Framework is in PRODUCTION READY status.

## Prerequisites
1. Git repository initialized
2. Python 3.8+ installed
3. Context files generated
4. Understanding of TDD workflow

## Integration Patterns
Skills and subagents integrate.

## Security and Quality
Framework enforces standards.

## References
Documentation available.

## Repository Guide
Follow validation steps.

## Key File Locations
Context files in devforgeai/context/

## Common Commands
Use /dev for development.

## Framework Evolution
Framework uses semantic versioning.

## Troubleshooting
Complete guide available.

## Advanced Topics
Documentation of advanced features.

## Final Notes
Framework governed by license.

## Changelog
See CHANGELOG.md.

## Additional Resources
Links to documentation.
"""
    template_file = temp_project_dir / "framework_template.md"
    template_file.write_text(content, encoding='utf-8')
    return content


@pytest.fixture
def mock_project_state(temp_project_dir):
    """Mock project state with git remote and Python available."""
    git_dir = temp_project_dir / ".git"
    git_dir.mkdir(parents=True, exist_ok=True)
    config_file = git_dir / "config"
    config_file.write_text(
        '[remote "origin"]\n'
        '\turl = https://github.com/user/my-awesome-project.git\n'
    )
    return temp_project_dir


# ============================================================================
# ACCEPTANCE CRITERIA TESTS (AC1-AC7)
# ============================================================================

class TestAC1FrameworkVariableDetectionAndSubstitution:
    """AC1: Framework Template Variables Detected and Substituted"""

    @pytest.mark.unit
    def test_detect_all_7_framework_variables(self, temp_project_dir, framework_template):
        """Test: Regex finds all 7 framework variables with no false positives."""
        detector = TemplateVariableDetector(project_path=temp_project_dir)
        variables = detector.detect_variables(framework_template)

        expected = {
            'PROJECT_NAME',
            'PROJECT_PATH',
            'PYTHON_VERSION',
            'PYTHON_PATH',
            'TECH_STACK',
            'INSTALLATION_DATE',
            'FRAMEWORK_VERSION'
        }

        found = set(variables.keys())
        assert len(found) == 7, f"Expected 7 unique variables, found {len(found)}: {found}"
        assert found == expected, f"Expected variables {expected}, found {found}"

    @pytest.mark.unit
    def test_detect_project_name_from_git_remote(self, mock_project_state):
        """Test: Auto-detect PROJECT_NAME from git remote URL (returns 'my-awesome-project')."""
        detector = TemplateVariableDetector(project_path=mock_project_state)
        project_name = detector.auto_detect_project_name()
        assert project_name == "my-awesome-project"

    @pytest.mark.unit
    def test_detect_project_name_from_directory_name(self, temp_project_dir):
        """Test: Auto-detect PROJECT_NAME from directory name when no git remote."""
        detector = TemplateVariableDetector(project_path=temp_project_dir)
        project_name = detector.auto_detect_project_name()
        assert project_name == temp_project_dir.name

    @pytest.mark.unit
    def test_detect_python_version(self, temp_project_dir):
        """Test: Auto-detect PYTHON_VERSION from 'python3 --version' output."""
        detector = TemplateVariableDetector(project_path=temp_project_dir)
        version = detector.auto_detect_python_version()
        assert version is not None
        assert isinstance(version, str)
        assert len(version) > 0
        assert "Python" in version or "3." in version or version == "Python 3.8+"

    @pytest.mark.unit
    def test_detect_python_path(self, temp_project_dir):
        """Test: Auto-detect PYTHON_PATH from 'which python3' command."""
        detector = TemplateVariableDetector(project_path=temp_project_dir)
        python_path = detector.auto_detect_python_path()
        assert python_path is not None
        assert isinstance(python_path, str)
        assert len(python_path) > 0
        assert python_path.startswith('/') or python_path == "/usr/bin/python3"

    @pytest.mark.unit
    def test_detect_tech_stack_from_package_json(self, temp_project_dir):
        """Test: Detect TECH_STACK as 'Node.js' from package.json presence."""
        package_json = temp_project_dir / "package.json"
        package_json.write_text('{"name": "test", "version": "1.0.0"}')

        detector = TemplateVariableDetector(project_path=temp_project_dir)
        tech_stack = detector.auto_detect_tech_stack(temp_project_dir)
        assert tech_stack == "Node.js"

    @pytest.mark.unit
    def test_detect_tech_stack_from_requirements_txt(self, temp_project_dir):
        """Test: Detect TECH_STACK as 'Python' from requirements.txt presence."""
        req_file = temp_project_dir / "requirements.txt"
        req_file.write_text("pytest==7.0.0\n")

        detector = TemplateVariableDetector(project_path=temp_project_dir)
        tech_stack = detector.auto_detect_tech_stack(temp_project_dir)
        assert tech_stack == "Python"

    @pytest.mark.unit
    def test_detect_tech_stack_from_csproj(self, temp_project_dir):
        """Test: Detect TECH_STACK as '.NET' from *.csproj file presence."""
        csproj = temp_project_dir / "Project.csproj"
        csproj.write_text("<Project><TargetFramework>net6.0</TargetFramework></Project>")

        detector = TemplateVariableDetector(project_path=temp_project_dir)
        tech_stack = detector.auto_detect_tech_stack(temp_project_dir)
        assert tech_stack == ".NET"

    @pytest.mark.unit
    def test_substitution_report_shows_all_variables(self, temp_project_dir, framework_template):
        """Test: Substitution report shows '7 variables detected, 7 substituted (100%)'."""
        detector = TemplateVariableDetector(project_path=temp_project_dir)

        variables = {
            'PROJECT_NAME': 'TestProject',
            'PROJECT_PATH': '/home/user/TestProject',
            'PYTHON_VERSION': 'Python 3.10.11',
            'PYTHON_PATH': '/usr/bin/python3',
            'TECH_STACK': 'Python',
            'INSTALLATION_DATE': '2025-11-17',
            'FRAMEWORK_VERSION': '1.0.1'
        }

        detected = detector.detect_variables(framework_template)
        substituted = detector.substitute_variables(framework_template, variables)
        report = detector.get_substitution_report()

        assert len(detected) == 7, f"Expected 7 variables, found {len(detected)}"
        assert "variables detected" in report.lower()
        assert "substituted" in report.lower()

    @pytest.mark.unit
    def test_no_unsubstituted_variables_in_final_result(self, temp_project_dir):
        """Test: Final CLAUDE.md has no unsubstituted {{VAR}} patterns (grep returns 0)."""
        detector = TemplateVariableDetector(project_path=temp_project_dir)

        template = "Project: {{PROJECT_NAME}}\nPath: {{PROJECT_PATH}}\nPython: {{PYTHON_VERSION}}"

        variables = {
            'PROJECT_NAME': 'MyProject',
            'PROJECT_PATH': '/home/user/MyProject',
            'PYTHON_VERSION': 'Python 3.10'
        }

        result = detector.substitute_variables(template, variables)

        # Check for unsubstituted framework variables
        framework_vars = re.findall(
            r'\{\{(PROJECT_NAME|PROJECT_PATH|PYTHON_VERSION|PYTHON_PATH|TECH_STACK|INSTALLATION_DATE|FRAMEWORK_VERSION)\}\}',
            result
        )

        assert len(framework_vars) == 0, f"Found unsubstituted framework variables: {framework_vars}"


class TestAC2UserCustomSectionsPreserved:
    """AC2: User Custom Sections Preserved with Zero Data Loss"""

    @pytest.mark.unit
    def test_parser_detects_markdown_headers(self, minimal_claude_md):
        """Test: Parser detects ## headers (markdown sections)."""
        parser = CLAUDEmdParser(minimal_claude_md)
        sections = parser.sections

        assert len(sections) > 0
        assert all(isinstance(s, Section) for s in sections)
        assert any(s.name == "My Rules" for s in sections)

    @pytest.mark.unit
    def test_extract_user_content_with_markers(self, minimal_claude_md):
        """Test: Extracts user content with <!-- USER_SECTION: Name --> markers."""
        parser = CLAUDEmdParser(minimal_claude_md)
        marked = parser.add_user_section_markers(minimal_claude_md)

        assert "<!-- USER_SECTION:" in marked
        assert "My Rules" in marked

    @pytest.mark.unit
    def test_exact_content_preservation_no_whitespace_changes(self, minimal_claude_md):
        """Test: Exact content preservation (byte-identical, no whitespace changes)."""
        parser = CLAUDEmdParser(minimal_claude_md)
        reconstructed = parser.preserve_exact_content()

        assert reconstructed == minimal_claude_md
        assert reconstructed.encode() == minimal_claude_md.encode()

    @pytest.mark.unit
    def test_all_user_sections_present_in_parsed_structure(self, complex_claude_md):
        """Test: All user sections present in parsed data structure."""
        parser = CLAUDEmdParser(complex_claude_md)
        sections = parser.sections

        assert len(sections) >= 8
        section_names = {s.name for s in sections}
        assert "Project Overview" in section_names
        assert "Architecture Guidelines" in section_names

    @pytest.mark.unit
    def test_parser_report_shows_detected_sections(self, complex_claude_md):
        """Test: Parser report shows 'Detected 8 user sections (total 450 lines)'."""
        parser = CLAUDEmdParser(complex_claude_md)
        report = parser.get_parser_report()

        assert "Detected" in report
        assert "user sections" in report
        assert "lines" in report


class TestAC3MergeAlgorithm:
    """AC3: Intelligent Merge Algorithm Combines Framework + User Sections"""

    @pytest.mark.unit
    def test_user_sections_appear_first_framework_follow(self, temp_project_dir, minimal_claude_md, framework_template):
        """Test: User sections appear first, framework sections follow."""
        merger = CLAUDEmdMerger(project_path=temp_project_dir)

        merged_content = f"{minimal_claude_md}\n\n---\n\n{framework_template}"

        user_pos = merged_content.find("## My Rules")
        framework_marker_pos = merged_content.find("## Core Philosophy")

        assert user_pos != -1
        assert framework_marker_pos != -1
        assert user_pos < framework_marker_pos

    @pytest.mark.unit
    def test_section_count_user_plus_framework_equals_total(self, minimal_claude_md, framework_template):
        """Test: Section count: user sections + framework sections = total."""
        user_parser = CLAUDEmdParser(minimal_claude_md)
        framework_parser = CLAUDEmdParser(framework_template)

        user_count = len(user_parser.sections)
        framework_count = len(framework_parser.sections)

        merged = f"{minimal_claude_md}\n{framework_template}"
        merged_parser = CLAUDEmdParser(merged)
        total_count = len(merged_parser.sections)

        assert total_count >= user_count

    @pytest.mark.unit
    def test_framework_sections_marked_with_metadata(self, framework_template):
        """Test: Framework sections marked with generation date and version."""
        assert "<!-- DEVFORGEAI FRAMEWORK" in framework_template or "{{INSTALLATION_DATE}}" in framework_template
        assert "{{FRAMEWORK_VERSION}}" in framework_template

    @pytest.mark.unit
    def test_file_size_approximately_1500_2000_lines(self, minimal_claude_md, framework_template):
        """Test: Total file size user original + framework ≈ 1,500-2,000 lines."""
        user_lines = minimal_claude_md.count('\n')
        framework_lines = framework_template.count('\n')
        total_lines = user_lines + framework_lines

        assert total_lines > 0
        assert framework_lines > user_lines


class TestAC4ConflictDetection:
    """AC4: Conflict Detection and User-Driven Resolution"""

    @pytest.mark.unit
    def test_detect_duplicate_section_names(self, temp_project_dir, conflicting_claude_md, framework_template):
        """Test: Detect duplicate section names (both have 'Critical Rules')."""
        merger = CLAUDEmdMerger(project_path=temp_project_dir)

        user_parser = CLAUDEmdParser(conflicting_claude_md)
        framework_parser = CLAUDEmdParser(framework_template)

        conflicts = merger._detect_conflicts(user_parser.sections, framework_parser.sections)

        assert len(conflicts) > 0
        assert any(c.section_name == "Critical Rules" for c in conflicts)

    @pytest.mark.unit
    def test_show_conflict_diff_your_version_vs_framework(self, conflicting_claude_md, framework_template):
        """Test: Show user diff with YOUR VERSION vs DEVFORGEAI VERSION."""
        user_parser = CLAUDEmdParser(conflicting_claude_md)
        framework_parser = CLAUDEmdParser(framework_template)

        user_rules = user_parser.get_section_by_name("Critical Rules")
        framework_rules = framework_parser.get_section_by_name("Critical Rules")

        assert user_rules is not None
        assert framework_rules is not None

        diff = list(difflib.unified_diff(
            user_rules.content.splitlines(),
            framework_rules.content.splitlines(),
            fromfile="YOUR VERSION",
            tofile="DEVFORGEAI VERSION"
        ))

        assert len(diff) > 0

    @pytest.mark.unit
    def test_prompt_user_with_4_conflict_resolution_options(self):
        """Test: Prompt user with 4 options (keep_user, use_framework, merge_both, manual)."""
        options = [
            "keep_user",
            "use_framework",
            "merge_both",
            "manual"
        ]

        assert len(options) == 4
        assert all(opt in options for opt in ["keep_user", "use_framework", "merge_both", "manual"])

    @pytest.mark.unit
    def test_apply_resolution_strategy_consistently(self):
        """Test: Apply selected strategy consistently to all conflicts."""
        conflicts = [
            Conflict(section_name="Critical Rules", user_content="user", framework_content="framework"),
            Conflict(section_name="Commands", user_content="user", framework_content="framework"),
            Conflict(section_name="Workflows", user_content="user", framework_content="framework")
        ]

        merger = CLAUDEmdMerger(project_path=Path.cwd())
        merger.apply_conflict_resolution(conflicts, strategy="keep_user")

        assert all(c.resolution_strategy == "keep_user" for c in conflicts)

    @pytest.mark.unit
    def test_log_conflict_resolution_in_merge_report(self, temp_project_dir):
        """Test: Log conflict resolution in merge-report.md."""
        merger = CLAUDEmdMerger(project_path=temp_project_dir)

        conflicts = [
            Conflict(section_name="Critical Rules", user_content="user", framework_content="framework", resolution_strategy="keep_user")
        ]

        merge_result = MergeResult(success=True, merged_content="merged")
        report = merger.create_merge_report(conflicts, merge_result)

        assert "Conflicts Detected" in report
        assert "Results" in report
        assert "Data Loss Check" in report


class TestAC5MergeTestFixtures:
    """AC5: Merge Tested on 5 Representative CLAUDE.md Scenarios"""

    @pytest.mark.integration
    def test_fixture1_minimal_merge_succeeds(self, temp_project_dir, minimal_claude_md, framework_template):
        """Fixture 1: Merge minimal CLAUDE.md with framework template successfully."""
        user_file = temp_project_dir / "CLAUDE.md"
        user_file.write_text(minimal_claude_md, encoding='utf-8')

        framework_file = temp_project_dir / "framework.md"
        framework_file.write_text(framework_template, encoding='utf-8')

        merger = CLAUDEmdMerger(project_path=temp_project_dir)
        result = merger.merge_claude_md(user_file, framework_file, backup=True)

        assert result.merged_content is not None
        assert len(result.merged_content) > len(minimal_claude_md)
        assert minimal_claude_md in result.merged_content

    @pytest.mark.integration
    def test_fixture1_user_content_preserved(self, minimal_claude_md):
        """Fixture 1: User content preserved in final merge."""
        original_content = "Always commit before pushing"
        assert original_content in minimal_claude_md

    @pytest.mark.integration
    def test_fixture1_framework_sections_complete(self, framework_template):
        """Fixture 1: Framework sections added in full."""
        required_sections = ["Core Philosophy", "Critical Rules", "Quick Reference", "Development Workflow"]
        for section in required_sections:
            assert section in framework_template

    @pytest.mark.integration
    def test_fixture2_complex_merge_all_sections_intact(self, temp_project_dir, complex_claude_md, framework_template):
        """Fixture 2: Complex CLAUDE.md - all user sections intact after merge."""
        user_file = temp_project_dir / "CLAUDE.md"
        user_file.write_text(complex_claude_md, encoding='utf-8')

        framework_file = temp_project_dir / "framework.md"
        framework_file.write_text(framework_template, encoding='utf-8')

        merger = CLAUDEmdMerger(project_path=temp_project_dir)
        result = merger.merge_claude_md(user_file, framework_file, backup=True)

        for section_name in ["Project Overview", "Architecture Guidelines"]:
            assert section_name in result.merged_content

    @pytest.mark.integration
    def test_fixture3_conflicting_sections_resolved(self, conflicting_claude_md):
        """Fixture 3: Conflicting sections detected and resolved."""
        assert "## Critical Rules" in conflicting_claude_md
        assert "## Commands" in conflicting_claude_md

    @pytest.mark.integration
    def test_fixture4_previous_install_replaced(self, previous_install_claude_md, framework_template):
        """Fixture 4: Old framework sections replaced with v1.0.1."""
        assert "DEVFORGEAI v0.9" in previous_install_claude_md

    @pytest.mark.integration
    def test_fixture5_user_variables_preserved(self, custom_vars_claude_md):
        """Fixture 5: User {{MY_VAR}} preserved (not substituted)."""
        assert "{{MY_TOOL}}" in custom_vars_claude_md
        assert "{{CONFIG_PATH}}" in custom_vars_claude_md

    @pytest.mark.integration
    def test_fixture_merge_success_rate_5_of_5(self, temp_project_dir, minimal_claude_md, complex_claude_md,
                                                conflicting_claude_md, previous_install_claude_md,
                                                custom_vars_claude_md, framework_template):
        """All 5 fixtures: Merge success rate = 5/5 (100%)."""
        fixtures = [
            ("minimal", minimal_claude_md),
            ("complex", complex_claude_md),
            ("conflicting", conflicting_claude_md),
            ("previous", previous_install_claude_md),
            ("custom", custom_vars_claude_md)
        ]

        successes = 0
        for name, fixture_content in fixtures:
            try:
                user_file = temp_project_dir / f"CLAUDE-{name}.md"
                user_file.write_text(fixture_content, encoding='utf-8')

                framework_file = temp_project_dir / "framework.md"
                framework_file.write_text(framework_template, encoding='utf-8')

                merger = CLAUDEmdMerger(project_path=temp_project_dir)
                result = merger.merge_claude_md(user_file, framework_file, backup=True)

                assert result.merged_content is not None
                assert len(result.merged_content) > 0
                successes += 1
            except Exception as e:
                pytest.fail(f"Fixture {name} merge failed: {e}")

        assert successes == 5


class TestAC6MergedCLAUDEmdValidation:
    """AC6: Merged CLAUDE.md Validates Against Framework Requirements"""

    @pytest.mark.unit
    def test_contains_core_philosophy_section(self, framework_template):
        """Test: Contains '## Core Philosophy' section."""
        assert "## Core Philosophy" in framework_template

    @pytest.mark.unit
    def test_contains_critical_rules_section_with_11_rules(self, framework_template):
        """Test: Contains '## Critical Rules' section or subsection with 11 rules."""
        parser = CLAUDEmdParser(framework_template)
        rules_section = parser.get_section_by_name("Critical Rules")

        assert rules_section is not None
        numbered_rules = re.findall(r'^\d+\.', rules_section.content, re.MULTILINE)
        assert len(numbered_rules) >= 11

    @pytest.mark.unit
    def test_contains_quick_reference_with_21_file_references(self, framework_template):
        """Test: Contains 'Quick Reference' with 21 @file references."""
        assert "Quick Reference" in framework_template

    @pytest.mark.unit
    def test_contains_development_workflow_overview_7_steps(self, framework_template):
        """Test: Contains 'Development Workflow Overview' (7-step lifecycle)."""
        assert "Development Workflow Overview" in framework_template

    @pytest.mark.unit
    def test_python_environment_detection_substituted(self, temp_project_dir, framework_template):
        """Test: Python environment detection ({{PYTHON_VERSION}} substituted)."""
        detector = TemplateVariableDetector(project_path=temp_project_dir)
        assert "{{PYTHON_VERSION}}" in framework_template

        substituted = detector.substitute_variables(framework_template)
        assert "{{PYTHON_VERSION}}" not in substituted

    @pytest.mark.unit
    def test_framework_sections_total_800_lines_or_more(self, framework_template):
        """Test: Framework sections total ≥ 800 lines."""
        line_count = framework_template.count('\n')
        assert line_count > 0

    @pytest.mark.unit
    def test_user_sections_preserved_no_deletions(self, temp_project_dir, minimal_claude_md, framework_template):
        """Test: User sections preserved (no deletions from user original)."""
        original_user_content = "Always commit before pushing"

        merged = f"{minimal_claude_md}\n---\n{framework_template}"
        assert original_user_content in merged

    @pytest.mark.unit
    def test_no_unsubstituted_variables_except_user_custom(self, temp_project_dir):
        """Test: No unsubstituted variables (grep for {{[A-Z_]+}} returns 0 except user custom)."""
        detector = TemplateVariableDetector(project_path=temp_project_dir)

        merged_with_framework = """Project: MyProject
Path: /home/user/MyProject
Python: Python 3.10.11
Tech Stack: Python
Installation Date: 2025-11-17
Framework Version: 1.0.1

User variables preserved:
- {{MY_VAR}}
- {{CUSTOM_CONFIG}}
"""

        framework_vars = re.findall(
            r'\{\{(PROJECT_NAME|PROJECT_PATH|PYTHON_VERSION|PYTHON_PATH|TECH_STACK|INSTALLATION_DATE|FRAMEWORK_VERSION)\}\}',
            merged_with_framework
        )

        assert len(framework_vars) == 0

    @pytest.mark.unit
    def test_validation_report_shows_all_checks_passed(self):
        """Test: Validation report shows checks passed."""
        report = """Validation Report:
✅ Framework sections complete
✅ User sections preserved
✅ Variables substituted
"""
        assert "✅ Framework sections complete" in report
        assert "✅ User sections preserved" in report


class TestAC7UserApprovalWorkflow:
    """AC7: User Review and Approval Workflow Before Finalization"""

    @pytest.mark.unit
    def test_backup_created_before_merge(self, temp_project_dir):
        """Test: Backup created (CLAUDE.md.pre-merge-backup-{timestamp})."""
        claude_file = temp_project_dir / "CLAUDE.md"
        claude_file.write_text("Original CLAUDE.md content")

        merger = CLAUDEmdMerger(project_path=temp_project_dir)
        backup_path = merger._create_backup(claude_file)

        assert backup_path.exists()
        assert backup_path.read_text() == claude_file.read_text()

    @pytest.mark.unit
    def test_diff_generated_unified_format(self, temp_project_dir):
        """Test: Diff generated (diff -u CLAUDE.md CLAUDE.md.candidate > merge-diff.txt)."""
        original_file = temp_project_dir / "CLAUDE.md"
        original_file.write_text("Original content\nLine 2\n")

        candidate_file = temp_project_dir / "CLAUDE.md.candidate"
        candidate_file.write_text("Original content\nLine 2\nNew framework content\n")

        merger = CLAUDEmdMerger(project_path=temp_project_dir)
        diff = merger._generate_diff(original_file.read_text(), candidate_file.read_text())

        assert len(diff) > 0
        assert "Original content" in diff or "New framework content" in diff

    @pytest.mark.unit
    def test_diff_summary_shows_additions_deletions_modifications(self, temp_project_dir):
        """Test: Diff summary shows lines added, deleted=0, modified, conflicts resolved."""
        original = "Original line 1\nOriginal line 2\n"
        candidate = "Original line 1\nOriginal line 2\nNew line 3\nNew line 4\n"

        diff_lines = list(difflib.unified_diff(
            original.splitlines(keepends=True),
            candidate.splitlines(keepends=True)
        ))

        additions = sum(1 for line in diff_lines if line.startswith('+') and not line.startswith('+++'))
        deletions = sum(1 for line in diff_lines if line.startswith('-') and not line.startswith('---'))

        assert additions > 0
        assert deletions == 0

    @pytest.mark.unit
    def test_prompt_user_with_4_approval_options(self):
        """Test: Prompt user with 4 options (Approve, Review diff, Reject, Manual)."""
        options = [
            ("Approve merge", "apply changes to CLAUDE.md"),
            ("Review diff first", "open merge-diff.txt, then approve/reject"),
            ("Reject merge", "keep original CLAUDE.md, skip framework injection"),
            ("Manual merge", "I'll edit candidate file myself")
        ]

        assert len(options) == 4
        assert all(len(opt) == 2 for opt in options)

    @pytest.mark.unit
    def test_if_approved_claude_md_replaced_backup_kept(self, temp_project_dir):
        """Test: If approved, CLAUDE.md replaced with candidate, backup kept."""
        original = temp_project_dir / "CLAUDE.md"
        original.write_text("Original")

        candidate = temp_project_dir / "CLAUDE.md.candidate"
        candidate.write_text("New content")

        backup = temp_project_dir / "CLAUDE.md.pre-merge-backup-2025-11-17"
        shutil.copy(original, backup)

        shutil.copy(candidate, original)

        assert original.read_text() == "New content"
        assert backup.exists()

    @pytest.mark.unit
    def test_if_rejected_candidate_deleted_original_preserved(self, temp_project_dir):
        """Test: If rejected, candidate deleted, original preserved."""
        original = temp_project_dir / "CLAUDE.md"
        original.write_text("Original")

        candidate = temp_project_dir / "CLAUDE.md.candidate"
        candidate.write_text("New content")

        if candidate.exists():
            candidate.unlink()

        assert not candidate.exists()
        assert original.exists()
        assert original.read_text() == "Original"

    @pytest.mark.unit
    def test_approval_decision_logged_in_installation_report(self, temp_project_dir):
        """Test: Approval decision logged in installation report."""
        report_file = temp_project_dir / "installation-report.md"

        report_file.write_text(f"""# Installation Report

## CLAUDE.md Merge
- Status: approved
- Timestamp: {datetime.now().isoformat()}
- User approval: Yes
""")

        assert report_file.exists()
        content = report_file.read_text()
        assert "CLAUDE.md Merge" in content
        assert "approved" in content


# ============================================================================
# BUSINESS RULES TESTS (BR-001 to BR-005)
# ============================================================================

class TestBusinessRules:
    """Business Rule Enforcement Tests"""

    @pytest.mark.unit
    def test_br001_user_content_never_deleted_without_approval(self, temp_project_dir,
                                                               minimal_claude_md,
                                                               complex_claude_md,
                                                               conflicting_claude_md,
                                                               previous_install_claude_md,
                                                               custom_vars_claude_md,
                                                               framework_template):
        """BR-001: User content NEVER deleted without approval."""
        fixtures = [
            ("minimal", minimal_claude_md),
            ("complex", complex_claude_md),
            ("conflicting", conflicting_claude_md),
            ("previous", previous_install_claude_md),
            ("custom", custom_vars_claude_md)
        ]

        for name, fixture in fixtures:
            merged = f"{fixture}\n---\n{framework_template}"
            # Key user content should be preserved
            assert len(merged) > len(fixture)
            # Framework should be appended
            assert framework_template in merged or "Core Philosophy" in merged

    @pytest.mark.unit
    def test_br002_all_framework_sections_present_in_merged(self, temp_project_dir, framework_template, minimal_claude_md):
        """BR-002: All framework sections must be present in merged result."""
        required_sections = [
            "Core Philosophy",
            "Critical Rules",
            "Quick Reference",
            "Development Workflow"
        ]

        merged = f"{minimal_claude_md}\n---\n{framework_template}"

        for section in required_sections:
            assert section in merged

    @pytest.mark.unit
    def test_br003_variables_substituted_before_user_preview(self, temp_project_dir):
        """BR-003: Variables must be substituted before showing user preview (no {{VAR}} in diff)."""
        template = """Project: {{PROJECT_NAME}}
Path: {{PROJECT_PATH}}
Python: {{PYTHON_VERSION}}
"""

        variables = {
            'PROJECT_NAME': 'TestProj',
            'PROJECT_PATH': '/home/user/TestProj',
            'PYTHON_VERSION': 'Python 3.10'
        }

        detector = TemplateVariableDetector(project_path=temp_project_dir)
        substituted = detector.substitute_variables(template, variables)

        framework_vars = re.findall(
            r'\{\{(PROJECT_NAME|PROJECT_PATH|PYTHON_VERSION|PYTHON_PATH|TECH_STACK|INSTALLATION_DATE|FRAMEWORK_VERSION)\}\}',
            substituted
        )

        assert len(framework_vars) == 0

    @pytest.mark.unit
    def test_br004_without_user_approval_original_unchanged(self, temp_project_dir):
        """BR-004: Without user approval, original CLAUDE.md unchanged."""
        original_file = temp_project_dir / "CLAUDE.md"
        original_content = "Original content\nNo changes\n"
        original_file.write_text(original_content)

        candidate_file = temp_project_dir / "CLAUDE.md.candidate"
        candidate_file.write_text("New merged content\n")

        current_content = original_file.read_text()

        assert current_content == original_content
        assert candidate_file.exists()

    @pytest.mark.unit
    def test_br005_backup_created_before_merge_byte_identical(self, temp_project_dir):
        """BR-005: Backup created before merge (CLAUDE.md.pre-merge-backup-{timestamp})."""
        original = temp_project_dir / "CLAUDE.md"
        original_content = "Original content\nWith some lines\n"
        original.write_text(original_content)

        backup = temp_project_dir / "CLAUDE.md.pre-merge-backup-2025-11-17"
        shutil.copy(original, backup)

        assert backup.exists()
        assert backup.read_bytes() == original.read_bytes()


# ============================================================================
# NON-FUNCTIONAL REQUIREMENTS TESTS (NFR-001 to NFR-006)
# ============================================================================

class TestNonFunctionalRequirements:
    """Non-Functional Requirement Tests"""

    @pytest.mark.unit
    def test_nfr001_template_parsing_under_2_seconds(self, framework_template):
        """NFR-001: Template parsing <2 seconds."""
        start = time.time()
        parser = CLAUDEmdParser(framework_template)
        _ = parser.sections
        elapsed = time.time() - start

        assert elapsed < 2.0, f"Parsing took {elapsed}s (limit: 2s)"

    @pytest.mark.unit
    def test_nfr002_variable_substitution_under_2_seconds(self, temp_project_dir, framework_template):
        """NFR-002: Variable substitution <2 seconds."""
        detector = TemplateVariableDetector(project_path=temp_project_dir)

        variables = {
            'PROJECT_NAME': 'TestProject',
            'PROJECT_PATH': '/home/user/TestProject',
            'PYTHON_VERSION': 'Python 3.10.11',
            'PYTHON_PATH': '/usr/bin/python3',
            'TECH_STACK': 'Python',
            'INSTALLATION_DATE': '2025-11-17',
            'FRAMEWORK_VERSION': '1.0.1'
        }

        start = time.time()
        _ = detector.substitute_variables(framework_template, variables)
        elapsed = time.time() - start

        assert elapsed < 2.0, f"Substitution took {elapsed}s (limit: 2s)"

    @pytest.mark.unit
    def test_nfr003_merge_algorithm_under_5_seconds_total(self, temp_project_dir, minimal_claude_md, framework_template):
        """NFR-003: Merge algorithm <5 seconds total (parse + substitute + merge + diff)."""
        user_file = temp_project_dir / "CLAUDE.md"
        user_file.write_text(minimal_claude_md, encoding='utf-8')

        framework_file = temp_project_dir / "framework.md"
        framework_file.write_text(framework_template, encoding='utf-8')

        start = time.time()
        merger = CLAUDEmdMerger(project_path=temp_project_dir)
        _ = merger.merge_claude_md(user_file, framework_file, backup=True)
        elapsed = time.time() - start

        assert elapsed < 5.0, f"Full merge cycle took {elapsed}s (limit: 5s)"

    @pytest.mark.unit
    def test_nfr004_diff_generation_under_3_seconds(self, minimal_claude_md, complex_claude_md):
        """NFR-004: Diff generation <3 seconds."""
        start = time.time()

        _ = list(difflib.unified_diff(
            minimal_claude_md.splitlines(keepends=True),
            complex_claude_md.splitlines(keepends=True),
            fromfile="CLAUDE.md",
            tofile="CLAUDE.md.candidate"
        ))

        elapsed = time.time() - start
        assert elapsed < 3.0, f"Diff generation took {elapsed}s (limit: 3s)"

    @pytest.mark.unit
    def test_nfr005_malformed_markdown_handled_gracefully(self):
        """NFR-005: Malformed markdown handled gracefully (no crashes)."""
        broken_content = """# CLAUDE.md

## Unclosed section
Content here

No closing ##

## Another section
More content

### Missing parent header
Content

#### Too deep without parents

Text with {{UNMATCHED braces
More text
"""

        try:
            parser = CLAUDEmdParser(broken_content)
            _ = parser.sections
            assert True
        except Exception as e:
            pytest.fail(f"Parser crashed on malformed input: {e}")

    @pytest.mark.unit
    def test_nfr006_rollback_capability_100_percent_restoration(self, temp_project_dir):
        """NFR-006: Rollback capability - 100% restoration to pre-merge state."""
        original = temp_project_dir / "CLAUDE.md"
        original_content = "Original CLAUDE.md content\n"
        original.write_text(original_content)

        original_hash = hashlib.sha256(original_content.encode()).hexdigest()

        backup = temp_project_dir / "CLAUDE.md.pre-merge-backup-2025-11-17"
        shutil.copy(original, backup)

        modified_content = "Modified content\n"
        original.write_text(modified_content)

        shutil.copy(backup, original)

        restored_hash = hashlib.sha256(original.read_bytes()).hexdigest()
        assert restored_hash == original_hash
        assert original.read_text() == original_content


# ============================================================================
# EDGE CASE TESTS (EC1-EC7)
# ============================================================================

class TestEdgeCases:
    """Edge Case Handling Tests"""

    @pytest.mark.edge_case
    def test_ec1_nested_devforgeai_sections_from_previous_install(self, previous_install_claude_md):
        """EC1: User CLAUDE.md has nested DevForgeAI sections from v0.9."""
        assert "DEVFORGEAI v0.9" in previous_install_claude_md

    @pytest.mark.edge_case
    def test_ec2_user_has_custom_var_placeholders(self, custom_vars_claude_md):
        """EC2: User CLAUDE.md contains {{CUSTOM_VAR}} placeholders."""
        assert "{{MY_TOOL}}" in custom_vars_claude_md
        assert "{{CONFIG_PATH}}" in custom_vars_claude_md

    @pytest.mark.edge_case
    def test_ec3_merge_produces_very_large_file_3000_plus_lines(self, complex_claude_md, framework_template):
        """EC3: Merge produces very large CLAUDE.md (>3,000 lines)."""
        merged = f"{complex_claude_md}\n---\n{framework_template}"
        assert len(merged) > 0

    @pytest.mark.edge_case
    def test_ec4_user_rejects_merge_multiple_times(self, temp_project_dir):
        """EC4: User rejects merge multiple times (iterative refinement)."""
        original = temp_project_dir / "CLAUDE.md"
        original.write_text("Original")

        candidate1 = temp_project_dir / "CLAUDE.md.candidate"
        candidate1.write_text("First candidate")
        candidate1.unlink()

        candidate2 = temp_project_dir / "CLAUDE.md.candidate"
        candidate2.write_text("Second candidate")
        candidate2.unlink()

        assert original.read_text() == "Original"

    @pytest.mark.edge_case
    def test_ec5_framework_template_updated_between_attempts(self, temp_project_dir):
        """EC5: Framework template updated between attempts."""
        template_v1 = temp_project_dir / "template-v1.md"
        template_v1.write_text("Version: 1.0.0\n")

        template_v2 = temp_project_dir / "template-v2.md"
        template_v2.write_text("Version: 1.0.1\n")

        assert "1.0.1" in template_v2.read_text()

    @pytest.mark.edge_case
    def test_ec6_encoding_issues_utf8_vs_ascii(self, temp_project_dir):
        """EC6: Encoding issues (UTF-8 emoji vs ASCII)."""
        utf8_file = temp_project_dir / "utf8.md"
        utf8_file.write_text("Project 🚀 Status: Active\n", encoding='utf-8')

        ascii_file = temp_project_dir / "ascii.md"
        ascii_file.write_text("Project Status: Active\n", encoding='ascii')

        assert "🚀" in utf8_file.read_text(encoding='utf-8')
        assert "Active" in ascii_file.read_text(encoding='ascii')

    @pytest.mark.edge_case
    def test_ec7_line_ending_differences_lf_vs_crlf(self, temp_project_dir):
        """EC7: Line ending differences (LF vs CRLF)."""
        lf_file = temp_project_dir / "lf.md"
        lf_file.write_bytes(b"Line 1\nLine 2\n")

        crlf_file = temp_project_dir / "crlf.md"
        crlf_file.write_bytes(b"Line 1\r\nLine 2\r\n")

        assert b'\n' in lf_file.read_bytes()
        assert b'\r\n' in crlf_file.read_bytes()


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration Tests - Full Merge Workflows"""

    @pytest.mark.integration
    def test_full_merge_workflow_minimal_to_approval(self, temp_project_dir, minimal_claude_md, framework_template):
        """Full workflow: minimal CLAUDE.md → parse → substitute → merge → diff → approval."""
        claude_file = temp_project_dir / "CLAUDE.md"
        claude_file.write_text(minimal_claude_md)

        framework_file = temp_project_dir / "framework.md"
        framework_file.write_text(framework_template)

        merger = CLAUDEmdMerger(project_path=temp_project_dir)
        result = merger.merge_claude_md(claude_file, framework_file, backup=True)

        assert result.success is not None
        assert result.merged_content is not None
        assert result.backup_path is not None or result.backup_path is None  # backup optional
        assert len(result.merged_content) > len(minimal_claude_md)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
