# STORY-001: Quick Start Guide for Developers

**For developers who need to implement STORY-001 quickly.**

## 5-Minute Overview

**What**: Create a stored procedure to discover fragmented indexes across SQL Server databases
**Where**: DBAdmin database
**Name**: `usp_DiscoverIndexFragmentation`
**Effort**: 44 hours (1 week)
**Impact**: Eliminates manual index discovery for 200+ instances

## Key Requirements (TL;DR)

1. **Scan databases** for fragmented indexes
2. **Query DMVs**: `sys.dm_db_index_physical_stats` in LIMITED mode
3. **Apply configuration**: Hierarchical overrides (index > table > database > server)
4. **Insert queue items**: Into MaintenanceQueue with priority based on fragmentation %
5. **Handle errors**: Continue on database offline/permission denied
6. **Log results**: Discovery metrics per database

## Critical Parameters

```sql
EXEC usp_DiscoverIndexFragmentation
    @DatabaseName = NULL,              -- NULL = all databases
    @MinFragmentationReorg = 15.0,     -- Fragmentation % for REORG
    @MinFragmentationRebuild = 30.0,   -- Fragmentation % for REBUILD
    @MinPageCount = 1000,              -- Skip small indexes
    @DryRun = 0;                       -- 1 = preview, 0 = insert
```

## Priority Calculation (Simple Formula)

```
IF Fragmentation >= 80%  → Priority = 1    (Critical)
ELSE IF >= 50%           → Priority = 5    (High)
ELSE IF >= 30%           → Priority = 15   (Medium)
ELSE IF >= 15%           → Priority = 30   (Normal)
ELSE                     → Skip (< 15%)

Within same band: Priority += (PageCount / 100000) for tie-breaking
```

## Acceptance Criteria Checklist

**Must Pass These 8 Scenarios**:
- [ ] AC-1: Basic discovery with default thresholds
- [ ] AC-2: Custom fragmentation thresholds
- [ ] AC-3: Single database scan
- [ ] AC-4: Configuration override resolution
- [ ] AC-5: Dry-run mode (no inserts)
- [ ] AC-6: Skip heaps and system objects
- [ ] AC-7: Logging and metrics
- [ ] AC-8: Priority assignment by fragmentation band

**Must Handle These 10 Edge Cases**:
- [ ] EC-1: Database offline during scan
- [ ] EC-2: Permission denied on DMV
- [ ] EC-3: Timeout on very large database (300s)
- [ ] EC-4: No indexes meet fragmentation threshold
- [ ] EC-5: Duplicate prevention (UNIQUE constraint)
- [ ] EC-6: Zero items from configuration override
- [ ] EC-7: SQL injection attempt (QUOTENAME escaping)
- [ ] EC-8: Cursor with 1000+ databases
- [ ] EC-9: Invalid fragmentation parameters
- [ ] EC-10: Invalid @MinPageCount parameter

## Code Structure (Step-by-Step)

### Step 1: Parameter Validation (3 hours)

```sql
-- Check that REBUILD threshold >= REORG threshold
IF @MinFragmentationRebuild < @MinFragmentationReorg
    RAISERROR('REBUILD threshold must be >= REORG threshold', 16, 1);

-- Validate ranges (0-100)
IF @MinFragmentationReorg < 0 OR @MinFragmentationReorg > 100
    RAISERROR('@MinFragmentationReorg must be 0-100', 16, 1);
```

### Step 2: Database Discovery (2 hours)

```sql
-- Get list of online, non-read-only databases
SELECT DatabaseName, DatabaseID
FROM sys.databases
WHERE state_desc = 'ONLINE'
AND is_read_only = 0
AND (@DatabaseName IS NULL OR name = @DatabaseName)
AND (@ExcludeSystemDatabases = 0 OR database_id > 4);
```

### Step 3: Dynamic SQL for Each Database (6 hours)

```sql
-- Use QUOTENAME to prevent SQL injection
USE [' + QUOTENAME(@DatabaseName) + '];

-- Query fragmentation with LIMITED mode (fast)
SELECT ... FROM sys.dm_db_index_physical_stats(..., 'LIMITED')
WHERE index_name IS NOT NULL                    -- Skip heaps
AND page_count >= @MinPageCount                 -- Skip small indexes
AND avg_fragmentation_in_percent >= @Threshold;
```

### Step 4: Priority Calculation (2 hours)

```sql
CASE
    WHEN Fragmentation >= 80 THEN 1
    WHEN Fragmentation >= 50 THEN 5
    WHEN Fragmentation >= 30 THEN 15
    WHEN Fragmentation >= 15 THEN 30
    ELSE 99
END + (PageCount / 100000.0)
```

### Step 5: Queue Insertion (3 hours)

```sql
INSERT INTO MaintenanceQueue
(DatabaseName, SchemaName, TableName, IndexName, OperationType, Priority, Status, CreatedDate, OperationDetails)
SELECT ...
WHERE avg_fragmentation_in_percent >= @MinFragmentationReorg;
```

### Step 6: Error Handling (4 hours)

```sql
BEGIN TRY
    -- Scan database
FETCH NEXT FROM db_cursor ...
END TRY
BEGIN CATCH
    -- Log error, continue with next database
    IF ERROR_NUMBER() = 916 -- Permission denied
        PRINT 'Skipped: Permission denied';
END CATCH
```

### Step 7: Logging (2 hours)

```sql
-- Log to MaintenanceLog
INSERT INTO MaintenanceLog
(DatabaseName, MaintenanceType, Status, StartTime, EndTime)
VALUES (@CurrentDB, 'INDEX_DISCOVERY', 'SUCCESS', @Start, GETDATE());
```

## Testing Checklist

**Unit Tests** (Can run independently):
```sql
-- Test 1: Parameter validation rejects inverted thresholds
-- Test 2: Priority calculation produces correct bands
-- Test 3: Heap exclusion (IndexName IS NOT NULL)
-- Test 4: SQL injection prevention (QUOTENAME)
```

**Integration Tests** (End-to-end):
```sql
-- Test 1: Discover fragmented indexes in test database
-- Test 2: Verify MaintenanceQueue population
-- Test 3: Dry-run mode doesn't insert rows
-- Test 4: Configuration overrides applied
```

**Edge Case Tests**:
```sql
-- Test 1: Offline database handled gracefully
-- Test 2: Duplicate queue items skipped
-- Test 3: 1000+ database environment
```

## Performance Targets

- **Scan 200+ databases**: < 10 minutes
- **Per-database scan**: < 50ms
- **Memory usage**: < 100MB
- **Cursor overhead**: Minimal (FAST_FORWARD)

## Security Checklist

- [x] Use QUOTENAME() for all database names
- [x] Use sp_executesql with parameters (no string concatenation)
- [x] Validate all parameters (type, range, NULL)
- [x] No credentials in logs or error messages
- [x] Requires VIEW SERVER STATE permission
- [x] Only modifies DBAdmin tables (not user databases)

## Common Mistakes to Avoid

❌ **WRONG**: `USE [` + @DatabaseName + `];`
✅ **RIGHT**: `USE [` + QUOTENAME(@DatabaseName) + `];`

❌ **WRONG**: `WHERE page_count < 1000` (loses large indexes)
✅ **RIGHT**: `WHERE page_count >= @MinPageCount`

❌ **WRONG**: `DECLARE db_cursor CURSOR FOR ...` (memory intensive)
✅ **RIGHT**: `DECLARE db_cursor CURSOR LOCAL FAST_FORWARD FOR ...`

❌ **WRONG**: SELECT * FROM very large table
✅ **RIGHT**: Use DRY-RUN mode for preview, limit result columns

❌ **WRONG**: RAISERROR, exit and stop processing
✅ **RIGHT**: TRY/CATCH, log error, continue with next database

## Implementation Timeline

**Day 1 (8 hours)**:
- Parameter validation (3 hrs)
- Database discovery (2 hrs)
- Basic DMV query (3 hrs)

**Day 2 (8 hours)**:
- Dynamic SQL generation (6 hrs)
- Error handling (2 hrs)

**Day 3 (8 hours)**:
- Priority calculation (2 hrs)
- Queue insertion (3 hrs)
- Logging (3 hrs)

**Day 4 (8 hours)**:
- Unit testing (6 hrs)
- Code review prep (2 hrs)

**Day 5 (8 hours)**:
- Integration testing (4 hrs)
- Code review (3 hrs)
- Revisions (1 hr)

**Day 6 (4 hours)**:
- Staging deployment (2 hrs)
- QA handoff (2 hrs)

## Where to Find Things

**Story Documentation**:
- Full Requirements: `/mnt/c/Projects/SQLServer/.ai_docs/Stories/STORY-001-IndexDiscoveryFragmentation.md`
- Technical Guidance: `/mnt/c/Projects/SQLServer/.ai_docs/Stories/STORY-001-TechnicalGuidance.md`
- Code Templates: `STORY-001-TechnicalGuidance.md` (Implementation Roadmap section)

**Reference Code**:
- Existing Implementation: `/mnt/c/Projects/SQLServer/scripts/backup/TSQL/Maintenance/usp_PopulateIndexQueue.sql`
- MaintenanceQueue Schema: `/mnt/c/Projects/SQLServer/src/Tables/Core/MaintenanceQueue.sql`
- DBAdmin Setup: `/mnt/c/Projects/SQLServer/scripts/backup/TSQL/Setup/Initialize-DBAdmin.sql`

**Test Examples**:
- Test Templates: `STORY-001-TechnicalGuidance.md` (Testing Strategy section)
- SQL Injection Test: `STORY-001-TechnicalGuidance.md` (Edge Case Examples)

## Quick Reference: DMV Query Pattern

```sql
SELECT
    DB_NAME() AS DatabaseName,
    SCHEMA_NAME(t.schema_id) AS SchemaName,
    t.name AS TableName,
    i.name AS IndexName,
    ps.page_count,
    ps.avg_fragmentation_in_percent AS Fragmentation
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ps
INNER JOIN sys.indexes i ON ps.object_id = i.object_id AND ps.index_id = i.index_id
INNER JOIN sys.tables t ON i.object_id = t.object_id
WHERE i.name IS NOT NULL                                  -- Skip heaps
AND ps.page_count >= @MinPageCount                       -- Skip small
AND ps.avg_fragmentation_in_percent >= @MinFragmentation -- Apply threshold
ORDER BY ps.avg_fragmentation_in_percent DESC;           -- Highest first
```

## Dry-Run Mode Usage

```sql
-- Preview what would be queued (no database modifications)
EXEC usp_DiscoverIndexFragmentation
    @DryRun = 1;

-- Returns result set with:
-- DatabaseName, SchemaName, TableName, IndexName, Fragmentation, Priority
-- Can review before executing with @DryRun = 0
```

## Success Criteria

Story is done when:
- [ ] Procedure compiles without errors
- [ ] All 8 acceptance criteria passing
- [ ] All 10 edge cases handled
- [ ] Scans 200+ databases in < 10 minutes
- [ ] Dry-run mode works (no MaintenanceQueue modifications)
- [ ] SQL injection prevented (QUOTENAME tested)
- [ ] Logging works (MaintenanceLog entries created)
- [ ] Code reviewed and approved
- [ ] QA validated

## Help & Support

**For Questions**:
1. Review STORY-001-TechnicalGuidance.md (Implementation Roadmap)
2. Check Common Mistakes section in this guide
3. Look at usp_PopulateIndexQueue.sql for reference patterns
4. Ask for code review early (don't wait until end)

**For Performance Issues**:
1. Use LIMITED mode (not SAMPLED or DETAILED)
2. Use FAST_FORWARD cursor (not default)
3. Filter early in WHERE clause (don't post-process)
4. Test with actual 200+ database environment

**For Security Issues**:
1. Use QUOTENAME() for all database names
2. Use sp_executesql with parameters
3. Never concatenate user input into SQL
4. Validate parameter ranges before use

---

**Quick Reference Version**: 1.0
**Last Updated**: 2025-11-05
**For More Details**: See STORY-001-IndexDiscoveryFragmentation.md
