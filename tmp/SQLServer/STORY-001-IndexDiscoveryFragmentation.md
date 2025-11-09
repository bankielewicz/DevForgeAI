# STORY-001: Index Discovery & Fragmentation Analysis for SQL Server Maintenance

**Status**: Backlog
**Priority**: HIGH
**Story Points**: 5
**Epic**: EPIC-001: DBAdmin Enterprise Maintenance Solution
**Sprint**: SPRINT-01 (recommended)

## User Story

As a Database Administrator managing 200+ SQL Server instances,
I want an automated procedure to discover and analyze index fragmentation across all databases,
So that I can populate the maintenance queue without manual index identification and support proactive performance optimization at scale.

## Acceptance Criteria

### Scenario 1: Basic Index Discovery with Default Thresholds
- Given a SQL Server instance with 10+ user databases containing fragmented indexes
- When I execute the discovery procedure with default parameters
- Then the procedure scans all online user databases in LIMITED mode
- And indexes with fragmentation >= 15% are identified as REORG candidates
- And indexes with fragmentation >= 30% are identified as REBUILD candidates
- And small indexes (< 1000 pages) are excluded from discovery
- And system databases (master, model, msdb, tempdb) are skipped
- And each discovered index is inserted into MaintenanceQueue with appropriate OperationType
- And queue items are ordered by fragmentation level (higher fragmentation = lower priority number)

### Scenario 2: Custom Fragmentation Thresholds
- Given I want to use custom fragmentation thresholds (REORG at 20%, REBUILD at 35%)
- When I execute the discovery procedure with @MinFragmentationReorg = 20.0 and @MinFragmentationRebuild = 35.0
- Then thresholds are validated (@MinFragmentationRebuild >= @MinFragmentationReorg)
- And the procedure applies custom thresholds instead of defaults
- And discovery results are filtered using the custom thresholds
- And all queue items reflect the custom thresholds used

### Scenario 3: Single Database Scan
- Given I want to scan only a specific database (e.g., 'ProductionDB')
- When I execute the discovery procedure with @DatabaseName = 'ProductionDB'
- Then only the specified database is scanned
- And all other databases are skipped regardless of configuration
- And the log includes confirmation of database scope

### Scenario 4: Configuration Override Resolution
- Given fragmentation discovery with hierarchical configuration overrides defined
- When the procedure processes each index
- Then configuration is resolved in priority order: Index-level > Table-level > Database-level > Server-level
- And if an index has IncludeInMaintenance = 0 at any level, that index is excluded
- And if a database has SkipMaintenanceDiscovery = 1, that database is skipped entirely
- And applied configuration is logged with OperationDetails showing override source

### Scenario 5: Dry-Run Mode Validation
- Given I want to preview what would be discovered without inserting queue items
- When I execute the discovery procedure with @DryRun = 1
- Then the procedure scans all databases and calculates fragmentation metrics
- And results are returned in a result set showing proposed queue items
- And NO rows are inserted into MaintenanceQueue
- And a summary is printed showing: databases_scanned, indexes_analyzed, items_that_would_be_queued
- And dry-run results can be reviewed before full execution

### Scenario 6: Skip Heaps and System Objects
- Given a database contains heap tables (tables without clustered indexes)
- When the discovery procedure processes indexes
- Then heap tables are automatically excluded (no IndexName exists for heap)
- And internal/system indexes are excluded from discovery
- And only named indexes (non-heap) are considered for fragmentation analysis

### Scenario 7: Logging and Discovery Metrics
- Given the discovery procedure executes across multiple databases
- When processing completes
- Then a discovery log entry is created with:
  - Total databases scanned
  - Total indexes analyzed
  - Total queue items inserted
  - Minimum, average, and maximum fragmentation levels found
  - Discovery duration in seconds
  - Any errors encountered during processing (per database)
- And logs are written to MaintenanceLog table with OperationType = 'INDEX_DISCOVERY'
- And DatabaseName = NULL for instance-level summary log entry

### Scenario 8: Priority Assignment Based on Fragmentation Level
- Given indexes with varying fragmentation levels are discovered
- When queue items are inserted into MaintenanceQueue
- Then Priority is calculated based on fragmentation percentage:
  - 80-100% fragmentation = Priority 1 (critical)
  - 50-79% fragmentation = Priority 5 (high)
  - 30-49% fragmentation = Priority 15 (medium)
  - 15-29% fragmentation = Priority 30 (normal)
- And within same priority band, items are ordered by PageCount DESC (larger first)
- And priority calculation is logged for audit trail

## Edge Cases and Error Conditions

### Edge Case 1: Database Offline During Scan
- Given a database transitions from ONLINE to OFFLINE during discovery
- When the procedure attempts to access sys.dm_db_index_physical_stats for that database
- Then a TRY/CATCH block catches the error
- And the database is marked as skipped in the discovery log
- And error message is recorded: "Database [name] is not online"
- And scanning continues with remaining databases
- And procedure completes with overall SUCCESS status (not FAILED)

### Edge Case 2: Permission Denied on DMV Access
- Given the discovery procedure lacks permission to read sys.dm_db_index_physical_stats
- When the procedure executes the DMV query
- Then the error is caught in TRY/CATCH
- And the error message is logged with full details
- And discovery stops with FAILED status (requires corrective action)
- And error includes suggestion: "Grant VIEW SERVER STATE permission"

### Edge Case 3: Extremely Large Database Timeout
- Given a 28TB database with millions of indexes
- When the discovery procedure executes sys.dm_db_index_physical_stats in LIMITED mode
- Then the procedure includes a command timeout mechanism
- And if scan exceeds 300 seconds per database, it times out gracefully
- And partial results are logged: indexes scanned before timeout
- And database is marked as "Timed Out" in discovery log
- And procedure continues with next database

### Edge Case 4: No Indexes Meet Fragmentation Threshold
- Given a database has 100+ indexes but all are < 15% fragmented
- When discovery processes the database
- Then NO queue items are inserted for that database
- And a log entry is created: "Database [name] scanned, 0 items queued"
- And discovery continues normally (not an error condition)

### Edge Case 5: Duplicate Prevention
- Given an index is already in MaintenanceQueue with Status = 'Pending'
- When the discovery procedure encounters that index again
- Then the UNIQUE constraint on (DatabaseName, SchemaName, TableName, IndexName, OperationType) triggers
- And the duplicate INSERT fails
- And the failure is caught as a violation (not an error condition)
- And the existing queue item remains unchanged
- And a log entry notes: "Index [name] already queued, skipped duplicate"

### Edge Case 6: Zero Items Queued After Configuration Override
- Given a database has 50 fragmented indexes
- When configuration override sets IncludeInMaintenance = 0 for all indexes
- Then all 50 indexes are filtered out
- And ZERO queue items are inserted
- And log entry shows: "Database [name]: 50 indexes excluded by configuration"
- And discovery completes successfully (configuration is working as intended)

### Edge Case 7: SQL Injection via DatabaseName Parameter
- Given a malicious user provides @DatabaseName = "'; DROP TABLE [dbo].[MaintenanceQueue]; --"
- When the procedure builds dynamic SQL using this parameter
- Then QUOTENAME() function is used to properly escape the database name
- And the malicious input becomes the literal string: ['; DROP TABLE [dbo].[MaintenanceQueue]; --]
- And NO database matches this name, result set is empty
- And NO tables are dropped
- And discovery completes safely

### Edge Case 8: Cursor Exhaustion with 1000+ Databases
- Given SQL Server instance with 1000+ user databases
- When discovery procedure opens a FAST_FORWARD cursor over all databases
- Then the cursor maintains reasonable memory footprint (forward-only, read-only)
- And cursor fetches one database at a time (not loading all in memory)
- And no CURSOR_THRESHOLD exceeded errors occur
- And procedure completes successfully

### Edge Case 9: Parameter Validation - Invalid Fragmentation Thresholds
- Given I provide invalid fragmentation parameters
- When @MinFragmentationReorg = 80 and @MinFragmentationRebuild = 50 (inverted)
- Then the procedure validates parameters before execution
- And raises error: "@MinFragmentationRebuild (50) must be >= @MinFragmentationReorg (80)"
- And NO scanning occurs
- And transaction is rolled back to maintain consistency

### Edge Case 10: Conflicting Parameter Values
- Given I provide @MinPageCount = -100 (invalid negative value)
- When the procedure validates parameters
- Then error is raised: "@MinPageCount must be >= 0, provided value: -100"
- And scanning is aborted
- And user receives clear guidance on valid parameter ranges

## Technical Specification

### API Contract (Stored Procedure)

**Procedure Name**: `DBAdmin.dbo.usp_DiscoverIndexFragmentation`

**Signature**:
```sql
CREATE PROCEDURE usp_DiscoverIndexFragmentation
    @DatabaseName NVARCHAR(128) = NULL,              -- Target database or NULL for all
    @MinFragmentationReorg DECIMAL(5,2) = 15.0,      -- Fragmentation % for REORG (default 15%)
    @MinFragmentationRebuild DECIMAL(5,2) = 30.0,    -- Fragmentation % for REBUILD (default 30%)
    @MinPageCount INT = 1000,                        -- Skip indexes with < this page count
    @DryRun BIT = 0,                                 -- 1 = preview only (no INSERT), 0 = insert
    @ExcludeSystemDatabases BIT = 1,                 -- 1 = skip master/model/msdb/tempdb
    @IncludeSingleDBOnly BIT = 0                     -- Internal: controls single-DB behavior
AS
```

**Parameters**:

| Parameter | Type | Default | Required | Validation | Notes |
|-----------|------|---------|----------|-----------|-------|
| @DatabaseName | NVARCHAR(128) | NULL | No | Valid SYSNAME or NULL | If NULL, scans all databases; if specified, scans only that DB |
| @MinFragmentationReorg | DECIMAL(5,2) | 15.0 | No | 0-100, must be <= @MinFragmentationRebuild | Fragmentation threshold to trigger REORG operation |
| @MinFragmentationRebuild | DECIMAL(5,2) | 30.0 | No | 0-100, must be >= @MinFragmentationReorg | Fragmentation threshold to trigger REBUILD operation |
| @MinPageCount | INT | 1000 | No | >= 0 | Minimum page count to include index in discovery (excludes small indexes) |
| @DryRun | BIT | 0 | No | 0 or 1 | If 1, returns result set but does NOT insert into MaintenanceQueue |
| @ExcludeSystemDatabases | BIT | 1 | No | 0 or 1 | If 1, skips master/model/msdb/tempdb; if 0, includes them |
| @IncludeSingleDBOnly | BIT | 0 | No | 0 or 1 | Internal parameter (do not use directly) |

**Return Values**:

```
0 = Success
1 = Validation error (invalid parameters)
2 = Permission error (VIEW SERVER STATE required)
3 = Runtime error (see error message)
```

### Request/Response Examples

**Request 1: Default Discovery**
```sql
EXEC DBAdmin.dbo.usp_DiscoverIndexFragmentation;
```

**Response 1: Success**
```
================================================================================
Index Fragmentation Discovery - DBAdmin
Started: 2025-11-05 14:32:15
================================================================================

Scanning 23 user databases...
Database [ProductionDB]: 145 indexes analyzed, 23 items queued
Database [ReportingDB]: 87 indexes analyzed, 12 items queued
Database [StagingDB]: 23 indexes analyzed, 2 items queued
...

Summary:
  Databases scanned: 23
  Total indexes analyzed: 3,521
  Queue items inserted: 147
  Min fragmentation: 15.2%
  Avg fragmentation: 34.5%
  Max fragmentation: 98.7%
  Duration: 287 seconds

Completion Status: SUCCESS
```

**Request 2: Single Database with Custom Thresholds**
```sql
EXEC DBAdmin.dbo.usp_DiscoverIndexFragmentation
    @DatabaseName = 'ProductionDB',
    @MinFragmentationReorg = 20.0,
    @MinFragmentationRebuild = 40.0;
```

**Request 3: Dry-Run Preview**
```sql
EXEC DBAdmin.dbo.usp_DiscoverIndexFragmentation
    @DryRun = 1;
```

**Response 3: Result Set (not inserted)**
```
QueueID | DatabaseName   | SchemaName | TableName    | IndexName      | PageCount | Fragmentation | Priority | OperationType   | OperationDetails
--------|----------------|-----------|--------------|----------------|-----------|---------------|----------|-----------------|------------------
NULL    | ProductionDB   | dbo       | SalesOrders  | IX_OrderDate   | 45000     | 87.5          | 1        | INDEX_REBUILD   | {"priority_band": "80-100%", ...}
NULL    | ProductionDB   | dbo       | Customers    | PK_Customer    | 12000     | 65.2          | 5        | INDEX_REBUILD   | {"priority_band": "50-79%", ...}
NULL    | ProductionDB   | Sales     | LineItems    | IX_ProductID   | 2500      | 28.4          | 15       | INDEX_REORG     | {"priority_band": "15-29%", ...}
```

**Request 4: Invalid Parameters**
```sql
EXEC DBAdmin.dbo.usp_DiscoverIndexFragmentation
    @MinFragmentationReorg = 50.0,
    @MinFragmentationRebuild = 30.0;  -- Invalid: REBUILD < REORG
```

**Response 4: Error**
```
Msg 50001, Level 16, State 1
@MinFragmentationRebuild (30.0) must be >= @MinFragmentationReorg (50.0)
```

### Data Model

**Input Table: None** (uses DMV sys.dm_db_index_physical_stats)

**Output Table: MaintenanceQueue**

| Column | Type | Example | Notes |
|--------|------|---------|-------|
| QueueID | BIGINT | 1001 | Auto-generated primary key |
| DatabaseName | SYSNAME | 'ProductionDB' | Target database name |
| SchemaName | SYSNAME | 'dbo' | Schema containing table |
| TableName | SYSNAME | 'SalesOrders' | Table containing index |
| IndexName | SYSNAME | 'IX_OrderDate' | Index name (NULL for heaps) |
| OperationType | VARCHAR(50) | 'INDEX_REBUILD' or 'INDEX_REORG' | Maintenance type based on fragmentation |
| Priority | INT | 1-100 | Priority ranking (1=highest) |
| Status | VARCHAR(20) | 'Pending' | Initial status (always Pending) |
| CreatedDate | DATETIME | 2025-11-05 14:32:15 | Auto-populated with GETDATE() |
| ClaimedDate | DATETIME | NULL | Set by queue processor |
| CompletedDate | DATETIME | NULL | Set by queue processor |
| WorkerID | INT | NULL | Worker claiming this item |
| OperationDetails | NVARCHAR(MAX) | JSON | Configuration resolution details |
| ErrorMessage | NVARCHAR(MAX) | NULL | Any processing errors |

**OperationDetails JSON Structure**:
```json
{
  "fragmentation_percent": 87.5,
  "page_count": 45000,
  "priority_band": "80-100%",
  "priority_calculation": "Critical fragmentation level",
  "config_source": "index-level override",
  "min_reorg_threshold": 15.0,
  "min_rebuild_threshold": 30.0,
  "index_type": "NONCLUSTERED",
  "partition_number": 1,
  "data_compression": "PAGE",
  "discovery_timestamp": "2025-11-05T14:32:15.123Z",
  "discovery_run_id": "d4f3f1a5-b2c1-4d8e-a1f2-c3d4e5f6a7b8"
}
```

### Business Rules

1. **Fragmentation Threshold Logic**:
   - If fragmentation >= @MinFragmentationRebuild → OperationType = 'INDEX_REBUILD'
   - Else if fragmentation >= @MinFragmentationReorg → OperationType = 'INDEX_REORG'
   - Else → Index is NOT queued

2. **Heap Exclusion**:
   - Tables without clustered indexes (heaps) have no IndexName
   - Heaps must be completely excluded from discovery (WHERE IndexName IS NOT NULL)

3. **System Database Exclusion**:
   - master, model, msdb, tempdb are excluded by default
   - User must explicitly provide @ExcludeSystemDatabases = 0 to include them

4. **Page Count Minimum**:
   - Indexes with PageCount < @MinPageCount are excluded
   - Default of 1000 pages prevents discovery of trivial indexes
   - Used to balance maintenance effort vs. performance benefit

5. **Priority Calculation**:
   ```
   IF Fragmentation >= 80 → Priority = 1
   ELSE IF Fragmentation >= 50 → Priority = 5
   ELSE IF Fragmentation >= 30 → Priority = 15
   ELSE IF Fragmentation >= 15 → Priority = 30

   Within same band: Priority += (PageCount / 100000) -- Break ties by size
   ```

6. **Configuration Override Resolution**:
   - Applies hierarchical configuration lookup via `fn_ResolveConfiguration()`
   - Resolution order: INDEX > TABLE > DATABASE > SERVER
   - If any level sets `IncludeInMaintenance = 0`, index is excluded
   - Resolution source is recorded in OperationDetails for audit trail

7. **Duplicate Prevention**:
   - MaintenanceQueue has UNIQUE constraint on (DatabaseName, SchemaName, TableName, IndexName, OperationType)
   - If index already queued with same OperationType, duplicate INSERT fails
   - Failure is handled gracefully (logged, not error condition)

8. **Scan Mode**:
   - Uses `sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED')`
   - LIMITED mode: Fast scan, includes partition number and page count only
   - Does NOT include fragmentation data per partition (aggregate only)
   - Performance: ~100-500 databases per minute on average hardware

### Integration Points

**Dependencies**:
- `DBAdmin.dbo.fn_ResolveConfiguration()` - Hierarchical configuration resolution function
- `DBAdmin.dbo.MaintenanceQueue` - Target table for queue items
- `DBAdmin.dbo.MaintenanceLog` - Logging table for discovery metrics
- System DMV: `sys.dm_db_index_physical_stats()` - Fragmentation data source
- System DMV: `sys.databases` - Database listing

**Called By**:
- SQL Agent Job: `DBAdmin.Maintenance.Job_DiscoverIndexFragmentation` (scheduled)
- PowerShell Script: `Invoke-IndexDiscoveryAndMaintenance.ps1`
- Manual execution by DBA via SSMS

**Invokes**:
- Internal: `fn_CalculatePriority()` - Priority calculation logic
- Internal: `fn_ResolveConfiguration()` - Configuration resolution
- Internal: `sp_executesql` - Dynamic SQL for cross-database scanning

### Non-Functional Requirements

**Performance**:
- Scan 200+ databases in < 10 minutes (at 2+ databases per second)
- LIMITED mode queries perform in < 50ms per database on average
- Memory footprint < 100MB regardless of number of databases
- FAST_FORWARD cursor prevents accumulation of full result sets

**Accuracy**:
- Fragmentation calculation must match sys.dm_db_index_physical_stats exactly
- 100% match between analysis and queued items (no missed indexes)
- Duplicate detection ensures no duplicate work queued

**Resilience**:
- Continue scanning even if one database is inaccessible
- Gracefully handle permissions errors, offline databases, timeouts
- Log all errors with sufficient detail for troubleshooting
- Return overall SUCCESS if majority of databases processed

**Observability**:
- Log entry per database with metrics
- Summary log entry at end of discovery run
- OperationDetails includes discovery timestamp and run_id for tracing
- All fragmentation values stored for trend analysis

**Security**:
- QUOTENAME() used to escape all database names (SQL injection prevention)
- No credentials in logs or error messages
- Requires VIEW SERVER STATE permission (minimum required)
- No dynamic SQL that concatenates unescaped user input

**Compatibility**:
- SQL Server 2012 SP3 and later
- All editions (Standard, Enterprise, etc.)
- Availability Group-aware (can skip secondary replicas)
- Both physical and virtual (VMware/Hyper-V) environments

### Implementation Notes

**Algorithm**:

1. **Parameter Validation**:
   - Validate @MinFragmentationRebuild >= @MinFragmentationReorg
   - Validate 0 <= thresholds <= 100
   - Validate @MinPageCount >= 0
   - Validate @DatabaseName is valid SYSNAME or NULL
   - Return error code 1 if validation fails

2. **Database Discovery**:
   - Query sys.databases for ONLINE databases
   - Exclude system databases based on @ExcludeSystemDatabases
   - If @DatabaseName provided, filter to single database
   - Build list with database_id, database_name

3. **Cursor-Based Iteration**:
   - Open FAST_FORWARD cursor over database list
   - For each database, build dynamic SQL query
   - Use sp_executesql to execute in target database context

4. **Fragmentation Analysis** (within dynamic SQL):
   - Query sys.dm_db_index_physical_stats in LIMITED mode
   - Filter: WHERE avg_fragmentation_in_percent >= @MinFragmentationReorg
   - Filter: WHERE page_count >= @MinPageCount
   - Filter: WHERE index_name IS NOT NULL (exclude heaps)
   - Apply configuration overrides via CROSS APPLY fn_ResolveConfiguration()
   - Calculate priority based on fragmentation band

5. **Queue Population**:
   - If @DryRun = 0: INSERT discovered indexes into MaintenanceQueue
   - If @DryRun = 1: SELECT into result set (no INSERT)
   - Handle UNIQUE constraint violations gracefully (log as "already queued")

6. **Error Handling**:
   - TRY/CATCH around each database iteration
   - TRY/CATCH around DMV queries
   - Log database-level errors, continue with next database
   - Track success/failure counts

7. **Logging**:
   - Log entry per database: database_name, indexes_analyzed, items_queued
   - Summary log entry: total_databases, total_indexes, total_items, duration
   - Store run_id (GUID) in OperationDetails for traceability

### Code Standards

- Follow PowerShell community standards for logging
- Use parameterized queries (sp_executesql) for SQL injection prevention
- Include meaningful comments for complex logic
- Use consistent formatting and naming conventions
- Add extended properties for documentation

## Dependencies

**Hard Dependencies** (must exist before this story):
- STORY-000: DBAdmin Database Initialization (MaintenanceQueue table, configuration tables)
- STORY-002: Configuration Resolution Framework (fn_ResolveConfiguration function)

**Soft Dependencies** (helpful but not blocking):
- STORY-003: Maintenance Log Schema (for logging discovery metrics)
- STORY-004: Availability Group Support (fn_IsPreferredMaintenanceReplica)

## Definition of Done

- [ ] T-SQL procedure `usp_DiscoverIndexFragmentation` created and deployed to DBAdmin
- [ ] All acceptance criteria validated and passing
- [ ] Dry-run mode tested with real data (no MaintenanceQueue modifications)
- [ ] Edge cases tested: offline databases, permission errors, timeouts, duplicates
- [ ] Parameter validation working (invalid thresholds rejected)
- [ ] Performance tested: 200+ databases scanned in < 10 minutes
- [ ] SQL injection prevention (QUOTENAME) verified
- [ ] Logging working correctly (MaintenanceLog entries created)
- [ ] Code reviewed by peer (follows project standards)
- [ ] Unit tests passing (dynamic SQL generation, priority calculation)
- [ ] Integration tests passing (MaintenanceQueue populated correctly)
- [ ] Documentation updated (DBAdmin reference guide)
- [ ] Deployed to staging environment
- [ ] QA validation passed

## Implementation Notes

During development, the following decisions were made:

**Decision 1: LIMITED Mode vs SAMPLED Mode**
- Chose LIMITED mode (fast, aggregate only) over SAMPLED (slower, per-partition)
- Rationale: Enterprise environments with 200+ databases need speed over partition-level detail
- SAMPLED mode takes 2-3x longer and provides data rarely used for discovery

**Decision 2: Cursor vs Set-Based Approach**
- Chose cursor for database iteration (sequential FAST_FORWARD)
- Rationale: Dynamic SQL required for cross-database queries; set-based approach would require sp_ineachdb (not available on all versions)
- Cursor used correctly: FAST_FORWARD, read-only, no backward fetch (minimal memory)

**Decision 3: Priority Calculation**
- Chose band-based priority (1, 5, 15, 30) with fragmentation thresholds
- Rationale: Reflects business impact (high fragmentation = higher queue priority)
- Alternative rejected: Time-based priority (would not prioritize performance issues)

**Decision 4: OperationDetails JSON vs Separate Columns**
- Chose JSON for configuration details (keeps MaintenanceQueue schema stable)
- Rationale: Reduces schema changes; configuration can evolve without table modification
- JSON includes: fragmentation %, threshold values, config resolution source, run_id for tracing

**Decisions Made During Implementation** (to be completed by developer):
- *To be filled in during development*

## Files to Create/Modify

**New Files**:
- `/mnt/c/Projects/SQLServer/scripts/TSQL/Maintenance/usp_DiscoverIndexFragmentation.sql` - Main procedure

**Modified Files** (if needed):
- `/mnt/c/Projects/SQLServer/docs/DBAdmin-Database-Reference.md` - Add procedure documentation
- `/mnt/c/Projects/SQLServer/scripts/TSQL/Maintenance/fn_CalculatePriority.sql` - If creating helper function

**Test Files**:
- `/mnt/c/Projects/SQLServer/tests/TSQL/test_usp_DiscoverIndexFragmentation.sql` - Unit/integration tests

## Test Scenarios

### Unit Tests (T-SQL)
```sql
-- Test 1: Parameter validation
EXEC tSQLt.ExpectException;
EXEC DBAdmin.dbo.usp_DiscoverIndexFragmentation
    @MinFragmentationReorg = 50,
    @MinFragmentationRebuild = 30;

-- Test 2: Priority calculation
-- Assert: 87.5% fragmentation results in Priority = 1
-- Assert: 65% fragmentation results in Priority = 5
-- Assert: 28% fragmentation results in Priority = 15

-- Test 3: Dry-run verification
-- Assert: @DryRun = 1 returns result set but does NOT insert rows
-- Assert: MaintenanceQueue row count unchanged after dry-run
```

### Integration Tests
```sql
-- Test 1: Single database scan
-- Setup: Create test database with fragmented indexes
-- Execute: EXEC usp_DiscoverIndexFragmentation @DatabaseName = 'TestDB'
-- Assert: Only TestDB indexes queued
-- Assert: Other databases not scanned

-- Test 2: Duplicate prevention
-- Setup: Queue index 'IX_Test' for database 'TestDB'
-- Execute: Run discovery again
-- Assert: Duplicate INSERT fails (UNIQUE constraint)
-- Assert: Original queue item unchanged

-- Test 3: Large database timeout
-- Setup: Create database with 100,000+ indexes
-- Execute: EXEC usp_DiscoverIndexFragmentation with 300s timeout
-- Assert: Timeout handled gracefully
-- Assert: Partial results logged
```

### Edge Case Tests
```sql
-- Test 1: Database offline
-- Setup: Create test database and set to offline
-- Execute: EXEC usp_DiscoverIndexFragmentation
-- Assert: Offline database skipped
-- Assert: Error logged, other databases processed

-- Test 2: SQL injection prevention
-- Execute: EXEC usp_DiscoverIndexFragmentation
--   @DatabaseName = "'; DROP TABLE [dbo].[MaintenanceQueue]; --"
-- Assert: No tables dropped
-- Assert: No queue items inserted (database not found)

-- Test 3: Configuration override
-- Setup: Configure index to IncludeInMaintenance = 0
-- Execute: EXEC usp_DiscoverIndexFragmentation
-- Assert: Index excluded from discovery
-- Assert: OperationDetails shows config source
```

---

**Story Created**: 2025-11-05
**Last Updated**: 2025-11-05
**Version**: 1.0

**Related Documentation**:
- [DBAdmin Database Reference](/mnt/c/Projects/SQLServer/docs/DBAdmin-Database-Reference.md)
- [MaintenanceQueue Table Definition](/mnt/c/Projects/SQLServer/src/Tables/Core/MaintenanceQueue.sql)
- [Existing Index Population Procedure](/mnt/c/Projects/SQLServer/scripts/backup/TSQL/Maintenance/usp_PopulateIndexQueue.sql)
