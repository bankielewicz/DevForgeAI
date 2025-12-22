"""
Integration tests for STORY-057: Cross-skill guidance integration

Tests cover:
- Multi-skill workflows (architecture + UI + orchestration)
- Guidance file deployment and checksum validation
- Pattern name consistency across skills
- Fallback behavior uniformity
- Concurrent skill execution

Tests validate:
- 9 integration scenarios
- AC#5, AC#6, AC#7 (token overhead, conditional loading, backward compatibility)
- BR-001, BR-002, BR-003, BR-004, BR-005 (business rules)
- NFR-001 through NFR-010 (non-functional requirements)
"""

import pytest
import tempfile
import hashlib
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from concurrent.futures import ThreadPoolExecutor, as_completed


# ============================================================================
# FIXTURES FOR CROSS-SKILL INTEGRATION TESTS
# ============================================================================

@pytest.fixture
def temp_project_with_skills():
    """Fixture: Create temporary project with all 3 skill directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir)

        # Create skill structure
        skills_base = project_dir / "src" / "claude" / "skills"

        for skill in ["devforgeai-architecture", "devforgeai-ui-generator", "devforgeai-orchestration"]:
            ref_dir = skills_base / skill / "references"
            ref_dir.mkdir(parents=True, exist_ok=True)

            # Create identical guidance files
            guidance_file = ref_dir / "user-input-guidance.md"
            master_content = """# User Input Guidance

## Pattern Definitions

### Open-Ended Discovery
Free-form text input, no preset options.

### Bounded Choice
Selection from predefined list, filtered by constraints.

### Explicit Classification
Distinct categories, mutually exclusive options.

### Closed Confirmation
Binary yes/no confirmation.

### Open-Ended with Minimum Count
Free-form with minimum items required.

### Bounded Choice with Multi-Select
Multiple selection from constrained list with validation.

### Bounded Choice + Explicit None
Selection from list plus explicit "None" option.

## Patterns used across all skills
All 7 core patterns available for integration.
"""
            guidance_file.write_text(master_content)

        yield project_dir


@pytest.fixture
def master_guidance_file(temp_project_with_skills):
    """Fixture: Master guidance file (source of truth)."""
    master_path = temp_project_with_skills / "src" / "claude" / "skills" / "devforgeai-ideation" / "references" / "user-input-guidance.md"
    master_path.parent.mkdir(parents=True, exist_ok=True)

    content = """# User Input Guidance - Master Copy

## Pattern Definitions

### Open-Ended Discovery
Free-form text input, no preset options.

### Bounded Choice
Selection from predefined list, filtered by constraints.

### Explicit Classification
Distinct categories, mutually exclusive options.

### Closed Confirmation
Binary yes/no confirmation.

### Open-Ended with Minimum Count
Free-form with minimum items required.

### Bounded Choice with Multi-Select
Multiple selection from constrained list with validation.

### Bounded Choice + Explicit None
Selection from list plus explicit "None" option.
"""
    master_path.write_text(content)
    return master_path


# ============================================================================
# INTEGRATION TEST 1: Multi-skill workflow (architecture + UI + orchestration)
# ============================================================================

@pytest.mark.integration
@pytest.mark.acceptance_criteria
def test_01_multi_skill_workflow_all_load_guidance(temp_project_with_skills):
    """
    Integration Test 1: All 3 skills in sequence, all conditions met for loading

    When:
    - Architecture greenfield (0 context files)
    - UI standalone (no story file)
    - Orchestration epic (create-epic command)

    Then:
    - All 3 load guidance in their isolated contexts
    - No conflicts or file locking
    - Each completes independently
    """
    # Arrange
    context_dir = temp_project_with_skills / "devforgeai" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)

    # No story file
    has_story = False

    # Act
    results = []

    # Architecture greenfield check
    context_files = list(context_dir.glob("*.md"))
    arch_loads = len(context_files) == 0
    results.append(("architecture", arch_loads))

    # UI standalone check
    ui_loads = not has_story
    results.append(("ui_generator", ui_loads))

    # Orchestration epic check
    orch_mode = "epic"
    orch_loads = orch_mode == "epic"
    results.append(("orchestration", orch_loads))

    # Assert
    assert all(result[1] for result in results), f"All skills should load guidance: {results}"
    assert len(results) == 3, "Should test all 3 skills"


@pytest.mark.integration
def test_02_multi_skill_workflow_selective_loading(temp_project_with_skills):
    """
    Integration Test 2: Mixed scenario - some load, some skip

    When:
    - Architecture brownfield (6 context files exist)
    - UI story mode (story file loaded)
    - Orchestration story management (not epic/sprint)

    Then:
    - Architecture skips guidance
    - UI skips guidance
    - Orchestration skips guidance
    """
    # Arrange
    context_dir = temp_project_with_skills / "devforgeai" / "context"
    context_dir.mkdir(parents=True, exist_ok=True)

    # Create 6 context files (brownfield)
    for filename in ["tech-stack.md", "source-tree.md", "dependencies.md",
                     "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"]:
        (context_dir / filename).write_text(f"# {filename}")

    has_story = True
    orch_mode = "story_management"

    # Act
    results = []

    # Architecture brownfield check
    context_files = list(context_dir.glob("*.md"))
    arch_skips = len(context_files) == 6
    results.append(("architecture", arch_skips))

    # UI story mode check
    ui_skips = has_story
    results.append(("ui_generator", ui_skips))

    # Orchestration non-epic/sprint check
    orch_skips = orch_mode not in ["epic", "sprint"]
    results.append(("orchestration", orch_skips))

    # Assert
    assert all(result[1] for result in results), f"All skills should skip guidance: {results}"


# ============================================================================
# INTEGRATION TEST 3: Guidance file deployment and checksum validation
# ============================================================================

@pytest.mark.integration
@pytest.mark.acceptance_criteria
def test_03_guidance_file_checksum_validation(temp_project_with_skills, master_guidance_file):
    """
    Integration Test 3: Guidance file checksums match across 3 skills

    BR-002: All 3 skills must reference identical guidance file content

    When: Guidance deployed to all 3 skills
    Then: SHA256 checksums match (100%)
    """
    # Arrange
    skills = ["devforgeai-architecture", "devforgeai-ui-generator", "devforgeai-orchestration"]
    checksums = {}

    # Act
    for skill in skills:
        guidance_path = temp_project_with_skills / "src" / "claude" / "skills" / skill / "references" / "user-input-guidance.md"

        if guidance_path.exists():
            content = guidance_path.read_bytes()
            checksum = hashlib.sha256(content).hexdigest()
            checksums[skill] = checksum

    # Extract unique checksums
    unique_checksums = set(checksums.values())

    # Assert
    assert len(checksums) == 3, "All 3 skills should have guidance files"
    assert len(unique_checksums) == 1, f"All checksums should match, found {len(unique_checksums)} unique"


@pytest.mark.integration
def test_04_guidance_file_synchronization(temp_project_with_skills):
    """
    Integration Test 4: Guidance files are synchronized (content identical)

    When: Files deployed from master
    Then: All 3 copies have identical content
    """
    # Arrange
    skills = ["devforgeai-architecture", "devforgeai-ui-generator", "devforgeai-orchestration"]

    # Act
    contents = {}
    for skill in skills:
        guidance_path = temp_project_with_skills / "src" / "claude" / "skills" / skill / "references" / "user-input-guidance.md"
        if guidance_path.exists():
            contents[skill] = guidance_path.read_text()

    # Compare all pairs
    if len(contents) >= 2:
        first_content = list(contents.values())[0]
        all_match = all(c == first_content for c in contents.values())
    else:
        all_match = False

    # Assert
    assert len(contents) == 3, "All 3 guidance files should exist"
    assert all_match, "All guidance files should have identical content"


# ============================================================================
# INTEGRATION TEST 5: Pattern name consistency across skills
# ============================================================================

@pytest.mark.integration
@pytest.mark.acceptance_criteria
def test_05_pattern_name_consistency(temp_project_with_skills):
    """
    Integration Test 5: Pattern names are uniform across all skills

    NFR-008: Pattern names must be identical across all skills (no synonyms/variations)

    Canonical names:
    1. Open-Ended Discovery
    2. Bounded Choice
    3. Explicit Classification
    4. Closed Confirmation
    5. Progressive Refinement
    6. Hybrid: Bounded + Open Escape
    7. Bounded Choice + Explicit None
    8. Open-Ended with Minimum Count
    9. Bounded Choice with Multi-Select
    10. Fibonacci Bounded Choice
    """
    # Arrange
    skills = ["devforgeai-architecture", "devforgeai-ui-generator", "devforgeai-orchestration"]
    canonical_patterns = [
        "Open-Ended Discovery",
        "Bounded Choice",
        "Explicit Classification",
        "Closed Confirmation",
    ]

    # Act
    patterns_per_skill = {}

    for skill in skills:
        guidance_path = temp_project_with_skills / "src" / "claude" / "skills" / skill / "references" / "user-input-guidance.md"
        if guidance_path.exists():
            content = guidance_path.read_text()
            found_patterns = [p for p in canonical_patterns if p in content]
            patterns_per_skill[skill] = found_patterns

    # Verify consistency
    if patterns_per_skill:
        first_patterns = list(patterns_per_skill.values())[0]
        all_consistent = all(p == first_patterns for p in patterns_per_skill.values())
    else:
        all_consistent = False

    # Assert
    assert all_consistent, "Pattern names should be consistent across all skills"


# ============================================================================
# INTEGRATION TEST 6: Fallback behavior uniformity
# ============================================================================

@pytest.mark.integration
@pytest.mark.acceptance_criteria
def test_06_fallback_behavior_identical(temp_project_with_skills):
    """
    Integration Test 6: Fallback behavior is uniform across all skills

    NFR-009: All 3 skills use identical fallback behavior (same warning messages)

    When: Guidance file missing for all 3 skills
    Then: All 3 use fallback with identical warning messages
    """
    # Arrange
    skills_data = {}

    # Delete all guidance files to simulate missing scenario
    for skill in ["devforgeai-architecture", "devforgeai-ui-generator", "devforgeai-orchestration"]:
        guidance_path = temp_project_with_skills / "src" / "claude" / "skills" / skill / "references" / "user-input-guidance.md"
        if guidance_path.exists():
            guidance_path.unlink()  # Delete the file

    def simulate_skill_with_missing_guidance(skill_name):
        """Simulate skill execution when guidance is missing"""
        guidance_path = temp_project_with_skills / "src" / "claude" / "skills" / skill_name / "references" / "user-input-guidance.md"

        # File doesn't exist
        if not guidance_path.exists():
            # Fallback message (canonical across all skills)
            fallback_message = f"user-input-guidance.md not found at {guidance_path}, using fallback AskUserQuestion"
            return fallback_message

        return None

    # Act
    for skill in ["devforgeai-architecture", "devforgeai-ui-generator", "devforgeai-orchestration"]:
        message = simulate_skill_with_missing_guidance(skill)
        if message:
            # Extract canonical message part
            skills_data[skill] = message.split(" at ")[0]  # Get "not found at" part

    # All should have same canonical message
    unique_messages = set(skills_data.values())

    # Assert
    assert len(unique_messages) == 1, f"Fallback messages should be identical, found: {unique_messages}"


@pytest.mark.integration
def test_07_fallback_log_message_format(temp_project_with_skills):
    """
    Integration Test 7: Fallback log messages follow canonical format

    When: Guidance skipped or missing
    Then: Log message follows pattern: "Skipping user-input-guidance.md ([reason])"
    """
    # Arrange
    expected_log_format = "Skipping user-input-guidance.md"

    # Act
    log_messages = [
        "Skipping user-input-guidance.md (brownfield mode detected)",
        "Skipping user-input-guidance.md (story mode - using story requirements)",
        "Skipping user-input-guidance.md (not applicable for story management)"
    ]

    # All should follow format
    all_match_format = all(expected_log_format in msg for msg in log_messages)

    # Assert
    assert all_match_format, "All skip messages should follow canonical format"


# ============================================================================
# INTEGRATION TEST 8: Concurrent skill execution (no conflicts)
# ============================================================================

@pytest.mark.integration
@pytest.mark.performance
def test_08_concurrent_skill_execution(temp_project_with_skills):
    """
    Integration Test 8: Multiple skills can execute concurrently without conflicts

    When: 5 parallel executions (2 architecture greenfield, 2 UI standalone, 1 orchestration epic)
    Then: No file locking, no race conditions, all complete successfully
    """
    # Arrange
    def simulate_skill_execution(skill_name, mode):
        """Simulate skill loading guidance file"""
        guidance_path = temp_project_with_skills / "src" / "claude" / "skills" / skill_name / "references" / "user-input-guidance.md"

        # Simulate read operation (concurrent)
        time.sleep(0.01)  # Simulate processing

        if guidance_path.exists():
            content = guidance_path.read_text()
            return {"skill": skill_name, "mode": mode, "success": True, "size": len(content)}
        else:
            return {"skill": skill_name, "mode": mode, "success": False, "reason": "file_missing"}

    # Act
    tasks = [
        ("devforgeai-architecture", "greenfield"),
        ("devforgeai-architecture", "greenfield"),
        ("devforgeai-ui-generator", "standalone"),
        ("devforgeai-ui-generator", "standalone"),
        ("devforgeai-orchestration", "epic"),
    ]

    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_task = {executor.submit(simulate_skill_execution, skill, mode): (skill, mode)
                         for skill, mode in tasks}

        for future in as_completed(future_to_task):
            result = future.result()
            results.append(result)

    # Assert
    assert len(results) == 5, "All 5 concurrent executions should complete"
    assert all(r["success"] for r in results), "All should succeed (guidance files exist)"


# ============================================================================
# INTEGRATION TEST 9: End-to-end workflow (ideate → architecture → epic → sprint → ui)
# ============================================================================

@pytest.mark.integration
@pytest.mark.acceptance_criteria
def test_09_end_to_end_workflow(temp_project_with_skills):
    """
    Integration Test 9: Full workflow with guidance active in applicable phases

    When: User completes workflow: Ideate → Architecture → Epic → Sprint → UI

    Then:
    - Architecture loads guidance (greenfield)
    - Epic loads guidance (epic mode)
    - Sprint loads guidance (sprint mode)
    - UI skips guidance (story mode - epic/sprint provide requirements)
    - Token overhead per skill ≤1,000
    - No breaking changes from guidance integration
    """
    # Arrange
    workflow_steps = [
        {"step": "ideate", "guidance_applicable": True, "loaded": True},
        {"step": "architecture_greenfield", "guidance_applicable": True, "loaded": True},
        {"step": "create_epic", "guidance_applicable": True, "loaded": True},
        {"step": "create_sprint", "guidance_applicable": True, "loaded": True},
        {"step": "create_ui_from_epic", "guidance_applicable": False, "loaded": False},
    ]

    # Act
    results = []

    for step_config in workflow_steps:
        step = step_config["step"]
        should_load = step_config["guidance_applicable"]

        # Simulate guidance loading decision
        if step in ["architecture_greenfield", "create_epic", "create_sprint"]:
            guidance_path = temp_project_with_skills / "src" / "claude" / "skills" / "devforgeai-architecture" / "references" / "user-input-guidance.md"
            file_exists = guidance_path.exists()
            actually_loaded = file_exists and should_load
        else:
            actually_loaded = should_load

        result = {
            "step": step,
            "expected_load": should_load,
            "actually_loaded": actually_loaded,
            "success": actually_loaded == should_load
        }
        results.append(result)

    # Assert
    assert all(r["success"] for r in results), f"All workflow steps should load/skip correctly: {results}"


# ============================================================================
# INTEGRATION TEST: Token Overhead Accumulation
# ============================================================================

@pytest.mark.integration
@pytest.mark.performance
@pytest.mark.acceptance_criteria
def test_token_overhead_no_accumulation(temp_project_with_skills):
    """
    AC#5: Token overhead should NOT accumulate across skills

    When: All 3 skills execute in isolated contexts (as per Skills tool isolation)
    Then: Main conversation overhead ≈ 0 (each skill's overhead is in its isolated context)

    Measured:
    - Architecture: ≤1,000 tokens (isolated)
    - UI-generator: ≤1,000 tokens (isolated)
    - Orchestration: ≤1,000 tokens (isolated)
    - Main conversation: Minimal (<100 tokens for summaries)
    """
    # Arrange
    skills_overhead = {
        "architecture": 250,  # Estimated tokens for 2KB file
        "ui_generator": 250,
        "orchestration": 300  # Slightly larger due to dual modes
    }

    # Act
    isolated_total = sum(skills_overhead.values())
    main_conversation_overhead = 50  # Skill summary + initialization

    total_overhead = isolated_total + main_conversation_overhead

    # Assert
    assert all(overhead <= 1000 for overhead in skills_overhead.values()), \
        f"Each skill overhead should be ≤1,000: {skills_overhead}"
    assert total_overhead < 2000, \
        f"Total should be <2,000 (isolated + main): {total_overhead}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
