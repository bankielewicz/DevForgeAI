## Output Format (RCA-006 Phase 2: Structured Requirements)

**CRITICAL:** This subagent provides CONTENT ONLY (no file creation). Parent skill (spec-driven-stories) will assemble your output into v2.0 structured YAML format.

**Your role:** Extract component details from feature description

**Output structured component information:**

When you identify components (services, workers, configuration, logging, repositories, APIs, data models), output in this format:

**Component Type: [Service|Worker|Configuration|Logging|Repository|API|DataModel]**
**Name:** [ComponentName]
**File Path:** src/[layer]/[path]/[ComponentName].cs
**Dependencies:** [List dependencies]

**Requirements:**
1. [Requirement 1 description]
   - Test: [Specific test for this requirement]
   - Priority: [Critical|High|Medium|Low]

2. [Requirement 2 description]
   - Test: [Specific test for this requirement]
   - Priority: [Critical|High|Medium|Low]

**Example Output:**

```
Component Type: Worker
Name: AlertDetectionWorker
File Path: src/Workers/AlertDetectionWorker.cs
Dependencies: IAlertDetectionService, ILogger<AlertDetectionWorker>

Requirements:
1. Must run continuous polling loop with cancellation token support
   - Test: Worker polls at 30s intervals until CancellationToken signals stop
   - Priority: Critical

2. Must handle exceptions without stopping worker
   - Test: Exception in poll iteration doesn't crash worker, logs error, continues
   - Priority: High
```

**Parent skill will convert to YAML:**
```yaml
- type: "Worker"
  name: "AlertDetectionWorker"
  file_path: "src/Workers/AlertDetectionWorker.cs"
  dependencies:
    - "IAlertDetectionService"
    - "ILogger<AlertDetectionWorker>"
  requirements:
    - id: "WKR-001"
      description: "Must run continuous polling loop with cancellation token support"
      testable: true
      test_requirement: "Test: Worker polls at 30s intervals until CancellationToken signals stop"
      priority: "Critical"
    - id: "WKR-002"
      description: "Must handle exceptions without stopping worker"
      testable: true
      test_requirement: "Test: Exception in poll iteration doesn't crash worker, logs error, continues"
      priority: "High"
```

**Component Type Selection Guide:**

Use these component types based on feature description:
- **Service:** Main business logic classes, orchestrators, application services
- **Worker:** Background tasks, polling loops, scheduled jobs (keywords: "poll", "background", "scheduled", "monitor")
- **Configuration:** Settings files, config loading (keywords: "appsettings", "configuration", "settings")
- **Logging:** Log configuration, sinks (keywords: "log", "Serilog", "NLog", "audit")
- **Repository:** Data access layer (keywords: "database", "repository", "Dapper", "EF Core", "data access")
- **API:** HTTP endpoints (keywords: "API", "endpoint", "REST", "GraphQL", "HTTP")
- **DataModel:** Database entities, DTOs (keywords: "entity", "table", "model", "DTO")

**See `devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md` for complete component schemas.**
