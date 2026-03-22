# QA Gaps: STORY-002

## Status: COVERAGE GAP REMAINING ⚠️

**Story:** Index Storage with SQLite Persistence
**Reviewed:** 2026-01-13
**Remaining:** schema.py coverage 71% (need 80%)

---

## Gap Status Summary

| Gap | Original Status | Current Status |
|-----|-----------------|----------------|
| Dependency Issue | Tests blocked | ✅ RESOLVED |
| schema.py Coverage | 47% reported | 71% actual (need 80%) |

---

## Remaining Gap: Schema Coverage (71% → 80%)

- **File:** `src/treelint/index/schema.py`
- **Current Coverage:** 71% (75 statements, 22 missed)
- **Required Coverage:** 80% (infrastructure layer threshold)
- **Gap:** 9 percentage points

### Untested Lines (from coverage report)
```
Missing: 110, 146-153, 168-192, 273-277, 281-283
```

These are migration-related code paths that are skipped because:
- Schema is at version 1 (no prior versions to migrate from)
- 7 tests are SKIPPED waiting for future schema versions

### Options to Close Gap

**Option A: Add tests for migration edge cases (~5-10 new tests)**
- Mock schema version to simulate upgrade scenarios
- Test migration rollback on failure
- Test corrupted version detection

**Option B: Accept current coverage with documented justification**
- 71% covers all currently exercised code paths
- Migration code is defensive for future versions
- Skipped tests will activate when migrations are needed

---

## Current Test Status

```
tests/unit/index/test_storage.py: 49 passed ✅
tests/unit/index/test_schema.py: 27 passed, 7 skipped ⚠️
Coverage: storage.py 92% ✅, schema.py 71% ⚠️
```

---

## Recommended Action

**Run `/dev STORY-002`** to add schema coverage tests:
1. Mock `get_schema_version()` to return old version
2. Test `migrate()` executes migration SQL
3. Test migration failure triggers rollback
4. Test `get_migration_sql()` returns valid SQL per version

This should add ~5-10 tests and bring coverage to ≥80%.

---

## Change Log

| Date | Action | By |
|------|--------|-----|
| 2026-01-13 | Status reverted to QA Failed | DevForgeAI Framework |
| 2026-01-13 | Dependency issue resolved | DevForgeAI Framework |
| 2026-01-13 | Coverage gap updated: 71% actual (not 47%) | DevForgeAI Framework |
