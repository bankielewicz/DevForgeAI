---
id: STORY-005
title: Windows Service Installation and Deployment Automation
epic: EPIC-001
sprint: Sprint-2
status: Backlog
priority: High
points: 5
type: Infrastructure
created: 2025-01-15
created_by: DevForgeAI Requirements Analyst
---

# STORY-005: Windows Service Installation and Deployment Automation

**Status**: Backlog
**Priority**: High
**Story Points**: 5
**Epic**: EPIC-001 (Core Monitoring Infrastructure)
**Sprint**: Sprint-2 (To be assigned)

---

## User Story

As a **DevOps Engineer**,
I want **automated PowerShell scripts to install and configure PollingService and AlertingService as Windows Services**,
So that **I can deploy OmniWatchAI to production servers quickly and consistently without manual configuration errors**.

---

## Acceptance Criteria

### Scenario 1: Install PollingService via PowerShell Script

**Given** Windows Server 2022 with Administrator privileges
**And** OmniWatchAI binaries built and copied to `C:\Program Files\OmniWatchAI\`
**When** I execute `.\Install-PollingService.ps1` from PowerShell as Administrator
**Then**:
- PowerShell script validates prerequisites (binaries exist, SQL Server accessible)
- Service is registered with Windows Service Control Manager:
  - Service Name: `OmniWatchAI.PollingService`
  - Display Name: `OmniWatchAI Polling Service`
  - Description: `Monitors SQL Server health by executing periodic health checks`
  - Binary Path: `C:\Program Files\OmniWatchAI\OmniWatchAI.PollingService.exe`
  - Startup Type: `Automatic` (starts on server boot)
- Service is installed but NOT started (manual start required for first-time configuration verification)
- Installation log created: `C:\Program Files\OmniWatchAI\logs\installation-polling-{timestamp}.log`
- Script output confirms: `PollingService installed successfully. Run 'Start-Service OmniWatchAI.PollingService' to start.`

**Test Evidence:**
```powershell
Get-Service -Name "OmniWatchAI.PollingService" | Select-Object Name, DisplayName, Status, StartType
# Expected: Name=OmniWatchAI.PollingService, Status=Stopped, StartType=Automatic
```

**Edge Case - Service Already Exists:**
```powershell
.\Install-PollingService.ps1
# Output: "Service already installed. Use -Force to reinstall or Uninstall-PollingService.ps1 first."
# Exit code: 1 (failure)
```

---

### Scenario 2: Install AlertingService via PowerShell Script

**Given** Windows Server 2022 with Administrator privileges
**And** OmniWatchAI binaries exist at `C:\Program Files\OmniWatchAI\`
**When** I execute `.\Install-AlertingService.ps1`
**Then**:
- Service registered with SCM:
  - Service Name: `OmniWatchAI.AlertingService`
  - Display Name: `OmniWatchAI Alerting Service`
  - Description: `Detects health check failures and sends email notifications`
  - Binary Path: `C:\Program Files\OmniWatchAI\OmniWatchAI.AlertingService.exe`
  - Startup Type: `Automatic`
- Service installed but NOT started
- Installation log: `C:\Program Files\OmniWatchAI\logs\installation-alerting-{timestamp}.log`
- Script confirms successful installation

**Test Evidence:**
```powershell
Get-Service -Name "OmniWatchAI.AlertingService" | Select-Object Name, Status, StartType
# Expected: Status=Stopped, StartType=Automatic
```

---

### Scenario 3: Configure Service Account with SQL Server Permissions

**Given** PollingService and AlertingService are installed
**And** Service account `DOMAIN\OmniWatchAI_ServiceAccount` exists (created by IT/DBA)
**When** I execute `.\Configure-ServiceAccount.ps1 -ServiceAccount "DOMAIN\OmniWatchAI_ServiceAccount"`
**Then**:
- Both services updated to run as specified service account:
  - PollingService runs as `DOMAIN\OmniWatchAI_ServiceAccount`
  - AlertingService runs as `DOMAIN\OmniWatchAI_ServiceAccount`
- Service account granted file system permissions:
  - Read/Execute: `C:\Program Files\OmniWatchAI\` (binaries and config)
  - Read/Write: `C:\Program Files\OmniWatchAI\logs\` (log files)
- SQL Server login verified (script validates connection):
  - Login exists on SQL Server instance
  - Database user created in `OmniWatchAI` database
  - Permissions granted: `db_datareader`, `db_datawriter`
- Script output: `Service account configured successfully. Services ready to start.`

**Test Evidence:**
```powershell
Get-WmiObject -Class Win32_Service | Where-Object { $_.Name -like "OmniWatchAI.*" } | Select-Object Name, StartName
# Expected: StartName=DOMAIN\OmniWatchAI_ServiceAccount for both services
```

**SQL Verification:**
```sql
-- Verify service account has required permissions
SELECT
    dp.name AS DatabaseUser,
    r.name AS DatabaseRole
FROM sys.database_principals dp
JOIN sys.database_role_members drm ON dp.principal_id = drm.member_principal_id
JOIN sys.database_principals r ON drm.role_principal_id = r.principal_id
WHERE dp.name = 'DOMAIN\OmniWatchAI_ServiceAccount';
-- Expected: Roles = db_datareader, db_datawriter
```

**Edge Case - Service Account Doesn't Exist:**
```powershell
.\Configure-ServiceAccount.ps1 -ServiceAccount "DOMAIN\InvalidAccount"
# Output: "ERROR: Service account 'DOMAIN\InvalidAccount' not found in Active Directory."
# Exit code: 1
```

---

### Scenario 4: Configure Auto-Recovery Policy (Restart on Failure)

**Given** PollingService and AlertingService are installed
**When** I execute `.\Configure-AutoRecovery.ps1`
**Then**:
- Auto-recovery policy configured for PollingService:
  - **First failure**: Restart service after 60 seconds
  - **Second failure**: Restart service after 60 seconds
  - **Subsequent failures**: Restart service after 60 seconds
  - **Reset failure count**: After 86400 seconds (24 hours)
- Auto-recovery policy configured for AlertingService (same settings)
- Windows Event Log notification enabled (log failures)
- Script output: `Auto-recovery configured. Services will auto-restart on failure within 60 seconds.`

**Test Evidence:**
```powershell
# Verify recovery settings via registry
$serviceName = "OmniWatchAI.PollingService"
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\$serviceName"
Get-ItemProperty -Path $regPath -Name FailureActions
# Expected: Reset=86400, Actions=Restart/60000/Restart/60000/Restart/60000
```

**Manual Recovery Test:**
1. Start PollingService
2. Force crash (kill process via Task Manager)
3. Verify service auto-restarts within 60 seconds
4. Check Event Log for recovery event

---

### Scenario 5: Uninstall Services (Cleanup Script)

**Given** PollingService and AlertingService are installed and running
**When** I execute `.\Uninstall-OmniWatchAI.ps1`
**Then**:
- Script prompts for confirmation: `Are you sure you want to uninstall OmniWatchAI services? (Y/N)`
- If confirmed (Y):
  - PollingService stopped gracefully (30-second timeout)
  - AlertingService stopped gracefully (30-second timeout)
  - Both services unregistered from SCM
  - Services no longer appear in Services.msc
  - Binaries remain in `C:\Program Files\OmniWatchAI\` (not deleted - data preservation)
  - Logs remain in `logs\` directory (audit trail)
  - Uninstallation log created: `logs\uninstall-{timestamp}.log`
  - Output: `OmniWatchAI services uninstalled successfully.`
- If cancelled (N):
  - No changes made
  - Output: `Uninstallation cancelled.`

**Test Evidence:**
```powershell
Get-Service -Name "OmniWatchAI.*"
# Expected: No services found (error)
```

**Edge Case - Services Not Installed:**
```powershell
.\Uninstall-OmniWatchAI.ps1
# Output: "No OmniWatchAI services found. Nothing to uninstall."
# Exit code: 0 (success)
```

---

### Scenario 6: Validate Installation Prerequisites

**Given** I want to install OmniWatchAI services
**When** I execute `.\Validate-Prerequisites.ps1`
**Then**:
- Script validates:
  - **Operating System**: Windows Server 2019+ or Windows 10/11 (for testing)
  - **PowerShell Version**: 5.1 or later
  - **Administrator Privileges**: Current user is Administrator
  - **Binaries Exist**:
    - `C:\Program Files\OmniWatchAI\OmniWatchAI.PollingService.exe` exists
    - `C:\Program Files\OmniWatchAI\OmniWatchAI.AlertingService.exe` exists
  - **SQL Server Connectivity**: Can connect to database from `appsettings.json` connection string
  - **Database Schema**: `OmniWatchAI` database exists with required tables (Endpoints, HealthCheckResults, Alerts)
  - **Service Account** (optional): If specified via `-ServiceAccount` parameter, validates account exists
- Output includes:
  - ✅ for passed checks
  - ❌ for failed checks
  - Overall status: `All prerequisites met. Ready to install.` OR `Prerequisites missing. See above for details.`

**Test Evidence (All Passed):**
```
Running OmniWatchAI Installation Prerequisites Check...

✅ Operating System: Windows Server 2022
✅ PowerShell Version: 5.1.22621.1778
✅ Administrator Privileges: Confirmed
✅ PollingService Binary: Found at C:\Program Files\OmniWatchAI\OmniWatchAI.PollingService.exe
✅ AlertingService Binary: Found at C:\Program Files\OmniWatchAI\OmniWatchAI.AlertingService.exe
✅ SQL Server Connection: localhost\SQLEXPRESS - Connected successfully
✅ Database Schema: OmniWatchAI database exists with 5 required tables

All prerequisites met. Ready to install.
```

**Test Evidence (Failure - Missing Database):**
```
❌ Database Schema: OmniWatchAI database not found
❌ SQL Server Connection: Cannot open database "OmniWatchAI" requested by the login

Prerequisites missing. Ensure database is created and migrations are applied.
Exit code: 1
```

---

### Scenario 7: Start Services After Installation

**Given** PollingService and AlertingService are installed but not running
**And** Configuration is validated (database accessible, endpoints exist)
**When** I execute `.\Start-OmniWatchAI.ps1`
**Then**:
- PollingService started (transitions to Running state)
- AlertingService started (transitions to Running state)
- Startup logged in Windows Event Log
- Services verified as Running before script exits
- Startup time < 10 seconds for both services
- Script output:
  ```
  Starting OmniWatchAI services...
  PollingService started successfully (3.2 seconds)
  AlertingService started successfully (2.8 seconds)
  All services running.
  ```

**Test Evidence:**
```powershell
Get-Service -Name "OmniWatchAI.*" | Select-Object Name, Status
# Expected: Status=Running for both services
```

**Edge Case - Service Fails to Start:**
```powershell
.\Start-OmniWatchAI.ps1
# If PollingService fails:
# Output: "ERROR: PollingService failed to start. Check Event Log for details."
# Event Log checked and error details displayed
# Exit code: 1
```

---

### Scenario 8: Stop Services (Graceful Shutdown)

**Given** PollingService and AlertingService are running
**When** I execute `.\Stop-OmniWatchAI.ps1`
**Then**:
- PollingService receives stop signal
- PollingService waits for in-flight health checks to complete (max 30 seconds)
- PollingService transitions to Stopped state
- AlertingService receives stop signal
- AlertingService waits for in-flight email sends (max 30 seconds)
- AlertingService transitions to Stopped state
- Both services stopped within 35 seconds total
- Shutdown logged in Event Log
- Script output:
  ```
  Stopping OmniWatchAI services...
  PollingService stopped successfully (12.5 seconds)
  AlertingService stopped successfully (5.3 seconds)
  All services stopped.
  ```

**Test Evidence:**
```powershell
Get-Service -Name "OmniWatchAI.*" | Select-Object Name, Status
# Expected: Status=Stopped for both services
```

**Edge Case - Service Hangs:**
```powershell
.\Stop-OmniWatchAI.ps1
# If service doesn't stop within 35 seconds:
# Output: "WARNING: PollingService did not stop gracefully within timeout. Forcing termination."
# Service forcibly terminated
# Exit code: 0 (still considered success)
```

---

### Scenario 9: Installation with Custom Binary Path

**Given** OmniWatchAI binaries are located at custom path `D:\Apps\OmniWatchAI\`
**When** I execute `.\Install-PollingService.ps1 -BinaryPath "D:\Apps\OmniWatchAI"`
**Then**:
- Script uses custom binary path instead of default `C:\Program Files\OmniWatchAI\`
- Service registered with binary path: `D:\Apps\OmniWatchAI\OmniWatchAI.PollingService.exe`
- Log directory created: `D:\Apps\OmniWatchAI\logs\`
- Service account granted permissions to custom path
- Installation successful

**Test Evidence:**
```powershell
Get-WmiObject -Class Win32_Service | Where-Object { $_.Name -eq "OmniWatchAI.PollingService" } | Select-Object PathName
# Expected: PathName=D:\Apps\OmniWatchAI\OmniWatchAI.PollingService.exe
```

---

### Scenario 10: Idempotent Installation (Force Reinstall)

**Given** PollingService is already installed and running
**When** I execute `.\Install-PollingService.ps1 -Force`
**Then**:
- Script detects existing service
- Existing service stopped gracefully
- Existing service uninstalled
- New service installed with latest binaries
- Service configuration preserved (startup type, service account)
- Installation log records reinstallation
- Script output:
  ```
  Existing PollingService detected. Reinstalling...
  Stopping existing service...
  Uninstalling existing service...
  Installing PollingService...
  PollingService reinstalled successfully.
  ```

**Test Evidence:**
- Service version updated to latest (verify via assembly version)
- Service runs with same service account as before
- Startup type remains Automatic

---

## Technical Specification

### Architecture & Dependencies

**Layer**: Infrastructure / Deployment Automation
**Component**: PowerShell installation scripts
**Related Components**:
- `OmniWatchAI.PollingService.exe` (binary)
- `OmniWatchAI.AlertingService.exe` (binary)
- Windows Service Control Manager (SCM)
- SQL Server (for database connectivity validation)

### File Structure

**PowerShell Scripts to Create:**

```
deployment/
├── Install-PollingService.ps1          # AC 1
├── Install-AlertingService.ps1         # AC 2
├── Configure-ServiceAccount.ps1        # AC 3
├── Configure-AutoRecovery.ps1          # AC 4
├── Uninstall-OmniWatchAI.ps1           # AC 5
├── Validate-Prerequisites.ps1          # AC 6
├── Start-OmniWatchAI.ps1               # AC 7
├── Stop-OmniWatchAI.ps1                # AC 8
├── Install-All.ps1                     # Orchestrates all installation steps
└── README.md                           # Deployment guide

deployment/modules/
├── OmniWatchAI.Installation.psm1       # Shared installation functions
└── OmniWatchAI.Validation.psm1         # Validation helper functions
```

### PowerShell Script Patterns

**Install-PollingService.ps1 (Example):**

```powershell
<#
.SYNOPSIS
    Installs OmniWatchAI PollingService as a Windows Service.

.DESCRIPTION
    Registers PollingService with Windows Service Control Manager.
    Configures startup type, recovery policy, and service account.

.PARAMETER BinaryPath
    Custom path to OmniWatchAI binaries (default: C:\Program Files\OmniWatchAI).

.PARAMETER ServiceAccount
    Service account to run the service (default: Network Service).

.PARAMETER Force
    Reinstall if service already exists.

.EXAMPLE
    .\Install-PollingService.ps1
    Installs service with default settings.

.EXAMPLE
    .\Install-PollingService.ps1 -BinaryPath "D:\Apps\OmniWatchAI" -ServiceAccount "DOMAIN\OmniWatchAI_SA" -Force
    Installs (or reinstalls) service with custom path and service account.
#>

[CmdletBinding()]
param(
    [string]$BinaryPath = "C:\Program Files\OmniWatchAI",
    [string]$ServiceAccount = "NT AUTHORITY\NetworkService",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$serviceName = "OmniWatchAI.PollingService"
$displayName = "OmniWatchAI Polling Service"
$description = "Monitors SQL Server health by executing periodic health checks"

# Import shared functions
Import-Module "$PSScriptRoot\modules\OmniWatchAI.Installation.psm1" -Force

# Validate prerequisites
Write-Host "Validating prerequisites..." -ForegroundColor Cyan
Test-Administrator
Test-BinariesExist -BinaryPath $BinaryPath -ServiceType "PollingService"

# Check if service exists
if (Get-Service -Name $serviceName -ErrorAction SilentlyContinue) {
    if ($Force) {
        Write-Host "Existing service detected. Forcing reinstall..." -ForegroundColor Yellow
        Uninstall-OmniWatchAIService -ServiceName $serviceName
    } else {
        Write-Error "Service '$serviceName' already exists. Use -Force to reinstall."
        exit 1
    }
}

# Install service
Write-Host "Installing $serviceName..." -ForegroundColor Cyan
$binaryFullPath = Join-Path $BinaryPath "OmniWatchAI.PollingService.exe"

New-Service `
    -Name $serviceName `
    -BinaryPathName $binaryFullPath `
    -DisplayName $displayName `
    -Description $description `
    -StartupType Automatic `
    -Credential (Get-ServiceAccountCredential -ServiceAccount $ServiceAccount)

Write-Host "✅ PollingService installed successfully." -ForegroundColor Green
Write-Host "Run 'Start-Service $serviceName' to start the service." -ForegroundColor Yellow

# Log installation
Write-InstallationLog -ServiceName $serviceName -BinaryPath $binaryFullPath -ServiceAccount $ServiceAccount
```

**OmniWatchAI.Installation.psm1 (Shared Module):**

```powershell
function Test-Administrator {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        throw "This script requires Administrator privileges. Run PowerShell as Administrator."
    }
}

function Test-BinariesExist {
    param(
        [string]$BinaryPath,
        [string]$ServiceType
    )

    $exeName = "OmniWatchAI.$ServiceType.exe"
    $fullPath = Join-Path $BinaryPath $exeName

    if (-not (Test-Path $fullPath)) {
        throw "Binary not found: $fullPath. Ensure binaries are copied to $BinaryPath."
    }

    Write-Host "✅ Binary found: $fullPath" -ForegroundColor Green
}

function Write-InstallationLog {
    param(
        [string]$ServiceName,
        [string]$BinaryPath,
        [string]$ServiceAccount
    )

    $logDir = Join-Path (Split-Path $BinaryPath -Parent) "logs"
    if (-not (Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir | Out-Null
    }

    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $logFile = Join-Path $logDir "installation-$ServiceName-$timestamp.log"

    $logEntry = @"
Installation Log
================
Service Name: $ServiceName
Binary Path: $BinaryPath
Service Account: $ServiceAccount
Installed By: $env:USERNAME
Timestamp: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Computer: $env:COMPUTERNAME
"@

    $logEntry | Out-File -FilePath $logFile -Encoding UTF8
    Write-Host "Installation logged: $logFile" -ForegroundColor Gray
}

Export-ModuleMember -Function Test-Administrator, Test-BinariesExist, Write-InstallationLog
```

### Data Model

**Not applicable** - No database changes for deployment scripts.

### API Contract

**Not applicable** - Windows Service installation (no HTTP API).

### Business Rules

1. **Administrator Privileges Required**: All installation scripts require Administrator
2. **Prerequisite Validation**: Must validate binaries, database, SQL connectivity before installation
3. **Idempotent Installation**: `-Force` parameter allows reinstallation without manual cleanup
4. **Graceful Shutdown**: Uninstall/Stop scripts wait for in-flight operations (30-second timeout)
5. **Auto-Recovery**: Services must be configured for automatic restart (60-second delay)
6. **Service Account Permissions**: File system (read binaries, write logs) + SQL Server (db_datareader, db_datawriter)
7. **Installation Logging**: All installation/uninstallation operations logged to `logs\installation-*.log`
8. **Default Paths**: Binary path defaults to `C:\Program Files\OmniWatchAI\` (customizable via parameter)

### Non-Functional Requirements

**Performance:**
- Service installation: < 10 seconds per service
- Service startup: < 10 seconds per service
- Service shutdown: < 35 seconds (30s grace + 5s force)
- Prerequisite validation: < 5 seconds

**Reliability:**
- Auto-recovery configured: 3 restart attempts with 60-second intervals
- 99.9% uptime target (auto-restart on failure)
- Idempotent scripts (can re-run without errors)

**Security:**
- Service runs with least privilege (Network Service or specified service account)
- Service account granted minimal permissions (no local admin)
- SQL Server permissions: db_datareader, db_datawriter only (no db_owner, sysadmin)
- No hardcoded credentials in scripts
- Installation logged for audit trail

**Usability:**
- Clear error messages (e.g., "Service account not found in Active Directory")
- Verbose output (✅/❌ indicators for each step)
- Help documentation (Get-Help Install-PollingService.ps1 -Full)
- README.md with deployment guide

**Scalability:**
- Scripts support custom binary paths (multi-instance deployments)
- Service account can manage 51-200 SQL Server endpoints

---

## Implementation Notes

### Technology Decisions

**PowerShell 5.1+:**
- Native Windows automation (no external dependencies)
- Built-in service management cmdlets (New-Service, Start-Service, Stop-Service)
- Administrator privilege checks
- Logging and error handling

**Windows Service Control Manager (SCM):**
- Native Windows service registration
- Auto-recovery via registry (FailureActions)
- Service account configuration (sc.exe or New-Service -Credential)

**sc.exe vs New-Service:**
- Use `New-Service` cmdlet for installation (PowerShell-native)
- Use `sc.exe failure` for auto-recovery configuration (registry manipulation)

### Code Patterns to Follow

**All PowerShell scripts must follow best practices:**
- [CmdletBinding()] for advanced function support
- Param blocks with type validation and defaults
- $ErrorActionPreference = "Stop" for fail-fast behavior
- try/catch for error handling
- Write-Host with color coding (Cyan=info, Green=success, Yellow=warning, Red=error)
- Comment-based help (synopsis, description, examples)
- Exit codes (0=success, 1=failure)

**Module Pattern:**
- Shared functions in `OmniWatchAI.Installation.psm1`
- Export-ModuleMember for public functions
- Import-Module with -Force for reloading

### Testing Strategy

**Manual Testing:**
- Test on Windows Server 2022 (primary target)
- Test on Windows 10/11 (development environment)
- Test with Network Service account (default)
- Test with domain service account (production scenario)
- Test force reinstall (-Force parameter)
- Test custom binary path (-BinaryPath parameter)

**Integration Testing:**
- Install → Start → Stop → Uninstall (full lifecycle)
- Install → Force crash → Verify auto-recovery
- Prerequisite validation with missing database
- Service account configuration with invalid account

**Validation Checklist:**
- [ ] Services appear in Services.msc
- [ ] Services start and stop cleanly
- [ ] Auto-recovery triggers on crash
- [ ] Event Log entries created
- [ ] Installation logs created
- [ ] File permissions correct (service account can read/write)
- [ ] SQL Server connection successful

### Compliance Checklist

- [ ] PowerShell best practices (CmdletBinding, Param, ErrorActionPreference)
- [ ] Administrator privilege checks
- [ ] Prerequisite validation before installation
- [ ] Idempotent scripts (can re-run safely)
- [ ] Graceful error handling (try/catch, error messages)
- [ ] Installation logging (audit trail)
- [ ] Comment-based help documentation
- [ ] No hardcoded credentials

---

## Dependencies

**Hard Dependencies (Must Complete First):**
- STORY-001: Windows Service Framework - PollingService (service binary exists)
- STORY-002: Windows Service Framework - AlertingService (service binary exists)

**Soft Dependencies (Should Complete First):**
- Database migrations applied (OmniWatchAI database exists)
- Service account created by IT/DBA (for production deployment)

**External Dependencies:**
- Windows Server 2019+ or Windows 10/11
- PowerShell 5.1+
- Administrator privileges
- SQL Server 2022 (database accessible)

---

## Definition of Done

**Code Implementation:**
- [ ] Install-PollingService.ps1 script created (AC 1)
- [ ] Install-AlertingService.ps1 script created (AC 2)
- [ ] Configure-ServiceAccount.ps1 script created (AC 3)
- [ ] Configure-AutoRecovery.ps1 script created (AC 4)
- [ ] Uninstall-OmniWatchAI.ps1 script created (AC 5)
- [ ] Validate-Prerequisites.ps1 script created (AC 6)
- [ ] Start-OmniWatchAI.ps1 script created (AC 7)
- [ ] Stop-OmniWatchAI.ps1 script created (AC 8)
- [ ] OmniWatchAI.Installation.psm1 module created (shared functions)
- [ ] OmniWatchAI.Validation.psm1 module created (validation functions)
- [ ] Install-All.ps1 orchestration script (runs all steps in sequence)

**Testing:**
- [ ] Manual test: Install both services on Windows Server 2022
- [ ] Manual test: Start/stop services via scripts
- [ ] Manual test: Uninstall services
- [ ] Manual test: Force reinstall (-Force parameter)
- [ ] Manual test: Custom binary path (-BinaryPath parameter)
- [ ] Manual test: Service account configuration (domain account)
- [ ] Manual test: Auto-recovery (force crash, verify restart)
- [ ] Manual test: Prerequisite validation (missing database)
- [ ] All tests pass (100% pass rate)

**Quality Gates:**
- [ ] PowerShell scripts follow best practices (CmdletBinding, Param, try/catch)
- [ ] Comment-based help documentation for all scripts
- [ ] Error messages are clear and actionable
- [ ] No hardcoded credentials or sensitive data
- [ ] Code review approved

**Documentation:**
- [ ] README.md in deployment/ directory with full deployment guide
- [ ] Prerequisites section (OS, PowerShell version, permissions)
- [ ] Step-by-step installation instructions
- [ ] Troubleshooting guide (service won't start, permission denied, etc.)
- [ ] Service account setup instructions (SQL Server permissions)
- [ ] Auto-recovery configuration documented

**Deployment:**
- [ ] Scripts tested on Windows Server 2022 (staging environment)
- [ ] Scripts tested with Network Service account (default)
- [ ] Scripts tested with domain service account (production scenario)
- [ ] Installation logs verified (correct format, no sensitive data)
- [ ] Event Log entries verified (service start/stop events)

**Configuration:**
- [ ] Default binary path: `C:\Program Files\OmniWatchAI\`
- [ ] Default service account: `NT AUTHORITY\NetworkService`
- [ ] Auto-recovery: 3 restart attempts, 60-second intervals
- [ ] Startup type: Automatic (starts on boot)

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
- STORY-001: Windows Service Framework - PollingService (provides binary)
- STORY-002: Windows Service Framework - AlertingService (provides binary)

**Successor Stories** (depend on this story):
- STORY-006: Service Configuration Management (appsettings.json, environment-specific config)

**Related Stories** (work together):
- None yet

---

## Story Metrics

**Estimation Breakdown:**
- Install-PollingService.ps1 + Install-AlertingService.ps1: 1 point
- Configure-ServiceAccount.ps1: 1 point
- Configure-AutoRecovery.ps1: 0.5 points
- Uninstall/Start/Stop scripts: 0.5 points
- Validate-Prerequisites.ps1: 1 point
- Shared modules (Installation.psm1, Validation.psm1): 0.5 points
- Testing and documentation: 0.5 points

**Total: 5 story points (estimated 2-3 days for experienced DevOps engineer with PowerShell experience)**

---

## Acceptance Criteria Summary

**Must Have (All 10 ACs must pass):**

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

**All acceptance criteria MUST be validated via manual testing on Windows Server.**

---

**Story Owner:** [TBD]
**Last Updated:** 2025-01-15
**Created By:** DevForgeAI Requirements Analyst
