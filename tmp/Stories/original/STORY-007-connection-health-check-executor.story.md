---
id: STORY-007
title: SQL Server Connection Health Check Executor
epic: EPIC-001
sprint: Backlog
status: Backlog
priority: High
points: 8
type: Infrastructure
created: 2025-01-15
created_by: DevForgeAI Requirements Analyst
---

# STORY-007: SQL Server Connection Health Check Executor

**Status**: Backlog
**Priority**: High
**Story Points**: 8
**Epic**: EPIC-001 (Core Monitoring Infrastructure)
**Sprint**: Backlog (To be assigned)

---

## User Story

As a **DevOps Engineer**,
I want **a connection health check executor that tests SQL Server connectivity, measures response time, and handles timeout/authentication/network failures with retry logic**,
So that **I can quickly detect SQL Server availability issues across 51-200 monitored instances and receive actionable alerts when connections fail**.

---

## Acceptance Criteria

### Scenario 1: Successful Connection to Accessible SQL Server

**Given** an endpoint configured with valid Windows Authentication credentials
**And** SQL Server instance is online and accessible
**When** connection health check executes
**Then**:
- SqlConnection.OpenAsync succeeds within 5 seconds
- Response time measured in milliseconds (connection establishment duration)
- HealthCheckResult saved with Success=true
- Response time logged: `[INFO] Connection check succeeded for {EndpointName}: {ResponseTimeMs}ms`
- No credentials logged (security requirement)

**Test Evidence:**
```csharp
// Arrange: Configure endpoint with Windows Authentication
var endpoint = new Endpoint
{
    Name = "PROD-SQL01",
    ServerName = "sql-prod-01.domain.local",
    InstanceName = null,  // Default instance
    Port = 1433,
    UseWindowsAuthentication = true,
    ConnectionString = "Server=sql-prod-01.domain.local;Integrated Security=true;TrustServerCertificate=true;Connection Timeout=30"
};

// Act: Execute connection check
var executor = new ConnectionCheckExecutor(logger, options);
var result = await executor.ExecuteAsync(endpoint, CancellationToken.None);

// Assert: Verify success
result.Success.Should().BeTrue();
result.ResponseTimeMs.Should().BeLessThan(5000);  // < 5 seconds
result.ErrorMessage.Should().BeNull();
result.EndpointId.Should().Be(endpoint.Id);
result.CheckTimestamp.Should().BeCloseTo(DateTime.UtcNow, TimeSpan.FromSeconds(2));

// Assert: Verify logging (no credentials)
_loggerMock.VerifyLog(LogLevel.Information, "Connection check succeeded", Times.Once());
_loggerMock.VerifyLog(logger => !logger.Contains("password"), Times.Always());
```

**Performance Target:**
- Connection establishment: < 2 seconds (typical)
- Maximum allowed: < 5 seconds (timeout threshold)
- Network latency included in response time

---

### Scenario 2: Connection Timeout Handling (SQL Server Unreachable)

**Given** endpoint configured with 30-second timeout (default)
**And** SQL Server instance is offline or network unreachable
**When** connection health check executes
**Then**:
- SqlConnection.OpenAsync throws SqlException after 30 seconds
- Timeout detected via exception handling (SqlException.Number = -1)
- HealthCheckResult saved with Success=false, ErrorMessage="Connection timeout after 30 seconds"
- Response time = timeout duration (~30000ms)
- Warning logged: `[WARN] Connection timeout for {EndpointName} after 30s`
- SqlConnection disposed (no lingering connections)

**Test Evidence:**
```csharp
// Arrange: Configure endpoint with unreachable server
var endpoint = new Endpoint
{
    Name = "UNREACHABLE-SQL",
    ServerName = "192.168.255.255",  // Non-routable IP (timeout guaranteed)
    Port = 1433,
    UseWindowsAuthentication = true,
    ConnectionString = "Server=192.168.255.255;Integrated Security=true;Connection Timeout=30"
};

// Act: Execute with timeout
var stopwatch = Stopwatch.StartNew();
var result = await executor.ExecuteAsync(endpoint, CancellationToken.None);
stopwatch.Stop();

// Assert: Verify timeout
result.Success.Should().BeFalse();
result.ErrorMessage.Should().Contain("timeout");
result.ResponseTimeMs.Should().BeGreaterThanOrEqualTo(29000);  // ~30s ± 1s
result.ResponseTimeMs.Should().BeLessThan(32000);
stopwatch.ElapsedMilliseconds.Should().BeCloseTo(30000, 2000);

// Assert: Verify no lingering connections
using var connection = new SqlConnection(monitoringDbConnectionString);
connection.Open();
var activeConnections = await connection.QueryAsync<int>(
    "SELECT COUNT(*) FROM sys.dm_exec_connections WHERE client_net_address = @IP",
    new { IP = GetLocalIP() });
activeConnections.Should().Be(0);  // No connections to unreachable server
```

**Timeout Configuration:**
- Default: 30 seconds (configurable per endpoint)
- Range: 5-300 seconds (validation required)
- Critical endpoints: 10 seconds (fast failure detection)
- Non-critical: 60 seconds (tolerate slower networks)

---

### Scenario 3: Authentication Failure Handling (Invalid Credentials)

**Given** endpoint configured with SQL Authentication and invalid credentials
**When** connection health check executes
**Then**:
- SqlConnection.OpenAsync throws SqlException (Number = 18456: "Login failed for user")
- Authentication error detected via exception number
- HealthCheckResult saved with Success=false, ErrorMessage="Authentication failed: Login failed for user 'sa'"
- No retry attempted (authentication errors are not transient)
- Error logged: `[ERROR] Authentication failed for {EndpointName}: {ErrorMessage}`
- Invalid credentials NOT logged (security requirement)

**Test Evidence:**
```csharp
// Arrange: Configure endpoint with invalid SQL credentials
var endpoint = new Endpoint
{
    Name = "SQL-AUTH-FAIL",
    ServerName = "sql-test-01.domain.local",
    Port = 1433,
    UseWindowsAuthentication = false,
    SqlUsername = "sa",
    SqlPassword = "WRONG_PASSWORD",  // Invalid password
    ConnectionString = "Server=sql-test-01.domain.local;User Id=sa;Password=WRONG_PASSWORD;Connection Timeout=30"
};

// Act: Execute connection check
var result = await executor.ExecuteAsync(endpoint, CancellationToken.None);

// Assert: Verify authentication failure
result.Success.Should().BeFalse();
result.ErrorMessage.Should().Contain("Authentication failed");
result.ErrorMessage.Should().Contain("Login failed");
result.ResponseTimeMs.Should().BeLessThan(5000);  // Fast fail (no timeout)

// Assert: Verify no credentials logged
_loggerMock.VerifyLog(LogLevel.Error, Times.Once());
_loggerMock.VerifyLog(logger => !logger.Contains("WRONG_PASSWORD"), Times.Always());
_loggerMock.VerifyLog(logger => !logger.Contains("sa"), Times.Never());  // Don't log username

// Assert: No retry attempted (authentication failures are not transient)
_loggerMock.VerifyLog(logger => logger.Contains("attempt"), Times.Never());
```

**Authentication Error Codes (SqlException.Number):**
- 18456: Login failed for user
- 18452: Login failed (SQL Server authentication not enabled)
- 18451: Login failed (password expired)
- All authentication errors: No retry, immediate failure

---

### Scenario 4: Network Failure Handling (Firewall, DNS, Routing)

**Given** endpoint with valid configuration but network-level failure
**When** connection health check executes
**Then**:
- SqlException thrown with network-specific error
- Network error categorized: DNS failure, connection refused, host unreachable
- HealthCheckResult saved with Success=false, ErrorMessage includes network error category
- Retry logic executed (network errors are transient)
- All retry attempts logged

**Test Evidence:**
```csharp
// Test Case 1: DNS Failure
var endpointDns = new Endpoint
{
    Name = "DNS-FAIL",
    ServerName = "nonexistent-sql-server.invalid",  // Invalid DNS name
    Port = 1433,
    ConnectionString = "Server=nonexistent-sql-server.invalid;Integrated Security=true;Connection Timeout=10"
};

var resultDns = await executor.ExecuteAsync(endpointDns, CancellationToken.None);
resultDns.Success.Should().BeFalse();
resultDns.ErrorMessage.Should().Contain("DNS");

// Test Case 2: Connection Refused (Port Closed)
var endpointRefused = new Endpoint
{
    Name = "PORT-CLOSED",
    ServerName = "sql-test-01.domain.local",
    Port = 9999,  // SQL Server not listening on this port
    ConnectionString = "Server=sql-test-01.domain.local,9999;Integrated Security=true;Connection Timeout=10"
};

var resultRefused = await executor.ExecuteAsync(endpointRefused, CancellationToken.None);
resultRefused.Success.Should().BeFalse();
resultRefused.ErrorMessage.Should().Contain("refused");

// Test Case 3: Host Unreachable (Firewall Blocking)
var endpointFirewall = new Endpoint
{
    Name = "FIREWALL-BLOCKED",
    ServerName = "192.168.1.100",  // Firewall blocks this IP
    Port = 1433,
    ConnectionString = "Server=192.168.1.100;Integrated Security=true;Connection Timeout=30"
};

var resultFirewall = await executor.ExecuteAsync(endpointFirewall, CancellationToken.None);
resultFirewall.Success.Should().BeFalse();
resultFirewall.ErrorMessage.Should().MatchRegex("unreachable|timeout|refused");
```

**Network Error Categories:**
- **DNS Failure:** "No such host is known" (SqlException inner exception)
- **Connection Refused:** "No connection could be made because the target machine actively refused it"
- **Host Unreachable:** "A connection attempt failed because the connected party did not properly respond"
- **Timeout:** SqlException.Number = -1 (see Scenario 2)

---

### Scenario 5: Retry Logic Execution with Exponential Backoff

**Given** endpoint configured with 3 retry attempts (default)
**And** connection fails on first 2 attempts (transient network error)
**And** connection succeeds on 3rd attempt
**When** connection health check executes
**Then**:
- Attempt 1: Fails, wait 1 second (2^0 = 1)
- Attempt 2: Fails, wait 2 seconds (2^1 = 2)
- Attempt 3: Succeeds
- Total execution time: ~3 seconds + response time
- HealthCheckResult saved with Success=true, Attempts=3
- All retry attempts logged

**Test Evidence:**
```csharp
// Arrange: Mock connection that fails twice, succeeds third time
var attemptCount = 0;
var mockConnectionFactory = new Mock<ISqlConnectionFactory>();
mockConnectionFactory
    .Setup(f => f.CreateConnection(It.IsAny<string>()))
    .Returns(() =>
    {
        attemptCount++;
        if (attemptCount <= 2)
        {
            // Simulate transient network failure
            throw new SqlException("Transient network error", null, null);
        }
        // Third attempt succeeds
        return new SqlConnection(validConnectionString);
    });

var endpoint = new Endpoint
{
    Name = "RETRY-TEST",
    ServerName = "sql-test-01.domain.local",
    MaxRetries = 3,
    ConnectionString = validConnectionString
};

// Act: Execute with retry
var stopwatch = Stopwatch.StartNew();
var result = await executor.ExecuteAsync(endpoint, CancellationToken.None);
stopwatch.Stop();

// Assert: Verify retry behavior
result.Success.Should().BeTrue();
result.Attempts.Should().Be(3);

// Verify exponential backoff delays: 1s + 2s = 3s minimum
stopwatch.ElapsedMilliseconds.Should().BeGreaterThanOrEqualTo(3000);
stopwatch.ElapsedMilliseconds.Should().BeLessThan(5000);  // 3s + connection time

// Verify logging for each attempt
_loggerMock.VerifyLog(LogLevel.Warning, "attempt 1/3", Times.Once());
_loggerMock.VerifyLog(LogLevel.Warning, "attempt 2/3", Times.Once());
_loggerMock.VerifyLog(LogLevel.Information, "succeeded", Times.Once());
```

**Retry Policy:**
- **Default Retries:** 3 attempts (configurable per endpoint: 0-5)
- **Backoff Formula:** Delay = 2^(attempt-1) seconds
  - Attempt 1: 0s delay (immediate)
  - Attempt 2: 1s delay (2^0)
  - Attempt 3: 2s delay (2^1)
  - Attempt 4: 4s delay (2^2)
  - Attempt 5: 8s delay (2^3)
- **Maximum Total Time:** (Timeout × MaxRetries) + Sum(backoff delays)
- **Non-Retryable Errors:** Authentication failures (18456, 18452, 18451)

---

### Scenario 6: Response Time Measurement Accuracy

**Given** SQL Server responds in 250 milliseconds
**When** connection health check executes
**Then**:
- Response time measured using Stopwatch (high precision)
- Stopwatch starts before SqlConnection.OpenAsync
- Stopwatch stops after OpenAsync completes
- Measured time = 250ms ± 50ms (tolerance for system variance)
- Response time saved in HealthCheckResult.ResponseTimeMs
- Response time logged with endpoint name

**Test Evidence:**
```csharp
// Arrange: Local SQL Server (fast response)
var endpoint = new Endpoint
{
    Name = "LOCAL-SQL",
    ServerName = "localhost",
    Port = 1433,
    ConnectionString = "Server=localhost;Integrated Security=true;TrustServerCertificate=true"
};

// Act: Execute multiple times to verify consistency
var responseTimes = new List<int>();
for (int i = 0; i < 10; i++)
{
    var result = await executor.ExecuteAsync(endpoint, CancellationToken.None);
    responseTimes.Add(result.ResponseTimeMs);
}

// Assert: Verify response time accuracy
var averageResponseTime = responseTimes.Average();
averageResponseTime.Should().BeLessThan(2000);  // Local server should be fast

// Verify consistency (standard deviation < 500ms)
var stdDev = CalculateStandardDeviation(responseTimes);
stdDev.Should().BeLessThan(500);

// Verify all results logged
_loggerMock.VerifyLog(LogLevel.Information, Times.Exactly(10));
```

**Response Time Measurement:**
- **Tool:** System.Diagnostics.Stopwatch (high-resolution timer)
- **Precision:** Microsecond accuracy (ElapsedMilliseconds)
- **Start Point:** Before SqlConnection.OpenAsync
- **End Point:** After OpenAsync completes
- **Includes:** Network latency, authentication, TLS handshake
- **Excludes:** Query execution time (connection-only check)

---

### Scenario 7: Thread Safety for Concurrent Execution

**Given** 10 connection checks executing concurrently (same endpoint)
**When** all health checks execute in parallel
**Then**:
- Each check uses isolated SqlConnection instance (no shared state)
- No race conditions or deadlocks
- All 10 checks complete successfully
- Each check has independent response time
- No connection pool exhaustion

**Test Evidence:**
```csharp
// Arrange: Single endpoint, 10 concurrent checks
var endpoint = new Endpoint
{
    Name = "CONCURRENT-TEST",
    ServerName = "sql-test-01.domain.local",
    Port = 1433,
    ConnectionString = "Server=sql-test-01.domain.local;Integrated Security=true;Max Pool Size=100"
};

var executor = new ConnectionCheckExecutor(logger, options);

// Act: Execute 10 concurrent checks
var tasks = Enumerable.Range(0, 10)
    .Select(_ => executor.ExecuteAsync(endpoint, CancellationToken.None))
    .ToList();

var results = await Task.WhenAll(tasks);

// Assert: Verify all succeeded
results.Should().AllSatisfy(r => r.Success.Should().BeTrue());

// Verify independent response times (some variance expected)
var responseTimes = results.Select(r => r.ResponseTimeMs).ToList();
responseTimes.Should().AllSatisfy(rt => rt.Should().BeGreaterThan(0));
responseTimes.Should().AllSatisfy(rt => rt.Should().BeLessThan(5000));

// Verify no deadlocks (all tasks completed)
tasks.Should().AllSatisfy(t => t.IsCompleted.Should().BeTrue());

// Verify connection pool not exhausted
using var connection = new SqlConnection(endpoint.ConnectionString);
connection.Open();  // Should succeed (pool has capacity)
```

**Thread Safety Requirements:**
- No shared mutable state (all state in method scope)
- Each execution creates new SqlConnection instance
- Concurrent executions use separate Stopwatch instances
- Logger is thread-safe (ILogger<T> is thread-safe)
- No static mutable fields

---

### Scenario 8: Connection Pooling Interference Prevention

**Given** connection pool has 90 active connections (near limit of 100)
**When** connection health check executes
**Then**:
- Check creates new connection (pool size = 91)
- Check completes successfully
- SqlConnection.Dispose returns connection to pool
- Pool size returns to 90 after check
- No pool exhaustion errors

**Test Evidence:**
```csharp
// Arrange: Fill connection pool to near capacity
var connectionString = "Server=sql-test-01.domain.local;Integrated Security=true;Max Pool Size=100";
var activeConnections = new List<SqlConnection>();

// Open 90 connections (hold them open)
for (int i = 0; i < 90; i++)
{
    var conn = new SqlConnection(connectionString);
    await conn.OpenAsync();
    activeConnections.Add(conn);
}

// Act: Execute health check with near-full pool
var endpoint = new Endpoint
{
    Name = "POOL-TEST",
    ServerName = "sql-test-01.domain.local",
    ConnectionString = connectionString
};

var result = await executor.ExecuteAsync(endpoint, CancellationToken.None);

// Assert: Check succeeded (pool had capacity)
result.Success.Should().BeTrue();

// Cleanup: Close all connections
foreach (var conn in activeConnections)
{
    conn.Dispose();
}

// Wait for pool cleanup
await Task.Delay(1000);

// Verify pool recovered (can open new connection)
using var testConnection = new SqlConnection(connectionString);
await testConnection.OpenAsync();  // Should succeed
```

**Connection Pool Management:**
- Always use `using` statement for SqlConnection disposal
- Disposal returns connection to pool (not closed)
- Pool size: Default 100 (configurable via connection string)
- Health check uses minimal pool slots (1 per concurrent check)
- No long-held connections (open → test → dispose)

---

### Scenario 9: Support for Both Windows and SQL Authentication

**Given** endpoints configured with different authentication methods
**When** connection health checks execute
**Then**:
- Windows Authentication endpoint uses Integrated Security=true
- SQL Authentication endpoint uses User Id and Password
- Both authentication types succeed
- Connection strings built correctly per authentication type
- Credentials never logged

**Test Evidence:**
```csharp
// Test Case 1: Windows Authentication
var endpointWindows = new Endpoint
{
    Name = "WINDOWS-AUTH",
    ServerName = "sql-test-01.domain.local",
    UseWindowsAuthentication = true,
    ConnectionString = "Server=sql-test-01.domain.local;Integrated Security=true;TrustServerCertificate=true"
};

var resultWindows = await executor.ExecuteAsync(endpointWindows, CancellationToken.None);
resultWindows.Success.Should().BeTrue();

// Test Case 2: SQL Authentication
var endpointSql = new Endpoint
{
    Name = "SQL-AUTH",
    ServerName = "sql-test-01.domain.local",
    UseWindowsAuthentication = false,
    SqlUsername = "omniwatch_user",
    SqlPassword = "SecureP@ssw0rd!",
    ConnectionString = "Server=sql-test-01.domain.local;User Id=omniwatch_user;Password=SecureP@ssw0rd!;TrustServerCertificate=true"
};

var resultSql = await executor.ExecuteAsync(endpointSql, CancellationToken.None);
resultSql.Success.Should().BeTrue();

// Assert: No credentials logged
_loggerMock.VerifyLog(logger => !logger.Contains("SecureP@ssw0rd!"), Times.Always());
_loggerMock.VerifyLog(logger => !logger.Contains("omniwatch_user"), Times.Always());
```

**Authentication Support:**
- **Windows Authentication:** Integrated Security=true (uses service account identity)
- **SQL Authentication:** User Id + Password (encrypted in database, encrypted in transit via TLS)
- **Connection String Security:**
  - TrustServerCertificate=true (allow self-signed certs)
  - Encrypt=true (TLS encryption)
  - No credentials in logs

---

### Scenario 10: Graceful Cancellation via CancellationToken

**Given** connection health check executing (in-flight)
**And** CancellationToken signals cancellation (service stopping)
**When** cancellation requested
**Then**:
- SqlConnection.OpenAsync respects cancellation token
- OperationCanceledException thrown
- HealthCheckResult NOT saved (cancelled checks ignored)
- SqlConnection disposed (no lingering connections)
- Cancellation logged: `[INFO] Connection check cancelled for {EndpointName}`

**Test Evidence:**
```csharp
// Arrange: Endpoint with slow connection
var endpoint = new Endpoint
{
    Name = "SLOW-CONNECT",
    ServerName = "slow-sql-server.domain.local",
    ConnectionString = "Server=slow-sql-server.domain.local;Integrated Security=true;Connection Timeout=60"
};

// Act: Execute with cancellation after 2 seconds
using var cts = new CancellationTokenSource();
cts.CancelAfter(TimeSpan.FromSeconds(2));

// Assert: Should throw OperationCanceledException
Func<Task> act = async () => await executor.ExecuteAsync(endpoint, cts.Token);
await act.Should().ThrowAsync<OperationCanceledException>();

// Verify cancellation logged
_loggerMock.VerifyLog(LogLevel.Information, "cancelled", Times.Once());

// Verify no result saved (check repository not called)
_repositoryMock.Verify(r => r.SaveAsync(It.IsAny<HealthCheckResult>()), Times.Never());
```

**Cancellation Handling:**
- All async methods accept CancellationToken parameter
- CancellationToken passed to SqlConnection.OpenAsync
- Cancelled checks throw OperationCanceledException
- Exception caught in orchestrator (not saved as failure)
- SqlConnection disposed in finally block (guaranteed cleanup)

---

## Technical Specification

### Architecture & Dependencies

**Layer**: Infrastructure Layer (External Concern - SQL Server Access)
**Component**: `OmniWatchAI.Infrastructure.Executors.ConnectionCheckExecutor`
**Invoked By**: Application Layer (`HealthCheckExecutor` from STORY-004)
**Dependencies**:
- Domain: `Endpoint` entity, `HealthCheckResult` entity
- Infrastructure: `ISqlConnectionFactory` (connection creation abstraction)
- Logging: `ILogger<ConnectionCheckExecutor>`

### Class Structure

**Files to Create:**

```
src/OmniWatchAI.Infrastructure/Executors/
├── ConnectionCheckExecutor.cs           # Main executor (AC 1-10)
├── IConnectionCheckExecutor.cs          # Interface (Domain layer)
└── ConnectionStringBuilder.cs           # Connection string formatting (AC 9)

src/OmniWatchAI.Infrastructure/Factories/
└── SqlConnectionFactory.cs              # ISqlConnectionFactory implementation

src/OmniWatchAI.Domain/Interfaces/
└── IConnectionCheckExecutor.cs          # Interface definition

tests/UnitTests/Infrastructure/
├── ConnectionCheckExecutorTests.cs      # AC 1-10 unit tests
├── ConnectionStringBuilderTests.cs      # Connection string formatting tests
└── RetryLogicTests.cs                   # AC 5 retry tests

tests/IntegrationTests/Infrastructure/
├── ConnectionCheckIntegrationTests.cs   # AC 1-10 with real SQL Server
├── AuthenticationTests.cs               # AC 3, 9 with real credentials
└── ConcurrencyTests.cs                  # AC 7 (10 concurrent checks)
```

### API Contract: IConnectionCheckExecutor

**Interface (Domain Layer):**

```csharp
namespace OmniWatchAI.Domain.Interfaces;

/// <summary>
/// Executes SQL Server connection health checks.
/// </summary>
public interface IConnectionCheckExecutor
{
    /// <summary>
    /// Tests SQL Server connectivity and measures response time.
    /// </summary>
    /// <param name="endpoint">Endpoint configuration (server, port, credentials).</param>
    /// <param name="cancellationToken">Cancellation token for graceful shutdown.</param>
    /// <returns>Health check result with success status and response time.</returns>
    Task<HealthCheckResult> ExecuteAsync(Endpoint endpoint, CancellationToken cancellationToken);
}
```

**Implementation (Infrastructure Layer):**

```csharp
namespace OmniWatchAI.Infrastructure.Executors;

public class ConnectionCheckExecutor : IConnectionCheckExecutor
{
    private readonly ISqlConnectionFactory _connectionFactory;
    private readonly ILogger<ConnectionCheckExecutor> _logger;
    private readonly ConnectionCheckOptions _options;

    public ConnectionCheckExecutor(
        ISqlConnectionFactory connectionFactory,
        ILogger<ConnectionCheckExecutor> logger,
        IOptions<ConnectionCheckOptions> options)
    {
        _connectionFactory = connectionFactory ?? throw new ArgumentNullException(nameof(connectionFactory));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        _options = options?.Value ?? throw new ArgumentNullException(nameof(options));
    }

    public async Task<HealthCheckResult> ExecuteAsync(
        Endpoint endpoint,
        CancellationToken cancellationToken)
    {
        if (endpoint == null)
            throw new ArgumentNullException(nameof(endpoint));

        var stopwatch = Stopwatch.StartNew();

        try
        {
            // Execute with retry logic (AC 5)
            var result = await ExecuteWithRetryAsync(endpoint, cancellationToken).ConfigureAwait(false);

            stopwatch.Stop();
            result.ResponseTimeMs = (int)stopwatch.ElapsedMilliseconds;

            _logger.LogInformation(
                "Connection check succeeded for {EndpointName} ({ServerName}): {ResponseTimeMs}ms",
                endpoint.Name,
                endpoint.ServerName,
                result.ResponseTimeMs);

            return result;
        }
        catch (OperationCanceledException)
        {
            stopwatch.Stop();
            _logger.LogInformation(
                "Connection check cancelled for {EndpointName} ({ServerName})",
                endpoint.Name,
                endpoint.ServerName);
            throw;  // Propagate cancellation to orchestrator
        }
        catch (Exception ex)
        {
            stopwatch.Stop();

            _logger.LogError(
                ex,
                "Connection check failed for {EndpointName} ({ServerName})",
                endpoint.Name,
                endpoint.ServerName);

            return new HealthCheckResult
            {
                EndpointId = endpoint.Id,
                CheckTimestamp = DateTime.UtcNow,
                Success = false,
                ResponseTimeMs = (int)stopwatch.ElapsedMilliseconds,
                ErrorMessage = GetUserFriendlyErrorMessage(ex)
            };
        }
    }

    private async Task<HealthCheckResult> ExecuteWithRetryAsync(
        Endpoint endpoint,
        CancellationToken cancellationToken)
    {
        var maxRetries = endpoint.MaxRetries ?? _options.DefaultMaxRetries;
        Exception lastException = null;

        for (int attempt = 1; attempt <= maxRetries; attempt++)
        {
            try
            {
                return await TestConnectionAsync(endpoint, cancellationToken).ConfigureAwait(false);
            }
            catch (SqlException ex) when (IsAuthenticationError(ex))
            {
                // Authentication errors are NOT transient - don't retry (AC 3)
                _logger.LogError(
                    ex,
                    "Authentication failed for {EndpointName} ({ServerName}): {ErrorMessage}",
                    endpoint.Name,
                    endpoint.ServerName,
                    ex.Message);
                throw;
            }
            catch (Exception ex) when (attempt < maxRetries)
            {
                lastException = ex;

                _logger.LogWarning(
                    ex,
                    "Connection check failed for {EndpointName} ({ServerName}), attempt {Attempt}/{MaxRetries}: {ErrorMessage}",
                    endpoint.Name,
                    endpoint.ServerName,
                    attempt,
                    maxRetries,
                    ex.Message);

                // Exponential backoff: 2^(attempt-1) seconds (AC 5)
                var delay = TimeSpan.FromSeconds(Math.Pow(2, attempt - 1));
                await Task.Delay(delay, cancellationToken).ConfigureAwait(false);

                // Continue to next retry
            }
            catch (Exception ex)
            {
                // Last attempt failed
                lastException = ex;
                throw;
            }
        }

        // Should never reach here
        throw lastException ?? new InvalidOperationException("Retry logic failed unexpectedly");
    }

    private async Task<HealthCheckResult> TestConnectionAsync(
        Endpoint endpoint,
        CancellationToken cancellationToken)
    {
        using var connection = _connectionFactory.CreateConnection(endpoint.ConnectionString);

        // Open connection with timeout and cancellation support (AC 1, 2, 10)
        await connection.OpenAsync(cancellationToken).ConfigureAwait(false);

        return new HealthCheckResult
        {
            EndpointId = endpoint.Id,
            CheckTimestamp = DateTime.UtcNow,
            Success = true,
            ResponseTimeMs = 0  // Set by caller
        };
    }

    private bool IsAuthenticationError(SqlException ex)
    {
        // SQL Server authentication error codes (AC 3)
        return ex.Number == 18456   // Login failed for user
            || ex.Number == 18452   // Login failed (SQL Server authentication not enabled)
            || ex.Number == 18451;  // Login failed (password expired)
    }

    private string GetUserFriendlyErrorMessage(Exception ex)
    {
        return ex switch
        {
            SqlException sqlEx when sqlEx.Number == -1 => "Connection timeout",
            SqlException sqlEx when sqlEx.Number == 18456 => "Authentication failed: Invalid credentials",
            SqlException sqlEx when sqlEx.Message.Contains("No such host is known") => "DNS resolution failed",
            SqlException sqlEx when sqlEx.Message.Contains("actively refused") => "Connection refused (port not open)",
            SqlException sqlEx when sqlEx.Message.Contains("did not properly respond") => "Host unreachable (firewall or network issue)",
            _ => $"Connection failed: {ex.Message}"
        };
    }
}
```

### Configuration Model

**ConnectionCheckOptions:**

```csharp
namespace OmniWatchAI.Infrastructure.Configuration;

public class ConnectionCheckOptions
{
    public int DefaultMaxRetries { get; set; } = 3;
    public int DefaultTimeoutSeconds { get; set; } = 30;
    public int MaxConcurrentChecks { get; set; } = 10;
}
```

**appsettings.json:**

```json
{
  "ConnectionCheck": {
    "DefaultMaxRetries": 3,
    "DefaultTimeoutSeconds": 30,
    "MaxConcurrentChecks": 10
  }
}
```

### Data Model: Endpoint Entity

**Update Endpoint entity with connection check properties:**

```csharp
namespace OmniWatchAI.Domain.Entities;

public class Endpoint
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string ServerName { get; set; }
    public string InstanceName { get; set; }  // NULL = default instance
    public int Port { get; set; } = 1433;

    // Authentication (AC 9)
    public bool UseWindowsAuthentication { get; set; } = true;
    public string SqlUsername { get; set; }  // NULL if Windows Auth
    public string SqlPassword { get; set; }  // Encrypted, NULL if Windows Auth

    // Connection string (pre-built for performance)
    public string ConnectionString { get; set; }

    // Retry configuration (AC 5)
    public int? MaxRetries { get; set; }  // NULL = use default (3)
    public int? TimeoutSeconds { get; set; }  // NULL = use default (30)

    // Monitoring settings
    public int Priority { get; set; } = 2;  // 1=Critical, 2=Normal, 3=Low
    public bool Enabled { get; set; } = true;
    public DateTime? LastCheckTimestamp { get; set; }
}
```

### Database Schema Migration

**Add columns to Endpoints table:**

```sql
-- Migration: 20250115_AddConnectionCheckSettings

ALTER TABLE Endpoints
ADD UseWindowsAuthentication BIT NOT NULL DEFAULT 1;

ALTER TABLE Endpoints
ADD SqlUsername NVARCHAR(100) NULL;

ALTER TABLE Endpoints
ADD SqlPassword NVARCHAR(500) NULL;  -- Encrypted

ALTER TABLE Endpoints
ADD ConnectionString NVARCHAR(1000) NULL;

ALTER TABLE Endpoints
ADD MaxRetries INT NULL;

ALTER TABLE Endpoints
ADD TimeoutSeconds INT NULL;

-- Create index for enabled endpoints query
CREATE INDEX IX_Endpoints_Enabled ON Endpoints(Enabled) INCLUDE (Id, Name, ServerName, ConnectionString);
```

### Business Rules

1. **Connection Timeout:** Default 30 seconds, configurable per endpoint (5-300s range)
2. **Retry Attempts:** Default 3, configurable per endpoint (0-5 range)
3. **Exponential Backoff:** Delay = 2^(attempt-1) seconds (1s, 2s, 4s, 8s, 16s)
4. **Authentication Errors:** Never retry (18456, 18452, 18451 error codes)
5. **Response Time:** Measured from OpenAsync start to completion (milliseconds)
6. **Credential Security:** No credentials logged, encrypted in database
7. **Thread Safety:** No shared mutable state, isolated SqlConnection per check
8. **Connection Pooling:** Always dispose SqlConnection, use `using` statements
9. **Cancellation:** All async methods accept CancellationToken, propagate to OpenAsync
10. **Fast Fail:** Connection checks must complete < 5 seconds (timeout or success)

### Non-Functional Requirements

**Performance:**
- Connection establishment: < 2 seconds (typical)
- Maximum execution time: < 5 seconds (fast fail)
- Response time measurement: Millisecond precision (Stopwatch)
- Connection pooling: No pool exhaustion (proper disposal)
- Thread safety: Support 10+ concurrent checks

**Reliability:**
- Retry logic: Handles transient network failures
- Timeout handling: Prevents hanging operations
- Exponential backoff: Reduces server load during outages
- Connection disposal: No resource leaks
- Graceful cancellation: Respects service shutdown

**Security:**
- No credentials logged: Passwords/usernames never in logs
- TLS encryption: Encrypt=true in connection strings
- Credential encryption: SqlPassword encrypted in database
- Authentication support: Windows Auth (preferred) and SQL Auth
- Certificate validation: TrustServerCertificate=true (allow self-signed)

**Scalability:**
- Thread-safe: No shared mutable state
- Concurrent execution: Support 10+ simultaneous checks
- Connection pooling: Efficient connection reuse
- Minimal memory: SqlConnection disposed immediately after check
- No bottlenecks: Isolated execution per endpoint

**Monitoring:**
- Response time logged: Every check logs duration
- Error categorization: DNS, timeout, refused, authentication
- Retry attempts logged: Track retry behavior
- Success rate tracking: Via HealthCheckResult persistence
- Slow connections flagged: Warnings for > 5 seconds

---

## Implementation Notes

### Technology Decisions

**SqlConnection:** Microsoft.Data.SqlClient 5.1.x
- Modern SQL Server client library
- Async/await support (OpenAsync)
- CancellationToken support (graceful cancellation)
- Connection pooling (automatic, configurable)
- TLS encryption support

**Stopwatch:** System.Diagnostics.Stopwatch
- High-resolution timer (microsecond precision)
- No external dependencies
- Elapsed time in milliseconds
- Lightweight (no allocation overhead)

**Retry Logic:** Custom implementation (no Polly)
- Simple exponential backoff (2^attempt seconds)
- No external dependencies (project constraint)
- Exception filtering (authentication vs transient)
- Configurable max retries per endpoint

**Logging:** ILogger<ConnectionCheckExecutor> (Serilog)
- Structured logging (placeholders, not interpolation)
- Context enrichment (endpoint name, server name)
- No credential logging (security requirement)
- Log levels: Info (success), Warning (retry), Error (failure)

### Code Patterns to Follow

**All code must follow coding-standards.md:**
- Constructor injection: `ISqlConnectionFactory`, `ILogger<T>`, `IOptions<T>`
- Async all the way: ConfigureAwait(false) in all await calls
- Structured logging: `_logger.LogInformation("{Placeholder}", value)`
- Specific exception handling: `catch (SqlException ex) when (ex.Number == 18456)`
- Fail fast validation: `if (endpoint == null) throw new ArgumentNullException`
- Using statements: `using var connection = ...` (guaranteed disposal)

**Repository Pattern:**
- Interface `IConnectionCheckExecutor` in Domain layer
- Implementation `ConnectionCheckExecutor` in Infrastructure layer
- No direct SqlConnection in Application layer
- Invoked by HealthCheckExecutor (STORY-004)

**Clean Architecture:**
- Executor in Infrastructure layer (external concern)
- Interface in Domain layer (dependency inversion)
- No domain references to infrastructure
- Application layer invokes via interface

### Testing Strategy

**Unit Tests** (xUnit + Moq):
- Mock ISqlConnectionFactory (simulate success, timeout, authentication failure)
- Test retry logic (verify 3 attempts, exponential backoff)
- Test timeout handling (verify OperationCanceledException after 30s)
- Test authentication error detection (verify no retry for 18456)
- Test response time measurement (verify Stopwatch usage)
- Test cancellation (verify CancellationToken propagation)
- Test error message formatting (verify user-friendly messages)
- Coverage target: 95% for ConnectionCheckExecutor

**Integration Tests** (xUnit + Testcontainers):
- Real SQL Server database (Docker container via Testcontainers.MsSql)
- Test successful connection (Windows Auth)
- Test timeout with unreachable server (192.168.255.255)
- Test authentication failure (invalid SQL credentials)
- Test retry with transient failure (stop/start SQL Server)
- Test concurrent execution (10 simultaneous checks)
- Test connection pooling (near-full pool scenario)
- Coverage target: 85% for integration scenarios

**Performance Tests:**
- Measure response time: Local SQL Server (< 100ms expected)
- Measure timeout duration: Unreachable server (~30000ms expected)
- Measure concurrent execution: 10 checks in parallel (no deadlocks)
- Measure connection pool usage: Verify no pool exhaustion
- Measure retry delays: Verify exponential backoff timing (1s, 2s, 4s)

### Edge Cases

**1. SQL Server Offline/Unreachable:**
- Timeout after 30 seconds (configurable)
- SqlException.Number = -1 detected
- Result: Success=false, ErrorMessage="Connection timeout"
- Retry logic executes (3 attempts default)

**2. Invalid Credentials:**
- SqlException.Number = 18456 detected
- No retry attempted (authentication errors are not transient)
- Result: Success=false, ErrorMessage="Authentication failed"
- Credentials NOT logged (security requirement)

**3. Network Timeout:**
- Timeout after configured duration (default 30s)
- Result: Success=false, ErrorMessage="Connection timeout"
- Retry logic executes

**4. Firewall Blocking Connection:**
- Connection refused or timeout (depends on firewall config)
- Retry logic executes
- Result: Success=false, ErrorMessage="Connection refused" or "Host unreachable"

**5. Connection Pooling Interference:**
- SqlConnection disposal returns to pool (not closed)
- Health check uses minimal pool slots
- No pool exhaustion (Max Pool Size=100 default)

**6. Concurrent Execution of Same Endpoint:**
- Each check uses isolated SqlConnection instance
- No shared mutable state
- Thread-safe (no race conditions)
- Independent response times

**7. Service Shutdown During Check:**
- CancellationToken signals cancellation
- SqlConnection.OpenAsync throws OperationCanceledException
- Connection disposed in finally block
- No result saved (cancelled checks ignored)

**8. DNS Failure:**
- SqlException inner exception: "No such host is known"
- Retry logic executes (DNS may resolve later)
- Result: Success=false, ErrorMessage="DNS resolution failed"

**9. Port Not Open:**
- Connection refused error
- Retry logic executes
- Result: Success=false, ErrorMessage="Connection refused (port not open)"

**10. Slow Connection (> 5 seconds):**
- Connection succeeds but takes > 5 seconds
- Warning logged: "Slow connection detected"
- Result: Success=true, ResponseTimeMs > 5000

### Compliance Checklist

- [ ] Clean Architecture (executor in Infrastructure layer, interface in Domain)
- [ ] All dependencies injected (ISqlConnectionFactory, ILogger, IOptions)
- [ ] Async/await throughout (ConfigureAwait(false) in Infrastructure layer)
- [ ] Structured logging (no string interpolation, no credentials)
- [ ] Specific exception handling (SqlException with error code filtering)
- [ ] CancellationToken support (passed to OpenAsync)
- [ ] Using statements (guaranteed SqlConnection disposal)
- [ ] Retry logic (exponential backoff, configurable max retries)
- [ ] No credential logging (security requirement)
- [ ] Thread safety (no shared mutable state)
- [ ] 95% unit test coverage
- [ ] No forbidden anti-patterns (no direct instantiation, no static mutable state)

---

## Dependencies

**Hard Dependencies (Must Complete First):**
- STORY-001: Windows Service Framework (PollingService lifecycle)
- STORY-003: Configuration Management (endpoint configuration loading)

**Soft Dependencies (Work Together):**
- STORY-004: Health Check Execution Engine (orchestrator invokes this executor)

**External Dependencies:**
- SQL Server 2022 database (monitored instances)
- Network connectivity to monitored SQL Server instances
- Service account with database access (Windows Auth or SQL Auth)

---

## Definition of Done

**Code Implementation:**
- [ ] ConnectionCheckExecutor.cs implements IConnectionCheckExecutor
- [ ] ExecuteAsync method tests connection, measures response time
- [ ] Retry logic with exponential backoff (3 attempts default)
- [ ] Timeout handling (30 seconds default, configurable)
- [ ] Authentication error detection (no retry for 18456, 18452, 18451)
- [ ] Network error categorization (DNS, refused, unreachable, timeout)
- [ ] Response time measurement (Stopwatch, millisecond precision)
- [ ] Thread safety (no shared mutable state)
- [ ] Connection pooling support (proper disposal)
- [ ] CancellationToken support (graceful shutdown)
- [ ] No credential logging (security requirement)
- [ ] SqlConnectionFactory.cs creates SqlConnection instances
- [ ] ConnectionStringBuilder.cs formats connection strings
- [ ] IConnectionCheckExecutor interface in Domain layer

**Testing:**
- [ ] Unit tests: Successful connection (mock factory)
- [ ] Unit tests: Timeout handling (mock timeout exception)
- [ ] Unit tests: Authentication failure (mock 18456 error, no retry)
- [ ] Unit tests: Network failure (mock network exception, retry)
- [ ] Unit tests: Retry logic (verify 3 attempts, exponential backoff)
- [ ] Unit tests: Response time measurement (verify Stopwatch)
- [ ] Unit tests: Thread safety (10 concurrent mock executions)
- [ ] Unit tests: Connection pooling (verify disposal)
- [ ] Unit tests: Cancellation (mock OperationCanceledException)
- [ ] Integration tests: Real SQL Server connection (Testcontainers)
- [ ] Integration tests: Timeout with unreachable server
- [ ] Integration tests: Authentication failure with invalid credentials
- [ ] Integration tests: Retry with transient failure
- [ ] Integration tests: 10 concurrent checks (thread safety)
- [ ] Integration tests: Connection pool near-full scenario
- [ ] Coverage: >= 95% for ConnectionCheckExecutor, >= 85% overall
- [ ] All tests pass (100% pass rate)

**Quality Gates:**
- [ ] No violations of architecture-constraints.md (executor in Infrastructure layer)
- [ ] No violations of coding-standards.md (naming, logging, DI, error handling)
- [ ] No violations of anti-patterns.md (no god objects, no direct instantiation)
- [ ] Code review approved
- [ ] No CRITICAL or HIGH severity issues from static analysis
- [ ] No credential leaks in logs (verified via log inspection)

**Documentation:**
- [ ] Code comments for retry logic (exponential backoff)
- [ ] Code comments for authentication error detection
- [ ] XML documentation for IConnectionCheckExecutor interface
- [ ] Configuration documentation (timeout, retries)
- [ ] Security documentation (credential handling)

**Database:**
- [ ] Endpoints table updated with connection check columns (EF Core migration)
- [ ] SqlUsername, SqlPassword columns (encrypted)
- [ ] ConnectionString column (pre-built for performance)
- [ ] MaxRetries, TimeoutSeconds columns (nullable, defaults in config)
- [ ] UseWindowsAuthentication column (default true)

**Performance:**
- [ ] Connection establishment < 2 seconds (typical, verified via integration test)
- [ ] Timeout duration ~30 seconds (verified via integration test)
- [ ] Retry delays correct: 1s, 2s, 4s (verified via integration test)
- [ ] 10 concurrent checks complete without deadlocks
- [ ] No connection pool exhaustion (verified with 90+ active connections)

**Configuration:**
- [ ] appsettings.json has ConnectionCheck section
- [ ] DefaultMaxRetries: 3
- [ ] DefaultTimeoutSeconds: 30
- [ ] MaxConcurrentChecks: 10
- [ ] Per-endpoint overrides supported (Endpoints table)

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
- STORY-008: Query Response Time Monitoring (builds on connection check)
- STORY-009: Database Status Checks (uses connection after established)
- STORY-010: Resource Metrics Collection (uses connection for DMV queries)

**Related Stories** (work together):
- STORY-004: Health Check Execution Engine (orchestrator invokes this executor)

---

## Story Metrics

**Estimation Breakdown:**
- ConnectionCheckExecutor implementation: 2 points
- Retry logic with exponential backoff: 2 points
- Timeout handling (CancellationTokenSource): 1 point
- Authentication error detection: 1 point
- Response time measurement (Stopwatch): 1 point
- Thread safety and connection pooling: 1 point

**Total: 8 story points (estimated 3-4 days for experienced .NET developer)**

---

## Acceptance Criteria Summary

**Must Have (All 10 ACs must pass):**

1. Successful connection to accessible SQL Server (< 5s, response time logged)
2. Connection timeout handling (30s default, configurable)
3. Authentication failure handling (18456 error, no retry)
4. Network failure handling (DNS, refused, unreachable, retry logic)
5. Retry logic with exponential backoff (3 attempts, 1s, 2s, 4s delays)
6. Response time measurement accuracy (Stopwatch, millisecond precision)
7. Thread safety for concurrent execution (10+ concurrent checks)
8. Connection pooling interference prevention (proper disposal)
9. Support for Windows and SQL Authentication (both types work)
10. Graceful cancellation via CancellationToken (service shutdown)

**All acceptance criteria MUST be validated via automated tests (unit + integration) with real SQL Server instances.**

---

**Story Owner:** [TBD]
**Last Updated:** 2025-01-15
**Created By:** DevForgeAI Requirements Analyst
