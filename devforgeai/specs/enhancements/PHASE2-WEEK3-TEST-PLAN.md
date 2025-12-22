# Week 3 AI Integration Test Plan

**Date:** 2025-11-07
**Purpose:** Define 5 test stories for Day 2 AI implementation testing
**Objective:** Verify 95%+ accuracy across diverse complexity levels

---

## Test Story Selection Criteria

**Diversity requirements:**
- 1 Simple (2-3 components, single type)
- 2 Medium (4-6 components, mixed types)
- 2 Complex (7+ components, all types)

**Coverage requirements:**
- All 7 component types represented
- Business rules in at least 2 stories
- NFRs in at least 3 stories
- API endpoints in at least 2 stories

---

## Test Story 1: Simple (Worker + Configuration)

**Complexity:** 2-3 components
**File:** `tests/fixtures/test-story-1-simple-v1.md`
**Purpose:** Baseline - AI should achieve near-perfect accuracy (98-100%)

**Freeform Tech Spec:**
```markdown
## Technical Specification

### Service Implementation

AlertDetectionWorker will poll the database every 30 seconds for new alerts.
It should inherit from BackgroundService and implement ExecuteAsync method.
The worker must handle exceptions gracefully and support cancellation tokens for clean shutdown.

### Configuration

appsettings.json should contain:
- PollingIntervalSeconds (default: 30)
- ConnectionStrings.OmniWatchDb (required)
```

**Expected AI Output (Ground Truth):**
```yaml
technical_specification:
  format_version: "2.0"
  components:
    - type: "Worker"
      name: "AlertDetectionWorker"
      file_path: "src/Workers/AlertDetectionWorker.cs"
      interface: "BackgroundService"
      polling_interval_ms: 30000
      requirements:
        - id: "WKR-001"
          description: "Must run continuous polling loop with 30s interval and cancellation support"
          testable: true
          test_requirement: "Test: Worker polls at 30s intervals until CancellationToken signals stop"
          priority: "Critical"
        - id: "WKR-002"
          description: "Must handle exceptions without stopping worker"
          testable: true
          test_requirement: "Test: Exception in poll iteration doesn't crash worker, logs error, continues"
          priority: "High"

    - type: "Configuration"
      name: "appsettings.json"
      file_path: "src/appsettings.json"
      required_keys:
        - key: "PollingIntervalSeconds"
          type: "int"
          default: 30
          required: false
          test_requirement: "Test: PollingIntervalSeconds default is 30 when not specified"
        - key: "ConnectionStrings.OmniWatchDb"
          type: "string"
          required: true
          test_requirement: "Test: Configuration loads ConnectionStrings.OmniWatchDb without exception"
```

**Validation Criteria:**
- [ ] 2 components detected (Worker, Configuration)
- [ ] Worker type classified correctly
- [ ] Configuration type classified correctly
- [ ] 2 worker requirements extracted
- [ ] 2 config keys extracted
- [ ] All test requirements specific (not generic)
- [ ] YAML valid and parseable

**Target Accuracy:** 98-100%

---

## Test Story 2: Medium (Service + Worker + Configuration + Logging)

**Complexity:** 4-5 components
**File:** `tests/fixtures/test-story-2-medium-v1.md`
**Purpose:** Test multi-component coordination understanding

**Freeform Tech Spec:**
```markdown
## Technical Specification

### Architecture

AlertingService (hosted service) coordinates the alert detection and email sending workers.
It implements IHostedService with OnStart and OnStop methods to manage worker lifecycle.

### Workers

1. AlertDetectionWorker - Polls database every 30 seconds for new alerts
2. EmailSenderWorker - Polls email queue every 10 seconds to send notifications

### Configuration

appsettings.json contains:
- AlertDetection.PollingIntervalSeconds (default: 30)
- EmailSender.PollingIntervalSeconds (default: 10)
- ConnectionStrings.OmniWatchDb
- SMTP settings (SmtpHost, SmtpPort, SmtpUsername, SmtpPassword)

### Logging

Configure Serilog with three sinks:
- File sink: logs/omniwatch-.txt (daily rolling)
- Windows Event Log: source "OmniWatch Service"
- Database sink: table dbo.Logs

### Non-Functional Requirements

- Service startup time must be under 5 seconds
- Workers must handle exceptions without crashing the service
```

**Expected Output:**
```yaml
technical_specification:
  format_version: "2.0"
  components:
    - type: "Service"
      # ... AlertingService details
    - type: "Worker"
      # ... AlertDetectionWorker details
    - type: "Worker"
      # ... EmailSenderWorker details
    - type: "Configuration"
      # ... appsettings.json with 5 keys
    - type: "Logging"
      # ... Serilog with 3 sinks

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Service startup time must be under 5 seconds"
      metric: "Startup time < 5s"
      test_requirement: "Test: Measure time from OnStart to Running state, assert < 5 seconds"
      priority: "High"
```

**Validation Criteria:**
- [ ] 5 components detected (1 Service, 2 Workers, 1 Configuration, 1 Logging)
- [ ] All types classified correctly
- [ ] Service dependencies include workers
- [ ] Configuration has 5 keys (2 polling intervals, connection string, 3 SMTP settings)
- [ ] Logging has 3 sinks
- [ ] NFRs extracted with measurable metrics
- [ ] All test requirements specific

**Target Accuracy:** 95-97%

---

## Test Story 3: Medium (API + Repository + DataModel)

**Complexity:** 5-6 components
**File:** `tests/fixtures/test-story-3-medium-v1.md`
**Purpose:** Test API contract understanding

**Freeform Tech Spec:**
```markdown
## Technical Specification

### API Endpoints

POST /api/users - Create new user account
- Request: {email, password, name, role}
- Validation: Email format, password strength (min 8 chars, uppercase, lowercase, number, special)
- Response 201: {id, email, name, role, created_at}
- Response 400: Validation errors
- Response 409: Email already exists

GET /api/users/{id} - Retrieve user by ID
- Response 200: User object
- Response 404: User not found

### Data Access

UserRepository implements IUserRepository with Dapper:
- GetById(id) → User or null
- Create(user) → User with generated ID
- Update(user) → Updated user
- Delete(id) → bool success

Must use parameterized queries to prevent SQL injection.

### Data Model

User table (dbo.Users):
- Id (UUID, primary key, auto-generated)
- Email (string, unique, max 255 chars)
- PasswordHash (string, 255 chars, never store plaintext)
- Name (string, max 100 chars)
- Role (enum: customer, admin, moderator)
- CreatedAt (datetime, auto-generated)

### Business Rules

1. Email must be unique across all users
2. Password must meet strength requirements (min 8 chars, mixed case, number, special char)
3. Role must be one of: customer, admin, moderator
```

**Expected Output:**
```yaml
technical_specification:
  format_version: "2.0"
  components:
    - type: "API"
      name: "CreateUser"
      endpoint: "/api/users"
      method: "POST"
      # ... request/response schemas, requirements

    - type: "API"
      name: "GetUser"
      endpoint: "/api/users/{id}"
      method: "GET"
      # ... requirements

    - type: "Repository"
      name: "UserRepository"
      # ... CRUD methods, requirements

    - type: "DataModel"
      name: "User"
      table: "dbo.Users"
      # ... fields with constraints

  business_rules:
    - id: "BR-001"
      rule: "Email must be unique across all users"
      # ... test_requirement
    - id: "BR-002"
      rule: "Password must meet strength requirements"
      # ... test_requirement
    - id: "BR-003"
      rule: "Role must be one of: customer, admin, moderator"
      # ... test_requirement
```

**Validation Criteria:**
- [ ] 4 components (2 APIs, 1 Repository, 1 DataModel)
- [ ] API endpoints correct (POST /api/users, GET /api/users/{id})
- [ ] Repository methods identified
- [ ] DataModel fields with constraints
- [ ] 3 business rules extracted
- [ ] All test requirements specific

**Target Accuracy:** 95-97%

---

## Test Story 4: Complex (Full Stack - 8 components)

**Complexity:** 8 components (all 7 types represented)
**File:** `tests/fixtures/test-story-4-complex-v1.md`
**Purpose:** Stress test - can AI handle full-stack story?

**Freeform Tech Spec:**
```markdown
## Technical Specification

### Complete Alert Management System

**Service Layer:**
AlertingService (IHostedService) coordinates all alert operations. Manages worker lifecycle.

**Background Workers:**
1. AlertDetectionWorker - Polls database every 30s for new alerts
2. EmailSenderWorker - Polls email queue every 10s to send notifications

**API Endpoints:**
- POST /api/alerts - Create new alert
- GET /api/alerts - List all alerts with pagination
- PATCH /api/alerts/{id}/resolve - Mark alert as resolved

**Data Access:**
- AlertRepository - CRUD operations using Dapper
- UserRepository - User lookups for alert assignment

**Database:**
Alert table (dbo.Alerts):
- Id, Severity (Info/Warning/Error), Message (max 500 chars), AssignedToUserId, CreatedAt, ResolvedAt

**Configuration:**
appsettings.json keys: ConnectionStrings.OmniWatchDb, AlertDetection.PollingIntervalSeconds,
EmailSender.PollingIntervalSeconds, Logging.LogLevel.Default

**Logging:**
Serilog with File (logs/omniwatch-.txt), EventLog (OmniWatch Service), Database (dbo.Logs) sinks.

### Business Rules

1. Alert severity must be Info, Warning, or Error
2. Alert message maximum 500 characters
3. Resolved alerts cannot be modified (immutable)

### Performance Requirements

- Service startup < 5 seconds
- API response time < 500ms (p95)
- Support 100 concurrent users
```

**Expected Output:** All 8 components with correct types and requirements

**Components:**
1. Service (AlertingService)
2. Worker (AlertDetectionWorker)
3. Worker (EmailSenderWorker)
4. API (CreateAlert)
5. API (ListAlerts)
6. API (ResolveAlert)
7. Repository (AlertRepository)
8. Repository (UserRepository)
9. DataModel (Alert)
10. Configuration (appsettings.json)
11. Logging (Serilog)

**Plus:** 3 business rules, 3 NFRs

**Target Accuracy:** 92-96% (complex, some details may be missed)

---

## Test Story 5: Edge Case (Ambiguous Text)

**Complexity:** 3-4 components
**File:** `tests/fixtures/test-story-5-edge-v1.md`
**Purpose:** Test AI's ability to handle ambiguous or poorly written specs

**Freeform Tech Spec:**
```markdown
## Technical Specification

The system needs a background process that checks for things periodically.
Configuration is loaded from somewhere. Logging goes to files and maybe the event log.
There's also a database component for storing data.

Performance should be good. Security is important.
```

**Challenge:** Extremely vague, no specific names or details

**Expected AI Behavior:**
- Detect 3-4 generic components (Worker, Configuration, Logging, DataModel)
- Infer generic names (BackgroundWorker, ApplicationConfig, etc.)
- Generate reasonable test requirements despite vagueness
- Handle gracefully (not fail)

**Validation Criteria:**
- [ ] AI doesn't fail (handles vague input)
- [ ] At least 3 components detected
- [ ] Types reasonable given context
- [ ] Test requirements generated (even if generic)
- [ ] YAML valid

**Target Accuracy:** 70-85% (acceptable given poor input quality)

---

## Ground Truth Creation Process

### For Each Test Story

**Step 1: Create v1.0 freeform story**
- Write realistic freeform tech spec
- Include components, business rules, NFRs
- Save as `tests/fixtures/test-story-X-v1.md`

**Step 2: Manually create perfect v2.0 migration**
- Expert human migration (100% accurate)
- All components correctly typed
- All requirements with specific tests
- Save as `tests/expected/test-story-X-ground-truth.md`

**Step 3: Document component inventory**
```yaml
# tests/expected/test-story-X-inventory.yaml
expected_components:
  - type: "Worker"
    name: "AlertDetectionWorker"
    requirement_count: 2
  - type: "Configuration"
    name: "appsettings.json"
    key_count: 2

expected_business_rules: 0
expected_nfrs: 0
```

**Step 4: Define accuracy measurement**
- How to compare AI output to ground truth
- Which fields must match exactly
- Which fields can vary (file paths can be inferred differently)

---

## Accuracy Measurement Methodology

### Component-Level Metrics

**1. Component Detection Rate:**
```
Detected = Number of components AI found
Expected = Number of components in ground truth
Rate = Detected / Expected × 100

Target: ≥95% (at least 95% of components found)
```

**2. Type Classification Accuracy:**
```
Correct = Components with correct type
Total = Components detected
Accuracy = Correct / Total × 100

Target: ≥95%
```

**3. Name Extraction Accuracy:**
```
Correct = Components with correct name
Total = Components detected
Accuracy = Correct / Total × 100

Target: ≥98% (names usually explicit)
```

**4. Requirement Extraction Rate:**
```
Extracted = Total requirements AI generated
Expected = Total requirements in ground truth
Rate = Extracted / Expected × 100

Target: ≥90%
```

**5. Test Requirement Quality Score:**
```
Specific = Test requirements that are specific (not generic)
Total = Total test requirements
Quality = Specific / Total × 100

Scoring:
- "Test: Worker polls at 30s intervals" = Specific ✅
- "Test: Verify worker works" = Generic ❌

Target: ≥85% specific
```

### Story-Level Accuracy

**Overall accuracy per story:**
```
Overall = Average(
    Component Detection,
    Type Classification,
    Name Extraction,
    Requirement Extraction,
    Test Req Quality
)
```

**Aggregate across 5 stories:**
```
Average Accuracy = Sum(Story Accuracies) / 5

Target: ≥95%
Minimum: ≥90% (no story below 90%)
```

---

## Test Execution Plan (Day 2)

### Morning (Hours 1-4)

**09:00-10:00: Implement AI integration**
- Add AIConverter class to migration script
- Implement Claude API calls
- Add prompt building logic

**10:00-11:00: Test Story 1 (Simple)**
```bash
python migrate_story_v1_to_v2.py tests/fixtures/test-story-1-simple-v1.md \
  --ai-assisted --dry-run

# Manual review:
# - Count components: Expected 2, Actual: __
# - Check types: Worker ✓ Configuration ✓
# - Review test requirements: Specific? Y/N
# - Calculate accuracy: __/2 = __%
```

**11:00-12:00: Refine prompt if needed**
- If Test Story 1 accuracy <95%, refine prompt
- Add examples, clarify instructions
- Re-test

**12:00-13:00: Test Story 2 (Medium - Service + Workers)**
- Run migration
- Manual review
- Calculate accuracy

### Afternoon (Hours 5-8)

**14:00-15:00: Test Story 3 (Medium - API + Repository)**
- Focus on API endpoint detection
- Verify repository CRUD methods extracted

**15:00-16:00: Test Story 4 (Complex - Full Stack)**
- Critical test (8 components)
- Detailed accuracy scoring
- Identify any missed components

**16:00-17:00: Test Story 5 (Edge Case - Vague)**
- Test robustness
- Verify graceful handling of poor input

**17:00-18:00: Calculate aggregate accuracy**
- Average across all 5 stories
- Document results
- Determine if ≥95% achieved

---

## Success Criteria (Day 2)

### Must Achieve

- [ ] Test Story 1 accuracy: ≥98%
- [ ] Test Story 2 accuracy: ≥95%
- [ ] Test Story 3 accuracy: ≥95%
- [ ] Test Story 4 accuracy: ≥92%
- [ ] Test Story 5 accuracy: ≥70%
- [ ] **Average across all 5: ≥95%**

### Should Achieve

- [ ] Zero YAML parsing errors (100% valid YAML)
- [ ] Test requirements 85%+ specific (not generic)
- [ ] All 7 component types correctly classified (no Worker → Service errors)

### Nice to Have

- [ ] Test Story 4 accuracy: ≥95% (complex story near-perfect)
- [ ] Test Story 5 accuracy: ≥85% (edge case handled well)

---

## Failure Analysis Protocol

**If any story <90% accuracy:**

**Step 1: Identify failure patterns**
```
Review AI output for test story X:
- Which components were missed? Why?
- Which types were misclassified? Pattern?
- Which test requirements were generic? Examples?
```

**Step 2: Categorize failure type**
- Component Detection Failure (missed components)
- Type Classification Error (Worker → Service)
- Requirement Extraction Failure (generic tests)
- YAML Syntax Error (invalid output)

**Step 3: Refine prompt**
Add specific instructions to address failure pattern:
```
If Worker → Service errors:
  Add: "Worker MUST have continuous execution (loop). Service has discrete lifecycle (OnStart/OnStop)."

If generic test requirements:
  Add more examples of specific vs generic

If components missed:
  Add: "Read carefully, identify ALL components mentioned"
```

**Step 4: Re-test**
- Run migration again with refined prompt
- Measure accuracy improvement
- Iterate until ≥95%

---

## Test Fixture File Structure

```
.claude/skills/devforgeai-story-creation/scripts/tests/
├── fixtures/                           # Input stories (v1.0 freeform)
│   ├── test-story-1-simple-v1.md
│   ├── test-story-2-medium-v1.md
│   ├── test-story-3-medium-v1.md
│   ├── test-story-4-complex-v1.md
│   └── test-story-5-edge-v1.md
│
├── expected/                           # Ground truth (manually created v2.0)
│   ├── test-story-1-ground-truth.md    # Perfect v2.0 migration
│   ├── test-story-2-ground-truth.md
│   ├── test-story-3-ground-truth.md
│   ├── test-story-4-ground-truth.md
│   ├── test-story-5-ground-truth.md
│   ├── test-story-1-inventory.yaml     # Component inventory for accuracy calc
│   ├── test-story-2-inventory.yaml
│   ├── test-story-3-inventory.yaml
│   ├── test-story-4-inventory.yaml
│   └── test-story-5-inventory.yaml
│
└── results/                            # AI migration outputs
    ├── test-story-1-ai-output.md       # AI-generated migration
    ├── test-story-2-ai-output.md
    ├── test-story-3-ai-output.md
    ├── test-story-4-ai-output.md
    └── test-story-5-ai-output.md
```

---

## Accuracy Calculation Script

**File:** `tests/calculate_accuracy.py`

**Usage:**
```bash
python tests/calculate_accuracy.py \
  tests/expected/test-story-1-ground-truth.md \
  tests/results/test-story-1-ai-output.md
```

**Output:**
```
Test Story 1 Accuracy Report:

Component Detection: 2/2 (100%)
Type Classification: 2/2 (100%)
Name Extraction: 2/2 (100%)
Requirement Extraction: 4/4 (100%)
Test Req Quality: 4/4 specific (100%)

Overall Accuracy: 100%

Status: ✅ EXCELLENT
```

---

## Day 2 Exit Criteria

**Proceed to Day 3 if:**
- ✅ Average accuracy ≥95% across 5 test stories
- ✅ No test story <90%
- ✅ Enhanced migration script functional
- ✅ All test requirements ≥85% specific

**Iterate Day 2 if:**
- ⚠️ Average accuracy 90-95% (close, refinement needed)
- ⚠️ One story <90% (outlier, fix prompt)

**Escalate if:**
- 🛑 Average accuracy <90% (fundamental issue)
- 🛑 AI consistently generates invalid YAML
- 🛑 Cannot achieve improvement over pattern matching

---

**This test plan ensures comprehensive validation of AI integration across simple, medium, complex, and edge case scenarios. 95%+ accuracy verified before proceeding to Week 4 pilot.**
