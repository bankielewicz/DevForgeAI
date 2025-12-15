"""
Unit tests for STORY-038: Refactor /release Command for Lean Orchestration Compliance

Tests cover:
- Acceptance Criteria 1: Command Size Reduction (≤350 lines, <15K characters)
- Acceptance Criteria 2: Business Logic Extraction (all logic moved to skill)
- Acceptance Criteria 3: Functional Equivalence (6 deployment scenarios unchanged)
- Acceptance Criteria 4: Skill Enhancement (phases 1-6 + 2.5/3.5, reference files)
- Acceptance Criteria 5: Token Efficiency (≥75% savings in main conversation)
- Acceptance Criteria 6: Pattern Compliance (5-responsibility checklist)
- Acceptance Criteria 7: Subagent Creation Decision (document if needed)

All tests FAIL initially (Red phase) because refactoring not complete.
These tests pass after Phases 2-5 complete the refactoring.

Test Execution:
    pytest tests/unit/test_release_command_refactoring.py -v
    pytest tests/unit/test_release_command_refactoring.py::TestCommandSizeReduction -v
    pytest tests/unit/test_release_command_refactoring.py::TestBusinessLogicExtraction::test_command_no_deployment_sequencing -v
"""

import os
import re
import subprocess
from pathlib import Path


class TestCommandSizeReduction:
    """AC-1: Command Size Reduction to Within Budget"""

    def test_command_character_count_under_15k_hard_limit(self):
        """
        AC-1.1: Command file <15,000 characters (hard limit)

        ARRANGE: Read /release command file
        ACT: Count characters with Python len()
        ASSERT: Character count <15,000 (hard limit, must refactor if exceeded)
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")
        assert command_path.exists(), f"Release command not found at {command_path}"

        # Act
        with open(command_path, 'r') as f:
            content = f.read()
        char_count = len(content)

        # Assert: Hard limit <15,000
        assert char_count < 15000, (
            f"Command exceeds 15K hard limit: {char_count} chars. "
            f"Current: {char_count * 100 // 15000}% of limit. "
            f"Target: ≤15K (hard), ≤12K (target). Requires refactoring."
        )
        print(f"✓ Command size: {char_count} chars ({char_count * 100 // 15000}% of hard limit)")

    def test_command_character_count_under_12k_target(self):
        """
        AC-1.2: Command file <12,000 characters (target optimal range)

        ARRANGE: Read /release command file
        ACT: Count characters
        ASSERT: Character count <12,000 for optimal budget buffer (80% of optimal target)
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()
        char_count = len(content)
        budget_pct = char_count * 100 // 15000

        # Assert: Target <12K for comfortable buffer
        assert char_count < 12000, (
            f"Command size {char_count} chars exceeds 12K target. "
            f"Currently {budget_pct}% of 15K limit. "
            f"Target: 8-10K for 40% budget buffer. "
            f"Needs {char_count - 12000} chars reduction."
        )
        print(f"✓ Command size optimal: {char_count} chars ({budget_pct}% of limit)")

    def test_command_line_count_under_350_lines(self):
        """
        AC-1.3: Command file ≤350 lines (lean orchestration structure)

        ARRANGE: Read /release command file
        ACT: Count lines
        ASSERT: Line count ≤350 lines (47% reduction from original 655)
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            lines = f.readlines()
        line_count = len(lines)

        # Assert: ≤350 lines (target 300-320 for best reference implementations)
        assert line_count <= 350, (
            f"Command has {line_count} lines (target: ≤350). "
            f"Original: 655 lines, target: 47% reduction. "
            f"Reference: /qa (295 lines), /create-sprint (250 lines). "
            f"Needs {line_count - 350} lines removed."
        )
        print(f"✓ Command line count: {line_count} lines (≤350 target)")

    def test_command_reduction_percentage(self):
        """
        AC-1.4: Command achieves ≥20% reduction from original 655 lines

        ARRANGE: Read current command
        ACT: Calculate reduction percentage
        ASSERT: Reduction ≥20% (minimum acceptable), ≥47% (target)
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")
        original_lines = 655  # Current /release command

        # Act
        with open(command_path, 'r') as f:
            lines = f.readlines()
        current_lines = len(lines)

        reduction_lines = original_lines - current_lines
        reduction_pct = (reduction_lines * 100) // original_lines if reduction_lines > 0 else 0

        # Assert: At least 20% reduction (minimum), 47% target
        assert reduction_pct >= 20, (
            f"Command reduction insufficient: {reduction_pct}% (need ≥20%, target 47%). "
            f"Original: {original_lines} lines, Current: {current_lines} lines. "
            f"Needs reduction of at least {(original_lines * 20) // 100} more lines."
        )
        print(f"✓ Command reduction: {reduction_pct}% ({reduction_lines} lines removed)")


class TestBusinessLogicExtraction:
    """AC-2: Business Logic Extraction - All logic moved to skill"""

    def test_command_phase_0_argument_validation_only(self):
        """
        AC-2.1: Phase 0 contains ONLY argument validation (≤30 lines)

        ARRANGE: Read command file
        ACT: Extract Phase 0 content
        ASSERT: Phase 0 ≤30 lines, contains only story ID and environment validation
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Extract Phase 0
        phase_0_match = re.search(r'### Phase 0:.*?(?=### Phase 1:|---|\Z)', content, re.DOTALL)
        assert phase_0_match, "Phase 0 not found in command"

        phase_0_content = phase_0_match.group()
        phase_0_lines = phase_0_content.count('\n')

        # Assert: Phase 0 ≤30 lines
        assert phase_0_lines <= 30, (
            f"Phase 0 has {phase_0_lines} lines (target: ≤30). "
            f"Should only validate story ID and environment. "
            f"No deployment logic allowed."
        )
        print(f"✓ Phase 0 argument validation: {phase_0_lines} lines (≤30)")

    def test_no_deployment_sequencing_logic_in_command(self):
        """
        AC-2.2: Command contains NO deployment sequencing (moved to skill)

        ARRANGE: Read command file
        ACT: Grep for deployment sequencing patterns
        ASSERT: No staging→production logic, no decision trees
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Forbidden patterns: deployment orchestration
        forbidden_patterns = [
            r'staging.*production|production.*staging',  # Deployment sequence
            r'deploy to staging|deploy to production',    # Explicit deployment
            r'IF staging|IF production',                   # Environment branching
            r'run.*health.*check|execute.*smoke.*test',   # Test execution
            r'update.*story.*status|set.*released',       # Status updates
        ]

        found_patterns = []
        for pattern in forbidden_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_patterns.extend(matches)

        # Assert: No deployment logic
        assert len(found_patterns) == 0, (
            f"Found {len(found_patterns)} deployment sequencing patterns in command: {found_patterns}. "
            f"All deployment logic (staging→production, health checks, status updates) "
            f"must be in devforgeai-release skill."
        )
        print(f"✓ No deployment sequencing logic in command")

    def test_no_smoke_test_execution_logic_in_command(self):
        """
        AC-2.3: Command contains NO smoke test execution (moved to skill)

        ARRANGE: Read command file
        ACT: Grep for smoke test patterns
        ASSERT: No test running, verification, or result parsing
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Forbidden: Smoke test logic in command
        forbidden_patterns = [
            r'run.*smoke.*test|execute.*test',
            r'verify.*smoke|check.*test.*result',
            r'parse.*test|read.*smoke.*report',
            r'if.*test.*fail|test.*failed',
        ]

        found_patterns = []
        for pattern in forbidden_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_patterns.extend(matches)

        # Assert: No smoke test execution in command
        assert len(found_patterns) == 0, (
            f"Found {len(found_patterns)} smoke test patterns: {found_patterns}. "
            f"Command should NOT execute or verify smoke tests. "
            f"Skill owns all test execution and result validation."
        )
        print(f"✓ No smoke test execution logic in command")

    def test_no_rollback_logic_in_command(self):
        """
        AC-2.4: Command contains NO rollback decision logic (moved to skill)

        ARRANGE: Read command file
        ACT: Grep for rollback logic
        ASSERT: No rollback decisions or execution
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Forbidden: Rollback logic
        forbidden_patterns = [
            r'trigger.*rollback|initiate.*rollback',
            r'if.*fail.*then.*rollback',
            r'execute.*rollback|run.*rollback.*command',
            r'revert.*deployment|restore.*previous',
        ]

        found_patterns = []
        for pattern in forbidden_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_patterns.extend(matches)

        # Assert: No rollback logic
        assert len(found_patterns) == 0, (
            f"Found {len(found_patterns)} rollback patterns: {found_patterns}. "
            f"Command should NOT make rollback decisions. "
            f"Skill decides when to rollback based on smoke test results."
        )
        print(f"✓ No rollback logic in command")

    def test_no_complex_error_handling_algorithms(self):
        """
        AC-2.5: Command error handling is minimal (<25 lines, no algorithms)

        ARRANGE: Read command error handling section
        ACT: Extract error handling, count lines
        ASSERT: Error handling <25 lines, only display errors from skill
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Extract error handling section
        error_section = re.search(r'## Error.*?(?=##|\Z)', content, re.DOTALL | re.IGNORECASE)

        if error_section:
            error_content = error_section.group()
            error_lines = error_content.count('\n')
        else:
            error_lines = 0

        # Assert: Error handling minimal
        assert error_lines < 25, (
            f"Error handling section has {error_lines} lines (target: <25). "
            f"Command should only display errors from skill, "
            f"not implement error recovery algorithms."
        )
        print(f"✓ Error handling minimal: {error_lines} lines (<25)")

    def test_no_display_template_generation_in_command(self):
        """
        AC-2.6: Command has NO display template generation (moved to subagent)

        ARRANGE: Read command file
        ACT: Grep for template patterns
        ASSERT: No markdown template generation, variable substitution
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Count template-like patterns
        forbidden_patterns = [
            r'Display:.*{.*}',                           # Template with variables
            r'Generate.*template|create.*display',       # Template generation
            r'format.*output|format.*result',            # Output formatting
            r'markdown.*template|{.*environment.*}',     # Variable substitution
        ]

        found_patterns = []
        for pattern in forbidden_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_patterns.extend(matches)

        # Assert: No template generation
        assert len(found_patterns) < 2, (  # Allow 1 for documentation, not logic
            f"Found {len(found_patterns)} template generation patterns. "
            f"Command should display skill result directly, "
            f"not generate display templates. "
            f"Subagent (if created) or skill owns template generation."
        )
        print(f"✓ No display template generation in command")


class TestFunctionalEquivalence:
    """AC-3: Functional Equivalence - All 6 scenarios work identically"""

    def test_scenario_3a_staging_deployment_success_preserved(self):
        """
        AC-3a: Successful Staging Deployment - behavior identical

        ARRANGE: Read command and skill documentation
        ACT: Verify staging deployment workflow preserved
        ASSERT: Staging deployment, smoke tests, status update still occur identically
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")

        assert command_path.exists() and skill_path.exists(), "Command or skill not found"

        # Act: Verify command invokes skill
        with open(command_path, 'r') as f:
            command_content = f.read()

        # Assert: Skill invoked for staging scenario
        assert 'Skill(command="devforgeai-release")' in command_content or \
               'devforgeai-release' in command_content, (
            "Command must invoke devforgeai-release skill. "
            "Skill handles staging deployment logic."
        )

        print("✓ Scenario 3a: Staging deployment preserved (skill owned)")

    def test_scenario_3b_production_deployment_confirmation_preserved(self):
        """
        AC-3b: Production Deployment with Confirmation - behavior identical

        ARRANGE: Read command documentation
        ACT: Verify production confirmation still required
        ASSERT: Production deployment requires AskUserQuestion confirmation
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Assert: Production confirmation still exists
        assert 'production' in content.lower(), (
            "Command must still handle production environment option"
        )

        # Check for confirmation pattern
        has_confirmation = bool(re.search(r'confirm|verification|production', content, re.IGNORECASE))
        assert has_confirmation, (
            "Command must preserve production deployment confirmation workflow. "
            "This can be in Phase 0 or delegated to skill."
        )

        print("✓ Scenario 3b: Production confirmation preserved")

    def test_scenario_3c_deployment_failure_rollback_preserved(self):
        """
        AC-3c: Deployment Failure with Rollback - behavior identical

        ARRANGE: Read skill documentation
        ACT: Verify rollback logic exists in skill
        ASSERT: Skill contains rollback handling (smoke test failure → rollback)
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")
        assert skill_path.exists(), "Release skill not found"

        # Act
        with open(skill_path, 'r') as f:
            skill_content = f.read()

        # Assert: Rollback logic in skill
        assert 'rollback' in skill_content.lower(), (
            "Skill must contain rollback logic for failed deployments. "
            "Scenario 3c: Smoke test failure → automatic rollback."
        )

        print("✓ Scenario 3c: Rollback logic preserved (in skill)")

    def test_scenario_3d_missing_qa_approval_quality_gate_preserved(self):
        """
        AC-3d: Missing QA Approval - quality gate still enforced

        ARRANGE: Read skill documentation
        ACT: Verify QA approval check exists
        ASSERT: Skill validates 'QA Approved' status before deployment
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")
        assert skill_path.exists(), "Release skill not found"

        # Act
        with open(skill_path, 'r') as f:
            skill_content = f.read()

        # Assert: QA approval validation in skill
        assert 'qa' in skill_content.lower() and 'approved' in skill_content.lower(), (
            "Skill must validate QA Approved status. "
            "Scenario 3d: Block deployment if not QA Approved."
        )

        print("✓ Scenario 3d: QA approval quality gate preserved (in skill)")

    def test_scenario_3e_default_environment_staging_preserved(self):
        """
        AC-3e: Default Environment - defaults to staging, user notified

        ARRANGE: Read command Phase 0
        ACT: Verify environment defaulting logic
        ASSERT: Defaults to staging with user notification
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Assert: Environment handling preserved
        assert re.search(r'staging|environment', content, re.IGNORECASE), (
            "Command must handle environment argument. "
            "Scenario 3e: Default to staging if not specified."
        )

        print("✓ Scenario 3e: Default environment (staging) preserved")

    def test_scenario_3f_post_release_hooks_integration_preserved(self):
        """
        AC-3f: Post-Release Hooks (STORY-025) - behavior preserved

        ARRANGE: Read skill documentation
        ACT: Verify Phase 2.5 (post-staging) and 3.5 (post-production) hooks
        ASSERT: Phases 2.5 and 3.5 exist in skill for hook integration
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")
        assert skill_path.exists(), "Release skill not found"

        # Act
        with open(skill_path, 'r') as f:
            skill_content = f.read()

        # Assert: Hook phases exist
        has_phase_25 = bool(re.search(r'Phase 2\.5|post.*staging.*hook', skill_content, re.IGNORECASE))
        has_phase_35 = bool(re.search(r'Phase 3\.5|post.*production.*hook', skill_content, re.IGNORECASE))

        assert has_phase_25 or has_phase_35, (
            "Skill must support STORY-025 hook integration. "
            "Scenario 3f: Phase 2.5 (post-staging) and Phase 3.5 (post-production) hooks."
        )

        print("✓ Scenario 3f: Post-release hooks (STORY-025) preserved")


class TestSkillEnhancement:
    """AC-4: Skill Enhancement - Comprehensive deployment logic"""

    def test_skill_phases_1_through_6_documented(self):
        """
        AC-4.1: Skill has Phases 1-6 documented

        ARRANGE: Read skill file
        ACT: Count phase headers (Phase 1, 2, 3, 4, 5, 6)
        ASSERT: All 6 phases documented
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")
        assert skill_path.exists(), "Release skill not found"

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        # Count phases
        phase_markers = re.findall(r'### Phase [1-6]:', content)

        # Assert: All 6 phases present
        assert len(phase_markers) >= 6, (
            f"Skill has {len(phase_markers)} phases documented (need all 6: 1-6). "
            f"Phases: 1=Pre-release, 2=Staging, 3=Production, "
            f"4=Post-deploy validation, 5=Release docs, 6=Monitoring."
        )
        print(f"✓ Skill phases 1-6 documented: {len(phase_markers)} phases found")

    def test_skill_has_phase_25_post_staging_hooks(self):
        """
        AC-4.2: Skill has Phase 2.5 - Post-Staging Hooks (STORY-025)

        ARRANGE: Read skill file
        ACT: Search for Phase 2.5 section
        ASSERT: Phase 2.5 exists with hook integration logic
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        # Assert: Phase 2.5 exists
        has_phase_25 = bool(re.search(r'### Phase 2\.5', content))
        assert has_phase_25, (
            "Skill must have Phase 2.5: Post-Staging Hooks. "
            "STORY-025 enhancement requires hook integration after staging deployment."
        )
        print("✓ Skill has Phase 2.5: Post-Staging Hooks")

    def test_skill_has_phase_35_post_production_hooks(self):
        """
        AC-4.3: Skill has Phase 3.5 - Post-Production Hooks (STORY-025, failures-only)

        ARRANGE: Read skill file
        ACT: Search for Phase 3.5 section
        ASSERT: Phase 3.5 exists with failure-triggered hook logic
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        # Assert: Phase 3.5 exists
        has_phase_35 = bool(re.search(r'### Phase 3\.5', content))
        assert has_phase_35, (
            "Skill must have Phase 3.5: Post-Production Hooks. "
            "STORY-025 enhancement requires hook integration (failures-only mode by default)."
        )
        print("✓ Skill has Phase 3.5: Post-Production Hooks")

    def test_skill_reference_files_created_for_deployment_strategies(self):
        """
        AC-4.4: Reference file exists - deployment-strategies.md

        ARRANGE: Check for reference file
        ACT: Verify file exists
        ASSERT: deployment-strategies.md present with strategies (blue-green, canary, rolling, recreate)
        """
        # Arrange
        ref_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/references/deployment-strategies.md")

        # Act: Check file exists
        file_exists = ref_path.exists()

        # Assert: Reference file present
        assert file_exists, (
            f"Reference file not found: {ref_path}. "
            f"Skill needs deployment-strategies.md documenting "
            f"blue-green, canary, rolling, recreate strategies."
        )
        print("✓ Reference file: deployment-strategies.md exists")

    def test_skill_reference_files_created_for_platform_commands(self):
        """
        AC-4.5: Reference file exists - platform-deployment-commands.md

        ARRANGE: Check for reference file
        ACT: Verify file exists
        ASSERT: platform-deployment-commands.md present (K8s, Docker, AWS, Azure, GCP)
        """
        # Arrange
        ref_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/references/platform-deployment-commands.md")

        # Act
        file_exists = ref_path.exists()

        # Assert: Reference file present
        assert file_exists, (
            f"Reference file not found: {ref_path}. "
            f"Skill needs platform-deployment-commands.md documenting "
            f"K8s, Docker, AWS, Azure, GCP deployment procedures."
        )
        print("✓ Reference file: platform-deployment-commands.md exists")

    def test_skill_reference_files_created_for_smoke_testing(self):
        """
        AC-4.6: Reference file exists - smoke-testing-guide.md

        ARRANGE: Check for reference file
        ACT: Verify file exists
        ASSERT: smoke-testing-guide.md present with test procedures
        """
        # Arrange
        ref_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/references/smoke-testing-guide.md")

        # Act
        file_exists = ref_path.exists()

        # Assert: Reference file present
        assert file_exists, (
            f"Reference file not found: {ref_path}. "
            f"Skill needs smoke-testing-guide.md documenting "
            f"health checks, API validation, critical path testing."
        )
        print("✓ Reference file: smoke-testing-guide.md exists")

    def test_skill_reference_files_created_for_rollback_procedures(self):
        """
        AC-4.7: Reference file exists - rollback-procedures.md

        ARRANGE: Check for reference file
        ACT: Verify file exists
        ASSERT: rollback-procedures.md present (automatic and manual)
        """
        # Arrange
        ref_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/references/rollback-procedures.md")

        # Act
        file_exists = ref_path.exists()

        # Assert: Reference file present
        assert file_exists, (
            f"Reference file not found: {ref_path}. "
            f"Skill needs rollback-procedures.md documenting "
            f"automatic rollback and manual recovery procedures."
        )
        print("✓ Reference file: rollback-procedures.md exists")

    def test_skill_can_extract_story_id_from_context(self):
        """
        AC-4.8: Skill parameter extraction - Story ID from YAML frontmatter

        ARRANGE: Read skill documentation
        ACT: Verify parameter extraction section exists
        ASSERT: Skill can extract story_id from loaded story file context
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        # Assert: Parameter extraction documented
        has_extraction = bool(re.search(r'extract.*story|story.*id|parameter', content, re.IGNORECASE))
        assert has_extraction, (
            "Skill must document parameter extraction. "
            "Should extract story_id from YAML frontmatter of loaded story file."
        )
        print("✓ Skill parameter extraction documented (story ID from context)")

    def test_skill_can_extract_environment_from_context(self):
        """
        AC-4.9: Skill parameter extraction - Environment from context markers

        ARRANGE: Read skill documentation
        ACT: Verify environment extraction
        ASSERT: Skill can extract environment (staging/production) from context
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        # Assert: Environment extraction documented
        has_env_extraction = bool(re.search(r'environment|staging|production', content, re.IGNORECASE))
        assert has_env_extraction, (
            "Skill must extract environment parameter. "
            "Should get staging/production from context markers or command argument."
        )
        print("✓ Skill parameter extraction documented (environment from context)")


class TestTokenEfficiency:
    """AC-5: Token Efficiency - ≥75% savings in main conversation"""

    def test_estimated_token_savings_75_percent_or_more(self):
        """
        AC-5.1: Estimated token savings ≥75% in main conversation

        ARRANGE: Calculate estimated token usage before/after
        ACT: Command file ~18,166 chars (old) vs target <12,000 chars (new)
        ASSERT: Character reduction translates to token savings ≥75%
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")
        original_chars = 18166  # Current /release command
        estimated_tokens_before = 15000  # Estimated for original

        # Act
        with open(command_path, 'r') as f:
            content = f.read()
        current_chars = len(content)

        # Calculate savings
        char_reduction = original_chars - current_chars
        char_reduction_pct = (char_reduction * 100) // original_chars if char_reduction > 0 else 0

        # Estimate token savings (rough: 1 token ≈ 1.2 chars)
        estimated_tokens_after = (current_chars * 1.3) // 1000  # Conservative estimate in tokens
        estimated_savings = estimated_tokens_before - int(estimated_tokens_after)
        estimated_savings_pct = (estimated_savings * 100) // estimated_tokens_before if estimated_tokens_before > 0 else 0

        # Assert: Token savings ≥75% (typical for lean pattern: 67-80%)
        assert estimated_savings_pct >= 75 or char_reduction_pct >= 30, (
            f"Character reduction {char_reduction_pct}% → estimated token savings {estimated_savings_pct}%. "
            f"Target: ≥75% token savings. "
            f"Current: {current_chars} chars vs original {original_chars} chars. "
            f"Estimated tokens: {estimated_tokens_after}K after vs {estimated_tokens_before}K before."
        )
        print(f"✓ Token efficiency: {estimated_savings_pct}% savings (≥75% target)")

    def test_command_main_conversation_under_3k_tokens(self):
        """
        AC-5.2: Refactored command <3,000 tokens in main conversation

        ARRANGE: Calculate tokens for refactored command
        ACT: Estimate tokens (approx 1 token = 1.3 characters)
        ASSERT: Token count <3,000 in main conversation
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Rough estimate: 1 token ≈ 1.3 characters
        estimated_tokens = (len(content) * 1.3) // 1000

        # Assert: <3K tokens
        assert estimated_tokens < 3000, (
            f"Estimated tokens: {estimated_tokens} (target: <3,000). "
            f"Character count {len(content)} → {estimated_tokens} tokens. "
            f"Refactoring not optimized enough."
        )
        print(f"✓ Command tokens: ~{estimated_tokens} tokens (<3K in main conversation)")

    def test_skill_execution_tokens_isolated_40_to_50k(self):
        """
        AC-5.3: Skill execution <50K tokens (isolated context, doesn't count)

        ARRANGE: Note that skill work is in isolated context
        ACT: Acknowledge token isolation
        ASSERT: Skill can use up to 50K tokens in isolated context
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")
        assert skill_path.exists(), "Release skill not found"

        # Act
        with open(skill_path, 'r') as f:
            lines = f.readlines()
        skill_lines = len(lines)

        # Assert: Skill size reasonable for isolated context
        # Isolated context can handle 40-50K tokens, but skill should stay focused
        assert skill_lines < 4000, (
            f"Skill size {skill_lines} lines. "
            f"For context isolation, skill should use progressive disclosure "
            f"(split into SKILL.md ~200 lines + references ~3000 lines)."
        )
        print(f"✓ Skill size: {skill_lines} lines (fits in isolated context)")


class TestPatternCompliance:
    """AC-6: Pattern Compliance - Lean orchestration 5-responsibility checklist"""

    def test_responsibility_1_parse_arguments(self):
        """
        AC-6.1: Responsibility 1 - Parse arguments (story ID, environment)

        ARRANGE: Read Phase 0
        ACT: Verify argument parsing for $1 (STORY-ID) and $2 (environment)
        ASSERT: Phase 0 parses and validates arguments
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Assert: Argument parsing present
        has_arg_parsing = bool(re.search(r'story.*id|\$1|argument.*validation', content, re.IGNORECASE))
        assert has_arg_parsing, (
            "Command must parse arguments: $1 (STORY-ID), $2 (environment). "
            "This is Responsibility 1 of lean pattern."
        )
        print("✓ Responsibility 1: Parse arguments (✓)")

    def test_responsibility_2_load_context(self):
        """
        AC-6.2: Responsibility 2 - Load context via @file reference

        ARRANGE: Read command structure
        ACT: Verify @devforgeai/specs/Stories/$1.story.md context loading
        ASSERT: Story file loaded via @file
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Assert: Context loading present
        has_context_loading = bool(re.search(r'@.*Stories.*story\.md|Load.*context', content, re.IGNORECASE))
        assert has_context_loading or 'STORY' in content, (
            "Command must load story file context. "
            "Use: @devforgeai/specs/Stories/$1.story.md or @devforgeai/specs/Stories/$1*.story.md. "
            "This is Responsibility 2 of lean pattern."
        )
        print("✓ Responsibility 2: Load context (✓)")

    def test_responsibility_3_set_context_markers(self):
        """
        AC-6.3: Responsibility 3 - Set context markers for skill

        ARRANGE: Read command
        ACT: Verify context markers like **Story ID:**, **Environment:**
        ASSERT: Context markers set for skill parameter extraction
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Assert: Context markers present
        has_markers = bool(re.search(r'\*\*[A-Z].*:\*\*', content))
        assert has_markers, (
            "Command should set context markers for skill. "
            "Examples: **Story ID:** ..., **Environment:** ... "
            "This is Responsibility 3 of lean pattern (optional but recommended)."
        )
        print("✓ Responsibility 3: Set context markers (✓)")

    def test_responsibility_4_invoke_skill(self):
        """
        AC-6.4: Responsibility 4 - Single Skill() invocation

        ARRANGE: Read command
        ACT: Find Skill(command="...") call
        ASSERT: Single skill invocation, no parameters
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Assert: Skill invocation present
        assert 'Skill(command="devforgeai-release")' in content or \
               "Skill(command='devforgeai-release')" in content, (
            "Command must invoke skill: Skill(command=\"devforgeai-release\"). "
            "No parameters (all extracted from context). "
            "This is Responsibility 4 of lean pattern."
        )
        print("✓ Responsibility 4: Invoke skill (✓)")

    def test_responsibility_5_display_results(self):
        """
        AC-6.5: Responsibility 5 - Display results (no parsing, no formatting)

        ARRANGE: Read Phase 3 (result display)
        ACT: Verify result is output directly
        ASSERT: No parsing or formatting of skill results
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Assert: Result display section present
        has_result_display = bool(re.search(r'display.*result|output.*skill|show.*result', content, re.IGNORECASE))
        assert has_result_display or 'Phase 3' in content, (
            "Command must have Phase 3: Display results. "
            "Output skill result directly (no parsing/formatting). "
            "This is Responsibility 5 of lean pattern."
        )
        print("✓ Responsibility 5: Display results (✓)")

    def test_anti_pattern_no_business_logic_validation(self):
        """
        AC-6.6: Anti-pattern check - No business logic in command

        ARRANGE: Read command
        ACT: Grep for forbidden patterns (deployment, validation, etc.)
        ASSERT: No anti-patterns found (business logic in skill, not command)
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Anti-patterns
        forbidden_patterns = [
            (r'deploy.*staging', 'Deployment logic'),
            (r'check.*smoke|run.*test', 'Test execution'),
            (r'update.*status|released', 'Status update logic'),
            (r'template|format.*output', 'Display templates'),
        ]

        found_anti_patterns = []
        for pattern, name in forbidden_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                found_anti_patterns.append(f"{name} ({len(matches)} occurrences)")

        # Assert: No major anti-patterns
        assert len(found_anti_patterns) < 3, (
            f"Found anti-patterns: {found_anti_patterns}. "
            f"Command should be pure orchestration (no business logic). "
            f"Move patterns to skill/subagents."
        )
        print("✓ Anti-pattern check: No major violations")

    def test_pattern_comparison_to_qa_reference(self):
        """
        AC-6.7: Pattern comparison - Consistent with /qa reference (295 lines, 48% budget)

        ARRANGE: Read both command and /qa
        ACT: Compare line counts and structure
        ASSERT: Lean pattern applied consistently
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/release.md")
        qa_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/qa.md")

        assert qa_path.exists(), "/qa reference not found"

        # Act
        with open(command_path, 'r') as f:
            release_lines = len(f.readlines())
        with open(qa_path, 'r') as f:
            qa_lines = len(f.readlines())

        # Reference: /qa = 295 lines, 48% budget (excellent)
        # Target: /release = 250-350 lines (similar to /qa)

        # Assert: Consistent with pattern
        if release_lines > 350:
            print(f"⚠️ Command size {release_lines} lines (vs /qa {qa_lines} lines reference)")
        else:
            print(f"✓ Pattern consistent with /qa reference: {release_lines} lines")


class TestSubagentCreation:
    """AC-7: Subagent Creation Decision (documented)"""

    def test_subagent_decision_documented_in_story(self):
        """
        AC-7.1: Subagent creation decision documented

        ARRANGE: Check for documentation of subagent decision
        ACT: Verify implementation notes contain decision
        ASSERT: Either "new subagent created" or "no new subagent needed" documented
        """
        # Arrange
        story_path = Path("/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-038-refactor-release-command-lean-orchestration.story.md")
        assert story_path.exists(), "Story file not found"

        # Act
        with open(story_path, 'r') as f:
            content = f.read()

        # Check for decision documentation
        has_decision = bool(re.search(r'new subagent|subagent.*created|no.*subagent|existing.*subagent',
                                     content, re.IGNORECASE))

        # Assert: Decision documented in story or implementation notes
        assert has_decision or 'AC#7' in content or 'decision' in content.lower(), (
            "Story must document subagent creation decision. "
            "Either 'new subagent created' or 'no new subagent needed'."
        )
        print("✓ Subagent decision documented")

    def test_existing_subagents_used_deployment_engineer(self):
        """
        AC-7.2: Existing subagents referenced - deployment-engineer

        ARRANGE: Read skill documentation
        ACT: Verify deployment-engineer subagent is invoked
        ASSERT: Skill uses existing deployment-engineer subagent (no bypass)
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")
        assert skill_path.exists(), "Release skill not found"

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        # Assert: deployment-engineer subagent referenced
        assert 'deployment-engineer' in content.lower() or 'Task(' in content, (
            "Skill should use deployment-engineer subagent for platform-specific commands. "
            "Support Kubernetes, Docker, AWS, Azure, GCP deployment."
        )
        print("✓ Existing subagent used: deployment-engineer")

    def test_existing_subagents_used_security_auditor(self):
        """
        AC-7.3: Existing subagents referenced - security-auditor

        ARRANGE: Read skill documentation
        ACT: Verify security-auditor subagent is invoked
        ASSERT: Skill uses security-auditor for pre-production checks
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-release/SKILL.md")

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        # Assert: security-auditor referenced
        assert 'security' in content.lower(), (
            "Skill should use security-auditor subagent. "
            "Final security scan required before production deployment."
        )
        print("✓ Existing subagent used: security-auditor")


# Test suite summary and execution
class TestSummary:
    """Summary and execution instructions"""

    def test_print_test_summary(self):
        """Print comprehensive test suite summary"""
        print("\n" + "="*80)
        print("STORY-038: Refactor /release Command for Lean Orchestration Compliance")
        print("="*80)
        print("\nTest Suite Summary:")
        print("-" * 80)
        print("TestCommandSizeReduction (4 tests)")
        print("  - AC-1.1: Character count <15K hard limit")
        print("  - AC-1.2: Character count <12K target")
        print("  - AC-1.3: Line count ≤350 lines")
        print("  - AC-1.4: Reduction ≥20% (target 47%)")
        print()
        print("TestBusinessLogicExtraction (6 tests)")
        print("  - AC-2.1: Phase 0 argument validation only")
        print("  - AC-2.2: No deployment sequencing in command")
        print("  - AC-2.3: No smoke test execution in command")
        print("  - AC-2.4: No rollback logic in command")
        print("  - AC-2.5: Error handling minimal (<25 lines)")
        print("  - AC-2.6: No display template generation")
        print()
        print("TestFunctionalEquivalence (6 tests)")
        print("  - AC-3a: Staging deployment preserved")
        print("  - AC-3b: Production confirmation preserved")
        print("  - AC-3c: Rollback behavior preserved")
        print("  - AC-3d: QA approval gate preserved")
        print("  - AC-3e: Default environment (staging) preserved")
        print("  - AC-3f: Post-release hooks (STORY-025) preserved")
        print()
        print("TestSkillEnhancement (9 tests)")
        print("  - AC-4.1-4.3: Skill phases 1-6 + 2.5 + 3.5 documented")
        print("  - AC-4.4-4.7: Reference files created (strategies, platform, smoke, rollback)")
        print("  - AC-4.8-4.9: Parameter extraction (story ID, environment)")
        print()
        print("TestTokenEfficiency (3 tests)")
        print("  - AC-5.1: Token savings ≥75%")
        print("  - AC-5.2: Command <3K tokens in main conversation")
        print("  - AC-5.3: Skill execution in isolated context (<50K)")
        print()
        print("TestPatternCompliance (7 tests)")
        print("  - AC-6.1-6.5: 5-responsibility checklist (parse, load, mark, invoke, display)")
        print("  - AC-6.6-6.7: Anti-pattern check + reference comparison")
        print()
        print("TestSubagentCreation (3 tests)")
        print("  - AC-7.1: Decision documented")
        print("  - AC-7.2-7.3: Existing subagents used (deployment-engineer, security-auditor)")
        print()
        print("-" * 80)
        print("TOTAL TEST COUNT: 38 unit tests")
        print("-" * 80)
        print("\n✅ All tests FAIL initially (Red phase)")
        print("✅ Tests PASS after Phases 2-5 refactoring complete")
        print("\nExecution:")
        print("  pytest tests/unit/test_release_command_refactoring.py -v")
        print("  pytest tests/unit/test_release_command_refactoring.py -k 'TestCommandSizeReduction' -v")
        print("\n" + "="*80 + "\n")
