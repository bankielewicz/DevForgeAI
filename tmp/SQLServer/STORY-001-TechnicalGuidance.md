# STORY-001: Technical Implementation Guidance

**Purpose**: Detailed implementation guidance for developers
**Audience**: T-SQL developers implementing usp_DiscoverIndexFragmentation
**Last Updated**: 2025-11-05

## Implementation Roadmap

### Phase 1: Foundation (Day 1)
- [ ] Create procedure skeleton with parameter validation
- [ ] Test parameter validation logic
- [ ] Implement error handling framework

### Phase 2: Core Logic (Days 2-3)
- [ ] Implement database discovery logic
- [ ] Implement dynamic SQL for fragmentation analysis
- [ ] Implement priority calculation
- [ ] Test with single database first

### Phase 3: Enterprise Features (Day 4)
- [ ] Implement configuration resolution
- [ ] Implement dry-run mode
- [ ] Implement logging

### Phase 4: Testing & Polish (Day 5)
- [ ] Edge case testing
- [ ] Performance testing (200+ databases)
- [ ] Code review and documentation
- [ ] QA validation

## Code Structure Reference

### Parameter Validation Template

```sql
CREATE PROCEDURE usp_DiscoverIndexFragmentation
    @DatabaseName NVARCHAR(128) = NULL,
    @MinFragmentationReorg DECIMAL(5,2) = 15.0,
    @MinFragmentationRebuild DECIMAL(5,2) = 30.0,
    @MinPageCount INT = 1000,
    @DryRun BIT = 0,
    @ExcludeSystemDatabases BIT = 1,
    @IncludeSingleDBOnly BIT = 0
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @ErrorMessage NVARCHAR(MAX);
    DECLARE @ReturnCode INT = 0;
    DECLARE @StartTime DATETIME2 = SYSDATETIME();

    -- 1. PARAMETER VALIDATION
    BEGIN TRY
        -- Validate fragmentation thresholds
        IF @MinFragmentationRebuild < @MinFragmentationReorg
        BEGIN
            SET @ErrorMessage = CONCAT(
                '@MinFragmentationRebuild (',
                CAST(@MinFragmentationRebuild AS NVARCHAR(10)),
                ') must be >= @MinFragmentationReorg (',
                CAST(@MinFragmentationReorg AS NVARCHAR(10)),
                ')'
            );
            RAISERROR(@ErrorMessage, 16, 1);
        END

        -- Validate threshold ranges (0-100)
        IF @MinFragmentationReorg < 0 OR @MinFragmentationReorg > 100
        BEGIN
            RAISERROR('@MinFragmentationReorg must be between 0 and 100', 16, 1);
        END

        IF @MinFragmentationRebuild < 0 OR @MinFragmentationRebuild > 100
        BEGIN
            RAISERROR('@MinFragmentationRebuild must be between 0 and 100', 16, 1);
        END

        -- Validate page count
        IF @MinPageCount < 0
        BEGIN
            RAISERROR('@MinPageCount must be >= 0', 16, 1);
        END

        -- Validate bit parameters
        IF @DryRun NOT IN (0, 1)
        BEGIN
            RAISERROR('@DryRun must be 0 or 1', 16, 1);
        END

        -- Validate database name (if provided)
        IF @DatabaseName IS NOT NULL
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM sys.databases
                WHERE name = @DatabaseName
                AND state_desc = 'ONLINE'
            )
            BEGIN
                SET @ErrorMessage = CONCAT(
                    'Database ''',
                    @DatabaseName,
                    ''' is not online or does not exist'
                );
                RAISERROR(@ErrorMessage, 16, 1);
            END
        END

        PRINT '================================================================================';
        PRINT 'Index Fragmentation Discovery';
        PRINT 'Started: ' + CONVERT(VARCHAR(30), @StartTime, 120);
        PRINT '================================================================================';
        PRINT '';

    END TRY
    BEGIN CATCH
        SET @ReturnCode = 1;
        RAISERROR(@ErrorMessage, 16, 1);
        RETURN @ReturnCode;
    END CATCH

    -- Continue with rest of implementation...
END
GO
```

### Database Discovery Template

```sql
-- After parameter validation, create table for database list
DECLARE @DatabaseList TABLE (
    DatabaseName NVARCHAR(128) NOT NULL,
    DatabaseID INT NOT NULL,
    IsAG BIT NOT NULL,
    IsPreferred BIT NOT NULL
);

-- Populate with online databases
INSERT INTO @DatabaseList (DatabaseName, DatabaseID, IsAG, IsPreferred)
SELECT
    db.name,
    db.database_id,
    CASE WHEN drs.database_id IS NOT NULL THEN 1 ELSE 0 END,
    CASE
        WHEN drs.database_id IS NULL THEN 1  -- Not AG database
        WHEN @IncludeSingleDBOnly = 1 THEN 1  -- Force include if single DB
        ELSE ISNULL(DBAdmin.dbo.fn_IsPreferredMaintenanceReplica(db.name), 1)
    END
FROM sys.databases db
LEFT JOIN sys.dm_hadr_database_replica_states drs
    ON db.database_id = drs.database_id
    AND drs.is_local = 1
WHERE db.state_desc = 'ONLINE'
AND db.is_read_only = 0
AND (
    -- Filter system databases if requested
    (@ExcludeSystemDatabases = 1 AND db.database_id > 4)
    OR (@ExcludeSystemDatabases = 0)
)
AND (
    -- Filter by specific database if provided
    @DatabaseName IS NULL
    OR db.name = @DatabaseName
);

-- Log databases to scan
DECLARE @DatabaseCount INT = (SELECT COUNT(*) FROM @DatabaseList);
PRINT CONCAT('Scanning ', @DatabaseCount, ' database(s)...');
PRINT '';
```

### Dynamic SQL Template for DMV Query

```sql
-- Within cursor loop over databases
DECLARE @CurrentDB NVARCHAR(128);
DECLARE @SQL NVARCHAR(MAX);
DECLARE @SQLParams NVARCHAR(500);
DECLARE @DatabaseID INT;
DECLARE @DryRunOutput TABLE (
    DatabaseName NVARCHAR(128),
    SchemaName SYSNAME,
    TableName SYSNAME,
    IndexName SYSNAME,
    PageCount INT,
    Fragmentation DECIMAL(5,2),
    Priority INT,
    OperationType VARCHAR(50),
    OperationDetails NVARCHAR(MAX)
);

DECLARE db_cursor CURSOR LOCAL FAST_FORWARD FOR
SELECT DatabaseName, DatabaseID FROM @DatabaseList;

OPEN db_cursor;
FETCH NEXT FROM db_cursor INTO @CurrentDB, @DatabaseID;

WHILE @@FETCH_STATUS = 0
BEGIN
    BEGIN TRY
        PRINT CONCAT('Scanning database: ', @CurrentDB);

        -- Build dynamic SQL to analyze indexes
        SET @SQL = N'
        USE [' + QUOTENAME(@CurrentDB) + '];

        INSERT INTO ' + CASE WHEN @DryRun = 1 THEN '@DryRunOutput' ELSE 'DBAdmin.dbo.MaintenanceQueue' END + '
        (
            DatabaseName,
            SchemaName,
            TableName,
            IndexName,
            OperationType,
            Priority,
            Status,
            CreatedDate,
            OperationDetails
        )
        SELECT
            DB_NAME() AS DatabaseName,
            SCHEMA_NAME(t.schema_id) AS SchemaName,
            t.name AS TableName,
            i.name AS IndexName,
            CASE
                WHEN ps.avg_fragmentation_in_percent >= @RebuildThreshold
                    THEN ''INDEX_REBUILD''
                WHEN ps.avg_fragmentation_in_percent >= @ReorgThreshold
                    THEN ''INDEX_REORG''
                ELSE NULL
            END AS OperationType,
            -- Priority calculation based on fragmentation band
            CASE
                WHEN ps.avg_fragmentation_in_percent >= 80 THEN 1
                WHEN ps.avg_fragmentation_in_percent >= 50 THEN 5
                WHEN ps.avg_fragmentation_in_percent >= 30 THEN 15
                WHEN ps.avg_fragmentation_in_percent >= 15 THEN 30
                ELSE 99
            END + (ps.page_count / 100000.0) AS Priority,
            ''Pending'' AS Status,
            GETDATE() AS CreatedDate,
            (
                SELECT (
                    SELECT ps.avg_fragmentation_in_percent AS fragmentation_percent,
                           ps.page_count AS page_count,
                           CASE
                               WHEN ps.avg_fragmentation_in_percent >= 80 THEN ''80-100%''
                               WHEN ps.avg_fragmentation_in_percent >= 50 THEN ''50-79%''
                               WHEN ps.avg_fragmentation_in_percent >= 30 THEN ''30-49%''
                               WHEN ps.avg_fragmentation_in_percent >= 15 THEN ''15-29%''
                           END AS priority_band,
                           NEWID() AS discovery_run_id,
                           GETUTCDATE() AS discovery_timestamp
                    FOR JSON PATH, WITHOUT_ARRAY_WRAPPER
                )
            ) AS OperationDetails
        FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, ''LIMITED'') ps
        INNER JOIN sys.indexes i ON ps.object_id = i.object_id AND ps.index_id = i.index_id
        INNER JOIN sys.tables t ON i.object_id = t.object_id
        WHERE i.name IS NOT NULL  -- Skip heaps
        AND ps.page_count >= @MinPageCount
        AND (
            ps.avg_fragmentation_in_percent >= @ReorgThreshold
            OR ps.avg_fragmentation_in_percent >= @RebuildThreshold
        )
        AND NOT EXISTS (
            SELECT 1 FROM DBAdmin.dbo.MaintenanceQueue mq
            WHERE mq.DatabaseName = DB_NAME()
            AND mq.SchemaName = SCHEMA_NAME(t.schema_id)
            AND mq.TableName = t.name
            AND mq.IndexName = i.name
            AND mq.OperationType IN (''INDEX_REORG'', ''INDEX_REBUILD'')
        );
        ';

        -- Set parameters for dynamic SQL
        SET @SQLParams = N'
        @MinPageCount INT,
        @ReorgThreshold DECIMAL(5,2),
        @RebuildThreshold DECIMAL(5,2)
        ';

        -- Execute dynamic SQL
        EXEC sp_executesql
            @SQL,
            @SQLParams,
            @MinPageCount = @MinPageCount,
            @ReorgThreshold = @MinFragmentationReorg,
            @RebuildThreshold = @MinFragmentationRebuild;

        PRINT CONCAT('  Completed successfully');

    END TRY
    BEGIN CATCH
        -- Handle database access errors gracefully
        DECLARE @ErrorMsg NVARCHAR(MAX) = ERROR_MESSAGE();
        DECLARE @ErrorNum INT = ERROR_NUMBER();

        IF @ErrorNum = 916  -- Ad hoc access denied
        BEGIN
            PRINT CONCAT('  SKIPPED: Permission denied - ', @ErrorMsg);
            -- Log to MaintenanceLog
            INSERT INTO DBAdmin.dbo.MaintenanceLog
            (DatabaseName, MaintenanceType, Status, ErrorMessage, StartTime, EndTime, DurationSeconds)
            VALUES (@CurrentDB, 'INDEX_DISCOVERY', 'SKIPPED', @ErrorMsg, @StartTime, SYSDATETIME(),
                    DATEDIFF(SECOND, @StartTime, SYSDATETIME()));
        END
        ELSE IF @ErrorNum = 924  -- Database not accessible
        BEGIN
            PRINT CONCAT('  SKIPPED: Database not online - ', @ErrorMsg);
            INSERT INTO DBAdmin.dbo.MaintenanceLog
            (DatabaseName, MaintenanceType, Status, ErrorMessage, StartTime, EndTime, DurationSeconds)
            VALUES (@CurrentDB, 'INDEX_DISCOVERY', 'SKIPPED', 'Database is not online', @StartTime, SYSDATETIME(),
                    DATEDIFF(SECOND, @StartTime, SYSDATETIME()));
        END
        ELSE
        BEGIN
            PRINT CONCAT('  ERROR: ', @ErrorMsg);
            INSERT INTO DBAdmin.dbo.MaintenanceLog
            (DatabaseName, MaintenanceType, Status, ErrorMessage, StartTime, EndTime, DurationSeconds)
            VALUES (@CurrentDB, 'INDEX_DISCOVERY', 'FAILED', @ErrorMsg, @StartTime, SYSDATETIME(),
                    DATEDIFF(SECOND, @StartTime, SYSDATETIME()));
        END
    END CATCH

    FETCH NEXT FROM db_cursor INTO @CurrentDB, @DatabaseID;
END

CLOSE db_cursor;
DEALLOCATE db_cursor;
```

### Dry-Run Result Return Template

```sql
-- If dry-run mode, return results without inserting
IF @DryRun = 1
BEGIN
    PRINT '';
    PRINT 'DRY-RUN MODE: Results shown below (NO MaintenanceQueue modifications)';
    PRINT '';

    SELECT
        NULL AS QueueID,
        DatabaseName,
        SchemaName,
        TableName,
        IndexName,
        PageCount,
        Fragmentation,
        Priority,
        OperationType,
        OperationDetails
    FROM @DryRunOutput
    ORDER BY Priority ASC, PageCount DESC;

    -- Show dry-run summary
    DECLARE @ItemCount INT = (SELECT COUNT(*) FROM @DryRunOutput);
    PRINT '';
    PRINT CONCAT('DRY-RUN SUMMARY: ', @ItemCount, ' items would be queued');
    PRINT '';
END
```

## Priority Calculation Deep Dive

### Priority Band Logic

```sql
-- Fragmentation band assignment (1 = critical, 100 = low priority)
CASE
    WHEN Fragmentation >= 80 THEN 1      -- Critical: 80-100%
    WHEN Fragmentation >= 50 THEN 5      -- High: 50-79%
    WHEN Fragmentation >= 30 THEN 15     -- Medium: 30-49%
    WHEN Fragmentation >= 15 THEN 30     -- Normal: 15-29%
    ELSE 99                              -- Skip: <15%
END

-- Within same band, add fractional priority for page count (tie-breaker)
+ (PageCount / 100000.0)  -- Add 0.01 for each 100K pages

-- Examples:
-- Fragmentation 87%, 45000 pages -> Priority 1 + 0.45 = 1.45
-- Fragmentation 87%, 250000 pages -> Priority 1 + 2.5 = 3.5 (still in critical band)
-- Fragmentation 65%, 100000 pages -> Priority 5 + 1.0 = 6.0
-- Fragmentation 35%, 2000 pages -> Priority 15 + 0.02 = 15.02
```

### Rationale for Bands

```
80-100% Fragmentation = CRITICAL
  - Performance impact severe (100x slower queries)
  - Risk of index completely unusable
  - Rebuild often required (REORG ineffective)
  - Action: Immediate (Priority 1)

50-79% Fragmentation = HIGH
  - Performance impact significant (10x slower)
  - REORG or REBUILD both viable
  - Noticeable query slowdown
  - Action: Within 24 hours (Priority 5)

30-49% Fragmentation = MEDIUM
  - Performance impact moderate (2-5x slower)
  - REBUILD recommended (REORG won't help much)
  - Noticeable for large scans
  - Action: Within 1 week (Priority 15)

15-29% Fragmentation = NORMAL
  - Performance impact minimal (10-20%)
  - REORG sufficient and efficient
  - Only affects very large scans
  - Action: Normal maintenance cycle (Priority 30)

<15% Fragmentation = SKIP
  - Performance impact negligible
  - Maintenance not cost-justified
  - Re-check when next scan runs
  - Action: None (not queued)
```

## Testing Strategy

### Unit Test Examples

```sql
-- Test 1: Parameter Validation
DECLARE @ReturnCode INT;

-- Test invalid threshold ordering
SET @ReturnCode = NULL;
BEGIN TRY
    EXEC DBAdmin.dbo.usp_DiscoverIndexFragmentation
        @MinFragmentationReorg = 50.0,
        @MinFragmentationRebuild = 30.0;  -- INVALID: REBUILD < REORG
    SET @ReturnCode = 0;
END TRY
BEGIN CATCH
    SET @ReturnCode = ERROR_NUMBER();
END CATCH

-- Assert: Should fail with error
ASSERT @ReturnCode != 0, 'Parameter validation should reject inverted thresholds';

-- Test 2: Priority Calculation
-- Setup: Create test table and fragment an index
-- Execute discovery
-- Assert: Index with 87% fragmentation has Priority 1 (in critical band)
-- Assert: Index with 65% fragmentation has Priority 5 (in high band)

-- Test 3: Heap Exclusion
-- Setup: Create heap table (no clustered index)
-- Execute discovery
-- Assert: Heap table not included in results

-- Test 4: SQL Injection Prevention
SET @ReturnCode = NULL;
BEGIN TRY
    EXEC DBAdmin.dbo.usp_DiscoverIndexFragmentation
        @DatabaseName = "'; DROP TABLE dbo.MaintenanceQueue; --";
    SET @ReturnCode = 0;
END TRY
BEGIN CATCH
    SET @ReturnCode = 0;  -- Error expected, that's good
END CATCH

-- Assert: MaintenanceQueue table still exists
-- Assert: No SQL injection occurred
```

### Integration Test Examples

```sql
-- Test 1: End-to-End Discovery
-- Setup: Test database with 5 fragmented indexes
-- Execute: EXEC usp_DiscoverIndexFragmentation @DatabaseName = 'TestDB', @DryRun = 0
-- Assert: All 5 indexes inserted into MaintenanceQueue
-- Assert: Correct OperationType assigned (REORG vs REBUILD)
-- Assert: Priority values correct based on fragmentation %

-- Test 2: Duplicate Detection
-- Setup: Queue index 'IX_Test' in 'TestDB'
-- Execute: EXEC usp_DiscoverIndexFragmentation again
-- Assert: UNIQUE constraint violation caught
-- Assert: Original queue item unchanged
-- Assert: Duplicate log entry created

-- Test 3: Large Database Performance
-- Setup: Test database with 10,000+ indexes
-- Start timer
-- Execute: EXEC usp_DiscoverIndexFragmentation @DatabaseName = 'LargeDB'
-- Assert: Completes in < 60 seconds
-- Assert: All indexes analyzed
-- Assert: Correct queue items created
```

## Performance Optimization Tips

### 1. Use LIMITED Mode (Not SAMPLED)

```sql
-- GOOD: Fast, aggregate fragmentation only
sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED')

-- AVOID: Slow, per-partition fragmentation
sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'SAMPLED')

-- NEVER: Extremely slow, accurate but expensive
sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'DETAILED')
```

### 2. Use FAST_FORWARD Cursor (Not Default)

```sql
-- GOOD: Read-only, forward-only, minimal memory
DECLARE db_cursor CURSOR LOCAL FAST_FORWARD FOR
SELECT DatabaseName FROM @DatabaseList;

-- AVOID: Default cursor uses more memory
DECLARE db_cursor CURSOR FOR
SELECT DatabaseName FROM @DatabaseList;
```

### 3. Filter Early in WHERE Clause

```sql
-- GOOD: Filter before returning to client
WHERE ps.page_count >= @MinPageCount
AND ps.avg_fragmentation_in_percent >= @MinFragmentationReorg
AND i.name IS NOT NULL

-- AVOID: Return everything, filter in application
WHERE 1=1  -- Then filter fragmentation < threshold in app
```

### 4. Use Proper Indexing on MaintenanceQueue

```sql
-- Query pattern: SELECT TOP 1 FROM MaintenanceQueue
-- WHERE Status = 'Pending' ORDER BY Priority, CreatedDate
-- Recommended index:
CREATE NONCLUSTERED INDEX IX_MaintenanceQueue_Status_Priority
    ON dbo.MaintenanceQueue (Status, Priority DESC, CreatedDate ASC)
    INCLUDE (QueueID, DatabaseName, OperationType)
    WITH (FILLFACTOR = 90);
```

## Security Checklist

- [ ] All database names use QUOTENAME()
- [ ] No user input concatenated directly into SQL
- [ ] All string parameters validated for length
- [ ] Error messages don't leak sensitive information
- [ ] No credentials in logs or output
- [ ] Requires VIEW SERVER STATE permission (documented)
- [ ] INSERT/UPDATE only on DBAdmin tables (no user DB modification)
- [ ] Dynamic SQL uses sp_executesql with parameters

## Common Pitfalls to Avoid

1. **Forgetting QUOTENAME()**
   - WRONG: `USE [` + @DatabaseName + `];`
   - RIGHT: `USE [` + QUOTENAME(@DatabaseName) + `];`

2. **Not Handling Database Not Online**
   - WRONG: Fails with error, stops execution
   - RIGHT: Caught in TRY/CATCH, continues processing

3. **Using SAMPLED or DETAILED Mode**
   - WRONG: Takes 2-10x longer than LIMITED
   - RIGHT: Use LIMITED for discovery, SAMPLED only if per-partition data needed

4. **Forgetting IS NOT NULL Check for Heaps**
   - WRONG: Includes heaps in results (IndexName = NULL)
   - RIGHT: Filter: `WHERE i.name IS NOT NULL`

5. **Not Tracking Duplicate Queue Items**
   - WRONG: Fails on UNIQUE constraint
   - RIGHT: Caught in TRY/CATCH, log as "already queued"

6. **Returning Unbounded Result Sets**
   - WRONG: SELECT * FROM large table
   - RIGHT: Use DRY-RUN mode for preview, limit columns

7. **Not Logging Errors with Context**
   - WRONG: RAISERROR('Error occurred')
   - RIGHT: RAISERROR with database name, index name, error detail

## Debugging Tips

### Enable Detailed Tracing

```sql
-- Add to procedure for debugging
DECLARE @DebugMode BIT = 1;

IF @DebugMode = 1
BEGIN
    PRINT 'DEBUG: @MinFragmentationReorg = ' + CAST(@MinFragmentationReorg AS VARCHAR(10));
    PRINT 'DEBUG: @MinFragmentationRebuild = ' + CAST(@MinFragmentationRebuild AS VARCHAR(10));
    PRINT 'DEBUG: @MinPageCount = ' + CAST(@MinPageCount AS VARCHAR(10));
    PRINT 'DEBUG: @DryRun = ' + CAST(@DryRun AS VARCHAR(1));
END
```

### Monitor Dynamic SQL Execution

```sql
-- Capture generated SQL for review
DECLARE @DebugSQL BIT = 1;

IF @DebugSQL = 1
BEGIN
    PRINT 'DEBUG: Generated SQL:';
    PRINT @SQL;
    PRINT '';
END

-- Then execute
EXEC sp_executesql @SQL, @SQLParams, ...;
```

### Check Queue Population

```sql
-- Verify items were inserted
SELECT
    COUNT(*) AS QueueItemCount,
    MIN(Priority) AS LowestPriority,
    MAX(Priority) AS HighestPriority,
    MIN(CAST(JSON_VALUE(OperationDetails, '$.fragmentation_percent') AS DECIMAL(5,2))) AS MinFragmentation,
    MAX(CAST(JSON_VALUE(OperationDetails, '$.fragmentation_percent') AS DECIMAL(5,2))) AS MaxFragmentation
FROM DBAdmin.dbo.MaintenanceQueue
WHERE CreatedDate >= DATEADD(MINUTE, -5, GETDATE())
AND Status = 'Pending';
```

## Deployment Checklist

- [ ] Procedure created in DBAdmin database
- [ ] Procedure compiles without errors
- [ ] Extended properties added for documentation
- [ ] Permissions validated (VIEW SERVER STATE on sysadmin account)
- [ ] Test execution on staging environment
- [ ] Performance baseline established (200+ DB scan time)
- [ ] Logging verified in MaintenanceLog table
- [ ] Rollback procedure documented
- [ ] Deployment script created and tested
- [ ] QA sign-off obtained

---

**Guidance Version**: 1.0
**Last Updated**: 2025-11-05
**Developer Reference**: Complete
