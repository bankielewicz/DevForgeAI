---
id: STORY-006
title: Windows Service Configuration Management and Runtime Behavior
epic: EPIC-001
sprint: Sprint-2
status: Backlog
priority: Medium
points: 3
type: Infrastructure
created: 2025-01-15
created_by: DevForgeAI Requirements Analyst
---

# STORY-006: Windows Service Configuration Management and Runtime Behavior

**Status**: Backlog
**Priority**: Medium
**Story Points**: 3
**Epic**: EPIC-001 (Core Monitoring Infrastructure)
**Sprint**: Sprint-2 (To be assigned)

---

## User Story

As a **System Administrator**,
I want **OmniWatchAI services to load configuration from appsettings.json with environment-specific overrides and validate configuration at startup**,
So that **I can customize service behavior (polling intervals, timeouts, SMTP settings) without recompiling the application and detect configuration errors before the service starts**.

---

## Acceptance Criteria

### Scenario 1: Load Configuration from appsettings.json at Startup

**Given** PollingService has `appsettings.json` in the service directory (`C:\Program Files\OmniWatchAI\`)
**And** `appsettings.json` contains:
```json
{
  "ConnectionStrings": {
    "OmniWatchDb": "Server=localhost;Database=OmniWatchAI;Integrated Security=true;"
  },
  "HealthCheck": {
    "DefaultPollingIntervalSeconds": 300,
    "MaxConcurrentChecks": 10,
    "DefaultTimeoutSeconds": 30
  },
  "Serilog": {
    "MinimumLevel": "Information"
  }
}
```
**When** I start PollingService
**Then**:
- Configuration loaded from `appsettings.json` within 1 second
- Settings are accessible via `IOptions<HealthCheckSettings>`
- Polling interval set to 300 seconds (5 minutes)
- Max concurrent checks set to 10
- Default timeout set to 30 seconds
- Database connection string used for all repository queries
- Service logs: `[INFO] Configuration loaded from appsettings.json. PollingInterval=300s, MaxConcurrent=10, Timeout=30s`

**Test Evidence:**
```csharp
// Unit test: Configuration loading
var config = serviceProvider.GetRequiredService<IOptions<HealthCheckSettings>>().Value;
Assert.Equal(300, config.DefaultPollingIntervalSeconds);
Assert.Equal(10, config.MaxConcurrentChecks);
Assert.Equal(30, config.DefaultTimeoutSeconds);
```

---

### Scenario 2: Environment-Specific Configuration Overrides (Production)

**Given** PollingService has both `appsettings.json` and `appsettings.Production.json`
**And** Environment variable `ASPNETCORE_ENVIRONMENT=Production` is set
**And** `appsettings.Production.json` contains:
```json
{
  "ConnectionStrings": {
    "OmniWatchDb": "Server=PROD-SQL-01;Database=OmniWatchAI;Integrated Security=true;"
  },
  "HealthCheck": {
    "DefaultPollingIntervalSeconds": 60,
    "MaxConcurrentChecks": 20
  },
  "Serilog": {
    "MinimumLevel": "Warning"
  }
}
```
**When** I start PollingService in Production environment
**Then**:
- Configuration loaded from `appsettings.json` first (base settings)
- Configuration from `appsettings.Production.json` overrides base settings
- Polling interval = 60 seconds (overridden from 300)
- Max concurrent checks = 20 (overridden from 10)
- Default timeout = 30 seconds (inherited from base, not overridden)
- Database connection string = `PROD-SQL-01` (overridden)
- Serilog minimum level = Warning (overridden from Information)
- Service logs: `[WARN] Configuration loaded. Environment=Production. PollingInterval=60s, MaxConcurrent=20`

**Test Evidence:**
```csharp
// Integration test: Environment-specific config
Environment.SetEnvironmentVariable("ASPNETCORE_ENVIRONMENT", "Production");
var config = LoadConfiguration();
Assert.Equal(60, config.HealthCheck.DefaultPollingIntervalSeconds);
Assert.Equal(20, config.HealthCheck.MaxConcurrentChecks);
Assert.Contains("PROD-SQL-01", config.ConnectionStrings.OmniWatchDb);
```

---

### Scenario 3: Configuration Validation at Startup (Invalid Values)

**Given** PollingService has `appsettings.json` with invalid configuration:
```json
{
  "HealthCheck": {
    "DefaultPollingIntervalSeconds": -10,
    "MaxConcurrentChecks": 0,
    "DefaultTimeoutSeconds": 5000
  }
}
```
**When** I start PollingService
**Then**:
- Configuration validation fails during startup (before service starts polling)
- Service logs detailed errors:
  ```
  [ERROR] Configuration validation failed:
  - DefaultPollingIntervalSeconds must be between 10 and 3600 (value: -10)
  - MaxConcurrentChecks must be between 1 and 50 (value: 0)
  - DefaultTimeoutSeconds must be between 5 and 300 (value: 5000)
  ```
- Service does NOT start (OnStart fails with ConfigurationException)
- Windows Service Control Manager shows service in "Stopped" state
- Event Log contains validation errors
- Exit code: 1 (failure)

**Test Evidence:**
```csharp
// Unit test: Configuration validation
var invalidConfig = new HealthCheckSettings
{
    DefaultPollingIntervalSeconds = -10,
    MaxConcurrentChecks = 0,
    DefaultTimeoutSeconds = 5000
};

var validator = new HealthCheckSettingsValidator();
var result = validator.Validate(invalidConfig);

Assert.False(result.IsValid);
Assert.Contains(result.Errors, e => e.PropertyName == "DefaultPollingIntervalSeconds");
Assert.Contains(result.Errors, e => e.PropertyName == "MaxConcurrentChecks");
Assert.Contains(result.Errors, e => e.PropertyName == "DefaultTimeoutSeconds");
```

---

### Scenario 4: Missing Configuration File (Fallback to Defaults)

**Given** PollingService is installed but `appsettings.json` is missing or corrupted
**When** I start PollingService
**Then**:
- Service detects missing configuration file
- Service logs warning: `[WARN] appsettings.json not found. Using default configuration.`
- Service uses hardcoded safe defaults:
  - DefaultPollingIntervalSeconds: 300 (5 minutes)
  - MaxConcurrentChecks: 10
  - DefaultTimeoutSeconds: 30
  - ConnectionStrings.OmniWatchDb: "Server=localhost;Database=OmniWatchAI;Integrated Security=true;"
  - Serilog.MinimumLevel: Information
- Service starts successfully with defaults
- Event Log warning recorded: "Configuration file missing. Using defaults."

**Test Evidence:**
```csharp
// Integration test: Missing appsettings.json
File.Delete("appsettings.json");  // Simulate missing file
var service = new PollingService(...);
service.OnStart(null);

// Verify defaults used
var config = service.GetConfiguration();
Assert.Equal(300, config.DefaultPollingIntervalSeconds);
Assert.Equal(10, config.MaxConcurrentChecks);
```

---

### Scenario 5: Connection String Validation (SQL Server Connectivity)

**Given** PollingService has `appsettings.json` with connection string:
```json
{
  "ConnectionStrings": {
    "OmniWatchDb": "Server=INVALID-SERVER;Database=OmniWatchAI;Integrated Security=true;"
  }
}
```
**When** I start PollingService
**Then**:
- Service loads configuration successfully (connection string syntactically valid)
- Service attempts to connect to database during startup health check
- Connection fails (invalid server name)
- Service logs error:
  ```
  [ERROR] Database connectivity check failed: A network-related or instance-specific error occurred while establishing a connection to SQL Server. Server not found or not accessible.
  ```
- Service DOES start but logs warning: `[WARN] Database unreachable at startup. Will retry on first health check poll.`
- Service transitions to "Running" state (resilient to temporary database outages)
- First health check poll will retry database connection

**Test Evidence:**
- Service starts successfully (status = Running)
- Event Log contains database connectivity warning
- Service does NOT crash on startup due to database issue
- Health check polling retries database connection every polling interval

**Rationale:** Service should be resilient to temporary database outages (e.g., database maintenance). Don't fail startup if database is temporarily unreachable.

---

### Scenario 6: Hot Reload Configuration Changes (No Service Restart)

**Given** PollingService is running with configuration:
```json
{ "HealthCheck": { "DefaultPollingIntervalSeconds": 300 } }
```
**When** I modify `appsettings.json` to:
```json
{ "HealthCheck": { "DefaultPollingIntervalSeconds": 60 } }
```
**And** Save the file (no service restart)
**Then**:
- Configuration file watcher detects change within 5 seconds
- Service logs: `[INFO] Configuration file changed. Reloading...`
- New configuration loaded and validated
- Polling interval updated to 60 seconds for next poll cycle
- In-flight health checks continue with old configuration (no interruption)
- Next poll cycle uses new 60-second interval
- Service logs: `[INFO] Configuration reloaded successfully. PollingInterval updated: 300s → 60s`

**Test Evidence:**
```csharp
// Integration test: Hot reload
var service = StartService();
Assert.Equal(300, service.GetPollingInterval());

// Modify appsettings.json
UpdateConfigurationFile("DefaultPollingIntervalSeconds", 60);

// Wait for file watcher to trigger
Thread.Sleep(6000);

// Verify new config loaded
Assert.Equal(60, service.GetPollingInterval());
```

**Limitations (Not Hot Reloadable):**
- Database connection string changes require service restart
- Logging configuration changes require service restart
- Service account changes require service restart

---

### Scenario 7: Secrets Management (Connection String from Environment Variable)

**Given** PollingService has `appsettings.json` with placeholder:
```json
{
  "ConnectionStrings": {
    "OmniWatchDb": "${OMNIWATCHAI_CONNECTION_STRING}"
  }
}
```
**And** Environment variable `OMNIWATCHAI_CONNECTION_STRING` is set to production connection string
**When** I start PollingService
**Then**:
- Configuration loader resolves environment variable
- Connection string replaced with environment variable value
- Actual connection string used: value from `OMNIWATCHAI_CONNECTION_STRING`
- Service logs: `[INFO] Connection string loaded from environment variable OMNIWATCHAI_CONNECTION_STRING`
- No sensitive connection string visible in `appsettings.json` (placeholder only)

**Test Evidence:**
```csharp
// Integration test: Environment variable substitution
Environment.SetEnvironmentVariable("OMNIWATCHAI_CONNECTION_STRING", "Server=PROD-SQL;Database=OmniWatchAI;Integrated Security=true;");
var config = LoadConfiguration();
Assert.Equal("Server=PROD-SQL;Database=OmniWatchAI;Integrated Security=true;", config.ConnectionStrings.OmniWatchDb);
Assert.DoesNotContain("${OMNIWATCHAI_CONNECTION_STRING}", config.ConnectionStrings.OmniWatchDb);
```

**Alternative (Production):** Use Windows environment variables instead of hardcoding connection strings in files.

---

### Scenario 8: SMTP Configuration for AlertingService

**Given** AlertingService has `appsettings.json` with SMTP configuration:
```json
{
  "Alerting": {
    "SmtpHost": "smtp.company.com",
    "SmtpPort": 587,
    "SmtpEnableSsl": true,
    "SmtpUsername": "${SMTP_USERNAME}",
    "SmtpPassword": "${SMTP_PASSWORD}",
    "FromAddress": "omniwatchai@company.com",
    "FromDisplayName": "OmniWatchAI Monitoring"
  }
}
```
**And** Environment variables `SMTP_USERNAME` and `SMTP_PASSWORD` are set
**When** I start AlertingService
**Then**:
- SMTP configuration loaded from `appsettings.json`
- Username and password resolved from environment variables
- SMTP settings validated:
  - SmtpHost is not empty
  - SmtpPort is between 1-65535
  - FromAddress is valid email format
- Service logs: `[INFO] SMTP configuration loaded. Host=smtp.company.com, Port=587, SSL=Enabled`
- AlertingService ready to send email notifications

**Test Evidence:**
```csharp
// Unit test: SMTP configuration validation
var smtpConfig = new SmtpSettings
{
    SmtpHost = "smtp.company.com",
    SmtpPort = 587,
    SmtpEnableSsl = true,
    FromAddress = "omniwatchai@company.com"
};

var validator = new SmtpSettingsValidator();
var result = validator.Validate(smtpConfig);
Assert.True(result.IsValid);
```

**Invalid SMTP Configuration Example:**
```json
{
  "Alerting": {
    "SmtpHost": "",
    "SmtpPort": 999999,
    "FromAddress": "invalid-email"
  }
}
```
**Expected Errors:**
```
[ERROR] SMTP configuration validation failed:
- SmtpHost cannot be empty
- SmtpPort must be between 1 and 65535 (value: 999999)
- FromAddress must be a valid email address (value: invalid-email)
```

---

### Scenario 9: Configuration Logging (No Sensitive Data)

**Given** PollingService starts with configuration containing:
- Database connection string: `Server=PROD-SQL;Database=OmniWatchAI;User Id=sa;Password=SecretP@ssw0rd!`
- SMTP credentials: Username=`smtp_user`, Password=`SecretSMTPPass!`
**When** Service logs configuration at startup
**Then**:
- Service logs non-sensitive configuration:
  ```
  [INFO] Configuration loaded successfully:
  - PollingInterval: 60 seconds
  - MaxConcurrentChecks: 20
  - Timeout: 30 seconds
  - Database: PROD-SQL (OmniWatchAI)
  - SMTP Host: smtp.company.com:587 (SSL Enabled)
  ```
- Service DOES NOT log sensitive data:
  - ❌ Connection string passwords
  - ❌ SMTP passwords
  - ❌ API keys
  - ❌ Credentials of any kind
- Log files, Event Log, and database logs contain no passwords

**Test Evidence:**
```csharp
// Integration test: Sensitive data not logged
var service = StartService();
var logOutput = ReadLogFile();

Assert.DoesNotContain("SecretP@ssw0rd!", logOutput);
Assert.DoesNotContain("SecretSMTPPass!", logOutput);
Assert.DoesNotContain("User Id=sa", logOutput);
Assert.Contains("Database: PROD-SQL", logOutput);  // Non-sensitive info OK
```

---

### Scenario 10: Configuration Override Precedence (Environment > File)

**Given** PollingService has configuration from multiple sources:
1. `appsettings.json`: `DefaultPollingIntervalSeconds = 300`
2. `appsettings.Production.json`: `DefaultPollingIntervalSeconds = 60`
3. Environment variable: `OMNIWATCHAI_POLLING_INTERVAL = 30`
**When** Service starts in Production environment
**Then**:
- Configuration sources loaded in order:
  1. appsettings.json (base)
  2. appsettings.Production.json (environment override)
  3. Environment variables (highest priority)
- Final configuration: `DefaultPollingIntervalSeconds = 30` (from environment variable)
- Service logs:
  ```
  [INFO] Configuration loaded from multiple sources:
  - appsettings.json: PollingInterval=300s
  - appsettings.Production.json: PollingInterval=60s (overridden)
  - Environment variable OMNIWATCHAI_POLLING_INTERVAL: 30s (final value)
  ```

**Precedence Order (Lowest to Highest):**
1. appsettings.json (default)
2. appsettings.{Environment}.json (environment-specific)
3. Environment variables (highest priority)

**Test Evidence:**
```csharp
// Integration test: Override precedence
Environment.SetEnvironmentVariable("ASPNETCORE_ENVIRONMENT", "Production");
Environment.SetEnvironmentVariable("OMNIWATCHAI_POLLING_INTERVAL", "30");

var config = LoadConfiguration();
Assert.Equal(30, config.HealthCheck.DefaultPollingIntervalSeconds);
```

---

## Technical Specification

### Architecture & Dependencies

**Layer**: Application Layer + Infrastructure Layer
**Component**: Configuration management (IOptions<T> pattern)
**Related Components**:
- Microsoft.Extensions.Configuration (appsettings.json loading)
- Microsoft.Extensions.Options (IOptions<T> dependency injection)
- FluentValidation (configuration validation)
- Serilog (logging)

### File Structure

**Files to Create:**

```
src/OmniWatchAI.Application/
├── Configuration/
│   ├── HealthCheckSettings.cs               # Strongly-typed settings (AC 1-2)
│   ├── SmtpSettings.cs                      # SMTP settings for AlertingService (AC 8)
│   ├── ConfigurationService.cs              # Configuration loading and hot reload (AC 6)
│   └── Validators/
│       ├── HealthCheckSettingsValidator.cs  # FluentValidation rules (AC 3)
│       └── SmtpSettingsValidator.cs         # SMTP validation (AC 8)

src/OmniWatchAI.PollingService/
├── appsettings.json                         # Default configuration (AC 1)
├── appsettings.Development.json             # Development overrides
├── appsettings.Production.json              # Production overrides (AC 2)
└── appsettings.Test.json                    # Test environment

src/OmniWatchAI.AlertingService/
├── appsettings.json
├── appsettings.Production.json
└── appsettings.Test.json

tests/UnitTests/Application.UnitTests/
├── Configuration/
│   ├── HealthCheckSettingsValidatorTests.cs  # AC 3
│   └── SmtpSettingsValidatorTests.cs         # AC 8

tests/IntegrationTests/PollingService.IntegrationTests/
├── ConfigurationLoadingTests.cs              # AC 1-2, 4-7, 10
└── ConfigurationHotReloadTests.cs            # AC 6
```

### Data Model (Strongly-Typed Configuration Classes)

**HealthCheckSettings.cs:**

```csharp
namespace OmniWatchAI.Application.Configuration;

public class HealthCheckSettings
{
    public const string SectionName = "HealthCheck";

    /// <summary>
    /// Default polling interval in seconds (10-3600). Default: 300 (5 minutes).
    /// </summary>
    public int DefaultPollingIntervalSeconds { get; set; } = 300;

    /// <summary>
    /// Maximum concurrent health checks (1-50). Default: 10.
    /// </summary>
    public int MaxConcurrentChecks { get; set; } = 10;

    /// <summary>
    /// Default timeout for health checks in seconds (5-300). Default: 30.
    /// </summary>
    public int DefaultTimeoutSeconds { get; set; } = 30;

    /// <summary>
    /// Retry count for failed health checks (0-5). Default: 3.
    /// </summary>
    public int RetryCount { get; set; } = 3;
}
```

**HealthCheckSettingsValidator.cs (FluentValidation):**

```csharp
using FluentValidation;

namespace OmniWatchAI.Application.Configuration.Validators;

public class HealthCheckSettingsValidator : AbstractValidator<HealthCheckSettings>
{
    public HealthCheckSettingsValidator()
    {
        RuleFor(x => x.DefaultPollingIntervalSeconds)
            .InclusiveBetween(10, 3600)
            .WithMessage("DefaultPollingIntervalSeconds must be between 10 and 3600 seconds (10 sec to 1 hour)");

        RuleFor(x => x.MaxConcurrentChecks)
            .InclusiveBetween(1, 50)
            .WithMessage("MaxConcurrentChecks must be between 1 and 50");

        RuleFor(x => x.DefaultTimeoutSeconds)
            .InclusiveBetween(5, 300)
            .WithMessage("DefaultTimeoutSeconds must be between 5 and 300 seconds (5 sec to 5 min)");

        RuleFor(x => x.RetryCount)
            .InclusiveBetween(0, 5)
            .WithMessage("RetryCount must be between 0 and 5");
    }
}
```

**SmtpSettings.cs:**

```csharp
namespace OmniWatchAI.Application.Configuration;

public class SmtpSettings
{
    public const string SectionName = "Alerting";

    public string SmtpHost { get; set; } = string.Empty;
    public int SmtpPort { get; set; } = 587;
    public bool SmtpEnableSsl { get; set; } = true;
    public string SmtpUsername { get; set; } = string.Empty;
    public string SmtpPassword { get; set; } = string.Empty;
    public string FromAddress { get; set; } = string.Empty;
    public string FromDisplayName { get; set; } = "OmniWatchAI Monitoring";
}
```

**SmtpSettingsValidator.cs:**

```csharp
using FluentValidation;

namespace OmniWatchAI.Application.Configuration.Validators;

public class SmtpSettingsValidator : AbstractValidator<SmtpSettings>
{
    public SmtpSettingsValidator()
    {
        RuleFor(x => x.SmtpHost)
            .NotEmpty()
            .WithMessage("SmtpHost cannot be empty");

        RuleFor(x => x.SmtpPort)
            .InclusiveBetween(1, 65535)
            .WithMessage("SmtpPort must be between 1 and 65535");

        RuleFor(x => x.FromAddress)
            .NotEmpty()
            .EmailAddress()
            .WithMessage("FromAddress must be a valid email address");
    }
}
```

### API Contract (Configuration Loading)

**Program.cs (PollingService):**

```csharp
var builder = Host.CreateDefaultBuilder(args)
    .UseWindowsService()  // Enable Windows Service hosting
    .ConfigureAppConfiguration((context, config) =>
    {
        var env = context.HostingEnvironment;

        config
            .SetBasePath(AppContext.BaseDirectory)
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)  // AC 1, 6
            .AddJsonFile($"appsettings.{env.EnvironmentName}.json", optional: true, reloadOnChange: true)  // AC 2
            .AddEnvironmentVariables("OMNIWATCHAI_");  // AC 7, 10
    })
    .ConfigureServices((context, services) =>
    {
        // Bind strongly-typed configuration (AC 1)
        services.Configure<HealthCheckSettings>(context.Configuration.GetSection(HealthCheckSettings.SectionName));

        // Register validators (AC 3)
        services.AddSingleton<IValidator<HealthCheckSettings>, HealthCheckSettingsValidator>();

        // Validate configuration at startup (AC 3)
        services.AddOptions<HealthCheckSettings>()
            .Validate(settings =>
            {
                var validator = new HealthCheckSettingsValidator();
                var result = validator.Validate(settings);
                return result.IsValid;
            }, "HealthCheck configuration validation failed");

        // Other services
        services.AddSingleton<IConfigurationService, ConfigurationService>();
        services.AddHostedService<PollingService>();
    })
    .UseSerilog();

var host = builder.Build();

// Validate configuration before starting (AC 3)
try
{
    var healthCheckSettings = host.Services.GetRequiredService<IOptions<HealthCheckSettings>>().Value;
    var validator = new HealthCheckSettingsValidator();
    var validationResult = validator.Validate(healthCheckSettings);

    if (!validationResult.IsValid)
    {
        var logger = host.Services.GetRequiredService<ILogger<Program>>();
        logger.LogError("Configuration validation failed:");
        foreach (var error in validationResult.Errors)
        {
            logger.LogError("- {PropertyName}: {ErrorMessage}", error.PropertyName, error.ErrorMessage);
        }
        return 1;  // Exit with failure
    }
}
catch (Exception ex)
{
    Console.WriteLine($"Failed to validate configuration: {ex.Message}");
    return 1;
}

await host.RunAsync();
return 0;
```

### Business Rules

1. **Configuration Validation**: All configuration must be validated at startup before service starts
2. **Default Values**: Service must have safe defaults if `appsettings.json` is missing
3. **Environment-Specific Overrides**: Production settings override defaults
4. **Hot Reload**: Configuration changes detected within 5 seconds (file watcher)
5. **Secrets Management**: Sensitive data (passwords, connection strings) from environment variables only
6. **Logging Security**: Never log passwords, connection strings, or credentials
7. **Override Precedence**: Environment variables > appsettings.{Environment}.json > appsettings.json
8. **Resilient Startup**: Service starts even if database is temporarily unreachable (retries on first poll)

### Non-Functional Requirements

**Performance:**
- Configuration loading: < 1 second
- Configuration validation: < 100ms
- Hot reload detection: < 5 seconds
- Memory overhead: < 10 MB for configuration

**Reliability:**
- Resilient to missing configuration files (fallback to defaults)
- Resilient to temporary database outages (retry on poll)
- Configuration errors detected at startup (fail fast)

**Security:**
- Sensitive data in environment variables (not in files)
- No passwords logged (Serilog filters)
- Configuration files secured via file permissions (service account read-only)

**Usability:**
- Clear validation error messages (property name + error description)
- Configuration documented in comments (XML doc comments)
- Default values sensible for production (300s polling, 10 concurrent, 30s timeout)

---

## Implementation Notes

### Technology Decisions

**Microsoft.Extensions.Configuration:**
- Standard .NET configuration system
- Supports JSON, environment variables, command line
- Hot reload via `reloadOnChange: true`

**Microsoft.Extensions.Options (IOptions<T> Pattern):**
- Strongly-typed configuration
- Dependency injection friendly
- Validation support

**FluentValidation:**
- Expressive validation rules
- Testable validators
- Rich error messages

**Environment Variable Substitution:**
- Use `${ENV_VAR_NAME}` syntax in JSON
- Resolve via AddEnvironmentVariables() provider
- Highest precedence (overrides JSON files)

### Code Patterns to Follow

**All code must follow coding-standards.md:**
- IOptions<T> injection for configuration access
- FluentValidation for validation rules
- Structured logging (no sensitive data)
- Async configuration loading (if database-driven)
- Fail fast on invalid configuration

### Testing Strategy

**Unit Tests:**
- HealthCheckSettingsValidator (all validation rules)
- SmtpSettingsValidator (all validation rules)
- Configuration defaults
- Validation error messages

**Integration Tests:**
- Load configuration from appsettings.json
- Environment-specific overrides (appsettings.Production.json)
- Environment variable substitution
- Hot reload (file change detection)
- Missing configuration file (defaults)
- Invalid configuration (startup failure)

**Manual Tests:**
- Modify appsettings.json while service running (hot reload)
- Set environment variables and verify override
- Remove appsettings.json and verify defaults
- Start service with invalid config and verify error logging

### Compliance Checklist

- [ ] Configuration validated at startup (FluentValidation)
- [ ] Strongly-typed settings (IOptions<T>)
- [ ] Environment-specific overrides (appsettings.{Environment}.json)
- [ ] Hot reload supported (reloadOnChange: true)
- [ ] Secrets in environment variables (not in files)
- [ ] No sensitive data logged
- [ ] Default values documented
- [ ] Validation errors logged clearly

---

## Dependencies

**Hard Dependencies (Must Complete First):**
- STORY-001: Windows Service Framework - PollingService (service executable exists)
- STORY-002: Windows Service Framework - AlertingService (service executable exists)

**Soft Dependencies:**
- STORY-005: Windows Service Installation (deployment scripts)

**External Dependencies:**
- Microsoft.Extensions.Configuration NuGet packages
- Microsoft.Extensions.Options NuGet packages
- FluentValidation NuGet package

---

## Definition of Done

**Code Implementation:**
- [ ] HealthCheckSettings.cs created with default values
- [ ] SmtpSettings.cs created with default values
- [ ] HealthCheckSettingsValidator.cs with validation rules (AC 3)
- [ ] SmtpSettingsValidator.cs with validation rules (AC 8)
- [ ] ConfigurationService.cs for configuration loading
- [ ] appsettings.json with defaults (AC 1)
- [ ] appsettings.Production.json with production overrides (AC 2)
- [ ] Program.cs registers configuration (IOptions<T>)
- [ ] Validation runs at startup (AC 3)

**Testing:**
- [ ] Unit tests: HealthCheckSettingsValidator (all validation rules)
- [ ] Unit tests: SmtpSettingsValidator (all validation rules)
- [ ] Integration tests: Configuration loading from JSON
- [ ] Integration tests: Environment-specific overrides
- [ ] Integration tests: Environment variable substitution
- [ ] Integration tests: Hot reload
- [ ] Integration tests: Missing configuration file (defaults)
- [ ] Integration tests: Invalid configuration (startup failure)
- [ ] Coverage: >= 95% for validators, >= 85% for configuration loading
- [ ] All tests pass (100% pass rate)

**Quality Gates:**
- [ ] No violations of architecture-constraints.md
- [ ] No violations of coding-standards.md
- [ ] No sensitive data logged (passwords, connection strings)
- [ ] Code review approved

**Documentation:**
- [ ] XML doc comments for all settings properties
- [ ] appsettings.json commented (explain each setting)
- [ ] README section: Configuration guide
- [ ] README section: Environment variables reference
- [ ] Troubleshooting: Invalid configuration errors

**Deployment:**
- [ ] appsettings.json deployed with service
- [ ] appsettings.Production.json deployed (production only)
- [ ] Environment variables documented in deployment guide
- [ ] Configuration validation tested on staging

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
- STORY-001: Windows Service Framework - PollingService
- STORY-002: Windows Service Framework - AlertingService

**Successor Stories** (depend on this story):
- STORY-004: Health Check Execution Engine (uses HealthCheckSettings)
- STORY-007: Email Alerting (uses SmtpSettings)

**Related Stories**:
- STORY-005: Windows Service Installation (deployment scripts)

---

## Story Metrics

**Estimation Breakdown:**
- Strongly-typed settings classes: 0.5 points
- FluentValidation validators: 1 point
- Configuration loading and validation at startup: 0.5 points
- Environment-specific overrides: 0.5 points
- Hot reload support: 0.5 points
- Testing and documentation: 0.5 points

**Total: 3 story points (estimated 1-2 days for experienced .NET developer)**

---

## Acceptance Criteria Summary

**Must Have (All 10 ACs must pass):**

1. Load configuration from appsettings.json at startup
2. Environment-specific configuration overrides (Production)
3. Configuration validation at startup (invalid values)
4. Missing configuration file (fallback to defaults)
5. Connection string validation (SQL Server connectivity)
6. Hot reload configuration changes (no service restart)
7. Secrets management (connection string from environment variable)
8. SMTP configuration for AlertingService
9. Configuration logging (no sensitive data)
10. Configuration override precedence (Environment > File)

**All acceptance criteria MUST be validated via automated tests and manual testing.**

---

**Story Owner:** [TBD]
**Last Updated:** 2025-01-15
**Created By:** DevForgeAI Requirements Analyst
