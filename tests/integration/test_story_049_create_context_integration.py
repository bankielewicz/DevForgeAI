"""
Integration Tests for STORY-049: /create-context command refactoring

This test suite validates the refactored /create-context command works
correctly in realistic scenarios: greenfield, brownfield, with/without hooks.

Test Categories:
1. Workflow Integration Tests - Command executes with correct phases
2. Hook Integration Tests - Hook registration works correctly
3. Context File Generation Tests - All 6 context files created
4. Backward Compatibility Workflow Tests - Greenfield/brownfield scenarios
5. Error Handling Integration Tests - Error paths work correctly
6. End-to-End Scenarios - Complete workflow validation

TDD Phase: RED - All tests initially failing (no implementation yet)
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List
import json
import re


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def temp_project_dir() -> str:
    """Create temporary project directory for testing."""
    temp_dir = tempfile.mkdtemp(prefix='test_create_context_')
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def test_project_structure(temp_project_dir: str) -> Dict[str, Path]:
    """Set up test project structure."""
    base = Path(temp_project_dir)

    # Create minimal directory structure
    dirs = [
        base / '.claude' / 'commands',
        base / '.claude' / 'skills',
        base / 'devforgeai' / 'context',
        base / 'devforgeai' / 'adrs',
        base / 'devforgeai' / 'protocols',
        base / '.ai_docs' / 'Stories',
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    return {
        'base': base,
        'context': base / 'devforgeai' / 'context',
        'adrs': base / 'devforgeai' / 'adrs',
        'protocols': base / 'devforgeai' / 'protocols',
        'commands': base / '.claude' / 'commands',
    }


@pytest.fixture
def context_file_paths(test_project_structure: Dict[str, Path]) -> Dict[str, Path]:
    """Expected context file paths."""
    context_dir = test_project_structure['context']
    return {
        'tech_stack': context_dir / 'tech-stack.md',
        'source_tree': context_dir / 'source-tree.md',
        'dependencies': context_dir / 'dependencies.md',
        'coding_standards': context_dir / 'coding-standards.md',
        'architecture_constraints': context_dir / 'architecture-constraints.md',
        'anti_patterns': context_dir / 'anti-patterns.md',
    }


@pytest.fixture
def command_path() -> Path:
    """Path to the actual /create-context command."""
    return Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/create-context.md")


@pytest.fixture
def command_content(command_path: Path) -> str:
    """Load actual command content."""
    if not command_path.exists():
        pytest.skip(f"Command file not found: {command_path}")
    return command_path.read_text(encoding='utf-8')


# ============================================================================
# Workflow Integration Tests
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestWorkflowIntegration:
    """Test that command workflow phases execute in correct order."""

    def test_command_phase_sequence_documented(self, command_content: str):
        """Test: Command documents correct phase sequence."""
        # Expected sequence:
        # Phase 0: Pre-Flight Check (if exists)
        # Phase 1: Pre-Flight Check OR Git Initialization Check
        # Phase 2: Git Initialization Check OR Architecture Skill
        # Phase 3: Architecture Skill or Review
        # Phase N: Hook Integration

        phases = re.findall(r'###\s+Phase\s+([0-9NnA-Za-z]+)', command_content)

        # Should have at least 6 main phases
        assert len(phases) >= 6, (
            f"Insufficient phases documented: {phases}"
        )

    def test_pre_flight_check_comes_first(self, command_content: str):
        """Test: Pre-Flight Check phase comes before architecture skill invocation."""
        pre_flight_pos = command_content.find('Phase 1') if 'Phase 1' in command_content else \
                         command_content.find('Pre-Flight')
        skill_pos = command_content.find('Architecture Skill') or command_content.find('Architecture skill')

        assert pre_flight_pos < skill_pos if pre_flight_pos > 0 and skill_pos > 0 else True, (
            "Pre-Flight Check should come before Architecture Skill invocation"
        )

    def test_architecture_skill_invoked_before_validation(self, command_content: str):
        """Test: Architecture skill invocation comes before final validation."""
        skill_pos = command_content.find('Skill(command="devforgeai-architecture")')
        validation_pos = command_content.find('Validation')

        if skill_pos > 0 and validation_pos > 0:
            assert skill_pos < validation_pos, (
                "Architecture Skill should be invoked before validation"
            )

    def test_hook_integration_comes_after_validation(self, command_content: str):
        """Test: Hook integration phase comes after validation phase."""
        validation_pattern = r'###\s+Phase\s+6|[Ff]inal\s+[Vv]alidation'
        hook_pattern = r'###\s+Phase\s+N|[Ff]eedback.*[Hh]ook'

        validation_pos = command_content.find('Phase 6') if 'Phase 6' in command_content else \
                         command_content.find('Final Validation')
        hook_pos = command_content.find('Phase N') if 'Phase N' in command_content else \
                  re.search(hook_pattern, command_content, re.IGNORECASE)

        if validation_pos > 0 and hook_pos is not None:
            hook_pos_idx = hook_pos.start() if hasattr(hook_pos, 'start') else command_content.find('Phase N')
            assert validation_pos < hook_pos_idx, (
                "Hook Integration should come after Validation phase"
            )

    def test_success_report_comes_last(self, command_content: str):
        """Test: Success Report phase is documented as final phase."""
        # Should have Phase 7 or final phase that's a success report
        assert 'Phase 7' in command_content or 'Success Report' in command_content, (
            "Success Report phase missing (should be Phase 7 or final phase)"
        )


# ============================================================================
# Hook Integration Workflow Tests
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestHookIntegrationWorkflow:
    """Test that hook integration workflow is correctly structured."""

    def test_step_1_determine_status_documented(self, command_content: str):
        """Test: Step 1 (Determine Operation Status) is documented."""
        assert re.search(r'[Ss]tep\s+1.*[Dd]etermine.*[Ss]tatus', command_content) or \
               'Determine Operation Status' in command_content, (
            "Step 1 (Determine Operation Status) not documented"
        )

    def test_step_2_check_eligibility_documented(self, command_content: str):
        """Test: Step 2 (Check Hook Eligibility) is documented."""
        assert re.search(r'[Ss]tep\s+2.*[Cc]heck.*[Ee]ligibility', command_content) or \
               'Check Hook Eligibility' in command_content, (
            "Step 2 (Check Hook Eligibility) not documented"
        )

    def test_step_3_invoke_hooks_documented(self, command_content: str):
        """Test: Step 3 (Invoke Hooks if Eligible) is documented."""
        assert re.search(r'[Ss]tep\s+3.*[Ii]nvoke.*[Hh]ook', command_content) or \
               'Invoke Hooks' in command_content, (
            "Step 3 (Invoke Hooks) not documented"
        )

    def test_step_4_phase_complete_documented(self, command_content: str):
        """Test: Step 4 (Phase Complete) is documented."""
        assert re.search(r'[Ss]tep\s+4.*[Cc]omplete', command_content) or \
               'Phase Complete' in command_content, (
            "Step 4 (Phase Complete) not documented"
        )

    def test_hook_check_exit_code_handling(self, command_content: str):
        """Test: Command handles hook check exit codes (0=eligible, 1=not)."""
        assert 'exit code' in command_content.lower() or 'HOOK_CHECK_EXIT' in command_content, (
            "Command doesn't document exit code handling for hook checks"
        )

    def test_hook_invocation_non_blocking(self, command_content: str):
        """Test: Hook invocation is documented as non-blocking."""
        # Should have non-blocking error handling (|| operator or similar)
        assert '||' in command_content or 'non-blocking' in command_content.lower(), (
            "Hook invocation should be non-blocking (uses || error handling)"
        )

    def test_operation_status_verification_pattern(self, command_content: str):
        """Test: Step 1 includes operation status verification (file checks)."""
        # Should check for context files existing
        context_files = [
            'tech-stack.md',
            'dependencies.md',
            'coding-standards.md',
            'architecture-constraints.md',
            'anti-patterns.md',
            'source-tree.md'
        ]

        # At least some context file checks should be referenced
        found_checks = sum(1 for f in context_files if f in command_content)

        assert found_checks >= 2, (
            f"Operation status check insufficient: only {found_checks}/6 context files referenced"
        )


# ============================================================================
# Context File Generation Integration Tests
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestContextFileGeneration:
    """Test that all 6 required context files are generated."""

    def test_tech_stack_generation_documented(self, command_content: str):
        """Test: tech-stack.md generation documented."""
        assert 'tech-stack.md' in command_content, (
            "tech-stack.md generation not documented"
        )

    def test_source_tree_generation_documented(self, command_content: str):
        """Test: source-tree.md generation documented."""
        assert 'source-tree.md' in command_content, (
            "source-tree.md generation not documented"
        )

    def test_dependencies_generation_documented(self, command_content: str):
        """Test: dependencies.md generation documented."""
        assert 'dependencies.md' in command_content, (
            "dependencies.md generation not documented"
        )

    def test_coding_standards_generation_documented(self, command_content: str):
        """Test: coding-standards.md generation documented."""
        assert 'coding-standards.md' in command_content, (
            "coding-standards.md generation not documented"
        )

    def test_architecture_constraints_generation_documented(self, command_content: str):
        """Test: architecture-constraints.md generation documented."""
        assert 'architecture-constraints.md' in command_content, (
            "architecture-constraints.md generation not documented"
        )

    def test_anti_patterns_generation_documented(self, command_content: str):
        """Test: anti-patterns.md generation documented."""
        assert 'anti-patterns.md' in command_content, (
            "anti-patterns.md generation not documented"
        )

    def test_all_6_files_required_together(self, command_content: str):
        """Test: Documentation indicates all 6 files are created together."""
        # Should clarify that all 6 are created as a set (not optional)
        required_pattern = r'all\s+6|six.*files|all.*context.*files'

        assert re.search(required_pattern, command_content, re.IGNORECASE), (
            "Command should clarify that all 6 context files are required together"
        )

    def test_architecture_skill_delegates_file_generation(self, command_content: str):
        """Test: Architecture skill (not command) generates context files."""
        # Command should invoke skill, skill creates files
        assert 'Skill(command="devforgeai-architecture")' in command_content, (
            "Architecture skill invocation missing"
        )


# ============================================================================
# Backward Compatibility Workflow Tests
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestBackwardCompatibilityWorkflows:
    """Test greenfield and brownfield workflow scenarios."""

    def test_greenfield_mode_documented(self, command_content: str):
        """Test: Greenfield mode (no existing context) documented."""
        assert 'greenfield' in command_content.lower() or \
               'new project' in command_content.lower(), (
            "Greenfield mode not documented"
        )

    def test_brownfield_mode_documented(self, command_content: str):
        """Test: Brownfield mode (existing context) documented."""
        assert 'brownfield' in command_content.lower() or \
               'existing' in command_content.lower(), (
            "Brownfield mode not documented"
        )

    def test_existing_context_detection_documented(self, command_content: str):
        """Test: Command documents detecting existing context files."""
        assert 'existing' in command_content.lower() or \
               'context files exist' in command_content.lower(), (
            "Existing context detection not documented"
        )

    def test_merge_option_documented(self, command_content: str):
        """Test: Merge option for existing context documented."""
        assert 'merge' in command_content.lower(), (
            "Merge option for existing context not documented"
        )

    def test_overwrite_option_documented(self, command_content: str):
        """Test: Overwrite option for existing context documented."""
        assert 'overwrite' in command_content.lower(), (
            "Overwrite option for existing context not documented"
        )

    def test_abort_option_documented(self, command_content: str):
        """Test: Abort option documented (user can cancel)."""
        assert 'abort' in command_content.lower() or \
               'cancel' in command_content.lower(), (
            "Abort/cancel option not documented"
        )


# ============================================================================
# Error Handling Integration Tests
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestErrorHandlingIntegration:
    """Test error handling for various failure scenarios."""

    def test_error_handling_section_exists(self, command_content: str):
        """Test: Error Handling section documented."""
        assert re.search(r'##\s+Error\s+Handling', command_content), (
            "Error Handling section missing"
        )

    def test_error_handling_contexts_documented(self, command_content: str):
        """Test: Multiple error scenarios documented."""
        error_patterns = [
            'existing',  # Context exists
            'failed',    # Skill failed
            'validation', # Validation failed
        ]

        found_errors = sum(1 for pattern in error_patterns if pattern in command_content.lower())

        assert found_errors >= 2, (
            f"Insufficient error scenarios documented: {found_errors} (expected: ≥2)"
        )

    def test_missing_context_files_error_documented(self, command_content: str):
        """Test: Error when context files missing documented."""
        assert re.search(r'[Mm]issing|[Nn]ot\s+found|[Ee]rror', command_content), (
            "Missing context files error not documented"
        )

    def test_architecture_skill_failure_error_documented(self, command_content: str):
        """Test: Error when architecture skill fails documented."""
        # Should have error recovery for skill failure
        assert re.search(r'[Ss]kill\s+[Ff]ailed|[Ss]kill.*[Ee]rror', command_content), (
            "Architecture skill failure error not documented"
        )

    def test_error_messages_user_friendly(self, command_content: str):
        """Test: Error messages are user-friendly (not cryptic)."""
        # Should have readable error descriptions
        assert 'Action:' in command_content or 'Recovery:' in command_content, (
            "Error handling doesn't include clear user-friendly actions"
        )


# ============================================================================
# End-to-End Scenario Tests
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestEndToEndScenarios:
    """Test complete workflows from start to finish."""

    def test_greenfield_complete_workflow_documented(self, command_content: str):
        """Test: Complete greenfield workflow (new project) documented."""
        # Should show full flow: no context → generate context → success

        # Check for sequential flow
        has_initial_check = 'existing' in command_content.lower() or 'check' in command_content.lower()
        has_generation = 'generate' in command_content.lower() or 'create' in command_content.lower()
        has_validation = 'validation' in command_content.lower()
        has_success = 'success' in command_content.lower()

        assert has_initial_check and has_generation and has_validation and has_success, (
            "Greenfield workflow not fully documented"
        )

    def test_brownfield_complete_workflow_documented(self, command_content: str):
        """Test: Complete brownfield workflow (existing context) documented."""
        # Should show: existing context → user chooses action (merge/overwrite/abort) → result

        has_detection = 'existing' in command_content.lower()
        has_options = 'merge' in command_content.lower() and \
                     'overwrite' in command_content.lower() and \
                     ('abort' in command_content.lower() or 'cancel' in command_content.lower())

        assert has_detection and has_options, (
            "Brownfield workflow not fully documented"
        )

    def test_successful_completion_criteria_documented(self, command_content: str):
        """Test: Success criteria for command completion documented."""
        assert 'Success' in command_content or 'completion' in command_content.lower(), (
            "Success criteria for command completion not documented"
        )

    def test_next_steps_after_success_documented(self, command_content: str):
        """Test: Next steps after successful context creation documented."""
        next_steps_keywords = [
            'next',
            'then',
            'after',
            'proceed',
            'use'
        ]

        found_guidance = sum(1 for kw in next_steps_keywords if kw in command_content.lower())

        assert found_guidance >= 2, (
            f"Next steps guidance insufficient: {found_guidance} keywords found"
        )


# ============================================================================
# Pattern File Integration Tests
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestPatternFileIntegration:
    """Test that refactored command properly uses externalized pattern file."""

    def test_pattern_file_path_correct(self, command_content: str):
        """Test: Pattern file path in Read() tool is correct."""
        # Should be: devforgeai/protocols/hook-integration-pattern.md
        assert 'devforgeai/protocols/hook-integration-pattern.md' in command_content, (
            "Incorrect pattern file path or missing Read tool reference"
        )

    def test_pattern_file_read_in_hook_phase(self, command_content: str):
        """Test: Pattern file is Read in Phase N (hook integration)."""
        # Find Phase N section
        phase_n_pattern = r'###\s+Phase\s+N.*?(?=###|##|$)'
        phase_n_match = re.search(phase_n_pattern, command_content, re.DOTALL | re.IGNORECASE)

        if phase_n_match:
            phase_n_content = phase_n_match.group(0)
            assert 'Read(' in phase_n_content and 'hook-integration' in phase_n_content, (
                "Pattern file not referenced in Phase N with Read tool"
            )

    def test_pattern_file_reference_clear(self, command_content: str):
        """Test: Pattern file reference is clear (says what to read and why)."""
        # Should have text like "Reference external pattern documentation"
        assert re.search(r'[Rr]eference.*[Pp]attern|[Pp]attern.*[Rr]eference|[Rr]ead.*pattern', command_content), (
            "Pattern file reference not clearly explained"
        )


# ============================================================================
# Regression Tests (Ensure nothing broke)
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestRegressionPrevention:
    """Test that refactoring didn't break existing functionality."""

    def test_no_critical_sections_removed(self, command_content: str):
        """Test: All critical workflow sections still present."""
        critical_sections = [
            'Phase',
            'Git',
            'Architecture',
            'Validation',
            'Success'
        ]

        missing = [s for s in critical_sections if s not in command_content]

        assert not missing, (
            f"Critical sections missing after refactoring: {missing}"
        )

    def test_no_broken_tool_calls(self, command_content: str):
        """Test: All tool calls are valid (Read, Write, Skill, Task, etc.)."""
        # Check for complete tool invocations
        tool_patterns = [
            r'Read\([^)]+\)',
            r'Write\([^)]+\)',
            r'Skill\([^)]+\)',
            r'Task\([^)]+\)',
            r'Glob\([^)]+\)',
            r'Grep\([^)]+\)',
            r'Edit\([^)]+\)',
            r'AskUserQuestion',
        ]

        # Check if command uses any tools
        has_tools = any(re.search(pattern, command_content) for pattern in tool_patterns)

        # If using tools, verify they look valid (basic sanity check)
        if has_tools:
            # Should have matched parentheses
            open_parens = command_content.count('(')
            close_parens = command_content.count(')')

            assert open_parens >= close_parens - 2, (  # Allow small margin for error
                f"Unbalanced parentheses in tool calls: "
                f"{open_parens} open, {close_parens} close"
            )

    def test_markdown_syntax_valid(self, command_content: str):
        """Test: Markdown syntax is valid (after refactoring)."""
        # Count headers
        headers = len(re.findall(r'^#+\s+\w+', command_content, re.MULTILINE))

        assert headers >= 5, (
            f"Insufficient headers after refactoring: {headers} found"
        )

        # Check for balanced backticks
        triple_backticks = command_content.count('```')
        assert triple_backticks % 2 == 0, (
            f"Unbalanced triple backticks: {triple_backticks}"
        )


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
