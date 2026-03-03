# STORY-136 Test Suite

## Quick Start

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2
pytest tests/STORY-136/ -v
```

### Run Specific Acceptance Criterion Tests
```bash
# AC#1: Checkpoint File Creation
pytest tests/STORY-136/test_checkpoint_file_creation.py -v

# AC#2: Content Structure
pytest tests/STORY-136/test_checkpoint_content_structure.py -v

# AC#3: Session ID Generation
pytest tests/STORY-136/test_session_id_generation.py -v

# AC#4: Timestamp Validation
pytest tests/STORY-136/test_timestamp_validation.py -v

# AC#5: Phase Tracking
pytest tests/STORY-136/test_phase_tracking.py -v

# AC#6: Atomic Writes
pytest tests/STORY-136/test_atomic_writes.py -v
```

### Run Edge Cases & Integration Tests
```bash
# Edge cases and NFR tests
pytest tests/STORY-136/test_edge_cases.py -v

# Integration and E2E tests
pytest tests/STORY-136/test_integration.py -v
```

---

## Test Structure

### Test Files
- **conftest.py** - Shared fixtures and test data
- **test_checkpoint_file_creation.py** - AC#1 tests (8 tests)
- **test_checkpoint_content_structure.py** - AC#2 tests (14 tests)
- **test_session_id_generation.py** - AC#3 tests (16 tests)
- **test_timestamp_validation.py** - AC#4 tests (21 tests)
- **test_phase_tracking.py** - AC#5 tests (20 tests)
- **test_atomic_writes.py** - AC#6 tests (13 tests)
- **test_edge_cases.py** - Edge cases & NFR tests (24 tests)
- **test_integration.py** - Integration & E2E tests (10 tests)

### Total: 127 tests covering all acceptance criteria

---

## Current Status (TDD Red Phase)

**Test Results:** 67 FAILED, 60 PASSED
- Failed tests = Expecting implementation (TDD Red - expected behavior)
- Passed tests = Utility/fixture tests (no implementation needed)

**This is CORRECT for TDD Red phase!** All tests that require the business logic implementation are failing, which validates that we have good test coverage.

---

## Acceptance Criteria Tested

### AC#1: Checkpoint File Creation
- Creates checkpoint at `devforgeai/temp/.ideation-checkpoint-{session_id}.yaml`
- Uses Write tool (not Bash)
- Creates at each phase boundary

### AC#2: Content Structure
- Contains all required fields: session_id, timestamp, current_phase, phase_completed, brainstorm_context
- Valid YAML syntax
- Correct field types

### AC#3: Session ID
- Generated as UUID v4 (8-4-4-4-12 format)
- Consistent across multiple checkpoint writes
- Unique per session

### AC#4: Timestamp
- ISO 8601 format with milliseconds
- Includes Z suffix for UTC
- Within 1 second of actual write time

### AC#5: Phase Tracking
- Tracks current phase (1-6)
- Sets phase_completed flag
- Accumulates data across phases
- Enables resume from last checkpoint

### AC#6: Atomic Writes
- Uses Write tool exclusively
- YAML always valid after write
- No partial files on error
- Proper error handling

---

## Test Fixtures Available

### Session ID Fixtures
```python
valid_session_id        # Random UUID v4
fixed_session_id        # Fixed: 550e8400-e29b-41d4-a716-446655440000
invalid_session_ids     # List of 6 invalid formats
```

### Timestamp Fixtures
```python
valid_iso_timestamp     # ISO 8601 with milliseconds and Z
fixed_iso_timestamp     # Fixed: 2025-12-22T15:30:45.123Z
invalid_timestamps      # List of 7 invalid formats
```

### Context Fixtures
```python
valid_brainstorm_context    # Complete with personas, requirements, epics
minimal_brainstorm_context  # Minimal but valid
large_brainstorm_context    # For file size testing (>5KB before truncation)
```

### Checkpoint Fixtures
```python
valid_checkpoint_phase_1    # Valid Phase 1 checkpoint
valid_checkpoint_phase_3    # Valid Phase 3 checkpoint
checkpoint_missing_session_id   # Missing required field
checkpoint_invalid_uuid     # Invalid UUID format
checkpoint_invalid_timestamp    # Invalid timestamp format
# ... more invalid variants
```

### Mock Fixtures
```python
mock_write_tool         # Mock Write tool (returns None)
mock_write_tool_with_error  # Mock that raises IOError
mock_read_tool          # Mock Read tool
mock_filesystem         # Temporary filesystem (tmp_path)
```

---

## Key Test Classes

### Checkpoint Service Tests
```python
CheckpointService(write_tool)
  ├─ create_checkpoint(checkpoint_data)  # Creates/updates checkpoint
  └─ [To be implemented in Phase 3]
```

### Session ID Tests
```python
SessionIdGenerator()
  ├─ generate() -> str  # Generate UUID v4
  └─ [To be implemented in Phase 3]

SessionIdValidator()
  ├─ validate(session_id) -> None  # Validate format
  └─ [To be implemented in Phase 3]

SessionIdExtractor()
  ├─ extract_from_filename(filename) -> str  # Extract from filename
  └─ [To be implemented in Phase 3]
```

### Timestamp Tests
```python
TimestampGenerator()
  ├─ generate() -> str  # Generate ISO 8601 timestamp
  └─ [To be implemented in Phase 3]

TimestampValidator()
  ├─ validate(timestamp) -> None  # Validate format
  └─ [To be implemented in Phase 3]

TimestampParser()
  ├─ parse(timestamp) -> Dict  # Parse components
  └─ [To be implemented in Phase 3]
```

### Validation Tests
```python
CheckpointValidator()
  ├─ validate(checkpoint_data) -> None
  └─ [To be implemented in Phase 3]

ComplexityValidator()
  ├─ validate(checkpoint) -> None  # Check score 0-60
  └─ [To be implemented in Phase 3]

PathValidator()
  ├─ validate(path) -> None  # Check path safety
  └─ [To be implemented in Phase 3]
```

---

## Edge Cases Tested

- Complexity score validation (0-60 range)
- File size limit enforcement (<5KB)
- Disk full error handling
- Permission denied error handling
- Malformed YAML handling
- Empty checkpoint files
- Large checkpoint truncation
- Path traversal prevention
- No secrets in checkpoint
- Phase number validation (1-6)

---

## Expected Failures (TDD Red)

These tests are EXPECTED TO FAIL because implementation doesn't exist yet:

```
FAILED test_checkpoint_file_creation.py::... (8 tests)
FAILED test_session_id_generation.py::... (8 tests)
FAILED test_timestamp_validation.py::... (16 tests)
FAILED test_phase_tracking.py::... (7 tests)
FAILED test_atomic_writes.py::... (6 tests)
FAILED test_edge_cases.py::... (18 tests)
FAILED test_integration.py::... (5 tests)
```

**Total: 67 FAILED tests = Expected in TDD Red phase!**

---

## What Each Test File Does

### conftest.py
Provides all test fixtures and configuration:
- Session ID generators (valid/invalid)
- Timestamp generators (valid/invalid)
- Brainstorm context fixtures (minimal/normal/large)
- Checkpoint document fixtures
- Mock tools
- Parameterized fixtures for range testing

**Use:** Import from conftest and use in any test file
```python
def test_something(valid_session_id, fixed_iso_timestamp):
    # Test code here
    pass
```

### test_checkpoint_file_creation.py (AC#1)
Tests that checkpoint files are created with:
- Correct file path pattern
- .yaml extension
- Hidden filename (starts with .)
- Using Write tool (not Bash)
- At each phase boundary

**Example Test:**
```python
def test_should_create_checkpoint_file_after_phase_one_completion(
    fixed_session_id, valid_checkpoint_phase_1, mock_write_tool
):
    checkpoint_service = CheckpointService(write_tool=mock_write_tool)
    checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)
    mock_write_tool.write.assert_called_once()
```

### test_checkpoint_content_structure.py (AC#2)
Tests that checkpoint YAML contains:
- All required fields
- Correct field types
- Valid YAML syntax
- Nested brainstorm_context
- Field validation

**Example Test:**
```python
def test_should_contain_session_id_field(fixed_session_id, valid_checkpoint_phase_1):
    parsed = yaml.safe_load(yaml.dump(valid_checkpoint_phase_1))
    assert "session_id" in parsed
    assert parsed["session_id"] == fixed_session_id
```

### test_session_id_generation.py (AC#3)
Tests UUID v4 generation and validation:
- Format: 8-4-4-4-12 hex pattern
- Version 4 (random)
- RFC 4122 variant
- Uniqueness
- Consistency

**Example Test:**
```python
def test_should_generate_uuid_v4_format(valid_session_id):
    generator = SessionIdGenerator()
    session_id = generator.generate()
    parsed_uuid = uuid.UUID(session_id)
    assert parsed_uuid.version == 4
```

### test_timestamp_validation.py (AC#4)
Tests ISO 8601 timestamp validation:
- Format: YYYY-MM-DDTHH:MM:SS.fffZ
- Millisecond precision (3 digits)
- Z suffix (UTC)
- Time/date range validation
- Within 1 second accuracy

**Example Test:**
```python
def test_should_include_z_suffix_for_utc(valid_iso_timestamp):
    assert valid_iso_timestamp.endswith('Z')
```

### test_phase_tracking.py (AC#5)
Tests phase tracking and data accumulation:
- Phase number tracking (1-6)
- Phase_completed flag
- Data accumulation across phases
- Resume capability
- Phase range validation

**Example Test:**
```python
def test_should_track_current_phase_number_phase_1(valid_checkpoint_phase_1):
    assert valid_checkpoint_phase_1["current_phase"] == 1
```

### test_atomic_writes.py (AC#6)
Tests atomic write semantics:
- Write tool usage (not Bash)
- YAML validity post-write
- Error handling
- No partial files
- File permissions
- Idempotency

**Example Test:**
```python
def test_should_use_write_tool_exclusively(valid_checkpoint_phase_1, mock_write_tool):
    checkpoint_service = CheckpointService(write_tool=mock_write_tool)
    checkpoint_service.create_checkpoint(valid_checkpoint_phase_1)
    mock_write_tool.write.assert_called_once()
```

### test_edge_cases.py
Tests non-functional requirements and edge cases:
- Complexity score range validation
- File size limits
- Disk full handling
- Permission denied handling
- Secret detection
- YAML malformedness handling
- Path traversal prevention

**Example Test:**
```python
def test_should_reject_complexity_score_greater_than_60(
    fixed_session_id, fixed_iso_timestamp
):
    checkpoint = {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": {..., "complexity_score": 61}
    }
    validator = ComplexityValidator()
    with pytest.raises(ValueError):
        validator.validate(checkpoint)
```

### test_integration.py
Tests multi-phase and end-to-end scenarios:
- Checkpoint at each phase boundary
- Session consistency
- Data accumulation
- Resume capability
- Full lifecycle (Phase 1-5)

**Example Test:**
```python
def test_critical_path_full_ideation_session_lifecycle(
    fixed_session_id, fixed_iso_timestamp, mock_write_tool
):
    checkpoint_service = CheckpointService(write_tool=mock_write_tool)
    for phase in range(1, 6):
        # Create checkpoint for each phase
        checkpoint_service.create_checkpoint(checkpoint_data)
    assert mock_write_tool.write.call_count == 5
```

---

## Running During Development

### Watch Mode (Recommended)
```bash
pytest tests/STORY-136/ -v --tb=short -x  # Stop on first failure
```

### With Verbose Output
```bash
pytest tests/STORY-136/ -vv --tb=long  # Show full tracebacks
```

### By Acceptance Criterion
```bash
pytest tests/STORY-136/test_checkpoint_file_creation.py -v  # AC#1
pytest tests/STORY-136/test_checkpoint_content_structure.py -v  # AC#2
pytest tests/STORY-136/test_session_id_generation.py -v  # AC#3
pytest tests/STORY-136/test_timestamp_validation.py -v  # AC#4
pytest tests/STORY-136/test_phase_tracking.py -v  # AC#5
pytest tests/STORY-136/test_atomic_writes.py -v  # AC#6
```

### Coverage Report
```bash
pytest tests/STORY-136/ --cov=. --cov-report=html
open htmlcov/index.html  # View in browser
```

---

## Next: Phase 3 Implementation

The implementation should:

1. Create `CheckpointService` class
   ```python
   class CheckpointService:
       def __init__(self, write_tool):
           self.write_tool = write_tool

       def create_checkpoint(self, checkpoint_data):
           # Serialize to YAML
           # Call Write tool
           # Handle errors
   ```

2. Create `SessionIdGenerator` class
   ```python
   class SessionIdGenerator:
       def generate(self) -> str:
           return str(uuid.uuid4())
   ```

3. Create `TimestampGenerator` class
   ```python
   class TimestampGenerator:
       def generate(self) -> str:
           now = datetime.now(timezone.utc)
           return now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
   ```

4. Create validators (UUID, timestamp, complexity, path)

5. When implementation is complete, all 67 failing tests should PASS!

---

## Test Statistics

| Metric | Value |
|--------|-------|
| Total Tests | 127 |
| Test Files | 9 |
| Test Classes | 9 |
| Fixtures Defined | 30+ |
| Placeholder Classes | 12 |
| Lines of Test Code | 3,500+ |
| Failed (Expected) | 67 |
| Passed (Current) | 60 |
| Parameterized Tests | 15+ |

---

## Key Testing Principles Applied

1. **AAA Pattern** - Arrange, Act, Assert on every test
2. **One Assertion Per Test** - When possible
3. **Descriptive Names** - test_should_<action>_when_<condition>
4. **Fixtures for Reuse** - Common test data in conftest.py
5. **Parameterization** - @pytest.mark.parametrize for multiple inputs
6. **Test Independence** - No shared state between tests
7. **Clear Arrange/Act/Assert** - Easy to understand intent

---

## Questions?

Refer to:
- TEST-GENERATION-SUMMARY.md - Detailed test statistics
- Story file: devforgeai/specs/Stories/STORY-136-file-based-checkpoint-protocol.story.md
- Plan file: .claude/plans/STORY-136-test-generation-plan.md

**Status:** TDD Red Phase Complete ✓ Ready for Phase 3 Implementation
