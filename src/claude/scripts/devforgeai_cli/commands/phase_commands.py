"""
Phase Validation CLI Commands.

Provides CLI commands for phase state management in the
Phase Execution Enforcement System.

Commands:
- phase-init: Create state file (exit 0=created, 1=exists, 2=invalid ID)
- phase-check: Validate transition (exit 0=allowed, 1=blocked, 2=missing subagents)
- phase-complete: Mark phase done (exit 0=success, 1=incomplete)
- phase-status: Show current state (exit 0=success, 1=not found)
- phase-record: Record subagent invocation (exit 0=recorded, 1=not found, 2=error)
"""

import json
import sys
from pathlib import Path


def _get_valid_phases():
    """Get VALID_PHASES constant from phase_state module."""
    from ..phase_state import PhaseState
    return PhaseState.VALID_PHASES


def _get_phase_state(project_root: str):
    """
    Get PhaseState instance with graceful error handling.

    PhaseState is co-located in the same package for simple imports.

    Args:
        project_root: Path to the project root directory

    Returns:
        PhaseState instance for phase tracking

    Raises:
        ImportError: If phase_state.py module cannot be imported, with
                     helpful diagnostic message including:
                     - Original error details
                     - Expected module location
                     - Fix instructions
                     - Note about /dev workflow continuation
    """
    try:
        from ..phase_state import PhaseState
        return PhaseState(project_root=Path(project_root))
    except ImportError as e:
        raise ImportError(
            f"PhaseState module not found: {e}\n\n"
            "The phase_state.py module is required for phase tracking.\n"
            "Expected location: .claude/scripts/devforgeai_cli/phase_state.py\n\n"
            "To fix:\n"
            "  1. Ensure STORY-253 (PhaseState module) is implemented\n"
            "  2. Reinstall CLI using one of these methods:\n\n"
            "     # Using pipx (recommended for CLI tools):\n"
            "     pipx install -e .claude/scripts/ --force\n\n"
            "     # Using virtual environment:\n"
            "     python3 -m venv .venv && source .venv/bin/activate\n"
            "     pip install -e .claude/scripts/\n\n"
            "     # Direct pip (if not externally-managed):\n"
            "     pip install -e .claude/scripts/\n\n"
            "  3. Retry your command\n\n"
            "Note: The /dev workflow can continue without CLI-based phase\n"
            "enforcement if this module is unavailable. Phase tracking is\n"
            "optional and does not block story development."
        ) from e


def phase_init_command(
    story_id: str,
    project_root: str,
    format: str = "text",
    workflow: str = "dev"
) -> int:
    """
    Initialize phase state file for a story.

    Args:
        story_id: Story identifier (e.g., "STORY-001")
        project_root: Project root directory
        format: Output format ("text" or "json")
        workflow: Workflow type ("dev" or "qa")

    Returns:
        Exit code: 0=created, 1=exists, 2=invalid ID or invalid workflow
    """
    try:
        # Validate workflow parameter (STORY-517, STORY-521)
        from ..phase_state import VALID_WORKFLOWS, WORKFLOW_SCHEMAS
        if workflow not in VALID_WORKFLOWS:
            if format == "json":
                print(json.dumps({
                    "success": False,
                    "error": f"Invalid workflow: '{workflow}'. Must be one of: {VALID_WORKFLOWS}",
                    "story_id": story_id
                }))
            else:
                print(f"ERROR: Invalid workflow: '{workflow}'. Must be one of: {VALID_WORKFLOWS}")
            return 2

        ps = _get_phase_state(project_root)

        # Determine state file path based on workflow type (STORY-521)
        if workflow == "dev":
            state_path = ps._get_state_path(story_id)
        elif workflow == "qa":
            state_path = ps._get_qa_state_path(story_id)
        else:
            state_path = ps.workflows_dir / f"{story_id}-{workflow}-phase-state.json"

        if state_path.exists():
            label = "QA state file" if workflow == "qa" else "State file"
            if format == "json":
                print(json.dumps({
                    "success": False,
                    "error": f"{label} already exists",
                    "story_id": story_id,
                    "path": str(state_path)
                }))
            else:
                print(f"{label} already exists for {story_id}")
                print(f"  Path: {state_path}")
            return 1

        # Use unified create_workflow for all workflow types (STORY-521)
        state = ps.create_workflow(story_id, workflow)

        if format == "json":
            result_data = {
                "success": True,
                "story_id": story_id,
                "path": str(state_path),
                "current_phase": state["current_phase"]
            }
            if workflow != "dev":
                result_data["workflow"] = workflow
            print(json.dumps(result_data))
        else:
            if workflow == "qa":
                label = f"Created QA phase state for {story_id}"
            elif workflow == "dev":
                label = f"Created phase state for {story_id}"
            else:
                label = f"Created {workflow} phase state for {story_id}"
            print(label)
            print(f"  Path: {state_path}")
            print(f"  Current phase: {state['current_phase']}")

        return 0

    except ValueError as e:
        if format == "json":
            print(json.dumps({
                "success": False,
                "error": str(e),
                "story_id": story_id
            }))
        else:
            print(f"ERROR: {e}")
        return 2

    except Exception as e:
        if format == "json":
            print(json.dumps({
                "success": False,
                "error": str(e),
                "story_id": story_id
            }))
        else:
            print(f"ERROR: {e}")
        return 2


def phase_check_command(
    story_id: str,
    from_phase: str,
    to_phase: str,
    project_root: str,
    format: str = "text"
) -> int:
    """
    Check if phase transition is allowed.

    Args:
        story_id: Story identifier
        from_phase: Source phase (e.g., "01")
        to_phase: Target phase (e.g., "02")
        project_root: Project root directory
        format: Output format

    Returns:
        Exit code: 0=allowed, 1=blocked, 2=missing subagents
    """
    try:
        ps = _get_phase_state(project_root)
        state = ps.read(story_id)

        if state is None:
            if format == "json":
                print(json.dumps({
                    "allowed": False,
                    "error": "State file not found",
                    "story_id": story_id
                }))
            else:
                print(f"State file not found for {story_id}")
            return 1

        # Rule 1: Previous phase must be completed
        if state["phases"][from_phase]["status"] != "completed":
            if format == "json":
                print(json.dumps({
                    "allowed": False,
                    "error": f"Phase {from_phase} not completed",
                    "story_id": story_id,
                    "from_phase": from_phase,
                    "to_phase": to_phase
                }))
            else:
                print(f"Phase {from_phase} not completed")
            return 1

        # Rule 2: Must be sequential (no skipping)
        # Use ordered VALID_PHASES list to handle decimal phases (4.5, 5.5)
        valid_phases = _get_valid_phases()
        try:
            from_idx = valid_phases.index(from_phase)
            to_idx = valid_phases.index(to_phase)
        except ValueError:
            if format == "json":
                print(json.dumps({
                    "allowed": False,
                    "error": f"Invalid phase: from='{from_phase}' or to='{to_phase}'",
                    "story_id": story_id
                }))
            else:
                print(f"Invalid phase: from='{from_phase}' or to='{to_phase}'")
            return 1

        if to_idx != from_idx + 1:
            expected = valid_phases[from_idx + 1] if from_idx + 1 < len(valid_phases) else "N/A"
            if format == "json":
                print(json.dumps({
                    "allowed": False,
                    "error": f"Cannot skip phases: {from_phase} -> {to_phase}, expected {expected}",
                    "story_id": story_id
                }))
            else:
                print(f"Cannot skip phases: {from_phase} -> {to_phase}")
            return 1

        # Rule 3: All required subagents must be invoked (supports OR-groups per STORY-306)
        # Fix: STORY-464 - nested lists (OR-groups) are unhashable, cannot use set()
        required = state["phases"][from_phase].get("subagents_required", [])
        invoked = set(state["phases"][from_phase].get("subagents_invoked", []))
        missing = []

        for requirement in required:
            if isinstance(requirement, list):
                # OR logic (STORY-306): any one subagent in list satisfies requirement
                if not any(subagent_name in invoked for subagent_name in requirement):
                    missing.append(f"({' OR '.join(requirement)})")
            else:
                # Simple requirement: subagent must be in invoked set
                if requirement not in invoked:
                    missing.append(requirement)

        if missing:
            if format == "json":
                print(json.dumps({
                    "allowed": False,
                    "error": f"Missing subagents: {missing}",
                    "story_id": story_id,
                    "missing_subagents": missing
                }))
            else:
                print(f"Missing subagents for phase {from_phase}:")
                for agent in missing:
                    print(f"  - {agent}")
            return 2

        # Transition allowed
        if format == "json":
            print(json.dumps({
                "allowed": True,
                "story_id": story_id,
                "from_phase": from_phase,
                "to_phase": to_phase
            }))
        else:
            print(f"Transition allowed: {from_phase} -> {to_phase}")

        return 0

    except Exception as e:
        if format == "json":
            print(json.dumps({
                "allowed": False,
                "error": str(e),
                "story_id": story_id
            }))
        else:
            print(f"ERROR: {e}")
        return 1


def phase_complete_command(
    story_id: str,
    phase: str,
    checkpoint_passed: bool,
    project_root: str,
    format: str = "text",
    workflow: str = "dev"
) -> int:
    """
    Mark a phase as complete.

    Args:
        story_id: Story identifier
        phase: Phase to complete (e.g., "02")
        checkpoint_passed: Whether checkpoint validation passed
        project_root: Project root directory
        format: Output format
        workflow: Workflow type ("dev" or "qa")

    Returns:
        Exit code: 0=success, 1=incomplete/error
    """
    try:
        ps = _get_phase_state(project_root)

        # Use unified complete_workflow_phase for all workflow types (STORY-521)
        state = ps.complete_workflow_phase(story_id, workflow, phase, checkpoint_passed)

        if format == "json":
            result_data = {
                "success": True,
                "story_id": story_id,
                "completed_phase": phase,
                "current_phase": state["current_phase"],
                "checkpoint_passed": checkpoint_passed
            }
            if workflow != "dev":
                result_data["workflow"] = workflow
            print(json.dumps(result_data))
        else:
            if workflow == "qa":
                print(f"QA phase {phase} completed for {story_id}")
            elif workflow == "dev":
                print(f"Phase {phase} completed for {story_id}")
            else:
                print(f"{workflow.capitalize()} phase {phase} completed for {story_id}")
            print(f"  Current phase: {state['current_phase']}")
            print(f"  Checkpoint passed: {checkpoint_passed}")

        return 0

    except ValueError as e:
        # Step validation failure (STORY-517) - exit code 1
        if format == "json":
            print(json.dumps({
                "success": False,
                "error": str(e),
                "story_id": story_id
            }))
        else:
            print(f"ERROR: {e}")
        return 1

    except Exception as e:
        if format == "json":
            print(json.dumps({
                "success": False,
                "error": str(e),
                "story_id": story_id
            }))
        else:
            print(f"ERROR: {e}")
        return 1


def phase_status_command(
    story_id: str,
    project_root: str,
    format: str = "text"
) -> int:
    """
    Display current phase status.

    Args:
        story_id: Story identifier
        project_root: Project root directory
        format: Output format

    Returns:
        Exit code: 0=success, 1=not found
    """
    try:
        ps = _get_phase_state(project_root)
        state = ps.read(story_id)

        if state is None:
            if format == "json":
                print(json.dumps({
                    "found": False,
                    "error": "State file not found",
                    "story_id": story_id
                }))
            else:
                print(f"State file not found for {story_id}")
            return 1

        if format == "json":
            print(json.dumps(state, indent=2))
        else:
            print(f"Story: {state['story_id']}")
            print(f"Started: {state['workflow_started']}")
            print(f"Current Phase: {state['current_phase']}")
            print(f"Blocking: {state['blocking_status']}")
            print()
            print("Phase Status:")
            for phase_id, phase_data in state["phases"].items():
                status = phase_data["status"]
                marker = "x" if status == "completed" else " "
                print(f"  [{marker}] Phase {phase_id}: {status}")
                if phase_data.get("subagents_invoked"):
                    print(f"      Subagents: {', '.join(phase_data['subagents_invoked'])}")

        return 0

    except Exception as e:
        if format == "json":
            print(json.dumps({
                "found": False,
                "error": str(e),
                "story_id": story_id
            }))
        else:
            print(f"ERROR: {e}")
        return 1


def phase_record_command(
    story_id: str,
    phase: str,
    subagent: str,
    project_root: str,
    format: str = "text"
) -> int:
    """
    Record a subagent invocation for a phase.

    Args:
        story_id: Story identifier (e.g., "STORY-001")
        phase: Phase ID (e.g., "02")
        subagent: Subagent name that was invoked
        project_root: Project root directory
        format: Output format ("text" or "json")

    Returns:
        Exit code: 0=recorded, 1=not found, 2=error
    """
    try:
        ps = _get_phase_state(project_root)
        ps.record_subagent(story_id, phase, subagent)

        if format == "json":
            print(json.dumps({
                "success": True,
                "story_id": story_id,
                "phase": phase,
                "subagent": subagent
            }))
        else:
            print(f"Recorded subagent '{subagent}' for {story_id} phase {phase}")

        return 0

    except Exception as e:
        if format == "json":
            print(json.dumps({
                "success": False,
                "error": str(e),
                "story_id": story_id
            }))
        else:
            print(f"ERROR: {e}")
        return 2


# =============================================================================
# STORY-525: Phase Record Step Command
# =============================================================================


def phase_record_step_command(
    story_id: str,
    phase: str,
    step_id: str,
    project_root: str,
    format: str = "text"
) -> int:
    """
    Record a step completion for a phase.

    Validates step_id against the registry before recording.

    Args:
        story_id: Story identifier (e.g., "STORY-525")
        phase: Phase ID (e.g., "02")
        step_id: Step identifier (e.g., "02.1")
        project_root: Project root directory
        format: Output format ("text" or "json")

    Returns:
        Exit code: 0=recorded, 1=error
    """
    try:
        ps = _get_phase_state(project_root)

        # Validate step_id against registry (hard error if missing)
        registry_path = ps._get_registry_path()
        if not registry_path.exists():
            msg = f"Registry not found at {registry_path}"
            print(f"ERROR: {msg}", file=sys.stderr)
            return 1
        registry_content = registry_path.read_text(encoding="utf-8")
        registry = json.loads(registry_content)
        phase_data = registry.get(phase, {})
        valid_step_ids = [s["id"] for s in phase_data.get("steps", [])]
        if step_id not in valid_step_ids:
            msg = f"Unknown step_id '{step_id}' for phase {phase}"
            print(msg, file=sys.stderr)
            return 1

        ps.record_step(story_id, phase, step_id)

        if format == "json":
            print(json.dumps({
                "success": True,
                "story_id": story_id,
                "phase": phase,
                "step_id": step_id
            }))
        else:
            print(f"Recorded step '{step_id}' for {story_id} phase {phase}")

        return 0

    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


# =============================================================================
# STORY-517: QA Marker Cleanup (RCA-045 REC-3)
# =============================================================================


def cleanup_qa_markers(
    story_id: str,
    project_root: str,
) -> int:
    """
    Remove legacy .qa-phase-N.marker files after QA completes.

    Per RCA-045 REC-3: qa-phase-state.json supersedes marker files.
    Old markers should be deleted during Phase 4 cleanup.

    Args:
        story_id: Story identifier (e.g., "STORY-517")
        project_root: Project root directory

    Returns:
        Number of marker files deleted
    """
    from pathlib import Path
    reports_dir = Path(project_root) / "devforgeai" / "qa" / "reports" / story_id
    deleted = 0

    if reports_dir.exists():
        for marker in reports_dir.glob(".qa-phase-*.marker"):
            marker.unlink()
            deleted += 1

    return deleted


# =============================================================================
# STORY-188: Observation Constants
# =============================================================================

# Observation categories (AC-4)
VALID_CATEGORIES = ["friction", "gap", "success", "pattern"]

# Observation severities (AC-5)
VALID_SEVERITIES = ["low", "medium", "high"]


def phase_observe_command(
    story_id: str,
    phase: str,
    category: str,
    note: str,
    severity: str = "medium",
    project_root: str = ".",
    format: str = "text"
) -> int:
    """
    Record a workflow observation for a phase.

    Captures friction, gaps, successes, and patterns during
    TDD workflow execution for AI analysis.

    Args:
        story_id: Story identifier (e.g., "STORY-188")
        phase: Phase ID (e.g., "04")
        category: Observation category (friction, gap, success, pattern)
        note: Description of the observation
        severity: Severity level (low, medium, high). Default: medium
        project_root: Project root directory
        format: Output format ("text" or "json")

    Returns:
        Exit code: 0=recorded, 1=not found, 2=invalid input
    """
    try:
        # Validate category
        if category not in VALID_CATEGORIES:
            if format == "json":
                print(json.dumps({
                    "success": False,
                    "error": f"Invalid category: '{category}'. Must be one of: {VALID_CATEGORIES}",
                    "story_id": story_id
                }))
            else:
                print(f"ERROR: Invalid category '{category}'")
                print(f"  Valid categories: {', '.join(VALID_CATEGORIES)}")
            return 2

        # Validate severity
        if severity not in VALID_SEVERITIES:
            if format == "json":
                print(json.dumps({
                    "success": False,
                    "error": f"Invalid severity: '{severity}'. Must be one of: {VALID_SEVERITIES}",
                    "story_id": story_id
                }))
            else:
                print(f"ERROR: Invalid severity '{severity}'")
                print(f"  Valid severities: {', '.join(VALID_SEVERITIES)}")
            return 2

        # Validate note is not empty
        if not note or not note.strip():
            if format == "json":
                print(json.dumps({
                    "success": False,
                    "error": "Observation note cannot be empty",
                    "story_id": story_id
                }))
            else:
                print("ERROR: Observation note cannot be empty")
            return 2

        ps = _get_phase_state(project_root)

        # Add observation
        observation_id = ps.add_observation(
            story_id=story_id,
            phase_id=phase,
            category=category,
            note=note,
            severity=severity
        )

        if observation_id is None:
            if format == "json":
                print(json.dumps({
                    "success": False,
                    "error": "State file not found",
                    "story_id": story_id
                }))
            else:
                print(f"State file not found for {story_id}")
            return 1

        if format == "json":
            print(json.dumps({
                "success": True,
                "story_id": story_id,
                "phase": phase,
                "category": category,
                "severity": severity,
                "observation_id": observation_id
            }))
        else:
            print(f"Recorded observation for {story_id} phase {phase}")
            print(f"  Category: {category}")
            print(f"  Severity: {severity}")
            print(f"  ID: {observation_id}")

        return 0

    except ValueError as e:
        if format == "json":
            print(json.dumps({
                "success": False,
                "error": str(e),
                "story_id": story_id
            }))
        else:
            print(f"ERROR: {e}")
        return 2

    except Exception as e:
        if format == "json":
            print(json.dumps({
                "success": False,
                "error": str(e),
                "story_id": story_id
            }))
        else:
            print(f"ERROR: {e}")
        return 2
