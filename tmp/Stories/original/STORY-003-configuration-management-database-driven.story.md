---
id: STORY-003
title: Configuration Management - Database-Driven Configuration with Audit Logging
epic: EPIC-001
sprint: Sprint-1
status: Backlog
priority: High
story-points: 8
size-estimate: Medium
created: 2025-01-15
---

# STORY-003: Configuration Management - Database-Driven Configuration with Audit Logging

**Status:** Backlog
**Priority:** High
**Story Points:** 8
**Epic:** EPIC-001 (Core Monitoring Infrastructure)
**Sprint:** Sprint-1
**Complexity:** Medium (database schema design, change detection, validation, audit logging)

---

## User Story

As a **system administrator**,
I want **to load all operational parameters (polling intervals, timeouts, parallelism, alert thresholds) from the database on service start and detect configuration changes without requiring a service restart**,
So that **I can manage monitoring behavior dynamically without service downtime, maintain an audit trail of all configuration changes for compliance, and apply safe defaults when invalid configuration is detected**.

---

## Acceptance Criteria

### Scenario 1: Configuration Loaded on Service Start (Performance - < 2 seconds)
- **Given** the Configuration, Endpoints, AlertRules, AlertRecipients, and AuditLog tables are populated with valid data
- **When** PollingService or AlertingService starts
- **Then** all configuration is loaded into memory within 2 seconds
- **And** configuration values are strongly typed (not strings)
- **And** a log entry records the configuration load with timestamp and record count

**Testable Assertions:**
```
- Config load duration <= 2000 milliseconds (measured via Stopwatch)
- All endpoint configurations loaded (count matches database)
- All alert rules loaded (count matches database)
- AlertRecipients with routing rules loaded correctly
- Log contains: "Configuration loaded. Endpoints: X, AlertRules: Y, Recipients: Z, Duration: Xms"
```

---

### Scenario 2: Strong Typing and Validation on Load
- **Given** configuration is being loaded from database
- **When** FluentValidation rules are applied to each configuration entity
- **Then** valid configurations are accepted and stored in memory
- **And** invalid configurations (e.g., negative polling intervals, invalid email addresses) are logged as warnings
- **And** safe default values are used for invalid configurations instead of failing startup

**Testable Assertions:**
```
- PollingIntervalSeconds must be >= 1 (cannot be 0 or negative)
- MaxParallelism must be >= 1 and <= 100
- EmailAddress must be valid format (validated via regex or EmailValidator)
- AlertThreshold values must be within valid ranges (e.g., 0-100 for percentages)
- Log warning: "Invalid configuration detected. Using safe default. Field: X, Invalid value: Y, Default: Z"
```

**Safe Default Values:**
- PollingIntervalSeconds: 60 (1 minute)
- MaxParallelism: 10
- HealthCheckTimeoutSeconds: 30
- RetryAttempts: 3
- EmailSmtpPort: 587 (TLS)

---

### Scenario 3: Change Detection and Reload Without Service Restart
- **Given** configuration changes are made to Configuration or Endpoints tables in the database
- **When** ConfigurationReloader detects change (via polling last_modified_timestamp or query row count)
- **Then** new configuration is loaded from database
- **And** in-memory configuration is atomically updated (no partial updates)
- **And** in-flight health checks continue using old configuration (safe switchover)
- **And** new checks use updated configuration
- **And** service restart is NOT required

**Testable Assertions:**
```
- Change detection runs every 30 seconds (configurable, default)
- Last_modified_timestamp or hash is checked for changes
- When change detected, configuration is reloaded from database
- In-memory config is updated via thread-safe mechanism (lock or Interlocked)
- Log info: "Configuration change detected. Reloading configuration..."
- Log info: "Configuration reloaded successfully. Changes: X endpoint(s), Y rule(s)"
```

**Implementation Options (to verify with user):**
1. Polling: Query `SELECT MAX(LastModified) FROM Configuration` every 30 seconds
2. Change notification: Use SQL Server Change Tracking or Query Notifications
3. Hybrid: Short-lived cache with max-age of 30 seconds

---

### Scenario 4: Audit Logging for All Configuration Changes
- **Given** a DBA (or admin) modifies configuration (INSERT, UPDATE, DELETE) in Configuration, Endpoints, AlertRules, or AlertRecipients tables
- **When** change is committed to database
- **Then** AuditLog table records: user, timestamp, operation type (INSERT/UPDATE/DELETE), old value, new value, affected table
- **And** audit log entry includes IP address (if available) and session identifier
- **And** audit logging does NOT impact configuration load/reload performance

**Testable Assertions:**
```
- For each UPDATE: AuditLog contains UserName, ChangeTimestamp, TableName, ColumnName, OldValue, NewValue, OperationType='UPDATE'
- For each INSERT: AuditLog contains UserName, ChangeTimestamp, TableName, new record ID, OperationType='INSERT'
- For each DELETE: AuditLog contains UserName, ChangeTimestamp, TableName, old record ID, OperationType='DELETE'
- Timestamp is in UTC (datetime2 with UTC offset)
- Audit logging is asynchronous (non-blocking) to avoid performance impact
```

**Audit Log Schema:**
```
AuditLog {
  Id (bigint, PK, identity),
  TableName (nvarchar(128)),
  OperationType (nvarchar(20)) -- 'INSERT', 'UPDATE', 'DELETE'
  ColumnName (nvarchar(128), nullable),
  OldValue (nvarchar(max), nullable),
  NewValue (nvarchar(max), nullable),
  UserName (nvarchar(256)),
  ChangeTimestamp (datetime2 UTC),
  IpAddress (nvarchar(45), nullable),
  SessionId (nvarchar(256), nullable),
  Indexed on: ChangeTimestamp DESC, TableName
}
```

---

### Scenario 5: Invalid Configuration Handling with Safe Defaults
- **Given** configuration contains invalid values (e.g., negative polling interval, out-of-range threshold)
- **When** configuration is loaded or reloaded
- **Then** invalid values are logged as warnings with details (field, invalid value, default used)
- **And** service continues to run with safe defaults instead of crashing
- **And** admin is alerted to review configuration in logs
- **And** invalid configurations are NOT persisted back to database (read-only)

**Testable Assertions:**
```
- Invalid value: polling_interval_seconds = -5 → Use default 60, log warning
- Invalid value: max_parallelism = 1000 → Use default 10, log warning
- Invalid value: email = "not-an-email" → Skip recipient, log error
- Invalid value: alert_threshold = 150 (for % metric) → Use default safe value, log warning
- Log level for invalid config: Warning or Error (configurable)
- Service startup continues even with multiple invalid configurations
```

---

### Scenario 6: Per-Endpoint Configuration Overrides
- **Given** a specific endpoint needs different polling interval or timeout than global defaults
- **When** configuration is loaded
- **Then** EndpointConfiguration table provides per-endpoint overrides
- **And** overrides are merged with global configuration (endpoint settings override global)
- **And** missing override values fall back to global configuration
- **And** validation applies to both global and override values

**Testable Assertions:**
```
- Global Configuration: PollingIntervalSeconds = 60
- Endpoint-specific override (for critical endpoint): PollingIntervalSeconds = 10
- Loaded config for that endpoint: PollingIntervalSeconds = 10 (override applied)
- Loaded config for other endpoints: PollingIntervalSeconds = 60 (global)
- Validation applies to override values (same rules as global)
```

**Database Schema:**
```
EndpointConfiguration {
  Id (int, PK),
  EndpointId (int, FK to Endpoints),
  PollingIntervalSeconds (int, nullable),
  HealthCheckTimeoutSeconds (int, nullable),
  RetryAttempts (int, nullable),
  LastModified (datetime2 UTC, indexed),
  Unique(EndpointId)
}
```

---

### Scenario 7: Database Connection Failure Handling
- **Given** the database is unreachable when service starts
- **When** configuration load is attempted
- **Then** service logs error "Failed to load configuration from database. Using hardcoded defaults."
- **And** hardcoded safe defaults are used for all configuration values
- **And** service continues to run (degraded mode)
- **And** configuration reload attempts continue at regular intervals (every 30 seconds)
- **And** when database becomes available, configuration is reloaded

**Testable Assertions:**
```
- When database is unavailable, SqlException is caught
- Log error: "Failed to load configuration from database. Using hardcoded defaults. Exception: ..."
- Hard-coded defaults are applied (same as invalid config defaults)
- Service continues to run (doesn't exit OnStart)
- Retry mechanism is active in ConfigurationReloader
- When connection is restored, next reload attempt succeeds
```

---

### Scenario 8: Concurrent Configuration Updates
- **Given** multiple administrators are making configuration changes simultaneously
- **When** ConfigurationReloader detects changes and reloads configuration
- **Then** in-memory configuration update is atomic (all-or-nothing)
- **And** no partial updates or race conditions occur
- **And** in-flight health checks using old config are not affected
- **And** new health checks use updated config

**Testable Assertions:**
```
- Configuration reload uses ReaderWriterLockSlim or Thread-safe collection
- Multiple concurrent reads are allowed (health checks reading config)
- Configuration update is serialized (one reload at a time)
- No race conditions in config access (verified via unit tests with ConcurrentBag)
- Log debug: "Configuration update lock acquired. Reloading configuration..."
```

---

## Technical Specification

### Database Schema

#### Configuration Table
```sql
CREATE TABLE Configuration (
    Id INT PRIMARY KEY IDENTITY(1,1),
    PollingIntervalSeconds INT NOT NULL DEFAULT 60,
    MaxParallelism INT NOT NULL DEFAULT 10,
    HealthCheckTimeoutSeconds INT NOT NULL DEFAULT 30,
    RetryAttempts INT NOT NULL DEFAULT 3,
    EmailSmtpHost NVARCHAR(256) NOT NULL,
    EmailSmtpPort INT NOT NULL DEFAULT 587,
    EmailSmtpUseSsl BIT NOT NULL DEFAULT 1,
    EmailFromAddress NVARCHAR(256) NOT NULL,
    LastModified DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    -- Constraints
    CONSTRAINT CK_PollingInterval CHECK (PollingIntervalSeconds >= 1),
    CONSTRAINT CK_MaxParallelism CHECK (MaxParallelism >= 1 AND MaxParallelism <= 100),
    CONSTRAINT CK_HealthCheckTimeout CHECK (HealthCheckTimeoutSeconds >= 5),
    CONSTRAINT CK_RetryAttempts CHECK (RetryAttempts >= 0 AND RetryAttempts <= 10)
);

CREATE NONCLUSTERED INDEX IX_Configuration_LastModified
    ON Configuration(LastModified DESC);
```

#### Endpoints Table
```sql
CREATE TABLE Endpoints (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(256) NOT NULL UNIQUE,
    ServerName NVARCHAR(256) NOT NULL,
    InstanceName NVARCHAR(256),
    Port INT NOT NULL DEFAULT 1433,
    Environment NVARCHAR(50) NOT NULL, -- 'Development', 'Test', 'Production'
    Enabled BIT NOT NULL DEFAULT 1,
    ConnectionStringTemplate NVARCHAR(MAX) NOT NULL,
    LastModified DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    -- Constraints
    CONSTRAINT CK_Port CHECK (Port >= 1 AND Port <= 65535),
    CONSTRAINT CK_Environment CHECK (Environment IN ('Development', 'Test', 'Production'))
);

CREATE NONCLUSTERED INDEX IX_Endpoints_LastModified
    ON Endpoints(LastModified DESC);
CREATE NONCLUSTERED INDEX IX_Endpoints_Environment
    ON Endpoints(Environment);
CREATE NONCLUSTERED INDEX IX_Endpoints_Enabled
    ON Endpoints(Enabled);
```

#### AlertRules Table
```sql
CREATE TABLE AlertRules (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(256) NOT NULL UNIQUE,
    AlertType NVARCHAR(50) NOT NULL, -- 'HighCpuUsage', 'HighMemoryUsage', 'SlowQuery', 'ConnectionFailure'
    Severity NVARCHAR(50) NOT NULL, -- 'Critical', 'Warning', 'Info'
    MetricName NVARCHAR(256),
    ThresholdValue DECIMAL(10, 2) NOT NULL,
    ThresholdUnit NVARCHAR(20), -- '%', 'ms', 'MB', etc.
    DurationSeconds INT NOT NULL DEFAULT 60, -- Alert triggered if threshold exceeded for N seconds
    Enabled BIT NOT NULL DEFAULT 1,
    LastModified DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    -- Constraints
    CONSTRAINT CK_AlertType CHECK (AlertType IN ('HighCpuUsage', 'HighMemoryUsage', 'SlowQuery', 'ConnectionFailure')),
    CONSTRAINT CK_Severity CHECK (Severity IN ('Critical', 'Warning', 'Info')),
    CONSTRAINT CK_ThresholdValue CHECK (ThresholdValue >= 0),
    CONSTRAINT CK_DurationSeconds CHECK (DurationSeconds >= 1)
);

CREATE NONCLUSTERED INDEX IX_AlertRules_LastModified
    ON AlertRules(LastModified DESC);
CREATE NONCLUSTERED INDEX IX_AlertRules_Enabled
    ON AlertRules(Enabled);
```

#### AlertRecipients Table
```sql
CREATE TABLE AlertRecipients (
    Id INT PRIMARY KEY IDENTITY(1,1),
    EmailAddress NVARCHAR(256) NOT NULL UNIQUE,
    AlertRuleId INT NOT NULL FK REFERENCES AlertRules(Id),
    Environment NVARCHAR(50), -- NULL = all, 'Development', 'Test', 'Production'
    MinimumSeverity NVARCHAR(50) NOT NULL DEFAULT 'Info', -- 'Critical', 'Warning', 'Info'
    Enabled BIT NOT NULL DEFAULT 1,
    LastModified DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    -- Constraints
    CONSTRAINT CK_MinimumSeverity CHECK (MinimumSeverity IN ('Critical', 'Warning', 'Info')),
    CONSTRAINT CK_EmailFormat CHECK (EmailAddress LIKE '%@%.%')
);

CREATE NONCLUSTERED INDEX IX_AlertRecipients_LastModified
    ON AlertRecipients(LastModified DESC);
CREATE NONCLUSTERED INDEX IX_AlertRecipients_AlertRuleId
    ON AlertRecipients(AlertRuleId);
CREATE NONCLUSTERED INDEX IX_AlertRecipients_Enabled
    ON AlertRecipients(Enabled);
```

#### AuditLog Table
```sql
CREATE TABLE AuditLog (
    Id BIGINT PRIMARY KEY IDENTITY(1,1),
    TableName NVARCHAR(128) NOT NULL,
    OperationType NVARCHAR(20) NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
    ColumnName NVARCHAR(128),
    OldValue NVARCHAR(MAX),
    NewValue NVARCHAR(MAX),
    RecordId INT,
    UserName NVARCHAR(256) NOT NULL,
    ChangeTimestamp DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    IpAddress NVARCHAR(45),
    SessionId NVARCHAR(256),

    -- Constraints
    CONSTRAINT CK_OperationType CHECK (OperationType IN ('INSERT', 'UPDATE', 'DELETE'))
);

CREATE NONCLUSTERED INDEX IX_AuditLog_ChangeTimestamp
    ON AuditLog(ChangeTimestamp DESC);
CREATE NONCLUSTERED INDEX IX_AuditLog_TableName
    ON AuditLog(TableName, ChangeTimestamp DESC);
CREATE NONCLUSTERED INDEX IX_AuditLog_UserName
    ON AuditLog(UserName, ChangeTimestamp DESC);
```

#### EndpointConfiguration Table (Per-Endpoint Overrides)
```sql
CREATE TABLE EndpointConfiguration (
    Id INT PRIMARY KEY IDENTITY(1,1),
    EndpointId INT NOT NULL UNIQUE FK REFERENCES Endpoints(Id) ON DELETE CASCADE,
    PollingIntervalSeconds INT,
    HealthCheckTimeoutSeconds INT,
    RetryAttempts INT,
    LastModified DATETIME2 NOT NULL DEFAULT GETUTCDATE(),

    -- Constraints
    CONSTRAINT CK_PollingInterval_Override CHECK (PollingIntervalSeconds IS NULL OR PollingIntervalSeconds >= 1),
    CONSTRAINT CK_HealthCheckTimeout_Override CHECK (HealthCheckTimeoutSeconds IS NULL OR HealthCheckTimeoutSeconds >= 5),
    CONSTRAINT CK_RetryAttempts_Override CHECK (RetryAttempts IS NULL OR RetryAttempts >= 0)
);

CREATE NONCLUSTERED INDEX IX_EndpointConfiguration_LastModified
    ON EndpointConfiguration(LastModified DESC);
```

---

### Domain Layer

#### Configuration Entities (OmniWatchAI.Domain/Entities/)

**Configuration.cs** - Global settings
```csharp
public class Configuration
{
    public int Id { get; set; }
    public int PollingIntervalSeconds { get; set; }
    public int MaxParallelism { get; set; }
    public int HealthCheckTimeoutSeconds { get; set; }
    public int RetryAttempts { get; set; }
    public string EmailSmtpHost { get; set; }
    public int EmailSmtpPort { get; set; }
    public bool EmailSmtpUseSsl { get; set; }
    public string EmailFromAddress { get; set; }
    public DateTime LastModified { get; set; }
}
```

**AlertRule.cs**
```csharp
public class AlertRule
{
    public int Id { get; set; }
    public string Name { get; set; }
    public AlertType AlertType { get; set; }
    public Severity Severity { get; set; }
    public string MetricName { get; set; }
    public decimal ThresholdValue { get; set; }
    public string ThresholdUnit { get; set; }
    public int DurationSeconds { get; set; }
    public bool Enabled { get; set; }
    public DateTime LastModified { get; set; }
}
```

**AlertRecipient.cs**
```csharp
public class AlertRecipient
{
    public int Id { get; set; }
    public string EmailAddress { get; set; }
    public int AlertRuleId { get; set; }
    public Environment? Environment { get; set; } // NULL = all environments
    public Severity MinimumSeverity { get; set; }
    public bool Enabled { get; set; }
    public DateTime LastModified { get; set; }
}
```

**EndpointConfiguration.cs** - Per-endpoint overrides
```csharp
public class EndpointConfiguration
{
    public int Id { get; set; }
    public int EndpointId { get; set; }
    public int? PollingIntervalSeconds { get; set; }
    public int? HealthCheckTimeoutSeconds { get; set; }
    public int? RetryAttempts { get; set; }
    public DateTime LastModified { get; set; }
}
```

**AuditLog.cs**
```csharp
public class AuditLog
{
    public long Id { get; set; }
    public string TableName { get; set; }
    public string OperationType { get; set; } // 'INSERT', 'UPDATE', 'DELETE'
    public string ColumnName { get; set; }
    public string OldValue { get; set; }
    public string NewValue { get; set; }
    public int? RecordId { get; set; }
    public string UserName { get; set; }
    public DateTime ChangeTimestamp { get; set; }
    public string IpAddress { get; set; }
    public string SessionId { get; set; }
}
```

#### Repository Interfaces (OmniWatchAI.Domain/Interfaces/)

**IConfigurationRepository.cs**
```csharp
public interface IConfigurationRepository
{
    Task<Configuration> GetConfigurationAsync(CancellationToken cancellationToken);
    Task<List<Endpoint>> GetAllEndpointsAsync(CancellationToken cancellationToken);
    Task<EndpointConfiguration> GetEndpointConfigurationAsync(int endpointId, CancellationToken cancellationToken);
    Task<List<AlertRule>> GetAllAlertRulesAsync(CancellationToken cancellationToken);
    Task<List<AlertRecipient>> GetAllAlertRecipientsAsync(CancellationToken cancellationToken);
    Task<DateTime> GetLastModifiedTimestampAsync(CancellationToken cancellationToken);
}

public interface IAuditLogRepository
{
    Task LogChangeAsync(AuditLog auditLog, CancellationToken cancellationToken);
}
```

---

### Application Layer

#### ConfigurationService.cs (OmniWatchAI.Application/Configuration/)

**Responsibilities:**
- Load configuration from database on service start
- Perform validation on loaded configuration
- Apply safe defaults for invalid values
- Provide thread-safe access to configuration
- Support configuration reload without service restart

```csharp
public interface IConfigurationService
{
    Task LoadConfigurationAsync(CancellationToken cancellationToken);
    Configuration GetConfiguration();
    List<Endpoint> GetAllEndpoints();
    List<AlertRule> GetAllAlertRules();
    List<AlertRecipient> GetAllAlertRecipients();
    int GetPollingInterval(int endpointId);
    int GetHealthCheckTimeout(int endpointId);
    int GetRetryAttempts(int endpointId);
}

public class ConfigurationService : IConfigurationService
{
    private readonly IConfigurationRepository _repository;
    private readonly ILogger<ConfigurationService> _logger;
    private readonly ReaderWriterLockSlim _configLock;

    private Configuration _configuration;
    private List<Endpoint> _endpoints;
    private List<AlertRule> _alertRules;
    private List<AlertRecipient> _alertRecipients;
    private Dictionary<int, EndpointConfiguration> _endpointConfigurations;

    // Thread-safe property access using ReaderWriterLockSlim
    public Configuration GetConfiguration()
    {
        _configLock.EnterReadLock();
        try
        {
            return _configuration;
        }
        finally
        {
            _configLock.ExitReadLock();
        }
    }

    public async Task LoadConfigurationAsync(CancellationToken cancellationToken)
    {
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();

        try
        {
            var configuration = await _repository.GetConfigurationAsync(cancellationToken);
            var endpoints = await _repository.GetAllEndpointsAsync(cancellationToken);
            var alertRules = await _repository.GetAllAlertRulesAsync(cancellationToken);
            var alertRecipients = await _repository.GetAllAlertRecipientsAsync(cancellationToken);

            // Validate and apply safe defaults
            ValidateAndApplyDefaults(configuration, endpoints, alertRules, alertRecipients);

            // Atomic update of in-memory configuration
            _configLock.EnterWriteLock();
            try
            {
                _configuration = configuration;
                _endpoints = endpoints;
                _alertRules = alertRules;
                _alertRecipients = alertRecipients;
            }
            finally
            {
                _configLock.ExitWriteLock();
            }

            stopwatch.Stop();
            _logger.LogInformation(
                "Configuration loaded successfully. Duration: {DurationMs}ms. Endpoints: {EndpointCount}, AlertRules: {AlertRuleCount}, Recipients: {RecipientCount}",
                stopwatch.ElapsedMilliseconds,
                endpoints.Count,
                alertRules.Count,
                alertRecipients.Count);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to load configuration from database. Using hardcoded defaults.");
            ApplyHardcodedDefaults();
        }
    }

    private void ValidateAndApplyDefaults(Configuration config, List<Endpoint> endpoints, List<AlertRule> rules, List<AlertRecipient> recipients)
    {
        // Validate configuration using FluentValidation
        var validator = new ConfigurationValidator();
        var result = validator.Validate(config);

        if (!result.IsValid)
        {
            foreach (var error in result.Errors)
            {
                _logger.LogWarning(
                    "Invalid configuration detected. Field: {Field}, Error: {Error}",
                    error.PropertyName,
                    error.ErrorMessage);
            }
        }

        // ... additional validation for endpoints, rules, recipients
    }

    private void ApplyHardcodedDefaults()
    {
        _configLock.EnterWriteLock();
        try
        {
            _configuration = new Configuration
            {
                PollingIntervalSeconds = 60,
                MaxParallelism = 10,
                HealthCheckTimeoutSeconds = 30,
                RetryAttempts = 3,
                EmailSmtpPort = 587,
                EmailSmtpUseSsl = true
            };
            _endpoints = new List<Endpoint>();
            _alertRules = new List<AlertRule>();
            _alertRecipients = new List<AlertRecipient>();
        }
        finally
        {
            _configLock.ExitWriteLock();
        }
    }
}
```

#### ConfigurationValidator.cs

```csharp
public class ConfigurationValidator : AbstractValidator<Configuration>
{
    public ConfigurationValidator()
    {
        RuleFor(c => c.PollingIntervalSeconds)
            .GreaterThanOrEqualTo(1)
            .WithMessage("Polling interval must be at least 1 second");

        RuleFor(c => c.MaxParallelism)
            .GreaterThanOrEqualTo(1)
            .LessThanOrEqualTo(100)
            .WithMessage("Max parallelism must be between 1 and 100");

        RuleFor(c => c.HealthCheckTimeoutSeconds)
            .GreaterThanOrEqualTo(5)
            .WithMessage("Health check timeout must be at least 5 seconds");

        RuleFor(c => c.EmailSmtpHost)
            .NotEmpty()
            .WithMessage("Email SMTP host is required");

        RuleFor(c => c.EmailFromAddress)
            .EmailAddress()
            .WithMessage("Email from address must be valid");
    }
}

public class EndpointValidator : AbstractValidator<Endpoint>
{
    public EndpointValidator()
    {
        RuleFor(e => e.Name)
            .NotEmpty()
            .Length(1, 256);

        RuleFor(e => e.ServerName)
            .NotEmpty()
            .Length(1, 256);

        RuleFor(e => e.Port)
            .GreaterThanOrEqualTo(1)
            .LessThanOrEqualTo(65535)
            .WithMessage("Port must be between 1 and 65535");

        RuleFor(e => e.Environment)
            .Must(env => env == Environment.Development || env == Environment.Test || env == Environment.Production)
            .WithMessage("Environment must be Development, Test, or Production");
    }
}

public class AlertRuleValidator : AbstractValidator<AlertRule>
{
    public AlertRuleValidator()
    {
        RuleFor(a => a.Name)
            .NotEmpty()
            .Length(1, 256);

        RuleFor(a => a.ThresholdValue)
            .GreaterThanOrEqualTo(0)
            .WithMessage("Threshold value cannot be negative");

        RuleFor(a => a.DurationSeconds)
            .GreaterThanOrEqualTo(1)
            .WithMessage("Duration must be at least 1 second");
    }
}

public class AlertRecipientValidator : AbstractValidator<AlertRecipient>
{
    public AlertRecipientValidator()
    {
        RuleFor(a => a.EmailAddress)
            .EmailAddress()
            .WithMessage("Email address must be valid");
    }
}
```

---

### Infrastructure Layer

#### ConfigurationRepository.cs (OmniWatchAI.Infrastructure/Repositories/)

```csharp
public class ConfigurationRepository : IConfigurationRepository
{
    private readonly ISqlConnectionFactory _connectionFactory;
    private readonly ILogger<ConfigurationRepository> _logger;

    public async Task<Configuration> GetConfigurationAsync(CancellationToken cancellationToken)
    {
        const string sql = @"
            SELECT TOP 1 Id, PollingIntervalSeconds, MaxParallelism, HealthCheckTimeoutSeconds,
                   RetryAttempts, EmailSmtpHost, EmailSmtpPort, EmailSmtpUseSsl, EmailFromAddress, LastModified
            FROM Configuration
            ORDER BY Id DESC";

        using var connection = _connectionFactory.CreateConnection();
        var config = await connection.QueryFirstOrDefaultAsync<Configuration>(sql);

        if (config == null)
            throw new ConfigurationException("No configuration found in database");

        return config;
    }

    public async Task<List<Endpoint>> GetAllEndpointsAsync(CancellationToken cancellationToken)
    {
        const string sql = @"
            SELECT Id, Name, ServerName, InstanceName, Port, Environment, Enabled,
                   ConnectionStringTemplate, LastModified
            FROM Endpoints
            WHERE Enabled = 1
            ORDER BY Name";

        using var connection = _connectionFactory.CreateConnection();
        var endpoints = await connection.QueryAsync<Endpoint>(sql);
        return endpoints.ToList();
    }

    public async Task<EndpointConfiguration> GetEndpointConfigurationAsync(int endpointId, CancellationToken cancellationToken)
    {
        const string sql = @"
            SELECT Id, EndpointId, PollingIntervalSeconds, HealthCheckTimeoutSeconds,
                   RetryAttempts, LastModified
            FROM EndpointConfiguration
            WHERE EndpointId = @EndpointId";

        using var connection = _connectionFactory.CreateConnection();
        var config = await connection.QueryFirstOrDefaultAsync<EndpointConfiguration>(sql, new { EndpointId = endpointId });
        return config;
    }

    public async Task<List<AlertRule>> GetAllAlertRulesAsync(CancellationToken cancellationToken)
    {
        const string sql = @"
            SELECT Id, Name, AlertType, Severity, MetricName, ThresholdValue, ThresholdUnit,
                   DurationSeconds, Enabled, LastModified
            FROM AlertRules
            WHERE Enabled = 1
            ORDER BY Name";

        using var connection = _connectionFactory.CreateConnection();
        var rules = await connection.QueryAsync<AlertRule>(sql);
        return rules.ToList();
    }

    public async Task<List<AlertRecipient>> GetAllAlertRecipientsAsync(CancellationToken cancellationToken)
    {
        const string sql = @"
            SELECT Id, EmailAddress, AlertRuleId, Environment, MinimumSeverity, Enabled, LastModified
            FROM AlertRecipients
            WHERE Enabled = 1
            ORDER BY EmailAddress";

        using var connection = _connectionFactory.CreateConnection();
        var recipients = await connection.QueryAsync<AlertRecipient>(sql);
        return recipients.ToList();
    }

    public async Task<DateTime> GetLastModifiedTimestampAsync(CancellationToken cancellationToken)
    {
        const string sql = @"
            SELECT MAX(LastModified) as LastModified
            FROM (
                SELECT MAX(LastModified) as LastModified FROM Configuration
                UNION ALL
                SELECT MAX(LastModified) as LastModified FROM Endpoints
                UNION ALL
                SELECT MAX(LastModified) as LastModified FROM AlertRules
                UNION ALL
                SELECT MAX(LastModified) as LastModified FROM AlertRecipients
                UNION ALL
                SELECT MAX(LastModified) as LastModified FROM EndpointConfiguration
            ) AS AllTables";

        using var connection = _connectionFactory.CreateConnection();
        var timestamp = await connection.QueryFirstOrDefaultAsync<DateTime?>(sql);
        return timestamp ?? DateTime.UtcNow;
    }
}
```

#### AuditLogRepository.cs

```csharp
public class AuditLogRepository : IAuditLogRepository
{
    private readonly ISqlConnectionFactory _connectionFactory;

    public async Task LogChangeAsync(AuditLog auditLog, CancellationToken cancellationToken)
    {
        const string sql = @"
            INSERT INTO AuditLog (TableName, OperationType, ColumnName, OldValue, NewValue,
                                 RecordId, UserName, ChangeTimestamp, IpAddress, SessionId)
            VALUES (@TableName, @OperationType, @ColumnName, @OldValue, @NewValue,
                   @RecordId, @UserName, @ChangeTimestamp, @IpAddress, @SessionId)";

        using var connection = _connectionFactory.CreateConnection();
        await connection.ExecuteAsync(sql, auditLog);
    }
}
```

---

### ConfigurationReloader Worker (OmniWatchAI.PollingService/Workers/)

```csharp
public class ConfigurationReloader : BackgroundWorker
{
    private readonly IConfigurationService _configurationService;
    private readonly ILogger<ConfigurationReloader> _logger;
    private readonly System.Timers.Timer _reloadTimer;
    private DateTime _lastModifiedTimestamp;

    public ConfigurationReloader(IConfigurationService configurationService, ILogger<ConfigurationReloader> logger)
    {
        _configurationService = configurationService ?? throw new ArgumentNullException(nameof(configurationService));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));

        // Check for configuration changes every 30 seconds
        _reloadTimer = new System.Timers.Timer(TimeSpan.FromSeconds(30).TotalMilliseconds);
        _reloadTimer.Elapsed += OnReloadTimerElapsed;
        _reloadTimer.AutoReset = false;
    }

    public void Start()
    {
        _reloadTimer.Start();
        _logger.LogInformation("Configuration reloader started. Checking for changes every 30 seconds.");
    }

    public void Stop()
    {
        _reloadTimer.Stop();
        _reloadTimer.Dispose();
        _logger.LogInformation("Configuration reloader stopped.");
    }

    private async void OnReloadTimerElapsed(object sender, System.Timers.ElapsedEventArgs e)
    {
        try
        {
            // Check if configuration has been modified
            var currentTimestamp = await _configurationService.GetLastModifiedTimestampAsync(CancellationToken.None);

            if (currentTimestamp > _lastModifiedTimestamp)
            {
                _logger.LogInformation("Configuration change detected. Reloading configuration...");
                await _configurationService.LoadConfigurationAsync(CancellationToken.None);
                _lastModifiedTimestamp = currentTimestamp;
                _logger.LogInformation("Configuration reloaded successfully.");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error while checking for configuration changes.");
        }
        finally
        {
            _reloadTimer.Start();
        }
    }
}
```

---

### Non-Functional Requirements

#### Performance Requirements

| Requirement | Target | Measurement |
|-------------|--------|------------|
| Configuration load on service start | < 2 seconds | Stopwatch measurement in logs |
| Per-endpoint polling interval override lookup | < 1 millisecond | In-memory dictionary lookup |
| Configuration reload detection (polling interval) | 30 seconds (configurable) | Timer interval |
| Audit log write latency | < 50 milliseconds | Async non-blocking insert |
| Configuration reloader CPU overhead | < 1% | Task Manager measurement |

**Performance Validation Tests:**
- Load 200 endpoints, 100 alert rules, 500 recipients in < 2 seconds
- Per-endpoint configuration lookup 10,000 times in < 10 milliseconds (1 microsecond average)
- Configuration reload with 500 configuration changes in < 500 milliseconds

---

#### Security Requirements

- **Audit Trail:** All configuration changes logged with user, timestamp, old/new values
- **Access Control:** Only DBA or admin can modify configuration tables (SQL Server permissions)
- **Secrets Management:** SMTP password stored securely in application configuration (not in database)
- **Email Validation:** All email addresses validated before storage (FluentValidation)
- **SQL Injection Prevention:** All database queries parameterized (Dapper with @Parameter syntax)

---

#### Reliability Requirements

- **Graceful Degradation:** Service starts even if database is unavailable (uses safe defaults)
- **Failover:** Configuration reload retries indefinitely with exponential backoff
- **Data Consistency:** Atomic configuration updates (ReaderWriterLockSlim)
- **Error Logging:** All configuration errors logged with full context (timestamp, values, error details)

---

## Implementation Notes

### Key Implementation Decisions

1. **Change Detection:** Use polling `MAX(LastModified)` query every 30 seconds (simpler than SQL Server Change Tracking, sufficient for MVP)
2. **Thread-Safe Updates:** Use `ReaderWriterLockSlim` for atomic configuration updates (allows concurrent reads, serialized writes)
3. **Audit Logging:** Asynchronous (fire-and-forget) to avoid blocking configuration operations
4. **Safe Defaults:** Use globally accessible constant class (e.g., `SafeDefaults.cs`) for default values
5. **Validation:** FluentValidation for all configuration entities (DDD pattern)

### Files to Create

**Domain Layer:**
- `src/OmniWatchAI.Domain/Entities/Configuration.cs`
- `src/OmniWatchAI.Domain/Entities/AlertRule.cs`
- `src/OmniWatchAI.Domain/Entities/AlertRecipient.cs`
- `src/OmniWatchAI.Domain/Entities/EndpointConfiguration.cs`
- `src/OmniWatchAI.Domain/Entities/AuditLog.cs`
- `src/OmniWatchAI.Domain/Interfaces/IConfigurationRepository.cs`
- `src/OmniWatchAI.Domain/Interfaces/IAuditLogRepository.cs`

**Application Layer:**
- `src/OmniWatchAI.Application/Configuration/IConfigurationService.cs`
- `src/OmniWatchAI.Application/Configuration/ConfigurationService.cs`
- `src/OmniWatchAI.Application/Configuration/ConfigurationValidator.cs`
- `src/OmniWatchAI.Application/Configuration/EndpointValidator.cs`
- `src/OmniWatchAI.Application/Configuration/AlertRuleValidator.cs`
- `src/OmniWatchAI.Application/Configuration/AlertRecipientValidator.cs`

**Infrastructure Layer:**
- `src/OmniWatchAI.Infrastructure/Repositories/ConfigurationRepository.cs`
- `src/OmniWatchAI.Infrastructure/Repositories/AuditLogRepository.cs`
- `src/OmniWatchAI.Infrastructure/Configuration/SafeDefaults.cs`

**Polling Service:**
- `src/OmniWatchAI.PollingService/Workers/ConfigurationReloader.cs`

**Tests:**
- `tests/UnitTests/Application.UnitTests/Configuration/ConfigurationServiceTests.cs`
- `tests/UnitTests/Application.UnitTests/Configuration/ConfigurationValidatorTests.cs`
- `tests/IntegrationTests/Infrastructure.IntegrationTests/Repositories/ConfigurationRepositoryTests.cs`

### Database Migration

Create EF Core migration file:
```
src/OmniWatchAI.Infrastructure/Migrations/20250115_AddConfigurationTables.cs
```

---

## Dependencies

**Hard Dependencies:**
- STORY-001 (Windows Service Framework - PollingService) MUST be completed first (ConfigurationReloader runs in PollingService)
- STORY-002 (Windows Service Framework - AlertingService) SHOULD be completed first (both services need configuration)

**Soft Dependencies:**
- EPIC-002: SQL Server Health Checks (will use configuration for polling intervals)

---

## Definition of Done

- [ ] All 5 configuration tables created (Configuration, Endpoints, AlertRules, AlertRecipients, EndpointConfiguration, AuditLog)
- [ ] Domain entities created with proper validation rules
- [ ] ConfigurationService loads all configuration < 2 seconds
- [ ] FluentValidation validators applied to all entities
- [ ] ConfigurationReloader detects changes and reloads without restart
- [ ] Safe defaults applied when configuration is invalid
- [ ] Audit logging captures all configuration changes
- [ ] Per-endpoint configuration overrides work correctly
- [ ] Thread-safe updates verified via concurrent access tests
- [ ] All acceptance criteria have passing tests
- [ ] Code review approved (architecture-constraints.md compliance)
- [ ] Unit tests: 95% coverage of ConfigurationService
- [ ] Integration tests: ConfigurationRepository tested against real SQL Server (Testcontainers)
- [ ] Documentation updated with configuration table schemas and usage examples
- [ ] No CRITICAL or HIGH violations from QA deep validation

---

## Implementation Notes

*To be completed during development by devforgeai-development skill*

### Phase 1: Red (Test Creation)
- Create failing unit tests for ConfigurationService
- Create integration tests for ConfigurationRepository
- Verify all acceptance criteria have test coverage

### Phase 2: Green (Implementation)
- Implement domain entities with validation
- Implement ConfigurationService with thread-safe configuration loading
- Implement ConfigurationRepository using Dapper
- Implement ConfigurationReloader for change detection
- Implement audit logging mechanism

### Phase 3: Refactor
- Extract common validation logic
- Optimize database queries
- Apply SOLID principles
- Code quality improvements

### Phase 4: Integration Testing
- Test with Testcontainers.MsSql
- Verify configuration load performance < 2 seconds
- Test concurrent configuration updates
- Test database failure scenarios

---

**Story ID:** STORY-003
**Created:** 2025-01-15
**Last Updated:** 2025-01-15
**Status:** Ready for Development
