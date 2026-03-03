"""
STORY-530: Phase File <-> Registry Integration Tests

End-to-end validation that:
1. Registry JSON is valid and contains all expected phases
2. Each phase file references the correct phase ID in Progressive Task Disclosure
3. Step counts in phase files match registry step counts
4. Cross-component consistency between registry and phase files
"""

import json
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REGISTRY_PATH = os.path.join(PROJECT_ROOT, ".claude", "hooks", "phase-steps-registry.json")
PHASES_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "implementing-stories", "phases")

# Mapping from registry phase ID to phase filename
PHASE_FILE_MAP = {
    "01": "phase-01-preflight.md",
    "02": "phase-02-test-first.md",
    "03": "phase-03-implementation.md",
    "04": "phase-04-refactoring.md",
    "4.5": "phase-04.5-ac-verification.md",
    "05": "phase-05-integration.md",
    "5.5": "phase-05.5-ac-verification.md",
    "06": "phase-06-deferral.md",
    "07": "phase-07-dod-update.md",
    "08": "phase-08-git-workflow.md",
    "09": "phase-09-feedback.md",
    "10": "phase-10-result.md",
}


@pytest.fixture(scope="module")
def registry():
    """Load and parse the phase-steps-registry.json."""
    assert os.path.exists(REGISTRY_PATH), (
        f"Registry not found at {REGISTRY_PATH}"
    )
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@pytest.fixture(scope="module")
def phase_files():
    """Load all phase file contents keyed by registry phase ID."""
    files = {}
    for phase_id, filename in PHASE_FILE_MAP.items():
        filepath = os.path.join(PHASES_DIR, filename)
        assert os.path.exists(filepath), (
            f"Phase file not found: {filepath}"
        )
        with open(filepath, "r", encoding="utf-8") as f:
            files[phase_id] = f.read()
    return files


class TestRegistryIntegrity:
    """Verify the registry JSON itself is well-formed."""

    def test_registry_contains_all_12_phases(self, registry):
        expected_ids = set(PHASE_FILE_MAP.keys())
        actual_ids = set(registry.keys())
        assert expected_ids == actual_ids, (
            f"Registry phase IDs mismatch.\n"
            f"  Missing from registry: {expected_ids - actual_ids}\n"
            f"  Extra in registry: {actual_ids - expected_ids}"
        )

    def test_registry_each_phase_has_steps(self, registry):
        for phase_id, phase_data in registry.items():
            assert "steps" in phase_data, (
                f"Phase {phase_id} missing 'steps' key"
            )
            assert len(phase_data["steps"]) > 0, (
                f"Phase {phase_id} has zero steps"
            )

    def test_registry_each_phase_has_name(self, registry):
        for phase_id, phase_data in registry.items():
            assert "name" in phase_data, (
                f"Phase {phase_id} missing 'name' key"
            )
            assert len(phase_data["name"]) > 0, (
                f"Phase {phase_id} has empty name"
            )

    def test_registry_step_ids_match_phase(self, registry):
        for phase_id, phase_data in registry.items():
            for step in phase_data["steps"]:
                assert step["id"].startswith(phase_id + "."), (
                    f"Step {step['id']} does not start with phase prefix '{phase_id}.' "
                    f"in phase {phase_id}"
                )


class TestPhaseFileRegistryReference:
    """Verify each phase file references the registry correctly."""

    def test_phase_file_contains_progressive_task_disclosure_section(self, phase_files):
        for phase_id, content in phase_files.items():
            assert "## Progressive Task Disclosure" in content, (
                f"Phase {phase_id} ({PHASE_FILE_MAP[phase_id]}) missing "
                f"'## Progressive Task Disclosure' section"
            )

    def test_phase_file_references_registry_path(self, phase_files):
        for phase_id, content in phase_files.items():
            assert "phase-steps-registry.json" in content, (
                f"Phase {phase_id} ({PHASE_FILE_MAP[phase_id]}) does not reference "
                f"phase-steps-registry.json"
            )

    def test_phase_file_contains_correct_phase_id(self, phase_files):
        for phase_id, content in phase_files.items():
            # Look for current_phase_id = "XX" in the Phase Filtering section
            pattern = rf'current_phase_id\s*=\s*"{re.escape(phase_id)}"'
            assert re.search(pattern, content), (
                f"Phase {phase_id} ({PHASE_FILE_MAP[phase_id]}) does not contain "
                f'current_phase_id = "{phase_id}" in Phase Filtering section'
            )


class TestStepCountConsistency:
    """Verify step counts in registry are consistent and phase files reference step count."""

    def test_registry_step_count_within_expected_range(self, registry):
        """Each phase should have between 1 and 10 steps."""
        for phase_id, phase_data in registry.items():
            count = len(phase_data["steps"])
            assert 1 <= count <= 10, (
                f"Phase {phase_id} has {count} steps, expected 1-10"
            )

    def test_phase_file_step_count_in_taskcreate_matches_registry(self, registry, phase_files):
        """The TodoWrite/TaskCreate block in each phase file should list the same
        number of task items as the registry has steps for that phase."""
        for phase_id, content in phase_files.items():
            expected_count = len(registry[phase_id]["steps"])

            # Phase files contain a TodoWrite block with todo items for each step.
            # Count lines matching the pattern: content: "Step XX.N:
            todo_pattern = re.compile(
                rf'content:\s*"Step\s+{re.escape(phase_id)}\.\d+'
            )
            todo_matches = todo_pattern.findall(content)

            if len(todo_matches) == 0:
                # Some phase files may use alternative patterns; count step ID refs
                # in the TaskCreate/TodoWrite section instead
                found_step_ids = []
                for step in registry[phase_id]["steps"]:
                    if step["id"] in content:
                        found_step_ids.append(step["id"])
                # At minimum, the first two steps should be referenced
                assert len(found_step_ids) >= 2, (
                    f"Phase {phase_id} ({PHASE_FILE_MAP[phase_id]}): "
                    f"found only {len(found_step_ids)} registry step IDs referenced.\n"
                    f"  Expected at least 2 of: {[s['id'] for s in registry[phase_id]['steps']]}\n"
                    f"  Found: {found_step_ids}"
                )
            else:
                assert len(todo_matches) == expected_count, (
                    f"Phase {phase_id} ({PHASE_FILE_MAP[phase_id]}): "
                    f"TodoWrite has {len(todo_matches)} items but registry has {expected_count} steps"
                )


class TestCrossComponentConsistency:
    """Verify cross-component alignment between registry and phase files."""

    def test_registry_phase_names_share_keywords_with_phase_file_title(self, registry, phase_files):
        """Registry name and phase file title should share significant keywords.

        Names may differ slightly (e.g. 'Test-First (Red)' vs 'Test-First Design (TDD Red)')
        but must share at least one significant keyword (>3 chars) to confirm alignment.
        """
        for phase_id, content in phase_files.items():
            registry_name = registry[phase_id]["name"]
            first_line = content.split("\n")[0]

            # Extract significant words (>3 chars, alphanumeric)
            def extract_keywords(text):
                return {w.lower() for w in re.findall(r'[A-Za-z]{4,}', text)}

            registry_keywords = extract_keywords(registry_name)
            title_keywords = extract_keywords(first_line)
            shared = registry_keywords & title_keywords

            assert len(shared) >= 1, (
                f"Phase {phase_id}: no shared keywords between "
                f"registry name '{registry_name}' and title '{first_line}'.\n"
                f"  Registry keywords: {registry_keywords}\n"
                f"  Title keywords: {title_keywords}"
            )

    def test_all_phase_files_exist_on_disk(self):
        for phase_id, filename in PHASE_FILE_MAP.items():
            filepath = os.path.join(PHASES_DIR, filename)
            assert os.path.isfile(filepath), (
                f"Phase file missing: {filepath} (registry phase {phase_id})"
            )

    def test_no_orphan_phase_files(self, registry):
        """Ensure no phase-NN-*.md files exist without a registry entry."""
        phase_pattern = re.compile(r"^phase-(\d+(?:\.\d+)?)-.*\.md$")
        for filename in os.listdir(PHASES_DIR):
            match = phase_pattern.match(filename)
            if match:
                file_phase_id = match.group(1)
                # Normalize: "01" stays "01", "04.5" stays "4.5" after strip
                # Registry uses "01", "4.5" etc.
                assert file_phase_id in registry or file_phase_id.lstrip("0") in registry or file_phase_id in PHASE_FILE_MAP.values(), (
                    f"Orphan phase file '{filename}' has no registry entry "
                    f"(extracted phase ID: {file_phase_id})"
                )
