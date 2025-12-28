# STORY-136 Test Generation Plan

**Story ID:** STORY-136
**Title:** File-Based Checkpoint Protocol for Ideation Sessions
**Phase:** Phase 2 - Test-First Design (TDD Red)
**Objective:** Generate comprehensive failing tests from acceptance criteria and technical specification
**Test Framework:** pytest (per tech-stack.md)
**Test Location:** tests/STORY-136/ (per source-tree.md, line 340)

---

## Context Summary

**Story Requirements:**
- Checkpoint file creation at phase boundaries in YAML format
- Session ID generation (UUID v4)
- Timestamp tracking (ISO 8601)
- Phase tracking (1-6) with data accumulation
- Atomic writes using Write tool (not Bash)

**Acceptance Criteria to Test:**
1. AC#1: Checkpoint file creation at `devforgeai/temp/.ideation-checkpoint-{session_id}.yaml`
2. AC#2: Content structure with required fields (session_id, timestamp, current_phase, phase_completed, brainstorm_context)
3. AC#3: Session ID validation (UUID v4 format)
4. AC#4: Timestamp validation (ISO 8601 with milliseconds)
5. AC#5: Phase tracking across boundaries with data accumulation
6. AC#6: Atomic writes using Write tool with YAML validity

**Technical Specification Components:**
- CheckpointService: Manages checkpoint lifecycle (create, update, validate)
- CheckpointSchema: YAML schema definition with required fields
- SessionIdGenerator: UUID v4 generation
- Business Rules: BR-001 to BR-004 (Write tool usage, path pattern, session ID consistency, error handling)
- Non-Functional Requirements: NFR-001 to NFR-004 (Performance <100ms, file size <5KB, atomicity, no secrets)
- Edge Cases: Disk full, permissions, UUID collision, malformed YAML, file size limits

---

## Test Generation Strategy

### Test Pyramid Distribution
- **Unit Tests (70%):** 20 tests
  - CheckpointService methods (create, update, validate)
  - SessionIdGenerator (UUID format, uniqueness)
  - CheckpointSchema (field validation, YAML parsing)
  - Timestamp validation
  - Error handling and edge cases

- **Integration Tests (20%):** 6 tests
  - Multi-phase checkpoint flow
  - Data accumulation across phases
  - End-to-end checkpoint write and read

- **E2E Tests (10%):** 2 tests
  - Critical path: Full ideation session checkpoint lifecycle
  - Error recovery: Session continues after write failure

### Test File Organization
```
tests/STORY-136/
├── conftest.py                          # Shared fixtures and mocks
├── test_checkpoint_file_creation.py     # AC#1 tests
├── test_checkpoint_content_structure.py # AC#2 tests
├── test_session_id_generation.py        # AC#3 tests
├── test_timestamp_validation.py         # AC#4 tests
├── test_phase_tracking.py               # AC#5 tests
├── test_atomic_writes.py                # AC#6 tests
├── test_integration.py                  # Integration tests
├── test_edge_cases.py                   # Edge case scenarios
└── fixtures/
    ├── valid_checkpoint.yaml            # Valid checkpoint example
    ├── invalid_checkpoints/             # Invalid checkpoint examples
    │   ├── missing_fields.yaml
    │   ├── invalid_uuid.yaml
    │   └── invalid_timestamp.yaml
    └── large_checkpoint.yaml            # For file size tests
```

---

## Test Design - Key Patterns

### Pattern 1: Fixture-Based Checkpoint Data
Each test file includes fixtures that provide:
- Valid checkpoint data (with all required fields)
- Invalid checkpoint data (missing fields, wrong types)
- Empty/minimal checkpoint data
- Large checkpoint data (for size limits)

### Pattern 2: Mock Write Tool
Since we're testing in isolation (unit tests), mock the Write tool:
```python
@pytest.fixture
def mock_write_tool(mocker):
    """Mock the Write tool to capture checkpoint content"""
    return mocker.patch('checkpoint_service.write_tool')
```

### Pattern 3: AAA Pattern Consistently
All tests follow Arrange-Act-Assert:
```python
def test_should_<action>_when_<condition>():
    # Arrange: Set up test data

    # Act: Execute the behavior

    # Assert: Verify the outcome
```

### Pattern 4: Parameterized Tests
Use `@pytest.mark.parametrize` for:
- Multiple UUID formats (valid/invalid)
- Multiple timestamp formats (valid/invalid)
- Multiple phase numbers (1-6, out of range)
- Multiple complexity scores (0-60, out of range)

---

## Test Coverage Mapping

### AC#1: Checkpoint File Creation
- test_should_create_checkpoint_file_after_phase_one_completion()
- test_should_create_checkpoint_at_correct_path()
- test_should_create_checkpoint_using_write_tool()
- test_should_not_use_bash_for_checkpoint_creation()

### AC#2: Content Structure
- test_should_contain_session_id_field()
- test_should_contain_timestamp_field()
- test_should_contain_current_phase_field()
- test_should_contain_phase_completed_field()
- test_should_contain_brainstorm_context_object()
- test_should_validate_yaml_syntax()
- test_should_parse_with_pyyaml()

### AC#3: Session ID Format
- test_should_generate_uuid_v4_session_id()
- test_should_validate_uuid_format_8_4_4_4_12()
- test_should_reject_invalid_uuid_formats()
- test_should_maintain_session_id_consistency_across_writes()

### AC#4: Timestamp Format
- test_should_record_iso_8601_timestamp()
- test_should_include_millisecond_precision()
- test_should_include_z_suffix_for_utc()
- test_should_validate_timestamp_within_one_second()

### AC#5: Phase Tracking
- test_should_track_current_phase_number()
- test_should_set_phase_completed_true()
- test_should_accumulate_data_across_phases()
- test_should_preserve_previous_phase_data()

### AC#6: Atomic Writes
- test_should_use_write_tool_exclusively()
- test_should_produce_valid_yaml_after_write()
- test_should_handle_write_tool_errors()
- test_should_not_create_partial_files_on_error()

### Edge Cases (NFR/Data Validation)
- test_should_validate_complexity_score_range_0_to_60()
- test_should_accept_empty_personas_array()
- test_should_accept_empty_requirements_array()
- test_should_reject_file_paths_with_parent_directory_traversal()
- test_should_handle_disk_full_error()
- test_should_handle_permission_denied_error()
- test_should_truncate_if_file_exceeds_5kb_limit()
- test_should_contain_no_secrets_in_checkpoint()

### Integration Tests
- test_should_create_checkpoint_at_each_phase_boundary()
- test_should_maintain_session_consistency_across_five_phases()
- test_should_resume_from_checkpoint_with_accumulated_data()

---

## Implementation Checklist

### Phase 1: Test File Creation
- [ ] Create conftest.py with shared fixtures
- [ ] Create test_checkpoint_file_creation.py (AC#1)
- [ ] Create test_checkpoint_content_structure.py (AC#2)
- [ ] Create test_session_id_generation.py (AC#3)
- [ ] Create test_timestamp_validation.py (AC#4)
- [ ] Create test_phase_tracking.py (AC#5)
- [ ] Create test_atomic_writes.py (AC#6)
- [ ] Create test_edge_cases.py (edge cases/NFR)
- [ ] Create test_integration.py (integration tests)

### Phase 2: Fixture Setup
- [ ] Create valid_checkpoint.yaml fixture
- [ ] Create invalid checkpoint YAML files
- [ ] Create large checkpoint YAML for size tests
- [ ] Create conftest.py pytest fixtures

### Phase 3: Verification
- [ ] Run pytest to confirm all tests fail (TDD Red)
- [ ] Verify test count matches target (28 tests)
- [ ] Verify no tests pass before implementation
- [ ] Generate test execution report

---

## Success Criteria for Test Generation

- [ ] All tests FAIL initially (TDD Red phase - no implementation exists)
- [ ] 28+ total tests generated (20 unit, 6 integration, 2 E2E)
- [ ] All tests follow naming convention: test_should_<action>_when_<condition>
- [ ] All tests follow AAA pattern (Arrange, Act, Assert)
- [ ] All acceptance criteria have corresponding tests
- [ ] All technical specification components tested
- [ ] All edge cases covered
- [ ] All tests are independent (no shared state)
- [ ] Fixtures provided for test data
- [ ] Tests can be run with: `pytest tests/STORY-136/`
- [ ] Coverage report generated showing test readiness

---

## Command to Run Tests

```bash
# Run all STORY-136 tests
pytest tests/STORY-136/ -v --tb=short

# Run with coverage
pytest tests/STORY-136/ --cov=checkpoint_service --cov-report=html

# Run specific test file
pytest tests/STORY-136/test_checkpoint_file_creation.py -v
```

---

## Technical Constraints

**From tech-stack.md:**
- Framework implementation uses Claude Code Terminal
- File operations use native tools (Read, Write, Glob, Grep) NOT Bash
- All framework components are documentation (Markdown with YAML frontmatter)

**From source-tree.md:**
- Test files located in: tests/ directory
- Framework test files follow pytest pattern

---

## Progress Tracking

**Status:** In Progress
**Start Time:** [TBD]
**Target Completion:** [TBD]

### Phases
1. **Phase 1: Test File Creation** - [Pending]
2. **Phase 2: Fixture Setup** - [Pending]
3. **Phase 3: Verification** - [Pending]
4. **Phase 4: Implementation Preparation** - [Pending]

---

## Next Steps

1. Create conftest.py with shared fixtures
2. Generate unit tests for each AC (6 test files)
3. Generate integration and edge case tests
4. Create YAML fixture files
5. Run pytest to verify all tests FAIL
6. Package test files for delivery to devforgeai-development skill

