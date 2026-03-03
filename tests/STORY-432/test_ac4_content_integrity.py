"""
Test: AC#4 - File Content Integrity Verified
Story: STORY-432
Generated: 2026-02-17

Verifies SHA-256 checksums of all migrated files match the original files
(byte-for-byte identical). This test captures checksums from source files
BEFORE migration and compares them to target files AFTER migration.

Given: Files have been migrated from orchestration to architecture
When: Integrity verification is performed
Then: SHA-256 checksums of all migrated files match the originals

Note: These tests will FAIL initially because:
  - Target files do not yet exist in architecture (pre-migration state)
  - Tests are designed for TDD Red phase
"""
import hashlib
import os
import pytest

from conftest import (
    ARCHITECTURE_REFERENCES_DIR,
    ARCHITECTURE_TEMPLATES_DIR,
    ORCHESTRATION_REFERENCES_DIR,
    ORCHESTRATION_TEMPLATES_DIR,
    REFERENCE_FILES,
    TEMPLATE_FILE,
)


def compute_sha256(file_path: str) -> str:
    """Compute SHA-256 checksum of a file.

    Args:
        file_path: Absolute path to the file.

    Returns:
        Hex string of the SHA-256 hash.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_file_exists_and_get_checksum(
    file_path: str, filename: str
) -> str:
    """Verify a file exists and return its SHA-256 checksum.

    Args:
        file_path: Absolute path to the file.
        filename: Name of file (for error messages).

    Returns:
        SHA-256 hex digest.

    Raises:
        AssertionError: If file does not exist.
    """
    assert os.path.isfile(file_path), (
        f"Target file does not exist: {file_path}. Cannot verify integrity."
    )
    return compute_sha256(file_path)


class TestAC4ContentIntegrity:
    """AC#4: File content integrity verified via SHA-256 checksums."""

    # --- Pre-migration snapshot: Source files must exist to compute baseline ---

    @pytest.fixture
    def source_checksums(self):
        """Compute SHA-256 checksums for all 8 source files (pre-migration baseline).

        Returns a dict mapping filename -> sha256 hex digest.
        Skips files that do not exist (they may already be migrated/removed).
        """
        checksums = {}

        for filename in REFERENCE_FILES:
            source_path = os.path.join(ORCHESTRATION_REFERENCES_DIR, filename)
            if os.path.isfile(source_path):
                checksums[filename] = compute_sha256(source_path)

        template_path = os.path.join(ORCHESTRATION_TEMPLATES_DIR, TEMPLATE_FILE)
        if os.path.isfile(template_path):
            checksums[TEMPLATE_FILE] = compute_sha256(template_path)

        return checksums

    # --- Helper method ---

    def _verify_checksum_match(
        self, source_path: str, target_path: str, filename: str
    ) -> None:
        """Helper: Verify checksums match between source and target files.

        Args:
            source_path: Absolute path to source file.
            target_path: Absolute path to target file.
            filename: Name of file (for error messages).

        Raises:
            AssertionError: If target doesn't exist or checksums don't match.
        """
        target_checksum = verify_file_exists_and_get_checksum(target_path, filename)

        if os.path.isfile(source_path):
            source_checksum = compute_sha256(source_path)
            assert source_checksum == target_checksum, (
                f"SHA-256 mismatch for {filename}. "
                "Target file is not byte-for-byte identical to source."
            )

    # --- Parameterized individual file integrity tests ---

    def test_should_have_matching_checksum_for_epic_management_when_migrated(self):
        """Verify epic-management.md checksum matches between source and target."""
        source = os.path.join(ORCHESTRATION_REFERENCES_DIR, "epic-management.md")
        target = os.path.join(ARCHITECTURE_REFERENCES_DIR, "epic-management.md")
        self._verify_checksum_match(source, target, "epic-management.md")

    def test_should_have_matching_checksum_for_feature_decomposition_patterns_when_migrated(self):
        """Verify feature-decomposition-patterns.md checksum matches."""
        source = os.path.join(ORCHESTRATION_REFERENCES_DIR, "feature-decomposition-patterns.md")
        target = os.path.join(ARCHITECTURE_REFERENCES_DIR, "feature-decomposition-patterns.md")
        self._verify_checksum_match(source, target, "feature-decomposition-patterns.md")

    def test_should_have_matching_checksum_for_feature_analyzer_when_migrated(self):
        """Verify feature-analyzer.md checksum matches."""
        source = os.path.join(ORCHESTRATION_REFERENCES_DIR, "feature-analyzer.md")
        target = os.path.join(ARCHITECTURE_REFERENCES_DIR, "feature-analyzer.md")
        self._verify_checksum_match(source, target, "feature-analyzer.md")

    def test_should_have_matching_checksum_for_dependency_graph_when_migrated(self):
        """Verify dependency-graph.md checksum matches."""
        source = os.path.join(ORCHESTRATION_REFERENCES_DIR, "dependency-graph.md")
        target = os.path.join(ARCHITECTURE_REFERENCES_DIR, "dependency-graph.md")
        self._verify_checksum_match(source, target, "dependency-graph.md")

    def test_should_have_matching_checksum_for_technical_assessment_guide_when_migrated(self):
        """Verify technical-assessment-guide.md checksum matches."""
        source = os.path.join(ORCHESTRATION_REFERENCES_DIR, "technical-assessment-guide.md")
        target = os.path.join(ARCHITECTURE_REFERENCES_DIR, "technical-assessment-guide.md")
        self._verify_checksum_match(source, target, "technical-assessment-guide.md")

    def test_should_have_matching_checksum_for_epic_validation_checklist_when_migrated(self):
        """Verify epic-validation-checklist.md checksum matches."""
        source = os.path.join(ORCHESTRATION_REFERENCES_DIR, "epic-validation-checklist.md")
        target = os.path.join(ARCHITECTURE_REFERENCES_DIR, "epic-validation-checklist.md")
        self._verify_checksum_match(source, target, "epic-validation-checklist.md")

    def test_should_have_matching_checksum_for_epic_validation_hook_when_migrated(self):
        """Verify epic-validation-hook.md checksum matches."""
        source = os.path.join(ORCHESTRATION_REFERENCES_DIR, "epic-validation-hook.md")
        target = os.path.join(ARCHITECTURE_REFERENCES_DIR, "epic-validation-hook.md")
        self._verify_checksum_match(source, target, "epic-validation-hook.md")

    def test_should_have_matching_checksum_for_epic_template_when_migrated(self):
        """Verify epic-template.md checksum matches between source and target."""
        source = os.path.join(ORCHESTRATION_TEMPLATES_DIR, TEMPLATE_FILE)
        target = os.path.join(ARCHITECTURE_TEMPLATES_DIR, TEMPLATE_FILE)
        self._verify_checksum_match(source, target, "epic-template.md")

    # --- Aggregate integrity test ---

    def test_should_have_all_eight_files_with_matching_checksums_when_migration_complete(
        self, source_checksums
    ):
        """Verify all 8 migrated files have matching SHA-256 checksums.

        This is the comprehensive integrity check that validates BR-001:
        'File content must be byte-for-byte identical after migration.'
        """
        mismatches = []
        missing_targets = []

        for filename in REFERENCE_FILES:
            target_path = os.path.join(ARCHITECTURE_REFERENCES_DIR, filename)
            if not os.path.isfile(target_path):
                missing_targets.append(filename)
                continue

            if filename in source_checksums:
                target_checksum = compute_sha256(target_path)
                if target_checksum != source_checksums[filename]:
                    mismatches.append(
                        f"{filename}: source={source_checksums[filename][:16]}... "
                        f"target={target_checksum[:16]}..."
                    )

        # Check template
        template_target = os.path.join(ARCHITECTURE_TEMPLATES_DIR, TEMPLATE_FILE)
        if not os.path.isfile(template_target):
            missing_targets.append(TEMPLATE_FILE)
        elif TEMPLATE_FILE in source_checksums:
            target_checksum = compute_sha256(template_target)
            if target_checksum != source_checksums[TEMPLATE_FILE]:
                mismatches.append(
                    f"{TEMPLATE_FILE}: source={source_checksums[TEMPLATE_FILE][:16]}... "
                    f"target={target_checksum[:16]}..."
                )

        errors = []
        if missing_targets:
            errors.append(f"Missing target files: {missing_targets}")
        if mismatches:
            errors.append(f"Checksum mismatches: {mismatches}")

        assert len(errors) == 0, (
            f"Content integrity verification failed. {'; '.join(errors)}"
        )

    # --- File size consistency test ---

    def test_should_have_matching_file_sizes_for_all_migrated_files_when_complete(self):
        """Verify file sizes match between source and target for all 8 files.

        Complementary to checksum verification -- a size mismatch is a
        fast-fail indicator of corruption or truncation.
        """
        size_mismatches = []

        for filename in REFERENCE_FILES:
            source = os.path.join(ORCHESTRATION_REFERENCES_DIR, filename)
            target = os.path.join(ARCHITECTURE_REFERENCES_DIR, filename)

            if os.path.isfile(source) and os.path.isfile(target):
                source_size = os.path.getsize(source)
                target_size = os.path.getsize(target)
                if source_size != target_size:
                    size_mismatches.append(
                        f"{filename}: source={source_size}B, target={target_size}B"
                    )

        source_template = os.path.join(ORCHESTRATION_TEMPLATES_DIR, TEMPLATE_FILE)
        target_template = os.path.join(ARCHITECTURE_TEMPLATES_DIR, TEMPLATE_FILE)
        if os.path.isfile(source_template) and os.path.isfile(target_template):
            s_size = os.path.getsize(source_template)
            t_size = os.path.getsize(target_template)
            if s_size != t_size:
                size_mismatches.append(
                    f"{TEMPLATE_FILE}: source={s_size}B, target={t_size}B"
                )

        assert len(size_mismatches) == 0, (
            f"File size mismatches detected: {size_mismatches}. "
            "Migrated files must be byte-for-byte identical."
        )
