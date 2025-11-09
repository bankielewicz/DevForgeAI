# STORY-008: Index Discovery & Fragmentation Analysis

---
id: STORY-008
title: Index Discovery & Fragmentation Analysis
epic: EPIC-002
status: Backlog
priority: High
points: 13
assigned_to: null
sprint: Backlog
created: 2025-11-05
updated: 2025-11-05
---

## Description

Implement automated index discovery and fragmentation analysis across all user databases (200+ SQL Server instances). The system scans databases using `sys.dm_db_index_physical_stats`, identifies fragmented indexes meeting configurable thresholds (default: reorganize >=15%, rebuild >=30%), and populates the MaintenanceQueue with rebuild/reorganize tasks. Discovery applies hierarchical configuration overrides, excludes small indexes and system databases, and prioritizes work items by fragmentation level.

## User Story

As a **DBA managing 200+ SQL Server instances**,
I want **automated index discovery that scans for fragmented indexes and populates the work queue**,
So that **I don't need to manually identify fragmented indexes, and maintenance operations can be automatically scheduled based on configurable thresholds**.

## Acceptance Criteria

### AC1: Discovery procedure accepts configuration parameters
**Given** the discovery procedure `usp_PopulateIndexMaintenanceQueue`
**When** I execute the procedure
**Then** it accepts the following parameters:
- `@DatabaseName` SYSNAME (specific database or NULL for all user databases)
- `@MinFragmentationReorg` DECIMAL(5,2) (default 15.0%, range 0-100)
- `@MinFragmentationRebuild` DECIMAL(5,2) (default 30.0%, range 0-100)
- `@MinPageCount` INT (default 1000 pages, range >= 0)
- `@DryRun` BIT (default 0, shows what would be queued without inserting)

### AC2: Query sys.dm_db_index_physical_stats in LIMITED mode
**Given** I execute discovery for a specific database
**When** the procedure queries index fragmentation
**Then** it uses `sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED')` for optimal performance (samples leaf-level pages only, not full scan)

### AC3: Apply hierarchical configuration overrides
**Given** configuration exists at multiple scopes (Global, Database, Table, Index)
**When** discovery evaluates thresholds for each index
**Then** it calls `fn_ResolveConfiguration(@DatabaseName, @SchemaName, @TableName, @IndexName)` and uses resolved thresholds (most specific wins)

### AC4: Insert queue items with fragmentation-based priority
**Given** an index has 45% fragmentation (qualifies for rebuild)
**When** discovery inserts the queue item
**Then** Priority is set to CAST(fragmentation_percent AS INT) (e.g., 45), and OperationType is 'INDEX_REBUILD'

**Given** an index has 20% fragmentation (qualifies for reorganize)
**When** discovery inserts the queue item
**Then** Priority is set to 20, and OperationType is 'INDEX_REORG'

### AC5: Skip system databases unless explicitly included
**Given** discovery executes with @DatabaseName = NULL (all databases)
**When** the procedure enumerates databases
**Then** it excludes master, model, msdb, and tempdb by default (only user databases scanned)

**Given** discovery executes with @DatabaseName = 'master' (explicitly named)
**When** the procedure runs
**Then** it includes the master database (explicit override)

### AC6: Skip heaps (tables without clustered indexes)
**Given** a table has no clustered index (heap)
**When** discovery analyzes indexes
**Then** it skips the heap (WHERE index_id > 0 filter), as heaps cannot be rebuilt via ALTER INDEX

### AC7: Log discovery metrics
**Given** discovery completes successfully
**When** the procedure finishes execution
**Then** it logs the following metrics to a discovery log table:
- Total databases scanned
- Total indexes analyzed
- Total items queued (rebuild + reorganize)
- Discovery duration (seconds)
- Timestamp

### AC8: Dry-run mode shows queued items without inserting
**Given** I execute discovery with @DryRun = 1
**When** the procedure runs
**Then** it returns a result set showing all indexes that WOULD be queued (DatabaseName, SchemaName, TableName, IndexName, OperationType, Priority, Fragmentation%), but does NOT insert into MaintenanceQueue

## Technical Specification

### Stored Procedure: usp_PopulateIndexMaintenanceQueue

```sql
CREATE PROCEDURE dbo.usp_PopulateIndexMaintenanceQueue
    @DatabaseName SYSNAME = NULL,           -- NULL = all user databases
    @MinFragmentationReorg DECIMAL(5,2) = 15.0,
    @MinFragmentationRebuild DECIMAL(5,2) = 30.0,
    @MinPageCount INT = 1000,
    @DryRun BIT = 0
AS
BEGIN
    SET NOCOUNT ON;

    -- Parameter validation
    IF @MinFragmentationRebuild < @MinFragmentationReorg
    BEGIN
        RAISERROR('MinFragmentationRebuild must be >= MinFragmentationReorg', 16, 1);
        RETURN;
    END

    IF @MinFragmentationReorg NOT BETWEEN 0 AND 100 OR @MinFragmentationRebuild NOT BETWEEN 0 AND 100
    BEGIN
        RAISERROR('Fragmentation thresholds must be between 0 and 100', 16, 1);
        RETURN;
    END

    -- Variables
    DECLARE @SQL NVARCHAR(MAX);
    DECLARE @CurrentDB SYSNAME;
    DECLARE @TotalDatabases INT = 0;
    DECLARE @TotalIndexes INT = 0;
    DECLARE @TotalQueued INT = 0;
    DECLARE @StartTime DATETIME = GETDATE();
    DECLARE @DurationSeconds INT;

    -- Temp table for databases to process
    CREATE TABLE #DatabasesToScan (DatabaseName SYSNAME);

    -- Enumerate databases
    INSERT INTO #DatabasesToScan (DatabaseName)
    SELECT name
    FROM sys.databases
    WHERE state_desc = 'ONLINE'
      AND is_read_only = 0
      AND name NOT IN ('master', 'model', 'msdb', 'tempdb')
      AND (@DatabaseName IS NULL OR name = @DatabaseName);

    -- If specific database requested and it's a system DB, include it (explicit override)
    IF @DatabaseName IS NOT NULL AND @DatabaseName IN ('master', 'model', 'msdb')
    BEGIN
        INSERT INTO #DatabasesToScan (DatabaseName) VALUES (@DatabaseName);
    END

    SET @TotalDatabases = @@ROWCOUNT;

    -- Dry-run temp table
    IF @DryRun = 1
    BEGIN
        CREATE TABLE #DryRunResults (
            DatabaseName SYSNAME,
            SchemaName SYSNAME,
            TableName SYSNAME,
            IndexName SYSNAME,
            OperationType VARCHAR(50),
            Priority INT,
            FragmentationPercent DECIMAL(5,2),
            PageCount BIGINT
        );
    END

    -- Cursor for database iteration
    DECLARE db_cursor CURSOR LOCAL FAST_FORWARD FOR
        SELECT DatabaseName FROM #DatabasesToScan ORDER BY DatabaseName;

    OPEN db_cursor;
    FETCH NEXT FROM db_cursor INTO @CurrentDB;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        BEGIN TRY
            -- Dynamic SQL to query fragmentation
            SET @SQL = N'
            USE ' + QUOTENAME(@CurrentDB) + N';

            ' + CASE WHEN @DryRun = 1 THEN N'
            INSERT INTO #DryRunResults (DatabaseName, SchemaName, TableName, IndexName, OperationType, Priority, FragmentationPercent, PageCount)
            ' ELSE N'
            INSERT INTO DBAdmin.dbo.MaintenanceQueue (DatabaseName, SchemaName, TableName, IndexName, OperationType, Priority, OperationDetails)
            ' END + N'
            SELECT
                DB_NAME() AS DatabaseName,
                OBJECT_SCHEMA_NAME(ips.object_id) AS SchemaName,
                OBJECT_NAME(ips.object_id) AS TableName,
                i.name AS IndexName,
                CASE
                    WHEN ips.avg_fragmentation_in_percent >= @MinFragmentationRebuild THEN ''INDEX_REBUILD''
                    WHEN ips.avg_fragmentation_in_percent >= @MinFragmentationReorg THEN ''INDEX_REORG''
                END AS OperationType,
                CAST(ips.avg_fragmentation_in_percent AS INT) AS Priority,
                ' + CASE WHEN @DryRun = 1 THEN N'
                ips.avg_fragmentation_in_percent AS FragmentationPercent,
                ips.page_count AS PageCount
                ' ELSE N'
                (SELECT
                    avg_fragmentation_in_percent,
                    page_count,
                    index_type_desc,
                    alloc_unit_type_desc
                 FOR JSON PATH, WITHOUT_ARRAY_WRAPPER) AS OperationDetails
                ' END + N'
            FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, ''LIMITED'') AS ips
            INNER JOIN sys.indexes AS i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
            WHERE ips.avg_fragmentation_in_percent >= @MinFragmentationReorg
              AND ips.page_count >= @MinPageCount
              AND i.index_id > 0 -- Exclude heaps
              AND i.is_disabled = 0 -- Exclude disabled indexes
              AND i.is_hypothetical = 0 -- Exclude hypothetical indexes
              AND OBJECTPROPERTY(ips.object_id, ''IsMSShipped'') = 0; -- Exclude system objects
            ';

            -- Execute dynamic SQL
            EXEC sp_executesql @SQL,
                N'@MinFragmentationReorg DECIMAL(5,2), @MinFragmentationRebuild DECIMAL(5,2), @MinPageCount INT',
                @MinFragmentationReorg, @MinFragmentationRebuild, @MinPageCount;

            SET @TotalQueued += @@ROWCOUNT;

        END TRY
        BEGIN CATCH
            -- Log error but continue processing other databases
            INSERT INTO DBAdmin.dbo.MaintenanceLog (Severity, Message, DatabaseName)
            VALUES ('ERROR', ERROR_MESSAGE(), @CurrentDB);
        END CATCH

        FETCH NEXT FROM db_cursor INTO @CurrentDB;
    END

    CLOSE db_cursor;
    DEALLOCATE db_cursor;

    -- Calculate duration
    SET @DurationSeconds = DATEDIFF(SECOND, @StartTime, GETDATE());

    -- Log discovery metrics
    IF @DryRun = 0
    BEGIN
        INSERT INTO DBAdmin.dbo.DiscoveryLog (DiscoveryType, DatabasesScanned, ItemsQueued, DurationSeconds)
        VALUES ('INDEX_MAINTENANCE', @TotalDatabases, @TotalQueued, @DurationSeconds);
    END

    -- Return dry-run results
    IF @DryRun = 1
    BEGIN
        SELECT * FROM #DryRunResults ORDER BY FragmentationPercent DESC, DatabaseName, SchemaName, TableName, IndexName;
    END

    -- Return summary
    SELECT
        @TotalDatabases AS DatabasesScanned,
        @TotalQueued AS ItemsQueued,
        @DurationSeconds AS DurationSeconds,
        @DryRun AS DryRunMode;

    DROP TABLE #DatabasesToScan;
    IF @DryRun = 1 DROP TABLE #DryRunResults;
END;
GO
```

### Supporting Table: DiscoveryLog

```sql
CREATE TABLE dbo.DiscoveryLog (
    DiscoveryLogID BIGINT IDENTITY(1,1) PRIMARY KEY,
    DiscoveryType VARCHAR(50) NOT NULL, -- 'INDEX_MAINTENANCE', 'STATISTICS_MAINTENANCE', 'CHECKDB'
    DatabasesScanned INT NOT NULL,
    ItemsQueued INT NOT NULL,
    DurationSeconds INT NOT NULL,
    DiscoveryDate DATETIME NOT NULL DEFAULT GETDATE()
);

CREATE NONCLUSTERED INDEX IX_DiscoveryLog_Date
    ON dbo.DiscoveryLog(DiscoveryDate DESC);
```

### Business Rules

1. **Fragmentation Threshold Logic:**
   - Fragmentation < 15%: No action (index healthy)
   - Fragmentation >= 15% and < 30%: INDEX_REORG (lightweight operation)
   - Fragmentation >= 30%: INDEX_REBUILD (heavy operation, reclaims space)

2. **Minimum Page Count Filter:**
   - Default 1000 pages (~8MB for 8KB pages)
   - Rationale: Small indexes have negligible performance impact even when fragmented
   - Reduces queue size by 50-70% in typical environments

3. **System Database Exclusion:**
   - master, model, msdb, tempdb excluded by default
   - Rationale: System databases rarely need index maintenance
   - Exception: Explicit @DatabaseName parameter overrides this rule

4. **Heap Exclusion:**
   - WHERE index_id > 0 filters heaps (tables without clustered indexes)
   - Rationale: Heaps cannot be rebuilt via ALTER INDEX syntax
   - Heap defragmentation requires ALTER TABLE ... REBUILD (future feature)

5. **Priority Calculation:**
   - Priority = CAST(fragmentation_percent AS INT)
   - Example: 45.7% fragmentation → Priority 45
   - Higher priority = processed first by workers

6. **Configuration Override Hierarchy:**
   - Index-level config > Table-level > Database-level > Global default
   - Future enhancement: Call fn_ResolveConfiguration() per index

7. **Duplicate Prevention:**
   - MaintenanceQueue table has unique constraint on (DatabaseName, SchemaName, TableName, IndexName, OperationType)
   - Discovery ignores duplicate key errors (index already queued)

8. **Disabled/Hypothetical Index Exclusion:**
   - WHERE is_disabled = 0 AND is_hypothetical = 0
   - Disabled indexes cannot be rebuilt
   - Hypothetical indexes exist only for query optimizer analysis

### Dependencies

- **STORY-001:** MaintenanceQueue table must exist
- **STORY-005:** fn_ResolveConfiguration() function (future integration)
- **STORY-004:** fn_GetResourceHealth() for throttling (future integration)
- **Permissions:** VIEW SERVER STATE, VIEW DATABASE STATE on all databases
- **SQL Server Version:** 2012+ (sys.dm_db_index_physical_stats supported)

## Edge Cases & Error Handling

### Edge Case 1: Database offline or in recovery
**Scenario:** Discovery attempts to scan a database that is offline or restoring
**Expected Behavior:** TRY/CATCH block catches error, logs to MaintenanceLog with Severity='ERROR', continues processing next database

**Validation:**
```sql
-- Test by setting database offline
ALTER DATABASE TestDB SET OFFLINE;
EXEC dbo.usp_PopulateIndexMaintenanceQueue @DatabaseName = 'TestDB';
-- Expected: Error logged, procedure completes successfully
```

### Edge Case 2: Permission denied accessing DMV
**Scenario:** SQL login lacks VIEW DATABASE STATE permission
**Expected Behavior:** TRY/CATCH catches error 297 (permission denied), logs error, continues to next database

**Mitigation:** Pre-execution permission check (future enhancement):
```sql
IF HAS_PERMS_BY_NAME(DB_NAME(), 'DATABASE', 'VIEW DATABASE STATE') = 0
    RAISERROR('Missing VIEW DATABASE STATE permission', 16, 1);
```

### Edge Case 3: Extremely large database (28TB) causing timeout
**Scenario:** sys.dm_db_index_physical_stats takes > 30 seconds for 28TB database
**Expected Behavior:** Dynamic SQL has no explicit timeout (inherits session settings), may fail with timeout error

**Mitigation:**
- Use LIMITED mode (faster than DETAILED or SAMPLED)
- Consider breaking large databases into batches (future enhancement)
- Increase command timeout in calling application

### Edge Case 4: No indexes meet fragmentation threshold
**Scenario:** All indexes have < 15% fragmentation (healthy database)
**Expected Behavior:** Procedure completes successfully, returns 0 ItemsQueued, logs to DiscoveryLog

**Validation:**
```sql
EXEC dbo.usp_PopulateIndexMaintenanceQueue @DatabaseName = 'HealthyDB';
-- Expected: DatabasesScanned=1, ItemsQueued=0
```

### Edge Case 5: All indexes already in queue (duplicates)
**Scenario:** Discovery runs twice without workers processing queue
**Expected Behavior:** INSERT ignores duplicate key errors (unique constraint), @@ROWCOUNT=0, TotalQueued=0

**Validation:**
```sql
-- Run twice
EXEC dbo.usp_PopulateIndexMaintenanceQueue @DatabaseName = 'DB1';
EXEC dbo.usp_PopulateIndexMaintenanceQueue @DatabaseName = 'DB1';
-- Expected: Second run returns ItemsQueued=0 (duplicates skipped)
```

### Edge Case 6: Configuration override results in zero items queued
**Scenario:** Global threshold is 15%, but Database-level override is 90%
**Expected Behavior:** Discovery uses 90% threshold (resolved config), most indexes excluded, ItemsQueued low or zero

**Validation:**
```sql
-- Set extreme threshold for one database
INSERT INTO dbo.MaintenanceConfiguration (Scope, DatabaseName, ConfigKey, ConfigValue)
VALUES ('Database', 'TestDB', 'MinFragmentationReorg', '90');

EXEC dbo.usp_PopulateIndexMaintenanceQueue @DatabaseName = 'TestDB';
-- Expected: ItemsQueued=0 or very low (only critically fragmented indexes)
```

### Edge Case 7: Dynamic SQL injection attempt in database name
**Scenario:** Malicious input: @DatabaseName = 'TestDB''; DROP TABLE MaintenanceQueue; --'
**Expected Behavior:** QUOTENAME() escapes database name, dynamic SQL fails safely with syntax error

**Security:**
```sql
-- QUOTENAME escapes single quotes
QUOTENAME('TestDB''; DROP TABLE MaintenanceQueue; --')
-- Returns: [TestDB''; DROP TABLE MaintenanceQueue; --]
-- SQL Server interprets this as a single database name (not SQL injection)
```

### Edge Case 8: Cursor exhaustion with 1000+ databases
**Scenario:** SQL Server instance hosts 1000+ databases (rare but possible in shared hosting)
**Expected Behavior:** CURSOR LOCAL FAST_FORWARD processes all databases sequentially, no memory exhaustion

**Performance:**
- Cursor declared with LOCAL FAST_FORWARD (optimized for sequential access)
- Each database processed independently (no transaction scope issues)
- Estimated time: 1000 databases × 5 seconds/database = 83 minutes (within 10-minute SLA? No, needs optimization)

**Mitigation (Phase 2):**
- Parallel processing (spawn multiple discovery workers)
- Filter databases by last scan time (incremental discovery)

### Edge Case 9: @MinFragmentationRebuild less than @MinFragmentationReorg
**Scenario:** Invalid parameters: @MinFragmentationReorg = 30, @MinFragmentationRebuild = 15
**Expected Behavior:** RAISERROR before processing, procedure exits with error

**Validation:**
```sql
EXEC dbo.usp_PopulateIndexMaintenanceQueue
    @MinFragmentationReorg = 30,
    @MinFragmentationRebuild = 15;
-- Expected: Error 50000 "MinFragmentationRebuild must be >= MinFragmentationReorg"
```

### Edge Case 10: Dry-run with 10,000+ indexes
**Scenario:** Dry-run returns massive result set (10,000+ rows)
**Expected Behavior:** Temp table #DryRunResults holds all rows, SELECT returns full result set

**Performance:**
- Temp table uses SYSNAME columns (efficient)
- Result set returned to client may be slow (network transfer)
- Consider pagination or TOP N filter for UI display

## Non-Functional Requirements

### Performance

- **Discovery Speed:** Scan 200+ databases in < 10 minutes (average 3 seconds per database)
- **DMV Query Performance:** sys.dm_db_index_physical_stats in LIMITED mode completes in < 5 seconds per database
- **Queue Insertion:** Batch insertion via dynamic SQL (single INSERT per database, not per index)
- **Cursor Overhead:** CURSOR LOCAL FAST_FORWARD minimizes memory and locking overhead
- **Scalability:** Support databases from 1MB to 28TB (adaptive via LIMITED mode sampling)

**Performance Validation:**
```sql
-- Test with timer
DECLARE @Start DATETIME = GETDATE();
EXEC dbo.usp_PopulateIndexMaintenanceQueue;
SELECT DATEDIFF(SECOND, @Start, GETDATE()) AS DurationSeconds;
-- Expected: < 600 seconds for 200 databases
```

### Security

- **SQL Injection Prevention:** QUOTENAME() used for all dynamic database/object names
- **Permission Enforcement:** Requires VIEW SERVER STATE and VIEW DATABASE STATE
- **Least Privilege:** Procedure runs in DBAdmin context, does not modify user databases
- **Parameter Validation:** All inputs validated (range checks, type checks)
- **Error Logging:** No sensitive data exposed in error messages

**Security Checklist:**
- [x] QUOTENAME() for dynamic identifiers
- [x] sp_executesql with parameterized queries (not string concatenation)
- [x] TRY/CATCH blocks prevent unhandled exceptions
- [x] No dynamic SQL executed in user database context (only SELECT)

### Reliability

- **Fault Tolerance:** TRY/CATCH per database (one database failure does not abort entire discovery)
- **Transactional Safety:** Each database scanned independently (no cross-database transactions)
- **Idempotency:** Running discovery multiple times produces same result (duplicate keys ignored)
- **Graceful Degradation:** If one database is inaccessible, others still processed
- **Recovery:** Discovery can be re-run at any time (stateless operation)

### Observability

- **Discovery Metrics Logged:** DiscoveryLog table captures:
  - DiscoveryType (INDEX_MAINTENANCE)
  - DatabasesScanned (total count)
  - ItemsQueued (total work items)
  - DurationSeconds (execution time)
  - DiscoveryDate (timestamp)

- **Error Logging:** MaintenanceLog captures per-database errors

- **Dry-Run Mode:** @DryRun = 1 shows queued items without side effects (testing/validation)

**Monitoring Query:**
```sql
-- Discovery history
SELECT TOP 10
    DiscoveryDate,
    DatabasesScanned,
    ItemsQueued,
    DurationSeconds,
    CAST(DurationSeconds AS FLOAT) / NULLIF(DatabasesScanned, 0) AS SecondsPerDatabase
FROM dbo.DiscoveryLog
WHERE DiscoveryType = 'INDEX_MAINTENANCE'
ORDER BY DiscoveryDate DESC;
```

### Usability

- **Dry-Run Mode:** @DryRun = 1 previews queued items without modifying MaintenanceQueue
- **Flexible Parameters:** All thresholds configurable (defaults work for 90% of scenarios)
- **Clear Result Set:** Procedure returns summary (DatabasesScanned, ItemsQueued, DurationSeconds)
- **Documentation:** Inline comments explain business logic

### Maintainability

- **Single Responsibility:** Procedure only discovers and queues (does not execute maintenance)
- **Testable:** Dry-run mode enables unit testing without side effects
- **Extensible:** Easy to add new filters (e.g., exclude specific tables)
- **Debuggable:** Error logging + dry-run mode aid troubleshooting

## Test Cases

### Test 1: Discovery with default parameters (all databases)
```sql
-- Arrange: Clean queue
DELETE FROM dbo.MaintenanceQueue;

-- Act: Run discovery
EXEC dbo.usp_PopulateIndexMaintenanceQueue;

-- Assert: Items queued
SELECT COUNT(*) AS TotalQueued FROM dbo.MaintenanceQueue;
-- Expected: > 0 (varies by environment)

SELECT TOP 5 * FROM dbo.MaintenanceQueue ORDER BY Priority DESC;
-- Expected: Highest fragmentation items first
```

### Test 2: Discovery for specific database
```sql
-- Arrange: Clean queue
DELETE FROM dbo.MaintenanceQueue;

-- Act: Run discovery for one database
EXEC dbo.usp_PopulateIndexMaintenanceQueue @DatabaseName = 'AdventureWorks';

-- Assert: Only AdventureWorks items queued
SELECT DISTINCT DatabaseName FROM dbo.MaintenanceQueue;
-- Expected: Only 'AdventureWorks'
```

### Test 3: Dry-run mode (no queue insertion)
```sql
-- Arrange: Clean queue
DELETE FROM dbo.MaintenanceQueue;

-- Act: Run in dry-run mode
EXEC dbo.usp_PopulateIndexMaintenanceQueue @DryRun = 1;

-- Assert: No items inserted
SELECT COUNT(*) FROM dbo.MaintenanceQueue;
-- Expected: 0 (dry-run does not insert)
```

### Test 4: Custom fragmentation thresholds
```sql
-- Arrange: Clean queue
DELETE FROM dbo.MaintenanceQueue;

-- Act: Run with aggressive thresholds
EXEC dbo.usp_PopulateIndexMaintenanceQueue
    @MinFragmentationReorg = 5.0,
    @MinFragmentationRebuild = 10.0;

-- Assert: More items queued (lower thresholds)
SELECT COUNT(*) FROM dbo.MaintenanceQueue;
-- Expected: > baseline (more indexes qualify)
```

### Test 5: Minimum page count filter
```sql
-- Arrange: Clean queue
DELETE FROM dbo.MaintenanceQueue;

-- Act: Run with high page count filter
EXEC dbo.usp_PopulateIndexMaintenanceQueue @MinPageCount = 10000;

-- Assert: Fewer items queued (large indexes only)
SELECT MIN(JSON_VALUE(OperationDetails, '$.page_count')) AS MinPageCount
FROM dbo.MaintenanceQueue;
-- Expected: >= 10000
```

### Test 6: System database exclusion
```sql
-- Arrange: Clean queue
DELETE FROM dbo.MaintenanceQueue;

-- Act: Run discovery
EXEC dbo.usp_PopulateIndexMaintenanceQueue;

-- Assert: No system databases in queue
SELECT DISTINCT DatabaseName FROM dbo.MaintenanceQueue
WHERE DatabaseName IN ('master', 'model', 'msdb', 'tempdb');
-- Expected: 0 rows
```

### Test 7: Priority based on fragmentation
```sql
-- Arrange: Clean queue
DELETE FROM dbo.MaintenanceQueue;

-- Act: Run discovery
EXEC dbo.usp_PopulateIndexMaintenanceQueue;

-- Assert: Priority matches fragmentation
SELECT TOP 5
    Priority,
    CAST(JSON_VALUE(OperationDetails, '$.avg_fragmentation_in_percent') AS DECIMAL(5,2)) AS Fragmentation
FROM dbo.MaintenanceQueue
ORDER BY Priority DESC;
-- Expected: Priority ≈ CAST(Fragmentation AS INT)
```

### Test 8: Invalid parameters (error handling)
```sql
-- Act: Run with invalid thresholds
EXEC dbo.usp_PopulateIndexMaintenanceQueue
    @MinFragmentationReorg = 30,
    @MinFragmentationRebuild = 15; -- Invalid (rebuild < reorg)

-- Assert: Error raised
-- Expected: Error 50000 "MinFragmentationRebuild must be >= MinFragmentationReorg"
```

### Test 9: Discovery metrics logged
```sql
-- Arrange: Clean discovery log
DELETE FROM dbo.DiscoveryLog WHERE DiscoveryType = 'INDEX_MAINTENANCE';

-- Act: Run discovery
EXEC dbo.usp_PopulateIndexMaintenanceQueue;

-- Assert: Log entry created
SELECT * FROM dbo.DiscoveryLog WHERE DiscoveryType = 'INDEX_MAINTENANCE';
-- Expected: 1 row with DatabasesScanned, ItemsQueued, DurationSeconds
```

### Test 10: Duplicate prevention (idempotency)
```sql
-- Arrange: Clean queue
DELETE FROM dbo.MaintenanceQueue;

-- Act: Run discovery twice
EXEC dbo.usp_PopulateIndexMaintenanceQueue @DatabaseName = 'TestDB';
DECLARE @FirstRunCount INT = @@ROWCOUNT;

EXEC dbo.usp_PopulateIndexMaintenanceQueue @DatabaseName = 'TestDB';
DECLARE @SecondRunCount INT = @@ROWCOUNT;

-- Assert: Second run queues 0 items (duplicates ignored)
SELECT @FirstRunCount AS FirstRun, @SecondRunCount AS SecondRun;
-- Expected: FirstRun > 0, SecondRun = 0
```

## Definition of Done

- [ ] Stored procedure `usp_PopulateIndexMaintenanceQueue` created with all parameters
- [ ] DiscoveryLog table created with indexes
- [ ] Parameter validation implemented (range checks, rebuild >= reorg)
- [ ] Dynamic SQL uses QUOTENAME() for SQL injection prevention
- [ ] TRY/CATCH error handling per database
- [ ] Dry-run mode functional (returns result set without inserting)
- [ ] Discovery metrics logged to DiscoveryLog table
- [ ] All 8 acceptance criteria verified
- [ ] All 10 edge cases tested and documented
- [ ] Unit tests pass (10 tests minimum)
- [ ] Integration test: Scan 10+ databases in < 30 seconds
- [ ] Performance test: Scan 200 databases in < 10 minutes
- [ ] Security test: SQL injection attempt blocked by QUOTENAME()
- [ ] Code reviewed against coding-standards.md
- [ ] Deployed to local dev SQL Server instance
- [ ] Documentation updated (source-tree.md, README.md)

## Implementation Notes

**Implementation Order:**

1. Create DiscoveryLog table (audit trail)
2. Implement usp_PopulateIndexMaintenanceQueue skeleton (parameters, validation)
3. Implement database enumeration logic (cursor over sys.databases)
4. Implement dynamic SQL for fragmentation query (sys.dm_db_index_physical_stats)
5. Implement priority calculation and queue insertion
6. Implement dry-run mode (temp table #DryRunResults)
7. Implement error handling (TRY/CATCH per database)
8. Implement discovery metrics logging
9. Write unit tests (10 tests)
10. Performance validation (200 databases)

**Performance Optimization Tips:**

- Use LIMITED mode (not DETAILED or SAMPLED) for fastest results
- CURSOR LOCAL FAST_FORWARD minimizes overhead
- Single INSERT per database (not per index) via dynamic SQL
- Consider parallel discovery workers (Phase 2 enhancement)

**Security Considerations:**

- QUOTENAME() prevents SQL injection in database names
- sp_executesql with parameters prevents injection in threshold values
- Procedure does not require elevated permissions in user databases

**Future Enhancements (Phase 2):**

- Integrate fn_ResolveConfiguration() for per-index threshold overrides
- Parallel discovery (multiple workers scanning different databases)
- Incremental discovery (only scan databases modified since last discovery)
- Discovery scheduling (SQL Agent job every 24 hours)
- Discovery reporting dashboard (Power BI or SSRS)

## Workflow History

### 2025-11-05 - Status: Backlog
- Story created from EPIC-002 Feature 2.1
- Assigned to Backlog (depends on EPIC-001 completion)
- Estimated at 13 points (Large complexity, multi-database iteration)
- Priority: High (foundation for all index maintenance)
- Dependencies: STORY-001 (MaintenanceQueue table)

---

**File Location:** `.ai_docs/Stories/STORY-008-index-discovery-fragmentation.story.md`
**Epic:** EPIC-002 (Index Maintenance Engine)
**Sprint:** Backlog (awaiting EPIC-001 completion)
**Related Stories:** STORY-001 (Queue Infrastructure), STORY-005 (Configuration Management)
