# Phase 3 Implementation Plan - Validation Enforcement

**Version:** 1.0
**Date:** 2025-11-07
**Timeline:** Weeks 6-7 (2 weeks)
**Risk Level:** 🟠 High (Automated Enforcement)
**Prerequisites:** Phase 2 successful (structured format deployed)

---

## 🎯 **Phase 3 Objectives**

### **Primary Goal**

Add automated validation in Phase 2 (GREEN) to enforce that implementation matches Technical Specification, preventing minimal stub implementations.

### **Success Criteria**

- [ ] implementation-validator subagent created and functional
- [ ] Phase 2 (GREEN) validates implementation against tech spec
- [ ] Minimal implementations detected automatically (no human oversight)
- [ ] Implementation completeness rises from 90% → 95%+
- [ ] False positive rate <5%
- [ ] Performance acceptable (<5 min validation time)

### **Why After Phase 2**

**Dependency:** Phase 3 validation requires Phase 2 structured format.

**Reason:**
- implementation-validator parses YAML tech specs (deterministic)
- v1.0 freeform specs cannot be parsed reliably (ambiguous)
- Phase 2 provides machine-readable foundation

---

## 📦 **Deliverables**

### **New Files (2 files)**

| File | Lines | Purpose |
|------|-------|---------|
| `implementation-validator.md` | ~400 | New subagent for Phase 2 validation |
| `implementation-validation-guide.md` | ~300 | Reference file for subagent |

**Total:** ~700 lines new

### **Modified Files (3 files)**

| File | Lines Added | Type | Purpose |
|------|-------------|------|---------|
| `tdd-green-phase.md` | +250 | Enhancement | Add Step 3: Implementation Validation |
| `devforgeai-development/SKILL.md` | +50 | Enhancement | Note validation step |
| `subagents-reference.md` | +30 | Documentation | Add implementation-validator |

**Total:** ~430 lines added

### **Documentation (2 files)**

| File | Lines | Purpose |
|------|-------|---------|
| `PHASE3-IMPLEMENTATION-GUIDE.md` | ~400 | User guide for validation |
| `PHASE3-TESTING-CHECKLIST.md` | ~500 | Testing strategy |

**Total:** ~900 lines documentation

---

## 📅 **Timeline: 2 Weeks**

### **Week 6: Subagent Creation & Integration (5 days)**

**Day 1: Subagent Design**
- Design implementation-validator prompt
- Define validation rules (file structure, config, logging, workers)
- Create validation checklist
- Design output format (structured JSON)
- **Time:** 6 hours

**Day 2: Subagent Implementation**
- Create `implementation-validator.md`
- Create `implementation-validation-guide.md`
- Define tool access (Read, Grep, Glob, Bash)
- Add code examples
- **Time:** 8 hours

**Day 3: Integration with Phase 2 (GREEN)**
- Add Step 3 to `tdd-green-phase.md`
- Update workflow to invoke implementation-validator
- Define when to invoke (after backend-architect completes)
- **Time:** 6 hours

**Day 4: Testing - Unit Level**
- Test validation with 3 stories
- Test all validation rules (file structure, config, logging)
- Test false positive scenarios
- Fix bugs
- **Time:** 8 hours

**Day 5: Documentation**
- Create implementation guide
- Create testing checklist
- Update framework documentation
- **Time:** 4 hours

**Week 6 Total:** 32 hours

---

### **Week 7: Testing & Deployment (5 days)**

**Day 1-2: Integration Testing**
- Full /dev workflow with 5 stories
- Test validation catches minimal implementations
- Test false positive handling
- Measure performance impact
- **Time:** 12 hours

**Day 3: Performance Optimization**
- Profile validation execution
- Optimize slow validation rules
- Target: <5 min validation time
- **Time:** 6 hours

**Day 4: User Acceptance Testing**
- Run with real stories
- Collect user feedback
- Measure time impact
- Validate quality improvement
- **Time:** 4 hours

**Day 5: Deployment**
- Final validation
- Deploy to production
- Monitor first 3 runs
- Post-deployment review
- **Time:** 4 hours

**Week 7 Total:** 26 hours

---

## 🔧 **Detailed Implementation Steps**

### **STEP 1: Create implementation-validator Subagent (Week 6, Day 2)**

**File:** `.claude/agents/implementation-validator.md`

```markdown
---
name: implementation-validator
description: Validates that Phase 2 (GREEN) implementation matches Technical Specification, preventing minimal stub implementations. Use after backend-architect completes implementation, before proceeding to Phase 3 (Refactor).
tools: Read, Grep, Glob, Bash
model: haiku
---

# Implementation Validator

Validate that implementation code matches Technical Specification requirements, ensuring no minimal stubs or incomplete implementations.

## Purpose

This subagent prevents the root cause identified in RCA-006: backend-architect creating minimal implementations that pass interface-level tests but don't fulfill technical specification requirements.

**Problem Solved:**
- Minimal worker implementations (no polling loop)
- Missing configuration files (appsettings.json not created)
- Unconfigured logging (Serilog sinks missing)
- Placeholder code passing tests

**Solution:**
Programmatically validate implementation against structured tech spec (v2.0 format).

---

## When Invoked

**Automatic (Proactive):**
- After backend-architect completes Phase 2 (GREEN) implementation
- Before proceeding to Phase 3 (REFACTOR)

**Explicit:**
```
Task(
  subagent_type="implementation-validator",
  description="Validate implementation completeness",
  prompt="Validate that implementation matches Technical Specification in STORY-002..."
)
```

---

## Workflow

### Step 1: Load Technical Specification

**Story file already in conversation context** (loaded by /dev command via @file)

**Extract structured tech spec:**
```python
# Parse YAML from ## Technical Specification section
tech_spec_yaml = extract_yaml_block(story_content, "## Technical Specification")
tech_spec = yaml.safe_load(tech_spec_yaml)

components = tech_spec["technical_specification"]["components"]
business_rules = tech_spec["technical_specification"]["business_rules"]
nfrs = tech_spec["technical_specification"]["non_functional_requirements"]
```

---

### Step 2: Validate File Structure

**For each component with file_path:**

```python
for component in components:
    file_path = component["file_path"]

    # Check file exists
    Glob(pattern=file_path)

    if not found:
        violations.append({
            "component": component["name"],
            "type": "MISSING_FILE",
            "severity": "CRITICAL",
            "message": f"File not created: {file_path}",
            "required_by": component["requirements"]
        })

    # Check file not empty
    Read(file_path=file_path)

    if file_is_empty or file_is_stub:
        violations.append({
            "component": component["name"],
            "type": "STUB_IMPLEMENTATION",
            "severity": "HIGH",
            "message": f"File is stub or minimal: {file_path}",
            "details": "File created but no implementation"
        })
```

---

### Step 3: Validate Configuration Files

**For configuration components:**

```python
for component in components:
    if component["type"] == "Configuration":
        file_path = component["file_path"]  # e.g., appsettings.json

        # Check file exists
        if not file_exists(file_path):
            violations.append({
                "component": component["name"],
                "type": "MISSING_CONFIG",
                "severity": "CRITICAL",
                "message": f"Configuration file not created: {file_path}"
            })
            continue

        # Load and parse config
        Read(file_path=file_path)
        config = json.loads(file_content)

        # Validate required keys
        for key_spec in component["required_keys"]:
            key_path = key_spec["key"]  # e.g., "ConnectionStrings.OmniWatchDb"

            if not key_exists_in_config(config, key_path):
                violations.append({
                    "component": component["name"],
                    "type": "MISSING_CONFIG_KEY",
                    "severity": "HIGH",
                    "message": f"Missing required key: {key_path}",
                    "expected": key_spec.get("example", "N/A")
                })
```

---

### Step 4: Validate Logging Configuration

**For logging components:**

```python
for component in components:
    if component["type"] == "Logging":
        logging_system = component["name"]  # e.g., "Serilog"
        config_file = component["file_path"]  # e.g., "Program.cs"

        # Read configuration file
        Read(file_path=config_file)

        # Validate logger initialization
        if logging_system == "Serilog":
            if "Log.Logger = new LoggerConfiguration()" not in file_content:
                violations.append({
                    "component": "Serilog",
                    "type": "LOGGING_NOT_CONFIGURED",
                    "severity": "HIGH",
                    "message": "Serilog not initialized in Program.cs"
                })

            # Validate each sink
            for sink in component["sinks"]:
                sink_name = sink["name"]  # e.g., "File", "EventLog"

                if f".WriteTo.{sink_name}" not in file_content:
                    violations.append({
                        "component": "Serilog",
                        "type": "MISSING_SINK",
                        "severity": "MEDIUM",
                        "message": f"Serilog sink not configured: {sink_name}",
                        "required_by": sink["test_requirement"]
                    })
```

---

### Step 5: Validate Worker Implementations

**For worker components:**

```python
for component in components:
    if component["type"] == "Worker":
        file_path = component["file_path"]

        # Read worker file
        Read(file_path=file_path)

        # Validate continuous loop
        for req in component["requirements"]:
            if "continuous loop" in req["description"].lower():
                if "while (" not in file_content:
                    violations.append({
                        "component": component["name"],
                        "type": "NO_POLLING_LOOP",
                        "severity": "CRITICAL",
                        "message": f"Worker missing continuous loop: {component['name']}",
                        "requirement": req["id"],
                        "expected": "while (!cancellationToken.IsCancellationRequested)"
                    })

        # Validate exception handling
        for req in component["requirements"]:
            if "exception" in req["description"].lower():
                if "try" not in file_content or "catch" not in file_content:
                    violations.append({
                        "component": component["name"],
                        "type": "NO_EXCEPTION_HANDLING",
                        "severity": "HIGH",
                        "message": f"Worker missing exception handling: {component['name']}",
                        "requirement": req["id"]
                    })
```

---

### Step 6: Generate Validation Report

**Output structured JSON:**

```json
{
  "validation_result": "FAIL",
  "implementation_completeness": "45%",
  "components_validated": 5,
  "components_passing": 2,
  "components_failing": 3,
  "violations": [
    {
      "component": "AlertDetectionWorker",
      "type": "NO_POLLING_LOOP",
      "severity": "CRITICAL",
      "message": "Worker missing continuous loop",
      "file": "src/Workers/AlertDetectionWorker.cs",
      "requirement": "WKR-001",
      "expected": "while (!cancellationToken.IsCancellationRequested)",
      "actual": "Placeholder comment only"
    },
    {
      "component": "appsettings.json",
      "type": "MISSING_CONFIG",
      "severity": "CRITICAL",
      "message": "Configuration file not created",
      "file": "src/OmniWatch.Service/appsettings.json",
      "requirement": "All configuration components"
    },
    {
      "component": "Serilog",
      "type": "MISSING_SINK",
      "severity": "HIGH",
      "message": "File sink not configured",
      "file": "Program.cs",
      "requirement": "LOG-001"
    }
  ],
  "recommendations": [
    "Implement continuous polling loop in AlertDetectionWorker (WKR-001)",
    "Create appsettings.json with required keys",
    "Configure Serilog File sink in Program.cs"
  ]
}
```

---

### Step 7: Return Result to Skill

**Phase 2 (GREEN) receives validation result:**

```python
# In tdd-green-phase.md Step 3 (NEW):

validation_result = implementation_validator_result

if validation_result["validation_result"] == "FAIL":
    # Display violations
    Display: "❌ PHASE 2 INCOMPLETE: Implementation doesn't match Technical Specification"
    Display: ""
    Display: f"Implementation Completeness: {validation_result['implementation_completeness']}"
    Display: ""
    Display: "Violations:"
    for violation in validation_result["violations"]:
        Display: f"  - {violation['component']}: {violation['message']}"
        Display: f"    Severity: {violation['severity']}"
        Display: f"    Expected: {violation.get('expected', 'N/A')}"

    # Ask user how to proceed
    AskUserQuestion(
        questions=[{
            "question": "Implementation validation failed. How should we proceed?",
            "header": "Validation",
            "multiSelect": False,
            "options": [
                {
                    "label": "Complete implementation now",
                    "description": "Re-invoke backend-architect to implement missing components (RECOMMENDED)"
                },
                {
                    "label": "Defer to follow-up story",
                    "description": "Document as technical debt, create tracking story"
                },
                {
                    "label": "Update tech spec",
                    "description": "Remove requirements from tech spec (requires ADR)"
                }
            ]
        }]
    )

elif validation_result["validation_result"] == "PASS":
    Display: "✅ Implementation Validation PASSED"
    Display: f"Implementation Completeness: {validation_result['implementation_completeness']}"
    Display: "Proceeding to Phase 3 (REFACTOR)..."
```

---

## Success Criteria

- [ ] All components validated against tech spec
- [ ] File structure validated (all files exist, not stubs)
- [ ] Configuration validated (keys present, loaded)
- [ ] Logging validated (sinks configured)
- [ ] Workers validated (loops, exception handling)
- [ ] Violations detected accurately (false positive rate <5%)
- [ ] Recommendations actionable
- [ ] Returns structured JSON result

---

## Framework Integration

**Invoked by:**
- devforgeai-development skill (Phase 2, after backend-architect)

**Requires:**
- Structured tech spec (v2.0 format from Phase 2)
- Implementation code (from backend-architect)

**Returns:**
- Validation result (PASS/FAIL)
- Violations list with severity
- Recommendations for fixes

**References:**
- `.claude/skills/devforgeai-development/references/implementation-validation-guide.md`

---
```

**Length:** ~400 lines

---

### **STEP 2: Create Reference File (Week 6, Day 2)**

**File:** `.claude/skills/devforgeai-development/references/implementation-validation-guide.md`

**Content:**
- DevForgeAI context (quality gates, workflow states)
- Validation rules by component type (7 types)
- Severity classification (CRITICAL, HIGH, MEDIUM, LOW)
- False positive prevention (flexible matching)
- Integration with Phase 2 workflow
- Troubleshooting guide

**Length:** ~300 lines

---

### **STEP 3: Add Step 3 to tdd-green-phase.md (Week 6, Day 3)**

**File:** `.claude/skills/devforgeai-development/references/tdd-green-phase.md`

**Insert after implementation (likely after Step 2):**

```markdown
### Step 3: Implementation Validation (RCA-006 Phase 3)

**Purpose:** Validate implementation matches Technical Specification before proceeding to refactoring.

**Execution:** After backend-architect completes implementation, before Phase 3 (REFACTOR).

---

#### 3.1 Invoke implementation-validator Subagent

```
Task(
  subagent_type="implementation-validator",
  description="Validate implementation completeness",
  prompt="Validate that implementation matches Technical Specification in story.

  Story content already loaded in conversation (via @file reference).

  Technical Specification is in structured v2.0 format (YAML).

  Validate:
  1. File structure (all files exist, not stubs)
  2. Configuration (appsettings.json created, keys present)
  3. Logging (Serilog configured, sinks active)
  4. Workers (polling loops, exception handling)
  5. Repositories (Dapper usage, parameterized queries)
  6. Services (DI, lifecycle, state management)

  Return:
  - Validation result (PASS/FAIL)
  - Implementation completeness percentage
  - Violations (component, type, severity, message)
  - Recommendations for fixes

  Reference file: implementation-validation-guide.md (loaded as needed)
  "
)
```

---

#### 3.2 Process Validation Result

**Parse subagent output:**
```python
validation_result = extract_json_from_subagent(response)

implementation_completeness = validation_result["implementation_completeness"]
violations = validation_result["violations"]
```

**Display result:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 IMPLEMENTATION VALIDATION REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Story: {STORY_ID}
Phase: 2 (GREEN - Implementation)

Components Validated: 5
Implementation Completeness: 45% ⚠️

VALIDATION RESULT: FAIL

Violations Found: 3

1. AlertDetectionWorker (CRITICAL)
   Issue: Missing continuous polling loop
   File: src/Workers/AlertDetectionWorker.cs
   Expected: while (!cancellationToken.IsCancellationRequested)
   Actual: Placeholder comment only
   Requirement: WKR-001

2. appsettings.json (CRITICAL)
   Issue: Configuration file not created
   File: src/OmniWatch.Service/appsettings.json
   Required Keys: ConnectionStrings.OmniWatchDb, AlertingService.PollingIntervalSeconds

3. Serilog (HIGH)
   Issue: File sink not configured
   File: Program.cs
   Expected: .WriteTo.File("logs/omniwatch-.txt")
   Actual: Serilog initialized but no sinks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

#### 3.3 Request User Decision

**If validation FAILS:**

```
AskUserQuestion(
    questions=[{
        "question": "Implementation validation failed (3 violations). How should we proceed?",
        "header": "Validation",
        "multiSelect": False,
        "options": [
            {
                "label": "Complete implementation now",
                "description": "Re-invoke backend-architect to fix violations (15-20 min). RECOMMENDED."
            },
            {
                "label": "Defer to follow-up story",
                "description": "Document as technical debt, create tracking story for missing components."
            },
            {
                "label": "Update tech spec",
                "description": "Remove requirements from tech spec (requires ADR for scope change)."
            }
        ]
    }]
)
```

---

#### 3.4 Process User Decision

**Decision 1: Complete implementation now**
```python
if user_decision == "complete_now":
    # Re-invoke backend-architect with specific fixes
    Task(
        subagent_type="backend-architect",
        description="Fix implementation violations",
        prompt=f"""
        Fix the following implementation violations:

        {format_violations(violations)}

        Technical Specification (structured YAML) is in conversation context.

        Implement missing components:
        1. AlertDetectionWorker: Add continuous polling loop
        2. appsettings.json: Create file with required keys
        3. Serilog: Configure File sink

        After fixes, run tests to ensure they still pass.
        """
    )

    # Re-run validation
    goto Step 3.1
```

**Decision 2: Defer to follow-up story**
```python
elif user_decision == "defer":
    # Same process as Phase 1 Step 4.5 (Defer decision)
    # Create follow-up story for deferred components
    # Document in workflow history

    DEFERRAL_RECORD = {
        "components": ["AlertDetectionWorker", "appsettings.json", "Serilog"],
        "violations": violations,
        "reason": "User deferred implementation to follow-up story",
        "follow_up_story": "STORY-XXX",
        "approved_by": "user",
        "approved_at": timestamp
    }

    # Add to Phase 4.5 tracking
```

**Decision 3: Update tech spec**
```python
elif user_decision == "update_spec":
    # Require ADR (same as Phase 1 Step 4.5)
    # Guide user through ADR creation
    # HALT workflow, wait for manual updates
```

---

#### 3.5 Validate All Violations Resolved

**Enforcement:**
```python
if validation_result["validation_result"] == "FAIL" and user_decision != "defer":
    # Re-run validation after fixes
    goto Step 3.1

if user_decision == "defer":
    # Allow progression with documented deferrals
    Display: "⚠️ Proceeding with deferred components (technical debt created)"

if validation_result["validation_result"] == "PASS":
    Display: "✅ Step 3 Complete: Implementation validated"
    Display: "Proceeding to Phase 3 (REFACTOR)..."
```

---

#### Step 3 Success Criteria

- [ ] implementation-validator invoked successfully
- [ ] Validation report generated
- [ ] Violations detected accurately
- [ ] User decision collected (if violations)
- [ ] Violations resolved OR deferred with approval
- [ ] Implementation completeness ≥90% (or user-approved <90%)
- [ ] Phase 2 completes successfully

---
```

**End of tdd-green-phase.md enhancement**

---

## 🚨 **Breaking Changes**

### **None - Phase 3 is Additive**

**No breaking changes:**
- ✅ Adds validation step to Phase 2
- ✅ Works with structured tech specs from Phase 2
- ✅ Backward compatible (v1.0 stories skip validation)
- ✅ Optional enforcement (can configure strict/warn mode)

**Configuration option:**
```yaml
# In devforgeai/context/architecture-constraints.md or tech-stack.md
implementation_validation:
  mode: "strict"  # HALT on violations
  # OR mode: "warn"  # Display violations, allow proceed
```

---

## 📊 **Success Metrics**

### **Phase 3 Success Criteria**

**Technical:**
- [ ] implementation-validator subagent created
- [ ] Step 3 integrated into Phase 2 (GREEN)
- [ ] Validation rules cover 7 component types
- [ ] False positive rate <5%
- [ ] Performance <5 min per validation

**Quality:**
- [ ] Implementation completeness: 90% → 95%+
- [ ] Minimal implementations detected: 100% (no escapes)
- [ ] Deferral rate remains <10% (Phase 1 + Phase 3)
- [ ] Technical debt fully documented

**User Experience:**
- [ ] Validation messages clear
- [ ] Recommendations actionable
- [ ] Time increase acceptable (+5-10 min)
- [ ] User satisfaction ≥80%

---

## 🎯 **Decision Point: End of Week 7**

### **GO Criteria (Phase 3 Complete)**

**GREEN LIGHT if ALL met:**
- ✅ All technical criteria met
- ✅ False positive rate <5%
- ✅ Performance <5 min
- ✅ User satisfaction ≥80%
- ✅ No critical bugs

**Action:** Phase 3 complete, framework at v2.0

---

### **ITERATE Criteria**

**YELLOW LIGHT if SOME missed:**
- ⚠️ False positive rate 5-10%
- ⚠️ Performance 5-10 min
- ⚠️ User satisfaction 60-80%
- ⚠️ Minor bugs found

**Action:** Week 8 optimization, re-test

---

### **NO-GO Criteria**

**RED LIGHT if ANY critical:**
- 🛑 False positive rate >10%
- 🛑 Performance >10 min
- 🛑 User rejection
- 🛑 Critical bugs

**Action:** Rollback, reassess

---

## 📚 **References**

**Implementation:**
- `.claude/agents/implementation-validator.md` (NEW - Week 6)
- `.claude/skills/devforgeai-development/references/implementation-validation-guide.md` (NEW - Week 6)
- `.claude/skills/devforgeai-development/references/tdd-green-phase.md` (Step 3 added)

**Documentation:**
- `devforgeai/specs/enhancements/PHASE3-IMPLEMENTATION-GUIDE.md` (NEW)
- `devforgeai/specs/enhancements/PHASE3-TESTING-CHECKLIST.md` (NEW)

---

**Phase 3 completes the RCA-006 enhancement by enforcing implementation completeness through automated validation.**
