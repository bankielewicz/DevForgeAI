# STORY-003 Configuration Management - Summary

## Story Overview

**Story ID:** STORY-003
**Title:** Configuration Management - Database-Driven Configuration with Audit Logging
**Epic:** EPIC-001 (Core Monitoring Infrastructure)
**Story Points:** 8
**Priority:** High
**Status:** Backlog

## User Story Statement

As a **system administrator**, I want to **load all operational parameters from the database on service start and detect configuration changes without requiring a service restart**, so that **I can manage monitoring behavior dynamically without service downtime, maintain an audit trail of all configuration changes for compliance, and apply safe defaults when invalid configuration is detected**.

---

## Key Acceptance Criteria (8 Scenarios)

### 1. ✅ Configuration Loaded on Service Start (< 2 seconds)
- Configuration, Endpoints, AlertRules, AlertRecipients, and AuditLog tables loaded from database
- All configuration values strongly typed (not strings)
- Load duration measured and logged

**Performance Validation:** Load 200 endpoints, 100 alert rules, 500 recipients in < 2 seconds

### 2. ✅ Strong Typing and Validation on Load
- FluentValidation applied to all configuration entities
- Invalid configurations logged as warnings (not service-breaking)
- Safe default values applied (PollingInterval: 60s, MaxParallelism: 10, etc.)

**Default Values:**
- PollingIntervalSeconds: 60
- MaxParallelism: 10
- HealthCheckTimeoutSeconds: 30
- RetryAttempts: 3

### 3. ✅ Change Detection and Reload Without Service Restart
- ConfigurationReloader detects changes every 30 seconds
- New configuration loaded from database
- In-memory configuration atomically updated (ReaderWriterLockSlim)
- In-flight health checks continue with old config (safe switchover)

**Implementation:** Polling `MAX(LastModified)` query every 30 seconds

### 4. ✅ Audit Logging for All Configuration Changes
- AuditLog table records: user, timestamp, operation type, old value, new value
- Captures: INSERT, UPDATE, DELETE operations
- Asynchronous logging (non-blocking)
- Includes IP address and session identifier

**Audit Log Captures:**
- TableName (Configuration, Endpoints, AlertRules, AlertRecipients)
- OperationType (INSERT, UPDATE, DELETE)
- ColumnName, OldValue, NewValue
- UserName, ChangeTimestamp (UTC), IpAddress, SessionId

### 5. ✅ Invalid Configuration Handling with Safe Defaults
- Invalid values logged with context (field, invalid value, default used)
- Service continues running with safe defaults (doesn't crash)
- Invalid configurations NOT persisted back to database

**Example:** PollingInterval = -5 → Use default 60, log warning

### 6. ✅ Per-Endpoint Configuration Overrides
- EndpointConfiguration table provides per-endpoint overrides
- Overrides merged with global configuration
- Missing overrides fall back to global configuration
- Validation applies to both global and override values

**Example:**
- Global: PollingIntervalSeconds = 60
- Endpoint override (critical): PollingIntervalSeconds = 10
- Loaded config uses 10 for that endpoint, 60 for others

### 7. ✅ Database Connection Failure Handling
- When database unavailable on startup, service logs error and uses hardcoded defaults
- Service continues running in degraded mode
- Configuration reload retries every 30 seconds
- When database becomes available, configuration is reloaded

### 8. ✅ Concurrent Configuration Updates
- In-memory configuration update is atomic (all-or-nothing)
- No partial updates or race conditions
- Thread-safe using ReaderWriterLockSlim
- Multiple concurrent reads allowed (health checks reading config)

---

## Database Schema (6 Tables)

### Configuration Table
```
Id, PollingIntervalSeconds, MaxParallelism, HealthCheckTimeoutSeconds,
RetryAttempts, EmailSmtpHost, EmailSmtpPort, EmailSmtpUseSsl,
EmailFromAddress, LastModified
```

### Endpoints Table
```
Id, Name, ServerName, InstanceName, Port, Environment, Enabled,
ConnectionStringTemplate, LastModified
```

### AlertRules Table
```
Id, Name, AlertType, Severity, MetricName, ThresholdValue,
ThresholdUnit, DurationSeconds, Enabled, LastModified
```

### AlertRecipients Table
```
Id, EmailAddress, AlertRuleId, Environment, MinimumSeverity,
Enabled, LastModified
```

### EndpointConfiguration Table (Per-Endpoint Overrides)
```
Id, EndpointId, PollingIntervalSeconds, HealthCheckTimeoutSeconds,
RetryAttempts, LastModified
```

### AuditLog Table
```
Id, TableName, OperationType, ColumnName, OldValue, NewValue,
RecordId, UserName, ChangeTimestamp, IpAddress, SessionId
```

---

## Architecture & Implementation

### Clean Architecture Layers

**Domain Layer (OmniWatchAI.Domain)**
- Configuration, AlertRule, AlertRecipient, EndpointConfiguration, AuditLog entities
- Repository interfaces (IConfigurationRepository, IAuditLogRepository)
- Pure business logic - no infrastructure dependencies

**Application Layer (OmniWatchAI.Application)**
- ConfigurationService (load, validate, provide access to configuration)
- Validators using FluentValidation:
  - ConfigurationValidator
  - EndpointValidator
  - AlertRuleValidator
  - AlertRecipientValidator

**Infrastructure Layer (OmniWatchAI.Infrastructure)**
- ConfigurationRepository (Dapper implementation)
- AuditLogRepository (Dapper implementation)
- SafeDefaults class with constant values

**Polling Service (OmniWatchAI.PollingService)**
- ConfigurationReloader worker (detects changes, triggers reload)

---

## Technical Specifications

### ConfigurationService Interface
```csharp
public interface IConfigurationService
{
    Task LoadConfigurationAsync(CancellationToken cancellationToken);
    Configuration GetConfiguration();
    List<Endpoint> GetAllEndpoints();
    List<AlertRule> GetAllAlertRules();
    List<AlertRecipient> GetAllAlertRecipients();
    int GetPollingInterval(int endpointId);  // With per-endpoint override
    int GetHealthCheckTimeout(int endpointId);
    int GetRetryAttempts(int endpointId);
}
```

### Key Implementation Details

**Thread-Safe Configuration Updates:**
- ReaderWriterLockSlim for atomic updates
- Multiple concurrent reads allowed
- Configuration updates serialized

**Configuration Loading:**
- Validate all entities with FluentValidation
- Apply safe defaults on validation failure
- Log all validation errors and defaults applied
- Measure load time and log performance

**Change Detection:**
- Polling mechanism: Query `MAX(LastModified)` every 30 seconds
- Compare timestamp with previous check
- On change detected, reload entire configuration

**Audit Logging:**
- Capture all INSERT/UPDATE/DELETE operations
- Store in AuditLog table asynchronously
- Include user, timestamp, old value, new value

---

## Non-Functional Requirements

### Performance
- Configuration load < 2 seconds (200 endpoints)
- Per-endpoint override lookup < 1 millisecond
- Change detection every 30 seconds (configurable)
- Audit log write < 50 milliseconds (async)

### Security
- Audit trail for compliance
- SQL injection prevention (Dapper parameterized queries)
- Email validation (FluentValidation)
- Secrets management (SMTP password in appsettings, not database)

### Reliability
- Graceful degradation (safe defaults if database unavailable)
- Failover with exponential backoff
- Atomic configuration updates
- Comprehensive error logging

---

## Files to Create

### Domain Layer (5 files)
- `src/OmniWatchAI.Domain/Entities/Configuration.cs`
- `src/OmniWatchAI.Domain/Entities/AlertRule.cs`
- `src/OmniWatchAI.Domain/Entities/AlertRecipient.cs`
- `src/OmniWatchAI.Domain/Entities/EndpointConfiguration.cs`
- `src/OmniWatchAI.Domain/Entities/AuditLog.cs`
- `src/OmniWatchAI.Domain/Interfaces/IConfigurationRepository.cs`
- `src/OmniWatchAI.Domain/Interfaces/IAuditLogRepository.cs`

### Application Layer (7 files)
- `src/OmniWatchAI.Application/Configuration/IConfigurationService.cs`
- `src/OmniWatchAI.Application/Configuration/ConfigurationService.cs`
- `src/OmniWatchAI.Application/Configuration/ConfigurationValidator.cs`
- `src/OmniWatchAI.Application/Configuration/EndpointValidator.cs`
- `src/OmniWatchAI.Application/Configuration/AlertRuleValidator.cs`
- `src/OmniWatchAI.Application/Configuration/AlertRecipientValidator.cs`

### Infrastructure Layer (3 files)
- `src/OmniWatchAI.Infrastructure/Repositories/ConfigurationRepository.cs`
- `src/OmniWatchAI.Infrastructure/Repositories/AuditLogRepository.cs`
- `src/OmniWatchAI.Infrastructure/Configuration/SafeDefaults.cs`

### Polling Service (1 file)
- `src/OmniWatchAI.PollingService/Workers/ConfigurationReloader.cs`

### Database Migration (1 file)
- `src/OmniWatchAI.Infrastructure/Migrations/20250115_AddConfigurationTables.cs` (EF Core migration)

### Tests (3 files)
- `tests/UnitTests/Application.UnitTests/Configuration/ConfigurationServiceTests.cs`
- `tests/UnitTests/Application.UnitTests/Configuration/ConfigurationValidatorTests.cs`
- `tests/IntegrationTests/Infrastructure.IntegrationTests/Repositories/ConfigurationRepositoryTests.cs`

---

## Dependencies

**Hard Dependency:**
- STORY-001 (Windows Service Framework - PollingService)
  - ConfigurationReloader runs in PollingService context
  - Must be completed first

**Soft Dependency:**
- STORY-002 (Windows Service Framework - AlertingService)
  - AlertingService also uses configuration

---

## INVEST Principles Compliance

✅ **Independent:** Can be developed independently (only depends on STORY-001)
✅ **Negotiable:** Details can be refined (change detection mechanism, validation rules)
✅ **Valuable:** Delivers system administrator value (dynamic configuration management)
✅ **Estimable:** Well-defined scope (8 acceptance criteria, clear schema, implementation patterns)
✅ **Small:** Can be completed in one sprint (8 story points)
✅ **Testable:** All acceptance criteria are testable and measurable

---

## Quality Standards

**Code Coverage Targets:**
- ConfigurationService: 95% coverage
- ConfigurationRepository: 85% coverage
- Validators: 90% coverage

**Test Types:**
- Unit tests: ConfigurationService, Validators
- Integration tests: ConfigurationRepository (Testcontainers.MsSql)
- Performance tests: Configuration load time < 2 seconds

**Code Quality:**
- No cross-layer dependencies
- Pure domain entities (no infrastructure dependencies)
- Dapper for all data access
- FluentValidation for all validation
- Async/await patterns throughout

---

## Key Implementation Decisions

1. **Change Detection:** Polling mechanism (simpler, sufficient for MVP)
2. **Thread Safety:** ReaderWriterLockSlim (allows concurrent reads)
3. **Validation Framework:** FluentValidation (testable, expressive)
4. **Safe Defaults:** Hardcoded constants when database unavailable
5. **Audit Logging:** Asynchronous (fire-and-forget) for performance

---

## Success Criteria Summary

| Criteria | Target | Status |
|----------|--------|--------|
| Load time | < 2 seconds | Acceptance Criteria #1 |
| Change detection | 30 seconds | Acceptance Criteria #3 |
| Thread-safe updates | Atomic | Acceptance Criteria #8 |
| Invalid config handling | Safe defaults applied | Acceptance Criteria #5 |
| Audit trail | All changes logged | Acceptance Criteria #4 |
| Per-endpoint overrides | Supported | Acceptance Criteria #6 |
| Database failure | Graceful degradation | Acceptance Criteria #7 |
| Code coverage | 95% ConfigurationService | Definition of Done |

---

**Complete Story File:** `.ai_docs/Stories/STORY-003-configuration-management-database-driven.story.md`

**Ready for:** Development with `/dev STORY-003` command
