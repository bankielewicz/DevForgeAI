# Windows Service Framework - Complete Requirements Summary

**Date:** 2025-01-15
**Project:** OmniWatchAI
**Epic:** EPIC-001 (Core Monitoring Infrastructure)
**Stories:** STORY-001, STORY-002

---

## Overview

The Windows Service Framework establishes the foundational infrastructure for two independent Windows Services:

1. **PollingService (STORY-001):** Executes health checks on SQL Server instances
2. **AlertingService (STORY-002):** Detects alerts and sends notifications

Both services implement Windows Service lifecycle management with:
- Graceful shutdown support (30-second grace period for in-flight operations)
- Auto-recovery configuration (automatic restart on crashes)
- Comprehensive logging (file, Event Log, database)
- CancellationToken-based operation coordination
- Clean Architecture principles (thin service layer, Application layer orchestration)

---

## Why Two Separate Services?

**Fault Isolation & Independent Scaling:**
- If PollingService crashes, AlertingService continues running (alerts still get sent)
- If AlertingService crashes, health checks continue (results queue for later alerting)
- Services can be scaled independently in future

**Clean Responsibility:**
- PollingService = Health check execution only
- AlertingService = Alert detection and email notification only
- Each service focuses on single responsibility

**Operational Flexibility:**
- Can restart PollingService without interrupting alerts
- Can restart AlertingService without interrupting checks
- Reduces maintenance window impact

---

## User Stories Overview

### STORY-001: PollingService Lifecycle Management (8 points)

**Primary Focus:** Windows Service lifecycle, graceful shutdown, auto-recovery

**Key Features:**
1. Service startup (< 5 seconds)
2. Graceful shutdown with in-flight check coordination (30s timeout)
3. Auto-recovery from crashes (Windows SCM)
4. CancellationToken propagation to all operations
5. Configuration loading from database (< 2 seconds)
6. Comprehensive logging (file, Event Log, database)
7. Service installation script (PowerShell)
8. Error handling during lifecycle
9. Single instance protection
10. Service health status reporting

**Acceptance Criteria:** 10 detailed scenarios covering happy path, edge cases, and error conditions

**Testing Approach:**
- Unit tests: Lifecycle logic, error handling
- Integration tests: Real database, actual service operations
- Manual testing: Service installation, SCM interaction, recovery

**Related Files to Create:**
- `src/OmniWatchAI.PollingService/PollingService.cs` (ServiceBase implementation)
- `src/OmniWatchAI.PollingService/Lifetime/ServiceLifecycleManager.cs`
- `src/OmniWatchAI.PollingService/Lifetime/GracefulShutdownHandler.cs`
- `src/OmniWatchAI.PollingService/Program.cs` (DI setup)
- Configuration classes and settings
- Comprehensive unit and integration tests

---

### STORY-002: AlertingService Lifecycle Management (5 points)

**Primary Focus:** Alert detection and email sending with same lifecycle patterns

**Key Features:**
1. Service startup (< 5 seconds)
2. Graceful shutdown with email operation coordination (30s timeout)
3. Auto-recovery from crashes
4. Alert detection from health check results
5. Alert routing to recipients based on environment/severity
6. Email sending with retry logic (3 attempts, 5-minute intervals)
7. Error handling for SMTP failures
8. Comprehensive logging

**Acceptance Criteria:** 10 scenarios covering alert detection, email operations, lifecycle events

**Testing Approach:**
- Unit tests: Alert detection logic, email retry
- Integration tests: Real database, real SMTP
- Manual testing: Email delivery verification, alert detection

**Related Files to Create:**
- `src/OmniWatchAI.AlertingService/AlertingService.cs`
- `src/OmniWatchAI.AlertingService/Lifetime/ServiceLifecycleManager.cs`
- Alert detection and email workers
- SMTP configuration and email templates
- Tests for alert detection, email sending, lifecycle

---

## Technical Requirements

### Windows Service Implementation

**Technology Stack (per tech-stack.md):**
- Framework: `.NET 8.0 LTS`
- Language: `C# 12.0`
- Hosting Model: `System.ServiceProcess.ServiceBase` (Windows Service)
- Database: `SQL Server 2022` with `Dapper 2.1.x` (data access)
- Logging: `Serilog 3.x` (structured logging)
- DI Container: `Microsoft.Extensions.DependencyInjection` (built-in)

**Architecture Pattern (per architecture-constraints.md):**
- Clean Architecture (4 layers)
- Presentation: PollingService/AlertingService (thin wrapper)
- Application: Orchestrators and use cases (business logic)
- Domain: Entities and value objects (pure business logic)
- Infrastructure: Repositories and data access (Dapper)

**Key Patterns:**
1. **Constructor Injection** - All dependencies injected via constructor
2. **Graceful Shutdown** - CancellationToken + 30-second timeout
3. **Async/Await** - All async operations, ConfigureAwait(false) in libraries
4. **Structured Logging** - Serilog with multiple sinks
5. **Repository Pattern** - All data access through repositories

### Graceful Shutdown Flow

```
1. Service receives stop signal (Windows SCM)
   ↓
2. OnStop() method called
   ↓
3. CancellationTokenSource created (30-second timeout)
   ↓
4. Cancellation token passed to all in-flight operations
   ↓
5. ServiceLifecycleManager.WaitForGracefulShutdown() waits for operations
   ↓
6. Operations complete or timeout at 30 seconds
   ↓
7. Service exits cleanly
   ↓
8. If timeout: service logs warning and force-exits at 35 seconds
```

### Auto-Recovery Configuration

**Windows Service Recovery Policy:**

```
Service: OmniWatchAI.PollingService / OmniWatchAI.AlertingService
Failures:
  - First failure:       Restart service (5 seconds delay)
  - Second failure:      Restart service (5 seconds delay)
  - Subsequent failures: Restart service (5 seconds delay)
  - Max restart attempts: 3 (configurable)
Configured via: PowerShell script or Registry
```

**Validation:**
- Registry key: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\OmniWatchAI.PollingService`
- FailureActions: First, Second, Subsequent = Restart (1)

### Logging Strategy

**Log Destinations (Serilog):**

1. **File Sink** (Rolling file)
   - Location: `C:\Logs\OmniWatchAI.PollingService\{date}.log`
   - Format: Structured (timestamp, level, message, context)
   - Retention: 30 days (older files deleted)

2. **Windows Event Log Sink**
   - Source: "OmniWatchAI.PollingService"
   - Events: Critical failures, service start/stop
   - For: System administrators monitoring

3. **Database Sink** (SQL Server)
   - Table: `AuditLog`
   - Fields: Timestamp, ServiceName, EventType, Message, Context
   - For: Compliance and historical analysis

**Log Levels:**
- `DEBUG`: Detailed operation flow (development only)
- `INFO`: Service lifecycle, normal operations
- `WARNING`: Recoverable errors, timeouts, retries
- `ERROR`: Critical failures requiring attention
- `FATAL`: Service-killing errors

**Sensitive Data Protection:**
- NO passwords in logs
- NO connection strings with credentials
- NO API keys or tokens
- Email addresses: partially obfuscated (user@***.com)

---

## Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| Service Startup | < 5 seconds | Time from Services.msc start to "Running" state |
| Configuration Load | < 2 seconds | Time to load 200+ endpoints from database |
| Graceful Shutdown | < 30 seconds | Time for in-flight operations to complete |
| Memory (Startup) | < 200 MB | Excluding health check operations |
| Health Check Execution | < 30 seconds per check | Timeout threshold per endpoint |
| Database Batch Insert | < 100 ms | Bulk insert of 200 health check results |
| SMTP Email Send | < 10 seconds | Per email via SMTP |
| Alert Detection | < 5 seconds | Scan 200 endpoints for alert conditions |

---

## Error Handling Strategy

### Scenario 1: Database Unavailable at Startup

**PollingService:**
- Attempt database connection (3 retries, 1-second intervals)
- If all fail: Load safe defaults, log warning
- Service starts (doesn't crash)
- Next scheduled poll will retry database

**AlertingService:**
- Same approach (configuration tables required)
- Continue running with cached configuration if available

### Scenario 2: SMTP Server Unreachable

**AlertingService:**
- Log warning (SMTP connection failed)
- Queue email for retry (5-minute interval)
- Retry up to 3 times total
- If all retries fail: Log error, move to next email
- Service continues (doesn't crash)

### Scenario 3: Health Check Hangs (Network Timeout)

**PollingService:**
- CancellationToken timeout at 30 seconds (per endpoint configuration)
- Operation cancelled, logged as timeout
- Result recorded: Failed (timeout)
- Service continues with next check

### Scenario 4: Service Stop Called During Long Operation

**Both Services:**
- Graceful shutdown initiated (30-second grace period)
- CancellationToken signalled to all operations
- Operations complete or timeout at 30 seconds
- Service exits cleanly
- Results persisted to database

### Scenario 5: Service Receives Unhandled Exception

**Both Services:**
- Exception caught at top level (OnStart/OnStop)
- Logged with full stack trace
- Service exits with error
- Windows SCM detects crash
- Auto-recovery triggered (after 5-second delay)
- Service restarted automatically

---

## Configuration Requirements

### PollingService Configuration

**appsettings.json:**

```json
{
  "PollingService": {
    "EnableAutoStart": true,
    "PollingIntervalSeconds": 60,
    "MaxConcurrentChecks": 10,
    "HealthCheckTimeoutSeconds": 30,
    "GracefulShutdownTimeoutSeconds": 30,
    "Logging": {
      "FilePath": "C:\\Logs\\OmniWatchAI.PollingService\\",
      "RetentionDays": 30
    }
  }
}
```

### AlertingService Configuration

**appsettings.json:**

```json
{
  "AlertingService": {
    "AlertDetectionIntervalSeconds": 120,
    "EmailRetryIntervalSeconds": 300,
    "MaxEmailRetries": 3,
    "SmtpHost": "smtp.company.com",
    "SmtpPort": 587,
    "SmtpUseTls": true,
    "SmtpUsername": "[from config database]",
    "SmtpPassword": "[from config database]"
  }
}
```

**Database Configuration Tables:**
- `Configuration` - Global settings (polling intervals, parallelism, email SMTP)
- `Endpoints` - SQL Server instances to monitor
- `AlertRules` - Alert thresholds
- `AlertRecipients` - Email recipients with routing rules
- `AuditLog` - Configuration changes and service events

---

## Testing Strategy

### Unit Tests (xUnit + Moq)

**PollingService Tests:**
- ServiceLifecycleManager: Graceful shutdown logic
- GracefulShutdownHandler: CancellationToken coordination
- Configuration loading: Parse settings, validate values
- Error handling: Specific exception handling in OnStart/OnStop
- Mocked: IHealthCheckOrchestrator, IConfigurationService, ILogger

**AlertingService Tests:**
- Alert detection logic (mock repositories)
- Email sending with retry (mock SMTP)
- Lifecycle management (same patterns as PollingService)
- Error handling (SMTP failures, database unavailable)

### Integration Tests (xUnit + Testcontainers)

**PollingService Integration:**
- Real SQL Server database (Docker container)
- Real configuration tables
- Actual service startup/stop cycle
- In-flight operation coordination
- Graceful shutdown with real health checks

**AlertingService Integration:**
- Real SQL Server database
- Real alert detection from health check results
- Real SMTP configuration (or mock SMTP for testing)
- Email send with retry logic
- Full lifecycle with real operations

### Manual Testing

**Service Installation:**
1. Run PowerShell installation script
2. Verify service in Services.msc
3. Verify auto-recovery policy configured
4. Start service manually

**Startup Verification:**
1. Check Windows Event Log for startup event
2. Check log file for configuration load message
3. Verify service state = Running
4. Verify workers initialized

**Graceful Shutdown:**
1. Start service, trigger health checks
2. Stop service while checks in-flight
3. Verify all results persisted
4. Verify service transitions to Stopped (not hanging)

**Auto-Recovery:**
1. Simulate service crash (throw exception)
2. Verify Windows Event Log shows crash
3. Wait 5 seconds
4. Verify service automatically restarts
5. Verify service resumes operations

---

## Deployment Checklist

### Pre-Deployment

- [ ] All unit tests pass (100% pass rate)
- [ ] All integration tests pass
- [ ] Code coverage: >= 95% business logic
- [ ] Code review approved
- [ ] No CRITICAL/HIGH severity violations
- [ ] Architecture and coding standards verified

### Deployment

- [ ] Windows Server 2022 environment ready
- [ ] Service account created (Network Service or custom account)
- [ ] Service account permissions: Read logs directory, write logs directory
- [ ] Logs directory created: `C:\Logs\OmniWatchAI.PollingService\` and `\AlertingService\`
- [ ] Installation scripts prepared (PowerShell)
- [ ] Database tables created (Configuration, Endpoints, AlertRules, etc.)
- [ ] Database migrations applied (EF Core)
- [ ] SMTP configuration available (for AlertingService)

### Post-Deployment

- [ ] Run installation script for PollingService
- [ ] Run installation script for AlertingService
- [ ] Start both services
- [ ] Verify both services running in Services.msc
- [ ] Check Windows Event Log for startup events
- [ ] Check log files for expected entries
- [ ] Monitor for 24 hours (baseline stability)

---

## Success Metrics

### Functional Success

**All Acceptance Criteria Met:**
- Both services start successfully
- Both services shut down gracefully
- Both services recover from crashes
- Health checks execute without data loss
- Alerts detected and sent reliably
- Configurations load correctly
- Logging complete and accessible

### Non-Functional Success

**Performance:**
- Service startup: < 5 seconds
- Configuration load: < 2 seconds
- Graceful shutdown: < 30 seconds
- Memory stable: < 200 MB at startup
- No memory leaks over 24-hour period

**Reliability:**
- 99.9% uptime (< 43 seconds downtime per month)
- Auto-recovery on all crash scenarios
- Zero data loss during shutdown
- All in-flight operations complete

**Quality:**
- Test coverage: >= 95% business logic
- Zero CRITICAL violations
- Zero HIGH violations
- Code review approved
- Documentation complete

---

## Dependencies & Sequencing

### Hard Dependencies

**STORY-001 (PollingService):**
- No hard external dependencies (foundation story)

**STORY-002 (AlertingService):**
- STORY-001 must complete first (needs health check results)

### Soft Dependencies

**Both Stories:**
- EPIC-001 Feature 2: Configuration Management (database-driven config)
- EPIC-001 Feature 4: Data Persistence (tables for results and alerts)

### Recommended Sequencing

```
Phase 1: Core Infrastructure (2 weeks)
├─ STORY-001: PollingService Framework (8 points, 3-4 days)
│  ├─ Develop lifecycle management
│  ├─ Implement graceful shutdown
│  ├─ Create installation script
│  ├─ Write comprehensive tests
│  └─ Deploy to staging
│
└─ STORY-002: AlertingService Framework (5 points, 2-3 days)
   ├─ Develop lifecycle management
   ├─ Implement alert detection
   ├─ Implement email sending
   ├─ Write comprehensive tests
   └─ Deploy to staging

Phase 2: Feature Development (follows after core infrastructure)
├─ STORY-003: Health Check Worker (parallel execution)
├─ STORY-004: Configuration Management
└─ STORY-005: Alert Detection Worker
```

---

## Risk Mitigation

### Risk 1: Service Crashes Under Load

**Probability:** Medium | **Impact:** High
**Mitigation:**
- Comprehensive exception handling in all lifecycle methods
- Graceful degradation (one failing check doesn't crash service)
- Auto-recovery configuration (automatic restart)
- Load testing before release (200 endpoints, max concurrency)

### Risk 2: Graceful Shutdown Hangs

**Probability:** Medium | **Impact:** High
**Mitigation:**
- Hard stop timeout (35 seconds maximum)
- Force-cancellation if grace period exceeded
- Comprehensive logging of shutdown progress
- Integration tests with hanging operations

### Risk 3: Database Connection Exhaustion

**Probability:** Medium | **Impact:** High
**Mitigation:**
- Connection pooling (SQL Client)
- Limit concurrent health checks (configurable max)
- Timeout per operation (30 seconds)
- Monitor connection pool status in logs

### Risk 4: In-Flight Data Loss During Stop

**Probability:** Low | **Impact:** Critical
**Mitigation:**
- Graceful shutdown forces completion of in-flight operations
- Results persisted in database before service exits
- Transactional consistency (batch inserts with rollback on error)
- Comprehensive integration tests verifying persistence

### Risk 5: SMTP Failures Causing Alert Loss

**Probability:** Medium | **Impact:** Medium
**Mitigation:**
- Retry logic (up to 3 attempts, 5-minute intervals)
- Alerts persisted in database (retry indefinitely if needed)
- Graceful degradation (one SMTP failure doesn't crash service)
- Error logging for troubleshooting

---

## Future Enhancements (Post-MVP)

1. **Web Dashboard:** ASP.NET Core web UI for configuration and monitoring
2. **Advanced Scheduling:** Hangfire for complex job scheduling
3. **Performance Monitoring:** Real-time metrics dashboard
4. **Automated Remediation:** Run scripts on alerts (restart services, etc.)
5. **Alert Escalation:** Escalate unresolved alerts to on-call
6. **Historical Analysis:** Long-term trend analysis and reporting
7. **Multi-Region Support:** Monitor multiple SQL Server regions
8. **Notification Channels:** Slack, PagerDuty, Teams integration

---

## Conclusion

The Windows Service Framework provides a robust, production-ready foundation for 24/7 SQL Server monitoring with:

- **Reliability:** 99.9% uptime through auto-recovery and graceful shutdown
- **Maintainability:** Clean Architecture enables easy testing and modification
- **Operability:** Comprehensive logging and monitoring for troubleshooting
- **Scalability:** Supports 51-200 endpoints with configurable parallelism
- **Security:** Secure credential handling, least-privilege service accounts

Both STORY-001 and STORY-002 follow INVEST principles:

✅ **Independent:** Can be developed and tested in isolation
✅ **Negotiable:** Implementation details can be refined
✅ **Valuable:** Delivers critical infrastructure for monitoring
✅ **Estimable:** Team can estimate effort (8 and 5 points respectively)
✅ **Small:** Can be completed in single sprint (combined 13 points)
✅ **Testable:** Detailed acceptance criteria enable comprehensive validation

---

**Document Version:** 1.0
**Last Updated:** 2025-01-15
**Created By:** DevForgeAI Requirements Analyst
**Status:** Complete and Ready for Development
