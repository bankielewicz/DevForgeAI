# Technical Specification Requirements (RCA-006)

Reference documentation for test-automator subagent. Contains dual-source test generation strategy for acceptance criteria AND technical specification.

---

## CRITICAL

Test generation MUST cover BOTH acceptance criteria AND technical specification.

**Problem Solved:** Previously, test-automator only generated tests from acceptance criteria, ignoring implementation details in Technical Specification. This led to:
- Interface-level tests only (mocks, not real implementations)
- Minimal implementations passing tests (stubs, placeholders)
- 70% deferral rate due to missing implementation tests

**Solution:** Treat Technical Specification as first-class testable requirements.

---

## Input Validation Before Test Generation

**Before generating ANY tests, validate story contains:**

```python
REQUIRED_SECTIONS = [
    "Acceptance Criteria",      # User behavior requirements (primary)
    "Technical Specification"   # Implementation requirements (MANDATORY)
]

for section in REQUIRED_SECTIONS:
    if section not in story_content:
        raise ValidationError(
            f"Cannot generate tests: Story missing '{section}' section\n\n"
            f"Test-automator requires both acceptance criteria AND technical specification.\n"
            f"Update story to include complete technical specification before test generation."
        )
```

**Technical Specification must contain:**
- [ ] File Structure (directory tree with file paths)
- [ ] Service Implementation Pattern (classes, methods, patterns)
- [ ] Configuration Requirements (appsettings.json structure)
- [ ] Logging Requirements (Serilog/NLog/log4net setup)
- [ ] Data Models (entities, repositories, database schemas)
- [ ] Business Rules (numbered validation rules)

**If Technical Specification incomplete:**

```
WARNING: TECHNICAL SPECIFICATION INCOMPLETE

Story contains Technical Specification section but missing:
- Configuration Requirements (appsettings.json not specified)
- Logging Requirements (no sink specifications)

Proceeding with partial coverage will result in deferrals.

Options:
1. Update story to complete Technical Specification (RECOMMENDED)
2. Generate tests from acceptance criteria only (will create deferrals)
3. Halt test generation, fix story first

Select option: ___
```

---

## Dual-Source Test Generation Strategy

**Tests MUST be generated from TWO sources:**

### Source 1: Acceptance Criteria (60% of tests)

**Purpose:** Validate user-facing behavior

**Test types:**
- Given/When/Then scenario tests
- End-to-end workflow tests
- API contract tests (request/response validation)
- UI interaction tests (if applicable)

**Example from AC1: "Service transitions to 'Running' state within 5 seconds"**

```csharp
[Fact]
public async Task OnStart_WithValidConfiguration_ShouldTransitionToRunningWithin5Seconds()
{
    // Arrange
    var startTime = DateTime.UtcNow;

    // Act
    await _service.StartAsync(CancellationToken.None);

    // Assert
    var elapsed = (DateTime.UtcNow - startTime).TotalSeconds;
    Assert.True(elapsed < 5, $"Service took {elapsed}s to start (expected <5s)");
    Assert.Equal(ServiceState.Running, _service.CurrentState);
}
```

### Source 2: Technical Specification (40% of tests)

**Purpose:** Validate implementation details match specification

**Test types:**
- Component existence tests (files created, classes exist)
- Configuration loading tests (appsettings.json parsed correctly)
- Logging sink tests (Serilog writes to File/EventLog/Database)
- Worker behavior tests (continuous loop, polling interval, exception handling)
- Dependency injection tests (services registered correctly)

**Example from Tech Spec: "Workers/AlertDetectionWorker.cs - Poll database for alerts"**

```csharp
[Fact]
public async Task AlertDetectionWorker_ShouldRunContinuousPollingLoop()
{
    // Arrange
    var cancellationTokenSource = new CancellationTokenSource();
    var pollCount = 0;

    _mockAlertService
        .Setup(s => s.DetectAlertsAsync())
        .Callback(() => pollCount++)
        .ReturnsAsync(new List<Alert>());

    // Act
    var workerTask = _worker.StartAsync(cancellationTokenSource.Token);
    await Task.Delay(1000); // Wait for 1 second
    cancellationTokenSource.Cancel();
    await workerTask;

    // Assert
    Assert.True(pollCount >= 2, $"Worker only polled {pollCount} times in 1s (expected >=2)");
}

[Fact]
public async Task AlertDetectionWorker_ShouldHandleExceptionsWithoutCrashing()
{
    // Arrange
    var cancellationTokenSource = new CancellationTokenSource(TimeSpan.FromSeconds(2));

    _mockAlertService
        .SetupSequence(s => s.DetectAlertsAsync())
        .ThrowsAsync(new Exception("Database timeout"))
        .ReturnsAsync(new List<Alert>()); // Should recover and continue

    // ACT & ASSERT
    await _worker.StartAsync(cancellationTokenSource.Token); // Should NOT throw
    // Worker should log exception but continue polling
}
```

**Example from Tech Spec: "Configure Serilog with File, EventLog, Database sinks"**

```csharp
[Fact]
public void Serilog_ShouldConfigureFileSink()
{
    // Arrange
    var testLogPath = Path.Combine(Path.GetTempPath(), "test-service.log");

    // ACT
    Log.Information("Test log entry");
    Log.CloseAndFlush();

    // Assert
    Assert.True(File.Exists(testLogPath), "Serilog File sink did not create log file");
    var logContent = File.ReadAllText(testLogPath);
    Assert.Contains("Test log entry", logContent);
}
```

---

## Technical Specification Test Matrix

**For EACH component in Technical Specification, generate:**

| Component Type | Required Tests |
|----------------|----------------|
| **Worker** | - Starts and runs loop<br>- Respects polling interval<br>- Handles exceptions<br>- Stops on cancellation |
| **Configuration** | - appsettings.json exists<br>- All required keys present<br>- Configuration loads successfully<br>- Invalid config throws clear error |
| **Logging** | - Logger configured<br>- Each sink writes successfully<br>- Log levels respected<br>- Structured logging works |
| **Repository** | - CRUD operations work<br>- Parameterized queries used<br>- Transactions handled<br>- Connection management correct |
| **Service** | - Dependency injection works<br>- Lifecycle methods called<br>- State transitions correct<br>- Error handling present |

---

## Coverage Gap Detection

**After generating tests from both sources, validate coverage:**

```python
TECH_SPEC_COMPONENTS = parse_technical_specification(story)
GENERATED_TESTS = parse_test_files(test_directory)

COVERAGE_MAP = {}
for component in TECH_SPEC_COMPONENTS:
    tests_for_component = find_tests_for_component(component, GENERATED_TESTS)

    COVERAGE_MAP[component.name] = {
        "requirements": component.requirements,
        "tests_generated": tests_for_component,
        "coverage_percentage": len(tests_for_component) / len(component.requirements) * 100
    }

TOTAL_COVERAGE = calculate_overall_coverage(COVERAGE_MAP)

if TOTAL_COVERAGE < 100:
    report_coverage_gaps(COVERAGE_MAP)
    # DevForgeAI Phase 1 Step 4 will handle gaps via AskUserQuestion
```

---

## Test Generation Workflow (Updated)

**Old workflow (AC-only):**
1. Parse acceptance criteria
2. Generate tests for each AC
3. Done

**New workflow (AC + Tech Spec):**
1. **Validate inputs** - Ensure story has AC AND tech spec
2. **Parse acceptance criteria** - Extract Given/When/Then scenarios
3. **Parse technical specification** - Extract components, requirements
4. **Generate AC tests (60%)** - Behavioral validation tests
5. **Generate tech spec tests (40%)** - Implementation validation tests
6. **Validate coverage** - Ensure all tech spec components tested
7. **Report gaps** - Pass to Phase 1 Step 4 for user decisions

---

## Output Format

**Return structured test suite:**

```json
{
  "tests_generated": 25,
  "acceptance_criteria_tests": 15,
  "technical_specification_tests": 10,
  "coverage": {
    "acceptance_criteria": "100%",
    "technical_specification": "80%"
  },
  "coverage_gaps": [
    {
      "component": "appsettings.json",
      "requirement": "Must contain ConnectionStrings.OmniWatchDb",
      "test_generated": false,
      "reason": "Configuration loading deferred to infrastructure setup"
    }
  ],
  "test_files": [
    "tests/Unit/AlertingServiceTests.cs",
    "tests/Unit/Workers/AlertDetectionWorkerTests.cs",
    "tests/Integration/AlertDetectionIntegrationTests.cs"
  ]
}
```

---

## Anti-Patterns to Avoid

**DON'T generate only interface tests:**
```csharp
// BAD: Only tests that interface is called (mock verification)
_mockAlertService.Verify(s => s.DetectAlertsAsync(), Times.Once);
```

**DO generate implementation behavior tests:**
```csharp
// GOOD: Tests actual behavior (continuous loop, exception handling)
await Task.Delay(1000);
Assert.True(pollCount >= 2, "Worker must poll continuously");
```

**DON'T skip configuration/logging tests:**
```csharp
// These are REQUIRED by tech spec, not optional
```

**DO validate infrastructure setup:**
```csharp
// GOOD: Tests that appsettings.json loads correctly
var config = LoadConfiguration();
Assert.NotNull(config.GetConnectionString("OmniWatchDb"));
```
