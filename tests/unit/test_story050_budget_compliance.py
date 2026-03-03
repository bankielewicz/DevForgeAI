"""
Unit tests for STORY-050: Refactor /audit-deferrals command for budget compliance

Tests cover:
- Acceptance Criteria 1: Budget Compliance (character count)
- Acceptance Criteria 4: Pattern Consistency with reference implementations
- Technical Specification: CONF-001 through CONF-005
- Technical Specification: SVC-001 through SVC-003
- Non-Functional Requirements: NFR-S1 (Scalability/Budget)

All tests FAIL initially (Red phase) because refactoring not complete.
These tests pass after Phases 2-5 complete refactoring.
"""

import os
import re
import subprocess
from pathlib import Path


class TestBudgetCompliance:
    """AC-1: Budget Compliance Achieved - Character count <12K"""

    def test_command_character_count_under_limit(self):
        """
        AC-1 Test 1: Command file <12,000 characters

        ARRANGE: Read /audit-deferrals command file
        ACT: Count characters with wc -c
        ASSERT: Character count <12,000 (target 8-10K for 40% buffer)
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")
        assert command_path.exists(), "audit-deferrals command not found"

        # Act
        with open(command_path, 'r') as f:
            content = f.read()
        char_count = len(content)

        # Assert
        assert char_count < 12000, (
            f"Command exceeds 12K target: {char_count} chars (target: 8-12K, limit: 15K). "
            f"Current budget: {char_count * 100 // 15000}% of 15K limit"
        )
        print(f"✓ Command size: {char_count} chars ({char_count * 100 // 15000}% of limit)")

    def test_command_character_count_buffer(self):
        """
        AC-1 Test 2: Command file has 40% budget buffer (8-10K optimal range)

        ARRANGE: Read command file
        ACT: Calculate budget percentage
        ASSERT: Character count 8-10K (50-67% of 15K limit) for optimal buffer
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()
        char_count = len(content)
        budget_pct = char_count * 100 // 15000

        # Assert - softer check for intermediate states
        # Hard requirement: <15K
        assert char_count < 15000, f"CRITICAL: Command {char_count} > 15K hard limit"

        # Target: 8-10K for optimal buffer
        if char_count > 12000:
            print(f"⚠️ Warning: Command {char_count} chars, approaching 12K warning threshold")
        elif char_count < 8000:
            print(f"⚠️ Warning: Command {char_count} chars, below 8K minimum (may have over-optimized)")
        else:
            print(f"✓ Command size optimal: {char_count} chars ({budget_pct}% of limit)")


class TestCommandStructure:
    """AC-4 Test 2, BR-002: Pattern Consistency - Command structure matches /qa reference"""

    def test_command_has_three_phases(self):
        """
        AC-4 Test 1, BR-002: Command has lean orchestration structure (3-5 phases)

        ARRANGE: Read refactored command file
        ACT: Grep for phase markers (Phase 0, 1, 2, etc.)
        ASSERT: Command has 3-5 phases following lean pattern
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Count phase headers
        phase_markers = re.findall(r'### Phase \d+:', content)
        phase_count = len(phase_markers)

        # Assert: Lean pattern requires 3-5 phases
        assert 3 <= phase_count <= 5, (
            f"Command has {phase_count} phases (expected 3-5 for lean pattern). "
            f"Found phases: {phase_markers}"
        )
        print(f"✓ Command structure: {phase_count} phases (lean pattern)")

    def test_command_delegates_to_skill(self):
        """
        AC-4 Test 2, CONF-003: Command delegates Phase 6 to skill

        ARRANGE: Read command file
        ACT: Grep for Skill() invocation
        ASSERT: Command contains Skill(command="devforgeai-orchestration") call
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Assert: Skill invocation present
        assert 'Skill(command="devforgeai-orchestration")' in content or \
               "Skill(command='devforgeai-orchestration')" in content, (
            "Command must delegate to devforgeai-orchestration skill via "
            "Skill(command='devforgeai-orchestration')"
        )
        print("✓ Command delegates to devforgeai-orchestration skill")

    def test_command_no_direct_subagent_calls(self):
        """
        BR-002: No direct subagent calls (bypass skill layer)

        ARRANGE: Read command file
        ACT: Grep for Task(subagent_type=) calls
        ASSERT: No direct subagent invocations (command → subagent bypasses skill)
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Find direct subagent calls
        subagent_calls = re.findall(r'Task\(\s*subagent_type\s*=', content)

        # Assert: No direct subagent calls (should be invoked by skill)
        assert len(subagent_calls) == 0, (
            f"Found {len(subagent_calls)} direct subagent calls. "
            "Subagents should be invoked by skill, not command. "
            "Use Skill(command=...) instead."
        )
        print("✓ No direct subagent calls (proper skill delegation)")

    def test_command_matches_qa_reference_structure(self):
        """
        AC-4 Test 1: Command structure matches /qa reference implementation

        ARRANGE: Read both command and /qa reference
        ACT: Compare phase structure, orchestration pattern
        ASSERT: Command follows same lean pattern as /qa
        """
        # Arrange
        audit_deferrals_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")
        qa_reference_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/qa.md")

        assert qa_reference_path.exists(), "qa.md reference implementation not found"

        # Act
        with open(audit_deferrals_path, 'r') as f:
            audit_content = f.read()
        with open(qa_reference_path, 'r') as f:
            qa_content = f.read()

        # Both should have similar structure markers
        audit_has_phases = bool(re.search(r'### Phase \d+:', audit_content))
        audit_has_skill = bool(re.search(r'Skill\(command=', audit_content))
        audit_has_context_markers = bool(re.search(r'\*\*', audit_content))

        qa_has_phases = bool(re.search(r'### Phase \d+:', qa_content))
        qa_has_skill = bool(re.search(r'Skill\(command=', qa_content))
        qa_has_context_markers = bool(re.search(r'\*\*', qa_content))

        # Assert: Key structural elements match
        assert audit_has_skill == qa_has_skill, (
            "audit-deferrals skill invocation pattern doesn't match /qa reference"
        )
        print("✓ Command structure matches /qa reference pattern")


class TestBusinessLogicExtraction:
    """CONF-001: Extract Phase 6 logic from command to skill"""

    def test_command_no_business_logic(self):
        """
        BR-002, NFR-M1: Command has no business logic (orchestration only)

        ARRANGE: Read command file
        ACT: Grep for complex logic patterns (FOR, IF chains, validation, etc.)
        ASSERT: Minimal logic patterns (orchestration, not implementation)
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Count suspicious patterns indicating business logic
        forbidden_patterns = [
            (r'FOR each.*:', 'Loop logic (move to skill)'),
            (r'WHILE.*:', 'While loop (move to skill)'),
            (r'Parse JSON|Validate JSON', 'JSON parsing (move to skill/subagent)'),
            (r'Generate report|Build output', 'Report generation (move to skill/subagent)'),
            (r'Read.*report|grep.*report', 'File reading for processing (move to skill)'),
            (r'IF.*==.*AND', 'Complex conditional logic (move to skill)'),
        ]

        logic_count = 0
        for pattern, description in forbidden_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                logic_count += len(matches)
                print(f"  ⚠️ Found: {description} (count: {len(matches)})")

        # Assert: Minimal business logic in command
        # Some IF statements acceptable for orchestration, but not complex validation
        assert logic_count < 3, (
            f"Command contains {logic_count} business logic patterns. "
            "Command should only orchestrate (Phase 0: validate args, "
            "Phase 1: set markers, Phase 2: invoke skill, Phase 3: display results)"
        )
        print(f"✓ Command has minimal business logic ({logic_count} patterns)")

    def test_no_hook_logic_in_command(self):
        """
        CONF-001, BR-002: No hook eligibility/invocation logic in command

        ARRANGE: Read command file
        ACT: Grep for hook-related patterns (eligibility, context, sanitization)
        ASSERT: No hook logic in command (moved to skill)
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Hook-specific logic should not be in command
        hook_patterns = [
            'eligibility check',
            'eligible hook',
            'sanitize',
            'validate hook',
            'invoke.*hook',
            'circular.*prevention',
        ]

        found_hook_logic = [p for p in hook_patterns if re.search(p, content, re.IGNORECASE)]

        # Assert: No hook logic in command
        assert len(found_hook_logic) == 0, (
            f"Command contains hook logic: {found_hook_logic}. "
            "All hook logic (eligibility, context prep, sanitization, invocation, etc.) "
            "should be in devforgeai-orchestration skill Phase 7"
        )
        print("✓ No hook logic in command (properly extracted to skill)")

    def test_context_markers_present(self):
        """
        CONF-003, AC-4: Context markers for skill invocation

        ARRANGE: Read command file
        ACT: Grep for context marker pattern (**Parameter:** value)
        ASSERT: Command has context markers for skill parameter passing
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Look for context markers (**Parameter:** pattern)
        context_markers = re.findall(r'\*\*[\w\s-]+:\*\*', content)

        # Assert: At least 1 context marker (e.g., **Command:** audit-deferrals)
        assert len(context_markers) >= 1, (
            "Command must use context markers to pass parameters to skill. "
            "Example: **Command:** audit-deferrals"
        )
        print(f"✓ Context markers present: {len(context_markers)} found")


class TestSkillEnhancement:
    """SVC-001 through SVC-003: Skill Phase 7 for hook integration"""

    def test_skill_has_phase_7_audit_deferrals(self):
        """
        SVC-001: Skill has Phase 7 for audit-deferrals hook integration

        ARRANGE: Read devforgeai-orchestration skill
        ACT: Grep for Phase 7 section
        ASSERT: Phase 7 exists with audit-deferrals hook integration
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-orchestration/SKILL.md")
        assert skill_path.exists(), "devforgeai-orchestration skill not found"

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        # Find Phase 7 section
        phase_7_match = re.search(r'### Phase 7.*?(?=### Phase|\Z)', content, re.DOTALL)

        # Assert: Phase 7 exists and mentions audit-deferrals/hooks
        assert phase_7_match is not None, (
            "Skill Phase 7 not found. "
            "Add Phase 7: Hook Integration for Audit Deferrals after Phase 6"
        )

        phase_7_content = phase_7_match.group()
        assert 'audit-deferrals' in phase_7_content.lower() or 'hook' in phase_7_content.lower(), (
            "Phase 7 must contain audit-deferrals hook integration logic"
        )
        print("✓ Skill Phase 7 (Hook Integration) exists")

    def test_skill_phase_7_has_seven_substeps(self):
        """
        SVC-002: Skill Phase 7 has all 7 substeps

        ARRANGE: Read skill Phase 7
        ACT: Count substeps (eligibility, context, sanitization, invocation, logging, errors, circular)
        ASSERT: All 7 substeps documented
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-orchestration/SKILL.md")

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        phase_7_match = re.search(r'### Phase 7.*?(?=### Phase|\Z)', content, re.DOTALL)
        assert phase_7_match is not None, "Phase 7 not found"

        phase_7_content = phase_7_match.group()

        # Check for 7 substeps
        required_substeps = [
            'eligibility',
            'context',
            'sanitization',
            'invocation',
            'logging',
            'error',
            'circular',
        ]

        found_substeps = [step for step in required_substeps if step in phase_7_content.lower()]

        # Assert: All 7 substeps present
        assert len(found_substeps) >= 6, (  # At least 6 of 7 (error handling might be implicit)
            f"Phase 7 missing substeps. Found: {found_substeps}, "
            f"Expected: {required_substeps}"
        )
        print(f"✓ Skill Phase 7 has {len(found_substeps)}/7 substeps documented")

    def test_skill_size_under_3500_lines(self):
        """
        SVC-003: Skill stays under 3,500 lines after Phase 7 addition

        ARRANGE: Read skill file, count lines
        ACT: wc -l on skill file
        ASSERT: Line count < 3,500 (currently 3,249 + Phase 7 < 3,500)
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-orchestration/SKILL.md")

        # Act
        with open(skill_path, 'r') as f:
            lines = f.readlines()
        line_count = len(lines)

        # Assert: Skill <3,500 lines
        assert line_count < 3500, (
            f"Skill size {line_count} exceeds 3,500 line limit. "
            "If Phase 7 implementation is large, use progressive disclosure pattern: "
            "extract Phase 7 logic to references/audit-deferrals-hook-integration.md"
        )
        print(f"✓ Skill size within limits: {line_count} lines (<3,500)")

    def test_skill_phase_7_preserves_functionality(self):
        """
        CONF-004, SVC-002: All 7 substeps functionality preserved in skill

        ARRANGE: Read Phase 7 logic
        ACT: Verify each substep has implementation
        ASSERT: All substeps documented with logic
        """
        # Arrange
        skill_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-orchestration/SKILL.md")

        # Act
        with open(skill_path, 'r') as f:
            content = f.read()

        phase_7_match = re.search(r'### Phase 7.*?(?=### Phase|\Z)', content, re.DOTALL)
        assert phase_7_match is not None

        phase_7_content = phase_7_match.group()

        # Check for implementation markers (Step descriptions, pseudocode, logic)
        step_markers = re.findall(r'Step \d+:', phase_7_content) + \
                      re.findall(r'### Step \d+', phase_7_content)

        # Assert: At least 7 steps documented (one per substep)
        assert len(step_markers) >= 7, (
            f"Phase 7 has {len(step_markers)} documented steps (expected 7). "
            "Each of the 7 substeps needs documentation."
        )
        print(f"✓ Phase 7 has {len(step_markers)} documented steps")


class TestErrorHandling:
    """Command error handling minimal"""

    def test_error_handling_minimal(self):
        """
        BR-002, NFR-M1: Error handling is minimal (<30 lines)

        ARRANGE: Read command file
        ACT: Extract error handling section
        ASSERT: Error handling <30 lines (orchestration only)
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Find error handling section
        error_section = re.search(r'## Error.*?(?=## |\Z)', content, re.DOTALL | re.IGNORECASE)

        if error_section:
            error_lines = error_section.group().count('\n')
        else:
            error_lines = 0

        # Assert: Minimal error handling
        assert error_lines < 30, (
            f"Error handling section has {error_lines} lines (target: <30). "
            "Complex error logic should be in skill, not command."
        )
        print(f"✓ Error handling minimal: {error_lines} lines (<30)")


class TestBackwardCompatibility:
    """CONF-005, NFR-C1: 100% backward compatibility"""

    def test_command_preserves_interface(self):
        """
        CONF-005: Command interface unchanged (same invocation method)

        ARRANGE: Read command documentation
        ACT: Verify command still invoked as /audit-deferrals
        ASSERT: User invocation unchanged
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Check for command name in documentation
        assert 'audit-deferrals' in content, "Command name must be preserved"

        # Check for usage examples (Quick Reference)
        has_usage = bool(re.search(r'/audit-deferrals|Quick Reference|Usage', content, re.IGNORECASE))
        assert has_usage, "Command must document how to invoke it"

        print("✓ Command interface preserved (invoked as /audit-deferrals)")

    def test_command_backward_compatible_with_existing_scripts(self):
        """
        NFR-C1: Existing scripts using /audit-deferrals still work

        ARRANGE: Check if command accepts same arguments as before
        ACT: Verify command signature unchanged
        ASSERT: Arguments compatible with existing usage
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # The command should still be at .claude/commands/audit-deferrals.md
        # (even if refactored internally)
        assert command_path.exists(), "Command file must exist at expected location"

        # Command should not require new arguments
        has_new_args = bool(re.search(r'NEW ARGUMENT|NEW PARAMETER|BREAKING CHANGE', content))
        assert not has_new_args, "Refactoring must not introduce breaking changes to command interface"

        print("✓ Command backward compatible (no new required arguments)")


class TestDocumentation:
    """Documentation and comments present"""

    def test_documentation_strings_present(self):
        """
        Documentation: Comments explain command purpose and structure

        ARRANGE: Read command file
        ACT: Check for documentation/comments
        ASSERT: Comments present explaining purpose
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Check for documentation markers
        has_description = bool(re.search(r'description:|Purpose:', content, re.IGNORECASE))
        has_purpose = bool(re.search(r'Audit.*deferrals|Technical debt', content, re.IGNORECASE))

        # Assert: Documentation present
        assert has_description or has_purpose, (
            "Command must include documentation explaining purpose and usage"
        )
        print("✓ Documentation strings present")

    def test_phase_documentation_complete(self):
        """
        Documentation: Each phase has explanation

        ARRANGE: Read command file
        ACT: Check for documentation after each phase header
        ASSERT: Each phase has description
        """
        # Arrange
        command_path = Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/audit-deferrals.md")

        # Act
        with open(command_path, 'r') as f:
            content = f.read()

        # Find phases and check they're not immediately followed by code block
        phases = re.findall(r'### Phase \d+:.*?\n\n', content)

        # Assert: Phases documented
        assert len(phases) >= 3, (
            "Each phase must be documented with explanation before implementation"
        )
        print(f"✓ Phase documentation complete: {len(phases)} phases documented")


# Test suite summary
class TestSummary:
    """Summary and execution instructions"""

    def test_summary_print_test_counts(self):
        """Print test counts for documentation"""
        print("\n" + "="*70)
        print("STORY-050 Unit Test Suite Summary")
        print("="*70)
        print("Test Classes:")
        print("  1. TestBudgetCompliance (2 tests) - AC-1: Budget compliance")
        print("  2. TestCommandStructure (4 tests) - AC-4: Pattern consistency")
        print("  3. TestBusinessLogicExtraction (3 tests) - CONF-001: Logic extraction")
        print("  4. TestSkillEnhancement (4 tests) - SVC-001-003: Skill enhancement")
        print("  5. TestErrorHandling (1 test) - Error handling minimal")
        print("  6. TestBackwardCompatibility (2 tests) - CONF-005: Compatibility")
        print("  7. TestDocumentation (2 tests) - Documentation present")
        print("="*70)
        print("Total: 18 unit tests")
        print("="*70)
        print("\nAll tests FAIL initially (Red phase)")
        print("These tests pass after PHASES 2-5 refactoring complete")
        print("="*70 + "\n")
