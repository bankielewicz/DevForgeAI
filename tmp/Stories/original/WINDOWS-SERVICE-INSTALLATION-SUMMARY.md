# Windows Service Installation and Configuration - Story Summary

**Feature**: Windows Service installation and configuration for OmniWatchAI platform

**Epic**: EPIC-001 (Core Monitoring Infrastructure)

**Created**: 2025-01-15

**Created By**: DevForgeAI Requirements Analyst

---

## Overview

This document summarizes the user stories created for the Windows Service installation and configuration feature. Two complementary stories cover the complete deployment and runtime configuration lifecycle for OmniWatchAI's PollingService and AlertingService.

---

## User Stories Created

### STORY-005: Windows Service Installation and Deployment Automation

**Priority**: High
**Story Points**: 5
**Focus**: Automated deployment scripts for Windows Service installation

**Key Features**:
- PowerShell scripts for installing PollingService and AlertingService
- Service account configuration with SQL Server permissions
- Auto-recovery policy configuration (restart on failure)
- Installation validation and prerequisite checking
- Service start/stop/uninstall scripts
- Support for custom binary paths and idempotent installation

**Acceptance Criteria** (10 scenarios):
1. Install PollingService via PowerShell script
2. Install AlertingService via PowerShell script
3. Configure service account with SQL Server permissions
4. Configure auto-recovery policy (restart on failure)
5. Uninstall services (cleanup script)
6. Validate installation prerequisites
7. Start services after installation
8. Stop services (graceful shutdown)
9. Installation with custom binary path
10. Idempotent installation (force reinstall)

**Deliverables**:
- 8 PowerShell deployment scripts
- 2 PowerShell modules (shared functions)
- Installation guide (README.md)
- Troubleshooting documentation

**File**: `/mnt/c/Projects/OmniWatchAI/.ai_docs/Stories/STORY-005-windows-service-installation-deployment.story.md`

---

### STORY-006: Windows Service Configuration Management and Runtime Behavior

**Priority**: Medium
**Story Points**: 3
**Focus**: Configuration loading, validation, and runtime behavior

**Key Features**:
- Load configuration from `appsettings.json` with environment-specific overrides
- Validate configuration at startup using FluentValidation
- Hot reload configuration changes without service restart
- Secrets management via environment variables
- SMTP configuration for AlertingService
- Configuration logging without sensitive data

**Acceptance Criteria** (10 scenarios):
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

**Deliverables**:
- Strongly-typed configuration classes (HealthCheckSettings, SmtpSettings)
- FluentValidation validators
- Configuration loading with IOptions<T> pattern
- Environment-specific appsettings files (Development, Production, Test)
- Configuration documentation

**File**: `/mnt/c/Projects/OmniWatchAI/.ai_docs/Stories/STORY-006-windows-service-configuration-management.story.md`

---

## Story Relationship

```
STORY-005 (Installation)          STORY-006 (Configuration)
        |                                  |
        v                                  v
[PowerShell Scripts]              [appsettings.json]
        |                                  |
        v                                  v
[Install Services]       →→→       [Load & Validate Config]
        |                                  |
        v                                  v
[Configure Auto-Recovery]          [Hot Reload Support]
        |                                  |
        v                                  v
[Start Services]                   [Runtime Behavior]
```

**Dependencies**:
- STORY-005 depends on STORY-001 and STORY-002 (service binaries must exist)
- STORY-006 depends on STORY-001 and STORY-002 (service framework must exist)
- STORY-006 is complementary to STORY-005 (configuration needed at runtime)

---

## Combined Business Value

**For DevOps Engineers:**
- ✅ Automated deployment scripts (no manual service registration)
- ✅ Consistent configuration across environments
- ✅ Service auto-recovery (99.9% uptime target)
- ✅ Easy troubleshooting (validation errors at startup)

**For System Administrators:**
- ✅ Environment-specific configuration (Dev/Test/Prod)
- ✅ Hot reload for configuration changes (no downtime)
- ✅ Secrets management via environment variables (secure)
- ✅ Clear error messages (validation failures)

**For Security/Compliance:**
- ✅ Least-privilege service account
- ✅ No hardcoded credentials
- ✅ No sensitive data in logs
- ✅ Installation audit trail

---

## Implementation Timeline

**Total Effort**: 8 story points (5 + 3)

**Suggested Sprint**: Sprint-2

**Estimated Duration**: 4-6 days (experienced .NET/DevOps engineer)

**Sequencing**:
1. Implement STORY-001 and STORY-002 first (service framework)
2. Implement STORY-005 and STORY-006 in parallel:
   - Developer 1: PowerShell deployment scripts (STORY-005)
   - Developer 2: Configuration management (STORY-006)
3. Integration testing: Install services → Validate configuration → Start services

---

## Key Technical Decisions

### Installation (STORY-005)

**Technology**: PowerShell 5.1+
- Native Windows automation
- Built-in service management cmdlets
- No external dependencies

**Patterns**:
- Modular scripts (shared functions in .psm1 modules)
- Idempotent installation (-Force parameter)
- Prerequisite validation before installation
- Graceful error handling with clear messages

### Configuration (STORY-006)

**Technology**: Microsoft.Extensions.Configuration + FluentValidation
- Strongly-typed settings (IOptions<T>)
- Environment-specific overrides
- Hot reload via file watcher
- Validation at startup

**Patterns**:
- IOptions<T> pattern for dependency injection
- FluentValidation for validation rules
- Environment variable substitution for secrets
- Override precedence: Environment > appsettings.{Env}.json > appsettings.json

---

## Non-Functional Requirements (Combined)

### Performance
- Service installation: < 10 seconds per service
- Service startup: < 10 seconds per service
- Configuration loading: < 1 second
- Hot reload detection: < 5 seconds

### Reliability
- Auto-recovery: 3 restart attempts, 60-second intervals
- 99.9% uptime target
- Resilient to missing configuration (fallback to defaults)
- Resilient to temporary database outages

### Security
- Service runs with least privilege (Network Service or custom service account)
- Secrets in environment variables (not in files)
- No sensitive data logged (passwords, connection strings)
- SQL Server permissions: db_datareader, db_datawriter only

### Usability
- Clear error messages (validation failures, missing prerequisites)
- Comprehensive documentation (installation guide, troubleshooting)
- Default values sensible for production
- Verbose script output (✅/❌ indicators)

---

## Testing Strategy (Combined)

### STORY-005 (Installation)

**Manual Testing** (primary):
- Install services on Windows Server 2022
- Start/stop services via PowerShell scripts
- Force crash and verify auto-recovery
- Custom binary path installation
- Service account configuration

**Integration Testing**:
- Full lifecycle: Install → Start → Stop → Uninstall
- Prerequisite validation with missing database
- Invalid service account

### STORY-006 (Configuration)

**Unit Testing** (primary):
- HealthCheckSettingsValidator (all validation rules)
- SmtpSettingsValidator (all validation rules)
- Configuration defaults

**Integration Testing**:
- Load configuration from appsettings.json
- Environment-specific overrides
- Hot reload (file change detection)
- Environment variable substitution
- Invalid configuration (startup failure)

**Coverage Targets**:
- Validators: 95%+
- Configuration loading: 85%+
- Overall: 80%+

---

## Definition of Done (Combined)

### Code Implementation

**STORY-005 (Installation)**:
- [ ] 8 PowerShell deployment scripts created
- [ ] 2 PowerShell modules created (shared functions)
- [ ] Installation guide (README.md)
- [ ] All scripts tested on Windows Server 2022

**STORY-006 (Configuration)**:
- [ ] HealthCheckSettings.cs + SmtpSettings.cs created
- [ ] FluentValidation validators created
- [ ] appsettings.json + environment-specific overrides
- [ ] Configuration validation at startup
- [ ] Hot reload support implemented

### Testing

**STORY-005**:
- [ ] Manual tests: Install/start/stop/uninstall
- [ ] Manual tests: Auto-recovery
- [ ] Manual tests: Custom binary path
- [ ] Manual tests: Service account configuration

**STORY-006**:
- [ ] Unit tests: All validators (95%+ coverage)
- [ ] Integration tests: Configuration loading
- [ ] Integration tests: Hot reload
- [ ] Integration tests: Invalid configuration
- [ ] 100% test pass rate

### Quality Gates

- [ ] No violations of architecture-constraints.md
- [ ] No violations of coding-standards.md
- [ ] No sensitive data logged
- [ ] Code review approved
- [ ] No CRITICAL/HIGH severity issues

### Documentation

**STORY-005**:
- [ ] Installation guide (deployment/README.md)
- [ ] Service account setup instructions
- [ ] Troubleshooting guide

**STORY-006**:
- [ ] Configuration guide (appsettings.json reference)
- [ ] Environment variables documentation
- [ ] Validation error messages documented

### Deployment

- [ ] Scripts tested on staging environment
- [ ] Services installed and running on test server
- [ ] Configuration validated in production-like environment
- [ ] Auto-recovery tested (force crash)

---

## Risk Assessment

### High Risk

**Service Account Permissions** (STORY-005):
- **Risk**: Service account doesn't have SQL Server permissions
- **Mitigation**: Configure-ServiceAccount.ps1 validates permissions before configuring
- **Impact**: Service won't start or will fail on first health check

**Invalid Configuration** (STORY-006):
- **Risk**: Invalid appsettings.json causes service to crash on startup
- **Mitigation**: FluentValidation at startup (fail fast with clear errors)
- **Impact**: Service won't start, but error is logged clearly

### Medium Risk

**Auto-Recovery Loops** (STORY-005):
- **Risk**: Service crashes repeatedly, triggers auto-recovery indefinitely
- **Mitigation**: Windows SCM limits restart attempts (3 attempts, then stops)
- **Impact**: Service requires manual intervention after 3 failures

**Hot Reload Issues** (STORY-006):
- **Risk**: Invalid configuration during hot reload crashes service
- **Mitigation**: Validate configuration before applying (revert on validation failure)
- **Impact**: Service continues with old configuration, logs error

### Low Risk

**Missing Configuration File** (STORY-006):
- **Risk**: appsettings.json deleted or corrupted
- **Mitigation**: Service uses hardcoded safe defaults
- **Impact**: Service runs with defaults, logs warning

---

## Acceptance Criteria Summary

### STORY-005 (10 ACs)

1. ✅ Install PollingService via PowerShell
2. ✅ Install AlertingService via PowerShell
3. ✅ Configure service account with SQL permissions
4. ✅ Configure auto-recovery policy
5. ✅ Uninstall services (cleanup)
6. ✅ Validate prerequisites
7. ✅ Start services
8. ✅ Stop services (graceful)
9. ✅ Custom binary path
10. ✅ Idempotent installation

### STORY-006 (10 ACs)

1. ✅ Load appsettings.json
2. ✅ Environment-specific overrides
3. ✅ Validate configuration at startup
4. ✅ Missing config → defaults
5. ✅ Connection string validation
6. ✅ Hot reload
7. ✅ Secrets from environment variables
8. ✅ SMTP configuration
9. ✅ No sensitive data logged
10. ✅ Override precedence

**Total**: 20 acceptance criteria across 2 stories

---

## File Locations

### User Stories

- **STORY-005**: `/mnt/c/Projects/OmniWatchAI/.ai_docs/Stories/STORY-005-windows-service-installation-deployment.story.md`
- **STORY-006**: `/mnt/c/Projects/OmniWatchAI/.ai_docs/Stories/STORY-006-windows-service-configuration-management.story.md`
- **Summary**: `/mnt/c/Projects/OmniWatchAI/.ai_docs/Stories/WINDOWS-SERVICE-INSTALLATION-SUMMARY.md` (this file)

### Implementation Files (To Be Created)

**PowerShell Scripts** (STORY-005):
```
deployment/
├── Install-PollingService.ps1
├── Install-AlertingService.ps1
├── Configure-ServiceAccount.ps1
├── Configure-AutoRecovery.ps1
├── Uninstall-OmniWatchAI.ps1
├── Validate-Prerequisites.ps1
├── Start-OmniWatchAI.ps1
├── Stop-OmniWatchAI.ps1
├── Install-All.ps1
└── modules/
    ├── OmniWatchAI.Installation.psm1
    └── OmniWatchAI.Validation.psm1
```

**Configuration Files** (STORY-006):
```
src/OmniWatchAI.Application/Configuration/
├── HealthCheckSettings.cs
├── SmtpSettings.cs
├── ConfigurationService.cs
└── Validators/
    ├── HealthCheckSettingsValidator.cs
    └── SmtpSettingsValidator.cs

src/OmniWatchAI.PollingService/
├── appsettings.json
├── appsettings.Development.json
├── appsettings.Production.json
└── appsettings.Test.json

src/OmniWatchAI.AlertingService/
├── appsettings.json
├── appsettings.Production.json
└── appsettings.Test.json
```

---

## Next Steps

1. **Review Stories**: Product Owner / Tech Lead review and approve
2. **Sprint Planning**: Assign to Sprint-2
3. **Resource Allocation**:
   - DevOps Engineer for STORY-005 (PowerShell scripts)
   - .NET Developer for STORY-006 (Configuration management)
4. **Prerequisite Check**: Ensure STORY-001 and STORY-002 are completed
5. **Implementation**: Follow TDD approach (Red → Green → Refactor)
6. **QA Validation**: Manual testing on Windows Server 2022
7. **Deployment**: Deploy to staging environment for validation

---

## Related Documentation

**Context Files**:
- `/mnt/c/Projects/OmniWatchAI/.devforgeai/context/tech-stack.md` - Technology constraints
- `/mnt/c/Projects/OmniWatchAI/.devforgeai/context/architecture-constraints.md` - Clean Architecture rules
- `/mnt/c/Projects/OmniWatchAI/.devforgeai/context/coding-standards.md` - C# coding standards

**Epics**:
- `/mnt/c/Projects/OmniWatchAI/.ai_docs/Epics/EPIC-001-core-monitoring-infrastructure.epic.md` - Core monitoring infrastructure

**Related Stories**:
- STORY-001: Windows Service Framework - PollingService
- STORY-002: Windows Service Framework - AlertingService
- STORY-003: Configuration Management (database-driven)
- STORY-004: Health Check Execution Engine

---

**Created By**: DevForgeAI Requirements Analyst
**Last Updated**: 2025-01-15
**Version**: 1.0
