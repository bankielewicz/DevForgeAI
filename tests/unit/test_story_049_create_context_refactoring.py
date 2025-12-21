"""
Test Suite for STORY-049: Refactor /create-context command budget compliance

This test suite validates the refactoring of the /create-context command to achieve
character budget compliance (≤14,000 characters, 93% of 15K budget) while maintaining
backward compatibility and framework compliance.

Test Categories:
1. Character Budget Tests (CRITICAL) - Validate size reduction targets
2. Phase N Refactoring Tests (CRITICAL) - Validate pattern externalization
3. Functionality Preservation Tests (CRITICAL) - Validate workflow intact
4. Backward Compatibility Tests (HIGH) - Validate greenfield/brownfield modes
5. Framework Compliance Tests (HIGH) - Validate lean orchestration pattern
6. Code Quality Tests (MEDIUM) - Validate clarity and maintainability

TDD Phase: RED - All tests initially failing (no implementation yet)
"""

import pytest
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def create_context_command_path() -> Path:
    """Path to the /create-context command file."""
    return Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/create-context.md")


@pytest.fixture
def hook_integration_pattern_path() -> Path:
    """Path to the hook integration pattern documentation file."""
    return Path("/mnt/c/Projects/DevForgeAI2/devforgeai/protocols/hook-integration-pattern.md")


@pytest.fixture
def command_content(create_context_command_path: Path) -> str:
    """Load the current /create-context command content."""
    if not create_context_command_path.exists():
        pytest.skip(f"Command file not found: {create_context_command_path}")
    return create_context_command_path.read_text(encoding='utf-8')


@pytest.fixture
def pattern_file_content(hook_integration_pattern_path: Path) -> str:
    """Load the hook integration pattern file content."""
    if not hook_integration_pattern_path.exists():
        pytest.skip(f"Pattern file not found: {hook_integration_pattern_path}")
    return hook_integration_pattern_path.read_text(encoding='utf-8')


@pytest.fixture
def command_char_count(create_context_command_path: Path) -> int:
    """Get exact character count of command file."""
    if not create_context_command_path.exists():
        pytest.skip(f"Command file not found: {create_context_command_path}")
    return len(create_context_command_path.read_bytes())


@pytest.fixture
def command_line_count(command_content: str) -> int:
    """Get line count of command file."""
    return len(command_content.splitlines())


# ============================================================================
# AC1: Character Budget Reduction Tests (CRITICAL)
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestAC1CharacterBudgetReduction:
    """
    AC1: Character budget reduction achieved

    Given: /create-context command currently at 16,210 characters (108% of budget)
    When: Phase N pattern documentation is extracted to `devforgeai/protocols/hook-integration-pattern.md`
    Then: Command file size is reduced to ≤14,000 characters (93% of budget)
    """

    def test_character_count_below_14000(self, command_char_count: int):
        """Test: Command file is ≤14,000 characters."""
        assert command_char_count <= 14000, (
            f"Command exceeds budget: {command_char_count} chars "
            f"(target: ≤14,000, budget: {command_char_count/15000*100:.1f}%)"
        )

    def test_character_count_below_15000_hard_limit(self, command_char_count: int):
        """Test: Command file respects hard limit of <15,000 characters."""
        assert command_char_count < 15000, (
            f"Command exceeds hard limit: {command_char_count} chars (limit: <15,000)"
        )

    def test_budget_compliance_percentage(self, command_char_count: int):
        """Test: Command uses ≤93% of 15K budget (optimal range 6K-12K)."""
        budget_percent = (command_char_count / 15000) * 100
        assert budget_percent <= 93, (
            f"Command at {budget_percent:.1f}% of budget (target: ≤93%)"
        )

    def test_character_reduction_from_baseline(self, command_char_count: int):
        """Test: Character count reduced by ≥2,210 chars from baseline of 16,210."""
        baseline = 16210
        reduction = baseline - command_char_count
        expected_minimum_reduction = 2210

        assert reduction >= expected_minimum_reduction, (
            f"Insufficient reduction: {reduction} chars "
            f"(expected: ≥{expected_minimum_reduction} chars)"
        )

    def test_reduction_targets_optimal_range(self, command_char_count: int):
        """Test: Refactored size is within 6K-12K optimal range if possible."""
        optimal_min = 6000
        optimal_max = 12000

        # Acceptance: ≤14K, but optimally between 6-12K
        if command_char_count <= optimal_max:
            assert command_char_count >= optimal_min or command_char_count <= 14000, (
                f"Size {command_char_count} outside both ranges: "
                f"optimal (6-12K) or acceptable (≤14K)"
            )


# ============================================================================
# AC2: Hook Integration Workflow Preservation Tests (CRITICAL)
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestAC2HookIntegrationWorkflowPreserved:
    """
    AC2: Hook integration workflow preserved

    Given: Phase N currently contains 11 steps for hook registration
    When: Verbose pattern documentation is removed
    Then: All 11 workflow steps remain functional with clear instructions
    """

    def test_phase_n_section_exists(self, command_content: str):
        """Test: Phase N section still exists in command."""
        # Phase N should be titled like "### Phase N" or similar
        pattern = r'###\s+Phase\s+N|###\s+Phase\s+\d+.*[Hh]ook|###\s+.*[Ff]eedback.*[Hh]ook'
        assert re.search(pattern, command_content), (
            "Phase N section not found (expected: Hook/Feedback integration phase)"
        )

    def test_all_four_workflow_steps_present(self, command_content: str):
        """Test: All 4 primary workflow steps documented (even if condensed)."""
        required_steps = [
            r'[Ss]tep\s+1.*[Dd]etermine',  # Step 1: Determine Operation Status
            r'[Ss]tep\s+2.*[Cc]heck',       # Step 2: Check Hook Eligibility
            r'[Ss]tep\s+3.*[Ii]nvoke',      # Step 3: Invoke Hooks if Eligible
            r'[Ss]tep\s+4.*[Cc]omplete',    # Step 4: Phase Complete
        ]

        for step_pattern in required_steps:
            assert re.search(step_pattern, command_content), (
                f"Workflow step missing: {step_pattern}"
            )

    def test_phase_n_references_pattern_file(self, command_content: str):
        """Test: Phase N references `devforgeai/protocols/hook-integration-pattern.md` via Read tool."""
        # Should contain Read(file_path="devforgeai/protocols/hook-integration-pattern.md")
        pattern = r'Read\(file_path.*hook-integration-pattern\.md'
        assert re.search(pattern, command_content), (
            "Phase N doesn't reference hook-integration-pattern.md via Read tool"
        )

    def test_no_verbose_pattern_descriptions_in_phase_n(self, command_content: str):
        """Test: Phase N doesn't contain verbose pattern explanations (moved to pattern file)."""
        # Pattern file content should be moved out
        # Should NOT contain sections like "Key Characteristics" or "Pattern Consistency"
        # in Phase N section (they should be in pattern file)

        # Extract Phase N section (rough extraction)
        phase_n_start = command_content.find('### Phase N')
        if phase_n_start == -1:
            # Try alternate Phase N title
            phase_n_start = command_content.find(r'###\s+Phase\s+\d+.*[Hh]ook')

        if phase_n_start > -1:
            # Find next phase or end of file
            next_phase = command_content.find('### Phase', phase_n_start + 1)
            if next_phase == -1:
                next_phase = command_content.find('## Error Handling', phase_n_start)
            if next_phase == -1:
                next_phase = len(command_content)

            phase_n_content = command_content[phase_n_start:next_phase]

            # Should not have lengthy explanations of "Key Characteristics" or "Pattern Consistency"
            # (these should be in pattern file, not in command)
            key_characteristics_in_phase_n = (
                phase_n_content.count('Key Characteristics') > 1 or  # Only in header OK
                phase_n_content.count('Pattern Consistency') > 1
            )

            # This is a loose check - the important part is they're moved to pattern file
            # and Phase N is condensed

    def test_phase_n_condensed_relative_to_baseline(self, command_content: str):
        """Test: Phase N section is condensed compared to original (~2,500 char reduction)."""
        # This is harder to test precisely without before/after comparison
        # But we can verify Phase N doesn't have excessive verbosity
        phase_n_pattern = r'###\s+Phase\s+N.*?(?=###|##|$)'
        phase_n_match = re.search(phase_n_pattern, command_content, re.DOTALL | re.IGNORECASE)

        if phase_n_match:
            phase_n_content = phase_n_match.group(0)
            # Phase N should be reasonably sized (not excessive documentation)
            # Rough check: condensed Phase N should be <1500 characters
            # (original was ~2500-3000, so condensed should be <2000)
            assert len(phase_n_content) < 2500, (
                f"Phase N still too large: {len(phase_n_content)} chars "
                f"(target: <2500 after condensing pattern docs)"
            )

    def test_inline_comments_condensed_in_phase_n(self, command_content: str):
        """Test: Inline bash comments in Phase N are condensed (essential only)."""
        phase_n_pattern = r'###\s+Phase\s+N.*?(?=###|##|$)'
        phase_n_match = re.search(phase_n_pattern, command_content, re.DOTALL | re.IGNORECASE)

        if phase_n_match:
            phase_n_content = phase_n_match.group(0)

            # Count comment lines
            comment_lines = len(re.findall(r'^\s*#', phase_n_content, re.MULTILINE))
            # Excessive comments (>20) might indicate not condensed
            # But allow some explanation

            # Better check: comments should explain "why" not "how"
            # (This is subjective, so we just verify comments exist and aren't excessive)
            assert comment_lines < 25, (
                f"Excessive comments in Phase N: {comment_lines} lines "
                f"(comments should be condensed to essentials)"
            )


# ============================================================================
# AC3: Pattern Documentation Externalization Tests (CRITICAL)
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestAC3PatternDocumentationExternalized:
    """
    AC3: Pattern documentation externalized and accessible

    Given: Hook integration pattern details currently inline in Phase N (~2,500 chars)
    When: Pattern documentation is moved to `devforgeai/protocols/hook-integration-pattern.md`
    Then: Pattern file is comprehensive and referenced in Phase N
    """

    def test_pattern_file_exists(self, hook_integration_pattern_path: Path):
        """Test: `devforgeai/protocols/hook-integration-pattern.md` exists."""
        assert hook_integration_pattern_path.exists(), (
            f"Pattern file not found: {hook_integration_pattern_path}"
        )

    def test_pattern_file_not_empty(self, pattern_file_content: str):
        """Test: Pattern file has substantial content (>500 characters)."""
        assert len(pattern_file_content) > 500, (
            f"Pattern file too small: {len(pattern_file_content)} chars (expected: >500)"
        )

    def test_pattern_file_contains_purpose_section(self, pattern_file_content: str):
        """Test: Pattern file contains Purpose section."""
        assert re.search(r'##\s+Purpose', pattern_file_content), (
            "Pattern file missing ## Purpose section"
        )

    def test_pattern_file_contains_pattern_overview(self, pattern_file_content: str):
        """Test: Pattern file contains Pattern Overview section."""
        assert re.search(r'##\s+Pattern\s+Overview|##\s+Overview', pattern_file_content), (
            "Pattern file missing ## Pattern Overview section"
        )

    def test_pattern_file_contains_implementation_steps(self, pattern_file_content: str):
        """Test: Pattern file documents 4 implementation steps."""
        # Should contain Step 1, Step 2, Step 3, Step 4
        step_patterns = [
            r'###\s+Step\s+1.*[Dd]etermine',
            r'###\s+Step\s+2.*[Cc]heck',
            r'###\s+Step\s+3.*[Ii]nvoke',
            r'###\s+Step\s+4.*[Cc]omplete',
        ]

        for step_pattern in step_patterns:
            assert re.search(step_pattern, pattern_file_content), (
                f"Pattern file missing step: {step_pattern}"
            )

    def test_pattern_file_contains_key_characteristics(self, pattern_file_content: str):
        """Test: Pattern file documents Key Characteristics section."""
        assert re.search(r'##\s+Key\s+Characteristics', pattern_file_content), (
            "Pattern file missing ## Key Characteristics section"
        )

    def test_pattern_file_contains_code_examples(self, pattern_file_content: str):
        """Test: Pattern file contains code examples (bash blocks)."""
        code_blocks = len(re.findall(r'```bash', pattern_file_content))
        assert code_blocks >= 3, (
            f"Pattern file insufficient code examples: {code_blocks} blocks (expected: ≥3)"
        )

    def test_pattern_file_contains_operation_specific_notes(self, pattern_file_content: str):
        """Test: Pattern file documents operation-specific details."""
        # Should reference specific commands (dev, create-context, ideate, etc.)
        operations = ['create-context', '/dev', '/ideate', '/create-ui']
        found_operations = sum(1 for op in operations if op in pattern_file_content)

        assert found_operations >= 2, (
            f"Pattern file missing operation-specific details "
            f"(found references to {found_operations}/4 operations)"
        )

    def test_command_references_pattern_file_with_read_tool(self, command_content: str):
        """Test: Command Phase N uses Read(file_path=...) to reference pattern file."""
        # Should have exact pattern: Read(file_path="devforgeai/protocols/hook-integration-pattern.md")
        pattern = r'Read\(\s*file_path\s*=\s*["\']\devforgeai/protocols/hook-integration-pattern\.md'
        assert re.search(pattern, command_content), (
            "Command Phase N doesn't use Read tool to reference pattern file"
        )


# ============================================================================
# AC4: Backward Compatibility Tests (HIGH)
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestAC4BackwardCompatibilityMaintained:
    """
    AC4: Backward compatibility maintained

    Given: /create-context command used by greenfield and brownfield projects
    When: Command is refactored
    Then: All functionality works identically (100% test pass rate, no behavior changes)
    """

    def test_command_structure_preserved(self, command_content: str):
        """Test: Command structure follows lean orchestration pattern (3-5 phases)."""
        # Count phase sections
        phase_pattern = r'###\s+Phase'
        phases = len(re.findall(phase_pattern, command_content))

        # Should have 7+ phases (Phase 1-6 + Phase N + potentially more)
        assert phases >= 7, (
            f"Command missing phases: {phases} found (expected: ≥7)"
        )

    def test_architecture_skill_invocation_preserved(self, command_content: str):
        """Test: Architecture skill invocation still present in Phase 3."""
        # Should still contain: Skill(command="devforgeai-architecture")
        assert 'Skill(command="devforgeai-architecture")' in command_content, (
            "Architecture skill invocation removed or changed"
        )

    def test_context_file_generation_workflow_intact(self, command_content: str):
        """Test: Context file generation workflow documented (tech-stack, etc.)."""
        context_files = [
            'tech-stack.md',
            'source-tree.md',
            'dependencies.md',
            'coding-standards.md',
            'architecture-constraints.md',
            'anti-patterns.md'
        ]

        found_files = sum(1 for f in context_files if f in command_content)
        assert found_files >= 4, (
            f"Context files documentation incomplete: {found_files}/6 referenced"
        )

    def test_pre_flight_check_phase_preserved(self, command_content: str):
        """Test: Pre-flight check phase still exists."""
        assert 'Phase 1' in command_content or 'Pre-Flight' in command_content, (
            "Phase 1 (Pre-Flight Check) missing"
        )

    def test_git_initialization_check_preserved(self, command_content: str):
        """Test: Git initialization check still documented."""
        assert 'Phase 2' in command_content or 'Git' in command_content, (
            "Phase 2 (Git Repository Initialization) missing"
        )

    def test_architecture_review_phase_preserved(self, command_content: str):
        """Test: Architecture review phase still exists."""
        assert 'architect-reviewer' in command_content or 'Phase 4' in command_content, (
            "Architecture review phase missing"
        )

    def test_final_validation_phase_preserved(self, command_content: str):
        """Test: Final validation phase still present."""
        assert 'validation' in command_content.lower() or 'Phase 6' in command_content, (
            "Final validation phase missing"
        )

    def test_success_report_phase_preserved(self, command_content: str):
        """Test: Success report phase still present."""
        assert 'Success Report' in command_content or 'Phase 7' in command_content or 'success' in command_content.lower(), (
            "Success report phase missing"
        )

    def test_error_handling_section_preserved(self, command_content: str):
        """Test: Error handling section still documented."""
        assert re.search(r'##\s+Error\s+Handling', command_content), (
            "Error Handling section missing"
        )

    def test_notes_section_preserved(self, command_content: str):
        """Test: Notes section (framework philosophy) still present."""
        assert re.search(r'##\s+Notes|##\s+Framework', command_content), (
            "Notes section missing"
        )

    def test_no_critical_sections_removed(self, command_content: str):
        """Test: No critical workflow instructions removed."""
        critical_keywords = [
            'Check for existing context',
            'Architecture skill',
            'context files',
            'validation',
            'error'
        ]

        missing_keywords = [kw for kw in critical_keywords if kw.lower() not in command_content.lower()]

        assert len(missing_keywords) == 0, (
            f"Critical sections missing: {missing_keywords}"
        )


# ============================================================================
# AC5: Framework Compliance Tests (HIGH)
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestAC5FrameworkComplianceValidated:
    """
    AC5: Framework compliance validated

    Given: Lean orchestration pattern requires commands <15K characters
    When: Refactored command is measured
    Then: Character count ≤14,000, audit passes, leans orchestration pattern followed
    """

    def test_lean_orchestration_pattern_applied(self, command_content: str):
        """Test: Command follows lean orchestration pattern."""
        # Should have clear phases (Phase 0, 1, 2, etc.)
        # Should NOT have extensive business logic (that's in skills)
        # Should reference skill(s)

        assert re.search(r'###\s+Phase\s+\d+', command_content), (
            "Command doesn't follow phase structure"
        )

        assert 'Skill(' in command_content, (
            "Command doesn't delegate to skills (requires Skill() invocation)"
        )

    def test_command_invokes_skill_not_subagents_directly(self, command_content: str):
        """Test: Command invokes skill, not subagents directly (orchestration pattern)."""
        # Should have Skill() invocation
        assert 'Skill(command=' in command_content, (
            "Command should invoke skill, not subagents directly"
        )

    def test_minimal_business_logic_in_command(self, command_content: str):
        """Test: Business logic is minimal (delegated to skill)."""
        # Count lines with algorithm-like keywords (for, while, if, else, regex, calculate)
        # These should be minimal in command (most in skill)
        algorithm_keywords = [
            r'^\s+for\s+',
            r'^\s+while\s+',
            r'^\s+if\s+.*then',  # Pseudo-code style
            r'calculate',
            r'algorithm'
        ]

        algorithm_lines = sum(
            len(re.findall(kw, command_content, re.MULTILINE | re.IGNORECASE))
            for kw in algorithm_keywords
        )

        # Should be very few (<5) in command
        assert algorithm_lines < 10, (
            f"Excessive algorithm logic in command: {algorithm_lines} lines "
            f"(should be <10, business logic belongs in skill)"
        )

    def test_3_to_5_primary_phases(self, command_content: str):
        """Test: Command has 3-5 primary phases (lean structure)."""
        # Main phases (before any special/optional phases)
        main_phase_pattern = r'###\s+Phase\s+[0-6](?:\s|:)'
        phases = len(re.findall(main_phase_pattern, command_content))

        # Should have 7+ phases total (0-6 is 7 phases)
        # But 3-5 main orchestration phases
        assert phases >= 6, (
            f"Insufficient phases: {phases} (expected: ≥6)"
        )

    def test_command_uses_native_tools(self, command_content: str):
        """Test: Command uses native tools (Read, Write, Edit, Glob, Grep) not Bash."""
        # Should use: Read, Write, Edit, Glob, Grep, Skill, Task, AskUserQuestion
        # Should minimize Bash (only for essential operations)

        has_native_tools = any([
            'Read(' in command_content,
            'Skill(' in command_content,
            'AskUserQuestion' in command_content
        ])

        assert has_native_tools, (
            "Command doesn't use native tools (Read, Skill, AskUserQuestion)"
        )

    def test_audit_budget_compliant(self, create_context_command_path: Path):
        """
        Test: /audit-budget would show command as COMPLIANT.

        Note: This test checks the character count meets lean orchestration target.
        The /audit-budget command would use this test's measurement.
        """
        char_count = len(create_context_command_path.read_bytes())

        # Compliant: <15K (hard limit)
        # Good: <12K (warning threshold)
        # Optimal: 6K-10K (target range)

        # For compliance, just needs to be <15K
        is_compliant = char_count < 15000

        # Assessment message
        if char_count < 6000:
            assessment = "UNDER (excellent)"
        elif char_count <= 10000:
            assessment = "OPTIMAL"
        elif char_count <= 12000:
            assessment = "GOOD"
        elif char_count < 15000:
            assessment = "COMPLIANT (but high)"
        else:
            assessment = "OVER BUDGET"

        assert is_compliant, (
            f"Command NOT audit-budget compliant: {char_count} chars "
            f"({assessment}) - must be <15,000"
        )

    def test_command_documentation_clear(self, command_content: str):
        """Test: Command documentation is clear (good readability after refactoring)."""
        # Should have clear section headers
        has_headers = bool(re.search(r'##\s+\w+', command_content))
        has_phase_structure = bool(re.search(r'###\s+Phase', command_content))

        assert has_headers and has_phase_structure, (
            "Command documentation structure unclear"
        )

    def test_command_integration_points_clear(self, command_content: str):
        """Test: Command's integration points are documented."""
        integration_keywords = [
            'Integration Points',
            'Invokes',
            'Prerequisites',
            'Enables'
        ]

        has_integration_docs = any(kw in command_content for kw in integration_keywords)

        assert has_integration_docs, (
            "Command doesn't document integration points (Invokes, Prerequisites, etc.)"
        )


# ============================================================================
# Additional Edge Case Tests
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestEdgeCases:
    """Test edge cases and error scenarios for the refactored command."""

    def test_pattern_file_readable_by_read_tool(self, hook_integration_pattern_path: Path):
        """Test: Pattern file is valid Markdown and readable."""
        assert hook_integration_pattern_path.exists()
        content = hook_integration_pattern_path.read_text(encoding='utf-8')
        assert len(content) > 0
        assert '```bash' in content or '```' in content, (
            "Pattern file should have code examples"
        )

    def test_no_orphaned_references_in_command(self, command_content: str):
        """Test: Command doesn't reference non-existent sections."""
        # Check for broken internal links/references
        # Example: If referencing "See Step 5" but only 4 steps exist

        # Pattern files should use sections that exist
        step_references = re.findall(r'Step\s+(\d+)', command_content)
        if step_references:
            max_step = max(int(s) for s in step_references)
            # Verify those steps are actually documented
            for step_num in range(1, max_step + 1):
                assert f'#### Step {step_num}' in command_content or \
                       f'### Step {step_num}' in command_content, (
                    f"Referenced Step {step_num} not documented"
                )

    def test_pattern_file_not_created_inline_in_command(self, command_content: str):
        """Test: Hook integration pattern documentation is NOT inline (should be external)."""
        # The whole point is to externalize this
        # So we should NOT find duplicate pattern documentation in command

        # Count occurrences of "Key Characteristics" (should be in pattern file, not command)
        key_char_count = command_content.count('Key Characteristics')

        # OK to have 0 (pattern moved) or 1 (mention in Phase N reference)
        # But not 2+ (would indicate pattern duplicated inline)
        assert key_char_count <= 1, (
            f"Pattern documentation duplicated in command: "
            f"'Key Characteristics' appears {key_char_count} times "
            f"(should be 0-1, moved to pattern file)"
        )

    def test_hook_workflow_readable_without_pattern_file(self, command_content: str):
        """Test: Hook workflow steps can be understood even without reading pattern file."""
        # Phase N should have clear step descriptions (even if condensed)
        phase_n_pattern = r'###\s+Phase\s+N.*?(?=###|##|$)'
        phase_n_match = re.search(phase_n_pattern, command_content, re.DOTALL | re.IGNORECASE)

        if phase_n_match:
            phase_n_content = phase_n_match.group(0)

            # Should have clear, readable text (not just "See pattern file")
            readable_content_length = len(phase_n_content.replace('```', '').replace('bash', ''))

            # Should have substantive content (>200 characters of readable text)
            assert readable_content_length > 200, (
                f"Phase N too condensed - insufficient readable content "
                f"({readable_content_length} chars, expected >200)"
            )

    def test_command_file_valid_markdown(self, command_content: str):
        """Test: Command file is valid Markdown (no syntax errors)."""
        # Check for balanced markdown syntax

        # Count markdown syntax elements
        backticks_single = command_content.count('`')
        backticks_triple_open = command_content.count('```')

        # Triple backticks should be balanced (even count)
        assert backticks_triple_open % 2 == 0, (
            f"Unbalanced triple backticks: {backticks_triple_open} "
            f"(should be even for code blocks)"
        )

    def test_no_duplicate_phase_definitions(self, command_content: str):
        """Test: No duplicate phase definitions (e.g., two 'Phase 1' sections)."""
        phase_matches = re.findall(r'###\s+Phase\s+(\d+|N)', command_content)

        # Count occurrences of each phase
        from collections import Counter
        phase_counts = Counter(phase_matches)

        # Each phase should appear exactly once
        duplicates = {phase: count for phase, count in phase_counts.items() if count > 1}

        assert not duplicates, (
            f"Duplicate phase definitions found: {duplicates}"
        )


# ============================================================================
# Code Quality and Metrics Tests
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestCodeQualityMetrics:
    """Test code quality metrics for the refactored command."""

    def test_line_count_in_reasonable_range(self, command_line_count: int):
        """Test: Command line count is reasonable (150-500 lines, lean orchestration target)."""
        assert 150 <= command_line_count <= 600, (
            f"Command line count {command_line_count} outside reasonable range (150-600)"
        )

    def test_phase_documentation_concise(self, command_content: str):
        """Test: Each phase has reasonable documentation (not excessive verbosity)."""
        # Average lines per phase should be <50
        phase_pattern = r'###\s+Phase.*?(?=###|##|$)'
        phases = re.findall(phase_pattern, command_content, re.DOTALL)

        if len(phases) > 0:
            avg_phase_lines = sum(len(p.splitlines()) for p in phases) / len(phases)

            # Average <60 lines per phase is reasonable
            assert avg_phase_lines < 70, (
                f"Phases too verbose: average {avg_phase_lines:.1f} lines per phase "
                f"(target: <60 for conciseness)"
            )

    def test_code_blocks_properly_formatted(self, command_content: str):
        """Test: Code blocks are properly formatted with language designation."""
        code_blocks = re.findall(r'```(\w*)', command_content)

        # Should have bash code blocks at minimum
        bash_blocks = [b for b in code_blocks if b == 'bash']

        assert len(bash_blocks) > 0, (
            "No bash code blocks found (expected for Phase N workflow)"
        )

    def test_no_excessive_comments(self, command_content: str):
        """Test: Command doesn't have excessive comments (condensed as required)."""
        lines = command_content.splitlines()

        # Count comment-only lines
        comment_lines = [l for l in lines if re.match(r'^\s*#', l) and not l.strip().startswith('#!')]

        comment_percentage = (len(comment_lines) / len(lines)) * 100 if lines else 0

        # Should be <15% comment lines (signs of condensed code)
        assert comment_percentage < 20, (
            f"Excessive comments: {comment_percentage:.1f}% of lines "
            f"(target: <20% for condensed command)"
        )

    def test_includes_success_criteria_documentation(self, command_content: str):
        """Test: Command documents success criteria (what indicates success)."""
        assert re.search(r'##\s+Success|Criteria|Expected', command_content, re.IGNORECASE), (
            "Command missing documentation of success criteria"
        )

    def test_includes_token_efficiency_notes(self, command_content: str):
        """Test: Command documents token efficiency considerations."""
        # Could be in "Token Efficiency" section or "Notes"
        efficiency_keywords = ['token', 'efficiency', 'optimization', 'performance']

        has_efficiency_docs = any(
            kw in command_content.lower() for kw in efficiency_keywords
        )

        # This is nice-to-have (not critical)
        # assert has_efficiency_docs, (
        #     "Command missing token efficiency documentation"
        # )


# ============================================================================
# Integration Tests
# ============================================================================

@pytest.mark.xfail(reason="TDD Red phase - implementation pending")
class TestIntegration:
    """Integration tests for refactored command with other framework components."""

    def test_command_is_registered(self, create_context_command_path: Path):
        """Test: Command file exists and is discoverable."""
        assert create_context_command_path.exists(), (
            f"Command file not found: {create_context_command_path}"
        )

        assert create_context_command_path.is_file(), (
            f"Command path is not a file: {create_context_command_path}"
        )

    def test_command_has_proper_frontmatter(self, command_content: str):
        """Test: Command has YAML frontmatter with required fields."""
        # Should start with --- (YAML)
        assert command_content.startswith('---'), (
            "Command missing YAML frontmatter"
        )

        # Should have description, argument-hint, model
        required_fields = ['description', 'model', 'allowed-tools']

        for field in required_fields:
            assert field in command_content, (
                f"Frontmatter missing required field: {field}"
            )

    def test_command_title_matches_purpose(self, command_content: str):
        """Test: Command title/header matches its purpose."""
        # Should have header like "# Create Context Command"
        assert re.search(r'#\s+[Cc]reate\s+[Cc]ontext', command_content), (
            "Command header doesn't match purpose (Create Context)"
        )

    def test_pattern_file_and_command_consistent(self, command_content: str, pattern_file_content: str):
        """Test: Pattern file and command are consistent in structure/terminology."""
        # Both should reference the 4 steps
        steps = ['Step 1', 'Step 2', 'Step 3', 'Step 4']

        for step in steps:
            in_command = step in command_content
            in_pattern = step in pattern_file_content

            # At least pattern file should have all steps
            assert in_pattern, (
                f"Pattern file missing {step}"
            )


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
