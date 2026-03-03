# EPIC-047: Technical Debt Automation Enhancement - Requirements Specification

**Document Version:** 1.0
**Created:** 2026-01-19
**Last Updated:** 2026-01-19
**Status:** Draft
**Author:** claude/requirements-analyst

---

## 1. Executive Summary

### 1.1 Purpose

This requirements specification defines the functional, non-functional, and integration requirements for EPIC-047: Technical Debt Automation Enhancement. The epic aims to transform the current manual technical debt tracking process into an automated, workflow-integrated system that prevents debt compounding and provides clear remediation pathways.

### 1.2 Scope

The epic encompasses six features delivered over 2 sprints (4 weeks):

| Feature | ID | Points | Complexity | Description |
|---------|-----|--------|------------|-------------|
| Technical Debt Register v2.0 Format Migration | F1 | 5 | Medium | Migrate register to hybrid YAML+Markdown with machine-parseable sections |
| QA-to-Technical-Debt Bridge | F2 | 8 | High | Automate debt entry creation from QA failure patterns |
| Standalone /verify-ac Command | F3 | 8 | High | Provide independent AC verification outside QA workflow |
| Next Steps Workflow After Debt Addition | F4 | 8 | High | Guided workflow for debt remediation decisions |
| Debt Compounding Prevention - Dev Pre-flight | F5 | 3 | Low | Block /dev if story references unresolved debt |
| Debt Compounding Prevention - Story Creation | F6 | 2 | Low | Warn during story creation if related debt exists |

**Total Story Points:** 34

### 1.3 Goals and Objectives

**Primary Goals:**

1. **Automate debt capture** - Eliminate manual debt entry by bridging QA failures to register
2. **Prevent debt compounding** - Block development that would add debt to existing debt
3. **Streamline remediation** - Provide clear next steps when debt is identified
4. **Enable standalone verification** - Allow AC verification independent of full QA workflow

**Success Metrics:**

| Metric | Current State | Target State | Measurement |
|--------|---------------|--------------|-------------|
| Manual debt entries | 100% manual | <10% manual | Register audit |
| Debt compounding incidents | Untracked | 0 per sprint | Pre-flight blocks |
| Time to debt remediation | Undefined | <3 sprints avg | Resolution tracking |
| AC verification accessibility | QA-only | On-demand | Command usage |

### 1.4 User-Locked Preferences

The following design decisions have been confirmed with the user and are LOCKED:

| Decision | Preference | Rationale |
|----------|------------|-----------|
| Automation Mode | Prompt first (confirm before adding) | User wants visibility before register modification |
| Next Steps Options | Remediation story, Debt epic, Add to sprint | Three action paths post-debt-addition |
| Command Interface | Both `/verify-ac` AND `/qa --verify-ac` flag | Supports different user workflows |
| Register Format | Hybrid YAML + Markdown | Machine-parseable metadata with human-readable details |

---

## 2. Functional Requirements

### 2.1 F1: Technical Debt Register v2.0 Format Migration

**Priority:** High
**Complexity:** Medium (5 points)
**Sprint Target:** Sprint 1

#### 2.1.1 Overview

Migrate the technical debt register from unstructured Markdown (v1.0) to a hybrid YAML+Markdown format (v2.0) that enables machine parsing while maintaining human readability.

#### 2.1.2 Functional Requirements

| ID | Requirement | Priority | Testable |
|----|-------------|----------|----------|
| FR-1.1 | Register MUST include YAML frontmatter with version, last_updated, and schema_version fields | Critical | Yes |
| FR-1.2 | Each debt entry MUST be a YAML block with machine-parseable fields (id, story_origin, type, severity, status, created_date, resolution_target) | Critical | Yes |
| FR-1.3 | Each debt entry MAY include Markdown description block following YAML metadata | High | Yes |
| FR-1.4 | System MUST validate register schema on read operations | High | Yes |
| FR-1.5 | Existing v1.0 entries MUST be migrated to v2.0 format via migration script | Medium | Yes |
| FR-1.6 | Register MUST support filtering by status (Open, In Progress, Resolved) | Medium | Yes |
| FR-1.7 | Register MUST support filtering by type (Story Split, Scope Change, External Blocker, QA Failure) | Medium | Yes |

#### 2.1.3 Data Schema (v2.0)

```yaml
# Technical Debt Register v2.0 Schema
---
version: "2.0"
schema_version: "2.0"
last_updated: "2026-01-19T12:00:00Z"
maintainer: "devforgeai-development skill"
analyzer: "technical-debt-analyzer subagent"

summary:
  total_open: 0
  total_in_progress: 0
  total_resolved: 0
  last_analyzed: null
  debt_by_type:
    story_split: 0
    scope_change: 0
    external_blocker: 0
    qa_failure: 0
  critical_issues:
    circular_deferrals: 0
    stale_debt_90days: 0

entries:
  - id: "DEBT-001"
    story_origin: "STORY-XXX"
    title: "Deferred item description"
    type: "Story Split|Scope Change|External Blocker|QA Failure"
    severity: "Critical|High|Medium|Low"
    status: "Open|In Progress|Resolved"
    created_date: "2026-01-19"
    resolution_target: "Sprint-X|YYYY-MM-DD|When {condition}"
    estimated_effort: "X points"
    justification: "Brief reason for deferral"
    cross_references:
      source_ac: "AC#N"              # Which AC was violated (if applicable)
      remediation_story: "STORY-YYY" # Story created to fix this debt
      epic: "EPIC-XXX"               # Debt epic if grouped for sprint planning
      adr: "ADR-XXX"                 # ADR if architectural decision involved
      blocker_condition: null        # External blocker condition (if applicable)
    tags: ["tag1", "tag2"]
    # Optional Markdown description follows in separate block
---

## DEBT-001: [Title]

**Detailed Description:**
[Extended Markdown description with context, impact analysis, and remediation notes]

**Resolution Notes:**
[Updated as debt is worked on]

---
```

#### 2.1.4 Acceptance Criteria

```xml
<acceptance_criteria id="AC1">
  <given>The technical-debt-register.md file exists in v1.0 format</given>
  <when>The migration script is executed</when>
  <then>All existing entries are converted to v2.0 YAML format with preserved data</then>
  <verification>
    <source_files>
      <file hint="Register file">devforgeai/technical-debt-register.md</file>
      <file hint="Migration script">scripts/migrate-debt-register-v2.sh</file>
    </source_files>
    <test_file>tests/STORY-XXX/test-ac1-migration.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>

<acceptance_criteria id="AC2">
  <given>A v2.0 format register exists</given>
  <when>A debt entry is programmatically read</when>
  <then>YAML metadata is parsed into structured data object with all required fields</then>
</acceptance_criteria>

<acceptance_criteria id="AC3">
  <given>An invalid YAML structure in the register</given>
  <when>Schema validation runs</when>
  <then>Specific validation errors are reported with line numbers and field names</then>
</acceptance_criteria>
```

---

### 2.2 F2: QA-to-Technical-Debt Bridge

**Priority:** Critical
**Complexity:** High (8 points)
**Sprint Target:** Sprint 1

#### 2.2.1 Overview

Create an automated bridge between QA failures and technical debt registration. When QA identifies deferred items or fails due to coverage/anti-pattern issues, the system prompts for debt addition with pre-populated entry data.

#### 2.2.2 Functional Requirements

| ID | Requirement | Priority | Testable |
|----|-------------|----------|----------|
| FR-2.1 | System MUST detect QA failures that warrant debt tracking (coverage gaps, deferred DoD items, anti-pattern violations) | Critical | Yes |
| FR-2.2 | System MUST prompt user before adding entry to register (per locked preference: "Prompt first") | Critical | Yes |
| FR-2.3 | System MUST pre-populate debt entry fields from QA context (story ID, failure type, severity) | High | Yes |
| FR-2.4 | User MUST be able to modify pre-populated values before confirmation | High | Yes |
| FR-2.5 | System MUST validate user input before register update | High | Yes |
| FR-2.6 | System MUST append entry to register using v2.0 format | Critical | Yes |
| FR-2.7 | System MUST update register summary counts after entry addition | Medium | Yes |
| FR-2.8 | System MUST trigger Next Steps Workflow (F4) after successful entry | High | Yes |

#### 2.2.3 Debt Detection Triggers

The bridge activates when QA reports:

| Trigger | Debt Type | Severity Mapping |
|---------|-----------|------------------|
| Coverage below 95% (Business Logic) | QA Failure | Critical |
| Coverage below 85% (Application) | QA Failure | High |
| Coverage below 80% (Infrastructure) | QA Failure | High |
| CRITICAL anti-pattern violation | QA Failure | Critical |
| HIGH anti-pattern violation | QA Failure | High |
| Deferred DoD item with "External blocker" | External Blocker | Based on item |
| Story split during development | Story Split | Medium |
| Scope change during development | Scope Change | Medium |

#### 2.2.4 User Prompt Interface

```markdown
## Technical Debt Detected

QA validation for **STORY-XXX** identified potential technical debt:

**Detected Issue:**
- Type: QA Failure - Coverage Gap
- Component: src/services/OrderService.ts
- Current: 82% | Required: 95% | Gap: 13%

**Proposed Debt Entry:**

| Field | Value | [Edit] |
|-------|-------|--------|
| ID | DEBT-047 (auto) | - |
| Title | Coverage gap in OrderService | [x] |
| Type | QA Failure | [x] |
| Severity | Critical | [x] |
| Resolution Target | Sprint-2 | [x] |
| Estimated Effort | 3 points | [x] |

**Actions:**
- [ ] Add to Technical Debt Register
- [ ] Skip (do not track as debt)
- [ ] Cancel QA workflow
```

#### 2.2.5 Acceptance Criteria

```xml
<acceptance_criteria id="AC1">
  <given>QA validation fails with coverage below threshold</given>
  <when>The QA workflow reaches Phase 3 result determination</when>
  <then>User is prompted with pre-populated debt entry form</then>
</acceptance_criteria>

<acceptance_criteria id="AC2">
  <given>User confirms debt entry addition</given>
  <when>The entry is validated</when>
  <then>Entry is appended to register with v2.0 format and summary counts updated</then>
</acceptance_criteria>

<acceptance_criteria id="AC3">
  <given>User selects "Skip" for debt tracking</given>
  <when>The prompt completes</when>
  <then>No entry is added and QA workflow continues normally</then>
</acceptance_criteria>

<acceptance_criteria id="AC4">
  <given>Debt entry is successfully added</given>
  <when>Register update completes</when>
  <then>Next Steps Workflow (F4) is triggered automatically</then>
</acceptance_criteria>
```

---

### 2.3 F3: Standalone /verify-ac Command

**Priority:** High
**Complexity:** High (8 points)
**Sprint Target:** Sprint 1

#### 2.3.1 Overview

Provide a standalone command for acceptance criteria verification that operates independently of the full QA workflow. This enables developers to verify AC compliance during development without triggering comprehensive QA validation.

#### 2.3.2 Functional Requirements

| ID | Requirement | Priority | Testable |
|----|-------------|----------|----------|
| FR-3.1 | System MUST provide `/verify-ac STORY-XXX` as standalone command | Critical | Yes |
| FR-3.2 | System MUST provide `/qa STORY-XXX --verify-ac` as alternative invocation | Critical | Yes |
| FR-3.3 | Both invocation methods MUST produce identical verification results | Critical | Yes |
| FR-3.4 | Command MUST use ac-compliance-verifier subagent for verification | High | Yes |
| FR-3.5 | Command MUST require XML AC format in story (per EPIC-046) | Critical | Yes |
| FR-3.6 | Command MUST report PASS/FAIL per AC with evidence | High | Yes |
| FR-3.7 | Command MUST NOT trigger full QA workflow (coverage analysis, anti-pattern scan, etc.) | Critical | Yes |
| FR-3.8 | Command MUST NOT update story status (verification only, no state change) | High | Yes |
| FR-3.9 | Command MUST generate verification report in JSON format | Medium | Yes |
| FR-3.10 | Command token budget MUST be <20K tokens | Medium | Yes |

#### 2.3.3 Command Interface

**Standalone Command:**
```bash
/verify-ac STORY-001
```

**QA Flag Alternative:**
```bash
/qa STORY-001 --verify-ac
```

**Output Format:**
```
AC Verification Results for STORY-001
======================================

Total ACs: 5 | Passed: 4 | Failed: 1 | Skipped: 0

AC#1: User Registration Form      [PASS]
  Evidence: src/components/RegistrationForm.tsx (lines 45-120)
  Coverage: Tests found in tests/STORY-001/test-ac1-registration.py

AC#2: Email Validation            [PASS]
  Evidence: src/validators/email.ts (lines 10-35)
  Coverage: Tests found in tests/STORY-001/test-ac2-email.py

AC#3: Password Strength Check     [FAIL]
  Expected: Minimum 12 characters with complexity rules
  Actual: Only length check implemented (no complexity)
  Missing: Uppercase, lowercase, number, special char validation
  Location: src/validators/password.ts (lines 5-15)

AC#4: Duplicate Email Prevention  [PASS]
  Evidence: src/services/UserService.ts (lines 78-95)

AC#5: Confirmation Email Sent     [PASS]
  Evidence: src/services/EmailService.ts (lines 120-145)

Overall Status: PARTIAL (4/5 ACs verified)

Recommendations:
1. Implement password complexity rules per AC#3
2. Add tests for complexity validation
```

#### 2.3.4 Skill Architecture

**New Skill:** `.claude/skills/devforgeai-ac-verification/SKILL.md`

```yaml
---
name: devforgeai-ac-verification
description: Standalone acceptance criteria verification using fresh-context technique. Invokes ac-compliance-verifier subagent for independent verification without full QA workflow.
tools: [Read, Grep, Glob, Task, AskUserQuestion]
model: claude-opus-4-6
---
```

**Skill Phases:**

| Phase | Description | Token Budget |
|-------|-------------|--------------|
| Phase 0: Setup | Validate CWD, load story file, extract AC blocks | 2K |
| Phase 1: Parse | Parse XML AC format, validate schema | 3K |
| Phase 2: Verify | Invoke ac-compliance-verifier per AC | 10K |
| Phase 3: Report | Aggregate results, generate report | 3K |
| Phase 4: Output | Display results, write JSON report | 2K |

#### 2.3.5 Acceptance Criteria

```xml
<acceptance_criteria id="AC1">
  <given>A story file with XML acceptance criteria exists</given>
  <when>/verify-ac STORY-XXX is executed</when>
  <then>AC verification runs and produces PASS/FAIL report per AC</then>
</acceptance_criteria>

<acceptance_criteria id="AC2">
  <given>A story file with XML acceptance criteria exists</given>
  <when>/qa STORY-XXX --verify-ac is executed</when>
  <then>Identical verification results are produced as standalone command</then>
</acceptance_criteria>

<acceptance_criteria id="AC3">
  <given>AC verification completes</given>
  <when>Results are generated</when>
  <then>Story status is NOT updated (verification only)</then>
</acceptance_criteria>

<acceptance_criteria id="AC4">
  <given>Story has legacy markdown AC format (not XML)</given>
  <when>/verify-ac is executed</when>
  <then>Error message instructs user to migrate to XML format per EPIC-046</then>
</acceptance_criteria>
```

---

### 2.4 F4: Next Steps Workflow After Debt Addition

**Priority:** High
**Complexity:** High (8 points)
**Sprint Target:** Sprint 2

#### 2.4.1 Overview

Provide a guided workflow for debt remediation decisions immediately after debt is added to the register. Users select from three action paths (per locked preference): create remediation story, add to debt epic, or add to current sprint.

#### 2.4.2 Functional Requirements

| ID | Requirement | Priority | Testable |
|----|-------------|----------|----------|
| FR-4.1 | System MUST offer three remediation options: Remediation Story, Debt Epic, Add to Sprint | Critical | Yes |
| FR-4.2 | "Remediation Story" option MUST create new story linked to debt entry | High | Yes |
| FR-4.3 | "Debt Epic" option MUST add debt to existing or new debt-specific epic | High | Yes |
| FR-4.4 | "Add to Sprint" option MUST add debt resolution to current sprint backlog | High | Yes |
| FR-4.5 | System MUST update debt entry with selected remediation path | High | Yes |
| FR-4.6 | System MUST support "None - track only" option for monitoring without action | Medium | Yes |
| FR-4.7 | Workflow MUST be skippable (user can defer decision) | Medium | Yes |

#### 2.4.3 Next Steps Interface

```markdown
## Technical Debt Added: DEBT-047

Entry successfully added to Technical Debt Register.

**What would you like to do next?**

1. **Create Remediation Story** (Recommended for Critical/High severity)
   - Creates STORY-XXX: "Resolve DEBT-047: [Title]"
   - Links story to debt entry for tracking
   - Adds story to backlog with appropriate priority

2. **Add to Technical Debt Epic**
   - Adds debt item to EPIC-XXX: "Technical Debt Reduction"
   - Groups related debt for sprint planning
   - Creates epic if none exists

3. **Add to Current Sprint**
   - Adds debt resolution work to Sprint-X
   - Immediate remediation (blocks other work)
   - Best for Critical severity blocking issues

4. **Track Only**
   - No immediate action
   - Debt tracked in register for future planning
   - Review during next sprint planning

Select an option [1-4]:
```

#### 2.4.4 Skill Architecture

**New Skill:** `.claude/skills/devforgeai-debt-workflow/SKILL.md`

```yaml
---
name: devforgeai-debt-workflow
description: Guided workflow for technical debt remediation decisions. Terminal skill - does not invoke other skills to prevent circular dependencies.
tools: [Read, Write, Edit, Glob, Grep, AskUserQuestion]
model: claude-opus-4-6
---
```

**Critical Design Constraint:** This skill is a TERMINAL skill - it MUST NOT invoke other skills (devforgeai-story-creation, devforgeai-orchestration) to prevent circular dependency chains. All story/epic creation is done via direct file operations.

#### 2.4.5 Acceptance Criteria

```xml
<acceptance_criteria id="AC1">
  <given>Debt entry DEBT-XXX was just added to register</given>
  <when>Next Steps workflow triggers</when>
  <then>User is presented with four remediation options</then>
</acceptance_criteria>

<acceptance_criteria id="AC2">
  <given>User selects "Create Remediation Story"</given>
  <when>Workflow processes selection</when>
  <then>New story is created with debt linkage and added to backlog</then>
</acceptance_criteria>

<acceptance_criteria id="AC3">
  <given>User selects "Add to Technical Debt Epic"</given>
  <when>Workflow processes selection</when>
  <then>Debt is linked to epic (existing or newly created)</then>
</acceptance_criteria>

<acceptance_criteria id="AC4">
  <given>User selects "Add to Current Sprint"</given>
  <when>Workflow processes selection</when>
  <then>Debt resolution work is added to current sprint backlog</then>
</acceptance_criteria>

<acceptance_criteria id="AC5">
  <given>User selects "Track Only"</given>
  <when>Workflow processes selection</when>
  <then>Debt status remains "Open" with no follow-up action created</then>
</acceptance_criteria>
```

---

### 2.5 F5: Debt Compounding Prevention - Dev Pre-flight

**Priority:** High
**Complexity:** Low (3 points)
**Sprint Target:** Sprint 2

#### 2.5.1 Overview

Prevent debt compounding by blocking `/dev` workflow if the target story references unresolved technical debt. This is implemented as a pre-flight check in Phase 01 of devforgeai-development skill.

#### 2.5.2 Functional Requirements

| ID | Requirement | Priority | Testable |
|----|-------------|----------|----------|
| FR-5.1 | Pre-flight MUST check technical-debt-register.md for entries matching story ID | Critical | Yes |
| FR-5.2 | Pre-flight MUST check for entries where follow_up field references story ID | High | Yes |
| FR-5.3 | If matching debt found with status "Open", workflow MUST display warning | Critical | Yes |
| FR-5.4 | User MUST acknowledge debt before proceeding (explicit consent) | Critical | Yes |
| FR-5.5 | User MAY choose to resolve debt first (redirect to remediation) | High | Yes |
| FR-5.6 | Pre-flight check MUST use lazy loading (Grep patterns) for performance | Medium | Yes |
| FR-5.7 | Pre-flight check MUST complete in <2 seconds | Medium | Yes |

#### 2.5.3 Pre-flight Check Logic

```python
# Pseudocode for pre-flight debt check
def check_story_debt(story_id: str) -> DebtCheckResult:
    # Lazy load: Use Grep instead of parsing entire register
    direct_matches = Grep(
        pattern=f"story_origin: {story_id}",
        path="devforgeai/technical-debt-register.md"
    )

    followup_matches = Grep(
        pattern=f"follow_up:.*{story_id}",
        path="devforgeai/technical-debt-register.md"
    )

    if direct_matches or followup_matches:
        # Parse only matching entries (not full register)
        debt_entries = parse_matched_entries(direct_matches + followup_matches)
        open_entries = [e for e in debt_entries if e.status == "Open"]

        if open_entries:
            return DebtCheckResult(
                blocked=True,
                entries=open_entries,
                message=f"Found {len(open_entries)} unresolved debt entries"
            )

    return DebtCheckResult(blocked=False)
```

#### 2.5.4 User Consent Interface

```markdown
## Debt Compounding Warning

**STORY-XXX** has unresolved technical debt that may compound:

| Debt ID | Title | Severity | Created |
|---------|-------|----------|---------|
| DEBT-012 | Missing validation in UserService | High | 2026-01-10 |
| DEBT-015 | Coverage gap in OrderController | Critical | 2026-01-15 |

**Proceeding without resolving this debt may:**
- Increase overall debt burden
- Make future remediation more complex
- Violate debt compounding prevention policy

**Options:**
1. **Resolve debt first** - Opens debt remediation workflow
2. **Acknowledge and proceed** - Continue with explicit consent
3. **Cancel** - Abort /dev workflow

Select an option [1-3]:
```

#### 2.5.5 Acceptance Criteria

```xml
<acceptance_criteria id="AC1">
  <given>Technical debt register has open entry for STORY-XXX</given>
  <when>/dev STORY-XXX is executed</when>
  <then>Pre-flight displays debt warning and requires user acknowledgment</then>
</acceptance_criteria>

<acceptance_criteria id="AC2">
  <given>User selects "Resolve debt first"</given>
  <when>Selection is processed</when>
  <then>Debt remediation workflow is triggered and /dev pauses</then>
</acceptance_criteria>

<acceptance_criteria id="AC3">
  <given>User selects "Acknowledge and proceed"</given>
  <when>Selection is processed</when>
  <then>/dev workflow continues with debt acknowledgment logged</then>
</acceptance_criteria>

<acceptance_criteria id="AC4">
  <given>No debt entries exist for story</given>
  <when>Pre-flight check runs</when>
  <then>Check completes in <2 seconds with no warning displayed</then>
</acceptance_criteria>
```

---

### 2.6 F6: Debt Compounding Prevention - Story Creation

**Priority:** Medium
**Complexity:** Low (2 points)
**Sprint Target:** Sprint 2

#### 2.6.1 Overview

Warn during story creation if related technical debt exists for the feature area or parent epic. This is a non-blocking warning (unlike F5) to maintain story creation velocity while increasing debt awareness.

#### 2.6.2 Functional Requirements

| ID | Requirement | Priority | Testable |
|----|-------------|----------|----------|
| FR-6.1 | Story creation MUST check for debt entries related to parent epic | High | Yes |
| FR-6.2 | Story creation MUST check for debt entries with matching tags | Medium | Yes |
| FR-6.3 | Warning MUST be informational (non-blocking) | Critical | Yes |
| FR-6.4 | Warning MUST display debt summary with option to view details | High | Yes |
| FR-6.5 | User MAY link new story to existing debt for tracking | Medium | Yes |
| FR-6.6 | Check MUST complete in <1 second (optimized for story creation flow) | Medium | Yes |

#### 2.6.3 Warning Interface

```markdown
## Related Technical Debt Detected

Stories in **EPIC-005** have accumulated technical debt:

| Debt ID | Title | Severity | Stories Affected |
|---------|-------|----------|------------------|
| DEBT-008 | Authentication refactor needed | High | STORY-015, STORY-018 |

**Note:** This is informational only. Story creation will proceed.

**Options:**
- [ ] Link this story to DEBT-008 for tracking
- [ ] View debt details
- [ ] Continue without linking

[Continue] [View Details]
```

#### 2.6.4 Acceptance Criteria

```xml
<acceptance_criteria id="AC1">
  <given>Parent epic EPIC-XXX has related debt entries</given>
  <when>Story is created under that epic</when>
  <then>Informational warning displays debt summary</then>
</acceptance_criteria>

<acceptance_criteria id="AC2">
  <given>Debt warning is displayed</given>
  <when>User chooses to continue</when>
  <then>Story creation proceeds normally without blocking</then>
</acceptance_criteria>

<acceptance_criteria id="AC3">
  <given>User opts to link story to debt</given>
  <when>Story is created</when>
  <then>Debt entry's cross_references.remediation_story field is updated with new story ID</then>
</acceptance_criteria>

<acceptance_criteria id="AC4">
  <given>No related debt exists for epic</given>
  <when>Story creation runs</when>
  <then>No warning displayed and creation completes in <1 second</then>
</acceptance_criteria>
```

---

## 3. Non-Functional Requirements

### 3.1 Performance Requirements

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-P1 | Debt register schema validation | <500ms for register up to 100 entries | High |
| NFR-P2 | Pre-flight debt check (F5) | <2 seconds end-to-end | Critical |
| NFR-P3 | Story creation debt warning (F6) | <1 second end-to-end | High |
| NFR-P4 | AC verification command (F3) | <20K tokens total | High |
| NFR-P5 | QA-to-debt bridge prompt | <3 seconds to display | Medium |
| NFR-P6 | Register update operation | <1 second for append | Medium |

### 3.2 Scalability Requirements

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-S1 | Register capacity | Support up to 500 debt entries | High |
| NFR-S2 | Concurrent access | Handle 3 parallel workflows accessing register | Medium |
| NFR-S3 | Entry growth | No performance degradation up to 100 open entries | High |

### 3.3 Reliability Requirements

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-R1 | Register integrity | Atomic updates (no partial writes) | Critical |
| NFR-R2 | Schema backward compatibility | v1.0 entries readable by v2.0 parser | High |
| NFR-R3 | Error recovery | Graceful degradation if register corrupted | High |
| NFR-R4 | Validation resilience | Continue workflow if optional checks fail | Medium |

### 3.4 Security Requirements

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-SEC1 | No sensitive data in debt entries | Automated scan for secrets patterns | High |
| NFR-SEC2 | Input validation on user-provided fields | Sanitize before register write | High |
| NFR-SEC3 | File path traversal prevention | Validate all file paths | High |

### 3.5 Token Efficiency Requirements

| ID | Requirement | Metric | Priority |
|----|-------------|--------|----------|
| NFR-T1 | Lazy loading for debt checks | Use Grep patterns, not full register parse | Critical |
| NFR-T2 | Progressive disclosure in workflows | Load reference files on-demand | High |
| NFR-T3 | devforgeai-ac-verification skill | <20K tokens per invocation | High |
| NFR-T4 | devforgeai-debt-workflow skill | <15K tokens per invocation | High |

---

## 4. User Interface/Interaction Requirements

### 4.1 Command Interface

| Command | Arguments | Description |
|---------|-----------|-------------|
| `/verify-ac` | `STORY-XXX` | Standalone AC verification |
| `/qa` | `STORY-XXX --verify-ac` | AC verification via QA command flag |
| `/dev` | `STORY-XXX` | Enhanced with debt pre-flight check |
| `/create-story` | `[description]` | Enhanced with debt awareness warning |

### 4.2 Prompt Patterns

All user prompts MUST follow the AskUserQuestion pattern with:

- Clear header explaining context
- Numbered options with descriptions
- Default option marked (if applicable)
- Cancel/skip option available
- Timeout handling (default after 60 seconds)

### 4.3 Report Formats

**AC Verification Report (JSON):**
```json
{
  "story_id": "STORY-XXX",
  "timestamp": "2026-01-19T12:00:00Z",
  "verifier": "ac-compliance-verifier",
  "results": {
    "total": 5,
    "passed": 4,
    "failed": 1,
    "skipped": 0
  },
  "details": [
    {
      "ac_id": "AC1",
      "status": "PASS",
      "evidence": {...}
    }
  ],
  "overall_status": "PARTIAL"
}
```

**Debt Entry (v2.0 YAML):**
```yaml
- id: "DEBT-047"
  story_origin: "STORY-XXX"
  title: "Coverage gap in OrderService"
  type: "QA Failure"
  severity: "Critical"
  status: "Open"
  created_date: "2026-01-19"
  resolution_target: "Sprint-2"
  estimated_effort: "3 points"
  justification: "Coverage at 82%, required 95%"
  cross_references:
    source_ac: "AC#2"
    remediation_story: "STORY-YYY"
    epic: null
    adr: null
    blocker_condition: null
  tags: ["coverage", "order-service"]
```

---

## 5. Data Requirements

### 5.1 Technical Debt Register v2.0 Schema

**Location:** `devforgeai/technical-debt-register.md`

**Version Header (Required):**
```yaml
---
version: "2.0"
schema_version: "2.0"
last_updated: "ISO8601 timestamp"
maintainer: "devforgeai-development skill"
analyzer: "technical-debt-analyzer subagent"
---
```

**Summary Section (Required):**
```yaml
summary:
  total_open: integer >= 0
  total_in_progress: integer >= 0
  total_resolved: integer >= 0
  last_analyzed: ISO8601 timestamp | null
  debt_by_type:
    story_split: integer >= 0
    scope_change: integer >= 0
    external_blocker: integer >= 0
    qa_failure: integer >= 0
  critical_issues:
    circular_deferrals: integer >= 0
    stale_debt_90days: integer >= 0
```

**Entry Schema (Per Debt Item):**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `id` | String | Yes | Pattern: `DEBT-NNN` |
| `story_origin` | String | Yes | Pattern: `STORY-NNN` |
| `title` | String | Yes | 5-100 characters |
| `type` | Enum | Yes | Story Split, Scope Change, External Blocker, QA Failure |
| `severity` | Enum | Yes | Critical, High, Medium, Low |
| `status` | Enum | Yes | Open, In Progress, Resolved |
| `created_date` | Date | Yes | Format: YYYY-MM-DD |
| `resolution_target` | String | Yes | Sprint-N, YYYY-MM-DD, or condition |
| `estimated_effort` | String | No | Pattern: `N points` or `N hours` |
| `justification` | String | Yes | 10-500 characters |
| `cross_references` | Object | No | Structured linkage object (see below) |
| `cross_references.source_ac` | String | No | AC#N format - which AC was violated |
| `cross_references.remediation_story` | String | No | STORY-NNN - story created to fix debt |
| `cross_references.epic` | String | No | EPIC-NNN - debt epic if grouped |
| `cross_references.adr` | String | No | ADR-NNN - architectural decision |
| `cross_references.blocker_condition` | String | No | External blocker condition |
| `tags` | Array | No | List of lowercase strings |
| `resolved_date` | Date | Conditional | Required if status=Resolved |
| `resolution_story` | String | Conditional | STORY-NNN if resolved via story |

### 5.2 Data Validation Rules

| Rule | Validation | Error Handling |
|------|------------|----------------|
| DR-1 | id must be unique within register | Reject duplicate, suggest next ID |
| DR-2 | story_origin must reference existing story | Warn if story file not found |
| DR-3 | severity must match type defaults (overridable) | Display default, allow override |
| DR-4 | resolution_target must be future date or valid sprint | Reject past dates |
| DR-5 | cross_references.remediation_story must reference valid story if provided | Warn if story file not found |
| DR-6 | cross_references.epic must reference valid epic if provided | Warn if epic file not found |
| DR-7 | cross_references.adr must reference valid ADR if provided | Warn if ADR file not found |
| DR-8 | cross_references.source_ac must match AC#N pattern if provided | Reject invalid format |

### 5.3 Cross-References Object

The `cross_references` object enables rich querying and bidirectional traceability:

**Structure:**
```yaml
cross_references:
  source_ac: "AC#N"              # Which AC was violated (enables AC→Debt tracing)
  remediation_story: "STORY-YYY" # Story created to fix (enables Debt→Story tracing)
  epic: "EPIC-XXX"               # Debt epic grouping (enables Epic→Debt tracing)
  adr: "ADR-XXX"                 # Architectural decision (enables ADR→Debt tracing)
  blocker_condition: "string"    # External blocker description (for external blockers)
```

**Cross-Session Query Patterns:**

```bash
# Find all debt linked to a specific AC
Grep(pattern="source_ac: \"AC#2\"", path="devforgeai/technical-debt-register.md")

# Find debt with remediation stories assigned
Grep(pattern="remediation_story: \"STORY-", path="devforgeai/technical-debt-register.md")

# Find unassigned debt (no remediation story)
Grep(pattern="remediation_story: null", path="devforgeai/technical-debt-register.md")

# Find debt grouped in a specific epic
Grep(pattern="epic: \"EPIC-047\"", path="devforgeai/technical-debt-register.md")

# Find debt with ADR references
Grep(pattern="adr: \"ADR-", path="devforgeai/technical-debt-register.md")

# Find external blocker debt
Grep(pattern="blocker_condition:", path="devforgeai/technical-debt-register.md")
```

**Bidirectional Traceability:**

| From | To | Query |
|------|----|-------|
| Story → Debt | Find debt created from story | `story_origin: "STORY-XXX"` |
| Debt → Story | Find remediation story | `remediation_story: "STORY-YYY"` |
| AC → Debt | Find debt from AC violation | `source_ac: "AC#N"` |
| Epic → Debt | Find debt in epic | `epic: "EPIC-XXX"` |
| ADR → Debt | Find debt with ADR | `adr: "ADR-XXX"` |

---

### 5.4 Migration Requirements (v1.0 → v2.0)

**Field Mapping:**

| v1.0 Field | v2.0 Mapping |
|------------|--------------|
| Story ID header | `story_origin` |
| Deferred item title | `title` |
| Date Deferred | `created_date` |
| Type | `type` (normalize to enum) |
| Justification | `justification` |
| Follow-up | `cross_references.remediation_story` or `cross_references.blocker_condition` |
| Priority | `severity` |
| Status | `status` |
| Resolution Target | `resolution_target` |
| Estimated Effort | `estimated_effort` |

**Migration Script Requirements:**
1. Backup v1.0 register before migration
2. Parse v1.0 Markdown entries
3. Generate unique `id` for each entry (DEBT-001, DEBT-002, ...)
4. Validate all required fields present
5. Write v2.0 format with preserved data
6. Verify migration integrity (entry count match)

---

## 6. Integration Requirements

### 6.1 Skill Integration

| New Skill | Invokes | Invoked By |
|-----------|---------|------------|
| devforgeai-ac-verification | ac-compliance-verifier | /verify-ac command, /qa command |
| devforgeai-debt-workflow | None (terminal) | devforgeai-qa (via bridge), devforgeai-development |

### 6.2 Subagent Integration

| Subagent | Used By | Purpose |
|----------|---------|---------|
| ac-compliance-verifier | devforgeai-ac-verification, devforgeai-qa | Fresh-context AC verification |
| technical-debt-analyzer | devforgeai-orchestration | Debt trend analysis |

### 6.3 Command Integration

| Command | Modifications |
|---------|---------------|
| `/qa` | Add `--verify-ac` flag routing to devforgeai-ac-verification |
| `/dev` | Add pre-flight debt check (F5) in Phase 01 |
| `/create-story` | Add debt awareness check (F6) in Phase 1 |

### 6.4 File Modifications

| File | Modification Type | Feature |
|------|------------------|---------|
| `devforgeai/technical-debt-register.md` | Format migration | F1 |
| `.claude/commands/verify-ac.md` | New file | F3 |
| `.claude/skills/devforgeai-ac-verification/SKILL.md` | New file | F3 |
| `.claude/skills/devforgeai-debt-workflow/SKILL.md` | New file | F4 |
| `.claude/skills/devforgeai-qa/SKILL.md` | Modify (add bridge) | F2 |
| `.claude/skills/devforgeai-qa/references/report-generation.md` | Modify | F2 |
| `.claude/commands/qa.md` | Modify (add flag) | F3 |
| `.claude/skills/devforgeai-development/SKILL.md` | Modify (add pre-flight) | F5 |
| `.claude/skills/devforgeai-development/phases/phase-01-preflight.md` | Modify | F5 |
| `.claude/skills/devforgeai-story-creation/SKILL.md` | Modify (add warning) | F6 |
| `.claude/skills/devforgeai-story-creation/references/story-discovery.md` | Modify | F6 |

### 6.5 Circular Dependency Prevention

**CRITICAL:** devforgeai-debt-workflow is designed as a TERMINAL skill:

```
devforgeai-qa
  -> devforgeai-debt-workflow (terminal, no further skill invocations)

devforgeai-development
  -> devforgeai-debt-workflow (terminal)

PROHIBITED:
devforgeai-debt-workflow -> devforgeai-story-creation (would create circle)
devforgeai-debt-workflow -> devforgeai-orchestration (would create circle)
```

Story/epic creation within debt-workflow uses direct file operations (Write, Edit) not skill invocation.

---

## 7. Acceptance Criteria Summary

### 7.1 Feature-Level AC Matrix

| Feature | Total ACs | Critical | High | Medium |
|---------|-----------|----------|------|--------|
| F1: Register v2.0 | 3 | 2 | 1 | 0 |
| F2: QA-to-Debt Bridge | 4 | 2 | 2 | 0 |
| F3: /verify-ac Command | 4 | 3 | 1 | 0 |
| F4: Next Steps Workflow | 5 | 1 | 3 | 1 |
| F5: Dev Pre-flight | 4 | 2 | 1 | 1 |
| F6: Story Creation Warning | 4 | 1 | 2 | 1 |
| **Total** | **24** | **11** | **10** | **3** |

### 7.2 Quality Gate Alignment

| Quality Gate | EPIC-047 Impact |
|--------------|-----------------|
| Gate 1: Context Validation | No change (context files not modified) |
| Gate 2: Test Passing | Pre-flight debt check may block progression |
| Gate 3: QA Approval | Debt bridge may create entries during QA |
| Gate 4: Release Readiness | Debt status included in release checklist |

---

## 8. Technical Risks and Mitigations

### 8.1 Risk Registry

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R1 | QA skill integration complexity | High | High | Extract bridge logic to reference file, not inline |
| R2 | Circular dependency in debt-workflow | Medium | Critical | Design as terminal skill, no skill invocations |
| R3 | Pre-flight performance regression | Medium | Medium | Lazy loading with Grep patterns |
| R4 | Register format backward compatibility | Low | High | Version header, migration script, schema validation |
| R5 | User prompt fatigue from debt warnings | Medium | Medium | Make warnings informational (F6), configurable thresholds |

### 8.2 Technical Debt Considerations

This epic aims to reduce technical debt but introduces complexity:

| Added Complexity | Justification |
|------------------|---------------|
| New skill (ac-verification) | Enables standalone verification, reduces coupling |
| New skill (debt-workflow) | Centralizes debt remediation logic |
| Register schema v2.0 | Machine-parseability enables automation |
| Pre-flight checks | Prevention > remediation (reduces future debt) |

---

## 9. ADR Requirement

**ADR-012: Technical Debt Register v2.0 Format**

**Status:** Required before F1 implementation
**Decision:** Adopt hybrid YAML+Markdown format for technical debt register

**Key Decisions:**
1. YAML frontmatter for version and summary
2. YAML blocks for each debt entry (machine-parseable)
3. Optional Markdown sections for human-readable details
4. Backward-compatible migration path from v1.0
5. Schema validation on all read/write operations

---

## 10. Glossary

| Term | Definition |
|------|------------|
| **Technical Debt** | Deferred work that adds complexity and must be addressed in future sprints |
| **Debt Compounding** | Adding new features on top of unresolved technical debt, increasing remediation cost |
| **Fresh-Context Verification** | AC verification technique where verifier has no prior knowledge of implementation |
| **Terminal Skill** | A skill that does not invoke other skills, preventing circular dependencies |
| **Debt Register** | Central tracking document for all technical debt entries |
| **Debt Entry** | Single item of technical debt with metadata and resolution tracking |
| **Remediation Story** | Story created specifically to address a technical debt entry |
| **Debt Epic** | Epic grouping multiple debt entries for coordinated remediation |
| **Pre-flight Check** | Validation that runs before main workflow begins |
| **QA-to-Debt Bridge** | Automated pathway from QA failure to debt register entry |

---

## 11. References

**Framework Documentation:**
- `devforgeai/technical-debt-register.md` - Current register (v1.0)
- `.claude/skills/devforgeai-qa/SKILL.md` - QA skill (integration target)
- `.claude/skills/devforgeai-development/SKILL.md` - Dev skill (pre-flight target)
- `.claude/agents/ac-compliance-verifier.md` - AC verification subagent
- `devforgeai/specs/adrs/ADR-010-strict-coverage-threshold-enforcement.md` - Coverage thresholds

**Related Epics:**
- EPIC-046: AC Compliance Verification System (prerequisite for XML AC format)
- EPIC-010: Parallel Story Development (depends_on field usage)

**Patterns and Standards:**
- `devforgeai/specs/context/coding-standards.md` - XML AC schema
- `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md` - Story template v2.6

---

**Document Status:** Draft
**Review Required:** Framework Maintainers
**Approval Required:** Before Sprint 1 planning
