# Test Integrity Snapshot Reference

**Purpose:** Create SHA-256 checksums of all test files at Phase 02 (RED) completion to detect unauthorized test modifications during later phases.

**Story:** STORY-502

---

## File Discovery Patterns

Discover test files using framework-specific glob patterns:

### Test File Patterns

| Framework | Glob Patterns |
|-----------|--------------|
| pytest | `**/test_*.py`, `**/*_test.py` |
| Jest | `**/*.test.js`, `**/*.test.ts`, `**/*.test.tsx`, `**/__tests__/**/*.js`, `**/__tests__/**/*.ts` |
| Vitest | `**/*.test.js`, `**/*.test.ts`, `**/*.test.tsx` |
| xUnit | `**/*Tests.cs`, `**/*Test.cs` |
| Shell | `**/test_*.sh`, `**/*_test.sh` |

### Configuration File Patterns

| Type | Glob Patterns |
|------|--------------|
| pytest config | `setup.cfg`, `pytest.ini`, `pyproject.toml` |
| Jest config | `jest.config.*` |
| Vitest config | `vitest.config.*` |

### Fixture and Mock File Patterns

| Type | Glob Patterns |
|------|--------------|
| Fixtures | `**/fixtures/**` |
| Mocks | `**/mocks/**`, `**/__mocks__/**` |
| Conftest | `**/conftest.py` |

---

## Snapshot Creation Algorithm

Execute the following steps to create a test integrity snapshot:

1. **Discover test files** using glob patterns from the table above, scoped to `tests/{STORY_ID}/` directory.

2. **Validate paths**: Reject any file path containing `..` (path traversal). Log WARNING and exclude.

3. **Compute SHA-256** for each discovered file:
   ```
   FOR each test_file in discovered_files:
     IF file is unreadable:
       Log WARNING: "Unreadable file excluded: {path}"
       SKIP file
     hash = hashlib.sha256(file_contents_bytes).hexdigest()
     # Result: 64 lowercase hex characters
   ```

4. **Write JSON snapshot** to `devforgeai/qa/snapshots/{STORY_ID}/red-phase-checksums.json`:
   ```json
   {
     "story_id": "STORY-NNN",
     "timestamp": "2026-02-27T14:30:00Z",
     "snapshot_type": "red-phase",
     "files": [
       {
         "path": "tests/STORY-NNN/test_ac1.sh",
         "sha256": "a1b2c3d4e5f6...64 lowercase hex characters",
         "size_bytes": 1234
       }
     ]
   }
   ```

### JSON Schema Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `story_id` | string | Story identifier in STORY-NNN format |
| `timestamp` | string | ISO-8601 formatted creation time |
| `snapshot_type` | string | Always `"red-phase"` for Phase 02 snapshots |
| `"files"` array | array | List of file entry objects |
| `"path"` (relative) | string | File path relative to project root |
| `sha256` | string | SHA-256 hash as 64 lowercase hex characters |
| `size_bytes` | integer | File size in bytes, integer >= 0 (non-negative) |

### Error Handling

- **Unreadable files**: Log WARNING, exclude from snapshot, continue processing remaining files.
- **Path traversal (`..`)**: Reject file, log WARNING, do not include in snapshot.
- **Empty directory**: Write snapshot with empty `"files"` array (valid state).

### Idempotency

Unchanged files produce identical SHA-256 hashes. Re-running the snapshot on the same unchanged files yields the same checksums.

### Overwrite Behavior (BR-005)

If `red-phase-checksums.json` already exists, overwrite it on re-execution. This supports re-running Phase 02 without manual cleanup.

---

## Phase 02 Integration

At the Phase 02 exit gate, after tests are verified in RED state:

1. Load this reference:
   ```
   Read(file_path="references/test-integrity-snapshot.md")
   ```

2. Execute the Snapshot Creation Algorithm above.

3. Verify the snapshot file was written successfully.

4. Proceed to Phase 03 (Green) with snapshot in place.

**Integration point:** The snapshot is consumed by the QA skill's diff-regression-detection phase to verify test integrity before QA approval.
