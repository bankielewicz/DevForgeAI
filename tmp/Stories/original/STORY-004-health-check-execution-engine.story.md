---
id: STORY-004
title: Health Check Execution Engine - Parallel Execution with Timeout and Retry
epic: EPIC-002
sprint: Sprint-1
status: Backlog
priority: Critical
points: 13
type: Infrastructure
created: 2025-01-15
created_by: DevForgeAI Requirements Analyst
---

# STORY-004: Health Check Execution Engine - Parallel Execution with Timeout and Retry

**Status**: Backlog
**Priority**: Critical
**Story Points**: 13
**Epic**: EPIC-002 (SQL Server Health Checks)
**Sprint**: Sprint-1 (To be assigned)

---

## User Story

As a **DevOps Engineer**,
I want **a parallel health check execution engine that executes 200 endpoint checks concurrently with timeout handling, retry logic, and priority queue management**,
So that **all monitored SQL Server instances are checked within 30 seconds while respecting concurrency limits and ensuring critical endpoints are checked first**.

---

## Acceptance Criteria

### Scenario 1: Parallel Execution with Concurrency Control

**Given** PollingService has 200 configured endpoints
**When** health check polling cycle starts
**Then**:
- Maximum 10 health checks execute concurrently (configurable via SemaphoreSlim)
- Total polling cycle completes in < 30 seconds (for 200 endpoints)
- Per-endpoint execution time averages < 5 seconds
- Concurrency limit prevents database connection exhaustion
- Execution metrics logged: Total cycle time, endpoints checked, failures, retries

**Test Evidence:**
- Load 200 endpoints into test database
- Start polling cycle with concurrency = 10
- Measure total execution time: Assert < 30 seconds
- Verify max concurrent connections: <= 10 (SQL Server DMV: `sys.dm_exec_sessions`)
- Log shows: `[INFO] Health check cycle completed: 200 endpoints, 28.4s total, 10 concurrent, 195 success, 5 failures, 3 retries`

**Performance Calculation:**
- 200 endpoints / 10 concurrent = 20 batches
- 5 seconds average per endpoint * 20 batches = 100 seconds theoretical
- With parallel execution: ~30 seconds actual (some endpoints faster than others)

---

### Scenario 2: Per-Endpoint Timeout Handling

**Given** endpoint configured with 30-second timeout (default)
**When** health check exceeds timeout (e.g., SQL Server unresponsive)
**Then**:
- Health check is cancelled via CancellationTokenSource.CancelAfter
- Timeout error logged: `[WARN] Health check timeout for endpoint {EndpointName} after 30s`
- Result saved with Success=false, ErrorMessage="Operation timed out after 30 seconds"
- No lingering connections (all SqlConnections disposed)
- Timeout does not block other concurrent health checks

**Test Evidence:**
- Create mock endpoint that hangs for 60 seconds
- Configure endpoint timeout = 30 seconds
- Execute health check
- Verify cancellation at 30 seconds (stopwatch.ElapsedMilliseconds ~= 30000ms ± 500ms)
- Database record: Success=false, ErrorMessage contains "timeout"
- SQL Server DMV shows connection closed: `sys.dm_exec_connections` count = 0 for endpoint

**Timeout Configuration (per endpoint):**
- Default: 30 seconds (configurable in Endpoints table: TimeoutSeconds column)
- Range: 5-300 seconds
- Critical endpoints: 10 seconds (fast detection)
- Non-critical: 60 seconds (tolerate slow responses)

---

### Scenario 3: Retry Logic with Exponential Backoff

**Given** endpoint health check fails on first attempt (e.g., transient network error)
**When** health check fails
**Then**:
- Retry N times per endpoint configuration (default 3 attempts)
- Exponential backoff: 1s, 2s, 4s (delay = 2^(attempt-1) seconds)
- All retry attempts complete within total timeout (30s)
- If all retries fail: Result marked as failed, all error messages logged
- If any retry succeeds: Result marked as success, previous errors logged as warnings

**Test Evidence:**
- Mock endpoint fails twice, succeeds on third attempt
- Configure endpoint: MaxRetries=3
- Execute health check
- Verify 3 attempts: Stopwatch shows delays ~1s, ~2s between attempts
- Log shows:
  - `[WARN] Health check failed for endpoint {Name}, attempt 1/3: {Error}`
  - `[WARN] Health check failed for endpoint {Name}, attempt 2/3: {Error}`
  - `[INFO] Health check succeeded for endpoint {Name}, attempt 3/3`
- Database record: Success=true, Attempts=3

**Retry Policy:**
- Default retries: 3
- Configurable per endpoint: 0-5 retries
- Total time = (timeout + sum of backoff delays) * attempts
- Example: 30s timeout, 3 retries = max 90s (if all timeout) + 7s backoff = 97s
- To meet 30s cycle target: Distribute slow endpoints across batches

---

### Scenario 4: Priority Queue for Critical Endpoints

**Given** endpoints configured with priority levels (Critical=1, Normal=2, Low=3)
**When** polling cycle starts
**Then**:
- Critical priority endpoints execute first (before Normal and Low)
- Priority order: Critical → Normal → Low (within concurrency limit)
- Critical endpoints complete within first 10 seconds of cycle
- Low priority endpoints may queue if concurrency limit reached
- Execution order logged: `[INFO] Executing endpoints: 10 Critical, 150 Normal, 40 Low`

**Test Evidence:**
- Configure endpoints:
  - 10 Critical (Priority=1)
  - 150 Normal (Priority=2)
  - 40 Low (Priority=3)
- Start polling cycle
- Verify first 10 checks are all Critical priority
- Measure time to complete Critical endpoints: < 10 seconds
- Log shows priority distribution

**Priority Queue Implementation:**
- Use `PriorityQueue<HealthCheckTask, int>` (C# .NET 8.0)
- Sort by Priority ASC (1=highest), then by LastCheckTimestamp ASC
- Critical endpoints always processed first
- If two endpoints have same priority, oldest check time goes first

---

### Scenario 5: Queue Overflow Handling (Interval Collision)

**Given** previous polling cycle still executing (160 of 200 endpoints complete)
**When** next polling interval arrives (e.g., 60-second interval timer fires)
**Then**:
- New cycle does NOT start (previous cycle still running)
- Warning logged: `[WARN] Previous health check cycle still running (160/200 complete). Queueing next cycle.`
- Queued cycle starts immediately after previous cycle completes
- No health check results dropped
- If queue depth > 2: Log critical warning (system overloaded)

**Test Evidence:**
- Configure polling interval = 60 seconds
- Configure endpoint execution time = 2 seconds each (200 endpoints = 40 seconds total)
- Verify only one cycle runs at a time
- Verify next cycle queued if interval arrives early
- Log shows queueing behavior

**Queue Management:**
- Max queue depth: 2 cycles (current + 1 pending)
- If queue full: Skip new cycle, log critical warning
- Track queue depth metric: `CurrentQueueDepth` (for monitoring)

---

### Scenario 6: Graceful Cancellation During Polling Cycle

**Given** health check cycle executing (50 of 200 endpoints complete)
**When** PollingService receives stop signal (OnStop called)
**Then**:
- CancellationToken propagated to all in-flight health checks
- All in-flight checks complete or cancel within 30 seconds
- Completed check results saved to database
- Cancelled checks NOT saved (no partial results)
- Service logs: `[INFO] Graceful shutdown: 50 checks completed, 150 cancelled`

**Test Evidence:**
- Start 200-endpoint polling cycle
- Call OnStop after 10 seconds (50 endpoints complete)
- Verify CancellationToken.IsCancellationRequested = true
- Database shows 50 records (completed before cancel)
- No records for cancelled checks
- Service stops within 30 seconds

---

### Scenario 7: Bulk Result Persistence (Performance)

**Given** polling cycle completes with 200 health check results
**When** results are persisted to database
**Then**:
- Bulk insert executes in < 100ms (Dapper batch insert)
- Single transaction for all results (atomicity)
- If database write fails: Results logged to file as backup
- Performance logged: `[INFO] Persisted 200 health check results in 87ms`

**Test Evidence:**
- Execute 200 health checks
- Measure bulk insert time: Start stopwatch before insert, stop after commit
- Assert duration < 100ms
- Verify transaction: All 200 records inserted or none (rollback on error)
- Test database failure: Disconnect SQL Server, verify file backup

**Bulk Insert Implementation:**
```csharp
const string sql = @"
    INSERT INTO HealthCheckResults (EndpointId, CheckTimestamp, Success, ResponseTimeMs, ErrorMessage)
    VALUES (@EndpointId, @CheckTimestamp, @Success, @ResponseTimeMs, @ErrorMessage)";

using var transaction = connection.BeginTransaction();
await connection.ExecuteAsync(sql, results, transaction);
transaction.Commit();
```

---

### Scenario 8: Execution Metrics and Logging

**Given** health check cycle executes
**When** cycle completes
**Then**:
- Per-endpoint execution time logged
- Aggregate metrics logged:
  - Total cycle time
  - Endpoints checked
  - Success count
  - Failure count
  - Retry count
  - Average execution time
  - P95 execution time (95th percentile)
- Metrics persisted to HealthCheckMetrics table
- Slow endpoints (> 10 seconds) logged as warnings

**Test Evidence:**
- Execute 200-endpoint cycle
- Verify log contains all metrics
- Database HealthCheckMetrics table has record:
  - CycleTimestamp
  - TotalDurationMs
  - EndpointsChecked
  - SuccessCount
  - FailureCount
  - RetryCount
  - AverageDurationMs
  - P95DurationMs
- Verify slow endpoint warning: `[WARN] Endpoint {Name} took {Duration}ms (> 10s threshold)`

---

### Scenario 9: Error Handling - All Endpoints Fail

**Given** all 200 endpoints fail (e.g., network outage)
**When** polling cycle completes
**Then**:
- All 200 results saved with Success=false
- Critical alert triggered: `[CRITICAL] All health checks failed (0/200 success)`
- Service continues running (does not crash)
- Next polling cycle attempts recovery
- Detailed error breakdown logged (timeout: 150, connection refused: 30, authentication: 20)

**Test Evidence:**
- Configure all endpoints to fail (mock network outage)
- Execute cycle
- Verify 200 failed records in database
- Verify service still running (Get-Service status = Running)
- Verify critical alert logged
- Verify error category breakdown in log

---

### Scenario 10: Configuration Per Endpoint

**Given** endpoints configured with different settings
**When** health check executes for each endpoint
**Then**:
- Timeout setting respected per endpoint (range: 5-300 seconds)
- Retry count respected per endpoint (range: 0-5)
- Priority respected per endpoint (Critical=1, Normal=2, Low=3)
- Custom query executed if configured (default: SELECT @@VERSION)
- Configuration loaded once at cycle start (not per endpoint)

**Test Evidence:**
- Configure endpoints:
  - Endpoint A: Timeout=10s, Retries=1, Priority=1
  - Endpoint B: Timeout=60s, Retries=5, Priority=3
  - Endpoint C: Timeout=30s, Retries=3, Priority=2, CustomQuery="SELECT COUNT(*) FROM sys.databases"
- Execute cycle
- Verify Endpoint A times out at 10s (not default 30s)
- Verify Endpoint B retries 5 times
- Verify Endpoint C executes custom query

**Configuration Schema (Endpoints table):**
```sql
CREATE TABLE Endpoints (
    Id INT PRIMARY KEY IDENTITY,
    Name NVARCHAR(100) NOT NULL,
    ServerName NVARCHAR(100) NOT NULL,
    InstanceName NVARCHAR(50),
    Port INT DEFAULT 1433,
    TimeoutSeconds INT DEFAULT 30,
    MaxRetries INT DEFAULT 3,
    Priority INT DEFAULT 2,  -- 1=Critical, 2=Normal, 3=Low
    CustomQuery NVARCHAR(MAX),  -- NULL = default query
    Enabled BIT DEFAULT 1
);
```

---

## Technical Specification

### Architecture & Dependencies

**Layer**: Application Layer (Use Case Orchestration)
**Component**: `OmniWatchAI.Application.HealthChecks`
**Related Components**:
- Presentation: `PollingService` (invokes orchestrator)
- Domain: `Endpoint`, `HealthCheckResult` (entities)
- Infrastructure: `HealthCheckRepository`, `EndpointRepository` (Dapper)

### File Structure

**Files to Create:**

```
src/OmniWatchAI.Application/HealthChecks/
├── HealthCheckOrchestrator.cs                  # Main orchestrator (AC 1, 5, 6, 8)
├── Execution/
│   ├── HealthCheckExecutor.cs                  # Single endpoint executor (AC 2, 3, 10)
│   ├── HealthCheckExecutionQueue.cs            # Priority queue (AC 4, 5)
│   └── ConcurrencyManager.cs                   # SemaphoreSlim wrapper (AC 1)
├── Metrics/
│   ├── HealthCheckMetrics.cs                   # Metrics model (AC 8)
│   └── MetricsCollector.cs                     # Collects execution metrics (AC 8)
├── Persistence/
│   └── BulkResultPersister.cs                  # Bulk insert (AC 7)
└── Retry/
    ├── RetryPolicy.cs                          # Retry logic (AC 3)
    └── ExponentialBackoffStrategy.cs           # Backoff calculation (AC 3)

src/OmniWatchAI.Domain/Entities/
├── Endpoint.cs                                 # Endpoint entity
├── HealthCheckResult.cs                        # Result entity
└── HealthCheckMetrics.cs                       # Metrics entity

src/OmniWatchAI.Infrastructure/Repositories/
├── HealthCheckRepository.cs                    # Dapper repository (AC 7)
├── EndpointRepository.cs                       # Endpoint config loading (AC 10)
└── MetricsRepository.cs                        # Metrics persistence (AC 8)

tests/UnitTests/
├── HealthCheckOrchestratorTests.cs             # AC 1, 5, 6
├── HealthCheckExecutorTests.cs                 # AC 2, 3, 10
├── HealthCheckExecutionQueueTests.cs           # AC 4, 5
├── RetryPolicyTests.cs                         # AC 3
└── BulkResultPersisterTests.cs                 # AC 7

tests/IntegrationTests/
├── ParallelExecutionTests.cs                   # AC 1 (200 endpoints, 10 concurrent)
├── TimeoutHandlingTests.cs                     # AC 2
├── RetryLogicTests.cs                          # AC 3
├── PriorityQueueTests.cs                       # AC 4
└── BulkPersistenceTests.cs                     # AC 7
```

### API Contract: HealthCheckOrchestrator

**Interface:**

```csharp
public interface IHealthCheckOrchestrator
{
    /// <summary>
    /// Executes health checks for all enabled endpoints.
    /// </summary>
    /// <param name="cancellationToken">Cancellation token for graceful shutdown.</param>
    /// <returns>Metrics for the execution cycle.</returns>
    Task<HealthCheckCycleMetrics> ExecuteAllHealthChecksAsync(CancellationToken cancellationToken);
}
```

**Implementation:**

```csharp
public class HealthCheckOrchestrator : IHealthCheckOrchestrator
{
    private readonly IEndpointRepository _endpointRepository;
    private readonly IHealthCheckExecutor _executor;
    private readonly IHealthCheckExecutionQueue _queue;
    private readonly IConcurrencyManager _concurrencyManager;
    private readonly IBulkResultPersister _persister;
    private readonly IMetricsCollector _metricsCollector;
    private readonly ILogger<HealthCheckOrchestrator> _logger;

    public async Task<HealthCheckCycleMetrics> ExecuteAllHealthChecksAsync(
        CancellationToken cancellationToken)
    {
        var startTime = DateTime.UtcNow;
        var stopwatch = Stopwatch.StartNew();

        // Load all enabled endpoints (AC 10)
        var endpoints = await _endpointRepository.GetEnabledEndpointsAsync();
        _logger.LogInformation("Loaded {Count} enabled endpoints", endpoints.Count);

        // Build priority queue (AC 4)
        _queue.EnqueueEndpoints(endpoints);

        var results = new ConcurrentBag<HealthCheckResult>();
        var tasks = new List<Task>();

        // Execute with concurrency control (AC 1)
        while (_queue.TryDequeue(out var endpoint))
        {
            await _concurrencyManager.WaitAsync(cancellationToken);

            var task = Task.Run(async () =>
            {
                try
                {
                    // Execute single endpoint check (AC 2, 3, 10)
                    var result = await _executor.ExecuteAsync(endpoint, cancellationToken);
                    results.Add(result);
                }
                finally
                {
                    _concurrencyManager.Release();
                }
            }, cancellationToken);

            tasks.Add(task);
        }

        // Wait for all checks to complete (AC 1, 6)
        await Task.WhenAll(tasks);

        stopwatch.Stop();

        // Persist results in bulk (AC 7)
        await _persister.PersistResultsAsync(results.ToList(), cancellationToken);

        // Collect and log metrics (AC 8)
        var metrics = _metricsCollector.CollectMetrics(results, stopwatch.ElapsedMilliseconds);
        await _metricsCollector.PersistMetricsAsync(metrics);

        _logger.LogInformation(
            "Health check cycle completed: {Endpoints} endpoints, {Duration}ms, {Success} success, {Failures} failures, {Retries} retries",
            endpoints.Count,
            stopwatch.ElapsedMilliseconds,
            metrics.SuccessCount,
            metrics.FailureCount,
            metrics.RetryCount);

        return metrics;
    }
}
```

### Data Model: HealthCheckExecutionQueue

**Priority Queue Implementation:**

```csharp
public class HealthCheckExecutionQueue : IHealthCheckExecutionQueue
{
    private readonly PriorityQueue<Endpoint, int> _queue;
    private readonly ILogger<HealthCheckExecutionQueue> _logger;

    public HealthCheckExecutionQueue(ILogger<HealthCheckExecutionQueue> logger)
    {
        _queue = new PriorityQueue<Endpoint, int>();
        _logger = logger;
    }

    public void EnqueueEndpoints(List<Endpoint> endpoints)
    {
        // Sort by Priority (1=highest), then LastCheckTimestamp (oldest first)
        var sortedEndpoints = endpoints
            .OrderBy(e => e.Priority)
            .ThenBy(e => e.LastCheckTimestamp);

        foreach (var endpoint in sortedEndpoints)
        {
            _queue.Enqueue(endpoint, endpoint.Priority);
        }

        _logger.LogInformation(
            "Enqueued {Count} endpoints: {Critical} Critical, {Normal} Normal, {Low} Low",
            endpoints.Count,
            endpoints.Count(e => e.Priority == 1),
            endpoints.Count(e => e.Priority == 2),
            endpoints.Count(e => e.Priority == 3));
    }

    public bool TryDequeue(out Endpoint endpoint)
    {
        return _queue.TryDequeue(out endpoint, out _);
    }
}
```

### Concurrency Control: SemaphoreSlim

**Implementation:**

```csharp
public class ConcurrencyManager : IConcurrencyManager
{
    private readonly SemaphoreSlim _semaphore;
    private readonly int _maxConcurrency;

    public ConcurrencyManager(int maxConcurrency = 10)
    {
        _maxConcurrency = maxConcurrency;
        _semaphore = new SemaphoreSlim(maxConcurrency, maxConcurrency);
    }

    public Task WaitAsync(CancellationToken cancellationToken)
    {
        return _semaphore.WaitAsync(cancellationToken);
    }

    public void Release()
    {
        _semaphore.Release();
    }

    public void Dispose()
    {
        _semaphore?.Dispose();
    }
}
```

### Timeout Handling: CancellationTokenSource

**Implementation:**

```csharp
public class HealthCheckExecutor : IHealthCheckExecutor
{
    public async Task<HealthCheckResult> ExecuteAsync(
        Endpoint endpoint,
        CancellationToken cancellationToken)
    {
        using var timeoutCts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        timeoutCts.CancelAfter(TimeSpan.FromSeconds(endpoint.TimeoutSeconds));

        var stopwatch = Stopwatch.StartNew();

        try
        {
            // Execute health check with timeout and retry
            var result = await ExecuteWithRetryAsync(endpoint, timeoutCts.Token);
            stopwatch.Stop();

            result.ResponseTimeMs = (int)stopwatch.ElapsedMilliseconds;
            return result;
        }
        catch (OperationCanceledException) when (timeoutCts.Token.IsCancellationRequested)
        {
            _logger.LogWarning(
                "Health check timeout for endpoint {Name} after {Timeout}s",
                endpoint.Name,
                endpoint.TimeoutSeconds);

            return new HealthCheckResult
            {
                EndpointId = endpoint.Id,
                CheckTimestamp = DateTime.UtcNow,
                Success = false,
                ResponseTimeMs = (int)stopwatch.ElapsedMilliseconds,
                ErrorMessage = $"Operation timed out after {endpoint.TimeoutSeconds} seconds"
            };
        }
    }

    private async Task<HealthCheckResult> ExecuteWithRetryAsync(
        Endpoint endpoint,
        CancellationToken cancellationToken)
    {
        var retryPolicy = new RetryPolicy(endpoint.MaxRetries);

        return await retryPolicy.ExecuteAsync(async (attempt) =>
        {
            try
            {
                return await CheckConnectionAsync(endpoint, cancellationToken);
            }
            catch (Exception ex) when (attempt < endpoint.MaxRetries)
            {
                _logger.LogWarning(
                    ex,
                    "Health check failed for endpoint {Name}, attempt {Attempt}/{Max}: {Error}",
                    endpoint.Name,
                    attempt,
                    endpoint.MaxRetries,
                    ex.Message);

                // Exponential backoff: 1s, 2s, 4s
                var delay = TimeSpan.FromSeconds(Math.Pow(2, attempt - 1));
                await Task.Delay(delay, cancellationToken);

                throw;  // Retry
            }
        });
    }

    private async Task<HealthCheckResult> CheckConnectionAsync(
        Endpoint endpoint,
        CancellationToken cancellationToken)
    {
        var connectionString = BuildConnectionString(endpoint);
        using var connection = new SqlConnection(connectionString);

        await connection.OpenAsync(cancellationToken);

        // Execute query (default or custom)
        var query = endpoint.CustomQuery ?? "SELECT @@VERSION";
        var result = await connection.ExecuteScalarAsync<string>(query);

        return new HealthCheckResult
        {
            EndpointId = endpoint.Id,
            CheckTimestamp = DateTime.UtcNow,
            Success = true,
            ResponseTimeMs = 0  // Set by caller
        };
    }
}
```

### Retry Policy: Exponential Backoff

**Implementation:**

```csharp
public class RetryPolicy
{
    private readonly int _maxRetries;

    public RetryPolicy(int maxRetries)
    {
        _maxRetries = maxRetries;
    }

    public async Task<HealthCheckResult> ExecuteAsync(
        Func<int, Task<HealthCheckResult>> action)
    {
        Exception lastException = null;

        for (int attempt = 1; attempt <= _maxRetries; attempt++)
        {
            try
            {
                return await action(attempt);
            }
            catch (Exception ex)
            {
                lastException = ex;

                if (attempt == _maxRetries)
                {
                    // All retries exhausted
                    throw;
                }

                // Continue to next retry
            }
        }

        // Should never reach here
        throw lastException;
    }
}
```

### Bulk Result Persistence: Dapper Batch Insert

**Implementation:**

```csharp
public class BulkResultPersister : IBulkResultPersister
{
    private readonly ISqlConnectionFactory _connectionFactory;
    private readonly ILogger<BulkResultPersister> _logger;

    public async Task PersistResultsAsync(
        List<HealthCheckResult> results,
        CancellationToken cancellationToken)
    {
        const string sql = @"
            INSERT INTO HealthCheckResults (EndpointId, CheckTimestamp, Success, ResponseTimeMs, ErrorMessage)
            VALUES (@EndpointId, @CheckTimestamp, @Success, @ResponseTimeMs, @ErrorMessage)";

        var stopwatch = Stopwatch.StartNew();

        using var connection = _connectionFactory.CreateConnection();
        connection.Open();
        using var transaction = connection.BeginTransaction();

        try
        {
            await connection.ExecuteAsync(sql, results, transaction);
            transaction.Commit();

            stopwatch.Stop();

            _logger.LogInformation(
                "Persisted {Count} health check results in {Duration}ms",
                results.Count,
                stopwatch.ElapsedMilliseconds);
        }
        catch (Exception ex)
        {
            transaction.Rollback();
            _logger.LogError(ex, "Failed to persist health check results to database");

            // Backup to file (AC 7)
            await BackupResultsToFileAsync(results);

            throw;
        }
    }

    private async Task BackupResultsToFileAsync(List<HealthCheckResult> results)
    {
        var fileName = $"healthcheck-results-{DateTime.UtcNow:yyyyMMddHHmmss}.json";
        var filePath = Path.Combine("C:\\OmniWatchAI\\Backup", fileName);

        var json = JsonSerializer.Serialize(results, new JsonSerializerOptions { WriteIndented = true });
        await File.WriteAllTextAsync(filePath, json);

        _logger.LogWarning("Health check results backed up to file: {FilePath}", filePath);
    }
}
```

### Metrics Model

**Entity:**

```csharp
public class HealthCheckCycleMetrics
{
    public DateTime CycleTimestamp { get; set; }
    public long TotalDurationMs { get; set; }
    public int EndpointsChecked { get; set; }
    public int SuccessCount { get; set; }
    public int FailureCount { get; set; }
    public int RetryCount { get; set; }
    public double AverageDurationMs { get; set; }
    public long P95DurationMs { get; set; }
    public int ConcurrencyLimit { get; set; }
}
```

**Database Schema:**

```sql
CREATE TABLE HealthCheckMetrics (
    Id INT PRIMARY KEY IDENTITY,
    CycleTimestamp DATETIME2 NOT NULL,
    TotalDurationMs BIGINT NOT NULL,
    EndpointsChecked INT NOT NULL,
    SuccessCount INT NOT NULL,
    FailureCount INT NOT NULL,
    RetryCount INT NOT NULL,
    AverageDurationMs FLOAT NOT NULL,
    P95DurationMs BIGINT NOT NULL,
    ConcurrencyLimit INT NOT NULL,
    CreatedAt DATETIME2 DEFAULT GETUTCDATE()
);
```

### Business Rules

1. **Concurrency Limit:** Max 10 concurrent health checks (configurable)
2. **Total Cycle Time:** < 30 seconds for 200 endpoints
3. **Per-Endpoint Timeout:** Default 30 seconds (configurable per endpoint: 5-300s)
4. **Retry Attempts:** Default 3 (configurable per endpoint: 0-5)
5. **Exponential Backoff:** Delay = 2^(attempt-1) seconds (1s, 2s, 4s, 8s, 16s)
6. **Priority Order:** Critical (1) → Normal (2) → Low (3)
7. **Queue Depth:** Max 2 pending cycles (current + 1 queued)
8. **Bulk Insert Time:** < 100ms for 200 results
9. **Execution Metrics:** Logged and persisted per cycle
10. **Graceful Shutdown:** All in-flight checks complete or cancel within 30 seconds

### Non-Functional Requirements

**Performance:**
- Total polling cycle: < 30 seconds (200 endpoints, 10 concurrent)
- Per-endpoint execution: < 5 seconds average
- Bulk insert: < 100ms (200 results)
- Memory usage: < 500 MB during full cycle execution
- CPU usage: < 50% on polling service host

**Reliability:**
- Retry logic handles transient failures
- Timeout prevents hanging operations
- Bulk persistence ensures atomicity (all-or-nothing)
- File backup if database write fails
- Graceful shutdown prevents data loss

**Scalability:**
- Support 51-200 endpoints
- Configurable concurrency (10 default, max 50)
- Priority queue handles varying endpoint counts
- Queue management prevents overload

**Concurrency:**
- SemaphoreSlim controls max concurrent connections
- Prevents database connection pool exhaustion
- Prevents monitored server overload
- Thread-safe result collection (ConcurrentBag)

**Monitoring:**
- Per-cycle metrics logged and persisted
- Slow endpoints flagged (> 10 seconds)
- Retry counts tracked
- Timeout counts tracked
- Error categorization (timeout, connection, authentication)

---

## Implementation Notes

### Technology Decisions

**Concurrency Control:** SemaphoreSlim
- .NET built-in, async-friendly
- Limits concurrent health checks to prevent connection exhaustion
- Configurable limit (default 10)

**Priority Queue:** PriorityQueue<T, TPriority> (.NET 8.0)
- Native priority queue (no external library)
- Efficient enqueue/dequeue operations
- Stable sort by priority

**Parallel Execution:** Task.WhenAll
- Executes health checks concurrently
- Respects cancellation tokens
- Collects results in thread-safe collection (ConcurrentBag)

**Timeout Handling:** CancellationTokenSource.CancelAfter
- Per-endpoint timeout configuration
- Cancels long-running operations
- Propagates cancellation to SqlConnection

**Retry Logic:** Custom RetryPolicy
- Exponential backoff strategy
- Configurable max retries per endpoint
- Logs all retry attempts

**Bulk Persistence:** Dapper ExecuteAsync with transaction
- Single transaction for atomicity
- Batch insert for performance
- Rollback on failure

### Code Patterns to Follow

**All code must follow coding-standards.md:**
- Constructor injection for all dependencies
- Async all the way (ConfigureAwait(false) in Application layer)
- Structured logging (no string interpolation)
- Specific exception handling (SqlException, OperationCanceledException)
- Fail fast validation

**Repository Pattern:**
- All data access via IEndpointRepository, IHealthCheckRepository
- No direct SqlConnection in orchestrator
- Dapper for all queries (not EF Core)

**Clean Architecture:**
- Orchestrator in Application layer
- Entities in Domain layer
- Repositories in Infrastructure layer
- No domain references in orchestrator (use DTOs)

### Testing Strategy

**Unit Tests** (xUnit + Moq):
- Mock IEndpointRepository, IHealthCheckExecutor, IHealthCheckExecutionQueue
- Test concurrency limit (10 tasks max at once)
- Test timeout handling (verify CancellationToken propagation)
- Test retry logic (verify 3 attempts, exponential backoff)
- Test priority queue ordering
- Test graceful cancellation
- Test metrics collection

**Integration Tests** (xUnit + Testcontainers):
- Real SQL Server database (Docker container)
- 200 endpoints in test database
- Measure total cycle time (< 30s)
- Verify max 10 concurrent connections (query sys.dm_exec_sessions)
- Test timeout with slow endpoint
- Test retry with transient failure
- Test bulk insert performance (< 100ms)

**Performance Tests:**
- Load test: 200 endpoints, 10 concurrent
- Measure cycle time under load
- Measure memory usage
- Measure CPU usage
- Verify concurrency limit

### Edge Cases

**1. Endpoint Hangs Indefinitely:**
- Timeout via CancellationTokenSource.CancelAfter
- Result saved with timeout error message
- No lingering connections

**2. All Health Checks Fail:**
- All 200 results saved with Success=false
- Critical alert logged
- Service continues running
- Next cycle attempts recovery

**3. Database Write Fails:**
- Transaction rollback
- Results backed up to JSON file
- Service logs error
- Next cycle continues

**4. Memory Pressure (200+ Concurrent):**
- SemaphoreSlim limits to 10 concurrent (prevents memory exhaustion)
- ConcurrentBag uses efficient memory allocation
- Results persisted immediately (not held in memory)

**5. Slow Endpoint (> 30s):**
- Timeout cancels operation
- Result marked as failed
- Other endpoints not blocked (parallel execution)

**6. Service Stop During Cycle:**
- CancellationToken propagated to all tasks
- In-flight checks complete or cancel
- Completed results saved before exit

**7. Configuration Change Mid-Cycle:**
- Cycle uses snapshot loaded at start
- Next cycle loads new configuration
- No mid-cycle reloads

**8. Priority Queue Empty:**
- TryDequeue returns false
- No crash (graceful handling)
- Cycle completes with 0 endpoints

**9. Retry Exceeds Total Timeout:**
- Total timeout = endpoint timeout * max retries + backoff delays
- If exceeded: Cancel remaining retries
- Result marked as failed

**10. Concurrent Cycles (Queue Overflow):**
- Max 2 cycles queued (current + 1 pending)
- Third cycle skipped, critical warning logged
- Indicates system overload

### Compliance Checklist

- [ ] Clean Architecture (Application layer orchestration)
- [ ] No business logic in PollingService (delegate to orchestrator)
- [ ] All dependencies injected (no direct instantiation)
- [ ] Async/await throughout (ConfigureAwait(false))
- [ ] Structured logging (not string interpolation)
- [ ] Parameterized SQL (Dapper repositories)
- [ ] Specific exception handling (SqlException, OperationCanceledException)
- [ ] CancellationToken support for graceful shutdown
- [ ] SemaphoreSlim for concurrency control
- [ ] PriorityQueue for critical endpoint prioritization
- [ ] 95% unit test coverage (business logic)
- [ ] No forbidden anti-patterns (god objects, static mutable state)

---

## Dependencies

**Hard Dependencies (Must Complete First):**
- STORY-001: Windows Service Framework (PollingService lifecycle)
- STORY-003: Configuration Management (endpoint configuration loading)

**Soft Dependencies (Should Complete First):**
- None (foundational story for health checks)

**External Dependencies:**
- SQL Server 2022 database
- Network connectivity to monitored SQL Server instances
- Service account with database access

---

## Definition of Done

**Code Implementation:**
- [ ] HealthCheckOrchestrator.cs implements ExecuteAllHealthChecksAsync
- [ ] HealthCheckExecutor.cs implements single endpoint execution with timeout and retry
- [ ] HealthCheckExecutionQueue.cs implements priority queue
- [ ] ConcurrencyManager.cs wraps SemaphoreSlim (max 10 concurrent)
- [ ] RetryPolicy.cs implements exponential backoff
- [ ] BulkResultPersister.cs implements bulk insert (< 100ms)
- [ ] MetricsCollector.cs collects and persists execution metrics
- [ ] EndpointRepository.cs loads enabled endpoints with configuration
- [ ] HealthCheckRepository.cs persists results
- [ ] All interfaces defined in Domain layer

**Testing:**
- [ ] Unit tests: HealthCheckOrchestrator (concurrency, cancellation, queueing)
- [ ] Unit tests: HealthCheckExecutor (timeout, retry, error handling)
- [ ] Unit tests: HealthCheckExecutionQueue (priority ordering)
- [ ] Unit tests: RetryPolicy (exponential backoff calculation)
- [ ] Unit tests: BulkResultPersister (transaction, rollback)
- [ ] Integration tests: 200 endpoints, 10 concurrent, < 30s total
- [ ] Integration tests: Timeout handling (verify 30s cancellation)
- [ ] Integration tests: Retry logic (verify 3 attempts, backoff delays)
- [ ] Integration tests: Priority queue (Critical first, then Normal, then Low)
- [ ] Integration tests: Bulk insert performance (< 100ms)
- [ ] Integration tests: Graceful cancellation (in-flight checks complete)
- [ ] Coverage: >= 95% for business logic, >= 85% for application layer
- [ ] All tests pass (100% pass rate)

**Quality Gates:**
- [ ] No violations of architecture-constraints.md (orchestrator in Application layer)
- [ ] No violations of coding-standards.md (naming, logging, DI, error handling)
- [ ] No violations of anti-patterns.md (no god objects, no direct instantiation, etc.)
- [ ] Code review approved
- [ ] No CRITICAL or HIGH severity issues from static analysis

**Documentation:**
- [ ] Code comments for complex logic (retry backoff, priority queue, timeout handling)
- [ ] API documentation (XML comments for IHealthCheckOrchestrator)
- [ ] Configuration documentation (endpoint timeout, retries, priority)
- [ ] Metrics documentation (cycle time, P95, success rate)

**Database:**
- [ ] HealthCheckMetrics table created (EF Core migration)
- [ ] Endpoints table updated with timeout, retry, priority columns
- [ ] HealthCheckResults table has indexes for performance

**Performance:**
- [ ] 200 endpoints complete in < 30 seconds (verified via integration test)
- [ ] Bulk insert completes in < 100ms (verified via integration test)
- [ ] Max 10 concurrent connections (verified via SQL Server DMV)
- [ ] Memory usage < 500 MB during full cycle

**Configuration:**
- [ ] appsettings.json has concurrency limit (default 10)
- [ ] appsettings.json has default timeout (30 seconds)
- [ ] appsettings.json has default retries (3)
- [ ] Endpoint configuration supports per-endpoint overrides

---

## Implementation Notes (To be completed during development)

<!-- This section will be filled in by devforgeai-development skill during implementation -->
<!-- Developer will document: DoD status, implementation decisions, files created, test results, AC verification -->

*To be completed during development*

---

## QA Validation History

<!-- This section tracks QA validation attempts and results -->

| Attempt | Mode | Status | Issues | Notes |
|---------|------|--------|--------|-------|
| - | - | Pending | - | Awaiting development |

---

## Related Stories

**Predecessor Stories** (must complete first):
- STORY-001: Windows Service Framework - PollingService Lifecycle Management
- STORY-003: Configuration Management - Database-Driven Settings

**Successor Stories** (depend on this story):
- STORY-005: Connection Availability Checks (uses orchestrator)
- STORY-006: Query Response Time Monitoring (uses orchestrator)
- STORY-007: Database Status Checks (uses orchestrator)
- STORY-008: Resource Metrics Collection (uses orchestrator)

**Related Stories** (work together):
- STORY-002: AlertingService Framework (consumes health check results)

---

## Story Metrics

**Estimation Breakdown:**
- Orchestrator setup: 2 points
- Concurrency control (SemaphoreSlim): 2 points
- Timeout handling (CancellationTokenSource): 2 points
- Retry logic (exponential backoff): 2 points
- Priority queue implementation: 2 points
- Bulk persistence (Dapper): 1 point
- Metrics collection and logging: 2 points

**Total: 13 story points (estimated 5-7 days for experienced .NET developer)**

---

## Acceptance Criteria Summary

**Must Have (All 10 ACs must pass):**

1. Parallel execution with 10 concurrent limit (< 30s for 200 endpoints)
2. Per-endpoint timeout handling (default 30s, configurable)
3. Retry logic with exponential backoff (3 attempts default)
4. Priority queue for critical endpoints (Critical → Normal → Low)
5. Queue overflow handling (max 2 pending cycles)
6. Graceful cancellation during polling cycle (30s timeout)
7. Bulk result persistence (< 100ms for 200 results)
8. Execution metrics and logging (cycle time, success/failure counts)
9. Error handling for all endpoints failing
10. Configuration per endpoint (timeout, retries, priority)

**All acceptance criteria MUST be validated via automated tests and integration tests with 200 real endpoints.**

---

**Story Owner:** [TBD]
**Last Updated:** 2025-01-15
**Created By:** DevForgeAI Requirements Analyst
